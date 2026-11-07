"""Advisory continuity policy: degrade confidence, never fabricate execution facts."""
from __future__ import annotations


def classify_advisory_continuity(*, verified_scopes: list[str],
                                 missing_scopes: list[str],
                                 conflicting_scopes: list[str],
                                 stale_scopes: list[str],
                                 duplicate_scopes: list[str] | None = None) -> dict:
    """Keep independent analysis available while execution gates stay closed.

    Duplicate scopes are informational only if upstream deduplication established
    identical source content. Conflicting facts are never silently reconciled.
    """
    verified = sorted(set(verified_scopes) - set(conflicting_scopes))
    missing = sorted(set(missing_scopes))
    conflicting = sorted(set(conflicting_scopes))
    stale = sorted(set(stale_scopes))
    duplicate = sorted(set(duplicate_scopes or []))
    if not verified:
        mode = "SCENARIO_ONLY"
        confidence = "LOW"
    elif conflicting:
        mode = "PARTIAL_WITH_CONFLICTS"
        confidence = "LOW"
    elif missing or stale:
        mode = "CONDITIONAL_FORECAST"
        confidence = "MEDIUM"
    else:
        mode = "EVIDENCE_BASED_FORECAST"
        confidence = "HIGH"
    return {
        "analysis_allowed": True,
        "analysis_mode": mode,
        "confidence_tier": confidence,
        "verified_scopes": verified,
        "missing_scopes": missing,
        "conflicting_scopes_excluded": conflicting,
        "stale_scopes": stale,
        "duplicate_scopes_deduplicated": duplicate,
        "assumptions_required": bool(missing or stale or conflicting or not verified),
        "order_coverage_verified": False,
        "deployable_cash_jpy": None,
        "execution_ready": False,
        "trade_execution_authorized": False,
    }


def assess_available_sources(source_status: dict[str, str]) -> dict:
    """Determine advisory coverage without demanding a complete four-file batch.

    Input statuses: verified, missing, stale, conflict, duplicate_verified.
    Unknown statuses are rejected rather than assumed verified.
    """
    allowed = {"verified", "missing", "stale", "conflict", "duplicate_verified"}
    unknown = {v for v in source_status.values() if v not in allowed}
    if unknown:
        raise ValueError(f"Unknown source statuses: {sorted(unknown)}")
    groups = {name: [] for name in allowed}
    for scope, status in source_status.items():
        groups[status].append(scope)
    result = classify_advisory_continuity(
        verified_scopes=groups["verified"] + groups["duplicate_verified"],
        missing_scopes=groups["missing"],
        conflicting_scopes=groups["conflict"],
        stale_scopes=groups["stale"],
        duplicate_scopes=groups["duplicate_verified"],
    )
    result["source_status"] = dict(source_status)
    result["source_count"] = len(source_status)
    result["verified_source_count"] = len(groups["verified"]) + len(groups["duplicate_verified"])
    result["forecast_is_conditional"] = result["analysis_mode"] != "EVIDENCE_BASED_FORECAST"
    return result
