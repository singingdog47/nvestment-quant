# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **59.13**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## Components
- trend: 70.15072444024412
- stress: 76.39250031471252
- participation: 44.26626672819566
- liquidity: 29.134282557934227
- positioning: 57.66981615729503

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **73**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.9399995803833,
  "hy_oas": 2.93,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 85.54,
  "treasury_volatility_percentile_rank": 0.9365,
  "treasury_volatility_stress_score": 29.76,
  "treasury_volatility_as_of_date": "2026-09-28",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9568,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-29T14:06:09.626180+00:00",
  "nfci": -0.555,
  "volume_ratio20_mean": 0.3812320639483558,
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
  "jpx_official_turnover_date": "2026-09-29",
  "jpx_official_turnover_million_jpy": 8103711.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.