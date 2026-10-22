# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.864** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-10-22T00:42:16+00:00",
  "generated_at_utc": "2026-10-22T00:42:16+00:00",
  "date_jst": "2026-10-22",
  "data_status": "partial",
  "regime_label": "NEUTRAL",
  "regime_score": 52.5,
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
  "sq_execution_caution_flag": false,
  "regime_flags": [],
  "components": {
    "trend": 63.11479447619234,
    "stress": 56.34999954223633,
    "participation": 41.47031647031647,
    "liquidity": 36.75114625125982,
    "positioning": 56.71738287234125
  },
  "evidence": {
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
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-10-22",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 50,
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
        "spot": 64586.23828125,
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
  "regime_label": "neutral",
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
  "generated_at": "2026-10-22T00:48:46+00:00",
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
      "age_hours": 0.12,
      "stale_limit_hours": 36
    },
    "v1_3_screening_full": {
      "status": "ok",
      "path": "data/screening_full.csv.gz",
      "age_hours": 0.12,
      "stale_limit_hours": 36
    },
    "v1_3_quality": {
      "status": "ok",
      "path": "data/quality_report.json",
      "age_hours": 0.12,
      "stale_limit_hours": 36
    },
    "v1_3_daily_report": {
      "status": "ok",
      "path": "data/daily_report.md",
      "age_hours": 0.12,
      "stale_limit_hours": 36
    },
    "fundamentals": {
      "status": "ok",
      "path": "data/fundamentals_latest.csv",
      "age_hours": 0.0,
      "stale_limit_hours": 3600
    }
  },
  "system_status": "ok"
}

## Source health
- TDnet: ok / records=0 / tier=primary
- EDINET: ok / records=1 / tier=primary
- SEC: ok / records=32 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=58 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-10-21T12:57:41.926431+00:00
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
| JP | Financials | 6 |
| JP | Other | 14 |
| US | Financials | 11 |
| US | Other | 5 |
| US | Shipping | 4 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8613.T | Marusan Securities Co.,Ltd. | Financials | 81.7 | 100.0 | unchanged |
| JP | 2 | 8622.T | Mito Securities Co.,Ltd. | Financials | 81.7 | 99.9 | new_entry |
| JP | 5 | 3932.T | Akatsuki Inc. | Other | 74.9 | 99.8 | unchanged |
| JP | 6 | 6750.T | ELECOM CO.,LTD. | Other | 73.0 | 99.7 | unchanged |
| JP | 7 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 72.8 | 99.7 | unchanged |
| JP | 10 | 2121.T | MIXI,Inc. | Other | 71.2 | 99.5 | unchanged |
| JP | 11 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 70.6 | 99.5 | unchanged |
| JP | 12 | 7744.T | Noritsu Koki Co.,Ltd. | Other | 70.4 | 99.4 | unchanged |
| JP | 13 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 70.0 | 99.4 | unchanged |
| JP | 14 | 9757.T | Funai Soken Holdings Incorporated | Other | 69.8 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 85.4 | 100.0 | unchanged |
| US | 2 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 82.5 | 100.0 | unchanged |
| US | 4 | BUSE | First Busey Corporation - Common Stock | Other | 81.5 | 99.9 | unchanged |
| US | 5 | DHT | DHT Holdings, Inc. | Shipping | 81.4 | 99.9 | unchanged |
| US | 7 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 81.0 | 99.8 | unchanged |
| US | 11 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 80.4 | 99.7 | unchanged |
| US | 13 | TRMD | TORM plc - Class A Common Stock | Other | 80.2 | 99.6 | unchanged |
| US | 15 | WSBC | WesBanco, Inc. - Common Stock | Other | 80.2 | 99.6 | unchanged |
| US | 20 | SFNC | Simmons First National Corporation - Common Stock | Other | 79.2 | 99.4 | unchanged |
| US | 25 | EQBK | Equity Bancshares, Inc. Class A Common Stock | Other | 78.7 | 99.3 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Fri, 29 May 2026 | guidance | ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE5mOXJYY0tyRW8yQUhTZ09US2tkWVM0bEwzUEgteml0SlBUdVZTaU14M3NWZGNUX2FvLTdCb2Z3dHBTVi1WdmlkUVV5ZWZSRVM5SlE?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 19 Oct 2026 | guidance | コーエーテクモホールディングス[3635]：業績予想の修正に関するお知らせ 2026年10月19日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE41YlFlN0NMQVhsY2VxRUhGR0hvV2ZGZXBOb0dORDZWTmpoVG5Db0x1dnlNNzQ0SEhhZUp6RzVVZmtTYS1lNlF3TGV6VTdoZXNtaTFzWS1sNWdQMVVnaUQ4el90WDE3UmFvU3c?oc=5
- [CRITICAL] 8622 水戸証券 | Tue, 28 Apr 2026 | earnings | 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTFB2UWpSZ2ZPQk5zd0k2Y0lfMzZuZUx3TTVLT2kxY000UElhaEc2MmViNEc2Zl9SZ2hIYVVHTmtfSTd3Uk9DVmdmM050WlJhcUFpVktoYjk2c1FSM3VmcWV5bklLQXg4OFFVX2c?oc=5
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006252/p15079219_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-09-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526390696/eqbk-20260910.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-15 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006318/p15075054_6-k.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-09-16 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000020/nwfl-20260916x8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006339/p15081246_6-k.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-09-16 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000089512626000053/exe-20260916.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-09-16 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000110465926108003/tm2625334d2_8k.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000162828026062234/fro-20260630.htm
- [HIGH] TEN Tsakos Energy Navigation Ltd Common Shares | 2026-09-17 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1166663/000119312526394366/d67788d6k.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-09-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000110465926108570/tm2625334d5_8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-18 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006391/p15095918_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-24 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006471/p15100061_6-k.htm
- [HIGH] ACNB ACNB Corporation - Common Stock | 2026-09-25 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/715579/000162828026063501/acnb-20260925.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006535/p15101807_6-k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-09-30 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026063997/stng6k-09302026.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-10-02 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526412356/wsbc-20261002.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-05 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006663/p15102252_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-05 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526412873/d16704d8k.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-10-06 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000110465926114046/tm2627119d1_8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026065357/stng6k-10072026.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006740/p15109105_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006733/p15107743_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-09 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006837/p15110413_6-k.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-13 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000063/buse-20261013.htm
- [HIGH] DHT DHT Holdings, Inc. | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1331284/000095015726001092/form6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006892/p15111556_6-k.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-10-13 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000089512626000057/exe-20261008.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526421701/eqbk-20261014.htm
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-10-15 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000119312526422936/d439916d8k.htm
- [HIGH] 4996 クミアイ化学工業 | 2026-10-19 | filing | 訂正臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z8G2
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-19 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026066288/stng6k-10192026.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-10-19 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000110465926116739/tm2627775d1_8k.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-10-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526427870/wsbc-20261021.htm
- [HIGH] 8622 水戸証券 | Mon, 09 Mar 2026 | dividend | 水戸証券、株主優待を新設して、配当＋優待利回り＝6.4％に！ 3月末に1000株以上の保有で地域特産品がもらえるが、来期以降は｢1年以上の継続保有｣が必須に - ダイヤモンド・オンライン | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiU0FVX3lxTE1QRlFKekV1VHlONVFFNmFzTzBKQ1FiajFfb2RmSjJIdE9qZmR4MkJ4RnEtRGhVLU51ZFo0dzRkMGJJNjY3d242azlHN19TLXZ6R1V3?oc=5
- [HIGH] 6701 NEC | Tue, 20 Oct 2026 | regulatory | NEC 委託先へのサイバー攻撃で個人情報漏えい - TBS NEWS DIG | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiV0FVX3lxTFAtUXY2ZVBoZm05SG5IeDhlOGRwRlhCVjdUQlVWOU1lUDRJVXhWd2V2ODJ3d2g4R09XT1p5aHBEU2pEMkZGbUJDNk1BTlBjcGZ5YlBZc0VHTQ?oc=5
- [HIGH] 8766 東京海上ホールディングス | Tue, 25 Aug 2026 | dividend | 東京海上、今期配当を実質増額修正 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE9wT0xDYXFnWmlOMU5XMTZsR0pNQjRHNkdLVWI0bGRPTWJrMlNHVnBZRWFQSFpsQ0lycFcwdzhuY1NLWGxIQXRFazlsV1lmSjdLZlE?oc=5
- [HIGH] 5032 ANYCOLOR | Wed, 09 Sep 2026 | buyback | 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMibEFVX3lxTE9SUEU1ZE41TXRpU2h5VTAyb1F4N3BWRTR5YTFFM0FDR1hJTHZrNWlRVUp3MlRuelBKYlpKNU0zTU15QWxaclYwejV0Y2pNWXkxMXgwVFY4U3RYRFpIRmNZanA3MExrQUF4Slk3eg?oc=5
- [HIGH] 8766 東京海上ホールディングス | Wed, 20 May 2026 | dividend | 東京海上HD(8766)、7期連続の「増配」を発表し、配当利回り3.1％に！ 年間配当は7年で3.2倍に増加、2027年3月期は前期比27円増の｢1株あたり245円｣に - ダイヤモンド・オンライン | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiU0FVX3lxTE9Sdko0cVUyckIzOWZqVUxYV3V6MlFsd2FpQk1Fem1FbXlEXzVORTNqb1V0b3dJc2dueEV5eXI1dlVOUWdsYkFDYUsyRnNtTFZ1QVlv?oc=5
- [HIGH] 6701 NEC | Wed, 21 Oct 2026 | regulatory | 委託事業者における個人情報漏えいについて - 大阪大学 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiZEFVX3lxTE9yX29uY2R4V2FsaXJqM2VBdGlVSlFDMFNLQVoyb2g0MmRQYkZfZ2EwTG1hMDA1RENHTmUzbkF1WTFiRnAxdjRwd2otLTlVMVVvMlBsM3dkWUMwOVZGbHI1M2ZCdkk?oc=5
- [HIGH] 6701 NEC | Wed, 21 Oct 2026 | regulatory | 大阪公立大のシステム障害、NECの再委託先へのサイバー攻撃が原因 [大阪府] [情報漏洩・個人情報流出の最新ニュース] - 朝日新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiZ0FVX3lxTE56T2dydkYycXU0QUdWYzJlWklTS05uTVVqS3QwYmhPM0JuMlNNZFVYMnVyOGNzV1E0NS11YjNNcExfb3RiNzNTU0hST1NMaUdqQlR4d2ZHQ2h6bVR4bElwV1FHWFJ1OWc?oc=5
- [HIGH] 6701 NEC | Wed, 21 Oct 2026 | regulatory | NECの委託先にサイバー攻撃、複数顧客でシステム障害と情報漏洩 - 日経クロステック | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiXEFVX3lxTE1VY1lKSXJFa3lxYWJPYWZCZmthb0pSeE1NUnkwa1lsWDJkRnVJek5SX0dZU1ByeVNpU2l1ZDFCNFp2UUgyX1FsQlp2LXFWcmlpYlV4ZC1aN2Nfa1Nw?oc=5

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.