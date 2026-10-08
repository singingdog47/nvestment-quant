import csv
from datetime import date
from pathlib import Path

from scripts.ai_credit_monitor import evaluate, forward_study, load_panel


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["date", "entity", "group", "cds_5y_bp", "source", "asof_utc"])
        writer.writeheader()
        writer.writerows(rows)


def sample_rows(day="2026-10-01"):
    return [
        {"date": day, "entity": f"AI{i}", "group": "ai", "cds_5y_bp": str(100 + i),
         "source": "licensed_test_fixture", "asof_utc": day + "T21:00:00Z"}
        for i in range(3)
    ] + [
        {"date": day, "entity": f"CONTROL{i}", "group": "control", "cds_5y_bp": str(50 + i),
         "source": "licensed_test_fixture", "asof_utc": day + "T21:00:00Z"}
        for i in range(3)
    ]


def test_absent_source_fails_closed(tmp_path):
    panel, warnings = load_panel(tmp_path / "absent.csv")
    result = evaluate(panel, warnings)
    assert result["actionable"] is False
    assert result["data_status"] == "unavailable"
    assert "CDS_SOURCE_MISSING" in warnings


def test_relative_spread_uses_median(tmp_path):
    file = tmp_path / "cds.csv"
    write_csv(file, sample_rows())
    panel, warnings = load_panel(file, today=date(2026, 10, 8))
    assert not warnings
    assert panel[0]["ai_minus_control_bp"] == 50
    assert evaluate(panel, warnings)["assessment"] == "observing_not_enough_history"


def test_rejects_future_duplicates_and_incomplete_panels(tmp_path):
    file = tmp_path / "cds.csv"
    rows = sample_rows()
    rows += [rows[0].copy()]
    rows += sample_rows("2026-11-01")
    write_csv(file, rows)
    panel, warnings = load_panel(file, today=date(2026, 10, 8))
    assert len(panel) == 1
    assert any(w.startswith("REJECT_ROW_") for w in warnings)


def test_stale_never_elevates_to_signal(tmp_path):
    file = tmp_path / "cds.csv"
    write_csv(file, sample_rows())
    panel, warnings = load_panel(file, today=date(2026, 10, 28), max_age_days=7)
    result = evaluate(panel, warnings)
    assert result["data_status"] == "unavailable"
    assert result["trade_signal"] is False


def test_forward_study_avoids_unrealized_and_same_day(tmp_path):
    file = tmp_path / "prices.csv"
    with open(file, "w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["date", "close"])
        for d, p in zip(range(1, 9), [100, 110, 100, 100, 100, 95, 90, 85]):
            writer.writerow([f"2026-10-{d:02d}", p])
    obs = [{"date": "2026-10-01", "ai_minus_control_bp": 50},
           {"date": "2026-10-07", "ai_minus_control_bp": 55}]
    study = forward_study(obs, file, horizon=5)
    assert len(study["samples"]) == 1
    assert study["samples"][0]["forward_return"] == -0.05
