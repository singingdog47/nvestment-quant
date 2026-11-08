"""Private investment-state writeback diagnostics must not leak Drive metadata.

No Google credentials, network calls, or actual brokerage operations are used.
"""
from datetime import datetime
import json

import pandas as pd
import run_portfolio_risk as risk
from private_horizon_decision import build_private_matrix
from verified_facts_ledger import append_verified_fact


class _FakeHttpError(Exception):
    def __init__(self, status):
        super().__init__("SENSITIVE_PRIVATE_DRIVE_FILE_ID_SHOULD_NEVER_BE_LOGGED")
        self.resp = type("Response", (), {"status": status})()


def _run_with_upload(tmp_path, monkeypatch, upload):
    monkeypatch.setattr(risk, "build_investment_state", lambda *args: {"test": True})
    monkeypatch.setattr(risk, "write_investment_state", lambda state, path: path)
    monkeypatch.setattr(risk, "upload_or_replace", upload)
    return risk._write_shared_investment_state(tmp_path, {}, {}, {})


def test_writeback_http_failure_has_safe_status_but_no_private_error_text(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(risk, "_truthy_env", lambda *args: True)

    def fail(*args):
        raise _FakeHttpError(403)

    result = _run_with_upload(tmp_path, monkeypatch, fail)
    assert result["drive_writeback"] is False
    assert result["drive_writeback_status"] == "error"
    assert result["drive_writeback_http_status"] == 403
    output = capsys.readouterr().out
    assert "HttpError" in output
    assert "http_status=403" in output
    assert "SENSITIVE_PRIVATE" not in output


def test_writeback_success_is_distinct_from_history_status(tmp_path, monkeypatch):
    monkeypatch.setattr(risk, "_truthy_env", lambda *args: True)
    called = []
    result = _run_with_upload(tmp_path, monkeypatch, lambda *args: called.append(args))
    assert len(called) == 1
    assert result["drive_writeback"] is True
    assert result["drive_writeback_status"] == "ok"
    assert result["drive_writeback_http_status"] is None


def test_writeback_disabled_does_not_attempt_upload(tmp_path, monkeypatch):
    monkeypatch.setattr(risk, "_truthy_env", lambda *args: False)

    def forbidden(*args):
        raise AssertionError("Drive upload must not be called")

    result = _run_with_upload(tmp_path, monkeypatch, forbidden)
    assert result["drive_writeback"] is False
    assert result["drive_writeback_status"] == "disabled"
    assert result["drive_writeback_http_status"] is None


def test_non_http_exception_does_not_leak_details(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(risk, "_truthy_env", lambda *args: True)

    def fail(*args):
        raise ValueError("SENSITIVE_PRIVATE_DRIVE_FILE_ID_SHOULD_NEVER_BE_LOGGED")

    result = _run_with_upload(tmp_path, monkeypatch, fail)
    assert result["drive_writeback_status"] == "error"
    assert result["drive_writeback_http_status"] is None
    assert "http_status=unknown" in capsys.readouterr().out


def test_configured_ledger_passes_only_coverage_to_decisions(tmp_path, monkeypatch):
    observed = "2026-11-06T22:45:00+09:00"
    now = datetime.fromisoformat("2026-11-06T23:00:00+09:00")
    ledger = tmp_path / "facts.jsonl"
    append_verified_fact(
        ledger, key="private-order-id", value="private-order-details",
        scope="orders_domestic_cash_document", observed_at=observed,
        evidence_ref="private:sha256:" + "a" * 64,
    )
    monkeypatch.setenv("PRIVATE_VERIFIED_FACTS_LEDGER_PATH", str(ledger))
    monkeypatch.setenv("INVESTMENT_STATE_DRIVE_WRITEBACK", "false")

    shared = risk._write_shared_investment_state(tmp_path, {}, {}, {}, now=now)
    state = shared["state"]
    audit = state["private_ledger_audit"]
    assert audit["status"] == "INCOMPLETE"
    assert "orders_domestic_cash" in audit["missing_fresh_scopes"]
    assert "private-order" not in json.dumps(state)

    matrix = build_private_matrix(
        pd.DataFrame(), outlook={"as_of_jst": "2026-11-06"},
        supply_rows=[], screening_rows=[], policy={"policy": {"actionable": True}},
        investment_state=state, source_as_of=observed, now=now,
    )
    assert matrix["status"] == "partial_data"
    assert "PRIVATE_LEDGER_COVERAGE_INCOMPLETE" in matrix["execution"]["blocking_conditions"]
