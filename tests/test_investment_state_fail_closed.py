import pytest

from investment_state import build_investment_state


def test_buying_power_is_not_deployable_cash(tmp_path):
    state = build_investment_state(
        {"status": "ok", "inputs": {
            "account_summary": {"cash_deposit_jpy": 50000},
            "buying_power": {"cash_buying_power_jpy": 2000000},
            "orders": {"items": [], "data_status": "ok"}}},
        {"source_as_of": "2099-01-01T10:00:00+09:00"},
        {"status": "ok"},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["open_orders"]["account_wide_coverage_verified"] is False
    assert state["execution_ready"] is False
    assert "deployable_cash_not_verified" in state["execution_blockers"]


@pytest.mark.parametrize("orders", [
    {},
    {"data_status": "ok"},
    {"data_status": "stale", "items": [{"status": "執行中"}]},
    {"data_status": "ok", "items": [{"status": ""}]},
])
def test_unavailable_order_rows_do_not_imply_zero_orders(orders, tmp_path):
    state = build_investment_state(
        {"inputs": {"orders": orders}}, {}, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert state["open_orders"]["count"] is None
