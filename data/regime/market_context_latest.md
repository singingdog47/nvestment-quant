# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **52.5**
- Confidence: **0.591**
- Actionable: **False**
- Data status: **partial**
- Flags: none

## Components
- trend: 63.11479447619234
- stress: 56.34999954223633
- participation: 41.47031647031647
- liquidity: 36.75114625125982
- positioning: 56.71738287234125

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **50**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 16.68000030517578,
  "hy_oas": null,
  "ig_oas": null,
  "treasury_volatility_proxy": 87.042,
  "treasury_volatility_percentile_rank": 0.8968,
  "treasury_volatility_stress_score": 32.74,
  "treasury_volatility_as_of_date": "2026-10-21",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9560,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-10-21T12:57:41.926431+00:00",
  "nfci": null,
  "volume_ratio20_mean": 0.7350229250251964,
  "positioning_sources": {
    "jpx_raw_healthy": 4,
    "cftc_normalized_values": 22
  },
  "component_coverage": {
    "trend": 1.0,
    "stress": 0.5,
    "participation": 1.0,
    "liquidity": 0.8,
    "positioning": 1.0
  },
  "critical_context_coverage": {
    "fred_credit_financial_conditions": 0.0,
    "available": 0,
    "expected": 3,
    "multiplier": 0.7
  },
  "base_weighted_coverage": 0.845,
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier",
  "jpx_official_turnover_date": "2026-10-21",
  "jpx_official_turnover_million_jpy": 7621582.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.