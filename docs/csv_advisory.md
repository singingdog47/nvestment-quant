# CSV-first portfolio advice

Routine portfolio analysis needs a current Rakuten assetbalance CSV, not a buying-power PDF.
Cash planning uses the separately parsed JPY deposit and Rakuten Bank balance,
less a JPY 500,000 reserve. Margin and FX collateral are excluded. This is a
planning estimate, not broker-certified executable buying power or reconciled
household spending. Missing bank balance or a failed balance reconciliation
must not be filled with zeros.

The private input folder may contain `private_order_declaration.json` with
`source: user_statement`, `scope: all_open_orders`, integer `count: 0`, and an
explicit timezone-aware `observed_at`. Only create this from an actual user
statement. The statement is valid on its JST observation day for at most eight
hours. Never roll its date forward automatically; ask for a brief status update
when needed, not an order screenshot. Order changes invalidate the statement.
Do not commit declarations or private balances to the repository.

The readiness report now distinguishes `analysis_ready`,
`capital_planning_ready`, and `execution_ready`. The latter remains false.
Legacy `data_ready` is the stricter broker-evidence gate and may remain false
while CSV analysis is ready. Neither flag says that market/fundamental research
has been completed. Current PDF cash differences or contradictory parsed
orders block the cash plan, but absence of a buying-power PDF does not.

Domestic and mutual-fund PDFs are retained separately in `order_documents`.
Multiple document types produce an explicitly partial aggregate, never an
account-wide zero-order assertion. The PDF parser dates documents; it does not
yet certify complete order rows.
