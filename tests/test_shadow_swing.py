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


def test_screen_freshness_is_independent_of_regime_date():
    import pandas as pd
    from shadow_swing import screening_is_postclose

    d = date(2026, 10, 15)
    assert not screening_is_postclose(pd.DataFrame(), d)
    assert not screening_is_postclose(
        pd.DataFrame([{"data_retrieved_at_utc": "2026-10-14T12:54:00Z"}]), d
    )
    assert not screening_is_postclose(
        pd.DataFrame([{"data_retrieved_at_utc": "2026-10-15T04:00:00Z"}]), d
    )
    assert screening_is_postclose(
        pd.DataFrame([{"data_retrieved_at_utc": "2026-10-15T08:50:00Z"}]), d
    )


def test_pending_hard_stop_missing_bar_is_visible_and_never_filled(monkeypatch, tmp_path):
    import shadow_swing as v1
    monkeypatch.setattr(v1, "OUT", tmp_path)
    monkeypatch.setattr(v1, "robust_fetch_bar", lambda *_: None)
    state = {
        "cash_jpy": 906700.0, "realized_pnl_jpy": 0.0,
        "positions": {"8622.T": {"qty": 100, "entry_price": 933.0}},
        "pending_orders": [{
            "signal_date": "2026-10-06", "side": "SELL", "symbol": "8622.T",
            "qty": 100, "order_type": "MARKET_NEXT_OPEN", "status": "PENDING"
        }]
    }
    config = {"execution": {"slippage_bps": 10, "limit_expiry_sessions": 2}}
    assert v1.process_pending(state, date(2026, 10, 7), config) == []
    assert state["pending_orders"][0]["execution_blocker"] == "MISSING_VERIFIED_OHLC"
    assert state["pending_orders"][0]["blocked_attempts"] == 1
    integrity = v1.pending_execution_integrity(state, date(2026, 10, 7), [])
    assert integrity["status"] == "BLOCKED_EXIT"
    assert "8622.T" in state["positions"]


def test_delayed_fill_records_actual_session_and_warning(monkeypatch, tmp_path):
    import shadow_swing as v1
    monkeypatch.setattr(v1, "OUT", tmp_path)
    monkeypatch.setattr(v1, "robust_fetch_bar", lambda *_: {
        "open": 813.0, "high": 820.0, "low": 810.0, "close": 816.0
    })
    state = {
        "cash_jpy": 906700.0, "realized_pnl_jpy": 0.0,
        "positions": {"8622.T": {"qty": 100, "entry_price": 933.0}},
        "pending_orders": [{
            "signal_date": "2026-10-06", "side": "SELL", "symbol": "8622.T",
            "qty": 100, "order_type": "MARKET_NEXT_OPEN", "status": "PENDING"
        }]
    }
    fills = v1.process_pending(
        state, date(2026, 10, 15),
        {"execution": {"slippage_bps": 10, "limit_expiry_sessions": 2}}
    )
    assert fills[0]["date"] == "2026-10-15"
    assert fills[0]["signal_to_fill_calendar_days"] == 9
    assert fills[0]["execution_warning"] == "DELAYED_EXECUTION"
    assert v1.pending_execution_integrity(state, date(2026, 10, 15), fills)["status"] == "DELAYED_EXECUTION"
    assert not state["pending_orders"]


def test_unverified_last_price_cannot_trigger_new_close_based_stop(monkeypatch):
    import pandas as pd
    import shadow_swing as v1
    monkeypatch.setattr(v1, "robust_fetch_bar", lambda *_: None)
    state = {
        "cash_jpy": 906700.0, "nav_jpy": 990200.0,
        "peak_nav_jpy": 1000400.0, "max_drawdown_pct": -1.0,
        "positions": {"8622.T": {
            "symbol": "8622.T", "qty": 100, "entry_price": 933.0,
            "last_price": 835.0, "peak_price": 937.0, "holding_sessions": 10
        }},
        "pending_orders": [], "status": "ACTIVE"
    }
    priced = v1.mark_to_market(state, pd.DataFrame(), date(2026, 10, 15))
    assert priced == set()
    assert state["positions"]["8622.T"]["holding_sessions"] == 10
    cfg = {"risk": {
        "hard_stop_pct": -0.06, "take_profit_pct": 0.12,
        "trailing_activation_pct": 0.08, "trailing_stop_pct": 0.05,
        "max_holding_sessions": 20
    }}
    v1.queue_mechanical_exits(
        state, date(2026, 10, 15), cfg,
        {"regime_label": "CONSTRUCTIVE", "stress_flag": False}, priced
    )
    assert state["pending_orders"] == []


def test_stale_buy_and_unsubstantiated_buy_cannot_enter(monkeypatch, tmp_path):
    import json
    import shadow_swing as v1
    monkeypatch.setattr(v1, "OUT", tmp_path)
    monkeypatch.setattr(v1, "META_CONFIG", tmp_path / "meta.json")
    (tmp_path / "meta.json").write_text(json.dumps({
        "investment_action_gate": {
            "required_for_buy_or_add": [
                "market_implied_view", "our_differing_view", "why_market_may_be_wrong",
                "catalyst_or_repricing_path", "disconfirming_condition",
                "expected_horizon", "confidence", "data_quality"
            ]
        }
    }), encoding="utf-8")
    decision_file = tmp_path / "gpt_decision_latest.json"
    base = {
        "decision_id": "old-buy", "decision_date": "2026-10-14",
        "mode": "SHADOW_ONLY", "meta_gate": {"passed": True},
        "actions": [{
            "action": "BUY", "symbol": "8622.T", "signal_price": 900,
            "target_weight_pct": 0.1, "market_implied_view": "Only a high rank"
        }]
    }
    state = {"positions": {}, "pending_orders": [], "processed_gpt_decision_ids": [],
             "cash_jpy": 1_000_000}
    cfg = {"initial_cash_jpy": 1_000_000,
           "risk": {"max_positions": 4, "max_position_pct": 0.25,
                    "max_invested_pct": 0.75, "min_cash_pct": 0.25},
           "execution": {"round_lot_shares": 100}}
    decision_file.write_text(json.dumps(base), encoding="utf-8")
    v1.ingest_gpt_decision(state, date(2026, 10, 15), cfg)
    assert not state["pending_orders"]
    base["decision_date"] = "2026-10-15"
    base["decision_id"] = "current-unsubstantiated-buy"
    decision_file.write_text(json.dumps(base), encoding="utf-8")
    v1.ingest_gpt_decision(state, date(2026, 10, 15), cfg)
    assert not state["pending_orders"]
    base["decision_id"] = "current-failed-meta"
    base["meta_gate"]["passed"] = False
    decision_file.write_text(json.dumps(base), encoding="utf-8")
    v1.ingest_gpt_decision(state, date(2026, 10, 15), cfg)
    assert not state["pending_orders"]
