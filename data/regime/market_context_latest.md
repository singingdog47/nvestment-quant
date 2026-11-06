# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **43.81**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 6.3219618762668786
- stress: 66.53499977111817
- participation: 42.26190476190476
- liquidity: 72.08053244143119
- positioning: 60.106090833359694

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **35**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 28.18000030517578,
  "hy_oas": 3.32,
  "ig_oas": 0.91,
  "treasury_volatility_proxy": 85.159,
  "treasury_volatility_percentile_rank": 0.8532,
  "treasury_volatility_stress_score": 36.01,
  "treasury_volatility_as_of_date": "2026-11-05",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9541,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-05T15:29:51.899012+00:00",
  "nfci": -0.459,
  "volume_ratio20_mean": 1.4852018094724209,
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
  "jpx_official_turnover_date": "2026-11-05",
  "jpx_official_turnover_million_jpy": 12709314.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.