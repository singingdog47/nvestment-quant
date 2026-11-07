"""Adapter for PR #81 private-account outputs to PR #82 verified facts.

Does not infer that a domestic-only order view covers all brokerage orders.
No raw brokerage values are written to the public repository.
"""
from __future__ import annotations

from import_verified_snapshot import import_verified_snapshot


def import_account_facts(account_inputs: dict, ledger_path: str) -> dict:
    inputs = account_inputs.get("inputs") or {}
    facts = []
    for kind, scope, keys in (
        ("account_summary", "account_summary", ("total_assets_jpy", "invested_assets_jpy",
            "deposits_total_jpy", "cash_deposit_jpy", "margin_collateral_jpy")),
        ("buying_power", "buying_power", ("cash_buying_power_jpy",)),
    ):
        data = inputs.get(kind) or {}
        if data.get("data_status") != "ok" or data.get("source_as_of_method") not in (
            "filename_embedded_export_time", "pdf_footer_explicit_year"):
            continue
        for key in keys:
            if data.get(key) is not None:
                facts.append({"key": f"{scope}:{key}", "value": data[key], "scope": scope})
    if not facts:
        raise ValueError("No verified account values available")
    # Snapshot-wide timestamp and evidence are not interchangeable across files.
    # Require a common verified observation time and retain every source reference.
    sources = [inputs[k] for k in ("account_summary", "buying_power") if
               any(f["scope"] == k for f in facts)]
    times = {s.get("source_as_of") for s in sources}
    if len(times) != 1 or None in times:
        raise ValueError("Mixed observation timestamps require per-source import")
    refs = [s.get("source_file") for s in sources]
    if any(not ref for ref in refs):
        raise ValueError("Missing evidence source file")
    return import_verified_snapshot({
        "verification_status": "verified", "observed_at": next(iter(times)),
        "evidence_ref": "private:" + "|".join(refs),
        "quality": {"source_verified": True, "coherence_verified": True,
                    "source_scope": "account_summary"},
        "facts": facts,
    }, ledger_path)
