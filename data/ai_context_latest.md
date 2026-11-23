# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.838** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-11-23T19:16:14+00:00",
  "generated_at_utc": "2026-11-23T19:16:14+00:00",
  "date_jst": "2026-11-24",
  "data_status": "ok",
  "regime_label": "DEFENSIVE",
  "regime_score": 35.74,
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
  "treasury_volatility_shock_flag": true,
  "sq_execution_caution_flag": false,
  "regime_flags": [
    "TREASURY_VOLATILITY_SHOCK"
  ],
  "components": {
    "trend": 0.0,
    "stress": 62.66750017166137,
    "participation": 32.13334876721843,
    "liquidity": 49.0351474172597,
    "positioning": 62.86284683617225
  },
  "evidence": {
    "trend_series": 4,
    "vix": 27.489999771118164,
    "hy_oas": 3.76,
    "ig_oas": 0.98,
    "treasury_volatility_proxy": 100.289,
    "treasury_volatility_percentile_rank": 0.9722,
    "treasury_volatility_stress_score": 27.08,
    "treasury_volatility_as_of_date": "2026-11-20",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9526,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-11-23T19:16:11.764792+00:00",
    "nfci": -0.478,
    "volume_ratio20_mean": 0.8922286854314925,
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
    "jpx_official_turnover_date": "2026-11-20",
    "jpx_official_turnover_million_jpy": 9521475.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-11-24",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 17,
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
        "spot": 56436.6484375,
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
  "regime_label": "defensive",
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
  "generated_at": "2026-11-23T19:17:29+00:00",
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
- EDINET: ok / records=6 / tier=primary
- SEC: ok / records=38 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=40 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-11-23T19:16:11.764792+00:00
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
| US | Financials | 10 |
| US | Other | 5 |
| US | Shipping | 5 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 575A.T | MAEZAWA Holdings CO.,LTD. | Other | 78.7 | 100.0 | unchanged |
| JP | 2 | 6196.T | Strike Group Co.,Ltd. | Other | 75.4 | 99.9 | unchanged |
| JP | 3 | 4595.T | MIZUHO MEDY CO.,LTD. | Other | 75.0 | 99.9 | unchanged |
| JP | 4 | 6750.T | ELECOM CO.,LTD. | Other | 73.5 | 99.8 | unchanged |
| JP | 5 | 8622.T | Mito Securities Co.,Ltd. | Financials | 73.1 | 99.8 | unchanged |
| JP | 6 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 72.3 | 99.7 | unchanged |
| JP | 7 | 8704.T | TRADERS HOLDINGS CO.,LTD. | Other | 71.8 | 99.7 | unchanged |
| JP | 9 | 3252.T | JINUSHI Co.,Ltd. | Other | 70.8 | 99.6 | unchanged |
| JP | 10 | 8892.T | ES-CON JAPAN Ltd. | Other | 70.6 | 99.5 | unchanged |
| JP | 11 | 3932.T | Akatsuki Inc. | Other | 70.6 | 99.5 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.3 | 100.0 | unchanged |
| US | 2 | LTC | LTC Properties, Inc. Common Stock | Other | 83.7 | 100.0 | unchanged |
| US | 3 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 82.5 | 99.9 | unchanged |
| US | 4 | HBNC | Horizon Bancorp, Inc. - Common Stock | Financials | 81.6 | 99.9 | unchanged |
| US | 5 | DHT | DHT Holdings, Inc. | Shipping | 81.4 | 99.9 | unchanged |
| US | 6 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 81.3 | 99.8 | unchanged |
| US | 11 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 80.1 | 99.7 | unchanged |
| US | 19 | SD | SandRidge Energy, Inc. Common Stock | Other | 78.6 | 99.4 | rank_up |
| US | 20 | TRMD | TORM plc - Class A Common Stock | Other | 78.4 | 99.4 | unchanged |
| US | 23 | FRO | Frontline Plc Ordinary Shares | Other | 78.3 | 99.3 | rank_up |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 4063 信越化学工業 | Tue, 27 Oct 2026 | earnings | 信越化学工業[4063]：2027年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月27日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE1KcDR4STR3TU1xeG02UW10bGtTVjVjQ2Qzbmw3ZkFIQWhadTdhRFI4aTFHYXR0bVlyYmFmc0R0SXgySE01WGNyenJPT0hVNTIxZGtDcVJaSmF3UzViVDNuZkdNTmJCUWQ0dkE?oc=5
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-09 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006837/p15110413_6-k.htm
- [HIGH] DHT DHT Holdings, Inc. | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1331284/000095015726001092/form6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-10-13 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006892/p15111556_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-10-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526421701/eqbk-20261014.htm
- [HIGH] IRWD Ironwood Pharmaceuticals, Inc. - Class A Common Stock | 2026-10-16 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1446847/000110465926116423/tm2627624d1_8k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-19 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026066288/stng6k-10192026.htm
- [HIGH] HBNC Horizon Bancorp, Inc. - Common Stock | 2026-10-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/706129/000070612926000082/hbnc-20261021.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526432747/ck0002017206-20261026.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026067899/stng6k-q32026epr.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000090/care-20261028.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000089/care-20261029.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000094/care-20261103.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122146/ltc-20260930x10q.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122029/ltc-20261103x8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007363/p15146295_6-k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-11-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526447297/ck0002017206-20260930.htm
- [HIGH] SD SandRidge Energy, Inc. Common Stock | 2026-11-04 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1349436/000162828026070276/sd-20261103.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000097/care-20260930.htm
- [HIGH] SD SandRidge Energy, Inc. Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1349436/000162828026071179/sd-20260930.htm
- [HIGH] IRWD Ironwood Pharmaceuticals, Inc. - Class A Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1446847/000110465926123319/irwd-20260930x10q.htm
- [HIGH] IRWD Ironwood Pharmaceuticals, Inc. - Class A Common Stock | 2026-11-05 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1446847/000110465926123029/tm2629044d1_8k.htm
- [HIGH] HBNC Horizon Bancorp, Inc. - Common Stock | 2026-11-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/706129/000070612926000087/hbnc-20260930.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-06 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007482/p15147800_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-11-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526451860/eqbk-20260930.htm
- [HIGH] DHT DHT Holdings, Inc. | 2026-11-09 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1331284/000114036126042813/ef20080524_6k.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000226/nhi-20261109.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000223/nhi-20261109.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000222/nhi-20261109.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000221/nhi-20260930.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-12 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000100/care-20261109.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-12 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007622/p15153820_6-k.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-13 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000230/nhi-20261109.htm
- [HIGH] CEPO Cantor Equity Partners I, Inc. - Class A Ordinary Shares | 2026-11-16 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2027708/000121390026120664/ea0310993-10q_cantor1.htm
- [HIGH] 9639 SANKYO FRONTIER CO.,LTD. | 2026-11-18 | filing | 訂正有価証券届出書（参照方式） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZIKT
- [HIGH] 9639 SANKYO FRONTIER CO.,LTD. | 2026-11-18 | filing | 訂正有価証券届出書（参照方式） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZIOR
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-18 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426008184/p15157214_6-k.htm
- [HIGH] 8766 東京海上ホールディングス | 2026-11-19 | filing | 半期報告書－第25期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZIN2
- [HIGH] 8766 東京海上ホールディングス | 2026-11-19 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZIN7
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-11-19 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526468835/eqbk-20261119.htm
- [HIGH] 2802 味の素 | 2026-11-20 | filing | 発行登録追補書類（株券､社債券等） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZJ44
- [HIGH] 6196 Strike Group Co.,Ltd. | 2026-11-20 | filing | 臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZJBN
- [HIGH] TEN Tsakos Energy Navigation Ltd Common Shares | 2026-11-20 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1166663/000119312526470357/d138948d6k.htm
- [HIGH] TEN Tsakos Energy Navigation Ltd Common Shares | 2026-11-20 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1166663/000119312526470281/d140309d6k.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-11-20 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000091957426008221/p15160196_6-k.htm
- [HIGH] 8622 水戸証券 | Mon, 02 Nov 2026 | buyback | 水戸証券[8622]：自己株式の取得状況に関するお知らせ 2026年11月2日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE96bHMwcS0zNVhKMUNXNGhmS0FYb3dSbGFkWDRGR2lLVkhadjRSUzEwcXdiVldIMDBGYjZlMVVSckRSVVhOWEpSdnlXTFhpT2VHNFB5YlR0WFFsYXUtUV81dnloWU1qUUNuRnc?oc=5
- [HIGH] 8622 水戸証券 | Mon, 09 Mar 2026 | dividend | 水戸証券、株主優待を新設して、配当＋優待利回り＝6.4％に！ 3月末に1000株以上の保有で地域特産品がもらえるが、来期以降は｢1年以上の継続保有｣が必須に - ダイヤモンド・オンライン | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiU0FVX3lxTE1QRlFKekV1VHlONVFFNmFzTzBKQ1FiajFfb2RmSjJIdE9qZmR4MkJ4RnEtRGhVLU51ZFo0dzRkMGJJNjY3d242azlHN19TLXZ6R1V3?oc=5

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.