# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **62.99**
- Confidence: **0.591**
- Actionable: **False**
- Data status: **partial**
- Flags: none

## Components
- trend: 79.30575789082798
- stress: 64.63499954223633
- participation: 55.11173827900012
- liquidity: 46.93314348929091
- positioning: 49.80831960274451

## Evidence
{
  "trend_series": 4,
  "vix": 14.430000305175781,
  "hy_oas": null,
  "ig_oas": null,
  "treasury_volatility_proxy": 74.687,
  "treasury_volatility_percentile_rank": 0.7659,
  "treasury_volatility_stress_score": 42.56,
  "treasury_volatility_as_of_date": "2026-08-28",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9575,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-08-28T21:48:33.185318+00:00",
  "nfci": null,
  "volume_ratio20_mean": 0.9386628697858183,
  "positioning_sources": {
    "jpx_raw_healthy": 4,
    "cftc_normalized_values": 22
  },
  "component_coverage": {
    "trend": 1.0,
    "stress": 0.5,
    "participation": 1.0,
    "liquidity": 0.8,
    "positioning": 1.0
  },
  "critical_context_coverage": {
    "fred_credit_financial_conditions": 0.0,
    "available": 0,
    "expected": 3,
    "multiplier": 0.7
  },
  "base_weighted_coverage": 0.845,
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier",
  "jpx_official_turnover_date": "2026-08-28",
  "jpx_official_turnover_million_jpy": 9093361.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.