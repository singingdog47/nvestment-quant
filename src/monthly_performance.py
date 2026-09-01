from __future__ import annotations

import calendar
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

VERSION = "1.1"


@dataclass(frozen=True)
class PortfolioSnapshot:
    as_of: datetime
    portfolio: pd.DataFrame
    source_file: str | None = None


def _num(value: Any) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _key(df: pd.DataFrame) -> pd.Series:
    if "holding_id" in df.columns:
        x = df["holding_id"].fillna("").astype(str).str.strip()
        if x.ne("").any():
            return x
    ticker = df.get("ticker", pd.Series("", index=df.index)).fillna("").astype(str).str.strip().str.upper()
    code = df.get("code", pd.Series("", index=df.index)).fillna("").astype(str).str.strip().str.upper()
    account = df.get("account", pd.Series("", index=df.index)).fillna("").astype(str).str.strip()
    name = df.get("name", pd.Series("", index=df.index)).fillna("").astype(str).str.strip()
    base = ticker.where(ticker.ne(""), code.where(code.ne(""), name))
    return base + "|" + account


def _snapshot_frame(snapshot: PortfolioSnapshot) -> pd.DataFrame:
    df = snapshot.portfolio.copy(); df["_key"] = _key(df)
    if "market_value" not in df.columns: raise ValueError("snapshot missing market_value")
    df["market_value"] = pd.to_numeric(df["market_value"], errors="coerce")
    for c in ["quantity", "current_price"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[df["market_value"].fillna(0).gt(0)].copy()


def _is_previous_month(a: datetime, b: datetime) -> bool:
    return (a.year == b.year and a.month + 1 == b.month) or (a.year + 1 == b.year and a.month == 12 and b.month == 1)


def _month_boundary_quality(start: datetime, end: datetime) -> dict[str, Any]:
    same_month = start.year == end.year and start.month == end.month
    previous_month_end_start = _is_previous_month(start, end) and start.day >= calendar.monthrange(start.year, start.month)[1] - 3
    same_month_early_start = same_month and start.day <= 3
    end_near_month_end = end.day >= calendar.monthrange(end.year, end.month)[1] - 3
    return {"same_calendar_month": same_month, "start_is_previous_month_end": previous_month_end_start,
            "end_is_month_end": end_near_month_end, "month_complete": end_near_month_end and (previous_month_end_start or same_month_early_start),
            "window_days": max(0.0, (end-start).total_seconds()/86400)}


def _component_summary(records: list[dict[str, Any]] | None, allowed: set[str]) -> dict[str, Any]:
    records = records or []; totals = {k: 0.0 for k in sorted(allowed)}; invalid = 0
    for r in records:
        if not isinstance(r, dict) or str(r.get("type", "")) not in allowed or _num(r.get("amount_jpy")) is None:
            invalid += 1; continue
        totals[str(r["type"])] += float(r["amount_jpy"])
    return {"status": "provided" if records and invalid == 0 else "missing_or_invalid", "totals_jpy": totals, "invalid_records": invalid}


def build_monthly_diagnostics(snapshots: list[PortfolioSnapshot], external_flows: list[dict[str, Any]] | None = None,
                              internal_returns: list[dict[str, Any]] | None = None,
                              costs_taxes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    ordered = sorted(snapshots, key=lambda x: x.as_of)
    if len(ordered) < 2: return {"version": VERSION, "status": "withheld", "reason": "need_at_least_two_portfolio_snapshots"}
    start, end = ordered[0], ordered[-1]; a, b = _snapshot_frame(start), _snapshot_frame(end)
    start_total, end_total = float(a.market_value.sum()), float(b.market_value.sum())
    if start_total <= 0 or end_total <= 0: return {"version": VERSION, "status": "withheld", "reason": "nonpositive_snapshot_market_value"}
    boundary = _month_boundary_quality(start.as_of, end.as_of); raw_change = end_total-start_total
    flows = external_flows or []; valid_flow_amounts=[]; invalid_flows=0
    for flow in flows:
        amount = _num(flow.get("amount_jpy")) if isinstance(flow, dict) else None
        if amount is None: invalid_flows += 1
        else: valid_flow_amounts.append(amount)
    net_external_flow=float(sum(valid_flow_amounts)); residual_gain=residual_return=None; residual_status="withheld"
    if flows and invalid_flows == 0:
        residual_gain=raw_change-net_external_flow; residual_return=residual_gain/start_total; residual_status="reference_only"
    internal = _component_summary(internal_returns, {"dividend", "interest", "fx", "realized_gain_loss"})
    costs = _component_summary(costs_taxes, {"withholding_tax", "trading_fee", "fund_expense", "other_cost"})

    cols=["_key","ticker","code","name","account","quantity","current_price","market_value"]
    m=a[[c for c in cols if c in a]].merge(b[[c for c in cols if c in b]], on="_key", how="outer", suffixes=("_start","_end"), indicator=True)
    start_mv=pd.to_numeric(m.get("market_value_start"),errors="coerce").fillna(0.0); end_mv=pd.to_numeric(m.get("market_value_end"),errors="coerce").fillna(0.0)
    q0=pd.to_numeric(m.get("quantity_start"),errors="coerce") if "quantity_start" in m else pd.Series(index=m.index,dtype=float)
    q1=pd.to_numeric(m.get("quantity_end"),errors="coerce") if "quantity_end" in m else pd.Series(index=m.index,dtype=float)
    p0=pd.to_numeric(m.get("current_price_start"),errors="coerce") if "current_price_start" in m else pd.Series(index=m.index,dtype=float)
    p1=pd.to_numeric(m.get("current_price_end"),errors="coerce") if "current_price_end" in m else pd.Series(index=m.index,dtype=float)
    stable_qty=q0.notna()&q1.notna()&(q0.sub(q1).abs()<=1e-9); stable_price=stable_qty&p0.notna()&p1.notna()&p0.gt(0)&start_mv.gt(0)
    price_return=pd.Series(index=m.index,dtype=float); price_return.loc[stable_price]=p1[stable_price]/p0[stable_price]-1
    price_pnl=pd.Series(index=m.index,dtype=float); price_pnl.loc[stable_price]=start_mv[stable_price]*price_return[stable_price]
    coverage=float(start_mv[stable_price].sum()/start_total); rows=[]
    for idx,row in m.iterrows():
        label=row.get("name_end") or row.get("name_start") or row.get("ticker_end") or row.get("ticker_start") or row.get("code_end") or row.get("code_start") or row.get("_key")
        rows.append({"holding":label,"start_market_value":_num(start_mv.iloc[idx]),"end_market_value":_num(end_mv.iloc[idx]),"quantity_stable":bool(stable_qty.iloc[idx]),"price_return":_num(price_return.iloc[idx]),"estimated_price_pnl_jpy":_num(price_pnl.iloc[idx]),"observation":str(row.get("_merge"))})
    rows.sort(key=lambda x:abs(x.get("estimated_price_pnl_jpy") or 0),reverse=True)
    changed=float(start_mv[~stable_qty.fillna(False)].sum()/start_total); status="current" if boundary["month_complete"] and coverage>=.80 else "reference_only"
    warnings=[]
    if not boundary["month_complete"]: warnings.append("observation_window_does_not_cover_full_calendar_month")
    if coverage<.80: warnings.append("price_attribution_coverage_below_80pct")
    if changed>.05: warnings.append("material_trading_activity_detected")
    if not flows: warnings.append("external_cash_flows_missing_twr_withheld")
    if internal["status"] != "provided": warnings.append("internal_return_components_missing")
    if costs["status"] != "provided": warnings.append("cost_tax_components_missing")
    return {"version":VERSION,"status":status,"analysis_mode":status,"privacy":"PRIVATE_OUTPUT_ONLY",
            "measurement_standard":"TWR methodology aligned with GIPS principles; not a claim of GIPS compliance",
            "start_as_of":start.as_of.astimezone(timezone.utc).isoformat(timespec="seconds"),"end_as_of":end.as_of.astimezone(timezone.utc).isoformat(timespec="seconds"),
            "start_source_file":start.source_file,"end_source_file":end.source_file,"boundary_quality":boundary,
            "holdings_balance":{"start_market_value_jpy":start_total,"end_market_value_jpy":end_total,"change_jpy":raw_change,"change_pct":raw_change/start_total,"important":"balance_change_is_not_investment_return"},
            "external_flows":{"status":"provided" if flows and invalid_flows==0 else "missing_or_invalid","net_external_flow_jpy":net_external_flow if flows and invalid_flows==0 else None,"invalid_flow_records":invalid_flows,"twr_role":"external flows define sub-period boundaries"},
            "internal_return_components":internal,"cost_tax_components":costs,
            "performance":{"twr_status":"withheld","twr":None,"cash_flow_adjusted_residual_status":residual_status,"cash_flow_adjusted_residual_gain_jpy":residual_gain,"cash_flow_adjusted_residual_return":residual_return,"note":"Exact TWR requires valuations at each external-flow boundary. Dividends/interest/FX are returns, not external cash flows."},
            "attribution":{"stable_quantity_start_value_coverage":coverage,"changed_quantity_start_value_weight":changed,"top_price_contributors":rows[:20],"note":"Price contribution is estimated only for unchanged quantities; internal income and cost/tax are separately classified."},"warnings":warnings}


def write_monthly_report(report: dict[str, Any], out_dir: str | Path) -> tuple[Path, Path]:
    d=Path(out_dir); d.mkdir(parents=True,exist_ok=True); jp=d/"portfolio_monthly_latest.json"; jp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    hb=report.get("holdings_balance",{}); p=report.get("performance",{}); a=report.get("attribution",{})
    lines=["# Private Monthly Portfolio Diagnostics v1.1","",f"- Status: {report.get('status')}",f"- Standard: {report.get('measurement_standard')}",f"- Window: {report.get('start_as_of')} -> {report.get('end_as_of')}","","## Balance change (not performance)",f"- Start: {hb.get('start_market_value_jpy')}",f"- End: {hb.get('end_market_value_jpy')}",f"- Change: {hb.get('change_jpy')} ({hb.get('change_pct')})","","## Performance",f"- TWR status: **{p.get('twr_status')}**",f"- TWR: {p.get('twr')}","- External CF: deposits/withdrawals/transfers only; dividends are return components.","- Gross return -> cost/tax -> net return is the target attribution flow.","","## Price attribution",f"- Stable-quantity coverage: {a.get('stable_quantity_start_value_coverage')}"]
    lines += ["", "## Warnings"] + ([f"- {x}" for x in report.get("warnings",[])] or ["- none"])
    lines += ["","## Governance","- Exact TWR remains withheld until external-CF timing and boundary valuations are available.","- This methodology is aligned with GIPS TWR principles; it does not claim GIPS compliance.","- PRIVATE: never commit private portfolio output to public artifacts."]
    mp=d/"portfolio_monthly_latest.md"; mp.write_text("\n".join(lines)+"\n",encoding="utf-8"); return jp,mp
