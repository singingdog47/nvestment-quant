import json
from pathlib import Path

import pytest

from src import private_decision_monitor as monitor
from src.decision_journal import append_event, instant, replay
from src.private_drive import _is_generated_private_output

PLAN = dict(id="p1", type="PLAN", symbol="PRIVATE-SAMPLE", recorded_at="2026-11-08T12:00:00+09:00",
            recommendation="HOLD", rationale="Private rationale", evidence="Private source",
            falsifier="Review new evidence by deadline", basis="TIME", review_by="2026-11-09T10:00:00+09:00")


def test_time_plan_and_approaching_then_overdue(tmp_path):
    path = tmp_path / "journal.jsonl"
    append_event(path, PLAN)
    early = monitor.audit_file(path, instant("2026-11-09T07:50:00+09:00"))
    assert early["status"] == "REVIEW_REQUIRED"
    assert early["items"][0]["due_soon"] and not early["items"][0]["overdue"]
    late = monitor.audit_file(path, instant("2026-11-09T10:50:00+09:00"))
    assert late["items"][0]["status"] == "OVERDUE_REQUIRES_REVIEW"
    assert late["items"][0]["overdue"]


def test_time_plan_cannot_hide_price_conditions():
    with pytest.raises(ValueError, match="TIME plans"):
        replay([{**PLAN, "threshold": 100}], instant("2026-11-09T07:00:00+09:00"))


def test_real_download_audit_upload_boundary(tmp_path, monkeypatch):
    source = tmp_path / "source.jsonl"
    append_event(source, PLAN)
    before = source.read_bytes()
    uploads = []
    def download(name, destination, **kwargs):
        assert name == "decision_journal.jsonl" and kwargs["require_unique"]
        return source
    def upload(path, name, mime):
        uploads.append((name, Path(path).read_text()))
    monkeypatch.setattr(monitor, "download_named", download)
    monkeypatch.setattr(monitor, "upload_or_replace", upload)
    result = monitor.run_monitor(tmp_path / "out", as_of=instant("2026-11-09T10:50:00+09:00"), writeback=True)
    assert result == {"status": "REVIEW_REQUIRED", "writeback": "SUCCESS"}
    assert "PRIVATE-SAMPLE" not in json.dumps(result)
    assert len(uploads) == 2 and "OVERDUE_REQUIRES_REVIEW" in uploads[0][1]
    assert source.read_bytes() == before  # monitor never mutates the producer's journal


@pytest.mark.parametrize("error,status", [(FileNotFoundError("private-id"), "MISSING_JOURNAL"),
    (ValueError("private-id"), "UNAVAILABLE_OR_INVALID")])
def test_missing_or_invalid_does_not_reuse_previous_success(tmp_path, monkeypatch, error, status):
    (tmp_path / monitor.REPORT).write_text('{"status":"TRACKING"}')
    def fail(*args, **kwargs):
        raise error
    monkeypatch.setattr(monitor, "download_named", fail)
    result = monitor.run_monitor(tmp_path)
    assert result["status"] == status
    written = (tmp_path / monitor.REPORT).read_text()
    assert "TRACKING" not in written and "private-id" not in written
    assert json.loads(written)["items"] == []


def test_writeback_failure_is_visible_without_leaking_error(tmp_path, monkeypatch):
    source = tmp_path / "source.jsonl"
    append_event(source, PLAN)
    def fail(*args):
        raise RuntimeError("private-url-and-secret")
    monkeypatch.setattr(monitor, "upload_or_replace", fail)
    result = monitor.run_monitor(tmp_path / "out", journal_path=source, writeback=True)
    assert result["writeback"] == "FAILED" and "secret" not in str(result)


def test_empty_journal_not_reported_as_all_clear(tmp_path):
    path = tmp_path / "empty.jsonl"
    path.write_text("")
    assert monitor.audit_file(path, instant("2026-11-09T10:00:00+09:00"))["status"] == "NO_PLANS"


def test_monitor_files_are_excluded_from_broker_import():
    for name in [monitor.JOURNAL, monitor.REPORT, "decision_monitor_latest.md"]:
        assert _is_generated_private_output(name)
