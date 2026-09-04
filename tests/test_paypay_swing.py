from paypay_swing import _cost, _research_status, score_rows


def _base_config():
    return {
        "weights": {"momentum": 0.35, "macro": 0.25, "trend": 0.20, "risk": 0.10, "cost": 0.10},
        "entry_gate": {"minimum_score": 68.0, "minimum_margin": 4.0, "minimum_momentum": 55.0, "minimum_trend": 55.0},
        "courses": {
            "GOLD": {"label": "金", "ticker": "GLD", "entry_cost_pct": 1.0, "exit_cost_pct": 0.0, "minimum_score": 68.0},
            "TECH": {"label": "テック", "ticker": "QQQ", "entry_cost_pct": 1.0, "exit_cost_pct": 0.0, "minimum_score": 68.0},
            "STANDARD": {"label": "標準", "ticker": "SPY", "entry_cost_pct": 1.0, "exit_cost_pct": 0.0, "minimum_score": 68.0},
            "BTC": {"label": "BTC", "ticker": "BTC-USD", "entry_cost_pct": 4.5, "exit_cost_pct": 4.5, "minimum_score": 80.0},
        },
        "macro_symbols": {"US10Y": "^TNX", "DXY": "DX-Y.NYB", "VIX": "^VIX"},
    }


def _row(series, close=110, r20=0.05, r60=0.10, vol=0.20, dd=-0.05):
    return {
        "series": series,
        "date": "2026-09-04",
        "close": close,
        "ret_20d": r20,
        "ret_60d": r60,
        "ma20": 105,
        "ma50": 102,
        "ma200": 95,
        "vol20_ann": vol,
        "drawdown_52w": dd,
    }


def test_crypto_round_trip_cost_is_about_8_8_percent():
    score, round_trip = _cost(4.5, 4.5)
    assert round(round_trip, 2) == 8.8
    assert score < 25


def test_normal_course_cost_is_one_percent_when_exit_is_free():
    score, round_trip = _cost(1.0, 0.0)
    assert round(round_trip, 2) == 1.0
    assert score == 91.0


def test_scoring_includes_cost_penalty_and_returns_all_courses():
    cfg = _base_config()
    rows = [
        _row("GOLD", r20=0.08, r60=0.15, vol=0.15),
        _row("TECH", r20=0.04, r60=0.08, vol=0.25),
        _row("STANDARD", r20=0.03, r60=0.06, vol=0.18),
        _row("BTC", r20=0.08, r60=0.15, vol=0.65),
        _row("US10Y", r20=-0.05, r60=-0.02, vol=0.10),
        _row("DXY", r20=-0.03, r60=-0.02, vol=0.08),
        _row("VIX", close=18, r20=-0.05, r60=-0.10, vol=0.80),
    ]
    ranking = score_rows(cfg, rows)
    assert len(ranking) == 4
    btc = next(x for x in ranking if x["key"] == "BTC")
    gold = next(x for x in ranking if x["key"] == "GOLD")
    assert btc["round_trip_cost_pct"] == 8.8
    assert gold["round_trip_cost_pct"] == 1.0
    assert btc["cost"] < gold["cost"]


def test_research_status_waits_when_leader_margin_is_too_small():
    cfg = _base_config()
    ranking = [
        {"key": "GOLD", "label": "金", "total": 75.0, "momentum": 70.0, "trend": 70.0},
        {"key": "TECH", "label": "テック", "total": 73.0, "momentum": 70.0, "trend": 70.0},
    ]
    result = _research_status(ranking, cfg)
    assert result["status"] == "WAIT_RESEARCH"
    assert result["leader"] is None
