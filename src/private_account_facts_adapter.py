"""Adapter for PR #81 private-account outputs to PR #82 verified facts.

Does not infer that a domestic-only order view covers all brokerage orders.
No raw brokerage values are written to the public repository.
"""
from __future__ import annotations

import math
from numbers import Real

from verified_facts_ledger import append_verified_facts


def _import_account_facts_with_verdict(account_inputs: dict, ledger_path: str, *, coherence: dict) -> dict:
    """Conservative bridge: requires explicit upstream coherence verification."""
    if account_inputs.get("status") != "ok" or account_inputs.get("missing_input_types") or account_inputs.get("stale_input_types"):
        raise ValueError("Incomplete or stale account inputs")
    if coherence.get("status") != "VERIFIED" or coherence.get("decision_safe") is not True:
        raise ValueError("PR81 coherence verdict must be VERIFIED")
    verdicts = coherence.get("inputs") or {}
    if any((verdicts.get(k) or {}).get("status") != "VERIFIED" for k in ("account_summary", "buying_power", "orders")):
        raise ValueError("Missing verified per-source coherence verdict")
    inputs = account_inputs.get("inputs") or {}
    batch = []
    source_summaries = []
    for kind, keys in (
        ("account_summary", ("total_assets_jpy", "invested_assets_jpy",
            "deposits_total_jpy", "cash_deposit_jpy", "margin_collateral_jpy")),
        ("buying_power", ("cash_buying_power_jpy",)),
    ):
        data = inputs.get(kind) or {}
        if data.get("status") != "ok" or data.get("source_as_of_method") not in (
            "filename_embedded_export_time", "pdf_footer_explicit_year"):
            raise ValueError("Unverified source: " + kind)
        if not data.get("source_as_of"):
            raise ValueError("Missing source observation time: " + kind)
        if (verdicts[kind].get("source_as_of") != data["source_as_of"] or
                verdicts[kind].get("source_as_of_method") != data["source_as_of_method"]):
            raise ValueError("Coherence verdict does not match source: " + kind)
        facts = []
        for key in keys:
            value = data.get(key)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
                raise ValueError("Invalid numeric account value: " + kind + ":" + key)
            if value < 0:
                raise ValueError("Negative account value requires manual reconciliation: " + kind + ":" + key)
            facts.append({"key": f"{kind}:{key}", "value": value, "scope": kind})
        if kind == "account_summary":
            total = data.get("total_assets_jpy")
            invested = data.get("invested_assets_jpy")
            if total is None or invested is None or total < invested:
                raise ValueError("Account total and invested assets inconsistent")
        if not facts:
            raise ValueError("Missing source values: " + kind)
        evidence = data.get("source_file") or account_inputs.get("source_file")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("Missing concrete source evidence: " + kind)
        batch.extend({
            **fact, "observed_at": data["source_as_of"],
            "evidence_ref": "private:" + evidence,
        } for fact in facts)
        source_summaries.append({"source_scope": kind,
                                 "source_as_of": data["source_as_of"],
                                 "facts_count": len(facts)})
    # A failure in any source cannot leave a partially imported account state.
    imported = append_verified_facts(ledger_path, batch, auto_supersede=True)
    return {"status": "ok", "facts_imported": len(imported),
            "source_imports": source_summaries}


def import_account_facts(account_inputs: dict, ledger_path: str, *, coherence: dict | None = None,
                         portfolio_manifest: dict | None = None, now=None) -> dict:
    """Public entrypoint: require current portfolio evidence and recompute coherence.

    Legacy coherence-only calls fail closed rather than trusting a cached label.
    """
    if portfolio_manifest is None:
        raise ValueError("Portfolio manifest required to recompute coherence")
    from private_data_coherence import classify_private_inputs
    verdict = classify_private_inputs(portfolio_manifest, account_inputs, now=now)
    if verdict.get("status") != "VERIFIED" or verdict.get("decision_safe") is not True:
        raise ValueError("Freshly recomputed source coherence is not VERIFIED")
    return _import_account_facts_with_verdict(account_inputs, ledger_path, coherence=verdict)
