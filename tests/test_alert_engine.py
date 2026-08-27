import pandas as pd

from alert_engine import detect_private_portfolio_alerts, detect_public_alerts


def test_public_alerts_detect_regime_vix_quality_and_rank_jump():
    regime = {
        "regime_label": "RISK_OFF",
        "stress_flag": True,
        "overheated_flag": False,
        "thin_liquidity_flag": False,
        "regime_score": 30,
        "components": {"liquidity": 20, "participation": 25},
        "evidence": {"vix": 32},
    }
    quality = {"actionable": False, "quality_score": 0.3, "primary_source_health": 0.4}
    snapshot = pd.DataFrame([
        {"name": "Example", "rank_change": 20},
        {"name": "Small move", "rank_change": 3},
    ])
    events = pd.DataFrame()
    previous = {"regime_label": "CONSTRUCTIVE", "vix": 18}

    report = detect_public_alerts(regime, quality, snapshot, events, previous)
    codes = {a["code"] for a in report["alerts"]}

    assert "REGIME_CHANGE" in codes
    assert "VIX_WARNING" in codes
    assert "VIX_JUMP" in codes
    assert "NOT_ACTIONABLE" in codes
    assert "RANK_JUMP" in codes
    assert report["highest_severity"] in {"WARNING", "CRITICAL"}


def test_public_alerts_no_missing_value_inference():
    report = detect_public_alerts({}, {}, pd.DataFrame(), pd.DataFrame(), {})
    assert report["alerts"] == []
    assert report["highest_severity"] == "INFO"


def test_public_alerts_detect_treasury_volatility_proxy_shock():
    result = detect_public_alerts(
        {"evidence": {"treasury_volatility_percentile_rank": 0.94}},
        {}, pd.DataFrame(), pd.DataFrame(), {},
    )
    alert = next(a for a in result["alerts"] if a["code"] == "TREASURY_VOLATILITY_SHOCK")
    assert alert["severity"] == "WARNING"
    assert "not ICE MOVE" in alert["message"]


def test_private_portfolio_alerts_are_private_and_deterministic():
    risk = {
        "portfolio": {
            "metrics": {"var_1d": 0.03, "annualized_volatility": 0.25, "beta": 1.4},
            "concentration": {"largest_weight": 0.12, "top5_weight": 0.55, "hhi": 0.08},
        }
    }
    out = detect_private_portfolio_alerts(risk, {"var_1d": 0.02})
    codes = {a["code"] for a in out["alerts"]}

    assert out["privacy"] == "PRIVATE_EPHEMERAL_ONLY"
    assert "VAR_HIGH" in codes
    assert "VAR_JUMP" in codes
    assert "SINGLE_NAME_CONCENTRATION" in codes
    assert "TOP5_CONCENTRATION" in codes
    assert "BETA_EXTREME" in codes


def test_private_alerts_surface_stale_inputs_and_partial_risk_coverage():
    risk = {
        "private_input_audit": {"status": "reference_only"},
        "portfolio": {"metrics": {"portfolio_weight_coverage": 0.70}, "concentration": {}},
    }
    out = detect_private_portfolio_alerts(risk)
    codes = {a["code"] for a in out["alerts"]}
    assert "PRIVATE_INPUT_REFERENCE_ONLY" in codes
    assert "PORTFOLIO_RISK_COVERAGE_LOW" in codes


def test_private_alerts_withhold_only_unavailable_components():
    risk = {
        "private_input_audit": {"status": "withheld"},
        "portfolio": {"metrics": {}, "concentration": {}},
    }
    out = detect_private_portfolio_alerts(risk)
    assert "PRIVATE_INPUT_INVALID_OR_STALE" in {a["code"] for a in out["alerts"]}
