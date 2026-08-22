# Investment Quant v1.6 -> v1.6.1 data-quality patch

This patch addresses the issues observed in the first live v1.6 run.

## Fixes

1. JPX legacy `.xls` support
   - adds `xlrd>=2.0.1`
2. FRED timeout resilience
   - 3-attempt retry with increasing timeouts/backoff
3. JPX short-selling resilience
   - direct spreadsheet/csv links
   - HTML table fallback
   - one-level related-page discovery
4. v1.3 breadth compatibility
   - recognizes `return_1m`, `return_3m`, `return_6m`, `return_12m`
   - recognizes `avg_turnover_30d`
5. Fundamental-quality accounting
   - `screening_latest.csv` is treated as a secondary fallback snapshot
   - it no longer falsely upgrades dedicated fundamental coverage to 100%

## Apply

Copy this patch's contents into the repository root, preserving directories and
overwriting files with the same names.

Then commit/push and manually run:

Actions -> Investment Intelligence v1.6 -> Run workflow

## What to verify

- `data/regime/market_source_health_latest.csv`
  - JPX:investor_type should no longer fail because of xlrd
  - JPX:margin should no longer fail because of xlrd
  - FRED series should retry before becoming error
  - v1.3 breadth adapter should show participation columns
- `data/intelligence/data_quality_latest.json`
  - fundamental coverage may fall if no dedicated fundamentals file exists.
    This is intentional and safer than a false 100% coverage signal.
