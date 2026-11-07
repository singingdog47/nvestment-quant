from datetime import datetime, timedelta
import pytest

from private_account_rechecked_import import import_account_facts_rechecked
from verified_facts_ledger import read_verified_facts


def fixture_inputs(at):
    return {"status": "ok", "inputs": {
        "account_summary": {"status": "ok", "source_as_of": at,
            "source_as_of_method": "filename_embedded_export_time",
            "source_file": "synthetic-portfolio.csv",
            "total_assets_jpy": 100, "invested_assets_jpy": 80},
        "buying_power": {"status": "ok", "source_as_of": at,
            "source_as_of_method": "pdf_footer_explicit_year",
            "source_file": "synthetic-buying.pdf", "cash_buying_power_jpy": 20},
        "orders": {"status": "ok", "source_as_of": at,
            "source_as_of_method": "pdf_footer_explicit_year",
            "items": [], "orders_count": 0}}}


def test_rechecked_import_writes_fresh_synthetic_data(tmp_path):
    at = "2099-01-01T10:00:00+09:00"
    manifest = {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"}
    p = tmp_path / "private.jsonl"
    result = import_account_facts_rechecked(
        manifest, fixture_inputs(at), p,
        now=datetime.fromisoformat("2099-01-01T11:00:00+09:00"))
    assert result["coherence_recomputed"] is True
    assert result["execution_ready"] is False
    assert read_verified_facts(p)["account_summary:total_assets_jpy"]["value"] == 100


def test_cached_verified_verdict_cannot_override_stale_inputs(tmp_path):
    at = "2099-01-01T10:00:00+09:00"
    manifest = {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"}
    p = tmp_path / "private.jsonl"
    with pytest.raises(ValueError, match="Freshly recomputed"):
        import_account_facts_rechecked(
            manifest, fixture_inputs(at), p,
            now=datetime.fromisoformat("2099-01-05T11:00:00+09:00"))
    assert not p.exists()


def test_mismatched_orders_timestamp_cannot_be_masked(tmp_path):
    at = "2099-01-01T10:00:00+09:00"
    manifest = {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"}
    payload = fixture_inputs(at)
    payload["inputs"]["orders"]["source_as_of"] = "2099-01-03T10:00:00+09:00"
    p = tmp_path / "private.jsonl"
    with pytest.raises(ValueError, match="Freshly recomputed"):
        import_account_facts_rechecked(
            manifest, payload, p,
            now=datetime.fromisoformat("2099-01-03T11:00:00+09:00"),
            max_age_hours=100)
    assert not p.exists()


def test_sources_on_opposite_sides_of_portfolio_cannot_exceed_skew(tmp_path):
    from private_data_coherence import classify_private_inputs
    at = "2099-01-02T12:00:00+09:00"
    manifest = {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"}
    payload = fixture_inputs(at)
    payload["inputs"]["account_summary"]["source_as_of"] = "2099-01-01T13:00:00+09:00"
    payload["inputs"]["orders"]["source_as_of"] = "2099-01-03T11:00:00+09:00"
    now = datetime.fromisoformat("2099-01-03T12:00:00+09:00")
    verdict = classify_private_inputs(manifest, payload, now=now, max_age_hours=72,
                                      max_skew_hours=24)
    assert "ACCOUNT_SOURCES_TIME_MISMATCH" in verdict["portfolio_reasons"]
    assert verdict["decision_safe"] is False
    p = tmp_path / "private.jsonl"
    with pytest.raises(ValueError, match="Freshly recomputed"):
        import_account_facts_rechecked(manifest, payload, p, now=now,
                                       max_age_hours=72, max_skew_hours=24)
    assert not p.exists()


def test_source_time_span_at_boundary_is_accepted_by_coherence():
    from private_data_coherence import classify_private_inputs
    at = "2099-01-02T12:00:00+09:00"
    manifest = {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"}
    payload = fixture_inputs(at)
    payload["inputs"]["account_summary"]["source_as_of"] = "2099-01-02T00:00:00+09:00"
    payload["inputs"]["orders"]["source_as_of"] = "2099-01-03T00:00:00+09:00"
    verdict = classify_private_inputs(
        manifest, payload, now=datetime.fromisoformat("2099-01-03T01:00:00+09:00"),
        max_age_hours=48, max_skew_hours=24)
    assert verdict["status"] == "VERIFIED"
