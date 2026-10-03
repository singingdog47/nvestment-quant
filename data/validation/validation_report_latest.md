# Investment Quant Validation Report v2.1

Generated: 2026-10-03T00:11:26+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 190 | 0.08% | 48.95% | 190 | -0.06% | 51.58% |
| 1m | 76 | 0.17% | 43.42% | 76 | -0.05% | 46.05% |
| 3m | 0 | n/a | n/a | 0 | n/a | n/a |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 76 | 0.17% | 76 | -0.05% | 46.05% |
| CONSTRUCTIVE | 1w | 170 | 0.24% | 170 | 0.18% | 54.71% |
| NEUTRAL | 1w | 20 | -1.26% | 20 | -2.16% | 25.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 46 | 1.13% | 46 | 1.10% | 43.48% |
| REVIEW | 1w | 178 | -0.19% | 178 | -0.20% | 48.31% |
| WAIT_DATA_QUALITY | 1m | 30 | -1.31% | 30 | -1.81% | 50.00% |
| WAIT_DATA_QUALITY | 1w | 12 | 4.05% | 12 | 1.98% | 100.00% |

## Interpretation guardrails

- Japanese equities use 1306.T as the TOPIX-linked benchmark proxy; explicit US markets use SPY.
- Unknown markets are left without benchmark attribution rather than guessed.
- Do not change factor weights automatically from small samples.
- Separate model error from data-quality failure and regime misclassification.
- Promote a model change only after an explicit human review and version bump.
- Human brokerage actions remain private and are joined by decision_id outside the public repository.
