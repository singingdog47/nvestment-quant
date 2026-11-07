"""Read-only private snapshot coverage and provenance audit.

Scope labels and digest strings are not proof of brokerage authenticity.
No audit result ever grants trading permission.
"""
from __future__ import annotations

from pathlib import Path
from private_asset_state_reader import read_asset_state

DEFAULT_SCOPES = ("account_summary", "buying_power", "orders_domestic_cash",
                  "orders_mutual_funds", "orders_foreign_equities",
                  "cash_and_settlement")


def _digest_label_present(value: object) -> bool:
    prefix = "private:sha256:"
    return (isinstance(value, str) and value.startswith(prefix)
            and len(value) == len(prefix) + 64
            and all(c in "0123456789abcdef" for c in value[len(prefix):]))


def audit_private_snapshot(ledger_path: str | Path, *, now: str,
                           required_scopes: tuple[str, ...] = DEFAULT_SCOPES) -> dict:
    state = read_asset_state(ledger_path, now=now, required_scopes=required_scopes)
    present = sorted({row["scope"] for row in state["facts"].values() if row["fresh"]})
    missing = state["missing_fresh_scopes"]
    missing_digests = sorted({
        row["scope"] for row in state["facts"].values()
        if row["fresh"] and row["scope"] in required_scopes
        and not _digest_label_present(row.get("evidence_ref"))
    })
    incomplete = bool(missing or missing_digests or state["stale_or_future_keys"] or not state["facts"])
    blockers = state["execution_blockers"] + (
        ["private_source_coverage_incomplete"] if missing else []
    ) + (["private_source_digest_unverified"] if missing_digests else [])
    return {
        "status": "INCOMPLETE" if incomplete else "HISTORICAL_COVERAGE_ONLY",
        "present_fresh_scopes": present,
        "missing_fresh_scopes": missing,
        "scopes_without_content_digest": missing_digests,
        "stale_or_future_keys": state["stale_or_future_keys"],
        "verified_record_count": len(state["facts"]),
        "execution_ready": False,
        "execution_blockers": sorted(set(blockers)),
        "note": "A digest label alone is not independently authenticated. Historical scope coverage never proves account-wide orders or deployable cash.",
    }
