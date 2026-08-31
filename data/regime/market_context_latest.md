# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **62.88**
- Confidence: **0.591**
- Actionable: **False**
- Data status: **partial**
- Flags: none

## Components
- trend: 74.29365147324822
- stress: 64.63499954223633
- participation: 57.123114131060696
- liquidity: 53.50144848641823
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
  "breadth_source_as_of_utc": "2026-08-31T07:23:16.701787+00:00",
  "nfci": null,
  "volume_ratio20_mean": 1.0700289697283645,
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