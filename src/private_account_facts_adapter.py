"""Adapter for PR #81 private-account outputs to PR #82 verified facts.

Does not infer that a domestic-only order view covers all brokerage orders.
No raw brokerage values are written to the public repository.
"""
from __future__ import annotations

from import_verified_snapshot import import_verified_snapshot


def import_account_facts(account_inputs: dict, ledger_path: str) -> dict:
    """Conservative bridge: requires explicit upstream coherence verification."""
    if account_inputs.get("status") != "ok" or account_inputs.get("missing_input_types") or account_inputs.get("stale_input_types"):
        raise ValueError("Incomplete or stale account inputs")
    if account_inputs.get("coherence_verified") is not True:
        raise ValueError("Explicit upstream coherence verification required")
    inputs = account_inputs.get("inputs") or {}
    results = []
    for kind, keys in (
        ("account_summary", ("total_assets_jpy", "invested_assets_jpy",
            "deposits_total_jpy", "cash_deposit_jpy", "margin_collateral_jpy")),
        ("buying_power", ("cash_buying_power_jpy",)),
    ):
        data = inputs.get(kind) or {}
        if data.get("data_status") != "ok" or data.get("source_as_of_method") not in (
            "filename_embedded_export_time", "pdf_footer_explicit_year"):
            raise ValueError("Unverified source: " + kind)
        if not data.get("source_file") or not data.get("source_as_of"):
            raise ValueError("Missing source evidence: " + kind)
        facts = [{"key": f"{kind}:{key}", "value": data[key], "scope": kind}
                 for key in keys if data.get(key) is not None]
        if not facts:
            raise ValueError("Missing source values: " + kind)
        results.append(import_verified_snapshot({
            "verification_status": "verified",
            "observed_at": data["source_as_of"],
            "evidence_ref": "private:" + data["source_file"],
            "quality": {"source_verified": True, "coherence_verified": True,
                        "source_scope": kind},
            "facts": facts,
        }, ledger_path))
    return {"status": "ok", "source_imports": results}
