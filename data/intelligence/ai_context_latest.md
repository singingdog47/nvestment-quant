# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.864** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-10-26T15:08:32+00:00",
  "generated_at_utc": "2026-10-26T15:08:32+00:00",
  "date_jst": "2026-10-27",
  "data_status": "ok",
  "regime_label": "NEUTRAL",
  "regime_score": 48.23,
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
    "trend": 40.891692907326885,
    "stress": 72.52499977111816,
    "participation": 41.53952843273232,
    "liquidity": 24.109141475477394,
    "positioning": 59.04864260835684
  },
  "evidence": {
    "trend_series": 4,
    "vix": 17.93000030517578,
    "hy_oas": 3.38,
    "ig_oas": 0.91,
    "treasury_volatility_proxy": 89.332,
    "treasury_volatility_percentile_rank": 0.9325,
    "treasury_volatility_stress_score": 30.06,
    "treasury_volatility_as_of_date": "2026-10-23",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9559,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-10-26T15:08:29.840357+00:00",
    "nfci": -0.496,
    "volume_ratio20_mean": 0.26592853688693485,
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
    "jpx_official_turnover_date": "2026-10-26",
    "jpx_official_turnover_million_jpy": 7359607.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-10-27",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 45,
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
        "spot": 62693.16015625,
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
  "generated_at": "2026-10-26T15:09:35+00:00",
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
- EDINET: ok / records=1 / tier=primary
- SEC: ok / records=29 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=54 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-10-26T15:08:29.840357+00:00
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
| JP | Financials | 7 |
| JP | Other | 13 |
| US | Financials | 13 |
| US | Other | 3 |
| US | Shipping | 4 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8613.T | Marusan Securities Co.,Ltd. | Financials | 81.8 | 100.0 | unchanged |
| JP | 2 | 8622.T | Mito Securities Co.,Ltd. | Financials | 80.1 | 99.9 | unchanged |
| JP | 5 | 6750.T | ELECOM CO.,LTD. | Other | 73.4 | 99.8 | unchanged |
| JP | 6 | 3932.T | Akatsuki Inc. | Other | 73.3 | 99.7 | unchanged |
| JP | 8 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 71.9 | 99.6 | unchanged |
| JP | 9 | 545A.T | Toranvia Co.,Ltd. | Other | 71.4 | 99.6 | unchanged |
| JP | 11 | 7744.T | Noritsu Koki Co.,Ltd. | Other | 71.2 | 99.5 | unchanged |
| JP | 12 | 2121.T | MIXI,Inc. | Other | 70.8 | 99.4 | unchanged |
| JP | 13 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 70.3 | 99.4 | unchanged |
| JP | 14 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 70.3 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 85.6 | 100.0 | unchanged |
| US | 2 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 83.3 | 100.0 | unchanged |
| US | 3 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 82.7 | 99.9 | unchanged |
| US | 5 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 82.4 | 99.9 | unchanged |
| US | 6 | DHT | DHT Holdings, Inc. | Shipping | 82.3 | 99.8 | unchanged |
| US | 11 | BUSE | First Busey Corporation - Common Stock | Other | 81.7 | 99.7 | unchanged |
| US | 13 | TRMD | TORM plc - Class A Common Stock | Other | 81.4 | 99.6 | unchanged |
| US | 25 | SFNC | Simmons First National Corporation - Common Stock | Other | 79.4 | 99.3 | unchanged |
| US | 26 | FRO | Frontline Plc Ordinary Shares | Other | 79.1 | 99.2 | unchanged |
| US | 28 | EQBK | Equity Bancshares, Inc. Class A Common Stock | Other | 79.1 | 99.2 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 8377 ほくほくフィナンシャルグループ | Fri, 29 May 2026 | guidance | ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE5mOXJYY0tyRW8yQUhTZ09US2tkWVM0bEwzUEgteml0SlBUdVZTaU14M3NWZGNUX2FvLTdCb2Z3dHBTVi1WdmlkUVV5ZWZSRVM5SlE?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | guidance | コーテクＨＤ、今期経常を21％上方修正、配当も8円増額 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE9pMjBXRG1BckVMTG1GNnQ4cWpoNGVBX01oZkhhSXNZNHZERFdxSDk0czlpVVdtZ2RQU3NhamtJN1k1SHRWcmkza2ktemJjd3JLZ3c?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | earnings | コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE81MFUxNWxkd1lSOFc0SEQwUnc0LWVpTWZMMWoxTmxFTGZPaW9HYm5hTmQ2bG9zSGNzbndwaUwzbldXTTVLTk9UZ3pXUlM1MURtcl9qaEUwdVlWa2VTV1J1dVZOY0EtM3UzS1E?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | guidance | コーエーテクモホールディングス[3635]：業績予想及び配当予想の修正に関するお知らせ 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE9IdklGSEFRZnFvTkNReG5vRkZlVG91V2ItS2dWQXluQXVsZjRLeUMwVGFiV3F4V2dFcTNvaHRlZzBTTlViVFFvT09PV2g3NVJMZHloUks2cVlZc2kwQkJ5QkIwRFBrcndDZlE?oc=5
- [CRITICAL] 3635 コーエーテクモホールディングス | Mon, 26 Oct 2026 | earnings | コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMizAFBVV95cUxNY3Nqd1I0OTczUndPdmg0RjQ3TWYyVUF5Ry1tUERRYnRvMjA2UUlOLUk0bnhrZE9BNGcwem4wZEhELV9IUmUxazNoSXlpR2VaeVdSN3kzU2ZhMWdDNGVSemUwNzJ4R0NYV2N5T0V3aUM4R2F6dWRmLU5OdFY3RUJ6UG9rZXdMckJPNjRONXBJOW1TWkE5cDJ4Tmw1TmowRWZYbFRpblV6bFpraWdHZkhaWmRhM0dpUTJ4eVUyY2RBSlNiTl93U0dvS0tGVlg?oc=5
- [CRITICAL] 4063 信越化学工業 | Tue, 28 Apr 2026 | earnings | 信越化学工業[4063]：2026年３月期決算短信〔日本基準〕（連結） 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE9YU0drSkNQX0wta25uTlZNY08xZ0FXWk9pbFJoVFhMeVhocTZuNkpEZ3dMX0xMUDkzYTNUWVNYOTdlMlhLSnRIbGNIQTFfcXJRdW5FSWFFcWN1Y2pfN2JaVTBad3hDdk1neGc?oc=5
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006252/p15079219_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-09-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526390696/eqbk-20260910.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-15 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006318/p15075054_6-k.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-09-16 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000020/nwfl-20260916x8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006339/p15081246_6-k.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000162828026062234/fro-20260630.htm
- [HIGH] TEN Tsakos Energy Navigation Ltd Common Shares | 2026-09-17 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1166663/000119312526394366/d67788d6k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-18 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006391/p15095918_6-k.htm
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
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-13 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000063/buse-20261013.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006892/p15111556_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526421701/eqbk-20261014.htm
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-10-15 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000119312526422936/d439916d8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-19 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026066288/stng6k-10192026.htm
- [HIGH] 8630 Sompo Holdings,Inc. | 2026-10-23 | filing | 変更報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z8VM
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