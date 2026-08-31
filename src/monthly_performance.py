from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

VERSION = "1.0"


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
    df = snapshot.portfolio.copy()
    df["_key"] = _key(df)
    if "market_value" not in df.columns:
        raise ValueError("snapshot missing market_value")
    df["market_value"] = pd.to_numeric(df["market_value"], errors="coerce")
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    if "current_price" in df.columns:
        df["current_price"] = pd.to_numeric(df["current_price"], errors="coerce")
    return df[df["market_value"].fillna(0).gt(0)].copy()


def _month_boundary_quality(start: datetime, end: datetime) -> dict[str, Any]:
    same_month = start.year == end.year and start.month == end.month
    month_complete = same_month and start.day <= 3 and end.day >= 27
    return {
        "same_calendar_month": same_month,
        "month_complete": month_complete,
        "window_days": max(0.0, (end - start).total_seconds() / 86400),
    }


def build_monthly_diagnostics(
    snapshots: list[PortfolioSnapshot],
    external_flows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    ordered = sorted(snapshots, key=lambda x: x.as_of)
    if len(ordered) < 2:
        return {"version": VERSION, "status": "withheld", "reason": "need_at_least_two_portfolio_snapshots"}
    start = ordered[0]; end = ordered[-1]
    a = _snapshot_frame(start); b = _snapshot_frame(end)
    start_total = float(a["market_value"].sum()); end_total = float(b["market_value"].sum())
    if start_total <= 0 or end_total <= 0:
        return {"version": VERSION, "status": "withheld", "reason": "nonpositive_snapshot_market_value"}

    boundary = _month_boundary_quality(start.as_of, end.as_of)
    raw_change = end_total - start_total
    raw_change_pct = raw_change / start_total
    flows = external_flows or []
    valid_flow_amounts: list[float] = []
    invalid_flows = 0
    for flow in flows:
        amount = _num(flow.get("amount_jpy")) if isinstance(flow, dict) else None
        if amount is None:
            invalid_flows += 1
        else:
            valid_flow_amounts.append(amount)
    net_external_flow = float(sum(valid_flow_amounts))

    # Do not pretend a balance change is investment performance. Exact TWR needs
    # valuations at each external-flow boundary. This engine deliberately withholds
    # TWR unless subperiod boundary returns are explicitly supplied in the future.
    twr_status = "withheld"
    twr = None
    residual_gain = None
    residual_return = None
    residual_status = "withheld"
    if flows and invalid_flows == 0:
        residual_gain = raw_change - net_external_flow
        residual_return = residual_gain / start_total
        residual_status = "reference_only"

    left_cols = [c for c in ["_key", "ticker", "code", "name", "account", "quantity", "current_price", "market_value"] if c in a.columns]
    right_cols = [c for c in ["_key", "ticker", "code", "name", "account", "quantity", "current_price", "market_value"] if c in b.columns]
    m = a[left_cols].merge(b[right_cols], on="_key", how="outer", suffixes=("_start", "_end"), indicator=True)
    start_mv = pd.to_numeric(m.get("market_value_start"), errors="coerce").fillna(0.0)
    end_mv = pd.to_numeric(m.get("market_value_end"), errors="coerce").fillna(0.0)
    q0 = pd.to_numeric(m.get("quantity_start"), errors="coerce") if "quantity_start" in m else pd.Series(index=m.index, dtype=float)
    q1 = pd.to_numeric(m.get("quantity_end"), errors="coerce") if "quantity_end" in m else pd.Series(index=m.index, dtype=float)
    p0 = pd.to_numeric(m.get("current_price_start"), errors="coerce") if "current_price_start" in m else pd.Series(index=m.index, dtype=float)
    p1 = pd.to_numeric(m.get("current_price_end"), errors="coerce") if "current_price_end" in m else pd.Series(index=m.index, dtype=float)
    stable_qty = q0.notna() & q1.notna() & (q0.sub(q1).abs() <= 1e-9)
    valid_price = p0.notna() & p1.notna() & p0.gt(0)
    stable_price = stable_qty & valid_price & start_mv.gt(0)
    price_return = pd.Series(index=m.index, dtype=float)
    price_return.loc[stable_price] = p1[stable_price] / p0[stable_price] - 1.0
    price_pnl = pd.Series(index=m.index, dtype=float)
    price_pnl.loc[stable_price] = start_mv[stable_price] * price_return[stable_price]
    attribution_coverage = float(start_mv[stable_price].sum() / start_total)

    rows = []
    for idx, row in m.iterrows():
        label = row.get("name_end") or row.get("name_start") or row.get("ticker_end") or row.get("ticker_start") or row.get("code_end") or row.get("code_start") or row.get("_key")
        rows.append({
            "holding": label,
            "start_market_value": _num(start_mv.iloc[idx]),
            "end_market_value": _num(end_mv.iloc[idx]),
            "quantity_stable": bool(stable_qty.iloc[idx]) if idx in stable_qty.index else False,
            "price_return": _num(price_return.iloc[idx]) if idx in price_return.index else None,
            "estimated_price_pnl_jpy": _num(price_pnl.iloc[idx]) if idx in price_pnl.index else None,
            "observation": str(row.get("_merge")),
        })
    rows.sort(key=lambda x: abs(x.get("estimated_price_pnl_jpy") or 0.0), reverse=True)

    changed_quantity_weight = float(start_mv[~stable_qty.fillna(False)].sum() / start_total)
    status = "current" if boundary["month_complete"] and attribution_coverage >= 0.80 else "reference_only"
    warnings: list[str] = []
    if not boundary["month_complete"]:
        warnings.append("observation_window_does_not_cover_full_calendar_month")
    if attribution_coverage < 0.80:
        warnings.append("price_attribution_coverage_below_80pct")
    if changed_quantity_weight > 0.05:
        warnings.append("material_trading_activity_detected")
    if not flows:
        warnings.append("external_cash_flows_missing_twr_withheld")

    return {
        "version": VERSION,
        "status": status,
        "analysis_mode": status,
        "privacy": "PRIVATE_OUTPUT_ONLY",
        "start_as_of": start.as_of.astimezone(timezone.utc).isoformat(timespec="seconds"),
        "end_as_of": end.as_of.astimezone(timezone.utc).isoformat(timespec="seconds"),
        "start_source_file": start.source_file,
        "end_source_file": end.source_file,
        "boundary_quality": boundary,
        "holdings_balance": {
            "start_market_value_jpy": start_total,
            "end_market_value_jpy": end_total,
            "change_jpy": raw_change,
            "change_pct": raw_change_pct,
            "important": "balance_change_is_not_investment_return",
        },
        "external_flows": {
            "status": "provided" if flows and invalid_flows == 0 else "missing_or_invalid",
            "net_external_flow_jpy": net_external_flow if flows and invalid_flows == 0 else None,
            "invalid_flow_records": invalid_flows,
        },
        "performance": {
            "twr_status": twr_status,
            "twr": twr,
            "cash_flow_adjusted_residual_status": residual_status,
            "cash_flow_adjusted_residual_gain_jpy": residual_gain,
            "cash_flow_adjusted_residual_return": residual_return,
            "note": "Exact TWR requires valuations at each external cash-flow boundary; residual return is not a substitute for TWR.",
        },
        "attribution": {
            "stable_quantity_start_value_coverage": attribution_coverage,
            "changed_quantity_start_value_weight": changed_quantity_weight,
            "top_price_contributors": rows[:20],
            "note": "Price contribution is estimated only for holdings with unchanged quantity and valid start/end prices.",
        },
        "warnings": warnings,
    }


def write_monthly_report(report: dict[str, Any], out_dir: str | Path) -> tuple[Path, Path]:
    d = Path(out_dir); d.mkdir(parents=True, exist_ok=True)
    json_path = d / "portfolio_monthly_latest.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    hb = report.get("holdings_balance", {}); p = report.get("performance", {}); a = report.get("attribution", {})
    lines = [
        "# Private Monthly Portfolio Diagnostics v1.0", "",
        f"- Status: {report.get('status')}",
        f"- Window: {report.get('start_as_of')} -> {report.get('end_as_of')}",
        f"- Full-month coverage: {(report.get('boundary_quality') or {}).get('month_complete')}", "",
        "## Balance change (not performance)",
        f"- Start holdings value: {hb.get('start_market_value_jpy')}",
        f"- End holdings value: {hb.get('end_market_value_jpy')}",
        f"- Change: {hb.get('change_jpy')} ({hb.get('change_pct')})", "",
        "## Performance measurement",
        f"- TWR status: **{p.get('twr_status')}**",
        f"- TWR: {p.get('twr')}",
        f"- Cash-flow-adjusted residual status: {p.get('cash_flow_adjusted_residual_status')}",
        f"- Cash-flow-adjusted residual return: {p.get('cash_flow_adjusted_residual_return')}",
        "- Balance changes are never promoted to investment returns.", "",
        "## Price attribution",
        f"- Stable-quantity coverage: {a.get('stable_quantity_start_value_coverage')}",
        f"- Changed-quantity weight: {a.get('changed_quantity_start_value_weight')}",
    ]
    for x in (a.get("top_price_contributors") or [])[:10]:
        lines.append(f"- {x.get('holding')}: return={x.get('price_return')} | estimated price P/L={x.get('estimated_price_pnl_jpy')}")
    lines += ["", "## Warnings"] + ([f"- {x}" for x in report.get("warnings", [])] or ["- none"])
    lines += ["", "## Governance", "- Exact TWR stays withheld until external cash-flow timing and boundary valuations are available.", "- Trades are separated from price effects whenever quantity changes.", "- PRIVATE: never commit or upload to public Actions artifacts."]
    md_path = d / "portfolio_monthly_latest.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
