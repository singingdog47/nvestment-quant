# Validation Learning v2.0

Purpose: close the loop from recorded decision -> matured outcome -> segmented evaluation -> human-reviewed model improvement.

The engine reads only matured records from `data/validation/outcomes.csv` and produces:

- `data/validation/learning_latest.json`
- `data/validation/learning_latest.md`

It evaluates outcomes by horizon, recommended action, market regime, rank bucket, and model version. Findings are suppressed for small segments. A model-change review gate opens only after a minimum number of matured observations.

Governance rules:

1. No factor weight is changed automatically.
2. No order is placed automatically.
3. Findings identify review targets, not causal proof.
4. Missing outcomes are not imputed.
5. A model change requires explicit human review, robustness checks, and a version bump.
6. Benchmark-relative attribution is a planned extension; current `outcomes.csv` stores absolute returns only.
