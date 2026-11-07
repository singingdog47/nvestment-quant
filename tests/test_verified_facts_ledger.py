import pytest
from verified_facts_ledger import FactConflict, append_verified_fact, read_verified_facts


def test_verified_facts_are_persistent_and_require_explicit_supersession(tmp_path):
    p = tmp_path / "facts.jsonl"
    args = dict(key="fund_order:5387:status", observed_at="2026-11-06T22:46:00+09:00",
                evidence_ref="private:rakuten-fund-history:20261106", scope="fund_orders")
    original = append_verified_fact(p, value="filled", **args)
    assert read_verified_facts(p)[args["key"]]["value"] == "filled"
    with pytest.raises(FactConflict):
        append_verified_fact(p, value="pending", **args)
    changed = append_verified_fact(p, value="settled", supersedes=original["fact_id"],
                                   **{**args, "observed_at": "2026-11-11T12:00:00+09:00",
                                      "evidence_ref": "private:rakuten-settlement:20261111"})
    assert changed["supersedes"] == original["fact_id"]
    assert len(p.read_text(encoding="utf-8").splitlines()) == 2


def test_older_observation_cannot_override_verified_fact(tmp_path):
    p = tmp_path / "facts.jsonl"
    a = append_verified_fact(p, key="cash", value=100, observed_at="2026-11-06T22:46:00+09:00",
                             evidence_ref="private:a", scope="account")
    with pytest.raises(FactConflict):
        append_verified_fact(p, key="cash", value=200, observed_at="2026-11-05T22:46:00+09:00",
                             evidence_ref="private:b", scope="account", supersedes=a["fact_id"])


def test_missing_evidence_rejected(tmp_path):
    with pytest.raises(ValueError):
        append_verified_fact(tmp_path / "facts.jsonl", key="cash", value=100,
                             observed_at="2026-11-06T22:46:00+09:00", evidence_ref="", scope="account")
