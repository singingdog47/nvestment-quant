# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **66.06**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 79.7241712876803
- stress: 74.53250045776367
- participation: 44.0356648199446
- liquidity: 59.536794609759795
- positioning: 57.66981615729503

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **70**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.389999389648438,
  "hy_oas": 3.12,
  "ig_oas": 0.84,
  "treasury_volatility_proxy": 92.015,
  "treasury_volatility_percentile_rank": 0.9683,
  "treasury_volatility_stress_score": 27.38,
  "treasury_volatility_as_of_date": "2026-10-01",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9570,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-01T16:20:52.639748+00:00",
  "nfci": -0.548,
  "volume_ratio20_mean": 1.1476805742634115,
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
  "jpx_official_turnover_date": "2026-10-01",
  "jpx_official_turnover_million_jpy": 9675554.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.