# Daily Quant Report

- Data retrieved (UTC): 2026-09-02T07:27:57.054761+00:00
- Price basis: TradingView scanner close; exact exchange timestamp unavailable.
- This report is for research. A high score is not a buy signal.

## Development status

- System version: v2.10
- Status: operational; private Drive history, valuation, monthly attribution v1.1, dynamic cash/tax friction and anti-FOMO execution controls active
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
| JP | Financials | 10 |
| JP | Other | 10 |
| US | Financials | 4 |
| US | Mortgage REIT | 5 |
| US | Other | 6 |
| US | Shipping | 5 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 77.8 | 100.0 | unchanged |
| JP | 2 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 76.9 | 99.9 | unchanged |
| JP | 3 | 3932.T | Akatsuki Inc. | Other | 76.5 | 99.9 | unchanged |
| JP | 5 | 8707.T | IwaiCosmo Holdings,Inc. | Other | 76.0 | 99.8 | unchanged |
| JP | 9 | 6750.T | ELECOM CO.,LTD. | Other | 73.3 | 99.6 | unchanged |
| JP | 10 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 72.1 | 99.5 | unchanged |
| JP | 11 | 2121.T | MIXI,Inc. | Other | 71.6 | 99.5 | unchanged |
| JP | 12 | 4763.T | CREEK & RIVER Co.,Ltd. | Other | 71.0 | 99.4 | unchanged |
| JP | 13 | 6927.T | Helios Techno Holding Co.,Ltd. | Other | 70.7 | 99.4 | unchanged |
| JP | 15 | 5351.T | SHINAGAWA REFRA CO.,LTD. | Other | 70.3 | 99.3 | unchanged |
| US | 1 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.1 | 100.0 | unchanged |
| US | 2 | MRP | Millrose Properties, Inc. Class A Common Stock | Other | 83.5 | 100.0 | unchanged |
| US | 3 | INSW | International Seaways, Inc. Common Stock  | Shipping | 82.8 | 99.9 | unchanged |
| US | 5 | ECO | Okeanis Eco Tankers Corp. Common Stock | Shipping | 82.3 | 99.9 | unchanged |
| US | 8 | NWFL | Norwood Financial Corp. - Common Stock | Financials | 81.6 | 99.8 | unchanged |
| US | 11 | ADAM | Adamas Trust, Inc. - Common Stock | Other | 80.9 | 99.7 | unchanged |
| US | 14 | BUSE | First Busey Corporation - Common Stock | Other | 80.2 | 99.6 | unchanged |
| US | 15 | WSBC | WesBanco, Inc. - Common Stock | Other | 80.1 | 99.6 | unchanged |
| US | 16 | TRMD | TORM plc - Class A Common Stock | Other | 80.0 | 99.6 | unchanged |
| US | 18 | FRO | Frontline Plc Ordinary Shares | Other | 79.7 | 99.5 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.
