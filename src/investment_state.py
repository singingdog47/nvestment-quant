from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


SCHEMA_VERSION = "1.0"


def _read_json(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _watchlist_summary(path: str | Path = "config/watchlist_master.csv") -> dict:
    p = Path(path)
    if not p.exists():
        return {"status": "missing", "active_count": 0, "high_priority": []}
    df = pd.read_csv(p, dtype=str).fillna("")
    if "status" in df.columns:
        df = df[df["status"].str.lower().eq("active")]
    high = df[df.get("priority", "").astype(str).str.lower().eq("high")] if "priority" in df.columns else df.iloc[0:0]
    return {
        "status": "ok",
        "active_count": int(len(df)),
        "high_priority": [
            {"code": str(r.get("code", "")), "ticker": str(r.get("ticker", "")), "name": str(r.get("name", "")),
             "thesis": str(r.get("thesis", "")), "trigger": str(r.get("trigger", "")),
             "invalidation": str(r.get("invalidation", ""))}
            for _, r in high.iterrows()
        ],
    }


def build_investment_state(
    account_inputs: dict,
    portfolio_manifest: dict,
    policy_payload: dict,
    *,
    decision_context_path: str | Path = "data/decision_context_latest.json",
    watchlist_path: str | Path = "config/watchlist_master.csv",
) -> dict:
    inputs = account_inputs.get("inputs") or {}
    account = inputs.get("account_summary") or {}
    buying = inputs.get("buying_power") or {}
    orders = inputs.get("orders") or {}
    decision = _read_json(decision_context_path)
    regime = decision.get("market_regime") or {}

    open_orders = []
    for item in orders.get("items") or []:
        status = str(item.get("status") or "")
        if any(token in status for token in ("執行中", "待機中", "受付済", "未約定")):
            open_orders.append(item)

    cash = buying.get("cash_buying_power_jpy")
    if cash is None:
        cash = account.get("cash_deposit_jpy")

    state = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "privacy": "private",
        "source_as_of": portfolio_manifest.get("source_as_of"),
        "portfolio": {
            "total_assets_jpy": account.get("total_assets_jpy"),
            "invested_assets_jpy": account.get("invested_assets_jpy"),
            "daily_change_jpy": account.get("daily_change_jpy"),
            "daily_change_pct": account.get("daily_change_pct"),
        },
        "capital": {
            "deployable_cash_jpy": cash,
            "absolute_defense_cash_jpy": (decision.get("policy_guardrails") or {}).get("absolute_defense_cash_jpy"),
        },
        "open_orders": {
            "count": len(open_orders),
            "items": open_orders,
            "source_status": inputs.get("orders", {}).get("data_status", "missing") if inputs.get("orders") else "missing",
        },
        "market_regime": {
            "label": regime.get("regime_label"),
            "score": regime.get("regime_score"),
            "confidence": regime.get("confidence"),
            "flags": regime.get("regime_flags") or [],
            "date_jst": regime.get("date_jst"),
            "actionable": regime.get("actionable"),
        },
        "watchlist": _watchlist_summary(watchlist_path),
        "policy": {
            "status": policy_payload.get("status"),
            "decision_gate": (decision.get("policy_guardrails") or {}).get("decision_gate"),
        },
        "quality": {
            "account_input_status": account_inputs.get("status"),
            "missing_input_types": account_inputs.get("missing_input_types") or [],
            "stale_input_types": account_inputs.get("stale_input_types") or [],
            "rule": "Shared state is context only; it never places, changes, or cancels orders.",
        },
    }
    return state


def write_investment_state(state: dict, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return p
