# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **44.48**
- Confidence: **0.8**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## Components
- trend: 24.958674745009837
- stress: 71.73000017166137
- participation: None
- liquidity: 26.12574407528307
- positioning: 62.462051551193944

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **29**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 17.489999771118164,
  "hy_oas": 3.34,
  "ig_oas": 0.91,
  "treasury_volatility_proxy": 100.311,
  "treasury_volatility_percentile_rank": 1.0,
  "treasury_volatility_stress_score": 25.0,
  "treasury_volatility_as_of_date": "2026-11-10",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9540,
  "breadth_status": "stale",
  "breadth_source_as_of_utc": "2026-11-06T15:05:36.552022+00:00",
  "nfci": -0.459,
  "volume_ratio20_mean": 0.3228186018820768,
  "positioning_sources": {
    "jpx_raw_healthy": 4,
    "cftc_normalized_values": 22
  },
  "component_coverage": {
    "trend": 1.0,
    "stress": 1.0,
    "participation": 0.0,
    "liquidity": 1.0,
    "positioning": 1.0
  },
  "critical_context_coverage": {
    "fred_credit_financial_conditions": 1.0,
    "available": 3,
    "expected": 3,
    "multiplier": 1.0
  },
  "base_weighted_coverage": 0.8,
  "confidence_method": "weighted subcomponent coverage x critical FRED context multiplier",
  "jpx_official_turnover_date": "2026-11-11",
  "jpx_official_turnover_million_jpy": 9356951.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.