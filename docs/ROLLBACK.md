# Rollback / Stable Report Policy

- Current known-good fallback branch: `stable-report-v2.5`.
- New development is merged only after Pull Request CI succeeds.
- If the main post-close job fails, the workflow automatically generates a public-safe report from the pinned stable branch.
- A manual `Stable Report Fallback v2.5` workflow remains available even while main is being repaired.
- Stable fallback never reads Google Drive portfolio data and never uploads private portfolio outputs.
- Do not move a stable branch until the replacement version has completed CI and at least one successful production/manual pipeline run.
- Restoring `main` itself is an explicit, potentially destructive action and should require human approval; generating a stable fallback report does not.
