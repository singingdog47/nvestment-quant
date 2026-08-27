from src.portfolio_policy import evaluate_policy


def test_exploration_cap_freezes_buys_without_forced_sale():
    result = evaluate_policy({
        "household_defensive_cash_jpy": 600000,
        "exploration_new_capital_cost_jpy": 643000,
        "exploration_ratio": 0.058,
        "satellite_core_ratio": 0.72,
        "lifestyle_benefit_ratio": 0.17,
        "tactical_cash_ratio": 0.052,
        "expected_return_definition": "geometric_cagr",
        "holding_count": 28,
    })
    assert "freeze_new_exploration_buys" in result["blocks"]
    assert "existing exploration overweight alone does not force a sale" in result["observations"]
    assert "holding_count_outside_reference_range_no_forced_trade" in result["observations"]


def test_defensive_cash_is_not_tactical_cash():
    result = evaluate_policy({
        "household_defensive_cash_jpy": 400000,
        "exploration_new_capital_cost_jpy": 100000,
        "satellite_core_ratio": 0.72,
        "lifestyle_benefit_ratio": 0.18,
        "exploration_ratio": 0.03,
        "tactical_cash_ratio": 0.07,
        "expected_return_definition": "arithmetic_expected_return",
    })
    assert "household_defensive_cash_below_minimum" in result["blocks"]


def test_tax_adjusted_sell_requires_account_and_switch_benefit():
    result = evaluate_policy({
        "household_defensive_cash_jpy": 600000,
        "exploration_new_capital_cost_jpy": 100000,
        "proposed_sell": True,
        "expected_return_definition": "geometric_cagr",
    })
    assert "withhold_tax_adjusted_sell_conclusion" in result["blocks"]
    assert "tax_adjusted_switch_benefit_required" in result["blocks"]


def test_prevent_double_volatility_drag():
    result = evaluate_policy({
        "household_defensive_cash_jpy": 600000,
        "exploration_new_capital_cost_jpy": 100000,
        "expected_return_definition": "geometric_cagr",
        "apply_volatility_drag": True,
    })
    assert "prevent_double_volatility_drag_adjustment" in result["blocks"]
