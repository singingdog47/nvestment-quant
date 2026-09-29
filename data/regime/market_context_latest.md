# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **63.31**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 76.60978017883659
- stress: 75.57250062942505
- participation: 43.77018920166129
- liquidity: 46.085726758851386
- positioning: 57.66981615729503

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **72**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.3799991607666,
  "hy_oas": 3.02,
  "ig_oas": 0.83,
  "treasury_volatility_proxy": 85.54,
  "treasury_volatility_percentile_rank": 0.9365,
  "treasury_volatility_stress_score": 29.76,
  "treasury_volatility_as_of_date": "2026-09-28",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9568,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-29T15:43:07.055170+00:00",
  "nfci": -0.555,
  "volume_ratio20_mean": 0.8050181689712848,
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