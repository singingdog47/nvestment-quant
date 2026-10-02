from datetime import date
from types import SimpleNamespace

import pandas as pd

from company_intel.backfill import scan_historical_edinet, audit_primary_coverage


def _targets():
    return pd.DataFrame([
        {"market": "JP", "code": "2585", "ticker": "2585.T", "name": "Life Drink", "source": "watchlist"},
        {"market": "JP", "code": "8766", "ticker": "8766.T", "name": "Tokyo Marine", "source": "watchlist"},
        {"market": "US", "code": "CARE", "ticker": "CARE", "name": "US Bank", "source": "screening"},
    ])


class Session:
    def __init__(self, fail=None):
        self.calls = []
        self.fail = fail

    def get(self, url, params, timeout):
        day = params["date"]
        self.calls.append(day)
        if day == self.fail:
            raise RuntimeError("temporary EDINET outage")
        return SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "results": [
                    {"secCode": "25850", "docID": "S1001234", "docDescription": "有価証券報告書"},
                    {"secCode": "87660", "docID": "S1002345", "docDescription": "訂正有価証券報告書"},
                    {"secCode": "87660", "docID": "S1003456", "docDescription": "変更報告書"},
                    {"secCode": "99990", "docID": "S1004567", "docDescription": "有価証券報告書"},
                ] if day == "2026-09-25" else []
            },
        )


def test_backfill_checkpoint_and_conservative_filing_filter(tmp_path, monkeypatch):
    monkeypatch.setenv("EDINET_API_KEY", "mock")
    checkpoint = tmp_path / "cursor.json"
    http = Session()
    events, result = scan_historical_edinet(
        _targets(), checkpoint, today=date(2026, 10, 2), days_per_run=2,
        lookback_days=12, session=http,
    )
    assert http.calls == ["2026-09-25", "2026-09-24"]
    assert result["next_date"] == "2026-09-23"
    assert len(events) == 1
    assert events[0].code == "2585"
    events2, result2 = scan_historical_edinet(
        _targets(), checkpoint, today=date(2026, 10, 2), days_per_run=2,
        lookback_days=12, session=http,
    )
    assert http.calls[-2:] == ["2026-09-23", "2026-09-22"]
    assert result2["next_date"] == "2026-09-21"


def test_failed_date_is_retried_not_skipped(tmp_path, monkeypatch):
    monkeypatch.setenv("EDINET_API_KEY", "mock")
    checkpoint = tmp_path / "cursor.json"
    failing = Session(fail="2026-09-24")
    _, first = scan_historical_edinet(
        _targets(), checkpoint, today=date(2026, 10, 2),
        days_per_run=3, lookback_days=12, session=failing,
    )
    assert first["status"] == "partial"
    assert first["next_date"] == "2026-09-24"
    _, second = scan_historical_edinet(
        _targets(), checkpoint, today=date(2026, 10, 2),
        days_per_run=1, lookback_days=12, session=Session(),
    )
    assert second["next_date"] == "2026-09-23"


def test_audit_uses_japanese_target_denominator_and_metric_coverage():
    p = pd.DataFrame([{
        "code": "2585", "document_id": "S1001234", "filed_date": "2026-09-25",
        "net_sales_jpy": 1000, "assets_jpy": 9000,
    }])
    rows, report = audit_primary_coverage(_targets(), p)
    assert report["target_count"] == 2
    assert report["companies_with_any_primary_metric"] == 1
    assert report["companies_with_all_six_metrics"] == 0
    assert report["metric_counts"]["net_sales_jpy"] == 1
    assert report["metric_counts"]["operating_cash_flow_jpy"] == 0
    assert rows.set_index("code").loc["2585", "status"] == "partial"
    assert rows.set_index("code").loc["8766", "status"] == "missing"
