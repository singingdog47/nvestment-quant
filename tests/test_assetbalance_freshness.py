from pathlib import Path
from types import SimpleNamespace
import pandas as pd

from run_portfolio_risk import _build_latest_portfolio


def test_latest_assetbalance_uses_brokerage_export_time_not_upload_time(tmp_path, monkeypatch):
    older = tmp_path / "assetbalance(all)_20261002_125052.csv"
    newer = tmp_path / "assetbalance(all)_20261002_154506.csv"
    older.write_bytes(b"older")
    newer.write_bytes(b"newer")
    import run_portfolio_risk
    monkeypatch.setattr(run_portfolio_risk, "_target_date", lambda: None)
    def parse(raw):
        value = 200 if raw == b"newer" else 100
        return SimpleNamespace(
            portfolio=pd.DataFrame({"market_value": [value], "weight": [1.0]}),
            source_encoding="utf-8", rows_seen=1, rows_kept=1
        )
    monkeypatch.setattr(run_portfolio_risk, "parse_rakuten_csv_bytes", parse)
    candidates = [
        (older, {"name": older.name, "modifiedTime": "2026-10-02T10:00:00Z"}),
        (newer, {"name": newer.name, "modifiedTime": "2026-10-02T08:00:00Z"}),
    ]
    path, manifest = _build_latest_portfolio(tmp_path, candidates)
    assert manifest["source_file"] == newer.name
    assert manifest["source_as_of"].startswith("2026-10-02T15:45:06")
    assert float(pd.read_csv(path)["market_value"].iloc[0]) == 200
