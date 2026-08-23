# Investment Quant v1.8 — Portfolio Risk Engine

Priority 2 of the adopted system design.

## Purpose

Evaluate a security not only as a standalone investment, but by whether adding it improves the current portfolio's risk/return structure.

This layer is deterministic. It does not place orders and it does not allow AI prose to change numerical risk metrics.

## Metrics

When market history is available, v1.8 calculates:

- portfolio beta versus a configurable benchmark (default `1306.T`)
- annualized historical volatility
- 1-day historical VaR / CVaR
- historical maximum drawdown
- average pairwise correlation
- covariance-based risk contribution by holding
- concentration HHI, effective number of holdings, largest and Top-5 weights
- sector / region / currency / market-cap / style exposures when supplied
- portfolio-weighted FX sensitivity and interest-rate sensitivity when supplied
- weighted factor tilts from the existing screening system

For screening candidates it simulates a configurable new position (default 2%) and measures:

- correlation with the existing portfolio
- change in annualized volatility
- change in VaR
- change in HHI
- portfolio-level verdict: `IMPROVES`, `NEUTRAL`, or `WORSENS`

The verdict is a diversification/risk verdict only. It is not a buy/sell signal.

## Private portfolio input

The public repository must never contain brokerage holdings.

The scheduled GitHub Actions workflow reads `portfolio_latest.csv` from the private Google Drive folder configured by:

- `GDRIVE_SERVICE_ACCOUNT_JSON`
- `GDRIVE_FOLDER_ID`

Results are written directly back to the same Drive folder as:

- `portfolio_risk_latest.json`
- `portfolio_risk_latest.md`

No portfolio file or risk report is committed to GitHub or uploaded as a GitHub Actions artifact.

### Minimum CSV columns

One identifier:

- `ticker`, or
- `code` (Japanese 4-digit codes can also include `market=JP`)

And one sizing field:

- `weight`, or
- `market_value`

Recommended optional metadata:

- `name`
- `sector`
- `region`
- `currency`
- `market_cap_bucket`
- `style`
- `fx_sensitivity`
- `rate_sensitivity`

Missing metadata remains missing. The engine does not guess it.

## Automation

`.github/workflows/portfolio-risk-v1.8.yml` runs at 17:05 JST on weekdays, after the post-close intelligence and decision layers. It can also be run manually.

If the private Drive secrets are absent, the workflow safely skips the private analysis instead of fabricating portfolio data.

## Governance

- Historical risk estimates are not forecasts.
- Missing data is surfaced rather than imputed as fact.
- Portfolio output is private by default.
- Candidate verdicts do not place orders.
- Human review remains required before any portfolio action.

## Next priority

Priority 3: exception detection and alerts (VIX/volume/flows/breadth/VaR/earnings/regime/rank changes), with INFO/WATCH/WARNING/CRITICAL severity.
