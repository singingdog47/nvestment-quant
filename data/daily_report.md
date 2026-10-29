# Daily Quant Report

- Data retrieved (UTC): 2026-10-29T14:23:26.716187+00:00
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
| US | Other | 2 |
| US | Shipping | 6 |

## Research candidates

| Market | Mkt Rank | Ticker | Name | Theme | Raw score | Cross-mkt pct | Daily change |
|---|---:|---|---|---|---:|---:|---|
| JP | 1 | 8622.T | Mito Securities Co.,Ltd. | Financials | 80.0 | 100.0 | unchanged |
| JP | 2 | 8624.T | Ichiyoshi Securities Co.,Ltd. | Financials | 77.6 | 99.9 | new_entry |
| JP | 4 | 545A.T | Toranvia Co.,Ltd. | Other | 74.0 | 99.8 | unchanged |
| JP | 5 | 6750.T | ELECOM CO.,LTD. | Other | 73.4 | 99.8 | unchanged |
| JP | 6 | 3932.T | Akatsuki Inc. | Other | 72.7 | 99.7 | unchanged |
| JP | 8 | 6036.T | KeePer Technical Laboratory Co.,Ltd. | Other | 72.5 | 99.6 | rank_up |
| JP | 9 | 2121.T | MIXI,Inc. | Other | 71.4 | 99.6 | unchanged |
| JP | 10 | 3635.T | KOEI TECMO HOLDINGS CO.,LTD. | Other | 71.0 | 99.5 | unchanged |
| JP | 11 | 7744.T | Noritsu Koki Co.,Ltd. | Other | 70.8 | 99.5 | unchanged |
| JP | 12 | 4516.T | Nippon Shinyaku Co.,Ltd. | Other | 70.3 | 99.4 | unchanged |
| US | 1 | STNG | Scorpio Tankers Inc. Common Shares | Shipping | 84.6 | 100.0 | unchanged |
| US | 2 | CARE | Carter Bankshares, Inc. - Common Stock | Financials | 84.6 | 100.0 | unchanged |
| US | 3 | HBNC | Horizon Bancorp, Inc. - Common Stock | Financials | 82.9 | 99.9 | new_entry |
| US | 6 | TEN | Tsakos Energy Navigation Ltd Common Shares | Other | 82.4 | 99.8 | unchanged |
| US | 7 | DHT | DHT Holdings, Inc. | Shipping | 82.3 | 99.8 | unchanged |
| US | 12 | TRMD | TORM plc - Class A Common Stock | Other | 81.2 | 99.7 | unchanged |
| US | 21 | EQBK | Equity Bancshares, Inc. Class A Common Stock | Other | 79.4 | 99.4 | unchanged |
| US | 24 | FRO | Frontline Plc Ordinary Shares | Other | 78.9 | 99.3 | unchanged |
| US | 25 | SFNC | Simmons First National Corporation - Common Stock | Other | 78.8 | 99.3 | unchanged |
| US | 27 | BUSE | First Busey Corporation - Common Stock | Other | 78.6 | 99.2 | unchanged |

## Required manual checks before an order

1. Verify the current executable price with the broker.
2. Check the latest earnings release, guidance, and material disclosures.
3. Do not add a second name with the same economic driver without reducing another position.

## Earnings-calendar status

No official cross-market earnings-calendar source is connected. Earnings-date alerts are intentionally marked unavailable rather than guessed.
