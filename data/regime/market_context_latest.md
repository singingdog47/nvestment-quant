# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **60.99**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 53.88147050636896
- stress: 86.81000068664551
- participation: 53.00829875518672
- liquidity: 49.49762356106936
- positioning: 51.00577429462018

## SQ execution overlay
- Active: **True**
- Next major SQ: **2026-09-11**
- Days to SQ: **1**
- Execution caution: **3.21/15.0**
- Confidence: **0.25**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **MILD_CAUTION**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.459999084472656,
  "hy_oas": 2.67,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 63.039,
  "treasury_volatility_percentile_rank": 0.4087,
  "treasury_volatility_stress_score": 69.35,
  "treasury_volatility_as_of_date": "2026-09-09",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9566,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-09T07:30:23.995238+00:00",
  "nfci": -0.558,
  "volume_ratio20_mean": 0.8897905890267339,
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