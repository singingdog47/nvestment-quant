import pytest

from investment_state import build_investment_state
from verified_facts_ledger import append_verified_fact


def _state(tmp_path, **kwargs):
    return build_investment_state(
        {"status": "ok", "inputs": {}}, {}, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv", **kwargs,
    )


def test_both_ledger_aliases_read_same_snapshot_once(tmp_path):
    ledger = tmp_path / "private.jsonl"
    append_verified_fact(ledger, key="bank:balance", value=100, scope="bank",
                         observed_at="2099-01-01T10:00:00+09:00",
                         evidence_ref="private:synthetic")
    state = _state(tmp_path, private_ledger_path=ledger, verified_ledger_path=ledger,
                   now="2099-01-01T11:00:00+09:00",
                   required_asset_scopes=("bank",))
    assert state["private_asset_state"] == state["verified_asset_history"]
    assert state["execution_ready"] is False


def test_conflicting_private_ledger_paths_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="Conflicting private ledger"):
        _state(tmp_path, private_ledger_path=tmp_path / "a.jsonl",
               verified_ledger_path=tmp_path / "b.jsonl")
