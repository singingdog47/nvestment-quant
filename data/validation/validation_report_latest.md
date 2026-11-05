# Investment Quant Validation Report v2.1

Generated: 2026-11-05T15:31:47+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 549 | -0.41% | 44.99% | 549 | -0.44% | 44.08% |
| 1m | 375 | -0.96% | 39.47% | 375 | -0.49% | 46.13% |
| 3m | 0 | n/a | n/a | 0 | n/a | n/a |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 345 | -0.84% | 345 | -0.30% | 46.96% |
| CONSTRUCTIVE | 1w | 434 | 0.14% | 434 | -0.12% | 47.93% |
| NEUTRAL | 1m | 20 | -2.75% | 20 | -3.97% | 20.00% |
| NEUTRAL | 1w | 110 | -2.76% | 110 | -1.89% | 27.27% |
| RISK_ON | 1m | 10 | -1.42% | 10 | -0.27% | 70.00% |
| RISK_ON | 1w | 5 | 4.42% | 5 | 3.45% | 80.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 345 | -0.93% | 345 | -0.38% | 45.80% |
| REVIEW | 1w | 537 | -0.50% | 537 | -0.49% | 42.83% |
| WAIT_DATA_QUALITY | 1m | 30 | -1.31% | 30 | -1.81% | 50.00% |
| WAIT_DATA_QUALITY | 1w | 12 | 4.05% | 12 | 1.98% | 100.00% |

## Interpretation guardrails

- Japanese equities use 1306.T as the TOPIX-linked benchmark proxy; explicit US markets use SPY.
- Unknown markets are left without benchmark attribution rather than guessed.
- Do not change factor weights automatically from small samples.
- Separate model error from data-quality failure and regime misclassification.
- Promote a model change only after an explicit human review and version bump.
- Human brokerage actions remain private and are joined by decision_id outside the public repository.
