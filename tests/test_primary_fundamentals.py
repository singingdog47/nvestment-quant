import io
import zipfile
from types import SimpleNamespace

import pandas as pd

from company_intel.primary_fundamentals import (
    extract_csv_zip, collect_primary_fundamentals, write_primary_fundamentals,
)
from company_intel.snapshot import _merge_existing


def make_zip(rows):
    data = "\t".join(["要素ID", "コンテキストID", "ユニットID", "値"]) + "\n"
    data += "\n".join("\t".join(row) for row in rows) + "\n"
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        archive.writestr("XBRL_TO_CSV/facts.csv", data.encode("utf-16"))
    return out.getvalue()


def test_primary_fact_parser_rejects_other_periods_members_and_units():
    content = make_zip([
        ["jpcrp_cor:NetSales", "Prior1YearDuration", "JPY", "999"],
        ["jpcrp_cor:NetSales", "CurrentYearDuration_NonConsolidatedMember", "JPY", "888"],
        ["jpcrp_cor:NetSales", "CurrentYearDuration", "USD", "777"],
        ["jpcrp_cor:NetSales", "CurrentYearDuration", "JPY", "1200000"],
        ["jpcrp_cor:OperatingIncome", "CurrentYearDuration", "JPY", "150000"],
        ["jpcrp_cor:Assets", "CurrentYearInstant", "JPY", "4900000"],
        ["jpcrp_cor:Assets", "Prior1YearInstant", "JPY", "123"],
    ])
    result = extract_csv_zip(content)
    assert result == {"net_sales_jpy": 1200000, "operating_income_jpy": 150000, "assets_jpy": 4900000}


def test_conflicting_duplicate_primary_value_does_not_count():
    content = make_zip([
        ["jpcrp_cor:NetSales", "CurrentYearDuration", "JPY", "100"],
        ["jpcrp_cor:NetSales", "CurrentYearDuration", "JPY", "101"],
    ])
    assert extract_csv_zip(content) == {}


def test_primary_fundamentals_provenance_and_snapshot_gate(tmp_path, monkeypatch):
    event = SimpleNamespace(
        source="EDINET", source_url="https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID=S1234567",
        title="有価証券報告書", code="2585", ticker="2585.T", event_date="2026-10-02",
    )
    content = make_zip([["jpcrp_cor:NetSales", "CurrentYearDuration", "JPY", "42000"]])

    class Response:
        def __init__(self, payload):
            self.content = payload
        def raise_for_status(self):
            return None

    class Session:
        def get(self, url, params, timeout):
            assert url.endswith("S1234567")
            assert params["type"] == 5
            return Response(content)

    monkeypatch.setenv("EDINET_API_KEY", "test_key")
    file_path = tmp_path / "data" / "fundamentals_latest.csv"
    frame, health = collect_primary_fundamentals([event], file_path, session=Session())
    assert health["new_companies"] == 1
    assert frame.loc[0, "net_sales_jpy"] == 42000
    write_primary_fundamentals(frame, file_path)
    monkeypatch.chdir(tmp_path)
    targets = pd.DataFrame([
        {"market": "JP", "code": "2585", "ticker": "2585.T", "name": "Life Drink", "source": "watchlist"},
        {"market": "JP", "code": "8766", "ticker": "8766.T", "name": "Tokyo Marine", "source": "watchlist"},
    ])
    targets["fundamental_status"] = "missing"
    merged = _merge_existing(targets)
    assert merged.set_index("code").loc["2585", "fundamental_status"] == "ok"
    assert merged.set_index("code").loc["8766", "fundamental_status"] == "missing"


def test_source_metadata_alone_cannot_raise_coverage(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "data" / "fundamentals_latest.csv"
    path.parent.mkdir()
    pd.DataFrame([{
        "code": "2585", "source": "EDINET", "source_tier": "primary",
        "document_id": "S1234567", "source_url": "https://example.org",
        "filed_date": "2026-10-02", "currency_unit": "JPY",
        "period_context": "CurrentYear",
    }]).to_csv(path, index=False)
    base = pd.DataFrame([{"code": "2585", "fundamental_status": "missing"}])
    assert _merge_existing(base).loc[0, "fundamental_status"] == "missing"
