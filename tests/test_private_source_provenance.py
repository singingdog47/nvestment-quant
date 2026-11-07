import hashlib
import pytest
from import_newer_verified_snapshot import import_newer_verified_snapshot
from private_source_provenance import verified_source_evidence
from verified_facts_ledger import FactConflict, read_verified_facts

def snapshot(day, value, evidence="private:synthetic"):
    return {"verification_status": "verified", "observed_at": f"2099-01-{day:02d}T10:00:00+09:00",
            "evidence_ref": evidence, "quality": {"source_verified": True,
            "coherence_verified": True, "source_scope": "bank"},
            "facts": [{"key": "bank:balance", "value": value, "scope": "bank"}]}

def test_private_file_hash_matches_bytes_and_is_recorded(tmp_path):
    p = tmp_path / "private.jsonl"
    f = tmp_path / "synthetic-export.csv"
    f.write_bytes(b"synthetic,100\n")
    expected = hashlib.sha256(f.read_bytes()).hexdigest()
    item = snapshot(1, 100)
    item["source_sha256"] = expected
    import_newer_verified_snapshot(item, p, source_file=f)
    assert read_verified_facts(p)["bank:balance"]["evidence_ref"] == "private:sha256:" + expected

def test_mismatched_digest_rejects_without_ledger(tmp_path):
    p = tmp_path / "private.jsonl"
    f = tmp_path / "synthetic-export.csv"
    f.write_bytes(b"synthetic,100\n")
    item = snapshot(1, 100)
    item["source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        import_newer_verified_snapshot(item, p, source_file=f)
    assert not p.exists()

def test_hash_claim_without_source_file_rejected(tmp_path):
    p = tmp_path / "private.jsonl"
    item = snapshot(1, 100, "private:sha256:" + "0" * 64)
    with pytest.raises(ValueError, match="Source file required"):
        import_newer_verified_snapshot(item, p)
    assert not p.exists()

def test_same_file_renamed_cannot_update_balance(tmp_path):
    p = tmp_path / "private.jsonl"
    first = tmp_path / "first.csv"
    second = tmp_path / "renamed.csv"
    first.write_bytes(b"synthetic,100\n")
    second.write_bytes(first.read_bytes())
    import_newer_verified_snapshot(snapshot(1, 100), p, source_file=first)
    before = p.read_bytes()
    with pytest.raises(FactConflict, match="distinct source evidence"):
        import_newer_verified_snapshot(snapshot(2, 120), p, source_file=second)
    assert p.read_bytes() == before

def test_symlink_source_rejected(tmp_path):
    f = tmp_path / "source.csv"
    f.write_bytes(b"synthetic")
    link = tmp_path / "link.csv"
    link.symlink_to(f)
    with pytest.raises(ValueError, match="non-symlink"):
        verified_source_evidence(link)
