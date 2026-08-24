import pandas as pd

from market_regime.scoring import score_regime, regime_label


def test_regime_scoring_has_confidence_and_label():
    market=pd.DataFrame([
        {"series":"JP_NIKKEI","close":40000,"ret_20d":0.04,"ret_60d":0.08,"ma20":39000,"ma50":38000,"ma200":35000},
        {"series":"US_SP500","close":6000,"ret_20d":0.03,"ret_60d":0.07,"ma20":5900,"ma50":5800,"ma200":5500},
        {"series":"VIX","close":16.0},
    ])
    fred=pd.DataFrame([
        {"series":"HY_OAS","value":3.0,"data_status":"ok"},
        {"series":"IG_OAS","value":0.9,"data_status":"ok"},
        {"series":"NFCI","value":-0.2,"data_status":"ok"},
    ])
    breadth={"participation_proxy":0.62,"n":5000}
    weights={"trend":0.30,"stress":0.25,"participation":0.20,"liquidity":0.15,"positioning":0.10}
    comp,ev,score,conf=score_regime(market,fred,breadth,[],pd.DataFrame(),weights)
    assert score is not None
    assert 0 <= score <= 100
    assert conf > 0.5
    assert ev["critical_context_coverage"]["available"] == 3
    assert regime_label(score,{"risk_on":70,"constructive":58,"neutral":42,"defensive":30}) in {"RISK_ON","CONSTRUCTIVE","NEUTRAL","DEFENSIVE","RISK_OFF"}


def test_missing_fred_context_reduces_confidence_and_stale_is_not_scored():
    market=pd.DataFrame([
        {"series":"JP_NIKKEI","close":40000,"ret_20d":0.04,"ret_60d":0.08,"ma20":39000,"ma50":38000,"ma200":35000},
        {"series":"JP_TOPIX_PROXY","close":3000,"ret_20d":0.03,"ret_60d":0.07,"ma20":2900,"ma50":2800,"ma200":2600,"volume_ratio20":0.9},
        {"series":"US_SP500","close":6000,"ret_20d":0.03,"ret_60d":0.07,"ma20":5900,"ma50":5800,"ma200":5500,"volume_ratio20":1.0},
        {"series":"US_NASDAQ","close":22000,"ret_20d":0.02,"ret_60d":0.06,"ma20":21500,"ma50":21000,"ma200":20000},
        {"series":"VIX","close":16.0},
        {"series":"HYG","close":80,"volume_ratio20":0.8},
        {"series":"LQD","close":110,"volume_ratio20":0.9},
    ])
    fred=pd.DataFrame([
        {"series":"HY_OAS","value":3.0,"data_status":"stale"},
        {"series":"IG_OAS","value":0.9,"data_status":"stale"},
        {"series":"NFCI","value":-0.2,"data_status":"stale"},
    ])
    cftc=pd.DataFrame([{"asset_mgr_net_pct_oi":0.02,"lev_money_net_pct_oi":-0.01}])
    weights={"trend":0.30,"stress":0.25,"participation":0.20,"liquidity":0.15,"positioning":0.10}
    _,ev,score,conf=score_regime(market,fred,{"participation_proxy":0.62,"n":5000},[],cftc,weights)
    assert score is not None
    assert ev["hy_oas"] is None
    assert ev["ig_oas"] is None
    assert ev["nfci"] is None
    assert ev["critical_context_coverage"]["available"] == 0
    assert conf < 0.60
