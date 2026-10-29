# Challenger2 — isolated 5,000,000 JPY paper-cohort fork

Fork approved in the 2026-10-29 JST operating review. Original Challenger 1 continues independently at 1,000,000 JPY; Shadow Swing v1/v2 automatic execution remains paused for assessment.

## Capital and audit

- Source: `data/shadow_challenger/state.json` as of **2026-10-28**.
- Source state blob SHA: `b76114004ae11b0ac4ce91cd58737ffab56a5a9a`.
- Source NAV: **992,027.83 JPY**, including a pre-fork loss of **7,972.17 JPY** versus original funded capital of 1m.
- Incremental **virtual cash**: **4,007,972.17 JPY**, bringing fork-start NAV to **5,000,000 JPY**.
- All source positions, pending orders, close trades and execution evidence are copied *once* into `data/shadow_challenger2/state.json`.
- Existing source trade history is retained for audit but is **not** attributed to new Challenger2 fills.
- Cash injection is **not** trading P&L and never counted as a BUY/SELL.
- Seeded `initial_cash_jpy` is the **new cohort's performance reference**, not the cumulative all-time source-account deposit ledger. The source loss and top-up are separately preserved under `fork_metadata` and `capital_ledger`.

## Isolation and schedule

- Runner: `src/shadow_challenger2.py`, strategy engine: `src/shadow_challenger.py`.
- Config: `config/shadow_challenger2_v1.json`, independent from `config/shadow_challenger_v1.json`.
- Ledger: `data/shadow_challenger2/`, never `data/shadow_challenger/`.
- GitHub Actions: `.github/workflows/shadow-challenger2.yml`, scheduled weekdays 23:25 JST plus the main post-close workflow completion.
- GitHub Action records only its own ledger files, using the shared repository-write concurrency group.
- No live broker integration; verified market OHLC required for any virtual fills; missing OHLC never allows synthetic fills.
- The original 100万円 account remains unchanged for a side-by-side comparison, but the risk-sizing rule differs as specified below.

## Risk and comparisons

- Challenger2 maximum individual position: **7.5%** of the original 5m cohort capital (375,000 JPY), which is stricter than the 15% absolute ceiling proposed in the discussion.
- Retained 6% stop, 12% target, 15bp simulated execution slippage per side, five names, 80% max gross deployed.
- Typical planned loss at maximum position, counting the stop plus assumed two-sided slippage, is approximately **23,625 JPY** (0.4725% of 5m), below the nominal 25,000 JPY ordinary-trade loss budget. Price gaps and liquidity events can exceed this and are *not* guaranteed.
- Monthly NAV drawdown of -3% generates a `WARNING`; -5% generates `REVIEW_REQUIRED` after the November baseline exists. These are review markers, not executable broker stop orders.
- Comparisons must distinguish (a) same candidate/decision quality, (b) size and lot constraints, (c) different exposure limits; simple return differences are **not** a pure capital-size causal test.

## November objective

- Starting reference for November: the independently verified **2026-10-30 after-close NAV** for each cohort, not the inherited source NAV and not any funding cashflow.
- Objective: **+3%** on 2026-10-30 reference NAV through 2026-11-30, **not guaranteed**.
- If 2026-10-30 NAV is missing or positions cannot be newly verified, show unavailable baseline/returns instead of fabricating a return.
- Observe fills, realized P&L, drawdown, actual exposure and benchmark-relative performance; pre-fork executions do not count as new Challenger2 activity.

Validation: `PYTHONPATH=src python -m pytest -q tests/test_shadow_challenger.py tests/test_shadow_challenger2.py`.
