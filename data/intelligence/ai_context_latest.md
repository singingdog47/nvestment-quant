# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.838** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-11-10T04:08:15+00:00",
  "generated_at_utc": "2026-11-10T04:08:15+00:00",
  "date_jst": "2026-11-10",
  "data_status": "ok",
  "regime_label": "NEUTRAL",
  "regime_score": 43.05,
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
    "trend": 19.828681363809842,
    "stress": 71.83249994277955,
    "participation": 36.01548059149723,
    "liquidity": 37.934458926556175,
    "positioning": 62.462051551193944
  },
  "evidence": {
    "trend_series": 4,
    "vix": 19.920000076293945,
    "hy_oas": 3.42,
    "ig_oas": 0.93,
    "treasury_volatility_proxy": 86.458,
    "treasury_volatility_percentile_rank": 0.873,
    "treasury_volatility_stress_score": 34.52,
    "treasury_volatility_as_of_date": "2026-11-09",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9540,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-11-06T15:05:36.552022+00:00",
    "nfci": -0.459,
    "volume_ratio20_mean": 0.6180364731639043,
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
    "jpx_official_turnover_date": "2026-11-09",
    "jpx_official_turnover_million_jpy": 9698328.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-11-10",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 31,
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
        "spot": 60041.0390625,
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
  "generated_at": "2026-11-10T04:09:26+00:00",
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
      "age_hours": 0.03,
      "stale_limit_hours": 36
    },
    "v1_3_screening_full": {
      "status": "ok",
      "path": "data/screening_full.csv.gz",
      "age_hours": 0.03,
      "stale_limit_hours": 36
    },
    "v1_3_quality": {
      "status": "ok",
      "path": "data/quality_report.json",
      "age_hours": 0.03,
      "stale_limit_hours": 36
    },
    "v1_3_daily_report": {
      "status": "ok",
      "path": "data/daily_report.md",
      "age_hours": 0.03,
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
- EDINET: ok / records=20 / tier=primary
- SEC: ok / records=38 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=54 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-11-06T15:05:36.552022+00:00
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
| JP | 1 | 545A.T | Toranvia Co.,Ltd. | Other | 75.2 | 100.0 | unchanged |
| JP | 2 | 6196.T | Strike Group Co.,Ltd. | Other | 73.5 | 99.9 | unchanged |
| JP | 3 | 3932.T | Akatsuki Inc. | Other | 73.3 | 99.9 | unchanged |
| JP | 4 | 8622.T | Mito Securities Co.,Ltd. | Financials | 73.1 | 99.8 | unchanged |
| JP | 5 | 6750.T | ELECOM CO.,LTD. | Other | 73.0 | 99.8 | unchanged |
| JP | 6 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 71.9 | 99.7 | unchanged |
| JP | 7 | 4765.T | SBI Global Asset Management Co.,Ltd. | Financials | 71.7 | 99.7 | unchanged |
| JP | 8 | 2121.T | MIXI,Inc. | Other | 71.7 | 99.6 | unchanged |
| JP | 10 | 4516.T | Nippon Shinyaku Co.,Ltd. | Other | 71.6 | 99.5 | unchanged |
| JP | 11 | 8704.T | TRADERS HOLDINGS CO.,LTD. | Other | 71.1 | 99.5 | unchanged |
| US | 1 | LTC | LTC Properties, Inc. Common Stock | Other | 85.3 | 100.0 | unchanged |
| US | 2 | FISI | Financial Institutions, Inc. - Common Stock | Financials | 84.6 | 100.0 | unchanged |
| US | 3 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 83.9 | 99.9 | unchanged |
| US | 5 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 82.7 | 99.9 | unchanged |
| US | 9 | TRMD | TORM plc - Class A Common Stock | Other | 82.2 | 99.8 | unchanged |
| US | 12 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 81.3 | 99.7 | unchanged |
| US | 14 | DHT | DHT Holdings, Inc. | Shipping | 80.8 | 99.6 | unchanged |
| US | 16 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 80.5 | 99.5 | unchanged |
| US | 21 | EQBK | Equity Bancshares, Inc. Class A Common Stock | Other | 79.5 | 99.4 | unchanged |
| US | 24 | SFNC | Simmons First National Corporation - Common Stock | Other | 79.1 | 99.3 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 6965 浜松ホトニクス | Fri, 15 May 2026 | guidance | 浜松ホトニクス---ストップ高、1-3月期増益転換で通期予想を上方修正 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiYEFVX3lxTE9XTHM1aVlfSFZ6NzBMUFN1ZEZCZWNpd3lYRUFDdkdrU3M4d1gxRGN4aFk5eml1dTAwMnpxOFhsVzNsN2wzOTN1QlQ5dURqNHZEZDJxSkhlQ0UwcTZ0M2tIaw?oc=5
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Mon, 09 Nov 2026 | guidance | ほくほくフィナンシャルグループ[8377]：第6次中期経営計画における経営指標目標の上方修正に関するお知らせ 2026年11月9日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE1hY2RWV3hWNEF0dHRNWUtaeThZUm1wM29renlYc09KaGE4SUlxcThKLU5GOFR6UnhRTm1SNVB3QU8zUmhpbVpiVjhvam9fMXZxR0xUNmJjZ1pOVlpEZ0NwU0hxbzdLU2xUa0E?oc=5
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Mon, 09 Nov 2026 | earnings | ほくほくフィナンシャルグループ[8377]：2027年3月期 第2四半期（中間期）決算短信〔日本基準〕（連結） 2026年11月9日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE1EeXQza09USG5jdGpKQXVoOFBIZ3g4dmxxYzAza255eENvMXdZamJnelZnOHBBOVkzVzUxRWNDZExDaThSLVM4cWhMeFB1NmhEckFGRmZqQ25YeVRiRmI2UWI0S0RWX3NzUVE?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | earnings | コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE81MFUxNWxkd1lSOFc0SEQwUnc0LWVpTWZMMWoxTmxFTGZPaW9HYm5hTmQ2bG9zSGNzbndwaUwzbldXTTVLTk9UZ3pXUlM1MURtcl9qaEUwdVlWa2VTV1J1dVZOY0EtM3UzS1E?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | guidance | コーエーテクモホールディングス[3635]：業績予想及び配当予想の修正に関するお知らせ 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE9IdklGSEFRZnFvTkNReG5vRkZlVG91V2ItS2dWQXluQXVsZjRLeUMwVGFiV3F4V2dFcTNvaHRlZzBTTlViVFFvT09PV2g3NVJMZHloUks2cVlZc2kwQkJ5QkIwRFBrcndDZlE?oc=5
- [CRITICAL] 4063 信越化学工業 | Tue, 28 Apr 2026 | earnings | 信越化学工業[4063]：2026年３月期決算短信〔日本基準〕（連結） 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE9YU0drSkNQX0wta25uTlZNY08xZ0FXWk9pbFJoVFhMeVhocTZuNkpEZ3dMX0xMUDkzYTNUWVNYOTdlMlhLSnRIbGNIQTFfcXJRdW5FSWFFcWN1Y2pfN2JaVTBad3hDdk1neGc?oc=5
- [CRITICAL] 8622 水戸証券 | Tue, 28 Apr 2026 | earnings | 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTFB2UWpSZ2ZPQk5zd0k2Y0lfMzZuZUx3TTVLT2kxY000UElhaEc2MmViNEc2Zl9SZ2hIYVVHTmtfSTd3Uk9DVmdmM050WlJhcUFpVktoYjk2c1FSM3VmcWV5bklLQXg4OFFVX2c?oc=5
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006535/p15101807_6-k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-09-30 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026063997/stng6k-09302026.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-10-02 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526412356/wsbc-20261002.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-05 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006663/p15102252_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-05 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526412873/d16704d8k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-10-06 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526415565/d151159d8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026065357/stng6k-10072026.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006740/p15109105_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-07 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006733/p15107743_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-09 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006837/p15110413_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006892/p15111556_6-k.htm
- [HIGH] DHT DHT Holdings, Inc. | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1331284/000095015726001092/form6-k.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-13 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000063/buse-20261013.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526421701/eqbk-20261014.htm
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-10-15 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000119312526422936/d439916d8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-19 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026066288/stng6k-10192026.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-10-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526427870/wsbc-20261021.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526432747/ck0002017206-20261026.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000066/buse-20261027.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026067899/stng6k-q32026epr.htm
- [HIGH] FISI Financial Institutions, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/862831/000119312526437786/fisi-20260930.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000090/care-20261028.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000089/care-20261029.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-10-29 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526437801/wsbc-20260930.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122146/ltc-20260930x10q.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122029/ltc-20261103x8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000094/care-20261103.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007363/p15146295_6-k.htm
- [HIGH] 5032 ANYCOLOR | 2026-11-04 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZBC4
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-11-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526447297/ck0002017206-20260930.htm
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-11-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000162828026070069/sfnc-20260930.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-11-04 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526447256/wsbc-20261104.htm
- [HIGH] 8630 Sompo Holdings,Inc. | 2026-11-05 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZB6S
- [HIGH] 4765 SBI Global Asset Management Co.,Ltd. | 2026-11-05 | filing | 半期報告書－第30期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZC3X
- [HIGH] 4765 SBI Global Asset Management Co.,Ltd. | 2026-11-05 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZC3T
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000097/care-20260930.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000070/buse-20260930.htm
- [HIGH] 4559 ZERIA PHARMACEUTICAL CO.,LTD. | 2026-11-06 | filing | 半期報告書－第73期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZCEK
- [HIGH] 4559 ZERIA PHARMACEUTICAL CO.,LTD. | 2026-11-06 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZCEO
- [HIGH] 4503 Astellas Pharma Inc. | 2026-11-06 | filing | 半期報告書－第22期(2026/04/01－2026/09/30) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZA8P
- [HIGH] 4503 Astellas Pharma Inc. | 2026-11-06 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZA8V
- [HIGH] 4063 信越化学工業 | 2026-11-06 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZCLT
- [HIGH] 2121 MIXI,Inc. | 2026-11-06 | filing | 半期報告書－第28期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZC0H

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.