# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.838** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-11-16T02:11:53+00:00",
  "generated_at_utc": "2026-11-16T02:11:53+00:00",
  "date_jst": "2026-11-16",
  "data_status": "ok",
  "regime_label": "NEUTRAL",
  "regime_score": 43.7,
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
    "trend": 18.599090241051215,
    "stress": 71.1125005722046,
    "participation": 40.39217954650625,
    "liquidity": 40.12133172259429,
    "positioning": 62.462051551193944
  },
  "evidence": {
    "trend_series": 4,
    "vix": 19.299999237060547,
    "hy_oas": 3.2,
    "ig_oas": 0.89,
    "treasury_volatility_proxy": 106.528,
    "treasury_volatility_percentile_rank": 0.996,
    "treasury_volatility_stress_score": 25.3,
    "treasury_volatility_as_of_date": "2026-11-13",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9533,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-11-13T15:25:50.869251+00:00",
    "nfci": -0.462,
    "volume_ratio20_mean": 0.6721832930648572,
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
    "jpx_official_turnover_date": "2026-11-13",
    "jpx_official_turnover_million_jpy": 9086090.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-11-16",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 25,
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
        "spot": 60154.75,
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
  "generated_at": "2026-11-16T02:14:25+00:00",
  "components": {
    "market_regime": {
      "status": "ok",
      "path": "data/regime/market_regime_latest.json",
      "age_hours": 0.03,
      "stale_limit_hours": 36
    },
    "v1_3_screening": {
      "status": "ok",
      "path": "data/screening_latest.csv",
      "age_hours": 0.05,
      "stale_limit_hours": 36
    },
    "v1_3_screening_full": {
      "status": "ok",
      "path": "data/screening_full.csv.gz",
      "age_hours": 0.05,
      "stale_limit_hours": 36
    },
    "v1_3_quality": {
      "status": "ok",
      "path": "data/quality_report.json",
      "age_hours": 0.05,
      "stale_limit_hours": 36
    },
    "v1_3_daily_report": {
      "status": "ok",
      "path": "data/daily_report.md",
      "age_hours": 0.05,
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
- EDINET: ok / records=43 / tier=primary
- SEC: ok / records=39 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=0 / tier=secondary
- yfinance: ok / records=40 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-11-13T15:25:50.869251+00:00
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
| US | Financials | 11 |
| US | Other | 4 |
| US | Shipping | 5 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 6196.T | Strike Group Co.,Ltd. | Other | 75.6 | 100.0 | unchanged |
| JP | 2 | 8622.T | Mito Securities Co.,Ltd. | Financials | 74.5 | 100.0 | unchanged |
| JP | 3 | 7937.T | TSUTSUMI JEWELRY CO.,LTD. | Other | 73.8 | 99.9 | new_entry |
| JP | 4 | 8704.T | TRADERS HOLDINGS CO.,LTD. | Other | 72.7 | 99.9 | unchanged |
| JP | 5 | 2121.T | MIXI,Inc. | Other | 72.3 | 99.8 | unchanged |
| JP | 6 | 6750.T | ELECOM CO.,LTD. | Other | 72.2 | 99.8 | unchanged |
| JP | 7 | 3252.T | JINUSHI Co.,Ltd. | Other | 72.1 | 99.7 | rank_up |
| JP | 8 | 4765.T | SBI Global Asset Management Co.,Ltd. | Financials | 71.6 | 99.7 | unchanged |
| JP | 11 | 3932.T | Akatsuki Inc. | Other | 71.3 | 99.5 | unchanged |
| JP | 12 | 8892.T | ES-CON JAPAN Ltd. | Other | 71.2 | 99.5 | unchanged |
| US | 1 | LTC | LTC Properties, Inc. Common Stock | Other | 84.4 | 100.0 | unchanged |
| US | 2 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.2 | 100.0 | unchanged |
| US | 3 | HBNC | Horizon Bancorp, Inc. - Common Stock | Financials | 83.2 | 99.9 | new_entry |
| US | 5 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 81.7 | 99.9 | unchanged |
| US | 6 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 81.6 | 99.8 | unchanged |
| US | 11 | DHT | DHT Holdings, Inc. | Shipping | 80.7 | 99.7 | unchanged |
| US | 16 | TRMD | TORM plc - Class A Common Stock | Other | 79.7 | 99.5 | unchanged |
| US | 18 | EQBK | Equity Bancshares, Inc. Class A Common Stock | Other | 79.4 | 99.5 | unchanged |
| US | 22 | SFNC | Simmons First National Corporation - Common Stock | Other | 78.7 | 99.4 | unchanged |
| US | 24 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 78.5 | 99.3 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 6701 NEC | 2026-11-13 | mna | 公開買付届出書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZHMY
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
- [HIGH] HBNC Horizon Bancorp, Inc. - Common Stock | 2026-10-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/706129/000070612926000082/hbnc-20261021.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526432747/ck0002017206-20261026.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-10-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000066/buse-20261027.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-10-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026067899/stng6k-q32026epr.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000090/care-20261028.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-10-29 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000089/care-20261029.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122146/ltc-20260930x10q.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926122029/ltc-20261103x8k.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-03 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000094/care-20261103.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007363/p15146295_6-k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-11-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526447297/ck0002017206-20260930.htm
- [HIGH] SFNC Simmons First National Corporation - Common Stock | 2026-11-04 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/90498/000162828026070069/sfnc-20260930.htm
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000097/care-20260930.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-11-05 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000070/buse-20260930.htm
- [HIGH] HBNC Horizon Bancorp, Inc. - Common Stock | 2026-11-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/706129/000070612926000087/hbnc-20260930.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-11-06 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426007482/p15147800_6-k.htm
- [HIGH] EQBK Equity Bancshares, Inc. Class A Common Stock | 2026-11-06 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1227500/000119312526451860/eqbk-20260930.htm
- [HIGH] BUSE First Busey Corporation - Common Stock | 2026-11-06 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/314489/000031448926000072/buse-20261106.htm
- [HIGH] DHT DHT Holdings, Inc. | 2026-11-09 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1331284/000114036126042813/ef20080524_6k.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000226/nhi-20261109.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000223/nhi-20261109.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000222/nhi-20261109.htm
- [HIGH] NHI National Health Investors, Inc. Common Stock | 2026-11-09 | earnings | SEC 10-Q filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/877860/000087786026000221/nhi-20260930.htm
- [HIGH] 2802 味の素 | 2026-11-10 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZDBT
- [HIGH] 3635 コーエーテクモホールディングス | 2026-11-10 | filing | 半期報告書－第18期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZCG7
- [HIGH] 3635 コーエーテクモホールディングス | 2026-11-10 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZCGA
- [HIGH] 4507 Shionogi & Co.,Ltd. | 2026-11-10 | filing | 発行登録書（株券､社債券等） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZDPD
- [HIGH] 4994 Taisei Lamick Group Head Quarter & Innovation Co.,Ltd. | 2026-11-10 | filing | 半期報告書－第62期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZD1B
- [HIGH] 4994 Taisei Lamick Group Head Quarter & Innovation Co.,Ltd. | 2026-11-10 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZD28
- [HIGH] 9433 KDDI | 2026-11-10 | filing | 半期報告書－第43期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZDAA
- [HIGH] 9433 KDDI | 2026-11-10 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZDB0
- [HIGH] 5351 SHINAGAWA REFRA CO.,LTD. | 2026-11-11 | filing | 半期報告書－第193期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZEA5
- [HIGH] 5351 SHINAGAWA REFRA CO.,LTD. | 2026-11-11 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZEE6
- [HIGH] 4507 Shionogi & Co.,Ltd. | 2026-11-11 | filing | 半期報告書－第162期(2026/04/01－2027/03/31) | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZEGF
- [HIGH] 4507 Shionogi & Co.,Ltd. | 2026-11-11 | filing | 確認書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZEGI
- [HIGH] 3099 三越伊勢丹ホールディングス | 2026-11-12 | filing | 自己株券買付状況報告書（法２４条の６第１項に基づくもの） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100ZFLZ

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.