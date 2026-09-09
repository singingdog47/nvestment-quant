# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **60.99**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 54.2730444783914
- stress: 87.44750011444091
- participation: 53.00829875518672
- liquidity: 47.59822820011253
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
  "vix": 15.65999984741211,
  "hy_oas": 2.68,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 62.979,
  "treasury_volatility_percentile_rank": 0.4048,
  "treasury_volatility_stress_score": 69.64,
  "treasury_volatility_as_of_date": "2026-09-08",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9566,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-09T07:30:23.995238+00:00",
  "nfci": -0.558,
  "volume_ratio20_mean": 0.8423057050028132,
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
  "jpx_official_turnover_date": "2026-09-09",
  "jpx_official_turnover_million_jpy": 10006607.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.