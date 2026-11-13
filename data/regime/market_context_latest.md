# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **47.65**
- Confidence: **0.8**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 28.960240412127668
- stress: 71.04999942779541
- participation: None
- liquidity: 36.14159873573716
- positioning: 62.462051551193944

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **28**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 18.700000762939453,
  "hy_oas": 3.3,
  "ig_oas": 0.9,
  "treasury_volatility_proxy": 109.814,
  "treasury_volatility_percentile_rank": 1.0,
  "treasury_volatility_stress_score": 25.0,
  "treasury_volatility_as_of_date": "2026-11-12",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9540,
  "breadth_status": "stale",
  "breadth_source_as_of_utc": "2026-11-06T15:05:36.552022+00:00",
  "nfci": -0.462,
  "volume_ratio20_mean": 0.572689968393429,
  "positioning_sources": {
    "jpx_raw_healthy": 4,
    "cftc_normalized_values": 22
  },
  "component_coverage": {
    "trend": 1.0,
    "stress": 1.0,
    "participation": 0.0,
    "liquidity": 1.0,
    "positioning": 1.0
  },
  "critical_context_coverage": {
    "fred_credit_financial_conditions": 1.0,
    "available": 3,
    "expected": 3,
    "multiplier": 1.0
  },
  "base_weighted_coverage": 0.8,
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier",
  "jpx_official_turnover_date": "2026-11-12",
  "jpx_official_turnover_million_jpy": 9725572.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.