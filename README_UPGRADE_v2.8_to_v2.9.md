# Upgrade v2.8 -> v2.9: Immutable Private Portfolio History

## Purpose
Persist private portfolio, valuation, and monthly diagnostics to Google Drive so that future reports can compare valuation and performance through time without publishing private holdings to GitHub.

## Storage layout
`<GDRIVE_FOLDER_ID>/history/portfolio/YYYY/MM/`

Per snapshot date:
- `portfolio_snapshot_YYYYMMDD.csv`
- `valuation_snapshot_YYYYMMDD.json`
- `monthly_performance_YYYYMMDD.json`
- `snapshot_manifest_YYYYMMDD.json`

## Immutability and corrections
- Same filename + same SHA-256: idempotent; no duplicate is created.
- Same filename + changed content: prior history is retained and a `_vN_corrected` file is created.
- Historical files are never updated in place.

## Snapshot manifest
Records:
- source filename and source-as-of timestamp
- source-as-of method
- system/engine versions
- valuation status / analysis mode / evidence tier
- metric coverage
- monthly status / TWR status
- market-value reconciliation difference
- SHA-256 of persisted source artifacts

## Data-quality policy
- Missing data is not converted to zero.
- `reference_only` and `withheld` states are persisted as quality metadata rather than being promoted to actionable conclusions.
- Balance change is not treated as TWR.
- Secondary/mixed fundamental evidence remains non-actionable until primary-source confirmation.

## Privacy controls
- Historical snapshots are written only to the configured private Google Drive folder.
- `.private` files are not included in public GitHub artifacts or public commits.
- `PORTFOLIO_DRIVE_WRITEBACK=false` remains the default in the post-close workflow to prevent generated `portfolio_latest.csv` from polluting the input root.
- `PORTFOLIO_HISTORY_WRITEBACK=true` independently enables immutable history under subfolders.
- Generated private output filenames are excluded from future input scans as an additional self-ingestion guard.

## Rationale
The August 2026 monthly review exposed two measurement gaps: portfolio valuation history was not persisted, and balance growth could not be separated cleanly from investment return without cash-flow data. v2.9 creates the longitudinal data layer needed for historical valuation comparison, attribution, and later out-of-sample validation while preserving the existing degraded-data governance model.
