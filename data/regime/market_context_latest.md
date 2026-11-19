# Market Regime v1.5

- Label: **DEFENSIVE**
- Score: **36.46**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: TREASURY_VOLATILITY_SHOCK

## Components
- trend: 0.5120346353444996
- stress: 66.3225004005432
- participation: 37.10358796296296
- liquidity: 38.731358250525275
- positioning: 65.00238697484912

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **22**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 24.559999465942383,
  "hy_oas": 3.43,
  "ig_oas": 0.92,
  "treasury_volatility_proxy": 106.012,
  "treasury_volatility_percentile_rank": 0.9841,
  "treasury_volatility_stress_score": 26.19,
  "treasury_volatility_as_of_date": "2026-11-18",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9527,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-18T16:29:07.327511+00:00",
  "nfci": -0.478,
  "volume_ratio20_mean": 0.6346339562631319,
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
  "jpx_official_turnover_date": "2026-11-18",
  "jpx_official_turnover_million_jpy": 8747024.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.