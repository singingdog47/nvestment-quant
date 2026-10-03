# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **68.65**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 84.85661201592544
- stress: 74.82249968528748
- participation: 44.389638860043846
- liquidity: 66.64965809675982
- positioning: 56.133531942148466

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **69**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.3100004196167,
  "hy_oas": 3.24,
  "ig_oas": 0.86,
  "treasury_volatility_proxy": 90.387,
  "treasury_volatility_percentile_rank": 0.9643,
  "treasury_volatility_stress_score": 27.68,
  "treasury_volatility_as_of_date": "2026-10-02",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9569,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-03T00:10:06.958854+00:00",
  "nfci": -0.548,
  "volume_ratio20_mean": 1.3255552786436957,
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
  "jpx_official_turnover_date": "2026-10-02",
  "jpx_official_turnover_million_jpy": 9126232.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.