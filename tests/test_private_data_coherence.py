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
            return ("国内株式取引 注文照会 注文一覧 注文状況 すべての注文 注文種類 現物のみ\n"
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
            return "注文照会 注文一覧 注文状況 すべての注文 注文種類 現物のみ\n1件中1～1件表示\n2026/11/06 22:45"

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
                Page("注文照会\n注文一覧\n注文状況 すべての注文\n注文種類 現物のみ\n11/06 22:45\n1件中1～1件表示\n"
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


def test_account_summary_prefers_export_time_over_later_upload(tmp_path, monkeypatch):
    from src import run_portfolio_risk as runner

    monkeypatch.setattr(
        runner, "parse_account_summary_bytes",
        lambda raw: {"total_assets_jpy": int(raw.decode())},
    )
    old = tmp_path / "old.csv"
    new = tmp_path / "new.csv"
    old.write_bytes(b"20000000")
    new.write_bytes(b"19000000")
    result = runner._build_latest_account_inputs(tmp_path, [
        (old, {"name": "assetbalance(all)_20261106_155900.csv", "modifiedTime": "2026-11-06T14:00:00Z"}),
        (new, {"name": "assetbalance(all)_20261106_225114.csv", "modifiedTime": "2026-11-06T13:00:00Z"}),
    ])
    summary = result["inputs"]["account_summary"]
    assert summary["source_file"] == "assetbalance(all)_20261106_225114.csv"
    assert summary["total_assets_jpy"] == 19000000


def test_account_summary_compares_offsets_as_instants(tmp_path, monkeypatch):
    from src import run_portfolio_risk as runner

    def fake_summary(raw):
        return {"total_assets_jpy": float(raw.decode()), "invested_assets_jpy": 100.0}

    monkeypatch.setattr(runner, "parse_account_summary_bytes", fake_summary)
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    a.write_bytes(b"1")
    b.write_bytes(b"2")
    monkeypatch.setattr(runner, "source_as_of", lambda name, modified: (
        "2026-11-06T22:00:00+09:00" if name == "a.csv" else "2026-11-06T14:00:00+00:00",
        "filename_embedded_export_time",
    ))
    result = runner._build_latest_account_inputs(tmp_path, [
        (a, {"name": "a.csv"}), (b, {"name": "b.csv"}),
    ])
    assert result["inputs"]["account_summary"]["total_assets_jpy"] == 2.0
    assert result["selection_policy"] == "verified_brokerage_observation_time_then_fallback"


def test_shared_state_hides_unverified_account_values(tmp_path):
    from src.investment_state import build_investment_state

    account_inputs = {"status": "partial", "inputs": {
        "account_summary": {
            "total_assets_jpy": 99999999,
            "invested_assets_jpy": 88888888,
            "daily_change_jpy": -12345,
            "daily_change_pct": -1.2,
            "source_as_of": "2026-11-01T10:00:00+09:00",
            "source_as_of_method": "filename_embedded_export_time",
        }
    }}
    manifest = {"source_as_of": "2026-11-06T22:51:14+09:00",
                "source_as_of_method": "filename_embedded_export_time"}
    state = build_investment_state(
        account_inputs, manifest, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert all(value is None for value in state["portfolio"].values())
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["open_orders"]["count"] is None
    assert state["quality"]["data_coherence"]["decision_safe"] is False


def test_orders_pdf_rejects_partial_pagination(tmp_path, monkeypatch):
    import pypdf
    import pytest
    from src.private_account_import import parse_orders_pdf

    class Page:
        def extract_text(self):
            return ("注文照会 注文一覧 注文状況 すべての注文 注文種類 現物のみ\n2件中1～1件表示\n"
                    "5391 約定 11/06 10:11:30 商船三井\n"
                    "9104 東証(SOR)\n2026/11/06 22:45\n")

    class Reader:
        def __init__(self, path):
            self.pages = [Page()]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    with pytest.raises(ValueError, match="pagination incomplete"):
        parse_orders_pdf(tmp_path / "orders.pdf")


def test_orders_pdf_rejects_filtered_status(tmp_path, monkeypatch):
    import pypdf
    import pytest
    from src.private_account_import import parse_orders_pdf

    class Page:
        def extract_text(self):
            return ("注文照会 注文一覧 注文状況 約定のみ 注文種類 現物のみ\n"
                    "1件中1～1件表示\n"
                    "5391 約定 11/06 10:11:30 商船三井\n"
                    "9104 東証(SOR)\n2026/11/06 22:45\n")

    class Reader:
        def __init__(self, path):
            self.pages = [Page()]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    with pytest.raises(ValueError, match="status filter"):
        parse_orders_pdf(tmp_path / "orders.pdf")


def test_unknown_timestamp_provenance_fails_closed():
    from datetime import datetime, timezone
    from src.private_data_coherence import classify_private_inputs

    timestamp = "2026-11-06T22:00:00+09:00"
    now = datetime(2026, 11, 6, 14, 0, tzinfo=timezone.utc)
    inputs = {"inputs": {
        kind: {"source_as_of": timestamp,
               "source_as_of_method": "unrecognized_source"}
        for kind in ("account_summary", "orders", "buying_power")
    }}
    manifest = {"source_as_of": timestamp,
                "source_as_of_method": "unrecognized_source"}
    verdict = classify_private_inputs(manifest, inputs, now=now)
    assert verdict["decision_safe"] is False
    assert "PORTFOLIO_TIMESTAMP_UNVERIFIED" in verdict["portfolio_reasons"]
    assert all(v["status"] == "UNVERIFIED" for v in verdict["inputs"].values())


def test_buying_power_pdf_uses_explicit_footer_year(tmp_path, monkeypatch):
    import pypdf
    from src.private_account_import import parse_buying_power_pdf

    class Page:
        def extract_text(self):
            return ("現物買付可能額 2,863,480 円\n"
                    "買付可能額（本日） 11/06 22:46\n"
                    "https://example.invalid/ 2026/11/06 22:46\n")

    class Reader:
        def __init__(self, path):
            self.pages = [Page()]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    parsed = parse_buying_power_pdf(tmp_path / "buying.pdf")
    assert parsed["cash_buying_power_jpy"] == 2863480
    assert parsed["source_as_of"] == "2026-11-06T22:46:00+09:00"
    assert parsed["source_as_of_method"] == "pdf_footer_explicit_year"


def test_buying_power_pdf_rejects_conflicting_footer_dates(tmp_path, monkeypatch):
    import pypdf
    import pytest
    from src.private_account_import import parse_buying_power_pdf

    class Page:
        def extract_text(self):
            return ("現物買付可能額 2,863,480 円\n"
                    "2026/11/06 22:46\n2026/11/05 22:46\n")

    class Reader:
        def __init__(self, path):
            self.pages = [Page()]

    monkeypatch.setattr(pypdf, "PdfReader", Reader)
    with pytest.raises(ValueError, match="Conflicting PDF footer timestamps"):
        parse_buying_power_pdf(tmp_path / "buying.pdf")


def test_weekend_rakuten_account_summary_rows():
    from src.private_account_import import parse_account_summary_bytes

    # Minimal anonymized fixture retaining the November 6 export's row format.
    raw = (
        '"資産合計","19,643,918","-1,851,576","-8.61"\n'
        '"保有商品の評価額合計","18,134,621","-1,665,951","-8.41"\n'
        '"楽天銀行普通預金残高","2,164,211"\n'
    ).encode("utf-8")
    result = parse_account_summary_bytes(raw)
    assert result["total_assets_jpy"] == 19643918
    assert result["invested_assets_jpy"] == 18134621
    assert result["daily_change_jpy"] == -1851576
    assert result["daily_change_pct"] == -8.61


def test_friday_snapshot_cannot_authorize_monday_trading():
    friday = {"source_as_of": "2026-11-06T22:51:14+09:00",
              "source_as_of_method": "filename_embedded_export_time"}
    account = {"inputs": {
        "account_summary": {"source_as_of": "2026-11-06T22:51:14+09:00",
                            "source_as_of_method": "filename_embedded_export_time"},
        "orders": {"source_as_of": "2026-11-06T22:45:00+09:00",
                   "source_as_of_method": "pdf_footer_explicit_year"},
        "buying_power": {"source_as_of": "2026-11-06T22:46:00+09:00",
                         "source_as_of_method": "pdf_footer_explicit_year"},
    }}
    monday = datetime.fromisoformat("2026-11-09T09:00:00+09:00")
    result = classify_private_inputs(friday, account, now=monday)
    assert result["decision_safe"] is False
    assert "PORTFOLIO_STALE_OR_FUTURE" in result["portfolio_reasons"]
    assert result["inputs"]["buying_power"]["status"] == "UNVERIFIED"


def test_actual_rakuten_margin_and_bank_label_variants():
    from src.private_account_import import parse_account_summary_bytes

    raw = ("資産合計,19,643,918\n").encode("utf-8")
    # Use quoted amounts, as in the brokerage CSV export.
    raw = ('資産合計,"19,643,918"\n'
           '保有商品の評価額合計,"18,134,621"\n'
           '国内株式信用保証金,"886,593"\n'
           'FX証拠金（純資産）,"171,991"\n'
           '楽天銀行普通預金残高,"2,164,211"\n').encode("utf-8")
    parsed = parse_account_summary_bytes(raw)
    assert parsed["margin_collateral_jpy"] == 886593
    assert parsed["fx_margin_net_assets_jpy"] == 171991
    assert parsed["rakuten_bank_balance_jpy"] == 2164211


def test_stale_evidence_allows_analysis_but_never_execution(tmp_path):
    from src.investment_state import build_investment_state
    manifest = {"source_as_of": "2026-11-06T22:51:14+09:00",
                "source_as_of_method": "filename_embedded_export_time"}
    state = build_investment_state(
        {"inputs": {}}, manifest, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    capabilities = state["decision_capabilities"]
    assert capabilities["analysis_allowed"] is True
    assert capabilities["recommendation_allowed"] is True
    assert capabilities["execution_ready"] is False
    assert "ACCOUNT_WIDE_ORDERS_NOT_VERIFIED" in capabilities["execution_blockers"]
    assert state["capital"]["deployable_cash_jpy"] is None


def test_unknown_portfolio_timestamp_cannot_be_treated_as_evidence(tmp_path):
    from src.investment_state import build_investment_state
    state = build_investment_state(
        {"inputs": {}}, {}, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert state["decision_capabilities"]["analysis_allowed"] is False
    assert state["decision_capabilities"]["execution_ready"] is False


def test_partially_filled_order_not_silently_treated_as_closed(tmp_path):
    from src.investment_state import build_investment_state
    from datetime import datetime, timezone
    stamp = datetime.now(timezone.utc).isoformat()
    manifest = {"source_as_of": stamp, "source_as_of_method": "filename_embedded_export_time"}
    inputs = {"inputs": {"orders": {"source_as_of": stamp,
        "source_as_of_method": "pdf_footer_explicit_year", "data_status": "ok",
        "items": [{"order_id": "123", "status": "一部約定", "code": "1234"}]}}}
    state = build_investment_state(inputs, manifest, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv")
    assert state["open_orders"]["count"] == 1
    assert state["open_orders"]["account_wide_complete"] is False
    assert state["decision_capabilities"]["execution_ready"] is False


def test_order_csv_partial_fill_is_open():
    from src.private_account_import import parse_orders_bytes
    raw = ("注文番号,銘柄コード,銘柄名,状況,売買,注文数量,約定数量,注文単価\n"
           "12345,1234,テスト銘柄,一部約定,買,100,30,500\n").encode("utf-8")
    parsed = parse_orders_bytes(raw)
    assert parsed["orders_count"] == 1
    assert parsed["open_orders_count"] == 1


def test_verified_buying_power_is_not_discretionary_cash(tmp_path):
    from src.investment_state import build_investment_state
    stamp = datetime.now(timezone.utc).isoformat()
    manifest = {"source_as_of": stamp, "source_as_of_method": "filename_embedded_export_time"}
    values = inputs(as_of=stamp)
    values["inputs"]["buying_power"]["cash_buying_power_jpy"] = 2863480
    state = build_investment_state(values, manifest, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv")
    assert state["capital"]["brokerage_cash_buying_power_jpy"] == 2863480
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["capital"]["buying_power_is_deployable_cash"] is False
    assert "DISCRETIONARY_CASH_NOT_RECONCILED" in state["decision_capabilities"]["execution_blockers"]
    assert state["decision_capabilities"]["execution_ready"] is False
