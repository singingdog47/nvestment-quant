"""Fail-closed read model for private verified observations.

A historical fact remains readable for analysis, but it is never execution-ready
without fresh source coverage and independent execution gates.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from verified_facts_ledger import read_verified_facts


def read_asset_state(ledger_path: str | Path, *, now: str,
                     max_age_hours: float = 36,
                     required_scopes: tuple[str, ...] = ()) -> dict:
    """Return facts with per-record freshness; never equate missing with zero."""
    if max_age_hours <= 0:
        raise ValueError("max_age_hours must be positive")
    reference = datetime.fromisoformat(now.replace("Z", "+00:00"))
    if reference.tzinfo is None:
        raise ValueError("now must have timezone")
    facts = read_verified_facts(ledger_path)
    records = {}
    present_scopes = set()
    for key, row in facts.items():
        observed = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
        age_hours = (reference - observed).total_seconds() / 3600
        fresh = 0 <= age_hours <= max_age_hours
        records[key] = {**row, "fresh": fresh, "age_hours": age_hours}
        if fresh:
            present_scopes.add(row["scope"])
    missing = sorted(set(required_scopes) - present_scopes)
    stale_keys = sorted(key for key, row in records.items() if not row["fresh"])
    # This read model never authorizes an order: order coverage, settlement and
    # genuinely deployable cash require independent, current verification.
    return {"status": "PARTIAL" if not records or missing or stale_keys else "VERIFIED_HISTORY",
            "facts": records, "missing_fresh_scopes": missing,
            "stale_or_future_keys": stale_keys, "execution_ready": False,
            "execution_blockers": [
                "account_wide_order_coverage_not_verified",
                "deployable_cash_not_verified",
                "live_execution_authorization_not_verified",
            ]}
