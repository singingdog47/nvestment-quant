# Market Regime v1.5

- Label: **DEFENSIVE**
- Score: **33.96**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 0.3333230636246034
- stress: 61.65499948501587
- participation: 32.10151637921056
- liquidity: 36.859530509986406
- positioning: 65.00238697484912

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **20**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 30.030000686645508,
  "hy_oas": 3.52,
  "ig_oas": 0.94,
  "treasury_volatility_proxy": 106.356,
  "treasury_volatility_percentile_rank": 0.9881,
  "treasury_volatility_stress_score": 25.89,
  "treasury_volatility_as_of_date": "2026-11-19",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9523,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-20T16:10:40.814104+00:00",
  "nfci": -0.478,
  "volume_ratio20_mean": 0.58783826274966,
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
  "jpx_official_turnover_date": "2026-11-20",
  "jpx_official_turnover_million_jpy": 9521475.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.