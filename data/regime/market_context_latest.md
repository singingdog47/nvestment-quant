# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **48.8**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 33.46305700031402
- stress: 75.37250034332276
- participation: 41.56163274745606
- liquidity: 37.28934209448062
- positioning: 60.106090833359694

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **36**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.979999542236328,
  "hy_oas": 3.4,
  "ig_oas": 0.93,
  "treasury_volatility_proxy": 81.856,
  "treasury_volatility_percentile_rank": 0.8056,
  "treasury_volatility_stress_score": 39.58,
  "treasury_volatility_as_of_date": "2026-11-03",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9549,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-04T15:27:57.331020+00:00",
  "nfci": -0.459,
  "volume_ratio20_mean": 0.6019085523620155,
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
  "jpx_official_turnover_date": "2026-11-04",
  "jpx_official_turnover_million_jpy": 11956505.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.