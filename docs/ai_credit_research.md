# AI信用スプレッド研究 v1 — OBSERVE ONLY

## 判定（2026-10-08）

**研究対象として採用。売買・リスク配分への実装は不採用（証拠不足）。**

- BIS *Quarterly Review*, Sep 2026, Graph 6.C: hyperscalers / semiconductor firms' CDS spreads rose while other S&P 500 companies were comparatively stable. This provides an economic rationale for measuring an **AI-relative credit component**, distinct from generic risk-off.
  https://www.bis.org/publications/qr-202609/yields-climb-yet-risk-appetite-holds-firm
- This **does not** establish predictive superiority over VIX, US Treasury yields, broad investment-grade/high-yield OAS, or semiconductor momentum. Nor does it justify a threshold like +20bp as an automatically bearish signal.
- Company-level CDS history generally requires a licensed, quality-controlled vendor feed. FRED corporate OAS (e.g. BAMLC0A0CM) is a **broad credit proxy**, **not** company CDS and not evidence of AI-relative widening. No substitution or imputation is permitted.
- BIS Graph 6.C is an aggregate chart, **not a machine-readable daily panel**. Do not digitize the chart and pretend the result is issuer-level daily CDS.

## Research data contract

Optional input: `data/ai_credit/source_cds.csv` (not committed), UTF-8:
```csv
date,entity,group,cds_5y_bp,source,asof_utc
```
- `date`: ISO observation date in a **uniform** market convention.
- `group`: `ai` or `control`. Keep a **pre-registered fixed issuer universe**; no survivors-only selection or composition drift.
- `cds_5y_bp`: quoted 5-year CDS spread in **basis points**, not option-adjusted spread or bond yield. Match restructuring clause, seniority, currency, contract tenor, bid/ask convention, vendor/close time across issuers.
- `source` / `asof_utc`: nonempty vendor identifier and timezone-aware source observation timestamp. Note: mandatory provenance fields **do not independently validate license or data authenticity**.
- At least three distinct companies per group on the same date; separate analysis should match credit ratings and sectors, because cross-sectional differences may be composition-driven.
- For research, prefer as-of historical snapshots and preserve their original publication timestamps; do not backfill revised data into historical signals without labeling revisions.

Example generation command (only after sourcing/licensing the issuer-level panel):
```sh
python -m scripts.ai_credit_monitor \
  --cds-csv data/ai_credit/source_cds.csv \
  --price-csv data/ai_credit/nasdaq100_daily.csv \
  --output data/ai_credit/assessment.json
```
Without input it prints unavailable, and returns `actionable=false`, `trade_signal=false`. No GitHub scheduled scraping, no position sizes, private PF or auto-orders.

## Validation required before operational promotion

1. **Data-quality gate**: at least 6 months, preferably 2+ years, of point-in-time observations; historical survivorship controls; reliable >90% issuer-day coverage; monitoring for vendor staleness/outliers, missingness, rating changes and CDS curve convention changes. The current minimum three per side is only a computational **floor**, not the evidence threshold.
2. **Incremental information**: compare lagged AI-minus-control CDS changes against VIX, US Treasury 10-year yield changes, US IG & HY OAS, NASDAQ/SOX 5/20-day momentum and realized volatility. Use a matched control universe; report partial correlation / conditional importance / multicollinearity.
3. **Out-of-sample**: walk-forward time split, purging/embargo overlapping labels, compare the same 1/5/20-trading-session NASDAQ/SOX returns, drawdowns and forward volatility. Separate 2026 AI funding events from general rate-shock events. No look-ahead: CDS publication cutoff must precede evaluation entry (earliest next-session close in the current exploratory code).
4. **Calibration and decision value**: baseline models (no-CDS; broad-credit-only; VIX+rates; combined). Show confidence intervals with block bootstraps, false-positive rate and net benefit of realistic transaction costs/tax/opportunity costs. Avoid arbitrary optimised thresholds.
5. **Promotion gate**: documented incremental out-of-sample lift on at least two regimes, stable data rights/access and ownership, no material drawdown/turnover deterioration, human review. Until then, `research_only` and `actionable=false` remain mandatory.

## Limitations in initial code

- Computes **median AI issuer CDS minus median control issuer CDS** for dates with coverage and its 20-observation change. It is **descriptive**, not a calibrated danger score, market regime, return forecast, or tradable signal.
- Does not yet normalize for ratings, currency, sectors, issuer size, liquidity or vendor revision; these are necessary before causal interpretation.
- Optional 5-session forward outcome ledger is **unvalidated** and not a backtest. The signal at date T is tested over close(T+1) to close(T+6); if T is a delayed publication, later entry is needed.
- No sample external quotes, generated placeholder spreads or manufactured CDS dataset is embedded.
- Use private / licensed source access and do not publish restricted rows as GitHub artifacts.

## Decision for now

Maintain qualitative monitoring of AI-funding credit stress and public BIS/issuer disclosures. The code lets us collect an auditable panel *if* rights-cleared CDS data becomes available. **Do not change any live quant/risk decisions on the basis of this module.**
