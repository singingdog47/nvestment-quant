import csv
from pathlib import Path

from validation.evaluate import _append_summary, _benchmark_symbol


def test_benchmark_assignment_is_deterministic():
    assert _benchmark_symbol({"market": "JP"}, "7203.T") == "1306.T"
    assert _benchmark_symbol({"market": "US"}, "MSFT") == "SPY"
    assert _benchmark_symbol({"market": ""}, "9984.T") == "1306.T"
    assert _benchmark_symbol({"market": "UNKNOWN"}, "ABC") is None


def test_outcomes_schema_migrates_without_losing_old_rows(tmp_path: Path):
    d = tmp_path / "data/validation"
    d.mkdir(parents=True)
    out = d / "outcomes.csv"
    out.write_text(
        "decision_id,captured_at,market_regime,recommended_action,horizon,symbol,rank,return,max_up,max_down,evaluated_price_date,model_version\n"
        "old,2026-01-01T00:00:00+00:00,NEUTRAL,REVIEW,1w,7203.T,1,0.01,0.02,-0.01,2026-01-08,1.7.0\n",
        encoding="utf-8",
    )
    _append_summary(
        tmp_path,
        [
            {
                "decision_id": "new",
                "captured_at": "2026-01-02T00:00:00+00:00",
                "market_regime": "RISK-ON",
                "recommended_action": "SELECTIVE_BUY",
                "horizon": "1w",
                "symbol": "6758.T",
                "rank": 1,
                "return": 0.03,
                "benchmark_symbol": "1306.T",
                "benchmark_return": 0.01,
                "excess_return": 0.02,
                "max_up": 0.04,
                "max_down": -0.01,
                "evaluated_price_date": "2026-01-09",
                "model_version": "2.1.0",
            }
        ],
    )
    with out.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert "excess_return" in rows[0]
    assert rows[0]["decision_id"] == "old"
    assert rows[0]["excess_return"] == ""
    assert rows[1]["excess_return"] == "0.02"
