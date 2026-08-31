# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.745** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.2",
  "engine_version": "1.5.2",
  "generated_at": "2026-08-31T22:23:00+00:00",
  "generated_at_utc": "2026-08-31T22:23:00+00:00",
  "date_jst": "2026-09-01",
  "data_status": "partial",
  "regime_label": "CONSTRUCTIVE",
  "regime_score": 61.49,
  "confidence": 0.591,
  "actionable": false,
  "actionability": {
    "minimum_confidence": 0.6,
    "critical_market_series_available": 3,
    "critical_market_series_expected": 3,
    "missing_core_context": [
      "HY_OAS",
      "IG_OAS",
      "NFCI"
    ],
    "reasons": [
      "confidence_below_threshold",
      "core_credit_or_financial_conditions_missing"
    ]
  },
  "overheated_flag": false,
  "stress_flag": false,
  "thin_liquidity_flag": false,
  "treasury_volatility_shock_flag": false,
  "regime_flags": [],
  "components": {
    "trend": 73.09568597803082,
    "stress": 64.79499988555908,
    "participation": 57.123114131060696,
    "liquidity": 46.35314644688251,
    "positioning": 49.80831960274451
  },
  "evidence": {
    "trend_series": 4,
    "vix": 14.920000076293945,
    "hy_oas": null,
    "ig_oas": null,
    "treasury_volatility_proxy": 73.188,
    "treasury_volatility_percentile_rank": 0.7421,
    "treasury_volatility_stress_score": 44.35,
    "treasury_volatility_as_of_date": "2026-08-31",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9575,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-08-31T07:23:16.701787+00:00",
    "nfci": null,
    "volume_ratio20_mean": 0.9270629289376502,
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
    "jpx_official_turnover_date": "2026-08-31",
    "jpx_official_turnover_million_jpy": 10414952.0,
    "jpx_official_turnover_status": "ok"
  },
  "rule": "Regime is context, not a trade signal. If actionable=false, do not infer missing market facts.",
  "source_priority": "official/public primary > internal v1.3 data > free secondary market feed > model inference"
}

## Policy guardrails
{
  "regime_label": "constructive",
  "absolute_defense_cash_jpy": 500000,
  "cash_target_range": [
    0.08,
    0.12
  ],
  "max_single_stock_weight": 0.05,
  "lifestyle_bucket_max_weight": 0.05,
  "exploration_bucket_max_weight": 0.1,
  "new_capital_top_rank_only": 5,
  "decision_gate": "OPEN_FOR_ANALYSIS",
  "note": "Guardrail only. This file never places orders."
}

## Integration health
{
  "generated_at": "2026-08-31T22:28:50+00:00",
  "components": {
    "market_regime": {
      "status": "ok",
      "path": "data/regime/market_regime_latest.json",
      "age_hours": 0.01,
      "stale_limit_hours": 36
    },
    "v1_3_screening": {
      "status": "ok",
      "path": "data/screening_latest.csv",
      "age_hours": 0.1,
      "stale_limit_hours": 36
    },
    "v1_3_screening_full": {
      "status": "ok",
      "path": "data/screening_full.csv.gz",
      "age_hours": 0.1,
      "stale_limit_hours": 36
    },
    "v1_3_quality": {
      "status": "ok",
      "path": "data/quality_report.json",
      "age_hours": 0.1,
      "stale_limit_hours": 36
    },
    "v1_3_daily_report": {
      "status": "ok",
      "path": "data/daily_report.md",
      "age_hours": 0.1,
      "stale_limit_hours": 36
    },
    "fundamentals": {
      "status": "missing",
      "path": "",
      "age_hours": null,
      "stale_limit_hours": 3600
    }
  },
  "system_status": "ok"
}

## Source health
- TDnet: ok / records=0 / tier=primary
- EDINET: ok / records=0 / tier=primary
- SEC: ok / records=58 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=14 / tier=secondary
- yfinance: ok / records=35 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-08-31T07:23:16.701787+00:00
- Price basis: TradingView scanner close; exact exchange timestamp unavailable.
- This report is for research. A high score is not a buy signal.

## Development status

- System version: v2.7
- Status: operational; stale-data reference mode and portfolio FX controls active
- Stable fallback: stable-report-v2.6
- Rollback ready: True

## Cross-market score policy

- JP/US factor inputs are percentile-ranked within their own market.
- Cross-market score is the percentile of the completed composite within each home market; it represents relative standing, not absolute valuation equivalence.
- Orders still require market-specific fundamentals, price verification, and portfolio-fit review.

## Concentration guard

- Maximum displayed research candidates per market for Financials or Shipping: 2
- Mortgage REITs are watch-only and excluded from the research-candidate list.

## Theme distribution in unfiltered score leaders

| Market | Theme | Names in top 20 |
|---|---|---:|
| JP | Financials | 9 |
| JP | Other | 11 |
| US | Financials | 5 |
| US | Mortgage REIT | 4 |
| US | Other | 6 |
| US | Shipping | 5 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 77.5 | 100.0 | unchanged |
| JP | 2 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 77.2 | 99.9 | unchanged |
| JP | 3 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 76.5 | 99.9 | unchanged |
| JP | 5 | 3932.T | Akatsuki Inc. | Other | 76.2 | 99.8 | unchanged |
| JP | 9 | 6750.T | ELECOM CO.,LTD. | Other | 72.8 | 99.6 | unchanged |
| JP | 10 | 2121.T | MIXI,Inc. | Other | 71.8 | 99.5 | unchanged |
| JP | 11 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 71.5 | 99.5 | unchanged |
| JP | 12 | 4763.T | CREEK & RIVER Co.,Ltd. | Other | 71.4 | 99.4 | unchanged |
| JP | 14 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 70.2 | 99.3 | unchanged |
| JP | 16 | 6927.T | Helios Techno Holding Co.,Ltd. | Other | 69.9 | 99.2 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 83.9 | 100.0 | unchanged |
| US | 2 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 83.1 | 100.0 | unchanged |
| US | 3 | INSW | International Seaways, Inc. Common Stock  | Shipping | 83.0 | 99.9 | unchanged |
| US | 5 | ECO | Okeanis Eco Tankers Corp. Common Stock | Shipping | 81.8 | 99.9 | unchanged |
| US | 7 | BUSE | First Busey Corporation - Common Stock | Other | 81.0 | 99.8 | unchanged |
| US | 8 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 81.0 | 99.8 | unchanged |
| US | 10 | ADAM | Adamas Trust, Inc. - Common Stock | Other | 80.9 | 99.7 | unchanged |
| US | 15 | WSBC | WesBanco, Inc. - Common Stock | Other | 80.1 | 99.6 | unchanged |
| US | 16 | TRMD | TORM plc - Class A Common Stock | Other | 79.9 | 99.6 | unchanged |
| US | 18 | FRO | Frontline Plc Ordinary Shares | Other | 79.6 | 99.5 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-07-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526310361/wsbc-20260721.htm
- [HIGH] HTGC Hercules Capital, Inc. Common Stock | 2026-07-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1280784/000128078426000032/htgc-20260721.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-07-22 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000012/nwfl-20260722x8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-07-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000071/care-20260722.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-07-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000070/care-20260723.htm
- [HIGH] ACNB ACNB Corporation - Common Stock | 2026-07-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/715579/000162828026049299/acnb-20260723.htm
- [HIGH] HTGC Hercules Capital, Inc. Common Stock | 2026-07-24 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1280784/000128078426000035/htgc-20260721.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-07-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000073/care-20260727.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-07-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000014/nwfl-20260727x8k.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-07-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000089512626000039/exe-20260727.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-07-28 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000049/buse-20260728.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-07-28 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000089512626000047/exe-20260630.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-07-28 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000089512626000046/exe-20260728.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-07-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000127368526000067/nymt-20260729.htm
- [HIGH] ACNB ACNB Corporation - Common Stock | 2026-07-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/715579/000162828026050410/acnb-20260728.htm
- [HIGH] ECO Okeanis Eco Tankers Corp. Common Stock | 2026-07-30 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1964954/000110465926088713/tm2621702d1_6k.htm
- [HIGH] ECO Okeanis Eco Tankers Corp. Common Stock | 2026-07-30 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1964954/000110465926088444/tm2621682d1_6k.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-07-30 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526326145/wsbc-20260630.htm
- [HIGH] HTGC Hercules Capital, Inc. Common Stock | 2026-07-30 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1280784/000128078426000043/htgc-20260728.htm
- [HIGH] HTGC Hercules Capital, Inc. Common Stock | 2026-07-30 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1280784/000128078426000042/htgc-20260630.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-07-30 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000110465926088451/tm2621424d1_8k.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-07-31 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000052/buse-20260729.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-07-31 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000127368526000069/adam-20260630.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426004739/p15041800_6k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-08-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526332732/ck0002017206-20260630.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-08-04 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526331663/ck0002017206-20260804.htm
- [HIGH] ECO Okeanis Eco Tankers Corp. Common Stock | 2026-08-04 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1964954/000110465926090446/tm2622199d1_6k.htm
- [HIGH] ECO Okeanis Eco Tankers Corp. Common Stock | 2026-08-04 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1964954/000110465926090431/tm2622199d2_6k.htm
- [HIGH] ECO Okeanis Eco Tankers Corp. Common Stock | 2026-08-04 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1964954/000110465926090429/eco-20260630x6k.htm
- [HIGH] DBRG DigitalBridge Group, Inc. | 2026-08-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1679688/000167968826000115/dbrg-20260630.htm
- [HIGH] DBRG DigitalBridge Group, Inc. | 2026-08-04 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1679688/000167968826000113/dbrg-20260804.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-08-05 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526335005/d177605d8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-08-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000077/care-20260630.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-08-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000055/buse-20260630.htm
- [HIGH] ACNB ACNB Corporation - Common Stock | 2026-08-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/715579/000162828026054143/acnb-20260630.htm
- [HIGH] HCI HCI Group, Inc. Common Stock | 2026-08-06 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1400810/000119312526338133/hci-20260806.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-08-07 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000057/buse-20260807.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-08-07 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000016/nwfl-20260630x10q.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426004877/p15046186_6k.htm
- [HIGH] HCI HCI Group, Inc. Common Stock | 2026-08-07 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1400810/000119312526340280/hci-20260630.htm
- [HIGH] INSW International Seaways, Inc. Common Stock  | 2026-08-10 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1679049/000110465926093061/insw-20260630x10q.htm
- [HIGH] INSW International Seaways, Inc. Common Stock  | 2026-08-10 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1679049/000110465926093033/tm2622617d1_8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-08-11 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000080/care-20260811.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-08-11 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000127368526000071/nymt-20260811.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426004935/p15047752_6k.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-08-12 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000110465926094556/tm2622924d1_8k.htm
- [HIGH] ECO Okeanis Eco Tankers Corp. Common Stock | 2026-08-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1964954/000110465926095242/tm2623040d1_6k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426005129/p15049955_6k.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-08-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000110465926097101/tm2623199d2_8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-08-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000083/care-20260817.htm

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.