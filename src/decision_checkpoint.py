"""Review explicit decision plans without mistaking a price trigger for an order.

Caller supplies PRIVATE rules and price observations. Neither personal
positions nor decision plans are stored in this public repository.
"""
from __future__ import annotations

from datetime import date


def review_rule(rule: dict, observation: dict, as_of: date) -> dict:
    """Return a concrete review status, not a broker execution instruction.

    action: TRIM, EXIT, BUY_REVIEW, or HOLD_REVIEW
    comparator: AT_OR_ABOVE or AT_OR_BELOW
    observations must include a dated high/low (intraday trigger) or close.
    An old unacted trigger remains OVERDUE rather than silently resetting.
    """
    required = ("id", "symbol", "action", "comparator", "threshold", "created_date")
    if any(k not in rule for k in required):
        raise ValueError("missing decision rule field")
    if rule["action"] not in {"TRIM", "EXIT", "BUY_REVIEW", "HOLD_REVIEW"}:
        raise ValueError("invalid action")
    if rule["comparator"] not in {"AT_OR_ABOVE", "AT_OR_BELOW"}:
        raise ValueError("invalid comparator")
    created = date.fromisoformat(rule["created_date"])
    expires = date.fromisoformat(rule["expires_on"]) if rule.get("expires_on") else None
    if as_of < created:
        raise ValueError("observation precedes rule")
    if rule.get("executed_at"):
        status = "EXECUTED_RECORDED"  # Recorded human action only, not inferred.
    elif rule.get("triggered_on"):
        status = "TRIGGERED_AWAITING_DECISION"
    elif expires and as_of > expires:
        status = "EXPIRED_REQUIRES_REVIEW"
    else:
        obs_date = date.fromisoformat(observation["date"])
        observed = obs_date >= created and obs_date <= as_of
        if rule["comparator"] == "AT_OR_ABOVE":
            price = observation.get("high", observation.get("close"))
            hit = observed and price is not None and float(price) >= float(rule["threshold"])
        else:
            price = observation.get("low", observation.get("close"))
            hit = observed and price is not None and float(price) <= float(rule["threshold"])
        status = "TRIGGERED_REQUIRES_DECISION" if hit else "WATCHING"
    return {
        "id": rule["id"], "symbol": rule["symbol"], "action": rule["action"],
        "status": status, "decision_required": status != "WATCHING" and status != "EXECUTED_RECORDED",
        "as_of": as_of.isoformat(),
        "note": "A price trigger is not an executed order. Record HOLD, CHANGE, or ACT explicitly.",
    }


def review_all(rules: list[dict], observations: dict, as_of: date) -> list[dict]:
    return [review_rule(rule, observations.get(rule["symbol"], {"date": as_of.isoformat()}), as_of)
            for rule in rules]
