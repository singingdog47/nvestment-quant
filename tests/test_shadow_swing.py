from datetime import date

from shadow_swing import as_float, market_is_stressed, new_state


CFG = {
    "initial_cash_jpy": 1_000_000,
    "start_date": "2026-09-10",
    "end_date": "2026-12-10",
}


def test_new_state_starts_fully_in_cash():
    state = new_state(CFG)
    assert state["mode"] == "SHADOW_ONLY"
    assert state["cash_jpy"] == 1_000_000
    assert state["nav_jpy"] == 1_000_000
    assert state["positions"] == {}
    assert state["pending_orders"] == []


def test_numeric_guard_rejects_nan():
    assert as_float("nan") is None
    assert as_float("100.5") == 100.5


def test_regime_stress_gate():
    assert market_is_stressed({"stress_flag": True}) is True
    assert market_is_stressed({"regime_label": "RISK-OFF"}) is True
    assert market_is_stressed({"regime_label": "CONSTRUCTIVE", "stress_flag": False}) is False


def test_experiment_dates_are_fixed():
    state = new_state(CFG)
    assert date.fromisoformat(state["start_date"]) == date(2026, 9, 10)
    assert date.fromisoformat(state["end_date"]) == date(2026, 12, 10)
