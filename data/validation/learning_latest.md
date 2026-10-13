# Investment Quant Validation Learning v2.1

Generated: 2026-10-13T15:56:01+00:00

This is a diagnostic learning layer. It does not automatically change factor weights or issue orders.

## Model-change gate
- Matured absolute-return observations: 512
- Benchmark-relative observations: 512
- Minimum benchmark-relative observations for review: 60
- Eligible for human model-change review: True

## Findings
- [WATCH] regime / CONSTRUCTIVE|1m (n=126): Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w (n=20): Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m (n=26): Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w (n=78): Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top10|1w (n=146): Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.
- [WATCH] rank_bucket / top3|1m (n=52): Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top3|1w (n=156): Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

## Known limits
- Benchmark assignment is deterministic: Japanese equities use 1306.T (TOPIX-linked ETF proxy); explicit US markets use SPY (S&P 500 ETF proxy). Unknown markets are left without a benchmark rather than inferred.
- Pre-v2.1 outcome rows may have blank benchmark fields and are excluded from benchmark-relative findings until new relative observations mature.
- Small samples can create false patterns; segment findings are suppressed below the minimum benchmark-relative sample threshold.
- The engine proposes review targets only and never changes weights or places orders automatically.
