"""Read-only completeness audit for private portfolio snapshots.

This reports evidence gaps; it does not infer zero holdings or permit trades.
"""
from __future__ import annotations

from pathlib import Path
from private_asset_state_reader import read_asset_state

DEFAULT_SCOPES = ("account_summary", "buying_power", "orders_domestic_cash",
                  "orders_mutual_funds", "orders_foreign_equities",
                  "cash_and_settlement")


def audit_private_snapshot(ledger_path: str | Path, *, now: str,
                           required_scopes: tuple[str, ...] = DEFAULT_SCOPES) -> dict:
    state = read_asset_state(ledger_path, now=now, required_scopes=required_scopes)
    present = sorted({row["scope"] for row in state["facts"].values() if row["fresh"]})
    missing = state["missing_fresh_scopes"]
    return {
        "status": "INCOMPLETE" if missing or state["stale_or_future_keys"] or not state["facts"] else "HISTORICAL_COVERAGE_ONLY",
        "present_fresh_scopes": present,
        "missing_fresh_scopes": missing,
        "stale_or_future_keys": state["stale_or_future_keys"],
        "verified_record_count": len(state["facts"]),
        "execution_ready": False,
        "execution_blockers": sorted(set(state["execution_blockers"] + (
            ["private_source_coverage_incomplete"] if missing else []
        ))),
        "note": "Historical scope coverage is not proof of complete account orders, settlement, or executable cash.",
    }
