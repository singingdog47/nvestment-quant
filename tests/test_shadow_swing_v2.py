from datetime import date
import json

import shadow_swing_v2 as v2


DAY = date(2026, 10, 15)
CFG = {
    "cohort": "unit-v2", "mode": "SHADOW_ONLY",
    "initial_cash_jpy": 5_000_000, "start_date": "2026-10-15",
    "end_date": "2027-01-15",
    "execution": {
        "slippage_bps": 15, "round_lot_shares": 100, "max_open_gap_pct": 3,
        "expiry_calendar_days": 4, "max_turnover_participation_pct": 2
    },
    "risk": {
        "max_positions": 8, "max_positions_per_theme": 2,
        "max_new_entries_per_session": 2, "max_position_pct": 0.125,
        "max_gross_invested_pct": 0.80, "uncertainty_size_multiplier": 0.5,
        "stop_loss_pct": 5, "take_profit_pct": 10, "max_holding_sessions": 10
    },
    "gate": {
        "min_total_score": 68, "min_momentum_score": 60,
        "min_risk_score": 42, "min_liquidity_score": 48,
        "min_return_1m_pct": 3, "min_return_3m_pct": 0,
        "max_return_1m_pct": 45, "min_avg_turnover_jpy": 100_000_000,
        "min_history_sessions": 4, "max_price_source_disagreement_pct": 3,
        "audit_top_japan_candidates": 80
    }
}


def screen():
    return {
        "ticker": "1234.T", "name": "Example company",
        "market": "JP", "eligible": "True", "research_candidate": "True",
        "data_retrieved_at_utc": "2026-10-15T07:50:00+00:00",
        "price": "110", "total_score": "80", "momentum_score": "78",
        "risk_score": "65", "liquidity_score": "70",
        "return_1m": "15", "return_3m": "25", "theme": "Industrial",
    }


def supply():
    return {
        "ticker": "1234.T", "observed_date": "2026-10-15",
        "price_as_of": "2026-10-15T06:30:00+00:00",
        "data_status": "ok", "current_price": "110",
        "avg_turnover_30d": "300000000", "current_volume_ratio_30d": "1.5",
        "daily_change_pct": "0.02", "context_flags": "NO_EXCEPTION",
        "short_percent_float": "", "days_to_cover": "",
        "short_interest_change_ratio": "", "data_quality_flags": ""
    }


def test_initial_capital_is_separate_from_v1():
    s = v2.initial_state(CFG)
    assert s["initial_cash_jpy"] == 5_000_000
    assert s["nav_jpy"] == 5_000_000
    assert s["positions"] == {}
    assert s["cohort"] == "unit-v2"
    assert s["mode"] == "SHADOW_ONLY"


def test_adversarial_gate_requires_positive_demand_not_just_high_score():
    p = supply()
    p["daily_change_pct"] = "-0.012"
    p["current_volume_ratio_30d"] = "1.0"
    audit = v2.evaluate_candidate(screen(), p, [100, 102, 106, 109], CFG, DAY)
    assert not audit["eligible"]
    assert "no_positive_demand_confirmation" in audit["vetoes"]
    assert audit["do_nothing_baseline"]
    assert audit["strongest_bear_case"]


def test_valid_breakout_with_unknown_short_positions_gets_uncertainty_flag():
    audit = v2.evaluate_candidate(screen(), supply(), [101, 102, 105, 108], CFG, DAY)
    assert audit["eligible"]
    assert audit["demand_mode"] == "volume_confirmed_breakout"
    assert "short_and_margin_positioning_unverified" in audit["unknowns"]


def test_stale_prices_and_source_mismatch_are_hard_vetoes():
    p = supply()
    p["price_as_of"] = "2026-10-14T06:30:00+00:00"
    p["current_price"] = "145"
    audit = v2.evaluate_candidate(screen(), p, [101, 102, 105, 108], CFG, DAY)
    assert "exchange_price_timestamp_stale" in audit["vetoes"]
    assert "price_source_disagreement" in audit["vetoes"]


def test_crowded_shorts_not_overridden_by_high_factor_score():
    p = supply()
    p["context_flags"] = "SHORT_CROWDING"
    audit = v2.evaluate_candidate(screen(), p, [101, 102, 105, 108], CFG, DAY)
    assert not audit["eligible"]
    assert "short_crowding_requires_manual_review" in audit["vetoes"]


def test_history_filters_future_data_and_stale_market_timestamps():
    rows = [
        {"ticker": "1234.T", "observed_date": "2026-10-13",
         "price_as_of": "2026-10-13T06:30:00+00:00", "current_price": "100"},
        {"ticker": "1234.T", "observed_date": "2026-10-14",
         "price_as_of": "2026-10-13T06:30:00+00:00", "current_price": "105"},
        {"ticker": "1234.T", "observed_date": "2026-10-16",
         "price_as_of": "2026-10-16T06:30:00+00:00", "current_price": "120"},
    ]
    assert v2.history_for_symbol(rows, "1234.T", DAY) == [100]


def setup_run(monkeypatch, tmp_path):
    monkeypatch.setattr(v2, "ROOT", tmp_path)
    monkeypatch.setattr(v2, "OUT", tmp_path / "shadow_swing_v2")
    monkeypatch.setattr(v2, "CFG_PATH", tmp_path / "config.json")
    v2.save_json(v2.CFG_PATH, CFG)


def test_market_feed_failure_blocks_new_entries_without_fabricated_fills(monkeypatch, tmp_path):
    setup_run(monkeypatch, tmp_path)
    monkeypatch.setattr(v2, "fetch_bar", lambda *a: None)
    report = v2.run(DAY)
    assert "benchmark_bar_unavailable" in report["market_data_blockers"]
    state = v2.read_json(v2.OUT / "state.json")
    assert state["nav_jpy"] == 5_000_000
    assert state["completed_trades"] == 0
    assert state["pending_buys"] == []


def test_intraday_stop_counts_actual_closed_trade_with_cost(monkeypatch, tmp_path):
    setup_run(monkeypatch, tmp_path)
    state = v2.initial_state(CFG)
    state["cash_jpy"] -= 100000
    state["positions"] = {
        "1234.T": {"entry_date": "2026-10-14", "entry_price": 100,
                   "last_price": 100, "qty": 1000, "holding_sessions": 2,
                   "theme": "Other", "unknowns": [], "demand_mode": "breakout"}
    }
    v2.save_json(v2.OUT / "state.json", state)
    def fake(symbol, day):
        if symbol == "1306.T":
            return {"open": 100, "high": 101, "low": 99, "close": 100}
        return {"open": 100, "high": 101, "low": 94, "close": 97}
    monkeypatch.setattr(v2, "fetch_bar", fake)
    result = v2.run(DAY)
    assert result["completed_trades"] == 1
    assert not v2.read_json(v2.OUT / "state.json")["positions"]
    assert result["nav_jpy"] < 5_000_000
    assert any(x["event"] == "SELL_FILLED" and x["reason"] == "intraday_stop"
               for x in result["events"])


def test_time_exit_cannot_fill_using_same_sessions_open(monkeypatch, tmp_path):
    setup_run(monkeypatch, tmp_path)
    state = v2.initial_state(CFG)
    state["cash_jpy"] -= 100000
    state["positions"] = {
        "1234.T": {"entry_date": "2026-10-01", "entry_price": 100,
                   "last_price": 100, "qty": 1000, "holding_sessions": 9,
                   "theme": "Other", "unknowns": [], "demand_mode": "trend"}
    }
    v2.save_json(v2.OUT / "state.json", state)
    monkeypatch.setattr(v2, "fetch_bar", lambda symbol, day:
        {"open": 102, "high": 103, "low": 99, "close": 101})
    first = v2.run(DAY)
    assert first["completed_trades"] == 0
    saved = v2.read_json(v2.OUT / "state.json")
    assert saved["positions"]["1234.T"]["exit_signal_date"] == DAY.isoformat()
    second = v2.run(date(2026, 10, 16))
    assert second["completed_trades"] == 1
    assert any(x["reason"] == "time_exit" for x in second["events"] if x["event"] == "SELL_FILLED")
