# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **59.36**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 47.72140910086321
- stress: 83.03499948501587
- participation: 49.08079760258184
- liquidity: 62.21004408622563
- positioning: 51.361148997264756

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **85**
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
  "hy_oas": 2.76,
  "ig_oas": 0.8,
  "treasury_volatility_proxy": 69.297,
  "treasury_volatility_percentile_rank": 0.6151,
  "treasury_volatility_stress_score": 53.87,
  "treasury_volatility_as_of_date": "2026-09-16",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9568,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-17T07:30:10.504454+00:00",
  "nfci": -0.56,
  "volume_ratio20_mean": 1.207251102155641,
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
  "jpx_official_turnover_date": "2026-09-16",
  "jpx_official_turnover_million_jpy": 7395180.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.