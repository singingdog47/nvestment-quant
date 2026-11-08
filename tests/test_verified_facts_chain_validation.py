import hashlib
import json
import pytest
from verified_facts_ledger import FactConflict, append_verified_fact, read_verified_facts


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _rehash(row):
    row["fact_id"] = hashlib.sha256(_canonical({
        k: v for k, v in row.items() if k not in ("fact_id", "recorded_at_utc")
    }).encode()).hexdigest()
    return row


def test_recomputed_hash_cannot_hide_backward_timestamp(tmp_path):
    p = tmp_path / "facts.jsonl"
    a = append_verified_fact(p, key="demo", value=100,
                             observed_at="2099-01-02T00:00:00+09:00",
                             evidence_ref="private:a", scope="bank")
    row = dict(a)
    row["value"] = 200
    row["observed_at"] = "2099-01-01T00:00:00+09:00"
    row["supersedes"] = a["fact_id"]
    p.write_text(p.read_text() + _canonical(_rehash(row)) + "\n", encoding="utf-8")
    with pytest.raises(FactConflict, match="out-of-order"):
        read_verified_facts(p)


def test_recomputed_hash_cannot_hide_invalid_supersession(tmp_path):
    p = tmp_path / "facts.jsonl"
    a = append_verified_fact(p, key="demo", value=100,
                             observed_at="2099-01-01T00:00:00+09:00",
                             evidence_ref="private:a", scope="bank")
    row = dict(a)
    row["supersedes"] = "unrelated"
    row["observed_at"] = "2099-01-02T00:00:00+09:00"
    p.write_text(p.read_text() + _canonical(_rehash(row)) + "\n", encoding="utf-8")
    with pytest.raises(FactConflict, match="invalid supersedes"):
        read_verified_facts(p)
