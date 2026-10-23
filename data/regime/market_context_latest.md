# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **53.43**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 42.92371344341866
- stress: 71.47249942779541
- participation: 41.55210258780036
- liquidity: 58.01690721340409
- positioning: 56.71738287234125

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **49**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 19.700000762939453,
  "hy_oas": 3.27,
  "ig_oas": 0.88,
  "treasury_volatility_proxy": 90.419,
  "treasury_volatility_percentile_rank": 0.9524,
  "treasury_volatility_stress_score": 28.57,
  "treasury_volatility_as_of_date": "2026-10-22",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9560,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-23T12:38:51.991864+00:00",
  "nfci": -0.496,
  "volume_ratio20_mean": 1.1136226803351021,
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
  "jpx_official_turnover_date": "2026-10-23",
  "jpx_official_turnover_million_jpy": 9920480.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.