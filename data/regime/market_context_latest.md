# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **63.36**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## Components
- trend: 86.48487273437607
- stress: 75.21249968528747
- participation: 42.61652053530226
- liquidity: 29.801088725663313
- positioning: 56.133531942148466

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **66**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.5600004196167,
  "hy_oas": 3.1,
  "ig_oas": 0.85,
  "treasury_volatility_proxy": 90.387,
  "treasury_volatility_percentile_rank": 0.9643,
  "treasury_volatility_stress_score": 27.68,
  "treasury_volatility_as_of_date": "2026-10-02",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9562,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-05T16:21:26.481001+00:00",
  "nfci": -0.548,
  "volume_ratio20_mean": 0.3991272181415828,
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
  "jpx_official_turnover_date": "2026-10-05",
  "jpx_official_turnover_million_jpy": 8721605.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.