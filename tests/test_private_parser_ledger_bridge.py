"""Synthetic-only end-to-end bridge from Rakuten CSV parser to private ledger."""
from datetime import datetime
from private_account_import import parse_account_summary_bytes
from private_data_coherence import classify_private_inputs
from private_account_facts_adapter import import_account_facts
from verified_facts_ledger import read_verified_facts


def test_parsed_csv_to_private_ledger_requires_independent_coherence(tmp_path):
    raw = ('資産合計,1000000\n保有商品の評価額合計,800000\n'
           '預り金,200000\n').encode("cp932")
    account = parse_account_summary_bytes(raw)
    assert account["total_assets_jpy"] == 1000000
    at = "2099-01-01T10:00:00+09:00"
    account.update(status="ok", source_as_of=at,
                   source_as_of_method="filename_embedded_export_time",
                   source_file="synthetic-account.csv")
    buying = {"status": "ok", "source_as_of": at,
              "source_as_of_method": "pdf_footer_explicit_year",
              "source_file": "synthetic-buying.pdf",
              "cash_buying_power_jpy": 300000}
    orders = {"status": "ok", "source_as_of": at,
              "source_as_of_method": "pdf_footer_explicit_year",
              "orders_count": 0, "items": []}
    payload = {"status": "ok", "inputs": {
        "account_summary": account, "buying_power": buying, "orders": orders}}
    manifest = {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"}
    coherence = classify_private_inputs(
        manifest, payload, now=datetime.fromisoformat("2099-01-01T11:00:00+09:00"))
    assert coherence["status"] == "VERIFIED"
    path = tmp_path / "private.jsonl"
    imported = import_account_facts(payload, str(path), coherence=coherence)
    assert imported["status"] == "ok"
    facts = read_verified_facts(path)
    assert facts["account_summary:total_assets_jpy"]["value"] == 1000000
    assert facts["buying_power:cash_buying_power_jpy"]["value"] == 300000
    assert "orders:account_wide_count" not in facts


def test_stale_csv_to_ledger_is_rejected(tmp_path):
    at = "2099-01-01T10:00:00+09:00"
    payload = {"status": "ok", "inputs": {
        kind: {"status": "ok", "source_as_of": at,
               "source_as_of_method": "filename_embedded_export_time"}
        for kind in ("account_summary", "buying_power", "orders")}}
    verdict = classify_private_inputs(
        {"source_as_of": at, "source_as_of_method": "filename_embedded_export_time"},
        payload, now=datetime.fromisoformat("2099-01-05T11:00:00+09:00"))
    assert verdict["decision_safe"] is False
    path = tmp_path / "private.jsonl"
    try:
        import_account_facts(payload, str(path), coherence=verdict)
    except ValueError:
        pass
    else:
        raise AssertionError("Stale brokerage input was accepted")
    assert not path.exists()
