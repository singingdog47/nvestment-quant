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
        p.write_bytes(b"synthetic PDF bytes for monkeypatched extraction")
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
        p.write_bytes(b"synthetic")
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
