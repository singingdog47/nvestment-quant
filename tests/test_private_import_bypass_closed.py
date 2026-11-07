import pytest
from private_account_facts_adapter import import_account_facts


def test_cached_verdict_only_is_rejected_before_writing(tmp_path):
    p = tmp_path / "private.jsonl"
    payload = {"status": "ok", "inputs": {}}
    cached = {"status": "VERIFIED", "decision_safe": True}
    with pytest.raises(ValueError, match="Portfolio manifest required"):
        import_account_facts(payload, str(p), coherence=cached)
    assert not p.exists()
