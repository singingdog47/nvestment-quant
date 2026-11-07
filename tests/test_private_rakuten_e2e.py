"""Synthetic private-ledger write/readback, never actual brokerage content."""
import pytest
from src import private_rakuten_e2e as mod


def test_historical_private_ledger_roundtrip(tmp_path, monkeypatch):
    csv = tmp_path / "assetbalance(all)_20990102_120000.csv"
    csv.write_bytes(('資産合計,2000\n保有商品の評価額合計,1000\n'
                     '預り金合計,800\n預り金,300\n外貨預り金,100\n'
                     '国内株式信用保証金,400\nFX証拠金（純資産）,200\n'
                     '楽天銀行普通預金残高,1234\n').encode("cp932"))
    pdfs = [tmp_path / f"{x}.pdf" for x in ("buying", "domestic", "fund")]
    for p in pdfs:
        p.write_bytes(("synthetic PDF " + p.stem).encode())
    monkeypatch.setattr(mod, "parse_buying_power_pdf", lambda path: {
        "status": "ok", "source_as_of": "2099-01-02T12:00:00+09:00",
        "cash_buying_power_jpy": 1800})
    monkeypatch.setattr(mod, "_pdf_text", lambda p:
        "楽天銀行普通預金残高 1,234" if p == pdfs[0]
        else "注文一覧 2099/01/02 12:00" if p == pdfs[1]
        else "購入・売却履歴 2099/01/02 12:00")
    ledger = tmp_path / "private" / "facts.jsonl"
    result = mod.verify_historical_files(csv, *pdfs, ledger)
    assert result["status"] == "HISTORICAL_PARTIAL_COVERAGE"
    assert result["ledger_facts_verified"] == 4
    assert result["execution_ready"] is False
    assert result["deployable_cash_jpy"] is None
    assert ledger.exists()
    assert ledger.stat().st_mode & 0o777 == 0o600
    # Same immutable historical observation can be reverified idempotently.
    original_bytes = ledger.read_bytes()
    assert mod.verify_historical_files(csv, *pdfs, ledger)["ledger_facts_verified"] == 4
    assert ledger.read_bytes() == original_bytes  # Replay adds no rows.


def test_missing_pdf_rejects_without_ledger(tmp_path):
    csv = tmp_path / "assetbalance(all)_20990102_120000.csv"
    csv.write_bytes(b"dummy")
    ledger = tmp_path / "facts.jsonl"
    with pytest.raises(ValueError, match="Missing"):
        mod.verify_historical_files(csv, tmp_path / "none.pdf",
                                    tmp_path / "none2.pdf",
                                    tmp_path / "none3.pdf", ledger)
    assert not ledger.exists()


def test_readback_rejects_changed_evidence_even_if_values_match(tmp_path, monkeypatch):
    csv = tmp_path / "assetbalance(all)_20990102_120000.csv"
    csv.write_bytes(('資産合計,2000\n保有商品の評価額合計,1000\n'
                     '預り金合計,800\n預り金,300\n外貨預り金,100\n'
                     '国内株式信用保証金,400\nFX証拠金（純資産）,200\n'
                     '楽天銀行普通預金残高,1234\n').encode("cp932"))
    pdfs = [tmp_path / f"{x}.pdf" for x in ("buying", "domestic", "fund")]
    for p in pdfs:
        p.write_bytes(("synthetic " + p.stem).encode())
    monkeypatch.setattr(mod, "parse_buying_power_pdf", lambda path: {
        "status": "ok", "source_as_of": "2099-01-02T12:00:00+09:00",
        "cash_buying_power_jpy": 1800})
    monkeypatch.setattr(mod, "_pdf_text", lambda p:
        "楽天銀行普通預金残高 1,234" if p == pdfs[0]
        else "注文一覧 2099/01/02 12:00" if p == pdfs[1]
        else "購入・売却履歴 2099/01/02 12:00")
    real_read = mod.read_verified_facts
    calls = [0]

    def forged_read(path):
        calls[0] += 1
        records = real_read(path)
        if calls[0] == 2:
            records["rakuten_historical:account_summary"]["evidence_ref"] = (
                "private:sha256:" + "0" * 64)
        return records

    monkeypatch.setattr(mod, "read_verified_facts", forged_read)
    with pytest.raises(ValueError, match="read-back mismatch"):
        mod.verify_historical_files(csv, *pdfs, tmp_path / "facts.jsonl")


def test_same_source_path_rejected_before_parsing(tmp_path):
    csv = tmp_path / "assetbalance(all)_20990102_120000.csv"
    csv.write_bytes(b"csv")
    pdf = tmp_path / "one.pdf"
    pdf.write_bytes(b"pdf")
    ledger = tmp_path / "facts.jsonl"
    with pytest.raises(ValueError, match="Source paths must be distinct"):
        mod.verify_historical_files(csv, pdf, pdf, pdf, ledger)
    assert not ledger.exists()


def test_duplicate_document_bytes_rejected_before_parsing(tmp_path):
    csv = tmp_path / "assetbalance(all)_20990102_120000.csv"
    csv.write_bytes(b"csv")
    pdfs = [tmp_path / f"{n}.pdf" for n in ("buying", "domestic", "fund")]
    for pdf in pdfs:
        pdf.write_bytes(b"identical source bytes")
    ledger = tmp_path / "facts.jsonl"
    with pytest.raises(ValueError, match="Duplicate source content"):
        mod.verify_historical_files(csv, *pdfs, ledger)
    assert not ledger.exists()


def test_order_transaction_timestamp_is_not_export_footer(tmp_path, monkeypatch):
    csv = tmp_path / "assetbalance(all)_20990102_120000.csv"
    csv.write_bytes(('資産合計,2000\n保有商品の評価額合計,1000\n'
                     '預り金合計,800\n預り金,300\n外貨預り金,100\n'
                     '国内株式信用保証金,400\nFX証拠金（純資産）,200\n'
                     '楽天銀行普通預金残高,1234\n').encode("cp932"))
    pdfs = [tmp_path / f"{name}.pdf" for name in ("buying", "domestic", "fund")]
    for pdf in pdfs:
        pdf.write_bytes(("synthetic " + pdf.stem).encode())
    monkeypatch.setattr(mod, "parse_buying_power_pdf", lambda path: {
        "status": "ok", "source_as_of": "2099-01-02T12:00:00+09:00",
        "cash_buying_power_jpy": 1800})
    def pdf_text(path):
        if path == pdfs[0]:
            return "楽天銀行普通預金残高 1,234"
        heading = "注文一覧" if path == pdfs[1] else "購入・売却履歴"
        # Transaction date appears near top, footer has no export timestamp.
        return heading + "\n2099/01/02 12:00\n" + "\n".join(
            ["注文の詳細"] * 12 + ["ページ末尾"])
    monkeypatch.setattr(mod, "_pdf_text", pdf_text)
    ledger = tmp_path / "facts.jsonl"
    with pytest.raises(ValueError, match="footer timestamp"):
        mod.verify_historical_files(csv, *pdfs, ledger)
    assert not ledger.exists()
