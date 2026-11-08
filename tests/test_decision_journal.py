import json
from copy import deepcopy

import pytest

from src.decision_journal import append_event, instant, replay


PLAN = dict(id="plan-1", type="PLAN", symbol="SAMPLE.T",
            recorded_at="2026-11-02T08:00:00+09:00", recommendation="HOLD",
            rationale="Test thesis", falsifier="Close below threshold",
            evidence="Synthetic test fixture", basis="CLOSE", comparator="AT_OR_BELOW",
            threshold=100, review_by="2026-11-04T16:00:00+09:00")
OBS = dict(id="obs-1", type="OBSERVATION", symbol="SAMPLE.T", plan_id="plan-1",
           recorded_at="2026-11-04T15:40:00+09:00", observed_at="2026-11-04T15:30:00+09:00",
           close=99, low=90, evidence="Synthetic close")
REVIEW = dict(id="review-1", type="REVIEW", symbol="SAMPLE.T", plan_id="plan-1",
              recorded_at="2026-11-04T16:00:00+09:00", recommendation="HOLD",
              reason="New evidence preserves thesis", evidence="Synthetic evidence",
              resolves="obs-1", review_by="2026-11-05T12:00:00+09:00")


def audit(events, at="2026-11-04T16:00:00+09:00"):
    return replay(events, instant(at))[0]


def test_close_rule_does_not_trigger_on_intraday_dip():
    assert audit([PLAN, {**OBS, "close": 101}], "2026-11-04T15:45:00+09:00")["status"] == "WATCHING"
    assert audit([{**PLAN, "basis": "INTRADAY"}, {**OBS, "close": 101}])["trigger_id"] == "obs-1"


def test_trigger_persists_through_rebound_and_deadline():
    rebound = {**OBS, "id": "obs-2", "recorded_at": "2026-11-05T15:40:00+09:00",
               "observed_at": "2026-11-05T15:30:00+09:00", "close": 105}
    row = audit([PLAN, OBS, rebound], "2026-11-06T08:00:00+09:00")
    assert row["status"] == "TRIGGERED_AWAITING_DECISION"
    assert row["overdue"] and row["trigger_id"] == "obs-1"


def test_hold_resolves_trigger_but_requires_new_deadline():
    assert audit([PLAN, OBS, REVIEW])["status"] == "WATCHING"
    assert audit([PLAN, OBS, REVIEW], "2026-11-05T12:00:00+09:00")["status"] == "OVERDUE_REQUIRES_REVIEW"


@pytest.mark.parametrize("field,value", [("reason", ""), ("evidence", ""),
    ("review_by", "2026-11-04T15:00:00+09:00"), ("resolves", "wrong"),
    ("recommendation", "REVIEW")])
def test_incomplete_conclusions_rejected(field, value):
    with pytest.raises(ValueError):
        audit([PLAN, OBS, {**REVIEW, field: value}])


def test_revision_requires_reason_and_active_predecessor():
    changed = {**PLAN, "id": "plan-2", "recorded_at": "2026-11-04T16:00:00+09:00",
               "threshold": 90, "supersedes": "plan-1",
               "review_by": "2026-11-05T16:00:00+09:00"}
    with pytest.raises(ValueError, match="change_reason"):
        audit([PLAN, OBS, changed])
    assert audit([PLAN, OBS, {**changed, "change_reason": "Revised thesis with new evidence"}])["plan_id"] == "plan-2"
    with pytest.raises(ValueError, match="active plan"):
        audit([PLAN, {**changed, "supersedes": "absent"}])


def test_as_of_does_not_use_future_review_or_revision():
    assert audit([PLAN, OBS, REVIEW], "2026-11-04T15:45:00+09:00")["status"] == "TRIGGERED_AWAITING_DECISION"
    assert audit([PLAN, OBS], "2026-11-03T08:00:00+09:00")["status"] == "NO_OBSERVATION"


def test_action_is_recommendation_not_inferred_fill():
    assert audit([PLAN, OBS, {**REVIEW, "recommendation": "EXIT"}])["status"] == "ACTION_RECOMMENDED"


@pytest.mark.parametrize("value", [None, float("nan"), float("inf"), -1, True])
def test_invalid_close_not_treated_as_safe(value):
    with pytest.raises((ValueError, TypeError)):
        audit([PLAN, {**OBS, "close": value}])


def test_future_and_preplan_observations_rejected():
    for observed in ["2026-11-01T15:30:00+09:00", "2026-11-05T15:30:00+09:00"]:
        with pytest.raises(ValueError):
            audit([PLAN, {**OBS, "observed_at": observed}])
    with pytest.raises(ValueError):
        audit([PLAN, {**OBS, "recorded_at": "2026-11-04T15:40:00"}])


def test_append_rejection_preserves_history(tmp_path):
    path = tmp_path / "private.jsonl"
    append_event(path, PLAN)
    before = path.read_bytes()
    with pytest.raises(ValueError):
        append_event(path, PLAN)
    assert path.read_bytes() == before
    append_event(path, OBS)
    append_event(path, REVIEW)
    assert len(path.read_text().splitlines()) == 3
    assert path.stat().st_mode & 0o777 == 0o600
    assert audit([json.loads(line) for line in path.read_text().splitlines()])["last_review"] == "review-1"


def test_repeated_trigger_requires_another_review():
    again = {**OBS, "id": "obs-2", "recorded_at": "2026-11-05T10:00:00+09:00",
             "observed_at": "2026-11-05T09:59:00+09:00"}
    assert audit([PLAN, OBS, REVIEW, again], "2026-11-05T10:01:00+09:00")["trigger_id"] == "obs-2"


def test_out_of_order_events_rejected():
    with pytest.raises(ValueError, match="chronological"):
        audit([PLAN, REVIEW, OBS])


def test_review_cannot_silently_change_threshold():
    with pytest.raises(ValueError, match="new PLAN"):
        audit([PLAN, OBS, {**REVIEW, "threshold": 90}])


def test_journal_cli_end_to_end(tmp_path):
    import subprocess
    import sys
    path = tmp_path / "journal.jsonl"
    event_path = tmp_path / "event.json"
    for event in [PLAN, OBS, REVIEW]:
        event_path.write_text(json.dumps(event), encoding="utf-8")
        subprocess.run([sys.executable, "-m", "src.decision_journal", str(path),
                        "append", str(event_path)], check=True)
    result = subprocess.run([sys.executable, "-m", "src.decision_journal", str(path),
        "audit", "--as-of", "2026-11-05T12:00:00+09:00"], check=True, capture_output=True, text=True)
    assert json.loads(result.stdout)[0]["status"] == "OVERDUE_REQUIRES_REVIEW"


def test_changed_timing_or_recommendation_requires_revision_link():
    changed = {**PLAN, "id": "plan-2", "recommendation": "EXIT",
               "recorded_at": "2026-11-02T09:00:00+09:00"}
    with pytest.raises(ValueError, match="active plan"):
        audit([PLAN, changed])


def test_observation_older_than_review_cannot_reopen_resolved_trigger():
    stale = {**OBS, "id": "late-copy", "recorded_at": "2026-11-04T17:00:00+09:00",
             "observed_at": "2026-11-04T15:45:00+09:00"}
    with pytest.raises(ValueError, match="latest review"):
        audit([PLAN, OBS, REVIEW, stale])
