# Decision-first / 軽量売買判断ゲート v1
2026-11-06: User requirement: intraday and overnight **decisions**, not end-of-day neutral classifications.
## Separation of concerns
1. Live observer: ChatGPT task "売買判断ゲート：寄り前・場中・夜間" checks sourced recent index futures, NASDAQ futures, VIX, and relevant broker orders only when material risk exists. On material changes it emits concrete human-executable recommendations.
2. Small deterministic policy: `config/decision_first_v1.json` + `scripts/decision_first.mjs` calculate HIGH/CRITICAL/UNVERIFIED and explicit action proposals from a time-stamped snapshot. Zero third-party packages, no downloads, no brokerage credentials.
3. Deep research: legacy quant pipeline remains *optional evidence*, not a permission gate for risk warnings. Expensive analysis is moved to weekly review and independently evaluated shadow systems.
4. No auto execution: no actual broker orders, no credentials, no sensitive portfolio files in public GitHub.
## Input contract
```json
{"now":"2026-11-06T00:05:00Z","market":{"nikkei_future_pct":{"value":-5.8,"as_of":"2026-11-05T22:00:00Z"}},"orders":[{"ticker":"EXAMPLE-ETF","side":"BUY","status":"OPEN","quantity":10,"limit_price":1234,"as_of":"2026-11-05T23:50:00Z"}],"positions":[{"ticker":"EXAMPLE-STOCK","shares":10,"exit_on_critical":true,"latest_price":1200,"quote_as_of":"2026-11-05T06:30:00Z"}]}
```
The example is illustrative only. Live private details must NOT be committed.
Run: `node scripts/decision_first.mjs /secure/path/snapshot.json`. Test: `node --test tests/decision_first.test.mjs`.
## Safety / explicit limitations
An index futures crash does NOT automatically mean sell every stock. Automatic suggestions to sell require an existing, *precommitted* policy such as exit_on_critical or a verified hard-stop and all are PROPOSAL_ONLY. Verify order books at execution. A stale open order becomes VERIFY_ORDER, never a fabricated cancellation. A stale market feed returns UNVERIFIED, not NEUTRAL. The scheduled ChatGPT task independently supplies sourced observations and is **not** guaranteed tick-by-tick monitoring. GitHub Actions success is not proof of live decision coverage.
## Acceptance tests
Capture event time, first warning time, impacted holdings, proposed order, execution status, and retrospective counterfactual. Targets: warning within one scheduled check, zero fabricated orders, no indefinite 'watch', critical false negatives measured separately. Stop/roll back if alert noise exceeds usefulness or data freshness becomes unreliable.
