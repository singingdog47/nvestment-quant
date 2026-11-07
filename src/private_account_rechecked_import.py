"""Recompute private coherence at the import boundary, not from a cached verdict.

A caller-supplied VERIFIED label is not independent evidence. This function
is deliberately non-executable and never authorizes trading.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from private_data_coherence import classify_private_inputs
from private_account_facts_adapter import import_account_facts


def import_account_facts_rechecked(
    portfolio_manifest: dict,
    account_inputs: dict,
    ledger_path: str | Path,
    *,
    now: datetime | None = None,
    max_age_hours: float = 36.0,
    max_skew_hours: float = 24.0,
) -> dict:
    current = now or datetime.now(timezone.utc)
    verdict = classify_private_inputs(
        portfolio_manifest, account_inputs, now=current,
        max_age_hours=max_age_hours, max_skew_hours=max_skew_hours,
    )
    if verdict["status"] != "VERIFIED" or verdict["decision_safe"] is not True:
        raise ValueError("Freshly recomputed source coherence is not VERIFIED")
    result = import_account_facts(account_inputs, str(ledger_path), coherence=verdict)
    return {**result, "coherence_recomputed": True, "execution_ready": False}
