# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **58.28**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 58.59738845920853
- stress: 73.65999982833863
- participation: 41.60219399538106
- liquidity: 55.262348998973266
- positioning: 56.71738287234125

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **50**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 18.010000228881836,
  "hy_oas": 3.33,
  "ig_oas": 0.87,
  "treasury_volatility_proxy": 87.042,
  "treasury_volatility_percentile_rank": 0.8968,
  "treasury_volatility_stress_score": 32.74,
  "treasury_volatility_as_of_date": "2026-10-21",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9561,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-22T12:59:30.157859+00:00",
  "nfci": -0.496,
  "volume_ratio20_mean": 1.0447587249743318,
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
  "jpx_official_turnover_date": "2026-10-22",
  "jpx_official_turnover_million_jpy": 7902051.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.