import numpy as np
import pandas as pd

from src.scoring import add_final_scores, add_technical_scores


def test_ineligible_rows_do_not_get_pre_score():
    frame = pd.DataFrame(
        [
            {"ticker": "A", "market": "US", "price_status": "ok", "price": 10, "avg_turnover_30d": 2_000_000, "return_1m": .1, "return_3m": .2, "return_6m": .3, "return_12m": .4, "volatility_1m": .2, "beta_1y": 1.0},
            {"ticker": "B", "market": "US", "price_status": "missing", "price": np.nan, "avg_turnover_30d": np.nan, "beta_1y": np.nan},
        ]
    )
    scored = add_technical_scores(frame)
    assert bool(scored.loc[scored.ticker.eq("A"), "eligible"].iloc[0])
    assert np.isnan(scored.loc[scored.ticker.eq("B"), "pre_score"].iloc[0])


def test_low_factor_coverage_is_unscored():
    frame = pd.DataFrame(
        [
            {"ticker": "A", "market": "US", "price_status": "ok", "fundamental_status": "ok", "momentum_score": 80, "risk_score": 70, "pe": 10, "earnings_yield": .1, "pb": 1, "roe": .2, "profit_margin": .15, "revenue_growth": .1, "earnings_growth": .1},
            {"ticker": "B", "market": "US", "price_status": "ok", "fundamental_status": "missing", "momentum_score": 50, "risk_score": 50},
        ]
    )
    scored = add_final_scores(frame)
    assert scored.loc[scored.ticker.eq("A"), "total_score"].notna().all()
    assert scored.loc[scored.ticker.eq("B"), "total_score"].isna().all()


def test_concentration_guard_and_mreit_watch_only():
    frame = pd.DataFrame(
        [
            {"ticker": "AGNC", "code": "AGNC", "market": "US", "name": "AGNC Investment Corp.", "price_status": "ok", "fundamental_status": "ok", "momentum_score": 80, "risk_score": 70, "pe": 10, "pb": 1, "roe": .2, "profit_margin": .15, "revenue_growth": .1, "earnings_growth": .1},
            {"ticker": "AAA", "code": "AAA", "market": "US", "name": "Example Bank", "price_status": "ok", "fundamental_status": "ok", "momentum_score": 80, "risk_score": 70, "pe": 10, "pb": 1, "roe": .2, "profit_margin": .15, "revenue_growth": .1, "earnings_growth": .1},
            {"ticker": "BBB", "code": "BBB", "market": "US", "name": "Second Bank", "price_status": "ok", "fundamental_status": "ok", "momentum_score": 80, "risk_score": 70, "pe": 10, "pb": 1, "roe": .2, "profit_margin": .15, "revenue_growth": .1, "earnings_growth": .1},
            {"ticker": "CCC", "code": "CCC", "market": "US", "name": "Third Bank", "price_status": "ok", "fundamental_status": "ok", "momentum_score": 80, "risk_score": 70, "pe": 10, "pb": 1, "roe": .2, "profit_margin": .15, "revenue_growth": .1, "earnings_growth": .1},
            {"ticker": "DHT", "code": "DHT", "market": "US", "name": "DHT Holdings", "price_status": "ok", "fundamental_status": "ok", "momentum_score": 80, "risk_score": 70, "pe": 10, "pb": 1, "roe": .2, "profit_margin": .15, "revenue_growth": .1, "earnings_growth": .1},
        ]
    )
    scored = add_final_scores(frame)
    assert scored.loc[scored.ticker.eq("AGNC"), "research_status"].iloc[0] == "watch_only_mreit"
    financials = scored[scored.theme.eq("Financials")]
    assert financials["research_candidate"].sum() == 2
    assert financials["research_status"].eq("held_back_theme_cap").sum() == 1
    assert scored.loc[scored.ticker.eq("DHT"), "theme"].iloc[0] == "Shipping"
