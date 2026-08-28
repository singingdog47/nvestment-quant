from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from .portfolio_policy import evaluate_policy, load_policy
except ImportError:  # supports PYTHONPATH=src / direct script execution
    from portfolio_policy import evaluate_policy, load_policy


def _num(v: Any) -> float | None:
    try:
        x = float(v)
        return x if pd.notna(x) else None
    except (TypeError, ValueError):
        return None


def build_policy_state(portfolio: pd.DataFrame, account_inputs: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build only facts supported by current private inputs.

    Sleeve/account/tax fields are intentionally not inferred from ticker names.
    When source columns are absent the policy engine returns warnings instead of
    fabricating classifications or sell conclusions.
    """
    state: dict[str, Any] = {"holding_count": int(len(portfolio))}
    total = _num(portfolio.get("market_value", pd.Series(dtype=float)).sum()) if "market_value" in portfolio else None
    if total and total > 0 and "sleeve" in portfolio.columns:
        values = portfolio.assign(_mv=pd.to_numeric(portfolio["market_value"], errors="coerce").fillna(0)).groupby("sleeve")["_mv"].sum()
        for sleeve in ("satellite_core", "lifestyle_benefit", "exploration", "tactical_cash"):
            if sleeve in values.index:
                state[f"{sleeve}_ratio"] = float(values[sleeve] / total)
    if "sleeve" in portfolio.columns and "cost_basis" in portfolio.columns:
        mask = portfolio["sleeve"].astype(str).eq("exploration")
        state["exploration_new_capital_cost_jpy"] = float(pd.to_numeric(portfolio.loc[mask, "cost_basis"], errors="coerce").fillna(0).sum())
    inputs = (account_inputs or {}).get("inputs") or {}
    bp = inputs.get("buying_power") or {}
    defensive = _num(bp.get("defensive_cash_jpy"))
    if defensive is not None:
        state["household_defensive_cash_jpy"] = defensive
    state["expected_return_definition"] = "geometric_cagr"
    return state


def write_policy_report(portfolio_path: str | Path, account_inputs: dict[str, Any], out_dir: str | Path) -> dict[str, Any]:
    portfolio = pd.read_csv(portfolio_path)
    state = build_policy_state(portfolio, account_inputs)
    result = evaluate_policy(state, load_policy())
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "ok",
        "source_fields_used": sorted(state.keys()),
        "policy": result,
        "privacy": "private_ephemeral_output",
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "portfolio_policy_latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Private Portfolio Policy v2.0", "", f"Generated: {payload['generated_at']}", "", "## Guardrails"]
    lines.append(f"- Actionable: {result['actionable']}")
    lines.append(f"- Blocks: {', '.join(result['blocks']) if result['blocks'] else 'none'}")
    lines.append(f"- Warnings: {', '.join(result['warnings']) if result['warnings'] else 'none'}")
    lines.append(f"- Observations: {', '.join(result['observations']) if result['observations'] else 'none'}")
    lines += ["", "## Interpretation", "- Missing sleeve, tax, or account metadata is reported as missing; it is never inferred from a company name.", "- This report creates no trade orders.", "- Private output must not be committed or uploaded as a public artifact."]
    (out / "portfolio_policy_latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload
