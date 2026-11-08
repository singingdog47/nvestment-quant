# Private runtime acceptance

The production source path now accepts dated order PDFs as partial document
evidence. It never promotes a PDF page or a displayed subset into complete order
rows. The normal portfolio runner creates the four-source historical ledger
when the latest matching CSV, buying-power PDF, domestic-order PDF and fund
history PDF pass reconciliation. Source dating, content status and ledger
coverage propagate to the private decision state and holding report.

`python -m src.private_runtime_readiness` exercises Drive download, production
holdings/account parsers, four-source reconciliation, ledger write/readback,
shared state, holding decision matrix, private report upload/readback and the
decision-journal monitor. It does not fetch new broker data on the user's behalf.
The readiness report is private_readiness_latest.json in the existing private
Drive folder; pre-create this file as the quota-owning user where service-account
creation is unavailable. Public logs contain only runtime/writeback status and
exception class. No private files are uploaded as public Actions artifacts.

The Private Runtime Readiness workflow runs after deployment changes and at
07:35 JST on weekdays, before the existing 07:50 advice task. It uses the
existing Drive secrets. Runtime failure exits nonzero; unavailable credentials
cannot be reported as a successful run. Publication readback is byte-checked.

## Acceptance and limits

- Runtime PASSED means the deployed code consumed real files and produced its
  expected output. It does not mean every brokerage fact is complete/current.
- The November 6 four-document replay reconciles balances and persists four
  facts. Partial order coverage, unverified settlement and aged inputs remain
  explicit. Unknown order count remains null, not zero.
- Complete account orders and available settled cash cannot be inferred from a
  displayed domestic-order subset, a fund history page or buying power alone.
- Future-day account analysis needs that day's input when current quantities,
  order state or cash are material. Historical documents remain available for
  dated analysis; publication time does not refresh their source timestamps.
- If source selection or reconciliation fails, no new verified ledger facts are
  fabricated. The incomplete-data state is part of correct software behavior.

Local acceptance: original four-file replay through production parsers, ledger,
shared state and decision report; synthetic tests cover incomplete documents,
transaction-vs-footer timestamps, partial coherence, missing sources and the
existing decision-monitor boundary. The production workflow run must also pass
before claiming remote runtime acceptance.
