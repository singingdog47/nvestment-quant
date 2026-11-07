import pytest
from private_account_facts_adapter import import_account_facts
from verified_facts_ledger import read_verified_facts


def _inputs():
    return {"status": "ok", "missing_input_types": [], "stale_input_types": [],
            "coherence_verified": True,
            "inputs": {
                "account_summary": {"data_status": "ok", "source_file": "holdings.csv",
                    "source_as_of": "2026-11-06T22:51:00+09:00",
                    "source_as_of_method": "filename_embedded_export_time",
                    "total_assets_jpy": 20000000, "invested_assets_jpy": 18000000},
                "buying_power": {"data_status": "ok", "source_file": "buying-power.pdf",
                    "source_as_of": "2026-11-06T22:46:00+09:00",
                    "source_as_of_method": "pdf_footer_explicit_year",
                    "cash_buying_power_jpy": 2800000}}}


def test_per_source_timestamps_are_preserved(tmp_path):
    path = tmp_path / "private" / "facts.jsonl"
    assert import_account_facts(_inputs(), str(path))["status"] == "ok"
    facts = read_verified_facts(path)
    assert facts["account_summary:total_assets_jpy"]["observed_at"].endswith("22:51:00+09:00")
    assert facts["buying_power:cash_buying_power_jpy"]["observed_at"].endswith("22:46:00+09:00")


def test_unverified_coherence_is_rejected(tmp_path):
    inputs = _inputs()
    inputs["coherence_verified"] = False
    with pytest.raises(ValueError, match="coherence"):
        import_account_facts(inputs, str(tmp_path / "facts.jsonl"))
