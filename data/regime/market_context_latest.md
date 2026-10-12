# Market Regime v1.5

- Label: **RISK_ON**
- Score: **73.95**
- Confidence: **0.8**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 92.02414619105342
- stress: 76.16999974250794
- participation: None
- liquidity: 45.135007244833446
- positioning: 57.382181808165846

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **60**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.390000343322754,
  "hy_oas": 3.15,
  "ig_oas": 0.82,
  "treasury_volatility_proxy": 87.562,
  "treasury_volatility_percentile_rank": 0.9246,
  "treasury_volatility_stress_score": 30.65,
  "treasury_volatility_as_of_date": "2026-10-09",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9562,
  "breadth_status": "stale",
  "breadth_source_as_of_utc": "2026-10-05T18:20:57.084630+00:00",
  "nfci": -0.494,
  "volume_ratio20_mean": 0.7919251811208363,
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
  "jpx_official_turnover_date": "2026-10-09",
  "jpx_official_turnover_million_jpy": 8793501.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.