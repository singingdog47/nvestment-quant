# Investment Quant Validation Report v2.1

Generated: 2026-10-13T15:06:43+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 380 | 0.84% | 56.58% | 380 | 0.18% | 50.53% |
| 1m | 132 | 0.69% | 43.18% | 132 | -0.16% | 41.67% |
| 3m | 0 | n/a | n/a | 0 | n/a | n/a |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 126 | 0.72% | 126 | -0.05% | 42.06% |
| CONSTRUCTIVE | 1w | 355 | 0.90% | 355 | 0.26% | 51.55% |
| NEUTRAL | 1m | 6 | 0.14% | 6 | -2.39% | 33.33% |
| NEUTRAL | 1w | 20 | -1.26% | 20 | -2.16% | 25.00% |
| RISK_ON | 1w | 5 | 4.42% | 5 | 3.45% | 80.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 102 | 1.28% | 102 | 0.33% | 39.22% |
| REVIEW | 1w | 368 | 0.73% | 368 | 0.12% | 48.91% |
| WAIT_DATA_QUALITY | 1m | 30 | -1.31% | 30 | -1.81% | 50.00% |
| WAIT_DATA_QUALITY | 1w | 12 | 4.05% | 12 | 1.98% | 100.00% |

## Interpretation guardrails

- Japanese equities use 1306.T as the TOPIX-linked benchmark proxy; explicit US markets use SPY.
- Unknown markets are left without benchmark attribution rather than guessed.
- Do not change factor weights automatically from small samples.
- Separate model error from data-quality failure and regime misclassification.
- Promote a model change only after an explicit human review and version bump.
- Human brokerage actions remain private and are joined by decision_id outside the public repository.
