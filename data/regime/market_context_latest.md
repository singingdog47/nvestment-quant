# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **62.97**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 62.589664055301625
- stress: 87.40249979972839
- participation: 53.69900898824614
- liquidity: 43.3201935467707
- positioning: 51.00577429462018

## SQ execution overlay
- Active: **True**
- Next major SQ: **2026-09-11**
- Days to SQ: **2**
- Execution caution: **2.68/15.0**
- Confidence: **0.25**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.720000267028809,
  "hy_oas": 2.68,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 62.979,
  "treasury_volatility_percentile_rank": 0.4048,
  "treasury_volatility_stress_score": 69.64,
  "treasury_volatility_as_of_date": "2026-09-08",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9567,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-08T07:29:54.486711+00:00",
  "nfci": -0.558,
  "volume_ratio20_mean": 0.7353548386692674,
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
  "jpx_official_turnover_date": "2026-09-08",
  "jpx_official_turnover_million_jpy": 9495876.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.