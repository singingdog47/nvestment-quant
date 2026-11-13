# Investment Quant Validation Report v2.1

Generated: 2026-11-13T15:27:56+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 609 | -0.34% | 47.13% | 609 | -0.33% | 45.98% |
| 1m | 450 | -1.92% | 35.11% | 450 | -1.00% | 42.89% |
| 3m | 0 | n/a | n/a | 0 | n/a | n/a |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 420 | -1.90% | 420 | -0.88% | 43.33% |
| CONSTRUCTIVE | 1w | 434 | 0.14% | 434 | -0.12% | 47.93% |
| NEUTRAL | 1m | 20 | -2.75% | 20 | -3.97% | 20.00% |
| NEUTRAL | 1w | 170 | -1.69% | 170 | -1.00% | 40.00% |
| RISK_ON | 1m | 10 | -1.42% | 10 | -0.27% | 70.00% |
| RISK_ON | 1w | 5 | 4.42% | 5 | 3.45% | 80.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 420 | -1.97% | 420 | -0.94% | 42.38% |
| REVIEW | 1w | 597 | -0.42% | 597 | -0.38% | 44.89% |
| WAIT_DATA_QUALITY | 1m | 30 | -1.31% | 30 | -1.81% | 50.00% |
| WAIT_DATA_QUALITY | 1w | 12 | 4.05% | 12 | 1.98% | 100.00% |

## Interpretation guardrails

- Japanese equities use 1306.T as the TOPIX-linked benchmark proxy; explicit US markets use SPY.
- Unknown markets are left without benchmark attribution rather than guessed.
- Do not change factor weights automatically from small samples.
- Separate model error from data-quality failure and regime misclassification.
- Promote a model change only after an explicit human review and version bump.
- Human brokerage actions remain private and are joined by decision_id outside the public repository.
