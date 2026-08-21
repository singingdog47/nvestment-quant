from __future__ import annotations
import json
from pathlib import Path
import pandas as pd, yaml
from .common import ensure_dir, now_iso, save_json
from .market_data import fetch_market_history
from .fred import fetch_fred
from .breadth import compute_breadth
from .jpx import fetch_jpx_sources
from .cftc import fetch_cftc
from .scoring import score_regime, regime_label

CFG=yaml.safe_load(Path("config/market_regime_v1_5.yml").read_text(encoding="utf-8"))
OUT=ensure_dir(CFG["outputs"]["directory"])

def _write_frame(df,path):
    if df is None: df=pd.DataFrame()
    df.to_csv(path,index=False,encoding="utf-8-sig")

def main():
    fetched=now_iso(); health=[]
    market,hist,h=fetch_market_history(CFG["market_symbols"],CFG.get("market_history_period","1y"),CFG.get("market_history_interval","1d")); health+=h
    _write_frame(market,OUT/"market_dashboard_latest.csv")
    fred,h=fetch_fred(CFG.get("fred_series",{})); health+=h; _write_frame(fred,OUT/"fred_latest.csv")
    breadth,h=compute_breadth(CFG.get("breadth",{}).get("source_candidates",[]),CFG.get("breadth",{}).get("min_universe",100)); health+=h; save_json(OUT/"breadth_latest.json",breadth)
    jpx_frames,jpx_index,jpx_h=fetch_jpx_sources(CFG.get("jpx_sources",{})); health+=jpx_h; _write_frame(jpx_index,OUT/"jpx_source_index_latest.csv")
    for name,df in jpx_frames.items(): _write_frame(df,OUT/f"jpx_{name}_latest.csv")
    if CFG.get("cftc",{}).get("enabled",True):
        cftc,h,cftc_url=fetch_cftc(CFG.get("cftc",{}).get("contracts",[])); health+=h; _write_frame(cftc,OUT/"cftc_latest.csv")
    else: cftc=pd.DataFrame(); cftc_url=""
    sc=CFG["scoring"]; components,evidence,score,confidence=score_regime(market,fred,breadth,jpx_h,cftc,sc["weights"])
    label=regime_label(score,sc["labels"])
    vix=evidence.get("vix"); trend=components.get("trend"); part=components.get("participation"); liq=components.get("liquidity")
    overheated=bool(trend is not None and trend>=75 and part is not None and part>=65 and vix is not None and float(vix)<18)
    stress_flag=bool((components.get("stress") is not None and components.get("stress")<35) or label=="RISK_OFF")
    thin_liquidity=bool(liq is not None and liq<35)
    flags=[x for x,b in (("OVERHEATED",overheated),("STRESS",stress_flag),("THIN_LIQUIDITY",thin_liquidity)) if b]
    critical_ok=sum(1 for name in ("JP_NIKKEI","US_SP500","VIX") if not market.empty and (market["series"]==name).any())
    actionable=bool(score is not None and confidence>=0.60 and critical_ok>=2)
    regime={
      "version":"1.5.0","generated_at":fetched,"regime_label":label,"regime_score":score,"confidence":confidence,
      "actionable":actionable,"overheated_flag":overheated,"stress_flag":stress_flag,"thin_liquidity_flag":thin_liquidity,"regime_flags":flags,
      "components":components,"evidence":evidence,
      "rule":"Regime is context, not a trade signal. If actionable=false, do not infer missing market facts.",
      "source_priority":"official/public primary > internal v1.3 data > free secondary market feed > model inference"
    }
    save_json(OUT/"market_regime_latest.json",regime)
    _write_frame(pd.DataFrame(health),OUT/"market_source_health_latest.csv")
    hist_path=OUT/"market_regime_history.csv"
    row=pd.DataFrame([{ "generated_at":fetched,"score":score,"label":label,"confidence":confidence,**{f"component_{k}":v for k,v in components.items()} }])
    if hist_path.exists():
        try: old=pd.read_csv(hist_path); row=pd.concat([old,row],ignore_index=True).tail(750)
        except Exception: pass
    _write_frame(row,hist_path)
    md=["# Market Regime v1.5","",f"- Label: **{label}**",f"- Score: **{score}**",f"- Confidence: **{confidence}**",f"- Actionable: **{actionable}**",f"- Flags: {', '.join(flags) if flags else 'none'}","","## Components"]
    for k,v in components.items(): md.append(f"- {k}: {v}")
    md += ["","## Evidence",json.dumps(evidence,ensure_ascii=False,indent=2),"","Regime is context, not an automatic trade signal."]
    (OUT/"market_context_latest.md").write_text("\n".join(md),encoding="utf-8")
    print(json.dumps(regime,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
