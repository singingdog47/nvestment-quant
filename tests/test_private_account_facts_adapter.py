import pytest
from private_account_facts_adapter import import_account_facts
from verified_facts_ledger import read_verified_facts


def _inputs():
    return {"status": "ok", "missing_input_types": [], "stale_input_types": [],
            "inputs": {
                "account_summary": {"status": "ok", "source_file": "holdings.csv",
                    "source_as_of": "2099-01-01T22:51:00+09:00",
                    "source_as_of_method": "filename_embedded_export_time",
                    "total_assets_jpy": 20000000, "invested_assets_jpy": 18000000},
                "buying_power": {"status": "ok", "source_file": "buying-power.pdf",
                    "source_as_of": "2099-01-01T22:46:00+09:00",
                    "source_as_of_method": "pdf_footer_explicit_year",
                    "cash_buying_power_jpy": 2800000}}}


def _coherence(inputs):
    return {"status": "VERIFIED", "decision_safe": True,
            "inputs": {key: {"status": "VERIFIED",
                             "source_as_of": value["source_as_of"],
                             "source_as_of_method": value["source_as_of_method"]}
                       for key, value in inputs["inputs"].items()} |
                      {"orders": {"status": "VERIFIED"}}}


def test_per_source_timestamps_are_preserved(tmp_path):
    path = tmp_path / "private" / "facts.jsonl"
    inputs = _inputs()
    assert import_account_facts(inputs, str(path), coherence=_coherence(inputs))["status"] == "ok"
    facts = read_verified_facts(path)
    assert facts["account_summary:total_assets_jpy"]["observed_at"].endswith("22:51:00+09:00")
    assert facts["buying_power:cash_buying_power_jpy"]["observed_at"].endswith("22:46:00+09:00")


def test_unverified_coherence_is_rejected(tmp_path):
    inputs = _inputs()
    verdict = _coherence(inputs)
    verdict["decision_safe"] = False
    with pytest.raises(ValueError, match="coherence"):
        import_account_facts(inputs, str(tmp_path / "facts.jsonl"), coherence=verdict)


def test_invalid_second_source_never_writes_first_source(tmp_path):
    path = tmp_path / "facts.jsonl"
    inputs = _inputs()
    verdict = _coherence(inputs)
    inputs["inputs"]["buying_power"]["source_file"] = ""
    with pytest.raises(ValueError, match="evidence"):
        import_account_facts(inputs, str(path), coherence=verdict)
    assert not path.exists()


def test_conflicting_second_source_rolls_back_first_source(tmp_path):
    from verified_facts_ledger import append_verified_fact, FactConflict
    path = tmp_path / "facts.jsonl"
    append_verified_fact(path, key="buying_power:cash_buying_power_jpy",
                         value=99, scope="buying_power",
                         observed_at="2098-12-31T10:00:00+09:00",
                         evidence_ref="private:synthetic")
    original = path.read_bytes()
    inputs = _inputs()
    with pytest.raises(FactConflict):
        import_account_facts(inputs, str(path), coherence=_coherence(inputs))
    assert path.read_bytes() == original


def test_account_source_provenance_is_preserved(tmp_path):
    path = tmp_path / "facts.jsonl"
    inputs = _inputs()
    import_account_facts(inputs, str(path), coherence=_coherence(inputs))
    facts = read_verified_facts(path)
    assert facts["account_summary:total_assets_jpy"]["evidence_ref"] == "private:holdings.csv"
    assert facts["buying_power:cash_buying_power_jpy"]["evidence_ref"] == "private:buying-power.pdf"
