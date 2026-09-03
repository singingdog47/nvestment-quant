# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **64.52**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 60.41702892490892
- stress: 83.65750014305115
- participation: 56.50708606982371
- liquidity: 61.29245040109437
- positioning: 49.80831960274451

## Evidence
{
  "trend_series": 4,
  "vix": 15.199999809265137,
  "hy_oas": 2.65,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 70.338,
  "treasury_volatility_percentile_rank": 0.631,
  "treasury_volatility_stress_score": 52.68,
  "treasury_volatility_as_of_date": "2026-09-02",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9568,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-03T07:28:46.343848+00:00",
  "nfci": -0.558,
  "volume_ratio20_mean": 1.1846612600273594,
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
  "jpx_official_turnover_date": "2026-09-02",
  "jpx_official_turnover_million_jpy": 9151252.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.