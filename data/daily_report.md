# Daily Quant Report

- Data retrieved (UTC): 2026-08-24T00:32:44.753412+00:00
- Price basis: TradingView scanner close; exact exchange timestamp unavailable.
- This report is for research. A high score is not a buy signal.

## Development status

- System version: v2.6
- Status: operational; cross-market score calibration and report-status visibility added
- Stable fallback: stable-report-v2.5
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
| US | Financials | 7 |
| US | Mortgage REIT | 4 |
| US | Other | 4 |
| US | Shipping | 5 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 78.3 | 100.0 | unchanged |
| JP | 2 | 3932.T | Akatsuki Inc. | Other | 77.1 | 99.9 | unchanged |
| JP | 3 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 76.7 | 99.9 | unchanged |
| JP | 4 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 75.5 | 99.8 | unchanged |
| JP | 9 | 6750.T | ELECOM CO.,LTD. | Other | 73.4 | 99.6 | unchanged |
| JP | 10 | 2121.T | MIXI,Inc. | Other | 72.4 | 99.5 | unchanged |
| JP | 11 | 8927.T | MEIHO ENTERPRISE CO.,LTD. | Other | 72.1 | 99.5 | unchanged |
| JP | 12 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 72.0 | 99.4 | unchanged |
| JP | 13 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 71.0 | 99.4 | unchanged |
| JP | 15 | 8789.T | FinTech Global Incorporated | Other | 70.6 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.0 | 100.0 | unchanged |
| US | 2 | INSW | International Seaways, Inc. Common Stock  | Shipping | 83.4 | 100.0 | unchanged |
| US | 3 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 83.3 | 99.9 | unchanged |
| US | 4 | DHT | DHT Holdings, Inc. | Shipping | 82.2 | 99.9 | unchanged |
| US | 5 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 81.8 | 99.9 | unchanged |
| US | 8 | ADAM | Adamas Trust, Inc. - Common Stock | Other | 81.2 | 99.8 | unchanged |
| US | 12 | BUSE | First Busey Corporation - Common Stock | Other | 80.7 | 99.7 | unchanged |
| US | 15 | WSBC | WesBanco, Inc. - Common Stock | Other | 80.3 | 99.6 | unchanged |
| US | 23 | ACNB | ACNB Corporation - Common Stock | Other | 78.2 | 99.4 | unchanged |
| US | 24 | DBRG | DigitalBridge Group, Inc. | Other | 78.2 | 99.3 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.
