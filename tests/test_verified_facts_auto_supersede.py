import pytest
from verified_facts_ledger import FactConflict, append_verified_facts, read_verified_facts, read_verified_history

def fact(key, value, day, scope="bank"):
    return {"key": key, "value": value, "scope": scope, "observed_at": f"2099-01-{day:02d}T10:00:00+09:00", "evidence_ref": f"private:synthetic-{day}"}

def test_multi_asset_auto_supersession(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_facts(p, [fact("bank:balance", 100, 1), fact("crypto:quantity", 2, 1, "crypto")])
    append_verified_facts(p, [fact("bank:balance", 120, 2), fact("crypto:quantity", 3, 2, "crypto")], auto_supersede=True)
    assert [r["value"] for r in read_verified_history(p, key="bank:balance")] == [100, 120]
    assert [r["value"] for r in read_verified_history(p, key="crypto:quantity")] == [2, 3]

def test_stale_batch_rolls_back(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_facts(p, [fact("bank:balance", 100, 2)])
    before = p.read_bytes()
    with pytest.raises(FactConflict, match="strictly newer"):
        append_verified_facts(p, [fact("new:asset", 9, 3), fact("bank:balance", 110, 1)], auto_supersede=True)
    assert p.read_bytes() == before
    assert "new:asset" not in read_verified_facts(p)

def test_scope_change_rejected(tmp_path):
    p = tmp_path / "facts.jsonl"
    append_verified_facts(p, [fact("bank:balance", 100, 1)])
    with pytest.raises(FactConflict, match="Scope changed"):
        append_verified_facts(p, [fact("bank:balance", 110, 2, "all_accounts")], auto_supersede=True)
