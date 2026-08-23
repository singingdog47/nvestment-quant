# AI Decision Context — Investment Quant v1.6

Generated quality score: **0.325** / actionable=False

## Market Regime v1.5
{
  "version": "1.5.0",
  "generated_at": "2026-08-23T22:23:53+00:00",
  "regime_label": "CONSTRUCTIVE",
  "regime_score": 67.84,
  "confidence": 1.0,
  "actionable": true,
  "overheated_flag": false,
  "stress_flag": false,
  "thin_liquidity_flag": false,
  "regime_flags": [],
  "components": {
    "trend": 80.41362399703866,
    "stress": 84.60999965667725,
    "participation": 56.23128311448975,
    "liquidity": 43.02708929807408,
    "positioning": 48.60196300007342
  },
  "evidence": {
    "trend_series": 4,
    "vix": 15.130000114440918,
    "hy_oas": null,
    "ig_oas": null,
    "breadth_n": 9584,
    "nfci": null,
    "volume_ratio20_mean": 0.8605417859614816,
    "positioning_sources": {
      "jpx_raw_healthy": 3,
      "cftc_normalized_values": 22
    }
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
  "decision_gate": "BLOCK_DATA_QUALITY",
  "note": "Guardrail only. This file never places orders."
}

## Integration health
{
  "generated_at": "2026-08-23T22:28:36+00:00",
  "components": {
    "market_regime": {
      "status": "ok",
      "path": "data/regime/market_regime_latest.json",
      "age_hours": 0.0,
      "stale_limit_hours": 36
    },
    "v1_3_screening": {
      "status": "ok",
      "path": "data/screening_latest.csv",
      "age_hours": 0.08,
      "stale_limit_hours": 36
    },
    "v1_3_screening_full": {
      "status": "ok",
      "path": "data/screening_full.csv.gz",
      "age_hours": 0.08,
      "stale_limit_hours": 36
    },
    "v1_3_quality": {
      "status": "ok",
      "path": "data/quality_report.json",
      "age_hours": 0.08,
      "stale_limit_hours": 36
    },
    "v1_3_daily_report": {
      "status": "ok",
      "path": "data/daily_report.md",
      "age_hours": 0.08,
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
- EDINET: missing / records=0 / tier=primary / EDINET_API_KEY not set
- SEC: missing / records=0 / tier=primary / SEC_USER_AGENT not set
- CompanyIR: ok / records=0 / tier=primary
- NewsRSS: ok / records=15 / tier=secondary
- yfinance: ok / records=36 / tier=secondary

## v1.3 Daily Quant Screen report (existing output; preserved)
# Daily Quant Report

- Data retrieved (UTC): 2026-08-23T22:23:51.893740+00:00
- Price basis: TradingView scanner close; exact exchange timestamp unavailable.
- This report is for research. A high score is not a buy signal.

## Concentration guard

- Maximum displayed research candidates per market for Financials or Shipping: 2
- Mortgage REITs are watch-only and excluded from the research-candidate list.

## Theme distribution in unfiltered score leaders

| Market | Theme | Names in top 20 |
|---|---|---:|
| JP | Financials | 9 |
| JP | Other | 11 |
| US | Financials | 7 |
| US | Mortgage REIT | 4 |
| US | Other | 4 |
| US | Shipping | 5 |

## Research candidates

| Market | Rank | Ticker | Name | Theme | Score | Daily change |
|---|---:|---|---|---|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 78.3 | unchanged |
| JP | 2 | 3932.T | Akatsuki Inc. | Other | 76.9 | unchanged |
| JP | 3 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 76.9 | unchanged |
| JP | 5 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 75.3 | unchanged |
| JP | 8 | 6750.T | ELECOM CO.,LTD. | Other | 73.5 | unchanged |
| JP | 10 | 2121.T | MIXI,Inc. | Other | 72.7 | unchanged |
| JP | 11 | 8927.T | MEIHO ENTERPRISE CO.,LTD. | Other | 71.8 | unchanged |
| JP | 12 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 71.5 | unchanged |
| JP | 13 | 8789.T | FinTech Global Incorporated | Other | 71.1 | unchanged |
| JP | 15 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 70.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.0 | unchanged |
| US | 2 | INSW | International Seaways, Inc. Common Stock  | Shipping | 83.4 | unchanged |
| US | 3 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 83.3 | unchanged |
| US | 4 | DHT | DHT Holdings, Inc. | Shipping | 82.2 | unchanged |
| US | 5 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 81.8 | unchanged |
| US | 8 | ADAM | Adamas Trust, Inc. - Common Stock | Other | 81.2 | unchanged |
| US | 12 | BUSE | First Busey Corporation - Common Stock | Other | 80.7 | unchanged |
| US | 15 | WSBC | WesBanco, Inc. - Common Stock | Other | 80.3 | unchanged |
| US | 23 | ACNB | ACNB Corporation - Common Stock | Other | 78.2 | unchanged |
| US | 24 | DBRG | DigitalBridge Group, Inc. | Other | 78.2 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected in v1.3. Earnings-date alerts are intentionally marked unavailable rather than guessed.


## Critical / high company events
- [CRITICAL] 4063 信越化学工業 | Fri, 24 Jul 2026 | earnings | 信越化学工業[4063]：2027年３月期 第１四半期決算短信〔日本基準〕（連結） 2026年7月24日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiakFVX3lxTE04eUN0Wk9UOTF4cmQ3Q3NfbXZGZ1pKN1pqQVhEdUVHNld1ZFJTUlk0Rm51UjVMUTlzdHFrYVJGakJiY2Z1WXgyTXJGankxVm1PV01UejJqN2s1dlNBVU03aTF5aVNMOEw0d2c?oc=5
- [HIGH] 4063 信越化学工業 | Fri, 24 Jul 2026 | dividend | 信越化、非開示だった今期経常は9％増益、未定だった配当は10円増配 - 株探 | Google News RSS (secondary) | status=unverified | https://news.google.com/rss/articles/CBMiUkFVX3lxTE92Zk0xTEFjb1BRVW1zRUpOb21xRmRtZTB6MkhQZkNKUWxPRERJZ2JEUlVSYXprUk0tZjk3WGdoTGlhVEZmM3A4TXBtb29XNWd4b1E?oc=5

## Mandatory AI rules
- Primary source > secondary news > model inference.
- A secondary RSS item is a detection signal, never sufficient evidence for a trade.
- If a material fact is missing/stale, write 判断不能 or データ未取得.
- Distinguish price date, event date, filing date, and fetched_at.
- Market Regime is context, not an automatic buy/sell signal.
- v1.3 screening score is candidate ranking, not a trade recommendation.
- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.
- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately.