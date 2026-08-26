from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import pandas as pd

from src.portfolio_risk import (
    RiskConfig,
    analyze,
    candidate_impact,
    concentration_stats,
    historical_var_cvar,
    fx_sensitivity_matrix,
    position_weighted_shock,
    resilience_score,
    validate_private_profile,
    write_private_report,
    classify_treasury_operation,
    cause_scenarios,
    max_drawdown,
    normalize_portfolio,
)


def test_normalize_market_value_to_weights():
    p = pd.DataFrame({"code": ["4063", "9433"], "market": ["JP", "JP"], "market_value": [60, 40]})
    x = normalize_portfolio(p)
    assert round(float(x["weight"].sum()), 8) == 1.0
    assert list(x["symbol"]) == ["4063.T", "9433.T"]


def test_basic_risk_math():
    r = pd.Series([0.01, -0.02, 0.015, -0.005] * 30, dtype=float)
    var, cvar = historical_var_cvar(r, 0.95)
    assert var is not None and var >= 0
    assert cvar is not None and cvar >= var
    assert max_drawdown(r) is not None
    c = concentration_stats(pd.Series([0.5, 0.3, 0.2]))
    assert round(c["hhi"], 2) == 0.38
    assert c["effective_holdings"] > 2


def test_candidate_impact_has_portfolio_level_verdict():
    n = 180
    idx = pd.date_range("2026-01-01", periods=n, freq="B", tz="UTC")
    rng = np.random.default_rng(3)
    base = rng.normal(0.0003, 0.012, n)
    returns = pd.DataFrame({
        "AAA": base,
        "BBB": base * 0.8 + rng.normal(0, 0.004, n),
        "CCC": -base * 0.15 + rng.normal(0.0002, 0.006, n),
        "1306.T": base * 0.9 + rng.normal(0, 0.003, n),
    }, index=idx)
    p = normalize_portfolio(pd.DataFrame({"ticker": ["AAA", "BBB"], "weight": [0.7, 0.3]}))
    x = candidate_impact(p, returns, "CCC", 0.10, "1306.T", 0.95)
    assert x["status"] == "ok"
    assert x["verdict"] in {"IMPROVES", "NEUTRAL", "WORSENS"}
    assert x["after_hhi"] < x["before_hhi"]


def test_analyze_reports_missing_metadata_without_inference():
    idx = pd.date_range("2025-01-01", periods=260, freq="B", tz="UTC")
    curves = {
        "4063.T": np.linspace(100, 120, len(idx)),
        "9433.T": np.linspace(100, 112, len(idx)) + np.sin(np.arange(len(idx))) * 2,
        "6701.T": np.linspace(100, 130, len(idx)) + np.cos(np.arange(len(idx))) * 3,
        "1306.T": np.linspace(100, 118, len(idx)) + np.sin(np.arange(len(idx)) / 4),
    }
    def fake_fetch(symbol, start, end):
        return pd.Series(curves[symbol], index=idx, name=symbol)

    portfolio = pd.DataFrame({
        "code": ["4063", "9433"], "market": ["JP", "JP"],
        "weight": [0.55, 0.45], "sector": ["Materials", "Telecom"],
    })
    screen = pd.DataFrame({
        "code": ["6701"], "market": ["JP"], "name": ["NEC"],
        "total_score": [80], "quality_score": [75], "momentum_score": [82],
    })
    report = analyze(portfolio, screen, RiskConfig(candidate_top_n=1), fetcher=fake_fetch)
    assert report["version"] == "1.9.0"
    assert report["privacy"] == "PRIVATE_OUTPUT_ONLY"
    assert report["portfolio"]["metrics"]["status"] in {"ok", "partial"}
    assert report["portfolio"]["metadata_exposures"]["currency"] == {}
    assert report["portfolio"]["metadata_exposures"]["rate_sensitivity"]["coverage"] == 0.0
    assert len(report["candidate_impact"]) == 1


def test_analyze_accepts_empty_screen_without_dropping_unpriced_holdings():
    portfolio = pd.DataFrame({
        "holding_id": ["stock", "fund"], "ticker": ["4063.T", ""],
        "name": ["Stock", "Fund"], "market_value": [600_000, 400_000],
    })
    def no_prices(symbol, start, end):
        return pd.Series(dtype=float, name=symbol)
    report = analyze(portfolio, pd.DataFrame(), fetcher=no_prices)
    assert report["portfolio"]["holdings"] == 2
    assert report["data_quality"]["portfolio_price_symbol_coverage_ratio"] == 0.6
    assert report["candidate_impact"] == []


def test_direct_fx_matrix_excludes_em_basket_and_matches_position_value():
    p = pd.DataFrame({
        "ticker": ["VTI", "EMFUND", "1306.T"],
        "market_value": [4_800_000, 3_200_000, 12_000_000],
        "fx_beta_usdjpy": [1.0, np.nan, 0.0],
    })
    x = fx_sensitivity_matrix(p, 160.0, (157, 155, 152, 150), total_assets=22_000_000)
    assert x["usdjpy_beta_equivalent_jpy"] == 4_800_000
    assert round(x["impact_per_one_yen_down_jpy"]) == -30_000
    assert round(x["scenarios"][-1]["direct_fx_impact_jpy"]) == -300_000
    assert round(x["scenarios"][-1]["impact_pct_total_assets"] * 100, 2) == -1.36


def test_small_tlt_position_cannot_be_reported_as_large_hedge():
    p = pd.DataFrame({"ticker": ["TLT", "VTI"], "market_value": [200_000, 19_800_000]})
    x = position_weighted_shock(p, "TLT", 0.15, total_assets=22_000_000)
    assert x["impact_jpy"] == 30_000
    assert round(x["portfolio_weight"] * 100, 2) == 0.91
    assert x["weight_basis"] == "total_assets"


def test_resilience_and_treasury_semantics():
    x = resilience_score(22_000_000, 7_000_000, 1_800_000, 600_000, 1_400_000)
    assert x["score"] is None
    assert x["score_status"] == "not_scored_without_validated_rubric"
    assert round(x["shock_loss_pct_unrealized_gain"] * 100, 1) == 20.0
    op = classify_treasury_operation("treasury_buyback")
    assert op["is_qe"] is False
    assert op["is_monetization"] is False
    assert classify_treasury_operation("buyback")["classification"] == "unclassified"


def test_cause_scenarios_report_coverage_and_natural_hedge():
    p = pd.DataFrame({
        "ticker": ["VTI", "BANK.T", "RETAIL.T", "EMFUND"],
        "market_value": [5_000_000, 2_000_000, 2_300_000, 2_800_000],
        "fx_beta_usdjpy": [1.0, 0.0, 0.0, np.nan],
        "scenario_return_boj_hike": [-.03, .08, .05, np.nan],
        "scenario_return_basis_boj_hike": ["local_currency", "jpy_nav", "jpy_nav", ""],
    })
    x = cause_scenarios(p, 159, [{"id": "boj_hike", "target_usdjpy": 155}], 22_000_000)[0]
    # Domestic bank/retail gains partially offset VTI local-price and FX losses.
    assert x["asset_return_impact_jpy"] == 125_000
    assert x["direct_fx_impact_jpy"] < 0
    assert 0 < x["assumption_coverage_ratio"] < 1
    assert x["status"] == "non_actionable"
    assert x["estimated_total_impact_jpy"] is None


def test_jpy_nav_scenario_does_not_double_count_fx():
    p = pd.DataFrame({
        "ticker": ["VTI"], "market_value": [5_000_000], "fx_beta_usdjpy": [1.0],
        "scenario_return_us_recession": [-.12], "scenario_return_basis_us_recession": ["jpy_nav"],
    })
    x = cause_scenarios(p, 159, [{"id": "us_recession", "target_usdjpy": 150,
                                  "coefficient_status": "validated_oos"}], 10_000_000)[0]
    assert x["status"] == "actionable"
    assert x["asset_return_impact_jpy"] == -600_000
    assert x["direct_fx_impact_jpy"] == 0
    assert x["estimated_total_impact_jpy"] == -600_000


def test_private_profile_freshness_and_reconciliation_gate():
    now = datetime(2026, 8, 26, 12, tzinfo=timezone.utc)
    good = {
        "enabled": True, "as_of_jst": "2026-08-26T18:00:00+09:00",
        "base_usdjpy": 159, "base_usdjpy_as_of_jst": "2026-08-26T18:00:00+09:00",
        "total_assets_jpy": 1_100_000, "invested_assets_jpy": 1_000_000,
    }
    ok = validate_private_profile(good, 1_000_000, "2026-08-26T09:00:00Z", now=now)
    assert ok["status"] == "ok"
    stale = validate_private_profile(good, 1_000_000, "2026-08-18T09:00:00Z", now=now)
    assert stale["actionable"] is False
    assert "portfolio_source_stale" in stale["errors"]
    mismatch = validate_private_profile(good, 900_000, "2026-08-26T09:00:00Z", now=now)
    assert "portfolio_market_value_reconciliation_failed" in mismatch["errors"]
    malformed = {**good, "total_assets_jpy": "not-a-number"}
    bad = validate_private_profile(malformed, 1_000_000, "2026-08-26T09:00:00Z", now=now)
    assert bad["actionable"] is False
    assert "total_assets_missing_or_nonpositive" in bad["errors"]


def test_private_markdown_surfaces_fx_scenarios_and_no_score(tmp_path):
    report = {
        "generated_at": "2026-08-26T09:00:00Z", "private_input_audit": {"status": "ok", "actionable": True},
        "portfolio": {"holdings": 1, "metrics": {}, "concentration": {},
                      "fx_sensitivity": {"status": "ok", "base_usdjpy": 159,
                          "usdjpy_beta_equivalent_jpy": 100, "direct_usd_market_value_jpy": 100,
                          "impact_per_one_yen_down_jpy": -1, "explicit_beta_coverage_ratio": 1,
                          "scenarios": []},
                      "cause_scenarios": [], "investor_financial_capacity": {"status": "ok",
                          "shock_loss_pct_assets": .1, "shock_loss_pct_unrealized_gain": .2,
                          "liquidity_coverage_ratio": 1.5, "remaining_unrealized_gain_jpy": 100}},
        "candidate_impact": [], "rules": [],
    }
    _, md = write_private_report(report, tmp_path)
    text = md.read_text(encoding="utf-8")
    assert "Direct FX sensitivity" in text
    assert "Cause-conditional scenarios" in text
    assert "Numeric score: not assigned" in text


def test_analyze_integrates_fresh_private_profile_without_dropping_fund():
    idx = pd.date_range("2025-01-01", periods=260, freq="B", tz="UTC")
    curves = {"VTI": np.linspace(100, 120, len(idx)), "1306.T": np.linspace(100, 110, len(idx))}
    def fake_fetch(symbol, start, end):
        return pd.Series(curves[symbol], index=idx, name=symbol)
    portfolio = pd.DataFrame({
        "holding_id": ["usd", "em"], "ticker": ["VTI", ""], "name": ["US", "EM"],
        "market_value": [600_000, 400_000], "currency": ["USD", "EM_BASKET"],
        "fx_exposure_type": ["direct", "currency_basket"], "fx_beta_usdjpy": [1.0, np.nan],
        "scenario_return_us_recession": [-.10, -.05],
        "scenario_return_basis_us_recession": ["local_currency", "jpy_nav"],
    })
    profile = {
        "enabled": True, "as_of_jst": "2026-08-26T18:00:00+09:00",
        "base_usdjpy": 159, "base_usdjpy_as_of_jst": "2026-08-26T18:00:00+09:00",
        "target_usdjpy": [150], "total_assets_jpy": 1_100_000, "invested_assets_jpy": 1_000_000,
        "cause_scenarios": [{"id": "us_recession", "target_usdjpy": 150,
                              "coefficient_status": "validated_oos"}],
        "resilience": {"enabled": True, "unrealized_gain_jpy": 300_000,
                       "free_cash_jpy": 100_000, "defensive_cash_jpy": 50_000,
                       "shock_loss_jpy": 100_000},
    }
    report = analyze(portfolio, pd.DataFrame(), fetcher=fake_fetch, private_profile=profile,
                     portfolio_source_as_of="2026-08-26T09:00:00Z",
                     now=datetime(2026, 8, 26, 12, tzinfo=timezone.utc))
    assert report["private_input_audit"]["actionable"] is True
    assert report["portfolio"]["holdings"] == 2
    assert report["portfolio"]["metrics"]["status"] == "partial"
    assert report["portfolio"]["fx_sensitivity"]["status"] == "ok"
    assert report["portfolio"]["cause_scenarios"][0]["actionable"] is True
    assert report["portfolio"]["investor_financial_capacity"]["score"] is None
