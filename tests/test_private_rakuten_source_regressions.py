"""Synthetic regressions derived from the 2026-11-06 Rakuten source layout.

No private account data is stored in the public repository.
"""
from private_account_import import parse_account_summary_bytes


def test_domestic_margin_collateral_label_is_recognized():
    raw = ('資産合計,"2,000"\n保有商品の評価額合計,"1,000"\n'
           '国内株式信用保証金,700\n預り金,300\n').encode("cp932")
    result = parse_account_summary_bytes(raw)
    assert result["margin_collateral_jpy"] == 700
    assert result["cash_deposit_jpy"] == 300


def test_yearless_pdf_footer_does_not_gain_current_year(tmp_path):
    from private_account_import import parse_buying_power_pdf
    from pypdf import PdfWriter
    from unittest.mock import patch
    p = tmp_path / "yearless.pdf"
    # Mock extracted PDF text while retaining a valid minimal PDF container.
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with p.open("wb") as fp:
        writer.write(fp)
    class FakePage:
        def extract_text(self):
            return "現物買付可能額 2,000 円\n11/06 22:46"
    class FakeReader:
        def __init__(self, path):
            self.pages = [FakePage()]
    with patch("pypdf.PdfReader", FakeReader):
        result = parse_buying_power_pdf(p)
    assert result["cash_buying_power_jpy"] == 2000
    assert result["source_as_of"] is None
    assert result["source_as_of_method"] == "missing"
