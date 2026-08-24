import math

import pandas as pd

from market_regime.scoring import score_regime
from market_regime.treasury_volatility import compute_treasury_volatility, parse_treasury_xml


def _yield_frame(n=140):
    dates = pd.bdate_range("2025-01-02", periods=n)
    rows = []
    for i, date in enumerate(dates):
        cycle = math.sin(i / 6.0) * 0.04
        shock = (i - 120) * 0.012 if i >= 120 else 0.0
        rows.append({
            "date": date,
            "2Y": 4.10 + i * 0.001 + cycle + shock,
            "5Y": 4.20 + i * 0.001 + cycle * 0.9 + shock * 0.8,
            "10Y": 4.35 + i * 0.001 + cycle * 0.8 + shock * 0.6,
            "30Y": 4.55 + i * 0.001 + cycle * 0.7 + shock * 0.5,
        })
    return pd.DataFrame(rows)


def test_compute_proxy_is_explicitly_not_ice_move():
    result, history = compute_treasury_volatility(_yield_frame())
    assert result["data_status"] == "ok"
    assert result["is_ice_move"] is False
    assert "not ICE MOVE" in result["label"]
    assert result["curve_realized_vol_20d_bps_ann"] > 0
    assert 0 <= result["percentile_rank"] <= 1
    assert 0 <= result["stress_score"] <= 100
    assert len(history) >= 100


def test_parse_official_treasury_atom_xml_by_local_field_names():
    xml = """<?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
      xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices">
      <entry><content type="application/xml"><m:properties>
        <d:NEW_DATE>2026-08-21T00:00:00</d:NEW_DATE>
        <d:BC_2YEAR>4.10</d:BC_2YEAR><d:BC_5YEAR>4.20</d:BC_5YEAR>
        <d:BC_10YEAR>4.30</d:BC_10YEAR><d:BC_30YEAR>4.50</d:BC_30YEAR>
      </m:properties></content></entry>
    </feed>"""
    frame = parse_treasury_xml(xml)
    assert len(frame) == 1
    assert frame.iloc[0]["10Y"] == 4.30
    assert str(frame.iloc[0]["date"].date()) == "2026-08-21"


def test_proxy_participates_in_stress_score_and_evidence():
    market = pd.DataFrame([{"series": "VIX", "close": 20.0}])
    fred = pd.DataFrame([
        {"series": "HY_OAS", "value": 3.0, "data_status": "ok"},
        {"series": "IG_OAS", "value": 0.9, "data_status": "ok"},
        {"series": "NFCI", "value": 0.0, "data_status": "ok"},
    ])
    weights = {"trend": 0.30, "stress": 0.25, "participation": 0.20, "liquidity": 0.15, "positioning": 0.10}
    proxy = {"data_status": "ok", "curve_realized_vol_20d_bps_ann": 150.0,
             "percentile_rank": 0.96, "stress_score": 28.0,
             "as_of_date": "2026-08-21", "is_ice_move": False}
    components, evidence, _, _ = score_regime(
        market, fred, {}, [], pd.DataFrame(), weights, treasury_volatility=proxy
    )
    assert components["stress"] < 75
    assert evidence["treasury_volatility_percentile_rank"] == 0.96
    assert evidence["treasury_volatility_is_ice_move"] is False
    assert evidence["component_coverage"]["stress"] == 1.0


def test_stale_proxy_is_audited_but_not_scored():
    proxy = {"data_status": "stale", "stress_score": 5.0, "percentile_rank": 1.0}
    components, evidence, _, _ = score_regime(
        pd.DataFrame([{"series": "VIX", "close": 15.0}]),
        pd.DataFrame(), {}, [], pd.DataFrame(), {"stress": 1.0},
        treasury_volatility=proxy,
    )
    assert components["stress"] == 85.0
    assert evidence["treasury_volatility_stress_score"] is None
    assert evidence["component_coverage"]["stress"] == 0.25
