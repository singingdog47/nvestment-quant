# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.858** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-10-21T00:38:49+00:00",
  "generated_at_utc": "2026-10-21T00:38:49+00:00",
  "date_jst": "2026-10-21",
  "data_status": "ok",
  "regime_label": "NEUTRAL",
  "regime_score": 52.9,
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
  "treasury_volatility_shock_flag": true,
  "sq_execution_caution_flag": false,
  "regime_flags": [
    "THIN_LIQUIDITY",
    "TREASURY_VOLATILITY_SHOCK"
  ],
  "components": {
    "trend": 52.82736456053606,
    "stress": 74.25000040054321,
    "participation": 39.791498209541416,
    "liquidity": 32.365874444621184,
    "positioning": 56.71738287234125
  },
  "evidence": {
    "trend_series": 4,
    "vix": 17.309999465942383,
    "hy_oas": 3.29,
    "ig_oas": 0.87,
    "treasury_volatility_proxy": 87.542,
    "treasury_volatility_percentile_rank": 0.9008,
    "treasury_volatility_stress_score": 32.44,
    "treasury_volatility_as_of_date": "2026-10-20",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9558,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-10-20T12:44:49.309669+00:00",
    "nfci": -0.499,
    "volume_ratio20_mean": 0.4718218611155295,
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
    "jpx_official_turnover_date": "2026-10-20",
    "jpx_official_turnover_million_jpy": 7563457.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-10-21",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 51,
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
        "spot": 65301.640625,
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
  "generated_at": "2026-10-21T00:39:57+00:00",
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
- EDINET: ok / records=2 / tier=primary
- SEC: ok / records=31 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=59 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-10-20T12:44:49.309669+00:00
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
| US | Financials | 12 |
| US | Other | 4 |
| US | Shipping | 4 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8613.T | Marusan Securities Co.,Ltd. | Financials | 81.8 | 100.0 | unchanged |
| JP | 2 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 77.7 | 99.9 | new_entry |
| JP | 4 | 3932.T | Akatsuki Inc. | Other | 75.1 | 99.8 | unchanged |
| JP | 6 | 6750.T | ELECOM CO.,LTD. | Other | 73.8 | 99.7 | unchanged |
| JP | 7 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 73.1 | 99.7 | unchanged |
| JP | 9 | 2121.T | MIXI,Inc. | Other | 71.3 | 99.6 | unchanged |
| JP | 11 | 8789.T | FinTech Global Incorporated | Other | 70.5 | 99.5 | unchanged |
| JP | 12 | 7744.T | Noritsu Koki Co.,Ltd. | Other | 70.0 | 99.4 | unchanged |
| JP | 13 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 70.0 | 99.4 | unchanged |
| JP | 14 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 69.9 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 85.3 | 100.0 | unchanged |
| US | 2 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 82.5 | 100.0 | unchanged |
| US | 4 | BUSE | First Busey Corporation - Common Stock | Other | 81.3 | 99.9 | unchanged |
| US | 5 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 81.3 | 99.9 | unchanged |
| US | 6 | DHT | DHT Holdings, Inc. | Shipping | 81.2 | 99.8 | unchanged |
| US | 11 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 80.3 | 99.7 | unchanged |
| US | 13 | TRMD | TORM plc - Class A Common Stock | Other | 80.2 | 99.6 | unchanged |
| US | 15 | WSBC | WesBanco, Inc. - Common Stock | Other | 79.9 | 99.6 | unchanged |
| US | 21 | SFNC | Simmons First National Corporation - Common Stock | Other | 79.0 | 99.4 | unchanged |
| US | 23 | EXE | Expand Energy Corporation - Common Stock | Other | 78.8 | 99.3 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Fri, 29 May 2026 | guidance | ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE5mOXJYY0tyRW8yQUhTZ09US2tkWVM0bEwzUEgteml0SlBUdVZTaU14M3NWZGNUX2FvLTdCb2Z3dHBTVi1WdmlkUVV5ZWZSRVM5SlE?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 19 Oct 2026 | guidance | コーエーテクモホールディングス[3635]：業績予想の修正に関するお知らせ 2026年10月19日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE41YlFlN0NMQVhsY2VxRUhGR0hvV2ZGZXBOb0dORDZWTmpoVG5Db0x1dnlNNzQ0SEhhZUp6RzVVZmtTYS1lNlF3TGV6VTdoZXNtaTFzWS1sNWdQMVVnaUQ4el90WDE3UmFvU3c?oc=5
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
- [HIGH] 6965 浜松ホトニクス | 2026-10-15 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z8FG
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-10-15 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000119312526422936/d439916d8k.htm
- [HIGH] 4996 クミアイ化学工業 | 2026-10-19 | filing | 訂正臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z8G2
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-19 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026066288/stng6k-10192026.htm
- [HIGH] EXE Expand Energy Corporation - Common Stock | 2026-10-19 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/895126/000110465926116739/tm2627775d1_8k.htm
- [HIGH] 6701 NEC | Tue, 20 Oct 2026 | regulatory | NEC 委託先へのサイバー攻撃で個人情報漏えい - TBS NEWS DIG | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiV0FVX3lxTFAtUXY2ZVBoZm05SG5IeDhlOGRwRlhCVjdUQlVWOU1lUDRJVXhWd2V2ODJ3d2g4R09XT1p5aHBEU2pEMkZGbUJDNk1BTlBjcGZ5YlBZc0VHTQ?oc=5
- [HIGH] 6701 NEC | Tue, 20 Oct 2026 | regulatory | ふるさとチョイス、情報流出445万件 NECは委託先から漏洩 - 朝日新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiZ0FVX3lxTE81T0c2NnJQU1hqdkY1Z3g0OTRlQlg3OXFEenU5MUtiZzBHNjBOaWo2V0piNlJBOWt3Wi1SM0RKUlp6ZHBJUmpjWmZmRGZvZ0RWS3lMQXA1a0V2VmoycEdFZ3AwbU1ZaGM?oc=5
- [HIGH] 6701 NEC | Tue, 20 Oct 2026 | regulatory | NEC、システム開発の委託先にサイバー攻撃 顧客3社の情報漏洩 - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMibEFVX3lxTE5hM1M2Q1pDTmZFY0pKRktaZHp1Um03c3V6bU5vd2dVR3RwVGxRMExBazdIU0FpREFCdGRsNUtqcXp3YWN5dHhHeG9WNFVhdjQxc0k1X0c3aFJ1VlJmS2xzUDEwVE9QVFduRXBPWg?oc=5
- [HIGH] 6701 NEC | Tue, 20 Oct 2026 | regulatory | ＮＥＣ委託先にサイバー攻撃、顧客企業３社の情報が漏えい…２社では個人情報漏えいを確認 - 読売新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiZkFVX3lxTE9kOHVXaVl4NjJ5ekl4b1VfTk50WDRlWUdKZVVhYy15ZVJMZlQyRF9UUm9BdHhoc01qVW1EVVJxUEs1N0dVX3RBQXJkYi1ILVp2blIyajItcmMxVUt1bDJiNnNCaU00Zw?oc=5
- [HIGH] 8766 東京海上ホールディングス | Wed, 07 Oct 2026 | buyback | 東京海上ホールディングス[8766]：自己株式の取得状況に関するお知らせ 2026年10月7日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE1FanduN011eWR1S1pDUmV3WGowYW9FelNDQTVnakRfeHBYRC1UdFhabmlCdmxpNlRpNmE1NlZfSnlqdDlrSEV3ZjRGcjAwbktDdkJtam9SdUNRSW5pU08ybXI2clhGUkUtUVE?oc=5
- [HIGH] 5032 ANYCOLOR | Wed, 09 Sep 2026 | buyback | 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMibEFVX3lxTE9SUEU1ZE41TXRpU2h5VTAyb1F4N3BWRTR5YTFFM0FDR1hJTHZrNWlRVUp3MlRuelBKYlpKNU0zTU15QWxaclYwejV0Y2pNWXkxMXgwVFY4U3RYRFpIRmNZanA3MExrQUF4Slk3eg?oc=5

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.