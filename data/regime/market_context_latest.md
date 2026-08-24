# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **58.17**
- Confidence: **0.591**
- Actionable: **False**
- Data status: **partial**
- Flags: THIN_LIQUIDITY

## Components
- trend: 71.7343553842388
- stress: 65.03499942779541
- participation: 56.58334293284184
- liquidity: 28.113063059131136
- positioning: 48.60196300007342

## Evidence
{
  "trend_series": 4,
  "vix": 15.850000381469727,
  "hy_oas": null,
  "ig_oas": null,
  "treasury_volatility_proxy": 72.293,
  "treasury_volatility_percentile_rank": 0.6984,
  "treasury_volatility_stress_score": 47.62,
  "treasury_volatility_as_of_date": "2026-08-24",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9583,
  "nfci": null,
  "volume_ratio20_mean": 0.5622612611826227,
  "positioning_sources": {
    "jpx_raw_healthy": 2,
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
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier"
}

Regime is context, not an automatic trade signal.