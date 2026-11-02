# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **48.54**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 30.930218984608267
- stress: 72.8149995994568
- participation: 42.11742949607027
- liquidity: 44.16831264548106
- positioning: 60.106090833359694

## SQ execution overlay
- Active: **False**
- Next major SQ: **2026-12-11**
- Days to SQ: **38**
- Execution caution: **0.0/15.0**
- Confidence: **0.4**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **NORMAL**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 19.690000534057617,
  "hy_oas": 3.44,
  "ig_oas": 0.94,
  "treasury_volatility_proxy": 82.863,
  "treasury_volatility_percentile_rank": 0.8214,
  "treasury_volatility_stress_score": 38.39,
  "treasury_volatility_as_of_date": "2026-10-30",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9554,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-11-02T18:14:32.202447+00:00",
  "nfci": -0.487,
  "volume_ratio20_mean": 0.7689828161370265,
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
  "jpx_official_turnover_date": "2026-11-02",
  "jpx_official_turnover_million_jpy": 8352102.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.