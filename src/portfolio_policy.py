from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VERSION = "2.0.0"
DEFAULT_POLICY = Path("config/portfolio_policy_v2_0.json")


def load_policy(path: str | Path = DEFAULT_POLICY) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evaluate_policy(state: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate allocation guardrails without creating automatic trade orders.

    Expected state keys are optional. Missing inputs produce warnings rather than
    fabricated conclusions. Ratios should be expressed as decimals.
    """
    p = policy or load_policy()
    warnings: list[str] = []
    blocks: list[str] = []
    observations: list[str] = []

    defensive = float(state.get("household_defensive_cash_jpy") or 0)
    min_defensive = float(p["capital_buckets"]["household_defensive_cash"]["minimum_jpy"])
    if defensive < min_defensive:
        blocks.append("household_defensive_cash_below_minimum")

    exploration_cost = state.get("exploration_new_capital_cost_jpy")
    exploration_cap = float(p["capital_buckets"]["exploration"]["new_capital_cost_cap_jpy"])
    if exploration_cost is None:
        warnings.append("exploration_cost_basis_missing")
    elif float(exploration_cost) >= exploration_cap:
        blocks.append("freeze_new_exploration_buys")
        observations.append("existing exploration overweight alone does not force a sale")

    for sleeve in ("satellite_core", "lifestyle_benefit", "exploration", "tactical_cash"):
        ratio = state.get(f"{sleeve}_ratio")
        cfg = p["capital_buckets"][sleeve]
        if ratio is None:
            warnings.append(f"{sleeve}_ratio_missing")
            continue
        r = float(ratio)
        if r < float(cfg["target_min"]): observations.append(f"{sleeve}_below_reference_range")
        if r > float(cfg["target_max"]): observations.append(f"{sleeve}_above_reference_range")

    if state.get("proposed_sell"):
        if not state.get("account_type"):
            blocks.append("withhold_tax_adjusted_sell_conclusion")
        if state.get("tax_adjusted_switch_benefit") is None:
            blocks.append("tax_adjusted_switch_benefit_required")

    definition = state.get("expected_return_definition")
    if definition not in p["return_model"]["allowed_definitions"]:
        warnings.append("expected_return_definition_missing_or_invalid")

    if state.get("apply_volatility_drag") and definition == "geometric_cagr":
        blocks.append("prevent_double_volatility_drag_adjustment")

    if state.get("holding_count") is not None:
        count = int(state["holding_count"])
        lo = int(p["portfolio_rules"]["reference_holding_count_min"])
        hi = int(p["portfolio_rules"]["reference_holding_count_max"])
        if count < lo or count > hi:
            observations.append("holding_count_outside_reference_range_no_forced_trade")

    return {
        "policy_version": VERSION,
        "trade_orders_created": False,
        "actionable": not blocks,
        "blocks": blocks,
        "warnings": warnings,
        "observations": observations,
    }
