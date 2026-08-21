import pandas as pd
from market_regime.scoring import score_regime, regime_label


def test_regime_scoring_has_confidence_and_label():
    market=pd.DataFrame([
        {"series":"JP_NIKKEI","close":40000,"ret_20d":0.04,"ret_60d":0.08,"ma20":39000,"ma50":38000,"ma200":35000},
        {"series":"US_SP500","close":6000,"ret_20d":0.03,"ret_60d":0.07,"ma20":5900,"ma50":5800,"ma200":5500},
        {"series":"VIX","close":16.0},
    ])
    fred=pd.DataFrame([
        {"series":"HY_OAS","value":3.0},
        {"series":"IG_OAS","value":0.9},
        {"series":"NFCI","value":-0.2},
    ])
    breadth={"participation_proxy":0.62,"n":5000}
    weights={"trend":0.30,"stress":0.25,"participation":0.20,"liquidity":0.15,"positioning":0.10}
    comp,ev,score,conf=score_regime(market,fred,breadth,[],pd.DataFrame(),weights)
    assert score is not None
    assert 0 <= score <= 100
    assert conf > 0.5
    assert regime_label(score,{"risk_on":70,"constructive":58,"neutral":42,"defensive":30}) in {"RISK_ON","CONSTRUCTIVE","NEUTRAL","DEFENSIVE","RISK_OFF"}
