# Investment Quant Validation Learning v2.0

Generated: 2026-08-23T14:13:27+00:00

This is a diagnostic learning layer. It does not automatically change factor weights or issue orders.

## Model-change gate
- Matured observations: 0
- Minimum for review: 60
- Eligible for human model-change review: False

## Findings
- No statistically gated review finding yet.

## Known limits
- Current outcome history evaluates absolute returns; benchmark-relative excess-return attribution is not yet stored in outcomes.csv.
- Small samples can create false patterns; segment findings are suppressed below the minimum sample threshold.
- The engine proposes review targets only and never changes weights or places orders automatically.
