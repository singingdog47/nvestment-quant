# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **52.72**
- Confidence: **0.8**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 33.07399611246446
- stress: 74.08499994277955
- participation: None
- liquidity: 51.46535935574042
- positioning: 60.106090833359694

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **39**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 19.420000076293945,
  "hy_oas": 3.26,
  "ig_oas": 0.89,
  "treasury_volatility_proxy": 82.863,
  "treasury_volatility_percentile_rank": 0.8214,
  "treasury_volatility_stress_score": 38.39,
  "treasury_volatility_as_of_date": "2026-10-30",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9558,
  "breadth_status": "stale",
  "breadth_source_as_of_utc": "2026-10-29T14:23:26.716187+00:00",
  "nfci": -0.487,
  "volume_ratio20_mean": 0.9514089838935105,
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
  "jpx_official_turnover_date": "2026-10-30",
  "jpx_official_turnover_million_jpy": 9395736.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.