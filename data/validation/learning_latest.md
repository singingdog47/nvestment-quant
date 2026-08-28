# Investment Quant Validation Learning v2.1

Generated: 2026-08-28T21:38:44+00:00

This is a diagnostic learning layer. It does not automatically change factor weights or issue orders.

## Model-change gate
- Matured absolute-return observations: 0
- Benchmark-relative observations: 0
- Minimum benchmark-relative observations for review: 60
- Eligible for human model-change review: False

## Findings
- No statistically gated benchmark-relative review finding yet.

## Known limits
- Benchmark assignment is deterministic: Japanese equities use 1306.T (TOPIX-linked ETF proxy); explicit US markets use SPY (S&P 500 ETF proxy). Unknown markets are left without a benchmark rather than inferred.
- Pre-v2.1 outcome rows may have blank benchmark fields and are excluded from benchmark-relative findings until new relative observations mature.
- Small samples can create false patterns; segment findings are suppressed below the minimum benchmark-relative sample threshold.
- The engine proposes review targets only and never changes weights or places orders automatically.
