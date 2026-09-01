# Upgrade v2.8 -> v2.9: Immutable Private Portfolio History

## Purpose
Persist private portfolio, valuation, and monthly diagnostics to Google Drive so future reports can compare valuation and performance through time without publishing private holdings to GitHub.

## Production storage
`<GDRIVE_FOLDER_ID>/history/portfolio/investment_quant_private_history_ledger`

The ledger is a **user-owned native Google Sheet**. GitHub Actions uses the service account only to append rows to this existing file.

Why: Google service accounts can read a shared My Drive folder and create folders, but they do not have personal Drive storage quota for creating ordinary stored files. A raw-file-per-snapshot design therefore fails with `storageQuotaExceeded` on My Drive. The user-owned Sheet avoids that quota path while retaining automated write access inherited from the shared folder.

## Ledger schema
Each logical snapshot row records:
- snapshot date and kind (`portfolio`, `valuation`, `monthly`, `manifest`)
- revision / corrected flag
- canonical SHA-256
- system version
- source file and source-as-of timestamp
- status / analysis mode / evidence tier
- coverage metadata
- payload JSON
- creation timestamp

Large JSON payloads are losslessly encoded as gzip+base64 rather than truncated when needed to stay within a Sheets cell-size safety bound.

## Immutability and corrections
- Same date + kind + same canonical SHA-256: idempotent; no duplicate row is appended.
- Same date + kind + changed content: prior row is retained and a new corrected revision is appended.
- Existing historical rows are never overwritten by the automated pipeline.
- Volatile run timestamps are excluded from canonical hashes so a simple rerun does not create a false correction.

## Data-quality policy
- Missing data is not converted to zero.
- `reference_only` and `withheld` states are persisted as quality metadata rather than being promoted to actionable conclusions.
- Balance change is not treated as TWR.
- Secondary/mixed fundamental evidence remains non-actionable until primary-source confirmation.
- Market-value reconciliation differences are stored in the manifest payload.

## Privacy controls
- The history ledger is inside the configured private Google Drive hierarchy.
- `.private` files are never included in public GitHub artifacts or public commits.
- `PORTFOLIO_DRIVE_WRITEBACK=false` remains the production setting, preventing generated `portfolio_latest.csv` from polluting the input root.
- `PORTFOLIO_HISTORY_WRITEBACK=true` independently enables append-only history.
- Generated private output filenames are excluded from future input scans as an additional self-ingestion guard.
- The ledger file ID is not hard-coded into the public repository; the service account resolves it by name inside the private folder hierarchy.

## Backfill support
`PORTFOLIO_TARGET_DATE=YYYY-MM-DD` can select a dated brokerage snapshot for one-time backfill. Monthly diagnostics are cut off at the same date so a later portfolio does not leak into an earlier snapshot.

## Rationale
The August 2026 monthly review exposed two measurement gaps: portfolio valuation history was not persisted, and balance growth could not be separated cleanly from investment return without cash-flow data. v2.9 creates the longitudinal data layer needed for historical valuation comparison, attribution, and later out-of-sample validation while preserving degraded-data governance.
