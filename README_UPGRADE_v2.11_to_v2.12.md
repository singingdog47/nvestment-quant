# Upgrade v2.11 → v2.12: Major-SQ Execution Overlay

## Purpose

Add major-SQ market-structure awareness without allowing a short-lived derivatives event to override the system's medium/long-term security selection.

## Design rule

SQ is **not** an alpha factor and is **not** a directional signal.

The overlay may affect only:

- order staging / split entries
- patience before execution
- preference for limit orders over unnecessary market orders
- how aggressively an entry price is pursued during major-SQ week

It must never directly change:

- security ranking
- fundamental score
- investment thesis
- portfolio strategic allocation

## New output

`data/regime/sq_execution_overlay_latest.json`

The same object is also embedded in:

`data/regime/market_regime_latest.json -> execution_overlay.sq`

and summarized in `data/regime/market_context_latest.md`.

## Automatic behavior

The engine automatically calculates the next quarterly major-SQ date (March, June, September, December; second Friday by default) and activates the overlay within the configured calendar window.

Calendar proximity alone is intentionally low confidence. It can create only a small execution caution adjustment.

## Optional structured enrichment

If `data/regime/sq_manual_input_latest.json` exists and is fresh, the overlay can consume explicitly sourced fields such as:

- Nikkei 225 option put/call open interest
- front/next futures open interest
- put wall / call wall / candidate magnet strike
- normalized arbitrage-balance z-score
- Nikkei 225 VI percentile

An example schema is provided at `config/sq_execution_input.example.json`.

Stale data is excluded from scoring. Missing values are never guessed.

## Interpretation safeguards

- Put/Call OI imbalance measures expiry sensitivity, not deterministic direction.
- Open interest alone is insufficient to infer dealer gamma sign.
- A strike with large OI is a reference level, not a guaranteed support/resistance level.
- `directional_bias` therefore remains `UNDETERMINED` unless a future validated model has stronger evidence.
- Maximum SQ execution adjustment is capped at 15 points and is separate from the stock-selection score.

## Data-source posture

JPX public pages remain the preferred primary references for derivatives open interest, daily futures/options reports, and index-arbitrage statistics. Production automation of clean strike-level OI extraction is deliberately marked as not yet implemented rather than silently substituting weaker data.

This release therefore works safely in calendar-only mode today and becomes more informative when verified structured derivatives data is supplied.

## Compatibility

- Existing market-regime score weights are unchanged.
- Existing screening/fundamental rankings are unchanged.
- Existing fallback branch is unchanged.
- Existing post-close workflow continues to run the market-regime stage in the same position.
