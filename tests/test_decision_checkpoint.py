from datetime import date
import pytest
from decision_checkpoint import review_rule, review_all


BASE = {
    "id": "sample-3500", "symbol": "TEST.T", "action": "TRIM",
    "comparator": "AT_OR_ABOVE", "threshold": 3500,
    "created_date": "2026-09-19", "expires_on": "2026-10-31"
}


def test_crossed_target_flags_decision_but_not_execution():
    o = review_rule(BASE, {"date": "2026-10-01", "high": 3935, "close": 3880},
                    date(2026, 10, 1))
    assert o["status"] == "TRIGGERED_REQUIRES_DECISION"
    assert o["decision_required"]


def test_old_trigger_never_resets_to_future_target():
    o = review_rule({**BASE, "triggered_on": "2026-10-01"},
                    {"date": "2026-10-22", "high": 2776},
                    date(2026, 10, 22))
    assert o["status"] == "TRIGGERED_AWAITING_DECISION"


def test_recorded_execution_does_not_raise_new_signal():
    o = review_rule({**BASE, "triggered_on": "2026-10-01", "executed_at": "2026-10-02"},
                    {"date": "2026-10-22", "close": 2776}, date(2026, 10, 22))
    assert o["status"] == "EXECUTED_RECORDED"
    assert not o["decision_required"]


def test_low_trigger_and_expiration():
    rule = {**BASE, "action": "BUY_REVIEW", "comparator": "AT_OR_BELOW", "threshold": 1000}
    assert review_rule(rule, {"date": "2026-10-22", "low": 999}, date(2026, 10, 22))["decision_required"]
    assert review_rule(rule, {"date": "2026-11-02", "low": 1100}, date(2026, 11, 2))["status"] == "EXPIRED_REQUIRES_REVIEW"


def test_invalid_action_rejected():
    with pytest.raises(ValueError):
        review_rule({**BASE, "action": "BROKER_BUY"}, {"date": "2026-10-22", "high": 9000},
                    date(2026, 10, 22))
