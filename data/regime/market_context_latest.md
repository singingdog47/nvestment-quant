# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **66.07**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 71.98644772828044
- stress: 86.4650002002716
- participation: 55.67749740753543
- liquidity: 44.15090536660804
- positioning: 51.00577429462018

## Evidence
{
  "trend_series": 4,
  "vix": 14.529999732971191,
  "hy_oas": 2.65,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 66.084,
  "treasury_volatility_percentile_rank": 0.5079,
  "treasury_volatility_stress_score": 61.9,
  "treasury_volatility_as_of_date": "2026-09-04",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9568,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-04T23:16:26.613933+00:00",
  "nfci": -0.558,
  "volume_ratio20_mean": 0.756122634165201,
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
  "jpx_official_turnover_date": "2026-09-04",
  "jpx_official_turnover_million_jpy": 9332575.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.