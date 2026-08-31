from datetime import datetime, timezone

import pandas as pd

from monthly_performance import PortfolioSnapshot, build_monthly_diagnostics


def _snapshot(day: int, price_a: float, qty_b: float = 10.0) -> PortfolioSnapshot:
    df = pd.DataFrame([
        {"holding_id": "a", "ticker": "1111.T", "name": "A", "quantity": 10, "current_price": price_a, "market_value": 10 * price_a},
        {"holding_id": "b", "ticker": "2222.T", "name": "B", "quantity": qty_b, "current_price": 50, "market_value": qty_b * 50},
    ])
    return PortfolioSnapshot(datetime(2026, 8, day, tzinfo=timezone.utc), df, f"p{day}.csv")


def test_balance_change_is_not_promoted_to_return():
    out = build_monthly_diagnostics([_snapshot(1, 100), _snapshot(31, 110)])
    assert out["status"] == "current"
    assert out["performance"]["twr_status"] == "withheld"
    assert out["performance"]["twr"] is None
    assert "external_cash_flows_missing_twr_withheld" in out["warnings"]
    assert out["attribution"]["stable_quantity_start_value_coverage"] == 1.0


def test_quantity_change_is_excluded_from_price_attribution():
    out = build_monthly_diagnostics([_snapshot(1, 100), _snapshot(31, 110, qty_b=20)])
    assert out["attribution"]["stable_quantity_start_value_coverage"] < 1.0
    b = [x for x in out["attribution"]["top_price_contributors"] if x["holding"] == "B"][0]
    assert b["quantity_stable"] is False
    assert b["estimated_price_pnl_jpy"] is None


def test_cash_flow_adjusted_residual_remains_reference_only():
    out = build_monthly_diagnostics(
        [_snapshot(1, 100), _snapshot(31, 110)],
        external_flows=[{"amount_jpy": 100.0}],
    )
    assert out["performance"]["cash_flow_adjusted_residual_status"] == "reference_only"
    assert out["performance"]["twr_status"] == "withheld"
