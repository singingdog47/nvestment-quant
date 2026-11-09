"""Conservative earnings/disclosure gate for investor-facing position reviews.

This module does not fetch earnings calendars. Unknown is not 'no event'.
No private holdings or orders should be committed to the repository.
"""
from datetime import datetime, timezone, timedelta

def assess_event_gate(symbol, as_of_utc, event_checked_at_utc=None,
                      event_status="UNKNOWN", event_published_at_utc=None,
                      event_reviewed=False, max_age_hours=24, source_url=None,
                      source_kind=None, coverage_start_utc=None):
    """Return a fail-closed event state; no trading order is generated."""
    if not symbol:
        raise ValueError("symbol required")
    now = datetime.fromisoformat(as_of_utc.replace("Z", "+00:00"))
    if now.tzinfo is None:
        raise ValueError("as_of_utc must include timezone")
    allowed = {"UNKNOWN", "NO_EVENT_CONFIRMED", "EVENT_FOUND"}
    if event_status not in allowed:
        raise ValueError("invalid event_status")
    checked = None
    if event_checked_at_utc:
        checked = datetime.fromisoformat(event_checked_at_utc.replace("Z", "+00:00"))
        if checked.tzinfo is None or checked > now or now - checked > timedelta(hours=max_age_hours):
            checked = None
    if checked is None or event_status == "UNKNOWN":
        return {"symbol": symbol, "state": "EVENT_UNVERIFIED",
                "decision_gate": "BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES",
                "reason": "Recent earnings/disclosures not verified with a fresh source"}
    if event_status == "NO_EVENT_CONFIRMED":
        # Absence requires a verified, bounded, primary-source coverage window.
        if source_kind not in {"JPX_TDNET", "ISSUER_IR"} or not source_url or not coverage_start_utc:
            return {"symbol": symbol, "state": "EVENT_UNVERIFIED",
                    "decision_gate": "BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES",
                    "reason": "No-event claim lacks primary source or coverage window"}
        start = datetime.fromisoformat(coverage_start_utc.replace("Z", "+00:00"))
        if start.tzinfo is None or start > now or now - start > timedelta(days=7):
            return {"symbol": symbol, "state": "EVENT_UNVERIFIED",
                    "decision_gate": "BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES",
                    "reason": "No-event coverage window invalid or too short"}
    if event_status == "EVENT_FOUND":
        if not event_published_at_utc:
            return {"symbol": symbol, "state": "EVENT_UNVERIFIED",
                    "decision_gate": "BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES",
                    "reason": "Event publication timestamp missing"}
        published = datetime.fromisoformat(event_published_at_utc.replace("Z", "+00:00"))
        if published.tzinfo is None or published > now:
            return {"symbol": symbol, "state": "EVENT_UNVERIFIED",
                    "decision_gate": "BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES",
                    "reason": "Event timestamp invalid"}
        if not event_reviewed or source_kind not in {"JPX_TDNET", "ISSUER_IR"} or not source_url:
            return {"symbol": symbol, "state": "EVENT_REVIEW_REQUIRED",
                    "decision_gate": "BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES",
                    "reason": "Recent earnings/disclosure must be analyzed before advice"}
        return {"symbol": symbol, "state": "EVENT_REVIEWED",
                "decision_gate": "ALLOW_FURTHER_REVIEW_NOT_AUTOTRADE",
                "reason": "Event reviewed; market, portfolio, orders still require validation"}
    return {"symbol": symbol, "state": "NO_EVENT_CONFIRMED",
            "decision_gate": "ALLOW_FURTHER_REVIEW_NOT_AUTOTRADE",
            "reason": "Fresh check found no event; not proof of future absence"}
