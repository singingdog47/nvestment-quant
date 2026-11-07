import pytest
from import_verified_snapshot import import_verified_snapshot
from verified_facts_ledger import FactConflict, read_verified_facts


def _snapshot(value="filled"):
    return {"verification_status": "verified", "observed_at": "2026-11-06T22:46:00+09:00",
            "evidence_ref": "private:fund-order-history:20261106",
            "quality": {"source_verified": True, "coherence_verified": True, "source_scope": "fund_orders"},
            "facts": [{"key": "fund_order:5387:status", "value": value,
                       "scope": "rakuten_fund_orders"}]}


def test_verified_snapshot_import(tmp_path):
    path = tmp_path / "private" / "facts.jsonl"
    result = import_verified_snapshot(_snapshot(), path)
    assert result["facts_imported"] == 1
    assert read_verified_facts(path)["fund_order:5387:status"]["value"] == "filled"


def test_unverified_snapshot_cannot_modify_ledger(tmp_path):
    path = tmp_path / "facts.jsonl"
    snapshot = _snapshot()
    snapshot["verification_status"] = "partial"
    with pytest.raises(ValueError):
        import_verified_snapshot(snapshot, path)
    assert not path.exists()


def test_conflicting_batch_is_rejected_before_writes(tmp_path):
    path = tmp_path / "facts.jsonl"
    import_verified_snapshot(_snapshot(), path)
    snapshot = _snapshot("pending")
    snapshot["facts"].insert(0, {"key": "cash:total", "value": 100,
                                  "scope": "account"})
    with pytest.raises(FactConflict):
        import_verified_snapshot(snapshot, path)
    assert "cash:total" not in read_verified_facts(path)


def test_self_declared_verified_without_upstream_evidence_rejected(tmp_path):
    snapshot = _snapshot()
    snapshot["quality"]["coherence_verified"] = False
    with pytest.raises(ValueError, match="coherence"):
        import_verified_snapshot(snapshot, tmp_path / "facts.jsonl")
