import pandas as pd
import requests

from market_regime.common import now_iso
from market_regime.coverage import build_data_coverage
from market_regime.fred import fetch_fred
from market_regime.jpx import _validate_frame


def test_fred_network_failure_reuses_recent_cache_as_stale(monkeypatch, tmp_path):
    cache_path=tmp_path/"fred_latest.csv"
    pd.DataFrame([
        {
            "series":"HY_OAS",
            "fred_id":"BAMLH0A0HYM2",
            "date":"2026-08-21",
            "value":2.75,
            "previous":2.73,
            "change":0.02,
            "source":"FRED",
            "source_url":"https://fred.example/cache",
            "fetched_at":now_iso(),
            "data_status":"ok",
        }
    ]).to_csv(cache_path,index=False)

    def fail(*args,**kwargs):
        raise requests.Timeout("temporary timeout")

    monkeypatch.setattr("market_regime.fred._get_with_retry",fail)
    frame,health=fetch_fred(
        {"HY_OAS":"BAMLH0A0HYM2"},
        cache_path=cache_path,
        max_cache_age_days=14,
    )
    assert frame.iloc[0]["data_status"] == "stale"
    assert frame.iloc[0]["value"] == 2.75
    assert health[0]["status"] == "stale"
    assert health[0]["transport_status"] == "error"
    assert health[0]["content_status"] == "cached_valid"


def test_fred_http_success_with_invalid_payload_is_partial(monkeypatch):
    class Response:
        text="DATE\n2026-08-21\n"
        url="https://fred.example/invalid"

    monkeypatch.setattr("market_regime.fred._get_with_retry",lambda *a,**k:Response())
    frame,health=fetch_fred({"HY_OAS":"BAMLH0A0HYM2"})
    assert frame.empty
    assert health[0]["status"] == "partial"
    assert health[0]["transport_status"] == "ok"
    assert health[0]["content_status"] == "invalid"


def test_jpx_date_only_payload_fails_content_validation():
    frame,report=_validate_frame(
        "short_selling",
        pd.DataFrame({"Date":["2026-08-20","2026-08-21"]}),
    )
    assert len(frame) == 2
    assert report["valid"] is False
    assert "columns<2" in report["issues"]
    assert "numeric_values<1" in report["issues"]


def test_jpx_table_with_numeric_observations_is_valid():
    _,report=_validate_frame(
        "short_selling",
        pd.DataFrame({"Date":["2026-08-20","2026-08-21"],"Ratio":["41.2%","42.1%"]}),
    )
    assert report["valid"] is True
    assert report["numeric_values"] == 2


def test_coverage_manifest_preserves_missing_partial_stale_and_planned_sources():
    manifest=build_data_coverage(
        [
            {"source":"FRED:HY","status":"stale","records":1},
            {"source":"JPX:short_selling","status":"partial","records":15},
            {"source":"CFTC:COT","status":"error","records":0},
        ],
        generated_at="2026-08-24T09:30:00+00:00",
        expected_sources=[
            {"source":"FRED:HY","required":True},
            {"source":"FRED:IG","required":True},
        ],
        not_implemented=[{"source":"MOVE","description":"planned"}],
        files=[{"path":"data/regime/fred_latest.csv","status":"stale"}],
    )
    statuses={row["source"]:row["status"] for row in manifest["sources"]}
    assert manifest["data_status"] == "partial"
    assert statuses == {
        "FRED:HY":"stale",
        "JPX:short_selling":"partial",
        "CFTC:COT":"missing",
        "FRED:IG":"missing",
        "MOVE":"not_implemented",
    }
    assert set(manifest["summary"]["critical_missing"]) == {"FRED:HY","FRED:IG"}

