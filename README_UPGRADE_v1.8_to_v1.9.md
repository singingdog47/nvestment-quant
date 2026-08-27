# Investment Quant v1.9 — FX and Investor Resilience Corrections

This release separates direct currency translation, local-asset returns, and
investor financial capacity. It fixes the prior error of assigning USD beta 1
to every non-domestic investment fund.

## New private inputs

Copy the examples into `.private/` (which remains untracked):

- `config/portfolio_risk_profile.example.json` → `.private/portfolio_risk_profile.json`
- `config/portfolio_risk_overlay.example.csv` → `.private/portfolio_risk_overlay.csv`

For GitHub Actions, store the same contents in encrypted repository secrets and
map them to `PORTFOLIO_RISK_PROFILE_JSON` and `PORTFOLIO_RISK_OVERLAY_CSV`.
Environment secrets take precedence over local private files. Never commit the
populated files or print these environment values in Actions logs.

The overlay is the reviewed holding-level source of truth. Relevant fields are:

- matching key preference: `holding_id`, then `name` + `account`, then `ticker`,
  then `code`. Keys must be non-empty and unique.

- `fx_beta_usdjpy`: 1 for direct unhedged USD translation, 0 for JPY/fully hedged,
  blank for unknown or a currency basket until validated.
- `scenario_return_boj_hike`
- `scenario_return_us_recession`
- `scenario_return_debasement`
- matching `scenario_return_basis_<scenario>` values: `local_currency` or
  `jpy_nav`

`local_currency` returns receive a separate direct FX translation. `jpy_nav`
returns already include FX and therefore receive no additional translation.
Missing or ambiguous return bases remain uncovered, preventing double counting.
If coverage is below the configured gate (90% by default), the engine reports
only a partial covered impact and withholds the total impact.
Even with sufficient coverage, a total estimate remains withheld until the
scenario is marked `validated_oos` after the documented holdout review.

## Conservative import rules

- Domestic securities and domestic-index funds: JPY, beta 0.
- Explicitly currency-hedged funds: HEDGED, beta 0.
- Emerging-market / China / India / Taiwan funds: EM_BASKET, beta missing.
- Direct US securities and clearly identified US-index funds: USD, beta 1.
- Everything else: UNKNOWN and manual review required.

Fund look-through data should be preferred over name rules. For basket funds,
estimate USDJPY beta only from a sufficiently long history and validate it out
of sample; never replace missing with 1.

## Required controls

1. Reconcile imported market value to the brokerage total before analysis.
2. Report direct USD-equivalent value and excluded basket value together.
3. Size every hedge benefit from actual position value (for example, duration
   gains on a small Treasury ETF position), not from a qualitative label.
4. Keep market-price resilience separate from investor financial capacity. The
   latter reports ratios using unrealized gain, free cash, defensive cash, and
   the chosen shock loss; it does not assign a numeric score without a validated
   rubric.
5. Treat US Treasury buybacks as debt-management/liquidity operations, not QE or
   monetization.
6. Require profile, portfolio-source, and FX timestamps for trade-actionable
   output. Stale, undated, proxied, or unreconciled-but-numeric inputs continue
   as explicitly labelled reference calculations; only the affected component
   is withheld when its required numeric inputs are unusable.
   For Rakuten exports, the timestamp embedded in the filename takes precedence
   over Drive's modification time so re-uploading an old CSV cannot make it
   appear fresh.

## Degraded-data operating modes

- `current`: inputs are fresh, reconciled, and eligible for decision support.
- `reference_only`: calculations continue from the last usable snapshot, but
  trade actionability is blocked and scenario totals are withheld.
- `withheld`: only the component missing essential numeric inputs is omitted;
  historical portfolio metrics and all unaffected sections continue.

When no private profile Secret is configured, the engine builds a conservative
reference profile from the imported portfolio market value and the latest
public USD/JPY observation in `market_dashboard_latest.csv`. The invested value
is clearly labelled as a total-assets proxy, so it can never masquerade as a
fully reconciled current balance sheet.

## Alternative validation method

For each dated scenario, store the predicted total impact, its direct-FX and
local-price components, assumption coverage, and subsequent realized portfolio
change. Evaluate at fixed 1-day, 1-week, and 1-month horizons against a frozen
model version. Review MAE, bias, interval coverage, and error by cause.

Coefficient changes must follow: record → evaluate → proposal → out-of-sample
validation → human approval. Do not automatically update FX betas or scenario
returns from the same observations used to evaluate them.

Suggested minimum review gates:

- at least 20 matured observations per scenario before proposing a coefficient change;
- a separate holdout period before acceptance;
- improvement in both MAE and directional calibration;
- no deterioration in tail-loss error or missing-data coverage.
