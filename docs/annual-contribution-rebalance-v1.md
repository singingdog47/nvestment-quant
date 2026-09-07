# Annual Contribution Rebalance v1.0

## Purpose

Keep the monthly 150,000 JPY contribution continuous while preventing portfolio risk drift from silently turning the long-term core into an unintended concentrated bet.

This module is a **cash-flow rebalance recommender**, not a trading system. It never sends orders, sells holdings, or changes Rakuten Securities settings.

## Baseline plan

- Diversified core: 100,000 JPY/month
  - Reference instrument: eMAXIS Slim 全世界株式（オール・カントリー）
- Growth tilt: 50,000 JPY/month
  - Reference instrument: eMAXIS NASDAQ100インデックス
- Total: 150,000 JPY/month

Standard full-year NISA routing:

- NISA tsumitate: diversified core 100,000 JPY/month
- NISA growth: remaining 50,000 JPY/month
- Annual NISA growth used by automatic contributions: 600,000 JPY
- Annual NISA growth capacity left for satellite opportunities: 1,800,000 JPY

Current-year remaining NISA capacity must always be checked before manually applying the plan.

## Review rule

- Scheduled review: December 1-10, once per year.
- Manual workflow dispatch can force a review outside that window for calibration/testing.
- No macro forecast, valuation forecast, interest-rate call, FX call, or short-term momentum view may change the monthly contribution plan.
- Existing assets are not sold just to rebalance.

Rebalancing priority:

1. New monthly contributions.
2. Dividends and additional cash.
3. Destination of new satellite purchases.
4. Existing-asset sale only if drift cannot be corrected and the tax-adjusted replacement benefit is positive.

## Growth-tilt steps

The only allowed automatic recommendation levels are:

- 50,000 JPY/month: baseline.
- 25,000 JPY/month: mild risk-budget breach.
- 0 JPY/month: severe risk-budget breach.

The remaining monthly contribution is redirected to the diversified core. Amounts above the 100,000 JPY/month NISA-tsumitate ceiling must be routed through the NISA growth allowance (or taxable account if current-year NISA capacity is unavailable).

## Risk estimation

The engine estimates historical covariance risk contribution and separately reports the current growth-factor score available from the screening system.

For mutual funds without directly usable price symbols, documented listed-market proxies are used only for risk estimation. Proxy use is disclosed in the private report and is never presented as exact look-through holdings data.

The strategic `growth_tilt` bucket currently means explicit NASDAQ100/FANG+ index exposure. Domestic-stock growth-factor exposure remains diagnostic until a separately validated mapping/model is calibrated.

## Calibration gate

Version 1.0 intentionally ships with `threshold_status = calibration_required`.

This means the first live private run:

- calculates current growth-tilt weight and historical risk contribution;
- measures market-data coverage;
- reports the portfolio growth-factor score and coverage;
- **does not change the baseline 100,000 / 50,000 contribution plan**.

Only after the live metrics are reviewed should mild/severe thresholds be activated in `config/contribution_rebalance_v1.json`. This prevents arbitrary 15%/20% or ±5-point thresholds from becoming policy without evidence.

## Privacy

- Portfolio inputs come from the existing private Google Drive integration.
- Private holdings are never committed to the public repository.
- The annual workflow writes only `contribution_rebalance_latest.json` and `contribution_rebalance_latest.md` back to the user's private Drive.
- No private outputs are uploaded as public GitHub Actions artifacts.

## Workflow

`.github/workflows/annual-contribution-rebalance-v1.yml`

- Manual: Actions -> Annual Contribution Rebalance v1.0 -> Run workflow.
- Scheduled: December 1 at approximately 09:17 JST.

The manual run defaults to `force_review=true` so calibration can be performed outside December.
