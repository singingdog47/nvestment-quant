# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.745** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-09-21T14:12:52+00:00",
  "generated_at_utc": "2026-09-21T14:12:52+00:00",
  "date_jst": "2026-09-21",
  "data_status": "ok",
  "regime_label": "CONSTRUCTIVE",
  "regime_score": 61.6,
  "confidence": 1.0,
  "actionable": true,
  "actionability": {
    "minimum_confidence": 0.6,
    "critical_market_series_available": 3,
    "critical_market_series_expected": 3,
    "missing_core_context": [],
    "reasons": []
  },
  "overheated_flag": false,
  "stress_flag": false,
  "thin_liquidity_flag": true,
  "treasury_volatility_shock_flag": false,
  "sq_execution_caution_flag": false,
  "regime_flags": [
    "THIN_LIQUIDITY"
  ],
  "components": {
    "trend": 70.71559944800754,
    "stress": 80.99000008583069,
    "participation": 50.02304412950801,
    "liquidity": 29.047369861698616,
    "positioning": 57.726288981550105
  },
  "evidence": {
    "trend_series": 4,
    "vix": 14.869999885559082,
    "hy_oas": 2.7,
    "ig_oas": 0.78,
    "treasury_volatility_proxy": 74.744,
    "treasury_volatility_percentile_rank": 0.7817,
    "treasury_volatility_stress_score": 41.37,
    "treasury_volatility_as_of_date": "2026-09-18",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9568,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-09-21T14:12:49.675803+00:00",
    "nfci": -0.56,
    "volume_ratio20_mean": 0.37818424654246535,
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
    "jpx_official_turnover_date": "2026-09-18",
    "jpx_official_turnover_million_jpy": 11269638.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-09-21",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 81,
      "event_proximity_score": 0.0,
      "pressure_intensity_score": 0.0,
      "confidence": 0.4,
      "data_status": "partial",
      "manual_input_freshness": "missing",
      "manual_input_age_days": null,
      "execution_caution_points": 0.0,
      "caution_cap_points": 15.0,
      "execution_stance": "NORMAL",
      "directional_bias": "UNDETERMINED",
      "price_structure": {
        "spot": 65018.94921875,
        "put_wall": null,
        "call_wall": null,
        "magnet_strike": null,
        "nearest_reference_distance_pct": null
      },
      "evidence": {
        "put_call_oi_ratio": null,
        "front_futures_share": null,
        "arbitrage_balance_zscore": null,
        "nikkei_vi_percentile": null,
        "component_scores": {
          "event_proximity": 0.0,
          "option_oi_imbalance": null,
          "front_futures_concentration": null,
          "strike_pin_proximity": null,
          "arbitrage_balance_extreme": null,
          "nikkei_vi_percentile": null
        },
        "source_notes": null
      },
      "policy_effects": {
        "alter_security_ranking": false,
        "alter_fundamental_score": false,
        "alter_investment_thesis": false,
        "use_for_execution_timing_only": true
      },
      "tactics": [
        "no_sq_specific_change"
      ],
      "rule": "SQ is a short-lived market-structure overlay. Use it for staging and limit-order timing only; do not infer direction from open interest alone."
    }
  },
  "rule": "Regime is context, not a trade signal. If actionable=false, do not infer missing market facts.",
  "execution_rule": "SQ may alter staging, patience, and limit-order execution only. It must not alter security ranking, fundamental score, or investment thesis.",
  "source_priority": "official/public primary > internal v1.3 data > free secondary market feed > model inference"
}

## Policy guardrails
{
  "regime_label": "constructive",
  "absolute_defense_cash_jpy": 500000,
  "cash_target_range": [
    0.15,
    0.18
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
  "generated_at": "2026-09-21T14:13:54+00:00",
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
      "age_hours": 0.02,
      "stale_limit_hours": 36
    },
    "v1_3_screening_full": {
      "status": "ok",
      "path": "data/screening_full.csv.gz",
      "age_hours": 0.02,
      "stale_limit_hours": 36
    },
    "v1_3_quality": {
      "status": "ok",
      "path": "data/quality_report.json",
      "age_hours": 0.02,
      "stale_limit_hours": 36
    },
    "v1_3_daily_report": {
      "status": "ok",
      "path": "data/daily_report.md",
      "age_hours": 0.02,
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
- EDINET: ok / records=5 / tier=primary
- SEC: ok / records=38 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=13 / tier=secondary
- yfinance: ok / records=36 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-09-21T14:12:49.675803+00:00
- Price basis: TradingView scanner close; exact exchange timestamp unavailable.
- This report is for research. A high score is not a buy signal.

## Development status

- System version: v2.13
- Status: operational; private Drive history, valuation, monthly attribution v1.1, dynamic cash/tax friction, anti-FOMO execution controls, PayPay swing research monitor, non-directional major-SQ execution timing overlay, and monitored-security supply/demand context active
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
| JP | Financials | 10 |
| JP | Other | 10 |
| US | Financials | 6 |
| US | Mortgage REIT | 3 |
| US | Other | 6 |
| US | Shipping | 5 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 76.3 | 100.0 | unchanged |
| JP | 2 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 75.3 | 99.9 | unchanged |
| JP | 3 | 8616.T | Tokai Tokyo Financial Holdings,Inc. | Financials | 75.0 | 99.9 | new_entry |
| JP | 4 | 3932.T | Akatsuki Inc. | Other | 75.0 | 99.8 | unchanged |
| JP | 8 | 6750.T | ELECOM CO.,LTD. | Other | 73.1 | 99.6 | unchanged |
| JP | 9 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 71.6 | 99.6 | unchanged |
| JP | 10 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 71.2 | 99.5 | unchanged |
| JP | 12 | 2121.T | MIXI,Inc. | Other | 70.9 | 99.4 | unchanged |
| JP | 13 | 4763.T | CREEK & RIVER Co.,Ltd. | Other | 70.2 | 99.4 | unchanged |
| JP | 15 | 8473.T | SBI Holdings,Inc. | Other | 69.7 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 85.0 | 100.0 | unchanged |
| US | 2 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 83.5 | 100.0 | unchanged |
| US | 3 | INSW | International Seaways, Inc. Common Stock  | Shipping | 83.1 | 99.9 | unchanged |
| US | 5 | MCHB | Mechanics Bancorp - Class A Common Stock | Financials | 82.1 | 99.9 | new_entry |
| US | 7 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 81.9 | 99.8 | unchanged |
| US | 9 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 81.6 | 99.8 | unchanged |
| US | 10 | BUSE | First Busey Corporation - Common Stock | Other | 81.1 | 99.7 | unchanged |
| US | 16 | WSBC | WesBanco, Inc. - Common Stock | Other | 79.8 | 99.6 | unchanged |
| US | 17 | TRMD | TORM plc - Class A Common Stock | Other | 79.8 | 99.5 | unchanged |
| US | 19 | FRO | Frontline Plc Ordinary Shares | Other | 79.6 | 99.5 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 6965 浜松ホトニクス | Fri, 15 May 2026 | guidance | 浜松ホトニクス---ストップ高、1-3月期増益転換で通期予想を上方修正 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiYEFVX3lxTE9XTHM1aVlfSFZ6NzBMUFN1ZEZCZWNpd3lYRUFDdkdrU3M4d1gxRGN4aFk5eml1dTAwMnpxOFhsVzNsN2wzOTN1QlQ5dURqNHZEZDJxSkhlQ0UwcTZ0M2tIaw?oc=5
- [CRITICAL] 6965 浜松ホトニクス | Thu, 06 Aug 2026 | guidance | 決算:浜松ホトニクス、26年9月期の純利益23%増 半導体関連伸び上方修正 - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMibEFVX3lxTFBmVEVJUmoxbkY1S2IwUEVSY1BFMVVLa1pDalQ1NXNZTHhPSnN0UlZ6dHlfSzNFOEZpWjkxVW0xRUNDSTBSS1FMQllsdnAtR0pkOW84T3VxbmR2ZlRmVWFERm5fVTlZeFktSi10NA?oc=5
- [HIGH] MCHB Mechanics Bancorp - Class A Common Stock | 2026-08-07 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1518715/000151871526000060/mchb-20260630.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-08-07 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000057/buse-20260807.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426004877/p15046186_6k.htm
- [HIGH] INSW International Seaways, Inc. Common Stock  | 2026-08-10 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1679049/000110465926093061/insw-20260630x10q.htm
- [HIGH] INSW International Seaways, Inc. Common Stock  | 2026-08-10 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1679049/000110465926093033/tm2622617d1_8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-08-11 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000080/care-20260811.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-08-11 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000127368526000071/nymt-20260811.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426004935/p15047752_6k.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-08-12 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000110465926094556/tm2622924d1_8k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426005129/p15049955_6k.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-08-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000110465926097101/tm2623199d2_8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-08-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000083/care-20260817.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-08-17 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026057375/stng6k-08172026.htm
- [HIGH] MCHB Mechanics Bancorp - Class A Common Stock | 2026-08-20 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1518715/000151871526000064/hmst-20260819.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-24 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426005684/p15057626_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-26 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000162828026058979/trmd-20260630.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-26 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000162828026058978/tormplc6-kaugust262026pres.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-08-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526371610/wsbc-20260827.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-08-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000091957426005942/p15060813_6k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426005821/p15059931_6-k.htm
- [HIGH] IMPP Imperial Petroleum Inc. - Common Shares | 2026-08-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1876581/000119312526372414/d324626d6k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-01 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526378466/d83131d8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-02 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006143/p15072501_6k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-09-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026060459/stng6k-09032026.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-09-04 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426006193/p15074444_6-k.htm
- [HIGH] LPG Dorian LPG Ltd. Common Stock | 2026-09-04 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1596993/000159699326000041/lpg-20260902x8k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-09-08 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426006196/p15076578_6-k.htm
- [HIGH] ADAM Adamas Trust, Inc. - Common Stock | 2026-09-10 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1273685/000127368526000073/adam-20260910.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006252/p15079219_6-k.htm
- [HIGH] IMPP Imperial Petroleum Inc. - Common Shares | 2026-09-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1876581/000119312526389346/d181516d6k.htm
- [HIGH] LPG Dorian LPG Ltd. Common Stock | 2026-09-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1596993/000159699326000046/lpg-20260910x8k.htm
- [HIGH] 4063 信越化学工業 | 2026-09-15 | filing | 臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z2DU
- [HIGH] 4063 信越化学工業 | 2026-09-15 | filing | 有価証券届出書（参照方式） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z2EE
- [HIGH] 8616 Tokai Tokyo Financial Holdings,Inc. | 2026-09-15 | filing | 訂正臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z2CA
- [HIGH] 8616 Tokai Tokyo Financial Holdings,Inc. | 2026-09-15 | filing | 訂正発行登録書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z24X
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-15 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006318/p15075054_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006339/p15081246_6-k.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000162828026062234/fro-20260630.htm
- [HIGH] MCHB Mechanics Bancorp - Class A Common Stock | 2026-09-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1518715/000151871526000068/hmst-20260916.htm
- [HIGH] TEN Tsakos Energy Navigation Ltd Common Shares | 2026-09-17 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1166663/000119312526394366/d67788d6k.htm
- [HIGH] HTGC Hercules Capital, Inc. Common Stock | 2026-09-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1280784/000128078426000046/htgc-20260917.htm
- [HIGH] 6701 NEC | 2026-09-18 | filing | 変更報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z2Q2
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-18 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006391/p15095918_6-k.htm
- [HIGH] 4063 信越化学工業 | Tue, 15 Sep 2026 | dividend | 信越化学工業[4063]：創立100周年記念配当の実施 及び 配当予想の修正に関するお知らせ 2026年9月15日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE1UaXotSERuMUFFNlctcE9TT0NPRVhhVVNDbHRCTWFJb0VVVFFxNzd4WUY5cjZ1RWtHemd0WnFraXgySFNUZm14bzhUWm9BV0J2ZVpNSzFrMEt5UldCLVZWeFM0YVNMcmNvdHc?oc=5
- [HIGH] 4063 信越化学工業 | Tue, 15 Sep 2026 | dividend | 信越化、今期配当を20円増額修正 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE14VEdPRDlYZE1odUpxZzR6TFpHaHl5MW8zQVhPVkkxRWVYbHNXVV9JUlZZV1pZRmlGOWNSZ250aFVycHNWRkx3YnFzN040dUd5c0E?oc=5

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.