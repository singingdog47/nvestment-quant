import pandas as pd

from portfolio_valuation import build_portfolio_valuation


def test_portfolio_valuation_uses_reciprocal_multiple_and_coverage():
    pf = pd.DataFrame([
        {"ticker": "1111.T", "market_value": 600.0, "name": "A"},
        {"ticker": "2222.T", "market_value": 400.0, "name": "B"},
    ])
    sc = pd.DataFrame([
        {"ticker": "1111.T", "price": 100, "pe": 10, "pb": 1, "dividend_yield": 3, "roe": 12,
         "earnings_growth": 8, "revenue_growth": 6, "value_score": 70, "quality_score": 60,
         "growth_score": 55, "fundamental_status": "ok", "fundamental_source": "TradingView scanner"},
        {"ticker": "2222.T", "price": 100, "pe": 20, "pb": 2, "dividend_yield": 2, "roe": 8,
         "earnings_growth": 4, "revenue_growth": 3, "value_score": 50, "quality_score": 50,
         "growth_score": 45, "fundamental_status": "ok", "fundamental_source": "TradingView scanner"},
    ])
    out = build_portfolio_valuation(pf, sc)
    # 1 / (0.6/10 + 0.4/20) = 12.5
    assert round(out["metrics"]["aggregate_pe"], 6) == 12.5
    assert out["coverage"]["pe"] == 1.0
    assert out["metrics"]["relative_value_score"] == 62.0
    # Secondary fundamentals are review-useful but never promoted to actionable.
    assert out["status"] == "current"
    assert out["analysis_mode"] == "reference_only"
    assert out["decision_actionable"] is False


def test_portfolio_valuation_does_not_impute_unmatched_fund():
    pf = pd.DataFrame([
        {"ticker": "1111.T", "market_value": 500.0},
        {"ticker": "FUND-X", "market_value": 500.0},
    ])
    sc = pd.DataFrame([
        {"ticker": "1111.T", "price": 100, "pe": 10, "pb": 1, "value_score": 60,
         "quality_score": 60, "growth_score": 60, "fundamental_status": "ok",
         "fundamental_source": "EDINET"},
    ])
    out = build_portfolio_valuation(pf, sc)
    assert out["coverage"]["screening_match"] == 0.5
    assert out["coverage"]["pe"] == 0.5
    assert out["status"] == "reference_only"
    assert out["decision_actionable"] is False
