# Investment Quant v1.7 — Decision Log / Validation Layer

## Purpose

v1.7 adds a verification layer to the existing screening, market-regime and company-intelligence pipeline. The goal is not automated trading. It is to preserve what the system knew and recommended at the time, then measure the result later.

## Priority 1 implemented in this branch

1. Immutable decision snapshots
   - captured timestamp
   - model version
   - market regime and regime components
   - data-quality gate
   - deterministic recommended action (`WAIT_DATA_QUALITY` when blocked, otherwise `REVIEW` unless an explicit action already exists)
   - Top-N screening candidates and available factor scores
   - exact input-file SHA256 hashes, sizes and timestamps

2. Ex-post outcome evaluation
   - 1 week / 1 month / 3 month horizons
   - return
   - maximum rise and maximum decline within the observation window
   - per-symbol outcome rows in `data/validation/outcomes.csv`

3. Validation reports
   - average return and win rate by horizon
   - results by market regime
   - results by recommended action
   - machine-readable metrics JSON

4. Safety / anti-overfitting rules
   - no factor-weight auto-tuning
   - model changes require human review and a version bump
   - missing data remains distinguishable from bad model decisions
   - brokerage holdings and actual human trades are not committed to the public repository

## Outputs

- `data/validation/decisions/YYYY/*.json`
- `data/validation/outcomes.csv`
- `data/validation/validation_report_latest.md`
- `data/validation/validation_metrics_latest.json`

## Human action logging

Decision snapshots include a stable `decision_id`. Actual brokerage actions should be stored in a private source and joined by this ID. This avoids leaking portfolio transactions into the public repository.

## Workflow

`.github/workflows/validation-v1.7.yml` runs at 17:20 JST on weekdays, after the v1.6 intelligence refresh. It captures the current decision snapshot, evaluates any due historical outcomes, generates the validation report, runs tests, and commits only `data/validation` outputs.

## Next priorities

- Priority 2: portfolio risk engine (beta, concentration, sector, correlation, FX/rate sensitivity, VaR and drawdown contribution)
- Priority 3: exception detection and INFO/WATCH/WARNING/CRITICAL alerts
- Priority 4: richer factor model and regime-dependent factor weights
