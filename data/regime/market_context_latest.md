# Market Regime v1.5

- Label: **DEFENSIVE**
- Score: **39.99**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY

## Components
- trend: 14.329012778078585
- stress: 69.2774993133545
- participation: 36.01548059149723
- liquidity: 34.39061567991211
- positioning: 60.106090833359694

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **34**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 24.290000915527344,
  "hy_oas": 3.32,
  "ig_oas": 0.93,
  "treasury_volatility_proxy": 85.159,
  "treasury_volatility_percentile_rank": 0.8532,
  "treasury_volatility_stress_score": 36.01,
  "treasury_volatility_as_of_date": "2026-11-05",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9540,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-06T15:05:36.552022+00:00",
  "nfci": -0.459,
  "volume_ratio20_mean": 0.5294403919978029,
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
  "jpx_official_turnover_date": "2026-11-06",
  "jpx_official_turnover_million_jpy": 13722985.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.