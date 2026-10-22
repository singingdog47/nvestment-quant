# Decision agility protocol — portfolio analysis and paper experiments

## Objective
Improve **risk-adjusted long-term wealth after tax and attention**, not turnover.
Every material discussion must end with a decision: `ACT_RECOMMENDED`,
`CONDITIONAL_ORDER_REVIEW`, `HOLD_WITH_FALSIFIER`, or `NO_EDGE`.
A score is research evidence, not an order. Live brokerage operations are NEVER
initiated by these scripts.

## Real portfolio (human decision)
- Distinguish **previously discussed**, **broker order submitted**, and
  **filled**. Do not infer orders from conversation.
- Store actual holding quantities and intended orders **only in private
  context** (conversation / private Drive), never in this public repository.
- When a previous threshold was crossed, label it **missed review** if no
  action is documented. Do not reuse an already-crossed price as an unqualified
  future target. Update the thesis, price, and timing.
- For each actionable name, include baseline HOLD, strongest BUY/ADD or TRIM
  argument, what would falsify it, action-by date, tax/account constraints,
  and the next practical limit/size if a decision is recommended.
- Do not add confirmations for trivial facts already established by
  conversation and matching cash-flow amounts. Ask only for material unknowns.
- Distinguish review of an opportunity from real execution. The user confirms
  any order in their actual brokerage account.
- Opportunistic **conditional reviews** may proceed with secondary/fallback
  information, clearly tagged. Missing **execution** price is never waived.

## Challenger comparison
Independent 2026-10-22 → 2027-01-22 paper-only ¥1m cohort.
Five holdings max, 20% each, 80% max gross. Missing optional FRED
credit context reduces position size, but does not stop research.
Only a same-session post-close screen produces a signal. Verified daily OHLC
is mandatory for simulated fills and exits; no retrospective fills.
Compare after 20/40/60 sessions against v1/v2, TOPIX (when observable),
and cash, tracking risk, benchmark excess return, drawdown,
trades, and **missed opportunities**.
Do not promote paper parameters to live capital without forward evidence.

## Private decision checkpoint adapter
`src/decision_checkpoint.py` exposes `review_all(rules, observations, date)`.
Inject account-specific watch rules and price bars from private context.
It never saves personal intentions in the public repository.
Statuses: WATCHING, TRIGGERED_REQUIRES_DECISION,
TRIGGERED_AWAITING_DECISION, EXPIRED_REQUIRES_REVIEW,
EXECUTED_RECORDED.

**NOTE**: the previously discussed 3,500 yen trigger was crossed and
does not represent an unfilled brokerage limit order. This is an
already-missed review, requiring a fresh present-day decision; it is
deliberately NOT installed as a new automatic trade trigger.

## Simplification priority
Keep existing v1/v2 intact as controls. Correct data freshness/price
availability, then measure evidence. Avoid adding extra gates or
rebalancing entire live portfolios based on noisy daily rank changes.
