# Investment Quant Validation Report v2.1

Generated: 2026-11-25T18:00:36+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 628 | -0.34% | 46.66% | 628 | -0.27% | 46.82% |
| 1m | 502 | -2.26% | 33.27% | 502 | -0.94% | 43.03% |
| 3m | 41 | -6.89% | 51.22% | 41 | -1.29% | 51.22% |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 442 | -2.00% | 442 | -0.87% | 42.99% |
| CONSTRUCTIVE | 1w | 434 | 0.14% | 434 | -0.12% | 47.93% |
| CONSTRUCTIVE | 3m | 41 | -6.89% | 41 | -1.29% | 51.22% |
| DEFENSIVE | 1w | 19 | -0.42% | 19 | 1.64% | 73.68% |
| NEUTRAL | 1m | 50 | -4.67% | 50 | -1.73% | 38.00% |
| NEUTRAL | 1w | 170 | -1.69% | 170 | -1.00% | 40.00% |
| RISK_ON | 1m | 10 | -1.42% | 10 | -0.27% | 70.00% |
| RISK_ON | 1w | 5 | 4.42% | 5 | 3.45% | 80.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 472 | -2.32% | 472 | -0.89% | 42.58% |
| REVIEW | 1w | 616 | -0.42% | 616 | -0.32% | 45.78% |
| REVIEW | 3m | 23 | -4.45% | 23 | 1.64% | 52.17% |
| WAIT_DATA_QUALITY | 1m | 30 | -1.31% | 30 | -1.81% | 50.00% |
| WAIT_DATA_QUALITY | 1w | 12 | 4.05% | 12 | 1.98% | 100.00% |
| WAIT_DATA_QUALITY | 3m | 18 | -10.02% | 18 | -5.03% | 50.00% |

## Interpretation guardrails

- Japanese equities use 1306.T as the TOPIX-linked benchmark proxy; explicit US markets use SPY.
- Unknown markets are left without benchmark attribution rather than guessed.
- Do not change factor weights automatically from small samples.
- Separate model error from data-quality failure and regime misclassification.
- Promote a model change only after an explicit human review and version bump.
- Human brokerage actions remain private and are joined by decision_id outside the public repository.
