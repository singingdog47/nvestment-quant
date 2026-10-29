# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **53.3**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY

## Components
- trend: 48.39176543449444
- stress: 76.15000011444091
- participation: 43.045764474748644
- liquidity: 34.90092249438477
- positioning: 59.04864260835684

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **43**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.65999984741211,
  "hy_oas": 3.18,
  "ig_oas": 0.88,
  "treasury_volatility_proxy": 84.03,
  "treasury_volatility_percentile_rank": 0.8413,
  "treasury_volatility_stress_score": 36.9,
  "treasury_volatility_as_of_date": "2026-10-28",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9558,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-29T14:23:26.716187+00:00",
  "nfci": -0.487,
  "volume_ratio20_mean": 0.5372980623596192,
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
  "jpx_official_turnover_date": "2026-10-29",
  "jpx_official_turnover_million_jpy": 15152265.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.