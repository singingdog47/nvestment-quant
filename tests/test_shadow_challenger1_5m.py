"""Audited Challenger1 5m fork; no network and no brokerage integration."""
import json
from datetime import date
from pathlib import Path

import shadow_challenger1_5m as fork

SEED = Path("tests/fixtures/challenger1_5m_initial_fork_20261102.json")


def setup(tmp_path, monkeypatch):
    root = tmp_path / "data"
    dest = root / "shadow_challenger1_5m"
    dest.mkdir(parents=True)
    (dest / "state.json").write_text(SEED.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(fork, "DATA_ROOT", root)
    monkeypatch.setattr(fork, "OUT_DIR", dest)
    return dest


def test_pinned_fork_capital_and_provenance():
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    cfg = json.loads(Path("config/shadow_challenger1_5m_v1.json").read_text(encoding="utf-8"))
    state = json.loads(Path("data/shadow_challenger1_5m/state.json").read_text(encoding="utf-8"))
    assert seed["mode"] == state["mode"] == cfg["mode"] == "SHADOW_ONLY"
    assert seed["cohort"] == state["cohort"] == cfg["cohort"]
    assert seed["initial_cash_jpy"] == cfg["initial_cash_jpy"] == 5_000_000
    assert seed["fork_metadata"] == state["fork_metadata"]
    assert seed["capital_ledger"] == state["capital_ledger"]
    assert seed["fork_metadata"]["source_snapshot_date"] == "2026-11-02"
    assert seed["fork_metadata"]["source_state_blob_sha"] == "61848a18816774a03269d93abe81ef59a66202c5"
    assert seed["fork_metadata"]["capital_topup_jpy"] == 4002953.07
    assert seed["capital_ledger"][0]["counts_as_pnl"] is False
    assert seed["capital_ledger"][0]["counts_as_trade"] is False
    inherited = seed["fork_metadata"]["pre_fork_executions"]
    assert state["execution_log"][:inherited] == seed["execution_log"]
    assert all(x.get("paper_only") and x.get("source", "").startswith("verified_") for x in state["execution_log"][inherited:])
    assert abs(state["cash_jpy"] + sum(p["qty"] * p["last_price"] for p in state["positions"].values()) - state["nav_jpy"]) < 0.01


def test_holiday_is_noop_and_first_session_is_independent(tmp_path, monkeypatch):
    dest = setup(tmp_path, monkeypatch)
    old = (dest / "state.json").read_text(encoding="utf-8")
    assert fork.run(date(2026, 11, 3), bar_source=lambda s, d: None)["status"] == "OUTSIDE_SESSION"
    assert (dest / "state.json").read_text(encoding="utf-8") == old
    bars = {"8789.T": {"open": 145, "high": 147, "low": 144, "close": 146},
            "3932.T": {"open": 1300, "high": 1320, "low": 1290, "close": 1300},
            "8622.T": {"open": 763, "high": 780, "low": 750, "close": 763},
            "1306.T": {"open": 410, "high": 412, "low": 409, "close": 410}}
    result = fork.run(date(2026, 11, 4), bar_source=lambda s, d: bars.get(s))
    assert result["strategy"] == "CHALLENGER1_5M"
    assert result["cohort"] == "2026-11-04-challenger1-5m-independent-fork"
    assert result["monthly_goal"]["baseline_nav_jpy"] == 5000000
    assert result["post_fork_verified_fills"] == 1
    state = json.loads((dest / "state.json").read_text(encoding="utf-8"))
    assert state["last_run_date"] == "2026-11-04"
    assert len(state["execution_log"]) == 4
    assert fork.run(date(2026, 11, 4), bar_source=lambda s, d: bars.get(s))["status"] == "ALREADY_PROCESSED"


def test_missing_fork_never_bootstraps_empty_account(tmp_path, monkeypatch):
    import pytest
    dest = setup(tmp_path, monkeypatch)
    (dest / "state.json").unlink()
    with pytest.raises(RuntimeError, match="audited fork"):
        fork.run(date(2026, 11, 4), bar_source=lambda s, d: None)


def test_independent_5m_cli_uses_same_gap_failure_policy():
    assert fork.fork_engine.cli_exit_code({"status": "SESSION_GAP_REQUIRES_AUDIT"}) == 2
    assert fork.fork_engine.cli_exit_code({"status": "OUTSIDE_SESSION"}) == 0
