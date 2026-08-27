from src.private_account_import import (
    parse_account_summary_bytes,
    parse_buying_power_pdf,
    parse_orders_bytes,
    source_as_of,
)


def test_account_summary_is_classified_separately_from_holdings():
    text = '''"■資産合計欄"
"","時価評価額[円]","前日比[円]","前日比[％]"
"資産合計","12,345,678","+12,345","+0.10"
"保有商品の評価額合計","11,000,000","+20,000","+0.18"
"預り金合計","700,000","-5,000","-0.71"
"預り金","650,000","-5,000","-0.76"
"外貨預り金","10,000","0","0.00"
"信用保証金","40,000","0","0.00"
"FX証拠金（純資産）","595,678","-2,655","-0.44"
'''
    result = parse_account_summary_bytes(text.encode("cp932"))
    assert result["total_assets_jpy"] == 12_345_678
    assert result["invested_assets_jpy"] == 11_000_000
    assert result["cash_deposit_jpy"] == 650_000
    assert result["daily_change_jpy"] == 12_345


def test_orders_are_audited_without_creating_orders():
    text = '''注文番号,状況,銘柄,売買,注文数量[株/口],約定数量[株/口],注文単価[円]
1001,約定,サンプルA,買付,100,100,850
1002,執行中,サンプルB,買付,100,0,1980
1003,待機中,サンプルC,売付,200,0,-
'''
    result = parse_orders_bytes(text.encode("cp932"))
    assert result["orders_count"] == 3
    assert result["filled_orders_count"] == 1
    assert result["open_orders_count"] == 2


def test_latest_timestamp_prefers_export_name():
    value, method = source_as_of("assetbalance(all)_20260827_155545.csv", "2026-08-28T01:00:00Z")
    assert value == "2026-08-27T15:55:45+09:00"
    assert method == "filename_embedded_export_time"


def test_buying_power_pdf_extracts_cash_and_embedded_timestamp(monkeypatch):
    text = '''買付可能額（本日）
08/27 20:22
現物買付可能額※
1,500,000 円
投資信託買付可能額※
1,500,000 円
信用新規建余力※
9,000,000 円
米国株式買付可能額（円貨）※
1,500,000 円
'''

    class Page:
        def extract_text(self):
            return text

    class Reader:
        def __init__(self, _):
            self.pages = [Page()]

    monkeypatch.setattr("pypdf.PdfReader", Reader)
    result = parse_buying_power_pdf("unused.pdf")
    assert result["cash_buying_power_jpy"] == 1_500_000
    assert result["fund_buying_power_jpy"] == 1_500_000
    assert result["margin_capacity_jpy"] == 9_000_000
    assert result["source_as_of"].endswith("08-27T20:22:00+09:00")
