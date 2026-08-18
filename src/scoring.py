from __future__ import annotations

import numpy as np
import pandas as pd

from .config import SETTINGS


def _percentile(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    ranked = numeric.rank(pct=True, method="average")
    return ranked if higher_is_better else 1.0 - ranked


def _market_rank(frame: pd.DataFrame, column: str, higher_is_better: bool = True) -> pd.Series:
    return frame.groupby("market", group_keys=False)[column].transform(
        lambda s: _percentile(s, higher_is_better)
    )


def _mean_available(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    existing = [column for column in columns if column in frame]
    if not existing:
        return pd.Series(np.nan, index=frame.index)
    return frame[existing].mean(axis=1, skipna=True)


def add_technical_scores(prices: pd.DataFrame) -> pd.DataFrame:
    frame = prices.copy()
    min_price = np.where(frame["market"].eq("JP"), SETTINGS.min_price_jp, SETTINGS.min_price_us)
    min_turnover = np.where(frame["market"].eq("JP"), SETTINGS.min_turnover_jp, SETTINGS.min_turnover_us)
    frame["eligible"] = (
        frame["price_status"].eq("ok")
        & frame["price"].ge(min_price)
        & frame["avg_turnover_30d"].ge(min_turnover)
    )
    for column in ("return_1m", "return_3m", "return_6m", "return_12m", "avg_turnover_30d"):
        frame[f"rank_{column}"] = _market_rank(frame, column, True)
    for column in ("volatility_1m", "beta_abs"):
        if column == "beta_abs":
            frame[column] = frame["beta_1y"].abs()
        frame[f"rank_{column}"] = _market_rank(frame, column, False)
    frame["momentum_score"] = 100 * _mean_available(
        frame,
        ["rank_return_1m", "rank_return_3m", "rank_return_6m", "rank_return_12m"],
    )
    frame["risk_score"] = 100 * _mean_available(frame, ["rank_volatility_1m", "rank_beta_abs"])
    frame["liquidity_score"] = 100 * frame["rank_avg_turnover_30d"]
    frame["pre_score"] = 0.60 * frame["momentum_score"] + 0.25 * frame["risk_score"] + 0.15 * frame["liquidity_score"]
    frame.loc[~frame["eligible"], "pre_score"] = np.nan
    return frame


def add_final_scores(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["earnings_yield"] = np.where(result["pe"].gt(0), 1.0 / result["pe"], np.nan)
    positive = ("earnings_yield", "dividend_yield", "roe", "gross_margin", "operating_margin", "profit_margin", "revenue_growth", "earnings_growth")
    negative = ("pb", "debt_to_equity")
    for column in positive:
        if column in result:
            result[f"rank_{column}"] = _market_rank(result, column, True)
    for column in negative:
        if column in result:
            result[f"rank_{column}"] = _market_rank(result, column, False)
    result["value_score"] = 100 * _mean_available(result, ["rank_earnings_yield", "rank_pb", "rank_dividend_yield"])
    result["quality_score"] = 100 * _mean_available(result, ["rank_roe", "rank_gross_margin", "rank_operating_margin", "rank_profit_margin", "rank_debt_to_equity"])
    result["growth_score"] = 100 * _mean_available(result, ["rank_revenue_growth", "rank_earnings_growth"])
    factor_columns = ["value_score", "quality_score", "growth_score", "momentum_score", "risk_score"]
    weights = pd.Series({"value_score": 0.25, "quality_score": 0.25, "growth_score": 0.20, "momentum_score": 0.15, "risk_score": 0.15})
    available = result[factor_columns].notna()
    weighted = result[factor_columns].mul(weights, axis=1).sum(axis=1, skipna=True)
    weight_sum = available.mul(weights, axis=1).sum(axis=1)
    result["factor_coverage"] = available.sum(axis=1) / len(factor_columns)
    result["total_score"] = weighted / weight_sum.replace(0, np.nan)
    result.loc[result["factor_coverage"] < 0.6, "total_score"] = np.nan
    result["flags"] = "ok"
    result.loc[result["price_status"].ne("ok"), "flags"] = "price_missing"
    result.loc[result["fundamental_status"].isin(["missing", np.nan]), "flags"] = "fundamental_missing"
    result.loc[result["fundamental_status"].eq("partial"), "flags"] = "fundamental_partial"
    result["market_rank"] = result.groupby("market")["total_score"].rank(
        ascending=False, method="first", na_option="bottom"
    )
    return result.sort_values("total_score", ascending=False, na_position="last").reset_index(drop=True)
