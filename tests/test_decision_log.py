import json
from pathlib import Path

from src.validation.decision_log import capture_decision_snapshot


def test_capture_decision_snapshot(tmp_path: Path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data/regime").mkdir()
    (tmp_path / "data/intelligence").mkdir()

    (tmp_path / "data/decision_context_latest.json").write_text(
        json.dumps(
            {
                "quality": {"quality_score": 0.3, "actionable": False},
                "market_regime": {
                    "regime_label": "CONSTRUCTIVE",
                    "regime_score": 67,
                    "regime_flags": [],
                    "components": {"trend": 80},
                    "evidence": {"vix": 15},
                },
                "policy_guardrails": {
                    "decision_gate": "BLOCK_DATA_QUALITY",
                    "absolute_defense_cash_jpy": 500000,
                    "cash_target_range": [0.08, 0.12],
                    "max_single_stock_weight": 0.05,
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "data/screening_latest.csv").write_text(
        "market,code,ticker,name,market_rank,price,value_score,quality_score\n"
        "JP,8001,8001.T,ITOCHU,1,2000,80,75\n",
        encoding="utf-8",
    )

    out = capture_decision_snapshot(tmp_path, model_version="test")
    record = json.loads(out.read_text(encoding="utf-8"))

    assert record["market_regime"] == "CONSTRUCTIVE"
    assert record["recommended_action"] == "WAIT_DATA_QUALITY"
    assert record["top_screening"][0]["ticker"] == "8001.T"
    assert record["top_screening"][0]["factors"]["value_score"] == 80.0
    assert record["actual_human_action"] is None
    assert record["model_version"] == "test"
    assert record["decision_id"]
