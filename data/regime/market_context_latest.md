# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **66.73**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 74.12269931379977
- stress: 85.17500022888183
- participation: 56.26296979478902
- liquidity: 46.45705985205344
- positioning: 49.80831960274451

## Evidence
{
  "trend_series": 4,
  "vix": 14.319999694824219,
  "hy_oas": 2.66,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 68.548,
  "treasury_volatility_percentile_rank": 0.5833,
  "treasury_volatility_stress_score": 56.25,
  "treasury_volatility_as_of_date": "2026-09-03",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9568,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-04T07:28:22.637684+00:00",
  "nfci": -0.558,
  "volume_ratio20_mean": 0.813776496301336,
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
  "jpx_official_turnover_date": "2026-09-03",
  "jpx_official_turnover_million_jpy": 8570403.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.