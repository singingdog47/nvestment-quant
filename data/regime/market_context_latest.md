# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **68.01**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 92.18239502067762
- stress: 75.78999965667725
- participation: 43.72474310125851
- liquidity: 46.16965495594139
- positioning: 57.382181808165846

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **58**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.770000457763672,
  "hy_oas": 3.11,
  "ig_oas": 0.83,
  "treasury_volatility_proxy": 88.52,
  "treasury_volatility_percentile_rank": 0.9325,
  "treasury_volatility_stress_score": 30.06,
  "treasury_volatility_as_of_date": "2026-10-13",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9557,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-14T12:54:00.267777+00:00",
  "nfci": -0.494,
  "volume_ratio20_mean": 0.8177913738985348,
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
  "jpx_official_turnover_date": "2026-10-14",
  "jpx_official_turnover_million_jpy": 8272690.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.