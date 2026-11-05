import pandas as pd

from src.pts_observer import PTSObservation, attach_forward_return, evaluate


CFG = {
    "thresholds": {
        "absolute_move_pct": 3.0,
        "min_turnover_jpy": 5_000_000,
        "high_confidence_turnover_jpy": 20_000_000,
    }
}


def test_alert_requires_move_and_liquidity():
    rows = [
        PTSObservation("1111", "liquid", 1000, 1040, 10000, 10_000_000),
        PTSObservation("2222", "thin", 1000, 1100, 10, 11_000),
        PTSObservation("3333", "quiet", 1000, 1020, 10000, 10_000_000),
    ]
    out = evaluate(rows, CFG).set_index("code")
    assert bool(out.loc["1111", "alert"]) is True
    assert bool(out.loc["2222", "alert"]) is False
    assert bool(out.loc["3333", "alert"]) is False


def test_forward_return_is_future_only():
    signals = pd.DataFrame([{"code": "1111", "session": "d0"}])
    closes = pd.DataFrame([
        {"code": "1111", "session": "d0", "close": 100.0},
        {"code": "1111", "session": "d1", "close": 105.0},
    ])
    out = attach_forward_return(signals, closes, 1)
    assert round(out.loc[0, "forward_1s_pct"], 6) == 5.0
