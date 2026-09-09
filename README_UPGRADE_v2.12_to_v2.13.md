# Upgrade v2.12 → v2.13: Monitored-Security Supply / Demand Context

## Purpose

Add a security-level supply/demand observation layer for the explicit watchlist and current screening leaders.  The layer helps identify situations where a small tradable float, elevated turnover, short crowding, or unusual volume can amplify price moves or make execution difficult.

It is deliberately separate from the five-factor security score and the Market Regime score.

## Data and calculations

The company-intelligence snapshot now requests these secondary Yahoo Finance fields for monitored targets:

- shares outstanding and float shares
- current and average volume
- shares short, prior-month shares short, short percent of float, and days to cover
- insider and institutional ownership observations
- regular-market price change and observation time

`src/supply_demand.py` validates and derives, when the required same-row inputs exist:

- free-float ratio
- average and current daily turnover of free float
- current volume versus 30-day average
- one-day notional execution capacity at the configured 10% participation rate
- short percent of float and days to cover
- month-over-month change in shares short
- non-directional context flags such as `TIGHT_FLOAT`, `SHORT_CROWDING`, and `PRICE_DOWN_ON_VOLUME_EXPANSION`

Missing values are never filled from peers, prior days, or market-cap assumptions.  A derived value is calculated only from explicitly observed inputs in the same record.

## Source hierarchy

Yahoo Finance observations are marked `secondary`.  An optional dated, sourced file at `config/supply_demand_manual.csv` can override individual fields with verified primary-source values.  The schema is documented in `config/supply_demand_manual.example.csv`.

## Outputs

- `data/supply_demand/supply_demand_latest.csv`
- `data/supply_demand/supply_demand_summary_latest.json`
- `data/supply_demand/supply_demand_summary_latest.md`
- `data/supply_demand/supply_demand_history.csv`

The post-close and morning intelligence workflows regenerate these files after Company Intelligence.  The integrated report and mobile brief show coverage and exceptional contexts.

## Governance and privacy

- The layer does not alter security ranking, factor score, fundamental assessment, Market Regime score, or investment thesis.
- It may influence only monitoring priority, execution caution, and liquidity due diligence.
- High volume with a price move is described as co-movement; it is not labelled accumulation or distribution.
- Public workflow targets are the public watchlist and screening leaders.  Private portfolio quantities are not read or written by this layer.
- Existing stable fallback behavior is unchanged.
