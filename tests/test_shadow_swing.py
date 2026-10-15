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



def test_legacy_hard_stop_uses_independent_ohlc_fallback_without_retrofill(monkeypatch, tmp_path):
    import shadow_swing as v1
    import shadow_swing_v2 as v2

    monkeypatch.setattr(v1, "OUT", tmp_path)
    monkeypatch.setattr(v1, "fetch_bar", lambda *_: None)
    monkeypatch.setattr(v2, "verified_daily_bar", lambda *_: {
        "open": 819.0, "high": 822.0, "low": 810.0, "close": 815.0
    })
    cfg = {"execution": {"slippage_bps": 10, "limit_expiry_sessions": 2}}
    state = {
        "cash_jpy": 906700.0, "realized_pnl_jpy": 0.0,
        "positions": {"8622.T": {"qty": 100, "entry_price": 933.0}},
        "pending_orders": [{
            "signal_date": "2026-10-06", "side": "SELL", "symbol": "8622.T",
            "qty": 100, "order_type": "MARKET_NEXT_OPEN",
            "reason": "hard_stop", "status": "PENDING"
        }]
    }
    fills = v1.process_pending(state, date(2026, 10, 15), cfg)
    assert len(fills) == 1
    assert fills[0]["date"] == "2026-10-15"  # No imaginary 10/07 fill.
    assert fills[0]["fill_price"] == round(819.0 * 0.999, 4)
    assert fills[0]["realized_pnl_jpy"] < 0
    assert not state["positions"]
    assert not state["pending_orders"]
