import pandas as pd

from src.decision_system import build_factor_table, build_alerts, regime_weights


def test_regime_weights_sum_to_one():
    for regime in ["Risk-On", "Neutral", "Risk-Off", "Panic", "Recovery", "Overheated"]:
        assert abs(sum(regime_weights(regime).values()) - 1.0) < 1e-9


def test_risk_off_rewards_quality_and_risk():
    w = regime_weights("Risk-Off")
    assert w["quality_score"] > w["growth_score"]
    assert w["risk_score"] > w["momentum_score"]


def test_factor_table_is_deterministic():
    df = pd.DataFrame([
        {"ticker": "A", "value_score": 90, "quality_score": 90, "growth_score": 20, "momentum_score": 20, "risk_score": 90, "liquidity_score": 80},
        {"ticker": "B", "value_score": 20, "quality_score": 20, "growth_score": 90, "momentum_score": 90, "risk_score": 20, "liquidity_score": 80},
    ])
    out = build_factor_table(df, "Risk-Off")
    assert out.iloc[0]["ticker"] == "A"
    assert list(out["regime_rank"]) == [1, 2]


def test_panic_creates_critical_alert():
    decision = {"market_regime": "Panic", "market_risk_level": "Critical"}
    factors = pd.DataFrame([{"ticker": "A", "rank_change": 0}])
    alerts = build_alerts(decision, factors, {"status": "private_data_required"})
    assert any(a["severity"] == "CRITICAL" for a in alerts)
