# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **62.68**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 69.14486213512593
- stress: 74.19999948501587
- participation: 42.820039247373884
- liquidity: 60.55376063985191
- positioning: 57.382181808165846

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **56**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.030000686645508,
  "hy_oas": 3.25,
  "ig_oas": 0.84,
  "treasury_volatility_proxy": 93.704,
  "treasury_volatility_percentile_rank": 0.9762,
  "treasury_volatility_stress_score": 26.79,
  "treasury_volatility_as_of_date": "2026-10-15",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9560,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-16T12:27:44.914871+00:00",
  "nfci": -0.499,
  "volume_ratio20_mean": 1.1765190159962977,
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
  "jpx_official_turnover_date": "2026-10-16",
  "jpx_official_turnover_million_jpy": 8524856.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.