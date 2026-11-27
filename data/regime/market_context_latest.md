# Market Regime v1.5

- Label: **DEFENSIVE**
- Score: **33.69**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## Components
- trend: 0.2270644574769225
- stress: 64.68500045776368
- participation: 35.36119472100023
- liquidity: 27.248391190155882
- positioning: 62.86284683617225

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **13**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 24.889999389648438,
  "hy_oas": 3.72,
  "ig_oas": 0.98,
  "treasury_volatility_proxy": 100.661,
  "treasury_volatility_percentile_rank": 0.9762,
  "treasury_volatility_stress_score": 26.79,
  "treasury_volatility_as_of_date": "2026-11-25",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9524,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-27T17:29:02.668031+00:00",
  "nfci": -0.444,
  "volume_ratio20_mean": 0.35350977975389697,
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
  "jpx_official_turnover_date": "2026-11-27",
  "jpx_official_turnover_million_jpy": 8358949.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.