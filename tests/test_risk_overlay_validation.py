import numpy as np
import pandas as pd

from src.risk_overlay_validation import (
    apply_exposure, blended_permission, compare_overlays, drawdown_exposure,
    simple_vol_momentum_exposure,
)


def test_drawdown_overlay_is_gradual_and_bounded():
    r = pd.Series([.01] * 20 + [-.02] * 12 + [.01] * 20)
    x = drawdown_exposure(r)
    assert x.min() >= .35
    assert x.max() <= 1.0
    assert ((x > .35) & (x < 1.0)).any()


def test_execution_uses_lagged_signal_no_lookahead():
    r = pd.Series([.10, -.10], index=[0, 1])
    e = pd.Series([0.0, 1.0], index=r.index)
    net = apply_exposure(r, e)
    assert net.iloc[0] == .10
    assert net.iloc[1] == 0.0


def test_flexible_permission_caps_single_overlay_cut():
    idx = range(3)
    base = pd.Series([1.0, 1.0, .8], index=idx)
    dd = pd.Series([.2, .4, .1], index=idx)
    x = blended_permission(base, dd, max_overlay_cut=.35)
    assert list(np.round(x, 2)) == [.65, .65, .45]


def test_regime_permission_can_restore_flexibility():
    base = pd.Series([1.0])
    dd = pd.Series([.4])
    x = blended_permission(base, dd, regime_permission=pd.Series([1.0]), max_overlay_cut=.5)
    assert x.iloc[0] == 1.0


def test_compare_is_explicitly_research_only():
    rng = np.random.default_rng(7)
    r = pd.Series(rng.normal(.0003, .01, 400))
    report = compare_overlays(r)
    assert report["status"] == "research_only"
    assert report["actionable"] is False
    assert set(report["strategies"]) == {"buy_hold", "simple_vol_momentum", "drawdown_only", "flexible_blend"}
