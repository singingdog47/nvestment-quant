import pandas as pd

from src.portfolio_policy_report import build_policy_state, write_policy_report


def test_build_policy_state_does_not_infer_sleeves_from_names():
    df = pd.DataFrame([{"code": "5591", "name": "AVILEN", "market_value": 85000}])
    state = build_policy_state(df, {})
    assert "exploration_ratio" not in state
    assert state["holding_count"] == 1


def test_build_policy_state_uses_explicit_sleeve_and_cost_basis():
    df = pd.DataFrame([
        {"code": "5591", "market_value": 85000, "cost_basis": 85000, "sleeve": "exploration"},
        {"code": "8001", "market_value": 915000, "cost_basis": 700000, "sleeve": "satellite_core"},
    ])
    state = build_policy_state(df, {})
    assert state["exploration_ratio"] == 0.085
    assert state["satellite_core_ratio"] == 0.915
    assert state["exploration_new_capital_cost_jpy"] == 85000


def test_write_policy_report_is_private_and_creates_no_orders(tmp_path):
    path = tmp_path / "portfolio.csv"
    pd.DataFrame([{"code": "8001", "market_value": 1000000, "sleeve": "satellite_core"}]).to_csv(path, index=False)
    payload = write_policy_report(path, {}, tmp_path / "out")
    assert payload["privacy"] == "private_ephemeral_output"
    assert payload["policy"]["trade_orders_created"] is False
    assert (tmp_path / "out" / "portfolio_policy_latest.json").exists()
    assert (tmp_path / "out" / "portfolio_policy_latest.md").exists()
