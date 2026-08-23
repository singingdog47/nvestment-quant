# Investment Quant v1.7 — Decision Validation System

v1.7 changes the system from a daily analytics pipeline into a versioned, testable decision-support process. It does **not** automate order execution.

## Implemented

### Priority 1 — Decision log / validation database
- Every run stores the UTC timestamp, system version, input SHA-256 hashes, market regime, risk level, deterministic recommended action, factor weights, Top-10 candidates, factor scores, reason/flags, and optional human action.
- `data/decision_log/decisions.jsonl` is append-only at the application level and preserves what the system knew at that time.
- Matured 1W / 1M / 3M observations are evaluated with market prices when available. Missing prices remain `unavailable`; they are never imputed.
- `data/decision_system/outcomes_latest.csv` stores returns and maximum favorable/adverse moves.
- `validation_report_latest.md` summarizes only matured observations.
- Validation results **never auto-change model weights**. Any model change requires human review and a versioned code/config change.

### Priority 2 — Portfolio-risk interface
- `portfolio_risk_latest.json` is produced every run.
- Because this repository is public, private positions are not inferred or committed. Default status is `private_data_required`.
- If a deliberately safe `data/portfolio_latest.csv` is provided and `ALLOW_REPO_PORTFOLIO=1`, v1.7 computes weight concentration (HHI/effective holdings), portfolio beta when available, theme concentration, and weighted factor tilts.
- Further private portfolio analytics can be joined from Drive/account data without weakening the public-repository privacy guardrail.

### Priority 3 — Exception detection
- `alerts_latest.json` uses deterministic thresholds and emits INFO / WATCH / WARNING / CRITICAL.
- Initial rules cover Panic/Risk-Off regimes, large screening-rank jumps, and portfolio concentration when private portfolio inputs are intentionally enabled.

### Priority 4 — Factor model / regime linkage
- Existing deterministic factors are separated and recombined as Value, Quality, Growth, Momentum, Risk and Liquidity.
- Regime-specific weights are versioned in code for Risk-On, Risk-Off/Panic, Recovery, Overheated and neutral conditions.
- `factor_scores_latest.csv` records the regime-adjusted score and rank so later validation can attribute changes to factors and regime.

## Workflow

`.github/workflows/decision-system-v1.7.yml` runs after the morning and post-close intelligence refreshes:
- 07:45 JST weekdays
- 16:45 JST weekdays

It runs the full repository test suite, executes `src/run_decision_system.py`, uploads 30-day artifacts, and commits only public-safe v1.7 outputs.

## Human action recording

For a manual run, the workflow can pass `HUMAN_ACTION` and `HUMAN_ACTION_NOTE`. If omitted, the log explicitly records `NOT_RECORDED`; the system never guesses what trade the user made.

## Governance

1. Data -> deterministic calculation -> decision log -> outcome measurement -> validation.
2. AI may interpret the results, but does not silently rewrite scores or historical records.
3. Missing/stale/private data stays missing; no synthetic portfolio facts are created.
4. Model/threshold changes require a new version and explicit human approval.
5. Order execution remains a human decision.

## Key outputs

- `data/decision_log/decisions.jsonl`
- `data/decision_system/decision_latest.json`
- `data/decision_system/factor_scores_latest.csv`
- `data/decision_system/outcomes_latest.csv`
- `data/decision_system/portfolio_risk_latest.json`
- `data/decision_system/alerts_latest.json`
- `data/decision_system/validation_report_latest.md`
- `data/decision_system/system_summary_latest.json`
