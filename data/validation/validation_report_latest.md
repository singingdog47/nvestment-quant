# Investment Quant Validation Report v2.1

Generated: 2026-10-16T12:29:01+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 380 | 0.84% | 56.58% | 380 | 0.18% | 50.53% |
| 1m | 140 | 0.55% | 42.14% | 140 | -0.29% | 40.71% |
| 3m | 0 | n/a | n/a | 0 | n/a | n/a |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 130 | 0.59% | 130 | -0.15% | 41.54% |
| CONSTRUCTIVE | 1w | 355 | 0.90% | 355 | 0.26% | 51.55% |
| NEUTRAL | 1m | 10 | -0.10% | 10 | -2.03% | 30.00% |
| NEUTRAL | 1w | 20 | -1.26% | 20 | -2.16% | 25.00% |
| RISK_ON | 1w | 5 | 4.42% | 5 | 3.45% | 80.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 110 | 1.05% | 110 | 0.13% | 38.18% |
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
