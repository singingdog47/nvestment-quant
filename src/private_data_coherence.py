"""Conservative, side-effect-free quality gate for private portfolio inputs.

Never interpret upload/processing time as brokerage observation time.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo else None
    except (TypeError, ValueError, OverflowError):
        return None


def classify_private_inputs(
    portfolio_manifest: dict,
    account_inputs: dict,
    *,
    now: datetime | None = None,
    max_age_hours: float = 36.0,
    max_skew_hours: float = 24.0,
) -> dict:
    """Return a non-mutating audit verdict; do not silently repair mismatches."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    now = now.astimezone(timezone.utc)
    pf_method = str(portfolio_manifest.get("source_as_of_method") or "")
    pf_time = _parse_timestamp(portfolio_manifest.get("source_as_of"))
    reasons: list[str] = []
    if pf_time is None or pf_method not in {"filename_embedded_export_time", "pdf_footer_explicit_year"}:
        reasons.append("PORTFOLIO_TIMESTAMP_UNVERIFIED")
    elif (now - pf_time).total_seconds() > max_age_hours * 3600 or pf_time > now:
        reasons.append("PORTFOLIO_STALE_OR_FUTURE")

    verdicts: dict[str, dict] = {}
    for kind in ("account_summary", "orders", "buying_power"):
        item = (account_inputs.get("inputs") or {}).get(kind)
        if not item:
            verdicts[kind] = {"status": "UNVERIFIED", "reasons": ["SOURCE_MISSING"]}
            continue
        method = str(item.get("source_as_of_method") or "")
        observed = _parse_timestamp(item.get("source_as_of"))
        issues: list[str] = []
        if observed is None or method not in {"filename_embedded_export_time", "pdf_footer_explicit_year"}:
            issues.append("TIMESTAMP_UNVERIFIED")
        if item.get("data_status") == "stale":
            issues.append("SOURCE_MARKED_STALE")
        if observed is not None:
            if observed > now or (now - observed).total_seconds() > max_age_hours * 3600:
                issues.append("STALE_OR_FUTURE")
            if pf_time is not None and abs((observed - pf_time).total_seconds()) > max_skew_hours * 3600:
                issues.append("PORTFOLIO_TIME_MISMATCH")
        verdicts[kind] = {
            "status": "VERIFIED" if not issues else "UNVERIFIED",
            "reasons": issues,
            "source_as_of": item.get("source_as_of"),
            "source_as_of_method": method,
        }

    # Comparing each source only to the portfolio can admit a 2x-skew
    # between two sources on opposite sides of the portfolio timestamp.
    # Require the whole observation window to fit the declared skew.
    source_times = [
        _parse_timestamp((account_inputs.get("inputs") or {}).get(kind, {}).get("source_as_of"))
        for kind in ("account_summary", "orders", "buying_power")
    ]
    if all(t is not None for t in source_times):
        span = (max(source_times) - min(source_times)).total_seconds()
        if span > max_skew_hours * 3600:
            reasons.append("ACCOUNT_SOURCES_TIME_MISMATCH")

    overall = "UNVERIFIED" if reasons else (
        "VERIFIED" if all(x["status"] == "VERIFIED" for x in verdicts.values()) else "PARTIAL"
    )
    return {
        "status": overall,
        "portfolio_reasons": reasons,
        "inputs": verdicts,
        "decision_safe": overall == "VERIFIED",
        "rule": "Unverified cash and orders must not be represented as current executable state.",
    }
