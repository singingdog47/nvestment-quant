from __future__ import annotations

from copy import deepcopy
from datetime import date

import numpy as np
import pandas as pd

from src.contribution_rebalance import (
    analyze_contribution_rebalance,
    load_rebalance_policy,
    prepare_rebalance_portfolio,
)


def _fake_fetcher(symbol, start, end):
    n = 260
    idx = pd.date_range("2025-01-01", periods=n, freq="B", tz="UTC")
    t = np.arange(n, dtype=float)
    curves = {
        "QQQ": 100 + 0.18 * t + np.sin(t / 7) * 2.0,
        "VTI": 100 + 0.10 * t + np.sin(t / 11) * 1.2,
        "1306.T": 100 + 0.08 * t + np.cos(t / 13) * 1.0,
        "AAA.T": 100 + 0.06 * t + np.sin(t / 9) * 2.5,
    }
    values = curves.get(symbol)
    if values is None:
        return pd.Series(dtype=float, name=symbol)
    return pd.Series(values, index=idx, name=symbol)


def _portfolio():
    return pd.DataFrame([
        {"holding_id": "core", "asset_type": "投資信託", "name": "楽天・全米株式インデックス・ファンド(楽天・VTI)", "ticker": "", "code": "", "market_value": 4_000_000},
        {"holding_id": "growth", "asset_type": "投資信託", "name": "eMAXIS NASDAQ100インデックス", "ticker": "", "code": "", "market_value": 1_000_000},
        {"holding_id": "jp", "asset_type": "国内株式", "name": "Example", "ticker": "AAA.T", "code": "0000", "market_value": 5_000_000},
    ])


def test_proxy_rules_classify_strategic_growth_sleeve():
    prepared, quality = prepare_rebalance_portfolio(_portfolio())
    growth = prepared.loc[prepared["rebalance_bucket"].eq("growth_tilt")]
    assert len(growth) == 1
    assert growth.iloc[0]["symbol"] == "QQQ"
    assert quality["proxy_positions"] == 2


def test_calibration_required_keeps_baseline_and_never_creates_orders():
    report = analyze_contribution_rebalance(
        _portfolio(), pd.DataFrame(), as_of=date(2026, 12, 3), fetcher=_fake_fetcher
    )
    assert report["decision"]["code"] == "CALIBRATION_REQUIRED_KEEP_BASELINE"
    assert report["recommended_monthly_plan"]["growth_tilt_total_jpy"] == 50_000
    assert report["decision"]["trade_orders_created"] is False
    assert report["decision"]["broker_settings_changed"] is False


def test_outside_review_window_does_not_change_plan_even_when_forced_thresholds_exist():
    policy = deepcopy(load_rebalance_policy())
    policy["risk_model"].update({
        "threshold_status": "active",
        "mild_upper_growth_risk_contribution": 0.0,
        "severe_upper_growth_risk_contribution": 0.0,
    })
    report = analyze_contribution_rebalance(
        _portfolio(), pd.DataFrame(), policy, as_of=date(2026, 9, 7), fetcher=_fake_fetcher
    )
    assert report["decision"]["code"] == "NO_CHANGE_OUTSIDE_REVIEW_WINDOW"
    assert report["recommended_monthly_plan"]["growth_tilt_total_jpy"] == 50_000


def test_active_mild_rule_reduces_growth_to_half_and_routes_nisa_correctly():
    policy = deepcopy(load_rebalance_policy())
    policy["risk_model"].update({
        "threshold_status": "active",
        "minimum_market_data_weight_coverage": 0.50,
        "mild_upper_growth_risk_contribution": -999.0,
        "severe_upper_growth_risk_contribution": 999.0,
        "mild_upper_growth_market_value_weight": None,
        "severe_upper_growth_market_value_weight": None,
    })
    report = analyze_contribution_rebalance(
        _portfolio(), pd.DataFrame(), policy, as_of=date(2026, 12, 3), fetcher=_fake_fetcher
    )
    plan = report["recommended_monthly_plan"]
    assert report["decision"]["code"] == "REDUCE_GROWTH_TILT_TO_HALF"
    assert plan["growth_tilt_total_jpy"] == 25_000
    assert plan["diversified_core_total_jpy"] == 125_000
    assert plan["nisa_tsumitate_diversified_core_jpy"] == 100_000
    assert plan["nisa_growth_diversified_core_jpy"] == 25_000
    assert plan["nisa_growth_growth_tilt_jpy"] == 25_000
    assert plan["annual_nisa_growth_used_by_auto_contributions_jpy"] == 600_000
    assert plan["annual_nisa_growth_remaining_for_satellite_jpy"] == 1_800_000


def test_active_severe_market_weight_rule_can_reduce_growth_to_zero():
    policy = deepcopy(load_rebalance_policy())
    policy["risk_model"].update({
        "threshold_status": "active",
        "minimum_market_data_weight_coverage": 0.50,
        "mild_upper_growth_risk_contribution": None,
        "severe_upper_growth_risk_contribution": None,
        "mild_upper_growth_market_value_weight": 0.05,
        "severe_upper_growth_market_value_weight": 0.08,
    })
    report = analyze_contribution_rebalance(
        _portfolio(), pd.DataFrame(), policy, as_of=date(2026, 12, 3), fetcher=_fake_fetcher
    )
    plan = report["recommended_monthly_plan"]
    assert report["decision"]["code"] == "REDUCE_GROWTH_TILT_TO_ZERO"
    assert plan["growth_tilt_total_jpy"] == 0
    assert plan["diversified_core_total_jpy"] == 150_000
    assert plan["nisa_tsumitate_diversified_core_jpy"] == 100_000
    assert plan["nisa_growth_diversified_core_jpy"] == 50_000
