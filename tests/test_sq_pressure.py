from datetime import date

from market_regime.sq_pressure import build_sq_execution_overlay, next_major_sq_date, second_friday


def _cfg():
    return {
        "enabled": True,
        "major_months": [3, 6, 9, 12],
        "activation_calendar_days": 6,
        "caution_cap_points": 15,
        "max_input_age_days": 3,
        "pin_distance_window_pct": 0.03,
    }


def test_second_friday_and_next_major_sq_2026_september():
    assert second_friday(2026, 9) == date(2026, 9, 11)
    assert next_major_sq_date(date(2026, 9, 8)) == date(2026, 9, 11)


def test_calendar_only_overlay_is_non_directional_and_low_impact():
    overlay = build_sq_execution_overlay(date(2026, 9, 8), 66399.84, _cfg(), {})
    assert overlay["active"] is True
    assert overlay["days_to_sq"] == 3
    assert overlay["directional_bias"] == "UNDETERMINED"
    assert overlay["data_status"] == "partial"
    assert overlay["execution_caution_points"] < 5
    assert overlay["policy_effects"]["alter_security_ranking"] is False
    assert overlay["policy_effects"]["alter_fundamental_score"] is False
    assert overlay["policy_effects"]["use_for_execution_timing_only"] is True


def test_structured_oi_input_increases_evidence_without_claiming_direction():
    manual = {
        "as_of_date": "2026-09-08",
        "option_put_oi": 140000,
        "option_call_oi": 100000,
        "front_futures_oi": 80000,
        "next_futures_oi": 20000,
        "put_wall": 65000,
        "call_wall": 67000,
        "magnet_strike": 66000,
        "arbitrage_balance_zscore": 1.5,
        "nikkei_vi_percentile": 0.80,
    }
    calendar_only = build_sq_execution_overlay(date(2026, 9, 8), 66399.84, _cfg(), {})
    overlay = build_sq_execution_overlay(date(2026, 9, 8), 66399.84, _cfg(), manual)
    assert overlay["data_status"] == "ok"
    assert round(overlay["evidence"]["put_call_oi_ratio"], 2) == 1.40
    assert round(overlay["evidence"]["front_futures_share"], 2) == 0.80
    assert overlay["confidence"] > calendar_only["confidence"]
    assert overlay["execution_caution_points"] > calendar_only["execution_caution_points"]
    assert overlay["directional_bias"] == "UNDETERMINED"


def test_outside_activation_window_has_no_execution_adjustment():
    overlay = build_sq_execution_overlay(date(2026, 8, 20), 65000, _cfg(), {})
    assert overlay["active"] is False
    assert overlay["execution_caution_points"] == 0
    assert overlay["execution_stance"] == "NORMAL"


def test_stale_manual_input_is_not_used_for_scoring():
    manual = {
        "as_of_date": "2026-08-30",
        "option_put_oi": 300000,
        "option_call_oi": 100000,
        "front_futures_oi": 90000,
        "next_futures_oi": 10000,
    }
    overlay = build_sq_execution_overlay(date(2026, 9, 8), 66399.84, _cfg(), manual)
    assert overlay["manual_input_freshness"] == "stale"
    assert overlay["data_status"] == "stale"
    assert overlay["evidence"]["put_call_oi_ratio"] is None
    assert overlay["evidence"]["front_futures_share"] is None
