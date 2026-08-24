import json
from pathlib import Path

from mobile_brief import build_mobile_brief


def _public_fixture(root: Path) -> None:
    (root / "data/regime").mkdir(parents=True)
    (root / "data/alerts").mkdir(parents=True)
    (root / "data/decision_context_latest.json").write_text(
        json.dumps({
            "quality": {"actionable": True, "quality_score": 0.745},
            "policy_guardrails": {"decision_gate": "OPEN_FOR_ANALYSIS"},
        }),
        encoding="utf-8",
    )
    (root / "data/quality_report.json").write_text(
        json.dumps({"universe_count": 9584, "scored_count": 5364, "price_missing_rate": 0.094}),
        encoding="utf-8",
    )
    (root / "data/regime/market_regime_latest.json").write_text(
        json.dumps({
            "regime_label": "CONSTRUCTIVE",
            "regime_score": 67.8,
            "components": {"liquidity": 37.2},
            "evidence": {"vix": 15.1},
        }),
        encoding="utf-8",
    )
    (root / "data/regime/market_regime_history.csv").write_text(
        "generated_at,score,label,component_trend,component_stress,component_participation,component_liquidity,component_positioning\n"
        "2026-08-23,67.8,CONSTRUCTIVE,80,84,56,43,48\n"
        "2026-08-24,67.7,CONSTRUCTIVE,82,84,57,37,48\n",
        encoding="utf-8",
    )
    (root / "data/alerts/alerts_latest.json").write_text(
        json.dumps({"highest_severity": "WATCH", "alerts": [{"severity": "WATCH", "title": "Market liquidity is soft"}]}),
        encoding="utf-8",
    )
    (root / "data/screening_latest.csv").write_text(
        "market,market_rank,name,ticker,theme,research_status,daily_change\n"
        "JP,1,Mito Securities,8622.T,Financials,research_candidate,unchanged\n"
        "JP,2,Akatsuki,3932.T,Other,research_candidate,unchanged\n"
        "US,1,Carter Bankshares,CARE,Financials,research_candidate,unchanged\n"
        "US,2,DHT,DHT,Shipping,research_candidate,unchanged\n",
        encoding="utf-8",
    )


def test_mobile_brief_tells_a_market_story(tmp_path: Path) -> None:
    _public_fixture(tmp_path)
    public_path, private_path = build_mobile_brief(tmp_path)
    text = public_path.read_text(encoding="utf-8")
    assert "3分で読む結論" in text
    assert "流動性が前回より低下" in text
    assert "今日の戦略" in text
    assert "Mito Securities" in text
    assert private_path is None


def test_private_portfolio_story_never_leaks_to_public(tmp_path: Path) -> None:
    _public_fixture(tmp_path)
    risk_dir = tmp_path / ".private/portfolio_risk"
    risk_dir.mkdir(parents=True)
    (risk_dir / "portfolio_risk_latest.json").write_text(
        json.dumps({
            "portfolio": {
                "holdings": 30,
                "metrics": {"beta": 0.91, "annualized_volatility": 0.18, "var_1d": 0.021, "cvar_1d": 0.032, "max_drawdown": -0.24},
                "concentration": {"largest_weight": 0.08, "top5_weight": 0.42, "effective_holdings": 17.2},
                "metadata_exposures": {"sector": {"Technology": 0.31, "Financials": 0.22}},
            },
            "candidate_impact": [{
                "status": "ok", "name": "PRIVATE_CANDIDATE", "verdict": "IMPROVES",
                "correlation_to_portfolio": 0.2, "delta_annualized_volatility": -0.003,
                "delta_var_1d": -0.0004,
            }],
        }),
        encoding="utf-8",
    )
    (risk_dir / "portfolio_alerts_latest.json").write_text(json.dumps({"alerts": []}), encoding="utf-8")
    public_path, private_path = build_mobile_brief(tmp_path)
    public = public_path.read_text(encoding="utf-8")
    assert private_path is not None
    private = private_path.read_text(encoding="utf-8")
    assert "PRIVATE_CANDIDATE" not in public
    assert "0.91" not in public
    assert "あなたのポートフォリオへの影響" in private
    assert "現在の保有は30銘柄" in private
    assert "PRIVATE_CANDIDATE" in private
    assert "分散改善候補" in private
