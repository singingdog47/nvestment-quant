# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.745** / actionable=True

## Market Regime v1.5
{
  "version": "1.5.3",
  "engine_version": "1.5.3",
  "generated_at": "2026-10-01T15:41:23+00:00",
  "generated_at_utc": "2026-10-01T15:41:23+00:00",
  "date_jst": "2026-10-02",
  "data_status": "ok",
  "regime_label": "CONSTRUCTIVE",
  "regime_score": 61.0,
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
    "trend": 72.66510715563918,
    "stress": 74.57250062942505,
    "participation": 43.7182594644506,
    "liquidity": 40.29581130714533,
    "positioning": 57.66981615729503
  },
  "evidence": {
    "trend_series": 4,
    "vix": 17.1299991607666,
    "hy_oas": 3.12,
    "ig_oas": 0.84,
    "treasury_volatility_proxy": 86.234,
    "treasury_volatility_percentile_rank": 0.9365,
    "treasury_volatility_stress_score": 29.76,
    "treasury_volatility_as_of_date": "2026-09-30",
    "treasury_volatility_status": "ok",
    "treasury_volatility_is_ice_move": false,
    "breadth_n": 9570,
    "breadth_status": "ok",
    "breadth_source_as_of_utc": "2026-10-01T15:41:21.001238+00:00",
    "nfci": -0.548,
    "volume_ratio20_mean": 0.6614952826786331,
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
    "jpx_official_turnover_date": "2026-10-01",
    "jpx_official_turnover_million_jpy": 9675554.0,
    "jpx_official_turnover_status": "ok"
  },
  "execution_overlay": {
    "sq": {
      "version": "1.0",
      "enabled": true,
      "active": false,
      "as_of_date": "2026-10-02",
      "next_major_sq_date": "2026-12-11",
      "days_to_sq": 70,
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
        "spot": 66753.71875,
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
  "generated_at": "2026-10-01T15:42:25+00:00",
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
- EDINET: ok / records=3 / tier=primary
- SEC: ok / records=34 / tier=primary
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=20 / tier=secondary
- yfinance: ok / records=36 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-10-01T15:41:21.001238+00:00
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
| JP | Financials | 8 |
| JP | Other | 12 |
| US | Financials | 8 |
| US | Mortgage REIT | 1 |
| US | Other | 5 |
| US | Shipping | 6 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 75.0 | 100.0 | unchanged |
| JP | 2 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 74.6 | 99.9 | unchanged |
| JP | 3 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 74.2 | 99.9 | new_entry |
| JP | 6 | 3932.T | Akatsuki Inc. | Other | 73.6 | 99.7 | unchanged |
| JP | 8 | 6750.T | ELECOM CO.,LTD. | Other | 72.7 | 99.6 | unchanged |
| JP | 10 | 2121.T | MIXI,Inc. | Other | 70.8 | 99.5 | unchanged |
| JP | 11 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 70.3 | 99.5 | unchanged |
| JP | 12 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 70.3 | 99.4 | unchanged |
| JP | 13 | 4763.T | CREEK & RIVER Co.,Ltd. | Other | 70.1 | 99.4 | unchanged |
| JP | 14 | 8789.T | FinTech Global Incorporated | Other | 69.8 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.1 | 100.0 | unchanged |
| US | 2 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 83.7 | 100.0 | unchanged |
| US | 3 | INSW | International Seaways, Inc. Common Stock  | Shipping | 83.2 | 99.9 | unchanged |
| US | 5 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 81.9 | 99.9 | unchanged |
| US | 6 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 81.6 | 99.9 | unchanged |
| US | 10 | BUSE | First Busey Corporation - Common Stock | Other | 80.6 | 99.7 | unchanged |
| US | 12 | TRMD | TORM plc - Class A Common Stock | Other | 80.3 | 99.7 | unchanged |
| US | 13 | FRO | Frontline Plc Ordinary Shares | Other | 80.2 | 99.6 | unchanged |
| US | 20 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 78.6 | 99.4 | unchanged |
| US | 22 | WSBC | WesBanco, Inc. - Common Stock | Other | 78.5 | 99.4 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 4063 信越化学工業 | Wed, 30 Sep 2026 | financing | 信越化学工業[4063]：取締役、執行役員及び従業員に対するストックオプション（新株予約権）の払込金額確定のお知らせ 2026年9月30日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE5zMFJma2EzNDVTUnlraDhFdnhBSXlQdksydzlWMjlCQjlNZ0p0NDVZTkZhVmlXbDRnLU5SWk40N1RHVWw5OXVjaklmQTVKY0tpb25IcGJkWkNXTm93WU5vYjdmZzRjRDYzVXc?oc=5
- [HIGH] CARE Carter Bankshares, Inc. - Common Stock | 2026-08-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1829576/000182957626000083/care-20260817.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-08-17 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026057375/stng6k-08172026.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-24 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426005684/p15057626_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-26 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000162828026058979/trmd-20260630.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-08-26 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000162828026058978/tormplc6-kaugust262026pres.htm
- [HIGH] WSBC WesBanco, Inc. - Common Stock | 2026-08-27 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/203596/000119312526371610/wsbc-20260827.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-08-28 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000018/nwfl-20260828x8k.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-08-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000091957426005942/p15060813_6k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-08-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426005821/p15059931_6-k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-01 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526378466/d83131d8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-02 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006143/p15072501_6k.htm
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-09-03 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026060459/stng6k-09032026.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-09-04 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426006193/p15074444_6-k.htm
- [HIGH] LPG Dorian LPG Ltd. Common Stock | 2026-09-04 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1596993/000159699326000041/lpg-20260902x8k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-09-08 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000091957426006196/p15076578_6-k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-11 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006252/p15079219_6-k.htm
- [HIGH] LPG Dorian LPG Ltd. Common Stock | 2026-09-14 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1596993/000159699326000046/lpg-20260910x8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-15 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006318/p15075054_6-k.htm
- [HIGH] NWFL Norwood Financial Corp. - Common Stock | 2026-09-16 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1013272/000101327226000020/nwfl-20260916x8k.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006339/p15081246_6-k.htm
- [HIGH] FRO Frontline Plc Ordinary Shares | 2026-09-16 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/913290/000162828026062234/fro-20260630.htm
- [HIGH] TEN Tsakos Energy Navigation Ltd Common Shares | 2026-09-17 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1166663/000119312526394366/d67788d6k.htm
- [HIGH] HTGC Hercules Capital, Inc. Common Stock | 2026-09-17 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1280784/000128078426000046/htgc-20260917.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-18 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006391/p15095918_6-k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-21 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526396754/d73132d8k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-22 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526397284/d244618d8k.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526399549/ck0002017206-20260923.htm
- [HIGH] MRP Millrose Properties, Inc. Class A Common Stock | 2026-09-23 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/2017206/000119312526398224/d126321d8k.htm
- [HIGH] CMBT CMB.TECH NV Ordinary Shares | 2026-09-23 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1604481/000160448126000010/eurn-20260630.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-24 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006471/p15100061_6-k.htm
- [HIGH] LTC LTC Properties, Inc. Common Stock | 2026-09-25 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/887905/000110465926110666/tm2626112d1_8k.htm
- [HIGH] ACNB ACNB Corporation - Common Stock | 2026-09-25 | filing | SEC 8-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/715579/000162828026063501/acnb-20260925.htm
- [HIGH] TRMD TORM plc - Class A Common Stock | 2026-09-28 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1655891/000091957426006535/p15101807_6-k.htm
- [HIGH] 6701 NEC | 2026-09-29 | filing | 変更報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z50A
- [HIGH] 4063 信越化学工業 | 2026-09-30 | filing | 訂正臨時報告書 | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z5HO
- [HIGH] 4063 信越化学工業 | 2026-09-30 | filing | 訂正有価証券届出書（参照方式） | EDINET (primary) | status=ok | https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S100Z5CC
- [HIGH] STNG Scorpio Tankers Inc. Common Shares | 2026-09-30 | filing | SEC 6-K filing | SEC EDGAR (primary) | status=ok | https://www.sec.gov/Archives/edgar/data/1483934/000162828026063997/stng6k-09302026.htm
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