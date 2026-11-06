from datetime import datetime, timezone

from src.private_data_coherence import classify_private_inputs

NOW = datetime(2026, 11, 6, 12, 0, tzinfo=timezone.utc)
PF = {"source_as_of": "2026-11-06T15:00:00+09:00", "source_as_of_method": "filename_embedded_export_time"}


def inputs(as_of="2026-11-06T15:00:00+09:00", method="filename_embedded_export_time"):
    return {"inputs": {
        kind: {"source_as_of": as_of, "source_as_of_method": method, "data_status": "ok"}
        for kind in ("account_summary", "orders", "buying_power")
    }}


def test_consistent_current_inputs_verified():
    result = classify_private_inputs(PF, inputs(), now=NOW)
    assert result["status"] == "VERIFIED"
    assert result["decision_safe"] is True


def test_old_orders_are_not_verified():
    x = inputs()
    x["inputs"]["orders"]["source_as_of"] = "2026-11-04T15:00:00+09:00"
    result = classify_private_inputs(PF, x, now=NOW)
    assert result["status"] == "PARTIAL"
    assert "PORTFOLIO_TIME_MISMATCH" in result["inputs"]["orders"]["reasons"]


def test_stale_buying_power_is_not_verified():
    x = inputs()
    x["inputs"]["buying_power"]["data_status"] = "stale"
    assert classify_private_inputs(PF, x, now=NOW)["inputs"]["buying_power"]["status"] == "UNVERIFIED"


def test_inferred_or_upload_time_not_trusted():
    x = inputs(method="drive_modified_time_fallback")
    assert classify_private_inputs(PF, x, now=NOW)["decision_safe"] is False


def test_unknown_portfolio_date_blocks_all_decisions():
    pf = {"source_as_of": None, "source_as_of_method": "missing"}
    result = classify_private_inputs(pf, inputs(), now=NOW)
    assert result["status"] == "UNVERIFIED"
    assert "PORTFOLIO_TIMESTAMP_UNVERIFIED" in result["portfolio_reasons"]


def test_missing_input_partial():
    x = inputs()
    del x["inputs"]["orders"]
    assert classify_private_inputs(PF, x, now=NOW)["inputs"]["orders"]["status"] == "UNVERIFIED"


def test_future_timestamp_is_not_verified():
    x = inputs("2026-11-07T15:00:00+09:00")
    assert classify_private_inputs(PF, x, now=NOW)["decision_safe"] is False


def test_yearless_pdf_date_requires_verification():
    x = inputs(method="pdf_embedded_timestamp_inferred_year")
    # The year is inferred and cannot be considered brokerage-verified.
    assert classify_private_inputs(PF, x, now=NOW)["inputs"]["buying_power"]["status"] == "UNVERIFIED"


def test_shared_state_withholds_stale_cash_and_unknown_order_count(tmp_path):
    from src.investment_state import build_investment_state

    from datetime import timedelta
    current = datetime.now(timezone.utc)
    manifest = {"source_as_of": current.isoformat(), "source_as_of_method": "filename_embedded_export_time"}
    stale = inputs(as_of=current.isoformat())
    stale["inputs"]["account_summary"].update({
        "cash_deposit_jpy": 300000, "total_assets_jpy": 2000000
    })
    stale["inputs"]["buying_power"].update({
        "cash_buying_power_jpy": 1000000, "data_status": "stale"
    })
    stale["inputs"]["orders"].update({
        "source_as_of": (current - timedelta(days=2)).isoformat(),
        "items": [{"status": "執行中", "code": "1234"}]
    })
    state = build_investment_state(
        stale, manifest, {"status": "ok"},
        decision_context_path=tmp_path / "missing_decision.json",
        watchlist_path=tmp_path / "missing_watchlist.csv",
    )
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["open_orders"]["count"] is None
    assert state["open_orders"]["source_status"] == "UNVERIFIED"
    assert state["quality"]["data_coherence"]["decision_safe"] is False


def test_shared_state_withholds_capital_if_pf_time_unverified(tmp_path):
    from src.investment_state import build_investment_state

    manifest = {"source_as_of": None, "source_as_of_method": "missing"}
    values = inputs()
    values["inputs"]["buying_power"]["cash_buying_power_jpy"] = 1000000
    state = build_investment_state(
        values, manifest, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["open_orders"]["count"] is None


def test_verified_account_cash_cannot_replace_missing_buying_power(tmp_path):
    from src.investment_state import build_investment_state

    current = datetime.now(timezone.utc)
    manifest = {"source_as_of": current.isoformat(), "source_as_of_method": "filename_embedded_export_time"}
    values = inputs(as_of=current.isoformat())
    values["inputs"]["account_summary"]["cash_deposit_jpy"] = 967191
    values["inputs"]["buying_power"]["cash_buying_power_jpy"] = None
    state = build_investment_state(
        values, manifest, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert state["capital"]["deployable_cash_jpy"] is None


def test_pdf_inferred_year_provenance_is_not_overwritten(tmp_path, monkeypatch):
    from src import run_portfolio_risk as runner

    pdf = tmp_path / "buying_power.pdf"
    pdf.write_bytes(b"synthetic")
    monkeypatch.setattr(runner, "parse_buying_power_pdf", lambda p: {
        "status": "ok", "source_as_of": "2026-11-06T22:46:00+09:00",
        "cash_buying_power_jpy": 2863480,
    })
    result = runner._build_latest_account_inputs(
        tmp_path, [(pdf, {"name": "buying_power.pdf", "modifiedTime": "2026-11-06T13:46:50Z"})]
    )
    item = result["inputs"]["buying_power"]
    assert item["source_as_of_method"] == "pdf_embedded_timestamp_inferred_year"
    assert classify_private_inputs(
        {"source_as_of": "2026-11-06T22:51:14+09:00", "source_as_of_method": "filename_embedded_export_time"},
        result, now=datetime(2026, 11, 6, 14, 0, tzinfo=timezone.utc),
    )["inputs"]["buying_power"]["status"] == "UNVERIFIED"


def test_orders_pdf_parses_filled_order_and_explicit_year(tmp_path, monkeypatch):
    import pypdf
    from src.private_account_import import parse_orders_pdf

    class Page:
        def extract_text(self):
            return ("国内株式取引 注文照会 注文一覧\n"
                    "1件中1～1件表示\n"
                    "5391 約定 11/06 10:11:30 商船三井\n"
                    "9104 東証(SOR)\n"
                    "2026/11/06 22:45\n")

    class Reader:
        def __init__(self, path):
            self.pages = [Page()]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    result = parse_orders_pdf(tmp_path / "orders.pdf")
    assert result["orders_count"] == 1
    assert result["open_orders_count"] == 0
    assert result["items"][0]["code"] == "9104"
    assert result["source_as_of_method"] == "pdf_footer_explicit_year"


def test_orders_pdf_rejects_incomplete_order_rows(tmp_path, monkeypatch):
    import pypdf
    import pytest
    from src.private_account_import import parse_orders_pdf

    class Page:
        def extract_text(self):
            return "注文照会 注文一覧\n1件中1～1件表示\n2026/11/06 22:45"

    class Reader:
        def __init__(self, path):
            self.pages = [Page()]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    with pytest.raises(ValueError, match="incomplete"):
        parse_orders_pdf(tmp_path / "orders.pdf")


def test_orders_pdf_real_layout_wrapped_headers_and_footer(tmp_path, monkeypatch):
    """Synthetic values, layout modeled on the Rakuten two-page inquiry PDF."""
    import pypdf
    from src.private_account_import import parse_orders_pdf

    class Page:
        def __init__(self, value):
            self.value = value
        def extract_text(self):
            return self.value

    class Reader:
        def __init__(self, path):
            self.pages = [
                Page("注文照会\n注文一覧\n11/06 22:45\n1件中1～1件表示\n"
                     "注文\n番号\n(ｱﾙｺﾞ)\n状況 注文日時\n"
                     "5391 約定 11/06 10:11:30 商船三井\n"
                     "9104 東証(SOR)\n現物 売付\n100 成行 657,820\n"
                     "市場執行済 本日中 特定 100 6,578.2 0\n"
                     "詳細 2026/11/06 通常注文 - 6,516.0\n"
                     "2026/11/06 22:45\n1 / 2 ページ"),
                Page("国内株式取引 注文照会・訂正・取消\n2026/11/06 22:45\n2 / 2 ページ"),
            ]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    result = parse_orders_pdf(tmp_path / "orders.pdf")
    assert result["orders_count"] == 1
    assert result["open_orders_count"] == 0
    assert result["items"][0]["order_id"] == "5391"
    assert result["items"][0]["code"] == "9104"
    assert result["source_as_of"] == "2026-11-06T22:45:00+09:00"
