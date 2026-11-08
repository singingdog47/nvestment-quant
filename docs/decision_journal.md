# Private decision journal

A price alert previously had no durable link to the subsequent conclusion or a
revised plan. `src.decision_journal` adds an append-only private JSONL journal
around the existing checkpoint evaluator. It records decisions; it does not
choose the economically best recommendation or demonstrate strategy returns.

## Use

Keep the journal and input events outside the public repository. The CLI writes
new journals with mode 0600 and locks read/append operations on Unix systems.
The complete journal is validated before append. Invalid revisions do not change
existing entries. It is not a cryptographic audit log: a file owner can still
edit it outside the CLI. Back up the private journal through the private data
workflow. Nothing is uploaded by this command.

```sh
python -m src.decision_journal /private/decisions.jsonl append /private/event.json
python -m src.decision_journal /private/decisions.jsonl audit --as-of 2026-11-09T16:00:00+09:00
```

Every event has a unique `id`, `type`, `symbol`, and timezone-aware
`recorded_at`. Entries must be in recorded order. This is the time information
became available to the reviewer, not an earlier inferred signal date.

| Event | Required content |
| --- | --- |
| PLAN | recommendation, rationale, falsifier, evidence, basis (CLOSE/INTRADAY/TIME), comparator (AT_OR_BELOW/AT_OR_ABOVE), positive threshold (price plans only), review_by |
| Replacement PLAN | all PLAN fields, supersedes (active plan ID), change_reason |
| OBSERVATION | plan_id, observed_at, evidence, close for CLOSE or low/high for INTRADAY (according to comparator) |
| REVIEW | plan_id, recommendation, reason, evidence, review_by; resolves (outstanding trigger event ID) when triggered |

Recommendations are HOLD/TRIM/EXIT/BUY/WAIT. A condition change requires a new
PLAN; REVIEW cannot modify threshold, comparator, basis or falsifier. Prices
must be finite and positive. Observations cannot precede the plan or latest
review, run backward, or be known after recorded_at. For CLOSE, the producer
must supply a completed session close, not an intraday quote. For an intraday
plan, use only extrema since the plan became effective; a full-day low recorded
before the plan is not valid evidence. The module does not fetch prices or
validate an exchange calendar.

A synthetic PLAN example (not a personal investment recommendation):

```json
{
  "id": "sample-plan-1", "type": "PLAN", "symbol": "SAMPLE.T",
  "recorded_at": "2026-11-09T08:00:00+09:00",
  "recommendation": "HOLD", "rationale": "Thesis remains intact",
  "falsifier": "Close below 100 requires review",
  "evidence": "private research reference", "basis": "CLOSE",
  "comparator": "AT_OR_BELOW", "threshold": 100,
  "review_by": "2026-11-09T16:00:00+09:00"
}
```

## Audit semantics

- A trigger persists through later rebounds until explicitly reviewed or
  superseded with a reason. It never becomes an assumed fill.
- A HOLD conclusion needs evidence, a reason and a future review deadline.
  Reaching that deadline requires another review, even if price has recovered.
- TRIM/EXIT/BUY remain `ACTION_RECOMMENDED`, not executed. WAIT remains
  `WAITING_FOR_EVIDENCE`; its deadline is still enforced.
- Missing observations are `NO_OBSERVATION`, not WATCHING. The returned
  last_observed_at exposes age; the plan's review deadline controls expiry.
- Past-due and triggered flags coexist. review_by is the next review deadline,
  not an expiry that silently retires the thesis.
- Historical audit uses only entries recorded by as_of. Later reviews cannot
  retroactively resolve an earlier outstanding trigger. All journal entries
  are still structurally validated, including entries after as_of.

## Regression evidence and integration boundary

Tests reproduce a breached threshold followed by rebound, a reasonless lowered
threshold, a changed recommendation without a revision link, missed deadlines,
and a close rule whose intraday low crossed but close recovered. They also
exercise historical as-of views, invalid/future prices, failed appends, and the
real append/audit CLI. Fixtures are synthetic; they do not assert that historical
personal advice was a mechanically binding trading rule.

The existing Action First Risk Watch workflow now has an independent private
monitor job. It reads `decision_journal.jsonl` from the configured private Drive
folder and writes `decision_monitor_latest.json` and `.md` there. It never
modifies the source journal or commits/uploads private Actions artifacts. Public
stdout contains only status and writeback success/failure. Source absence,
ambiguity or corruption cannot reuse an old successful report. The workflow
requires existing GDRIVE_SERVICE_ACCOUNT_JSON and GDRIVE_FOLDER_ID secrets;
without them its private job reports failure while public risk checks continue.

TIME plans monitor a deadline without inventing a numeric price trigger. They
must omit threshold/comparator and accept REVIEW rather than price OBSERVATION
entries. The monitor flags deadlines within four hours and overdue plans.
TRACKING refers only to registered advice, not complete PF monitoring or market
safety. Missing price observations remain unknown. Producers must supply new
verified observations; this module does not fetch market prices.

The designated advice producer (the private monitoring task) must download the
latest journal, append validated events, re-read the remote source to detect a
changed hash before replacing it, and verify readback. GitHub only reads this
journal, avoiding a second automatic writer. Do not write from parallel task
runs. The Drive connector does not offer a compare-and-swap content update;
this is a single-writer protocol, not a transactional multi-writer guarantee.
New advice is not recorded merely by appearing in chat: saving and readback must
succeed. On failure report recording unavailable, retain the original journal,
and do not claim that the new advice is monitored. Historical imports use the
current recorded_at and preserve the original advice time in source metadata.

Monitor CLI, also usable with a local copy and explicit replay time:

```sh
python -m src.private_decision_monitor --writeback
python -m src.private_decision_monitor --journal /private/decisions.jsonl --as-of 2026-11-09T10:50:00+09:00
```

Return, tax, slippage and early-sale opportunity-cost evaluation remain separate
from process-consistency tests. Scheduled deployment and the first recorded
scheduled run are separate evidence; do not claim the latter from CI alone.
