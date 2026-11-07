import pytest
from verified_facts_ledger import FactConflict, append_verified_fact, append_verified_facts, read_verified_facts


def _fact(key, value, supersedes=None):
    return {"key": key, "value": value, "observed_at": "2099-01-01T10:00:00+09:00",
            "evidence_ref": "private:synthetic", "scope": "test",
            "supersedes": supersedes}


def test_batch_conflict_never_writes_partial_rows(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_fact(p, **_fact("known", 1))
    original = p.read_bytes()
    with pytest.raises(FactConflict):
        append_verified_facts(p, [_fact("new", 2), _fact("known", 3)])
    assert p.read_bytes() == original


def test_batch_commit_and_reload(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_facts(p, [_fact("bank", 100), _fact("fx", -20)])
    assert set(read_verified_facts(p)) == {"bank", "fx"}
    assert p.read_bytes().endswith(b"\n")


def test_duplicate_keys_within_batch_rejected(tmp_path):
    p = tmp_path / "facts.jsonl"
    with pytest.raises(FactConflict):
        append_verified_facts(p, [_fact("same", 1), _fact("same", 2)])
    assert not p.exists()
