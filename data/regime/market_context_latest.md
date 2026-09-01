# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **61.54**
- Confidence: **0.591**
- Actionable: **False**
- Data status: **partial**
- Flags: none

## Components
- trend: 70.06790394530778
- stress: 63.51999931335449
- participation: 56.858509044820835
- liquidity: 55.277971195949945
- positioning: 49.80831960274451

## Evidence
{
  "trend_series": 4,
  "vix": 15.770000457763672,
  "hy_oas": null,
  "ig_oas": null,
  "treasury_volatility_proxy": 73.188,
  "treasury_volatility_percentile_rank": 0.7421,
  "treasury_volatility_stress_score": 44.35,
  "treasury_volatility_as_of_date": "2026-08-31",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9575,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-01T10:37:46.226421+00:00",
  "nfci": null,
  "volume_ratio20_mean": 1.105559423918999,
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
  "jpx_official_turnover_date": "2026-09-01",
  "jpx_official_turnover_million_jpy": 8436078.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.