from investment_state import build_investment_state


def test_build_investment_state_keeps_private_execution_context(tmp_path):
    watch = tmp_path / "watch.csv"
    watch.write_text(
        "market,code,ticker,name,priority,status,thesis,trigger,invalidation\n"
        "JP,2585,2585.T,Life Drink,high,active,growth,1300,fcf\n"
        "JP,9999,9999.T,Inactive,high,inactive,x,y,z\n",
        encoding="utf-8",
    )
    account_inputs = {
        "status": "ok",
        "missing_input_types": [],
        "stale_input_types": [],
        "inputs": {
            "account_summary": {"total_assets_jpy": 20000000, "invested_assets_jpy": 18000000},
            "buying_power": {"cash_buying_power_jpy": 2464342},
            "orders": {"data_status": "ok", "items": [
                {"status": "執行中", "code": "2585", "name": "Life Drink", "side": "買", "quantity": 100, "limit_price_jpy": 1300},
                {"status": "取消済", "code": "8766", "name": "Tokyo Marine", "side": "買", "quantity": 100, "limit_price_jpy": 500},
            ]},
        },
    }
    state = build_investment_state(account_inputs, {"source_as_of": "2026-10-02T12:50:52+09:00"}, {},
                                   decision_context_path=tmp_path / "missing.json", watchlist_path=watch)
    assert state["capital"]["deployable_cash_jpy"] == 2464342
    assert state["open_orders"]["count"] == 1
    assert state["open_orders"]["items"][0]["code"] == "2585"
    assert state["watchlist"]["active_count"] == 1
