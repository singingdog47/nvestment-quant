# Market Regime v1.5

- Label: **DEFENSIVE**
- Score: **36.92**
- Confidence: **0.925**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 0.028752371118972775
- stress: 63.39499937057495
- participation: 32.13334876721843
- liquidity: 55.65665972883321
- positioning: 62.86284683617225

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **17**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 3,
  "vix": 26.6200008392334,
  "hy_oas": 3.76,
  "ig_oas": 0.98,
  "treasury_volatility_proxy": 99.353,
  "treasury_volatility_percentile_rank": 0.9683,
  "treasury_volatility_stress_score": 27.38,
  "treasury_volatility_as_of_date": "2026-11-23",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9526,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-23T19:16:11.764792+00:00",
  "nfci": -0.478,
  "volume_ratio20_mean": 1.0577664932208304,
  "positioning_sources": {
    "jpx_raw_healthy": 4,
    "cftc_normalized_values": 22
  },
  "component_coverage": {
    "trend": 0.75,
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
  "base_weighted_coverage": 0.925,
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier",
  "jpx_official_turnover_date": "2026-11-20",
  "jpx_official_turnover_million_jpy": 9521475.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.