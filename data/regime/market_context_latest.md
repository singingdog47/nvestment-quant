# Market Regime v1.5

- Label: **NEUTRAL**
- Score: **55.72**
- Confidence: **1.0**
- Actionable: **True**
- Data status: **ok**
- Flags: none

## Components
- trend: 37.09321304013397
- stress: 79.23499988555909
- participation: 49.276990436686255
- liquidity: 65.52227012778194
- positioning: 51.00577429462018

## SQ execution overlay
- Active: **True**
- Next major SQ: **2026-09-11**
- Days to SQ: **0**
- Execution caution: **3.75/15.0**
- Confidence: **0.25**
- Data status: **partial**
- Directional bias: **UNDETERMINED**
- Execution stance: **MILD_CAUTION**
- Rule: SQ changes execution timing only; it does not change the security ranking or investment thesis.

## Evidence
{
  "trend_series": 4,
  "vix": 17.84000015258789,
  "hy_oas": 2.71,
  "ig_oas": 0.81,
  "treasury_volatility_proxy": 74.12,
  "treasury_volatility_percentile_rank": 0.75,
  "treasury_volatility_stress_score": 43.75,
  "treasury_volatility_as_of_date": "2026-09-10",
  "treasury_volatility_status": "ok",
  "treasury_volatility_is_ice_move": false,
  "breadth_n": 9569,
  "breadth_status": "ok",
  "breadth_source_as_of_utc": "2026-09-11T07:29:18.209236+00:00",
  "nfci": -0.564,
  "volume_ratio20_mean": 1.2893567531945487,
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
  "jpx_official_turnover_date": "2026-09-10",
  "jpx_official_turnover_million_jpy": 9103130.0,
  "jpx_official_turnover_status": "ok"
}

Regime is context, not an automatic trade signal.