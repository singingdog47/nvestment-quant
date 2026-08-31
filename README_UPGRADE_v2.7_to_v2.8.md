# Upgrade v2.7 -> v2.8

## Purpose

The August 2026 monthly review exposed two measurement gaps that can materially distort investment decisions:

1. Portfolio valuation could not be measured consistently because current holdings and fundamental multiples were not joined at portfolio weights.
2. Month-over-month account balance changes could be mistaken for investment returns when deposits, withdrawals, purchases, sales, or transfers were mixed in.

v2.8 adds measurement layers for both issues without weakening the existing v1.9+ degraded-data safeguards.

## 1. Portfolio Valuation Engine

New module: `src/portfolio_valuation.py`

### Metrics

- Aggregate P/E: calculated from weighted earnings yield, not arithmetic mean P/E.
- Aggregate P/B: calculated from weighted book yield, not arithmetic mean P/B.
- Earnings yield.
- Weighted dividend yield.
- Weighted ROE.
- Weighted earnings growth and revenue growth.
- Relative Value Score.
- Quality and Growth context.
- Value-trap guard score and flags.

### Coverage rules

Every metric reports portfolio market-value coverage. Missing fund look-through or missing fundamentals are not filled with zero.

- Core valuation coverage >=70%: calculation can be `current`.
- Partial match: `reference_only`.
- Insufficient match: `withheld`.

### Evidence rule

Screening fundamentals from secondary/undocumented providers can be used for relative review, but do not make valuation trade-actionable. Primary IR / EDINET / TDnet / SEC confirmation is required before valuation is promoted to an actionable conclusion.

This deliberately separates:

`calculation possible` != `decision actionable`.

## 2. Monthly Performance Diagnostics

New module: `src/monthly_performance.py`

### Critical rule

`balance change != investment return`

The engine calculates and labels holdings balance changes, but exact TWR remains `withheld` until external cash-flow timing and boundary valuations are available.

### What can still be measured with incomplete cash-flow data

- Start/end holdings market value.
- Observation-window quality.
- Whether the window spans month-end boundaries.
- Quantity-change detection.
- Price return and estimated price P/L for unchanged-quantity holdings.
- Attribution coverage.
- Material trading-activity warning.

A cash-flow-adjusted residual may be calculated if explicit flows are supplied, but it remains `reference_only` and is not substituted for TWR.

## 3. Private Pipeline Integration

`src/run_portfolio_risk.py` now generates, in the private runner only:

- `portfolio_valuation_latest.json`
- `portfolio_valuation_latest.md`
- `portfolio_monthly_latest.json`
- `portfolio_monthly_latest.md`

The existing public/private boundary remains intact. These files are not added to public Actions artifacts or public repository commits.

When `PORTFOLIO_DRIVE_WRITEBACK=true`, the new private files are eligible for writeback to the configured private Drive folder under the same policy as the existing private risk outputs. Default remains `false`.

## 4. Integrated Report

`src/final_report.py` now appends, only to the private integrated report when available:

1. Portfolio risk
2. Portfolio valuation
3. Monthly diagnostics
4. Private alerts

The public report only states the measurement status and governance rules; it does not persist holdings or private valuation values.

## 5. CI

`Private Portfolio Engine Tests v2.8` now covers:

- existing portfolio policy tests;
- reciprocal P/E aggregation;
- valuation coverage gating;
- secondary-source actionability guard;
- missing-fund non-imputation;
- balance-change/TWR separation;
- quantity-change exclusion from price attribution;
- reference-only cash-flow residual behavior.

## 6. What v2.8 still does not claim

The following remain intentionally incomplete rather than guessed:

- exact portfolio TWR without dated external cash flows and boundary valuations;
- historical self-valuation comparison before private valuation snapshots are persisted;
- fund-level valuation without look-through holdings/fundamentals;
- primary-source valuation confirmation for every holding when only secondary screening fundamentals are available;
- fair-value price targets from simple P/E or P/B alone.

## 7. Next measurement priorities

1. Dated deposit/withdrawal ledger ingestion and exact TWR subperiod chaining.
2. Primary-fundamental join for held names from IR/EDINET/TDnet/SEC.
3. Persisted private month-end valuation snapshots for self-history comparison.
4. Sector/rate/FX/cyclicality factor attribution with fund look-through where available.
5. Benchmark-relative monthly attribution and max-drawdown reporting.

## Governance

- No automated order placement.
- No automatic factor-weight or coefficient changes.
- Missing data degrades only the affected component.
- `WAIT / do nothing` remains a valid decision.
- Model changes still follow record -> evaluate -> proposal -> out-of-sample validation -> human approval.
