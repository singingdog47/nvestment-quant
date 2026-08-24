from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd, yaml

from .common import ensure_dir, now_iso, save_json
from .market_data import fetch_market_history
from .fred import fetch_fred
from .breadth import compute_breadth
from .jpx import fetch_jpx_sources
from .cftc import fetch_cftc
from .coverage import build_data_coverage, normalize_status
from .scoring import score_regime, regime_label
from .treasury_volatility import fetch_treasury_volatility

CFG=yaml.safe_load(Path("config/market_regime_v1_5.yml").read_text(encoding="utf-8"))
OUT=ensure_dir(CFG["outputs"]["directory"])


def _write_frame(df,path):
    if df is None: df=pd.DataFrame()
    df.to_csv(path,index=False,encoding="utf-8-sig")


def _frame_status(df):
    if df is None or df.empty:
        return "missing"
    if "data_status" not in df.columns:
        return "ok"
    statuses={normalize_status(x) for x in df["data_status"].dropna().tolist()}
    if not statuses:
        return "partial"
    if statuses == {"ok"}:
        return "ok"
    if statuses == {"stale"}:
        return "stale"
    if statuses == {"missing"}:
        return "missing"
    return "partial"


def _health_status(rows):
    statuses=[normalize_status(x.get("status")) for x in rows]
    if not statuses:
        return "missing"
    if all(x == "ok" for x in statuses):
        return "ok"
    if all(x == "stale" for x in statuses):
        return "stale"
    if all(x == "missing" for x in statuses):
        return "missing"
    return "partial"


def _date_jst(timestamp):
    return datetime.fromisoformat(timestamp).astimezone(ZoneInfo("Asia/Tokyo")).date().isoformat()


def main():
    fetched=now_iso(); health=[]
    market,hist,h=fetch_market_history(CFG["market_symbols"],CFG.get("market_history_period","1y"),CFG.get("market_history_interval","1d")); health+=h
    _write_frame(market,OUT/"market_dashboard_latest.csv")
    fred,h=fetch_fred(
        CFG.get("fred_series",{}),
        cache_path=OUT/"fred_latest.csv",
        max_cache_age_days=CFG.get("freshness",{}).get("fred_cache_max_age_days",14),
    ); health+=h; _write_frame(fred,OUT/"fred_latest.csv")
    treasury_cfg=CFG.get("treasury_volatility",{})
    if treasury_cfg.get("enabled",True):
        treasury_vol,treasury_history,treasury_h=fetch_treasury_volatility(
            treasury_cfg,
            cache_path=OUT/"treasury_volatility_latest.json",
        )
        health+=treasury_h
        save_json(OUT/"treasury_volatility_latest.json",treasury_vol)
        treasury_history_path=OUT/"treasury_volatility_history.csv"
        if (treasury_history is None or treasury_history.empty) and treasury_vol.get("data_status")=="stale" and treasury_history_path.exists():
            try:
                treasury_history=pd.read_csv(treasury_history_path)
                treasury_history["data_status"]="stale"
            except Exception:
                treasury_history=pd.DataFrame()
        _write_frame(treasury_history,treasury_history_path)
    else:
        treasury_vol={"name":"UST_YIELD_VOLATILITY_PROXY","data_status":"not_implemented","is_ice_move":False}
        treasury_history=pd.DataFrame()
        treasury_h=[{"source":"USTreasury:daily_treasury_yield_curve","status":"not_implemented","records":0,"fetched_at":fetched,"error":"source disabled by configuration","source_tier":"primary"}]
        health+=treasury_h
        save_json(OUT/"treasury_volatility_latest.json",treasury_vol)
        _write_frame(treasury_history,OUT/"treasury_volatility_history.csv")
    breadth,h=compute_breadth(CFG.get("breadth",{}).get("source_candidates",[]),CFG.get("breadth",{}).get("min_universe",100)); health+=h; save_json(OUT/"breadth_latest.json",breadth)
    jpx_frames,jpx_index,jpx_h=fetch_jpx_sources(CFG.get("jpx_sources",{})); health+=jpx_h; _write_frame(jpx_index,OUT/"jpx_source_index_latest.csv")
    for name,df in jpx_frames.items(): _write_frame(df,OUT/f"jpx_{name}_latest.csv")
    if CFG.get("cftc",{}).get("enabled",True):
        cftc,h,cftc_url=fetch_cftc(CFG.get("cftc",{}).get("contracts",[])); cftc_health=h; health+=h; _write_frame(cftc,OUT/"cftc_latest.csv")
    else:
        cftc=pd.DataFrame(); cftc_url=""; cftc_health=[{"source":"CFTC:COT","status":"not_implemented","records":0,"fetched_at":fetched,"error":"source disabled by configuration","source_tier":"primary"}]; health+=cftc_health
    sc=CFG["scoring"]; components,evidence,score,confidence=score_regime(market,fred,breadth,jpx_h,cftc,sc["weights"],treasury_volatility=treasury_vol)
    label=regime_label(score,sc["labels"])
    vix=evidence.get("vix"); trend=components.get("trend"); part=components.get("participation"); liq=components.get("liquidity")
    overheated=bool(trend is not None and trend>=75 and part is not None and part>=65 and vix is not None and float(vix)<18)
    stress_flag=bool((components.get("stress") is not None and components.get("stress")<35) or label=="RISK_OFF")
    thin_liquidity=bool(liq is not None and liq<35)
    treasury_percentile=evidence.get("treasury_volatility_percentile_rank")
    treasury_shock=bool(
        treasury_vol.get("data_status")=="ok"
        and treasury_percentile is not None
        and float(treasury_percentile)>=float(treasury_cfg.get("shock_percentile",0.90))
    )
    flags=[x for x,b in (("OVERHEATED",overheated),("STRESS",stress_flag),("THIN_LIQUIDITY",thin_liquidity),("TREASURY_VOLATILITY_SHOCK",treasury_shock)) if b]
    critical_names=("JP_NIKKEI","US_SP500","VIX")
    critical_ok=sum(1 for name in critical_names if not market.empty and (market["series"]==name).any())
    min_confidence=float(sc.get("actionable_min_confidence",0.60))
    missing_core_context=[name for name in ("HY_OAS","IG_OAS","NFCI") if evidence.get(name.lower()) is None]
    actionability_reasons=[]
    if score is None: actionability_reasons.append("regime_score_missing")
    if confidence<min_confidence: actionability_reasons.append("confidence_below_threshold")
    if critical_ok<2: actionability_reasons.append("critical_market_series_missing")
    if missing_core_context: actionability_reasons.append("core_credit_or_financial_conditions_missing")
    actionable=bool(score is not None and confidence>=min_confidence and critical_ok>=2)
    data_status="ok" if actionable else ("partial" if score is not None else "missing")
    engine_version=str(CFG.get("version","1.5.2"))
    regime={
      "version":engine_version,"engine_version":engine_version,"generated_at":fetched,"generated_at_utc":fetched,"date_jst":_date_jst(fetched),"data_status":data_status,
      "regime_label":label,"regime_score":score,"confidence":confidence,
      "actionable":actionable,"actionability":{"minimum_confidence":min_confidence,"critical_market_series_available":critical_ok,"critical_market_series_expected":len(critical_names),"missing_core_context":missing_core_context,"reasons":actionability_reasons},
      "overheated_flag":overheated,"stress_flag":stress_flag,"thin_liquidity_flag":thin_liquidity,"treasury_volatility_shock_flag":treasury_shock,"regime_flags":flags,
      "components":components,"evidence":evidence,
      "rule":"Regime is context, not a trade signal. If actionable=false, do not infer missing market facts.",
      "source_priority":"official/public primary > internal v1.3 data > free secondary market feed > model inference"
    }
    save_json(OUT/"market_regime_latest.json",regime)
    _write_frame(pd.DataFrame(health),OUT/"market_source_health_latest.csv")
    hist_path=OUT/"market_regime_history.csv"
    row=pd.DataFrame([{ "generated_at":fetched,"score":score,"label":label,"confidence":confidence,"actionable":actionable,"data_status":data_status,**{f"component_{k}":v for k,v in components.items()} }])
    if hist_path.exists():
        try: old=pd.read_csv(hist_path); row=pd.concat([old,row],ignore_index=True).tail(750)
        except Exception: pass
    _write_frame(row,hist_path)
    md=["# Market Regime v1.5","",f"- Label: **{label}**",f"- Score: **{score}**",f"- Confidence: **{confidence}**",f"- Actionable: **{actionable}**",f"- Data status: **{data_status}**",f"- Flags: {', '.join(flags) if flags else 'none'}","","## Components"]
    for k,v in components.items(): md.append(f"- {k}: {v}")
    md += ["","## Evidence",json.dumps(evidence,ensure_ascii=False,indent=2),"","Regime is context, not an automatic trade signal."]
    (OUT/"market_context_latest.md").write_text("\n".join(md),encoding="utf-8")

    expected_sources=[]
    for logical_name,ticker in CFG.get("market_symbols",{}).items():
        expected_sources.append({"source":f"yfinance:{ticker}","logical_name":logical_name,"required":logical_name in critical_names})
    for logical_name,sid in CFG.get("fred_series",{}).items():
        expected_sources.append({"source":f"FRED:{sid}","logical_name":logical_name,"required":logical_name in ("HY_OAS","IG_OAS","NFCI")})
    expected_sources.append({"source":"USTreasury:daily_treasury_yield_curve","logical_name":"UST_YIELD_VOLATILITY_PROXY","required":False})
    expected_sources.append({"source":"v1.3 breadth adapter","logical_name":"BREADTH","required":True})
    for name in CFG.get("jpx_sources",{}):
        expected_sources.append({"source":f"JPX:{name}","logical_name":name,"required":False})
    expected_sources.append({"source":"CFTC:COT","logical_name":"CFTC_POSITIONING","required":False})
    file_rows=[
        {"path":str(OUT/"market_dashboard_latest.csv"),"status":_frame_status(market),"records":len(market)},
        {"path":str(OUT/"fred_latest.csv"),"status":_frame_status(fred),"records":len(fred)},
        {"path":str(OUT/"treasury_volatility_latest.json"),"status":normalize_status(treasury_vol.get("data_status")),"records":1 if treasury_vol.get("data_status") in ("ok","stale") else 0},
        {"path":str(OUT/"treasury_volatility_history.csv"),"status":_frame_status(treasury_history) if treasury_history is not None and not treasury_history.empty else "missing","records":len(treasury_history) if treasury_history is not None else 0},
        {"path":str(OUT/"breadth_latest.json"),"status":normalize_status(breadth.get("status")),"records":breadth.get("n",0)},
        {"path":str(OUT/"jpx_source_index_latest.csv"),"status":_health_status(jpx_h),"records":len(jpx_index)},
        {"path":str(OUT/"cftc_latest.csv"),"status":_health_status(cftc_health),"records":len(cftc)},
        {"path":str(OUT/"market_regime_latest.json"),"status":data_status,"records":1},
        {"path":str(OUT/"market_regime_history.csv"),"status":"ok","records":len(row)},
        {"path":str(OUT/"market_context_latest.md"),"status":data_status,"records":1},
    ]
    coverage=build_data_coverage(
        health,
        generated_at=fetched,
        expected_sources=expected_sources,
        not_implemented=CFG.get("coverage",{}).get("not_implemented",[]),
        files=file_rows,
    )
    save_json(CFG.get("coverage",{}).get("manifest_path","data/data_coverage_latest.json"),coverage)
    print(json.dumps(regime,ensure_ascii=False,indent=2))


if __name__=="__main__": main()
