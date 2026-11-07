from private_asset_state_reader import read_asset_state
from verified_facts_ledger import append_verified_facts


def _row(key, scope, value, when):
    return {"key": key, "scope": scope, "value": value,
            "observed_at": when, "evidence_ref": "private:synthetic"}


def test_fresh_balances_still_do_not_authorize_execution(tmp_path):
    path = tmp_path / "facts.jsonl"
    append_verified_facts(path, [
        _row("broker:equity:value", "equities", 100, "2099-01-02T09:00:00+09:00"),
        _row("bank:balance", "bank", 200, "2099-01-02T09:00:00+09:00"),
    ])
    state = read_asset_state(path, now="2099-01-02T10:00:00+09:00",
                             required_scopes=("equities", "bank"))
    assert state["status"] == "VERIFIED_HISTORY"
    assert state["execution_ready"] is False
    assert state["facts"]["bank:balance"]["fresh"] is True


def test_old_snapshot_never_becomes_live_cash(tmp_path):
    path = tmp_path / "facts.jsonl"
    append_verified_facts(path, [
        _row("bank:balance", "bank", 200, "2099-01-01T09:00:00+09:00")
    ])
    state = read_asset_state(path, now="2099-01-04T10:00:00+09:00",
                             required_scopes=("bank",))
    assert state["status"] == "PARTIAL"
    assert state["missing_fresh_scopes"] == ["bank"]
    assert state["facts"]["bank:balance"]["fresh"] is False
    assert state["execution_ready"] is False


def test_partial_order_scope_does_not_satisfy_account_wide_scope(tmp_path):
    path = tmp_path / "facts.jsonl"
    append_verified_facts(path, [
        _row("domestic:orders", "domestic_equity_orders", [], "2099-01-02T09:00:00+09:00")
    ])
    state = read_asset_state(path, now="2099-01-02T10:00:00+09:00",
                             required_scopes=("account_wide_orders",))
    assert state["missing_fresh_scopes"] == ["account_wide_orders"]
    assert state["execution_ready"] is False


def test_future_dated_data_is_not_fresh(tmp_path):
    path = tmp_path / "facts.jsonl"
    append_verified_facts(path, [
        _row("fx:balance", "fx", 10, "2099-01-03T10:00:00+09:00")
    ])
    state = read_asset_state(path, now="2099-01-02T10:00:00+09:00")
    assert state["facts"]["fx:balance"]["fresh"] is False


def test_missing_data_is_not_zero(tmp_path):
    state = read_asset_state(tmp_path / "missing.jsonl",
                             now="2099-01-02T10:00:00+09:00",
                             required_scopes=("bank",))
    assert state["facts"] == {}
    assert state["missing_fresh_scopes"] == ["bank"]
    assert state["execution_ready"] is False
