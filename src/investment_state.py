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
    verified_ledger_path: str | Path | None = None,
    private_ledger_path: str | Path | None = None,
    now: str | None = None,
    required_asset_scopes: tuple[str, ...] = (),
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

    # Neither buying power nor deposit balance proves freely deployable cash.
    # Buying power can include linked bank balances or unsettled proceeds.
    cash = None

    # One source of truth: never silently merge conflicting private ledgers.
    if (private_ledger_path is not None and verified_ledger_path is not None
            and Path(private_ledger_path) != Path(verified_ledger_path)):
        raise ValueError("Conflicting private ledger paths")
    selected_ledger = private_ledger_path if private_ledger_path is not None else verified_ledger_path
    asset_state = None
    if selected_ledger is not None:
        from private_asset_state_reader import read_asset_state
        asset_state = read_asset_state(
            selected_ledger,
            now=now or datetime.now(timezone.utc).isoformat(),
            required_scopes=required_asset_scopes,
        )

    # Advisory forecasts remain available even when private inputs are partial.
    # This does NOT relax the separate execution blockers.
    from src.advisory_continuity import assess_available_sources
    source_status = {}
    for kind in ("account_summary", "buying_power", "orders"):
        item = inputs.get(kind) or {}
        if not item:
            source_status[kind] = "missing"
        elif str(item.get("data_status") or "").lower() in ("stale", "expired"):
            source_status[kind] = "stale"
        elif str(item.get("data_status") or "").lower() in ("conflict", "mismatch"):
            source_status[kind] = "conflict"
        elif item.get("source_as_of") and item.get("source_as_of_method") in (
                "filename_embedded_export_time", "pdf_footer_explicit_year"):
            source_status[kind] = ("verified" if str(item.get("data_status") or "").lower()
                                   in ("verified", "reconciled", "ok_verified")
                                   else "dated_unreconciled")
        else:
            source_status[kind] = "missing"
    advisory = assess_available_sources(source_status)
    # Timestamp evidence establishes only source dating, not correctness.
    advisory["source_verification_limit"] = (
        "Source timestamps checked; numerical reconciliation and coverage "
        "must be assessed separately.")
    advisory["source_dating_only"] = True
    advisory["recommendations_allowed"] = True
    advisory["recommendations_are_hypothetical"] = True

    # Unverified or conflicted summaries must not leak into authoritative portfolio fields.
    account_for_state = account if source_status["account_summary"] == "verified" else {}
    state = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "privacy": "private",
        "source_as_of": portfolio_manifest.get("source_as_of"),
        "portfolio": {
            "total_assets_jpy": account_for_state.get("total_assets_jpy"),
            "invested_assets_jpy": account_for_state.get("invested_assets_jpy"),
            "daily_change_jpy": account_for_state.get("daily_change_jpy"),
            "daily_change_pct": account_for_state.get("daily_change_pct"),
        },
        "capital": {
            "deployable_cash_jpy": cash,
            "absolute_defense_cash_jpy": (decision.get("policy_guardrails") or {}).get("absolute_defense_cash_jpy"),
        },
        "open_orders": {
            "count": len(open_orders),
            "items": open_orders,
            "source_status": inputs.get("orders", {}).get("data_status", "missing") if inputs.get("orders") else "missing",
            "coverage": "domestic_cash_equity_only",
            "account_wide_coverage_verified": False,
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
        "private_asset_state": asset_state,
        "advisory_continuity": advisory,
        "advisory_source_values": {
            "account_summary": account if source_status["account_summary"] == "stale" else None,
            "label": "historical_unverified_not_for_execution",
        },
        "execution_ready": False,
        "execution_blockers": ["account_wide_order_coverage_not_verified",
                               "deployable_cash_not_verified",
                               "live_execution_authorization_not_verified"],
        "quality": {
            "account_input_status": account_inputs.get("status"),
            "missing_input_types": account_inputs.get("missing_input_types") or [],
            "stale_input_types": account_inputs.get("stale_input_types") or [],
            "rule": "Shared state is context only; it never places, changes, or cancels orders.",
        },
    }
    if asset_state is not None:
        state["verified_asset_history"] = asset_state
        state["execution_blockers"] = sorted(set(
            state["execution_blockers"] + asset_state["execution_blockers"]
        ))
    return state


def write_investment_state(state: dict, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return p
