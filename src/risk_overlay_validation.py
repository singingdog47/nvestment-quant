from __future__ import annotations

import math
from typing import Iterable

import numpy as np
import pandas as pd

VERSION = "1.0.0"


def _series(values: Iterable[float] | pd.Series) -> pd.Series:
    x = pd.Series(values, dtype=float).replace([np.inf, -np.inf], np.nan).dropna()
    return x


def wealth_index(returns: Iterable[float] | pd.Series) -> pd.Series:
    r = _series(returns)
    return (1.0 + r).cumprod()


def max_drawdown(returns: Iterable[float] | pd.Series) -> float | None:
    w = wealth_index(returns)
    if w.empty:
        return None
    dd = w / w.cummax() - 1.0
    return float(dd.min())


def geometric_return(returns: Iterable[float] | pd.Series, periods_per_year: int = 252) -> float | None:
    r = _series(returns)
    if r.empty or (1.0 + r).le(0).any():
        return None
    return float((1.0 + r).prod() ** (periods_per_year / len(r)) - 1.0)


def annualized_volatility(returns: Iterable[float] | pd.Series, periods_per_year: int = 252) -> float | None:
    r = _series(returns)
    if len(r) < 2:
        return None
    return float(r.std(ddof=1) * math.sqrt(periods_per_year))


def apply_exposure(returns: pd.Series, exposure: pd.Series, cost_bps: float = 0.0) -> pd.Series:
    r = pd.Series(returns, dtype=float)
    e = pd.Series(exposure, index=r.index, dtype=float).clip(0.0, 1.0).shift(1).fillna(1.0)
    turnover = e.diff().abs().fillna(abs(e.iloc[0] - 1.0))
    return r * e - turnover * (cost_bps / 10000.0)


def simple_vol_momentum_exposure(
    returns: pd.Series,
    vol_window: int = 20,
    momentum_window: int = 100,
    target_vol: float = 0.15,
    floor: float = 0.35,
) -> pd.Series:
    r = pd.Series(returns, dtype=float)
    vol = r.rolling(vol_window).std(ddof=1) * math.sqrt(252)
    trend = (1.0 + r).rolling(momentum_window).apply(np.prod, raw=True) - 1.0
    vol_scale = (target_vol / vol).clip(upper=1.0)
    # A weak trend reduces risk, but never forces an all-or-nothing exit.
    trend_scale = pd.Series(np.where(trend < 0, 0.65, 1.0), index=r.index)
    return (vol_scale * trend_scale).clip(lower=floor, upper=1.0).fillna(1.0)


def drawdown_exposure(
    returns: pd.Series,
    soft: float = -0.08,
    hard: float = -0.16,
    floor: float = 0.35,
) -> pd.Series:
    w = wealth_index(returns)
    dd = w / w.cummax() - 1.0
    if hard >= soft or not (0.0 <= floor <= 1.0):
        raise ValueError("require hard < soft <= 0 and 0 <= floor <= 1")
    scale = pd.Series(1.0, index=dd.index)
    scale[dd <= hard] = floor
    mid = (dd < soft) & (dd > hard)
    scale[mid] = 1.0 - (1.0 - floor) * ((soft - dd[mid]) / (soft - hard))
    return scale


def blended_permission(
    base_exposure: pd.Series,
    drawdown_overlay: pd.Series,
    regime_permission: pd.Series | None = None,
    max_overlay_cut: float = 0.50,
) -> pd.Series:
    """Flexible permission layer: overlays can reduce risk, never dictate a trade.

    The cap prevents one noisy signal from collapsing exposure. A separate
    regime permission may soften or waive the cut when evidence conflicts.
    """
    b = pd.Series(base_exposure, dtype=float)
    d = pd.Series(drawdown_overlay, index=b.index, dtype=float)
    proposed = np.minimum(b, d)
    if regime_permission is not None:
        rp = pd.Series(regime_permission, index=b.index, dtype=float).clip(0.0, 1.0)
        proposed = proposed + (b - proposed) * rp
    lower = (b - max_overlay_cut).clip(lower=0.0)
    return pd.Series(np.maximum(proposed, lower), index=b.index).clip(0.0, 1.0)


def evaluate(returns: pd.Series, exposure: pd.Series, cost_bps: float = 0.0) -> dict:
    net = apply_exposure(returns, exposure, cost_bps)
    vol = annualized_volatility(net)
    geo = geometric_return(net)
    mdd = max_drawdown(net)
    turnover = float(pd.Series(exposure, index=net.index).diff().abs().sum())
    return {
        "geometric_return": geo,
        "annualized_volatility": vol,
        "max_drawdown": mdd,
        "return_over_abs_drawdown": (geo / abs(mdd)) if geo is not None and mdd not in (None, 0) else None,
        "turnover": turnover,
        "cost_bps": float(cost_bps),
    }


def compare_overlays(returns: pd.Series, cost_bps: float = 5.0) -> dict:
    r = pd.Series(returns, dtype=float).dropna()
    hold = pd.Series(1.0, index=r.index)
    simple = simple_vol_momentum_exposure(r)
    dd = drawdown_exposure(r)
    flexible = blended_permission(simple, dd, max_overlay_cut=0.35)
    return {
        "version": VERSION,
        "status": "research_only",
        "actionable": False,
        "strategies": {
            "buy_hold": evaluate(r, hold, cost_bps=0.0),
            "simple_vol_momentum": evaluate(r, simple, cost_bps=cost_bps),
            "drawdown_only": evaluate(r, dd, cost_bps=cost_bps),
            "flexible_blend": evaluate(r, flexible, cost_bps=cost_bps),
        },
        "governance": {
            "rule": "No strategy is promoted from this in-sample diagnostic alone.",
            "next_gate": "walk-forward/out-of-sample tests across bull, fast-crash, slow-bear, and whipsaw periods",
        },
    }
