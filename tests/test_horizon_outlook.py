from __future__ import annotations

import csv
import json
from datetime import datetime, timezone

from horizon_outlook import build_outlook, grade_hypotheses, run


NOW = datetime(2026, 10, 16, 12, 35, tzinfo=timezone.utc)


def _regime():
    return {
        "date_jst": "2026-10-16",
        "data_status": "ok",
        "actionable": True,
        "regime_label": "CONSTRUCTIVE",
        "regime_score": 62.68,
        "treasury_volatility_shock_flag": True,
    }


def _supply():
    return {
        "observed_date_jst": "2026-10-16",
        "data_status": "partial",
        "coverage": {"current_vs_average_volume": 0.7},
    }


def _observations():
    return [{
        "market": "JP", "code": "6701", "ticker": "6701.T", "name": "NEC",
        "observed_date": "2026-10-16",
        "data_status": "ok", "confidence": "0.7",
        "current_volume_ratio_30d": "1.8",
        "context_flags": "VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION",
        "price_as_of": "2026-10-16T06:30:00+00:00",
    }]


def _screening():
    return [{"market": "JP", "code": "6701", "ticker": "6701.T", "name": "NEC",
             "market_rank": "1", "research_status": "research_candidate"}]


def test_three_horizons_and_immutable_research_prior():
    result = build_outlook(_regime(), _supply(), _observations(), _screening(), NOW)
    assert [item["name"] for item in result["horizons"]] == ["short", "medium", "long"]
    assert result["horizons"][0]["view"] == "TWO_WAY_WITH_RATES_VOLATILITY_RISK"
    assert result["horizons"][2]["view"] == "FUNDAMENTALS_NOT_ESTABLISHED"
    assert len(result["prospective_hypotheses"]) == 1
    hypothesis = result["prospective_hypotheses"][0]
    assert hypothesis["symbol"] == "6701.T"
    assert hypothesis["benchmark_symbol"] == "1306.T"
    assert hypothesis["expected_sign"] == "positive"
    assert hypothesis["probability"] == 0.55
    assert hypothesis["execution"] == "RESEARCH_ONLY_NO_AUTO_TRADE"
    assert result["source_status"]["private_portfolio_included"] is False


def test_missing_or_stale_inputs_do_not_generate_forecasts():
    reg = _regime()
    reg["date_jst"] = "2026-10-15"
    out = build_outlook(reg, _supply(), _observations(), _screening(), NOW)
    assert out["prospective_hypotheses"] == []
    assert out["horizons"][0]["view"] == "INSUFFICIENT_DATA"
    fresh = _regime()
    old = _supply()
    old["observed_date_jst"] = "2026-10-15"
    out = build_outlook(fresh, old, _observations(), _screening(), NOW)
    assert out["prospective_hypotheses"] == []


def test_price_without_volume_does_not_imply_net_flow():
    rows = _observations()
    rows[0]["current_volume_ratio_30d"] = "0.8"
    out = build_outlook(_regime(), _supply(), rows, _screening(), NOW)
    assert out["prospective_hypotheses"] == []


def test_brier_grade_uses_later_existing_validation_outcome_only():
    h = build_outlook(_regime(), _supply(), _observations(), _screening(), NOW)["prospective_hypotheses"]
    early = [{"symbol": "6701.T", "horizon": "1w",
              "captured_at": "2026-10-16T12:00:00+00:00", "excess_return": "0.05"}]
    assert grade_hypotheses(h, early)["pending_n"] == 1
    later = [{"symbol": "6701.T", "horizon": "1w",
              "captured_at": "2026-10-16T12:40:00+00:00", "excess_return": "0.02"}]
    result = grade_hypotheses(h, later)
    assert result["graded_n"] == 1
    assert result["accuracy"] == 1.0
    assert abs(result["mean_brier"] - 0.2025) < 1e-10
    assert result["calibrated"] is False


def test_run_writes_outputs_and_never_revises_same_day_archive(tmp_path):
    for rel, payload in (
        ("data/regime/market_regime_latest.json", _regime()),
        ("data/supply_demand/supply_demand_summary_latest.json", _supply()),
    ):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
    for rel, rows in (
        ("data/supply_demand/supply_demand_latest.csv", _observations()),
        ("data/screening_latest.csv", _screening()),
    ):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    first = run(tmp_path, now=NOW)
    original = first["archive"].read_text(encoding="utf-8")
    assert len(json.loads(original)["prospective_hypotheses"]) == 1
    updated = _observations()
    updated[0]["context_flags"] = "NO_EXCEPTION"
    path = tmp_path / "data/supply_demand/supply_demand_latest.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(updated[0]))
        writer.writeheader()
        writer.writerows(updated)
    second = run(tmp_path, now=NOW)
    assert second["archive"].read_text(encoding="utf-8") == original
    assert json.loads(second["latest"].read_text(encoding="utf-8"))["prospective_hypotheses"] == []
    assert json.loads(second["learning"].read_text(encoding="utf-8"))["pending_n"] == 1
