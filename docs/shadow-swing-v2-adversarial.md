# AI Shadow Swing v2 — 5m critical-demand paper cohort

## Why this exists

The 2026-09-15 v1 purchase of 8622.T had a plausible long-term earnings thesis, but the BUY decision did not require independently verifiable incremental buying pressure. V1 has an unresolved hard-stop order from 2026-10-06, which must not be hidden, erased, or incorrectly counted as filled.

V2 is a new independent 5,000,000 JPY simulated cohort starting 2026-10-15. Existing 1,000,000 JPY data/shadow_swing records stay unchanged for historical comparison. Virtual capital is not transferred to a real account and is not the user's personal investment budget.

This is a rule-driven simulation based on quant outputs; not a claim that ChatGPT discretion independently reviewed every trade, and NOT proven alpha.

## Faster evidence generation without forced trading

- At most 2 next-open simulated BUY signals per session; up to 8 positions, no more than 2 from a single theme.
- Single-name weight <=12.5% of initial capital; aggregate invested <=80%; no leverage or shorts.
- Missing short/credit observations explicitly recorded as unknown and reduce position weight by 50%.
- Hard stop -5%, take profit +10%, maximum 10 trading sessions with 15bps slippage each side.
- Review after >=30 fully CLOSED trades; proposed end is 2027-01-15.
- If no candidate qualifies, execute no buys. Never lower standards to meet a trade quota.

## Required adversarial pre-trade questions

1. Demand: what current price/volume evidence supports buying NOW, distinct from 1/3-month momentum?
2. Skeptic: could this be exhausted momentum, credit overhang, heavy down-volume, stale observations, source mismatch or an unusually large daily gap?
3. Alternative: why this security versus holding cash and TOPIX ETF 1306.T?
4. Missing evidence: are credit/short figures missing rather than actually benign? Record unknowns and size conservatively.
5. Falsification: what observable price/time event terminates the hypothesis, and what happens if the benchmark beats this trade?

A high screening score never overrides a failed demand veto. Thresholds are provisional test hypotheses, not statistical edge estimates.

## Temporal and execution integrity

- Same-day post-close data may create a signal; actual next-session OHLC must execute it, never a scanner last-price.
- Point-in-time history includes only observations dated before the signal with valid same-day timestamps.
- Proposal at close, buy next opening price (+15bps slippage), reject +3% open gaps.
- An intraday stop uses the stop price unless the market opens lower; ambiguous hit-order assumes stop before take-profit.
- Time exits are scheduled at close and executed only at a later opening (no same-bar open).
- Missing OHLC means no fabricated fill; missing market-data blockers are surfaced.
- Missing benchmark, regime or same-date scanner observations halt new entries.
- Every daily state has date idempotency, immutable original budget and separate output directory; no resetting performance.
- Taxes, commissions, limit-locks and partial fills are not fully simulated and may degrade realized performance.

## Output, success metrics, limits

- data/shadow_swing_v2/latest_report.md, latest.json, state.json
- data/shadow_swing_v2/adversarial_review_latest.json (positive and negative gate decisions)
- data/shadow_swing_v2/equity_curve.csv and trades.csv with benchmark-matched returns where available

At >=30 closed trades, evaluate win/loss ratios, realized expectancy, turnover, risk-adjusted return, slippage, benchmark excess return and rejection efficiency. Comparing a 5m book's raw P&L with a 1m book's raw P&L is invalid: compare return % and exposures.

Fail-safe: any fabricated fill, forward-looking data, unexplained order, state reset or unverified price must be corrected before reporting skill.

## Known independent issue: v1

This upgrade DOES NOT retroactively fill v1's 8622.T hard-stop from 2026-10-06. Existing positions, P&L and pending orders remain intact. Investigate missing Yahoo market OHLC in v1 separately; do not create an invented historical fill. V2 exposes feed failures rather than hiding them.

Schedule: runs once after successful post-close pipeline or a late-JST fallback through a dedicated GitHub Actions workflow. Real securities orders remain forbidden.
