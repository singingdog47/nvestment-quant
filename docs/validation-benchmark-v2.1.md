# Validation Benchmark-Relative Upgrade v2.1

This upgrade changes validation from absolute-return-only evaluation to benchmark-relative evaluation where a deterministic benchmark can be assigned.

## Benchmark policy

- Japanese equities: `1306.T` (TOPIX-linked ETF proxy)
- Explicit US markets: `SPY` (S&P 500 ETF proxy)
- Unknown markets: no benchmark is inferred

## Stored outcome fields

`data/validation/outcomes.csv` adds:

- `benchmark_symbol`
- `benchmark_return`
- `excess_return`

Existing pre-v2.1 rows are preserved during schema migration and keep blank benchmark fields.

## Learning policy

Validation Learning v2.1 uses benchmark-relative observations for findings and for the model-change review gate. Absolute returns remain visible as descriptive context, but a rising market alone should no longer be treated as evidence that the screening signal added value.

No factor weight is changed automatically. No order is placed automatically.
