# Market Regime v1.5

- Label: **DEFENSIVE**
- Score: **41.0**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## Components
- trend: 17.340078199311463
- stress: 70.41500062942505
- participation: 40.39217954650625
- liquidity: 25.82682506846249
- positioning: 62.462051551193944

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **27**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 20.1299991607666,
  "hy_oas": 3.2,
  "ig_oas": 0.89,
  "treasury_volatility_proxy": 109.814,
  "treasury_volatility_percentile_rank": 1.0,
  "treasury_volatility_stress_score": 25.0,
  "treasury_volatility_as_of_date": "2026-11-12",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9533,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-13T15:25:50.869251+00:00",
  "nfci": -0.462,
  "volume_ratio20_mean": 0.3148206267115622,
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
  "jpx_official_turnover_date": "2026-11-13",
  "jpx_official_turnover_million_jpy": 9086090.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.