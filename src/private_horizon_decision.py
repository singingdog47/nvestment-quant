"""Private, evidence-gated holding-level multi-horizon decision matrix.

Reads private portfolio CSV only inside the private workflow and writes only to
.private/. Outputs are NOT suitable for repository artifacts or public reports.
Does not send, queue or place trades; risk gates are authoritative.
"""
from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

JST = timezone(timedelta(hours=9))
VERSION = "1.0.0"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def _num(value: Any) -> float | None:
    if value is None or str(value).strip() in {"", "-", "nan", "None"}:
        return None
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (ValueError, TypeError):
        return None


def _date(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _norm_symbol(row: dict[str, Any]) -> str | None:
    asset = str(row.get("asset_type") or "")
    code = str(row.get("code") or "").strip()
    if "国内株" in asset and len(code) == 4 and code.isdigit():
        return code + ".T"
    if "米国株" in asset and code:
        return code.upper()
    return None


def _short_signal(
    symbol: str, day: str, outlook: dict[str, Any],
    supply: dict[str, dict[str, str]],
) -> tuple[str, str, str]:
    forecast = next((x for x in outlook.get("prospective_hypotheses") or []
                     if x.get("symbol") == symbol and x.get("as_of_jst") == day), None)
    if forecast:
        side = "POSITIVE_HYPOTHESIS" if forecast.get("expected_sign") == "positive" else "NEGATIVE_HYPOTHESIS"
        return side, "prospective_relative_forecast", str(forecast.get("id"))
    observation = supply.get(symbol)
    if not observation or observation.get("observed_date") != day:
        return "UNKNOWN", "missing_or_stale_supply", ""
    stamp = _date(observation.get("price_as_of"))
    if stamp is None or stamp.astimezone(JST).date().isoformat() != day:
        return "UNKNOWN", "missing_or_stale_price", ""
    confidence = _num(observation.get("confidence"))
    if observation.get("data_status") != "ok" or (confidence or 0) < 0.6:
        return "UNKNOWN", "low_coverage_supply", ""
    flags = set((observation.get("context_flags") or "").split("|"))
    if "PRICE_UP_ON_VOLUME_EXPANSION" in flags:
        return "UP_VOLUME_OBSERVED", "coincident_volume_price_not_verified_flow", ""
    if "PRICE_DOWN_ON_VOLUME_EXPANSION" in flags:
        return "DOWN_VOLUME_OBSERVED", "coincident_volume_price_not_verified_flow", ""
    return "NEUTRAL_OBSERVATION", "no_material_volume_price_event", ""


def _medium_signal(screen: dict[str, Any] | None, day: str) -> tuple[str, str]:
    """3-month price trend is a *proxy*, never sector net flow evidence."""
    if not screen:
        return "UNKNOWN", "no_public_screen_match"
    # Price timestamps can be unavailable for TradingView; the daily screen
    # is only a proxy if its retrieval timestamp is dated to the same JST day.
    stamp = _date(screen.get("data_retrieved_at_utc"))
    if stamp is None or stamp.astimezone(JST).date().isoformat() != day:
        return "UNKNOWN", "screen_freshness_unverified"
    momentum = _num(screen.get("return_3m"))
    if momentum is None:
        return "UNKNOWN", "three_month_return_missing"
    if momentum >= 10:
        return "POSITIVE_MOMENTUM_PROXY", "three_month_return_above_10pct_not_flow"
    if momentum <= -10:
        return "NEGATIVE_MOMENTUM_PROXY", "three_month_return_below_minus10pct_not_flow"
    return "MIXED_MOMENTUM_PROXY", "three_month_return_between_minus10_and_10pct_not_flow"


def _classify_policy(short: str, medium: str, long: str, weight: float | None, account: str) -> tuple[str, list[str]]:
    reasons = ["missing_long_horizon_fundamental_thesis"]
    if short in {"NEGATIVE_HYPOTHESIS", "DOWN_VOLUME_OBSERVED"}:
        action = "HOLD_REVIEW_DOWNSIDE"
        reasons.append("short_selling_pressure_hypothesis_or_observation")
    elif short in {"POSITIVE_HYPOTHESIS", "UP_VOLUME_OBSERVED"} and medium == "POSITIVE_MOMENTUM_PROXY":
        action = "WATCH_ADDITION_ONLY"
        reasons.append("short_positive_and_medium_positive_proxy")
    elif medium == "NEGATIVE_MOMENTUM_PROXY":
        action = "HOLD_REVIEW_THESIS"
        reasons.append("three_month_trend_negative")
    else:
        action = "HOLD_RESEARCH"
    if weight is not None and weight >= 0.10:
        action = "REVIEW_CONCENTRATION"
        reasons.append("holding_weight_over_10pct_reference_not_forced_sale")
    if "NISA" in account:
        reasons.append("NISA_disposal_requires_tax_and_reinvestment_review")
    return action, reasons


def build_private_matrix(
    holdings: pd.DataFrame,
    *,
    outlook: dict[str, Any],
    supply_rows: list[dict[str, str]],
    screening_rows: list[dict[str, str]],
    policy: dict[str, Any],
    investment_state: dict[str, Any],
    source_as_of: str | None,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    day = now.astimezone(JST).date().isoformat()
    source = _date(source_as_of)
    source_fresh = source is not None and source.astimezone(JST).date().isoformat() == day
    outlook_fresh = outlook.get("as_of_jst") == day
    policy_info = policy.get("policy") or {}
    blocks = list(policy_info.get("blocks") or [])
    gate = str((investment_state.get("policy") or {}).get("decision_gate") or "")
    open_orders = (investment_state.get("open_orders") or {}).get("count")
    # Buying power is NOT deployable cash: the bank sweep and scheduled
    # external family payments must be reconciled first.
    capital_state = "UNVERIFIED_HOUSEHOLD_CASH_FLOWS"
    if not source_fresh:
        blocks.append("STALE_PRIVATE_PORTFOLIO")
    if not outlook_fresh:
        blocks.append("STALE_HORIZON_RESEARCH")
    if not policy_info.get("actionable", False):
        blocks.append("PORTFOLIO_POLICY_NOT_ACTIONABLE")
    if gate.startswith("BLOCK"):
        blocks.append("EXISTING_DECISION_GATE_BLOCK")
    if open_orders is None:
        blocks.append("OPEN_ORDER_STATUS_UNVERIFIED")
    elif open_orders > 0:
        blocks.append("OPEN_ORDERS_NEED_RECONCILIATION")
    # This report is never authorized to recommend immediate buys even with
    # an apparently healthy policy flag; cash-flow validation is external.
    blocks = sorted(set(blocks))
    supply = {str(x.get("ticker") or ""): x for x in supply_rows}
    screen = {str(x.get("ticker") or ""): x for x in screening_rows}
    invested = sum((_num(x) or 0) for x in holdings.get("market_value", pd.Series(dtype=float)).tolist())
    items = []
    for _, raw in holdings.iterrows():
        item = raw.to_dict()
        symbol = _norm_symbol(item)
        market_value = _num(item.get("market_value")) or 0
        if market_value <= 0:
            continue
        account = str(item.get("account") or "")
        weight = market_value / invested if invested > 0 else None
        short, short_reason, forecast_id = _short_signal(symbol, day, outlook, supply) if symbol and outlook_fresh else ("UNKNOWN", "missing_or_stale_horizon_data", "")
        medium, medium_reason = _medium_signal(screen.get(symbol), day) if symbol else ("UNKNOWN", "unmatched_asset")
        # Weekly price trends cannot establish long-term intrinsic value.
        long = "UNASSESSED_FUNDAMENTALS"
        action, reasons = _classify_policy(short, medium, long, weight, account)
        if not source_fresh:
            action = "WAIT_FRESH_PRIVATE_SNAPSHOT"
        items.append({
            "symbol": symbol, "name": str(item.get("name") or ""),
            "asset_type": str(item.get("asset_type") or ""),
            "account": account, "market_value_jpy": market_value,
            "weight_in_invested_assets": weight,
            "horizons": {
                "short_1_2w": {"signal": short, "basis": short_reason, "forecast_id": forecast_id},
                "medium_1_3m": {"signal": medium, "basis": medium_reason},
                "long_1_3y": {"signal": long, "basis": "primary_fundamentals_and_valuation_not_integrated"},
            },
            "research_action": action,
            "reasons": reasons,
            "trade_authorized": False,
        })
    # Deterministic decision order: scrutiny of downside and concentration,
    # then prospective ideas. Never label this a buy list.
    precedence = {
        "REVIEW_CONCENTRATION": 0, "HOLD_REVIEW_DOWNSIDE": 1,
        "HOLD_REVIEW_THESIS": 2, "WATCH_ADDITION_ONLY": 3,
        "HOLD_RESEARCH": 4, "WAIT_FRESH_PRIVATE_SNAPSHOT": 5,
    }
    items.sort(key=lambda x: (precedence.get(x["research_action"], 9), -x["market_value_jpy"], x["name"]))
    return {
        "version": VERSION, "generated_at_utc": now.isoformat(timespec="seconds"),
        "as_of_jst": day, "source_as_of": source_as_of,
        "status": "research_only" if source_fresh and outlook_fresh else "partial_data",
        "execution": {"authorized": False, "orders_created": 0,
                      "existing_policy_gate": gate,
                      "blocking_conditions": blocks,
                      "cash_flow_status": capital_state,
                      "1_in_1_out_review": "required_for_any_satellite_replacement",
                      "sell_tax_cost": "not_calculated_without_price_and_tax_confirmation"},
        "holding_count": len(items), "holdings": items,
        "privacy": "PRIVATE_EPHEMERAL_NOT_PUBLIC_REPOSITORY",
        "limits": [
            "Short volume-price flags are observations, not identified institutional net flow.",
            "Medium three-month price returns are proxies, not inferred cash inflows.",
            "Long-horizon intrinsic value is unassessed without verified fundamentals.",
            "No automatic buys or forced sales; household cash and already-booked vehicle transfer remain outside brokerage buying power.",
            "Do not publish, commit or upload this payload to public GitHub artifacts.",
        ],
    }


def write_private_matrix(
    portfolio_path: str | Path, *, source_as_of: str | None,
    policy_payload: dict[str, Any], investment_state: dict[str, Any],
    root: str | Path = ".", output_dir: str | Path = ".private/portfolio_risk",
    now: datetime | None = None,
) -> dict[str, Any]:
    root = Path(root)
    holdings = pd.read_csv(portfolio_path, dtype={"code": str, "ticker": str})
    outcome = build_private_matrix(
        holdings,
        outlook=_load_json(root / "data/horizon_outlook/horizon_latest.json"),
        supply_rows=_load_csv(root / "data/supply_demand/supply_demand_latest.csv"),
        screening_rows=_load_csv(root / "data/screening_latest.csv"),
        policy=policy_payload, investment_state=investment_state,
        source_as_of=source_as_of, now=now,
    )
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "portfolio_horizon_decision_latest.json"
    md_path = out / "portfolio_horizon_decision_latest.md"
    json_path.write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Private PF × multi-horizon research matrix",
        f"Source as of: {source_as_of}, status: {outcome['status']}",
        "This output is not a buy/sell order. Households payments and cash are not reconciled.",
        f"Decision gate: {outcome['execution']['existing_policy_gate']}",
        f"Blocking conditions: {', '.join(outcome['execution']['blocking_conditions']) or 'research-only independent block'}",
        "",
        "| 銘柄 | 短期 | 中期 | 長期 | 調査アクション |",
        "|---|---|---|---|---|",
    ]
    for item in outcome["holdings"]:
        h = item["horizons"]
        lines.append(
            f"| {item['name']} ({item['symbol'] or '-'}) | {h['short_1_2w']['signal']} | "
            f"{h['medium_1_3m']['signal']} | {h['long_1_3y']['signal']} | {item['research_action']} |"
        )
    lines += ["", "## Interpretation", *["- " + x for x in outcome["limits"]]]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"status": outcome["status"], "holding_count": len(outcome["holdings"]),
            "orders_created": 0, "json_path": str(json_path), "markdown_path": str(md_path)}
