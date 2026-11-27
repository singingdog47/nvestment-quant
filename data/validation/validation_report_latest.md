# Investment Quant Validation Report v2.1

Generated: 2026-11-27T17:30:40+00:00

This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.
Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.

## Screening outcome by horizon

| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |
|---|---:|---:|---:|---:|---:|---:|
| 1w | 643 | -0.30% | 47.43% | 643 | -0.27% | 46.66% |
| 1m | 552 | -2.21% | 32.43% | 552 | -0.48% | 45.29% |
| 3m | 53 | -4.56% | 50.94% | 53 | 0.92% | 50.94% |

## Outcome by market regime

| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| CONSTRUCTIVE | 1m | 442 | -2.00% | 442 | -0.87% | 42.99% |
| CONSTRUCTIVE | 1w | 434 | 0.14% | 434 | -0.12% | 47.93% |
| CONSTRUCTIVE | 3m | 53 | -4.56% | 53 | 0.92% | 50.94% |
| DEFENSIVE | 1w | 34 | 0.35% | 34 | 0.78% | 58.82% |
| NEUTRAL | 1m | 100 | -3.21% | 100 | 1.20% | 53.00% |
| NEUTRAL | 1w | 170 | -1.69% | 170 | -1.00% | 40.00% |
| RISK_ON | 1m | 10 | -1.42% | 10 | -0.27% | 70.00% |
| RISK_ON | 1w | 5 | 4.42% | 5 | 3.45% | 80.00% |

## Outcome by recommended action

| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |
|---|---|---:|---:|---:|---:|---:|
| REVIEW | 1m | 522 | -2.26% | 522 | -0.41% | 45.02% |
| REVIEW | 1w | 631 | -0.38% | 631 | -0.32% | 45.64% |
| REVIEW | 3m | 35 | -1.75% | 35 | 3.97% | 51.43% |
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
