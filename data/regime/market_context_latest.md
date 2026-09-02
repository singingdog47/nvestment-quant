# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **65.71**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 60.4820388698096
- stress: 82.80999988555908
- participation: 54.82663287639673
- liquidity: 72.77366106729926
- positioning: 49.80831960274451

## Evidence
{
  "trend_series": 4,
  "vix": 16.34000015258789,
  "hy_oas": 2.63,
  "ig_oas": 0.8,
  "treasury_volatility_proxy": 70.498,
  "treasury_volatility_percentile_rank": 0.6389,
  "treasury_volatility_stress_score": 52.08,
  "treasury_volatility_as_of_date": "2026-09-01",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9577,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-02T07:27:57.054761+00:00",
  "nfci": -0.566,
  "volume_ratio20_mean": 1.5610903427275749,
  "positioning_sources": {
    "jpx_raw_healthy": 4,
    "cftc_normalized_values": 22
  },
  "component_coverage": {
    "trend": 1.0,
    "stress": 1.0,
    "participation": 1.0,
    "liquidity": 1.0,
    "positioning": 1.0
  },
  "critical_context_coverage": {
    "fred_credit_financial_conditions": 1.0,
    "available": 3,
    "expected": 3,
    "multiplier": 1.0
  },
  "base_weighted_coverage": 1.0,
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier",
  "jpx_official_turnover_date": "2026-09-01",
  "jpx_official_turnover_million_jpy": 8436078.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.