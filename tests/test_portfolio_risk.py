from __future__ import annotations

import numpy as np
import pandas as pd

from src.portfolio_risk import (
    RiskConfig,
    analyze,
    candidate_impact,
    concentration_stats,
    historical_var_cvar,
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
    assert report["version"] == "1.8.0"
    assert report["privacy"] == "PRIVATE_OUTPUT_ONLY"
    assert report["portfolio"]["metrics"]["status"] in {"ok", "partial"}
    assert report["portfolio"]["metadata_exposures"]["currency"] == {}
    assert report["portfolio"]["metadata_exposures"]["rate_sensitivity"]["coverage"] == 0.0
    assert len(report["candidate_impact"]) == 1
