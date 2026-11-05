# Portfolio Policy v2.0 — Live Integration Gate

Purpose: trigger repository-wide pull-request CI after the Portfolio Policy v2.0 unit/integration workflow passed.

Validation scope:
- current policy configuration parses successfully;
- policy/report modules import in package and script execution modes;
- repository-wide tests remain green with policy integration present;
- private portfolio inputs/results remain ephemeral and are not committed or uploaded as public artifacts;
- no trade-order execution is introduced by this gate.

After this PR gate passes, the next production step is to validate the manual private Portfolio Risk Engine path before relying on the post-close pipeline.
