# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.847** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-11-04T15:27:59+00:00",
  "generated_at_utc": "2026-11-04T15:27:59+00:00",
  "date_jst": "2026-11-05",
  "data_status": "ok",
  "regime_label": "NEUTRAL",
  "regime_score": 48.8,
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
  "thin_liquidity_flag": false,
  "treasury_volatility_shock_flag": false,
  "sq_execution_caution_flag": false,
  "regime_flags": [],
  "components": {
    "trend": 33.46305700031402,
    "stress": 75.37250034332276,
    "participation": 41.56163274745606,
    "liquidity": 37.28934209448062,
    "positioning": 60.106090833359694
  },
  "evidence": {
    "trend_series": 4,
    "vix": 16.979999542236328,
    "hy_oas": 3.4,
    "ig_oas": 0.93,
    "treasury_volatility_proxy": 81.856,
    "treasury_volatility_percentile_rank": 0.8056,
    "treasury_volatility_stress_score": 39.58,
    "treasury_volatility_as_of_date": "2026-11-03",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9549,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-11-04T15:27:57.331020+00:00",
    "nfci": -0.459,
    "volume_ratio20_mean": 0.6019085523620155,
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
    "jpx_official_turnover_date": "2026-11-04",
    "jpx_official_turnover_million_jpy": 11956505.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-11-05",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 36,
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
        "spot": 63081.859375,
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
  "generated_at": "2026-11-04T15:29:10+00:00",
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
- EDINET: ok / records=5 / tier=primary
- SEC: ok / records=31 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=56 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-11-04T15:27:57.331020+00:00
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
| JP | Financials | 5 |
| JP | Other | 15 |
| US | Financials | 12 |
| US | Other | 4 |
| US | Shipping | 4 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 6196.T | Strike Group Co.,Ltd. | Other | 74.7 | 100.0 | unchanged |
| JP | 2 | 545A.T | Toranvia Co.,Ltd. | Other | 74.3 | 99.9 | unchanged |
| JP | 3 | 6750.T | ELECOM CO.,LTD. | Other | 73.3 | 99.9 | unchanged |
| JP | 4 | 3932.T | Akatsuki Inc. | Other | 72.9 | 99.8 | unchanged |
| JP | 5 | 8622.T | Mito Securities Co.,Ltd. | Financials | 72.9 | 99.8 | unchanged |
| JP | 6 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 72.0 | 99.7 | unchanged |
| JP | 7 | 2121.T | MIXI,Inc. | Other | 72.0 | 99.7 | unchanged |
| JP | 8 | 8704.T | TRADERS HOLDINGS CO.,LTD. | Other | 71.7 | 99.6 | unchanged |
| JP | 9 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 71.6 | 99.6 | unchanged |
| JP | 10 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 71.4 | 99.5 | unchanged |
| US | 1 | FISI | Financial Institutions, Inc. - Common Stock | Financials | 84.1 | 100.0 | unchanged |
| US | 2 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 83.3 | 100.0 | unchanged |
| US | 4 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 82.8 | 99.9 | unchanged |
| US | 10 | DHT | DHT Holdings, Inc. | Shipping | 81.2 | 99.7 | unchanged |
| US | 12 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 80.7 | 99.7 | unchanged |
| US | 13 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 80.6 | 99.6 | unchanged |
| US | 17 | TRMD | TORM plc - Class A Common Stock | Other | 79.8 | 99.5 | unchanged |
| US | 18 | EQBK | Equity Bancshares, Inc. Class A Common Stock | Other | 79.7 | 99.5 | unchanged |
| US | 26 | SFNC | Simmons First National Corporation - Common Stock | Other | 78.7 | 99.2 | unchanged |
| US | 28 | HCI | HCI Group, Inc. Common Stock | Other | 78.6 | 99.2 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 6965 浜松ホトニクス | Fri, 15 May 2026 | guidance | 浜松ホトニクス---ストップ高、1-3月期増益転換で通期予想を上方修正 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiYEFVX3lxTE9XTHM1aVlfSFZ6NzBMUFN1ZEZCZWNpd3lYRUFDdkdrU3M4d1gxRGN4aFk5eml1dTAwMnpxOFhsVzNsN2wzOTN1QlQ5dURqNHZEZDJxSkhlQ0UwcTZ0M2tIaw?oc=5
- [CRITICAL] 4063 信越化学工業 | Fri, 30 Oct 2026 | guidance | 信越化学工業(4063) 電子材料部門の想定以上の好調を受け、業績予想を上方修正 - QUICK Money World | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiVkFVX3lxTFBtU0QtZkNiejUtR1BiQTdQZHYtUzAtMlRJcEZ0dXpTQnZxV0dlX2w1VFo2QmZjd2tlSkJ5d3lDal8wekM1UE1lTjg3b0hKQlJYUjRVbldn?oc=5
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Mon, 02 Nov 2026 | guidance | ほくほくフィナンシャルグループ[8377]：業績予想および配当予想の修正に関するお知らせ 2026年11月2日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTFBieHh0eEw2R2tvV0ozUC1KNDctemZMdjM5Xy1IX0RTZklGLUpCN2I2dXNtWnEyX0FpWTkwYU9oWXpTNG5VOEFubGdmREI0ZnhOaEFJWVpmZHRyMFE1SU8wTWhOM1RrQmRaekE?oc=5
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Mon, 02 Nov 2026 | guidance | ほくほくＦＧ、今期経常を22％上方修正・最高益予想を上乗せ、配当も22円増額 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE1WWl9KXzNGeXlTUE9oNWpseDZoRzNiZ0dZdm82MU1zUmpJMW44eldBR0Uyek5ud21IdUNkTERpSTFRd051MDhSVXFEY0JHRHNyclE?oc=5
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Mon, 02 Nov 2026 | guidance | 〔決算〕ほくほくFG、連結純利益420億円に上方修正＝26年9月中間(時事通信) - Yahoo!ファイナンス | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMihwFBVV95cUxPREFvVGlDaXpsVFUwU2VyVVdmbElPcDlaXy1ZUzlaTVFCbld5SGRselZQd21GR0ROc1o4SWJwM2hmSldIMnk1dVQ4RjZwclBIRXJ3LTRNWTlnYXNjbW5tcFQ5emJaSDFHMEJmcDN1V2czaDN1U0E5UDFVSkF4bFl6Y1VNWU53ckE?oc=5
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Mon, 02 Nov 2026 | guidance | ◎〔決算〕ほくほくＦＧ、連結純利益４２０億円に上方修正 - 時事通信ニュース | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiVEFVX3lxTE1DM2JsWXN1OXh0b25wTDJwYmtWY0tBbFFfUzVOeEJ2VGZpVmZONDRKdmNJSGJYcXVUY0JRMklmQzVDQVljcDA2V0doUVVEeWdQajNsQQ?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | earnings | コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE81MFUxNWxkd1lSOFc0SEQwUnc0LWVpTWZMMWoxTmxFTGZPaW9HYm5hTmQ2bG9zSGNzbndwaUwzbldXTTVLTk9UZ3pXUlM1MURtcl9qaEUwdVlWa2VTV1J1dVZOY0EtM3UzS1E?oc=5
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526396754/d73132d8k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-22 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526397284/d244618d8k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526399549/ck0002017206-20260923.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526398224/d126321d8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-24 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006471/p15100061_6-k.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-09-25 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926110666/tm2626112d1_8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006535/p15101807_6-k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-09-30 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026063997/stng6k-09302026.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-05 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006663/p15102252_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-05 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526412873/d16704d8k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-10-06 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526415565/d151159d8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026065357/stng6k-10072026.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006740/p15109105_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006733/p15107743_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-09 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006837/p15110413_6-k.htm
- [HIGH] DHT DHT Holdings, Inc. | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1331284/000095015726001092/form6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006892/p15111556_6-k.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-13 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000063/buse-20261013.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526421701/eqbk-20261014.htm
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-10-15 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000119312526422936/d439916d8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-19 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026066288/stng6k-10192026.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526432747/ck0002017206-20261026.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000066/buse-20261027.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026067899/stng6k-q32026epr.htm
- [HIGH] 6701 NEC | 2026-10-29 | filing | 半期報告書－第189期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZALL
- [HIGH] 6701 NEC | 2026-10-29 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZALS
- [HIGH] FISI Financial Institutions, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/862831/000119312526437786/fisi-20260930.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000090/care-20261028.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000089/care-20261029.htm
- [HIGH] 6701 NEC | 2026-10-30 | filing | 発行登録書（株券､社債券等） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZANF
- [HIGH] 3932 Akatsuki Inc. | 2026-10-30 | filing | 臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZB18
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000094/care-20261103.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007363/p15146295_6-k.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122146/ltc-20260930x10q.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122029/ltc-20261103x8k.htm
- [HIGH] 5032 ANYCOLOR | 2026-11-04 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZBC4
- [HIGH] 9433 KDDI | Fri, 30 Oct 2026 | regulatory | KDDI、顧客情報2万人分漏洩か ライフネット生命への不正アクセスで - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMibEFVX3lxTE9IQ3NfMzlqTzloTC1ZMjN3Y05sdVRHTWpIMjlmSkVNa2tQUzN2SkE5eFBkaWlsNlBNd3JOamRNMEpuM01BY0x3bk9mY21DaDlmdGtjZFRQMWRDTWJLZm5KX0lfSWkxbThmenhhUQ?oc=5
- [HIGH] 9433 KDDI | Mon, 02 Nov 2026 | regulatory | KDDI、2万2541件の顧客情報漏えいか ライフネット生命への不正アクセスで（アスキー） - Yahoo!ニュース | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMif0FVX3lxTFA0VlAzbG5oVUU2MzhxVjNTTUNMSHRJWTFTc0lUSGdZYWpGNDNta0Z6aGcyNVpDTDh3QWNkd3owbVhPZ1EydzR6Q1FBaXFQd3d4R3lFQldQOHE2V1BDd2JVMl9wWUFSeUgzUE5mSXJGLWEzREQ2VWh0VFM3ekRxVUU?oc=5
- [HIGH] 8622 水戸証券 | Mon, 02 Nov 2026 | buyback | 水戸証券[8622]：自己株式の取得状況に関するお知らせ 2026年11月2日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMizAFBVV95cUxOS1ZtVGh1ck1GZzl6dHZvczR6SHNzcW9peU1zNXEtX3N3T0RuWjI2ZmdjZ1VVeklBWC0xd0YxaVJWZHMxREo4MlIxX0QtWFNERHF4SzdGR2swRm01QVNhaWdTMkpqRHJUdldYeWVkLU40VG5oNXRiOTI4bWprbzkwQkxPdDZJNUpPbmVtZ2tqSHMxR2Z1LXFaOXFlZTNBQjlUU3FDUjM2OE1waXZ1Wi1WUXM0UHlnSjlUeGc3ZWpfek5vVEVmSUFLdU5KWXE?oc=5
- [HIGH] 8622 水戸証券 | Sat, 07 Mar 2026 | dividend | 水戸証券(8622)、4期連続となる「増配」を発表し、配当利回り5.9％に！ 年間配当は4年で3.0倍に増加、2026年3月期は前期比13円増の｢1株あたり43円｣に！ - ダイヤモンド・オンライン | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiU0FVX3lxTE1hN2dNanhnWGxoWUxBZ0JIaXpYYjUxU29WY2V4SDVrV05QZGV2OEFSbnFpS1ZyUHllaUJod0EycUgxUFA5ak4zVktwZ3Jjb1M2SjFN?oc=5
- [HIGH] 8766 東京海上ホールディングス | Tue, 25 Aug 2026 | dividend | 東京海上、今期配当を実質増額修正 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE9wT0xDYXFnWmlOMU5XMTZsR0pNQjRHNkdLVWI0bGRPTWJrMlNHVnBZRWFQSFpsQ0lycFcwdzhuY1NLWGxIQXRFazlsV1lmSjdLZlE?oc=5

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.