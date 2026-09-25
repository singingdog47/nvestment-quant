# Market Regime v1.5

- Label: **CONSTRUCTIVE**
- Score: **67.31**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 82.12758738402131
- stress: 77.60499994277954
- participation: 48.51924406545287
- liquidity: 51.95119464749005
- positioning: 57.726288981550105

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **77**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 15.670000076293945,
  "hy_oas": 2.73,
  "ig_oas": 0.77,
  "treasury_volatility_proxy": 83.46,
  "treasury_volatility_percentile_rank": 0.9246,
  "treasury_volatility_stress_score": 30.65,
  "treasury_volatility_as_of_date": "2026-09-24",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9567,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-24T12:44:37.410445+00:00",
  "nfci": -0.555,
  "volume_ratio20_mean": 0.9516548661872513,
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
  "jpx_official_turnover_date": "2026-09-24",
  "jpx_official_turnover_million_jpy": 10039026.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.