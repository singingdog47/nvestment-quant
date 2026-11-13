# Private order ledger and sell/hold review

Use this separately from the decision journal and holdings CSV. The decision
journal records plans, observations and reviews. The trade ledger records
broker-observed order states, not intentions or inferred fills. The reviewer
reads the trade ledger, including linked rationale when available. It never
places or modifies a brokerage order or changes holdings or buying power.

## Private input and one writer

In the existing restricted Drive folder keep exactly one
`private_trade_ledger.jsonl` and one `private_trade_review_latest.json`.
The account holder or the designated private task is the only writer of the
ledger, and they should not write concurrently. GitHub only reads the ledger.
Record a broker screenshot as a manually checked JSON array, or import an
order-export CSV with explicit Japanese headers. Do not use a chat suggestion,
a position disappearing from a holdings CSV, or an expired date to invent a
fill or to certify account-wide order coverage.

Each snapshot has schema_version=1, asset=JP_CASH_EQUITY, broker, account_alias,
account_type, order_id, order_at, symbol (exchange suffix .T), side (BUY/SELL),
status, quantity, filled_quantity, observed_at, recorded_at, and evidence_ref.
Use decimal strings for yen fields, including fill_price_jpy and
fill_value_jpy when any shares filled. Use actual execution_date when the
source proves it, otherwise leave it null. Never substitute the order date
for an unverified execution date. good_until and limit_price_jpy are optional.
An optional decision object carries reason, evidence_ref, timing_basis and
decided_at if known. Link to the actual pre-order advice when known, and make
any retrospective reconstruction explicit. Never backdate recorded_at.
Optional execution_day_close preserves an independently sourced close for D+0.

```sh
python -m src.private_trade_review --ledger .private/trade_ledger.jsonl --append .private/verified_rows.json
python -m src.private_trade_review --ledger .private/trade_ledger.jsonl --rakuten-orders-csv .private/orders.csv --observed-at '2026-01-16T16:00:00+09:00' --evidence-ref 'private:broker-export'
python -m src.private_trade_review --ledger .private/trade_ledger.jsonl --out .private/review.json
```

Download and retain the original bytes before appending. The CLI validates
the whole ledger and rejects conflicting or regressing evidence; duplicate
observations are no-ops. Immediately before replacing the existing Drive
object, re-read it and compare it to the original bytes. If changed, restart
the import on the new version. Read back the result after writing. Drive's
connector does not provide transactional compare-and-swap. Keep all inputs
and outputs private and do not add them to Git or upload them as Actions
artifacts. An unsupported CSV or PDF layout needs verified row transcription,
not guessing missing dates or values.

## Comparison and limits

The private workflow refreshes the report on trading-week afternoons and can
be run on demand. For an executed sale with a verified execution date it
compares observed proceeds to holding the sold quantity through the close on
D+0, D+1, D+5 and D+20 JPX sessions. A missing quote or an unverified execution
date stays missing, an uncompleted session stays pending, and a detected split
requires review. These are price comparisons, not strategy returns, tax, fees,
dividends, benefits, slippage or reinvestment attribution. An open buy remains
an open observation, not a position or a filled trade. An expired deadline is
not itself proof of the broker's final disposition.

The source is not a complete account statement. No new screenshot or order is
picked up just by appearing in a chat. A writer must save and verify it;
freshness is the source observation time, not report-generation time.
