import pytest

from import_newer_verified_snapshot import import_newer_verified_snapshot
from verified_facts_ledger import FactConflict, read_verified_facts, read_verified_history


def _snapshot(at, value, *, scope="bank", evidence="private:synthetic"):
    return {
        "verification_status": "verified", "observed_at": at,
        "evidence_ref": evidence,
        "quality": {"source_verified": True, "coherence_verified": True,
                    "source_scope": scope},
        "facts": [{"key": "bank:balance", "value": value, "scope": scope}],
    }


def test_daily_verified_update_links_history(tmp_path):
    p = tmp_path / "facts.jsonl"
    import_newer_verified_snapshot(_snapshot("2099-01-01T10:00:00+09:00", 100), str(p))
    import_newer_verified_snapshot(_snapshot("2099-01-02T10:00:00+09:00", 120), str(p))
    history = read_verified_history(p, key="bank:balance")
    assert [row["value"] for row in history] == [100, 120]
    assert history[1]["supersedes"] == history[0]["fact_id"]


def test_old_document_cannot_override_new_balance(tmp_path):
    p = tmp_path / "facts.jsonl"
    import_newer_verified_snapshot(_snapshot("2099-01-02T10:00:00+09:00", 120), str(p))
    original = p.read_bytes()
    with pytest.raises(FactConflict, match="strictly newer"):
        import_newer_verified_snapshot(_snapshot("2099-01-01T10:00:00+09:00", 100), str(p))
    assert p.read_bytes() == original


def test_equal_timestamp_different_balance_rejected(tmp_path):
    p = tmp_path / "facts.jsonl"
    snapshot = _snapshot("2099-01-01T10:00:00+09:00", 100)
    import_newer_verified_snapshot(snapshot, str(p))
    with pytest.raises(FactConflict):
        import_newer_verified_snapshot(_snapshot("2099-01-01T10:00:00+09:00", 150), str(p))
    assert read_verified_facts(p)["bank:balance"]["value"] == 100


def test_scope_change_requires_manual_reconciliation(tmp_path):
    p = tmp_path / "facts.jsonl"
    import_newer_verified_snapshot(_snapshot("2099-01-01T10:00:00+09:00", 100), str(p))
    with pytest.raises(FactConflict, match="Scope changed"):
        import_newer_verified_snapshot(_snapshot("2099-01-02T10:00:00+09:00", 120,
                                                  scope="all_accounts"), str(p))


def test_unverified_source_cannot_update_balance(tmp_path):
    p = tmp_path / "facts.jsonl"
    snapshot = _snapshot("2099-01-01T10:00:00+09:00", 100)
    snapshot["quality"]["coherence_verified"] = False
    with pytest.raises(ValueError, match="coherence"):
        import_newer_verified_snapshot(snapshot, str(p))
    assert not p.exists()


def test_newer_batch_conflict_rolls_back_all_assets(tmp_path):
    p = tmp_path / "facts.jsonl"
    import_newer_verified_snapshot(_snapshot("2099-01-01T10:00:00+09:00", 100), str(p))
    original = p.read_bytes()
    batch = _snapshot("2099-01-02T10:00:00+09:00", 120)
    batch["facts"].append({"key": "bank:balance", "value": 999, "scope": "bank"})
    with pytest.raises(ValueError, match="unique"):
        import_newer_verified_snapshot(batch, str(p))
    assert p.read_bytes() == original
