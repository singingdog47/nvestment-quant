"""Independent AI-efficiency / potential-acquisition paper cohort.

Not a takeover probability model. Screens only observable public fundamentals,
retains candidate *and rejected* observations, and uses next-session verified
opens for virtual trades. No broker APIs or real money; no changing v1/v2 state.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from shadow_swing_v2 import verified_daily_bar, number

JST = ZoneInfo("Asia/Tokyo")
ROOT = Path("data")
OUT = ROOT / "ai_ma_shadow"
CONFIG = Path("config/ai_ma_shadow_v1.json")


def load(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return default


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def csv_rows(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def is_same_jst_date(timestamp, session):
    if not timestamp:
        return False
    try:
        dt = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        return dt.tzinfo is not None and dt.astimezone(JST).date() == session
    except (ValueError, TypeError):
        return False


def screen_candidates(rows, cfg, session):
    """Select low valuation + underlying operating viability, NOT 'likely TOB'."""
    accepted, rejected = [], []
    g = cfg["gate"]
    for r in rows:
        symbol = r.get("ticker", "")
        if r.get("market") != "JP" or not symbol.endswith(".T"):
            continue
        cap = number(r.get("market_cap"))
        pe = number(r.get("pe"))
        pb = number(r.get("pb"))
        roe = number(r.get("roe"))
        margin = number(r.get("operating_margin"))
        turnover = number(r.get("avg_turnover_30d"))
        candidate = {
            "symbol": symbol, "name": r.get("name"), "signal_date": session.isoformat(),
            "observable": {"market_cap": cap, "pe": pe, "pb": pb, "roe_pct": roe,
                           "operating_margin_pct": margin, "avg_turnover_jpy": turnover},
            "ai_restructuring_evidence": "UNVERIFIED",
            "ownership_takeover_evidence": "UNVERIFIED",
            "target_event_probability": None, "mna_synergy_estimate": None,
            "investment_thesis": "Undervalued operating company; improvement and M&A are UNPROVEN optionality.",
        }
        fail = []
        if not is_same_jst_date(r.get("data_retrieved_at_utc"), session):
            fail.append("stale_or_undated_screen")
        if str(r.get("eligible", "")).lower() != "true":
            fail.append("not_screening_eligible")
        if any(x is None for x in (cap, pe, pb, roe, margin, turnover)):
            fail.append("missing_valuation_or_quality")
        else:
            if not g["market_cap_min"] <= cap <= g["market_cap_max"]:
                fail.append("market_cap_outside_range")
            if not 0 < pe <= g["pe_max"] or not 0 < pb <= g["pb_max"]:
                fail.append("not_cheap")
            if roe < g["roe_min"] or margin < g["operating_margin_min"]:
                fail.append("weak_underlying_economics")
            if turnover < g["turnover_min"]:
                fail.append("illiquid")
        candidate["vetoes"] = fail
        candidate["eligible"] = not fail
        candidate["id"] = hashlib.sha256((session.isoformat()+"|"+symbol+"|ai-ma-v1").encode()).hexdigest()[:18]
        if fail:
            rejected.append(candidate)
        else:
            accepted.append(candidate)
    accepted.sort(key=lambda x:(x["observable"]["pb"],x["observable"]["pe"],x["symbol"]))
    return accepted, rejected


def new_state(cfg):
    initial=cfg["virtual_initial_cash_jpy"]
    return {"version":"1.0.0","cohort":cfg["cohort"],"mode":"SHADOW_ONLY",
            "initial_cash_jpy":initial,"cash_jpy":initial,"positions":{},
            "pending_buys":[],"pending_sells":[],"completed_trades":[],
            "last_run_date":None,"nav_jpy":initial,"peak_nav_jpy":initial,
            "max_drawdown_pct":0.0,"benchmark_start_close":None,
            "baseline_benchmark_nav_jpy":None}


def _add_csv(path, row, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=csv_rows(path)
    date_key=row.get("date")
    data=[r for r in data if r.get("date") != date_key]
    data.append({k:row.get(k) for k in fields})
    with path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def run(as_of=None, root=ROOT, cfg_path=CONFIG, price_loader=verified_daily_bar):
    cfg=load(Path(cfg_path),{})
    if cfg.get("mode") != "SHADOW_ONLY" or not cfg.get("governance",{}).get("real_orders_forbidden"):
        raise ValueError("paper-only governance required")
    day=as_of or datetime.now(JST).date()
    root=Path(root)
    out=root/"ai_ma_shadow"
    state_path=out/"state.json"
    state=load(state_path,None) or new_state(cfg)
    if state.get("cohort")!=cfg["cohort"] or state.get("initial_cash_jpy")!=cfg["virtual_initial_cash_jpy"]:
        raise RuntimeError("cohort mismatch: never reset or top-up an existing virtual ledger")
    if state.get("last_run_date") and day.isoformat() <= state["last_run_date"]:
        return load(out/"latest.json", {"status":"not_updated"})
    if day < date.fromisoformat(cfg["start_date"]):
        return {"status":"before_cohort_start","as_of_date":day.isoformat()}
    if day > date.fromisoformat(cfg["end_date"]):
        return {"status":"cohort_end_reached","as_of_date":day.isoformat()}

    events=[]
    missing=[]
    benchmark_bar=price_loader(cfg["benchmark_symbol"],day)
    benchmark_close=number(benchmark_bar.get("close")) if benchmark_bar else None
    # Mark-to-market and execute previously queued orders ONLY on verified daily OHLC.
    for symbol,holding in list(state["positions"].items()):
        bar=price_loader(symbol,day)
        if bar is None:
            missing.append("missing_holding_bar:"+symbol)
            continue
        holding["last_close"]=bar["close"]
        held_calendar=(day-date.fromisoformat(holding["entry_date"])).days
        if held_calendar >= cfg["risk"]["max_holding_calendar_days"] and symbol not in state["pending_sells"]:
            state["pending_sells"].append(symbol)
            events.append({"event":"TIME_EXIT_QUEUED","symbol":symbol})
    for symbol in list(state["pending_sells"]):
        holding=state["positions"].get(symbol)
        if not holding:
            state["pending_sells"].remove(symbol)
            continue
        # Positions are not closed at the signal-day close. Previous session exit is
        # executed at a verified later open, but never on the same entry session.
        if holding["entry_date"] >= day.isoformat():
            continue
        bar=price_loader(symbol,day)
        if bar is None:
            missing.append("exit_missing_bar:"+symbol)
            continue
        value=bar["open"]*(1-cfg["execution"]["slippage_bps"]/10000)
        amount=round(holding["qty"]*value,2)
        state["cash_jpy"]+=amount
        state["completed_trades"].append({"symbol":symbol,"exit_date":day.isoformat(),
            "entry_date":holding["entry_date"],"entry_price":holding["entry_price"],
            "exit_price":value,"qty":holding["qty"],"pnl_jpy":amount-holding["cost_jpy"]})
        del state["positions"][symbol]
        state["pending_sells"].remove(symbol)
        events.append({"event":"VIRTUAL_SELL","symbol":symbol})
    for order in list(state["pending_buys"]):
        if order["signal_date"] >= day.isoformat():
            continue
        symbol=order["symbol"]
        bar=price_loader(symbol,day)
        if bar is None:
            missing.append("entry_missing_bar:"+symbol)
            continue
        opening=number(bar.get("open"))
        if opening is None or opening<=0:
            missing.append("invalid_entry_bar:"+symbol)
            continue
        if abs(opening/order["signal_price"]-1)*100>cfg["execution"]["max_open_gap_pct"]:
            events.append({"event":"GAP_VETO","symbol":symbol})
            state["pending_buys"].remove(order)
            continue
        fill=opening*(1+cfg["execution"]["slippage_bps"]/10000)
        qty=order["qty"]
        cost=round(fill*qty,2)
        if cost>state["cash_jpy"]:
            events.append({"event":"CASH_VETO","symbol":symbol})
            state["pending_buys"].remove(order)
            continue
        state["positions"][symbol]={"entry_date":day.isoformat(),"entry_price":fill,
            "qty":qty,"cost_jpy":cost,"last_close":bar["close"],"signal_id":order["id"]}
        state["cash_jpy"]-=cost
        state["pending_buys"].remove(order)
        events.append({"event":"VIRTUAL_BUY","symbol":symbol,"qty":qty})

    # Signal-only: public screen after 15:30 JST, no lookahead, no broker info.
    screen=csv_rows(root/"screening_latest.csv")
    if not screen or not is_same_jst_date(screen[0].get("data_retrieved_at_utc"),day):
        accepted,rejected=[],[]
        missing.append("fresh_jp_screen_unavailable")
    else:
        accepted,rejected=screen_candidates(screen,cfg,day)
    current=state["positions"]
    queued={x["symbol"] for x in state["pending_buys"]}
    if len(state["pending_buys"]) < cfg["risk"]["max_new_entries_per_day"]:
        for candidate in accepted:
            if len(current)+len(queued)>=cfg["risk"]["max_positions"]:
                break
            if len(queued)>=cfg["risk"]["max_new_entries_per_day"]:
                break
            symbol=candidate["symbol"]
            if symbol in current or symbol in queued:
                continue
            # No trade without verifiable closing price; scanner "last" is insufficient.
            bar=price_loader(symbol,day)
            if bar is None:
                missing.append("signal_bar_unavailable:"+symbol)
                continue
            price=number(bar.get("close"))
            if price is None or price<=0:
                continue
            # One signal per market session, at most 10% initial NAV per position.
            budget=min(cfg["virtual_initial_cash_jpy"]*cfg["risk"]["max_position_weight"],
                state["cash_jpy"]*0.95)
            lot=cfg["execution"]["lot"]
            qty=int(budget/(lot*price))*lot
            if qty<lot:
                continue
            if qty*price>cfg["risk"]["max_avg_turnover_participation"]*candidate["observable"]["avg_turnover_jpy"]:
                continue
            state["pending_buys"].append({
                "signal_date":day.isoformat(),"symbol":symbol,"qty":qty,
                "signal_price":price,"id":candidate["id"],
                "thesis":"value+operating_quality; AI/M&A unverified and not priced into eligibility",
            })
            queued.add(symbol)
            events.append({"event":"VIRTUAL_BUY_QUEUED_NEXT_OPEN","symbol":symbol})
    mv=sum(h["qty"]*h["last_close"] for h in current.values())
    state["nav_jpy"]=round(state["cash_jpy"]+mv,2)
    state["peak_nav_jpy"]=max(state["peak_nav_jpy"],state["nav_jpy"])
    state["max_drawdown_pct"]=min(state["max_drawdown_pct"],
        100*(state["nav_jpy"]/state["peak_nav_jpy"]-1))
    if benchmark_close:
        if state["benchmark_start_close"] is None:
            state["benchmark_start_close"]=benchmark_close
        state["baseline_benchmark_nav_jpy"]=round(cfg["virtual_initial_cash_jpy"]*benchmark_close/state["benchmark_start_close"],2)
    else:
        missing.append("benchmark_price_unavailable")
    state["last_run_date"]=day.isoformat()
    public_candidates=[{k:x[k] for k in ("id","symbol","name","observable","ai_restructuring_evidence",
                         "ownership_takeover_evidence","target_event_probability","vetoes","eligible")}
                       for x in accepted[:cfg["audit"]["max_candidates"]]]
    result={"version":"1.0.0","as_of_date":day.isoformat(),"cohort":cfg["cohort"],
        "mode":"SHADOW_ONLY","status":"RESEARCH_NOT_VALIDATED",
        "initial_cash_jpy":cfg["virtual_initial_cash_jpy"],"nav_jpy":state["nav_jpy"],
        "benchmark_nav_jpy":state["baseline_benchmark_nav_jpy"],
        "positions_count":len(current),"completed_trades":len(state["completed_trades"]),
        "pending_buys":len(state["pending_buys"]),
        "screened_jp_count":sum(x.get("market")=="JP" for x in screen),
        "qualified_count":len(accepted),"rejected_count":len(rejected),
        "candidates":public_candidates,"data_blockers":sorted(set(missing)),"events":events,
        "hypothesis":{
            "H1":"AI-enabled cost/sales improvements improve future margins; unverified until operating data obtained",
            "H2":"Acquisition/privatization becomes more common among candidates; target probabilities unverified",
            "H3":"Value+AI/M&A enhanced basket outperforms matched value-only and TOPIX after costs; UNTESTED",
        },
        "control_cohorts":["data/shadow_swing","data/shadow_swing_v2"],
        "critical_limitation":"Current cohort trades value+quality proxy ONLY. Without firm-specific AI, ownership, or takeover evidence, it cannot demonstrate incremental AI/M&A alpha; a matched value-only control and point-in-time historical database are required.",
        "paper_only":True}
    write(state_path,state)
    write(out/"latest.json",result)
    daily=out/"history"/(day.isoformat()+".json")
    if not daily.exists():
        write(daily,result)
    _add_csv(out/"equity_curve.csv",{"date":day.isoformat(),
        "nav_jpy":state["nav_jpy"],"benchmark_nav_jpy":state["baseline_benchmark_nav_jpy"],
        "positions":len(current),"completed_trades":len(state["completed_trades"])},
        ["date","nav_jpy","benchmark_nav_jpy","positions","completed_trades"])
    md=["# AI restructuring / M&A shadow research",f"Date: {day.isoformat()}",
        f"Initial virtual capital: ¥{cfg['virtual_initial_cash_jpy']:,}",
        f"NAV: ¥{state['nav_jpy']:,.0f}; TOPIX benchmark NAV: {state['baseline_benchmark_nav_jpy']}",
        f"Qualified: {len(accepted)} / JP screen: {result['screened_jp_count']}",
        f"Completed trades: {len(state['completed_trades'])}; queued: {len(state['pending_buys'])}",
        "No takeover predictions or proven AI synergies: all unverified.",
        "Current score is a value+quality baseline, not incremental AI/M&A skill.",
        "Missing: "+(", ".join(result["data_blockers"]) or "none"),"",
        "## Candidates (NOT BUY RECOMMENDATIONS)"]
    for x in public_candidates:
        md.append(f"- {x['symbol']} {x['name']}: PER={x['observable']['pe']}, PBR={x['observable']['pb']} (AI and M&A unverified)")
    (out/"latest_report.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run(),ensure_ascii=False))
