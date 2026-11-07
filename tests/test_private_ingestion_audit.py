from private_ingestion_audit import audit_private_snapshot
from verified_facts_ledger import append_verified_fact


def test_empty_private_snapshot_reports_all_required_gaps(tmp_path):
    audit = audit_private_snapshot(tmp_path / "missing.jsonl",
                                   now="2099-01-02T10:00:00+09:00")
    assert audit["status"] == "INCOMPLETE"
    assert "orders_mutual_funds" in audit["missing_fresh_scopes"]
    assert "orders_foreign_equities" in audit["missing_fresh_scopes"]
    assert audit["execution_ready"] is False


def test_domestic_order_view_does_not_claim_account_wide_coverage(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_fact(p, key="orders:domestic:count", value=0,
                         scope="orders_domestic_cash",
                         observed_at="2099-01-02T09:00:00+09:00",
                         evidence_ref="private:synthetic-domestic-orders")
    audit = audit_private_snapshot(p, now="2099-01-02T10:00:00+09:00")
    assert "orders_domestic_cash" in audit["present_fresh_scopes"]
    assert "orders_mutual_funds" in audit["missing_fresh_scopes"]
    assert "orders_foreign_equities" in audit["missing_fresh_scopes"]
    assert "cash_and_settlement" in audit["missing_fresh_scopes"]
    assert audit["execution_ready"] is False


def test_stale_cash_cannot_satisfy_current_coverage(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_fact(p, key="cash:balance", value=100,
                         scope="cash_and_settlement",
                         observed_at="2099-01-01T00:00:00+09:00",
                         evidence_ref="private:synthetic-cash")
    audit = audit_private_snapshot(p, now="2099-01-04T10:00:00+09:00")
    assert "cash_and_settlement" in audit["missing_fresh_scopes"]
    assert audit["stale_or_future_keys"] == ["cash:balance"]
