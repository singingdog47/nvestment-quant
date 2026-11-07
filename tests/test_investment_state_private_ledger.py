from investment_state import build_investment_state
from verified_facts_ledger import append_verified_fact


def _build(tmp_path, ledger, *, now, required_scopes=()):
    return build_investment_state(
        {"status": "ok", "inputs": {"buying_power": {"cash_buying_power_jpy": 999999}}},
        {"source_as_of": "2099-01-01T10:00:00+09:00"},
        {"status": "ok"},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
        private_ledger_path=ledger,
        now=now,
        required_asset_scopes=required_scopes,
    )


def test_empty_private_ledger_is_not_verified(tmp_path):
    state = _build(tmp_path, tmp_path / "missing.jsonl",
                   now="2099-01-01T11:00:00+09:00")
    assert state["private_asset_state"]["status"] == "PARTIAL"
    assert state["private_asset_state"]["facts"] == {}
    assert state["execution_ready"] is False


def test_verified_history_visible_but_never_execution_ready(tmp_path):
    ledger = tmp_path / "private.jsonl"
    append_verified_fact(
        ledger, key="bank:balance", value=100, scope="bank",
        observed_at="2099-01-01T10:00:00+09:00",
        evidence_ref="private:synthetic",
    )
    state = _build(tmp_path, ledger, now="2099-01-01T11:00:00+09:00",
                   required_scopes=("bank", "crypto"))
    assert state["private_asset_state"]["facts"]["bank:balance"]["value"] == 100
    assert state["private_asset_state"]["missing_fresh_scopes"] == ["crypto"]
    assert state["private_asset_state"]["status"] == "PARTIAL"
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["execution_ready"] is False


def test_stale_private_history_never_enables_execution(tmp_path):
    ledger = tmp_path / "private.jsonl"
    append_verified_fact(
        ledger, key="cash", value=100, scope="bank",
        observed_at="2099-01-01T10:00:00+09:00",
        evidence_ref="private:synthetic",
    )
    state = _build(tmp_path, ledger, now="2099-01-04T10:00:00+09:00",
                   required_scopes=("bank",))
    assert state["private_asset_state"]["status"] == "PARTIAL"
    assert state["private_asset_state"]["stale_or_future_keys"] == ["cash"]
    assert state["execution_ready"] is False
