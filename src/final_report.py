from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _top_screening(path: Path, limit: int = 10) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []
    rank_col = next((x for x in ("market_rank", "rank") if x in rows[0]), None)
    if rank_col:
        try:
            rows.sort(key=lambda r: float(r.get(rank_col) or 1e9))
        except Exception:
            pass
    return rows[:limit]


def _candidate_label(r: dict[str, str]) -> str:
    return str(r.get("name") or r.get("ticker") or r.get("code") or "unknown")


def build_final_report(root: str | Path = ".") -> tuple[Path, Path | None]:
    root = Path(root)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ctx = _load_json(root / "data/decision_context_latest.json")
    regime = _load_json(root / "data/regime/market_regime_latest.json")
    alerts = _load_json(root / "data/alerts/alerts_latest.json")
    learning = _load_json(root / "data/validation/learning_latest.json")
    top = _top_screening(root / "data/screening_latest.csv", 10)

    quality = ctx.get("quality") or {}
    policy = ctx.get("policy_guardrails") or {}
    gate = str(policy.get("decision_gate") or "UNKNOWN")
    actionable = bool(quality.get("actionable"))
    highest = alerts.get("highest_severity") or "INFO"

    if not actionable or gate.startswith("BLOCK"):
        priority = "WAIT / DATA QUALITY REVIEW"
    elif highest in {"CRITICAL", "WARNING"}:
        priority = "RISK REVIEW BEFORE NEW ACTION"
    else:
        priority = "SELECTIVE REVIEW OF TOP CANDIDATES"

    lines = [
        "# Investment Quant Daily Integrated Report v2.4",
        "",
        f"Generated (UTC): {now}",
        "",
        "## 1. 結論 / 今日の優先アクション",
        f"- **{priority}**",
        f"- Decision gate: `{gate}`",
        f"- Data actionable: `{actionable}`",
        "",
        "## 2. 市場レジーム",
        f"- Regime: **{regime.get('regime_label', 'unknown')}**",
        f"- Score: {regime.get('regime_score', 'n/a')}",
        f"- Confidence: {regime.get('confidence', 'n/a')}",
        f"- VIX: {(regime.get('evidence') or {}).get('vix', 'n/a')}",
        f"- Flags: {', '.join(regime.get('regime_flags') or []) or 'none'}",
        "",
        "## 3. 例外検知 / アラート",
        f"- Highest severity: **{highest}**",
        f"- Counts: {alerts.get('counts', {})}",
    ]
    for a in (alerts.get("alerts") or [])[:8]:
        lines.append(f"- [{a.get('severity')}] {a.get('category')} / {a.get('title')}")

    lines += ["", "## 4. スクリーニング上位候補"]
    if top:
        for i, r in enumerate(top, 1):
            code = r.get("ticker") or r.get("code") or ""
            score = r.get("total_score") or r.get("pre_score") or r.get("score") or "n/a"
            lines.append(f"- {i}. {_candidate_label(r)} {code} | score={score}")
    else:
        lines.append("- データ未取得")

    change = learning.get("change_gate") or {}
    lines += [
        "",
        "## 5. 過去判断の検証 / 学習",
        f"- Matured observations: {change.get('matured_observations', 0)}",
        f"- Eligible for model-change review: {change.get('eligible_for_model_change_review', False)}",
    ]
    for f in (learning.get("findings") or [])[:6]:
        lines.append(f"- [{f.get('severity')}] {f.get('dimension')} / {f.get('segment')}: {f.get('message')}")

    lines += [
        "",
        "## 6. データ品質 / 反証",
        f"- Quality score: {quality.get('quality_score', 'n/a')}",
        f"- Primary source health (configured feeds only): {quality.get('primary_source_health', 'n/a')}",
        f"- Primary fundamental coverage: {quality.get('primary_fundamental_coverage', quality.get('fundamental_coverage', 'n/a'))}",
        f"- Secondary fundamental coverage: {quality.get('secondary_fundamental_coverage', 'n/a')}",
        f"- Effective fundamental coverage (secondary haircut applied): {quality.get('effective_fundamental_coverage', 'n/a')}",
        f"- Fundamental evidence tier: {quality.get('fundamental_evidence_tier', 'n/a')}",
    ]
    optional = quality.get("optional_primary_sources_unconfigured") or quality.get("missing_primary_configuration") or []
    if optional:
        lines.append("- Optional primary feeds not configured (confidence booster; not a hard decision blocker):")
        for item in optional:
            lines.append(f"  - {item.get('source')}: {item.get('reason')}")
    lines += [
        "- Missing data must not be converted into unsupported buy/sell conclusions.",
        "",
        "## 7. ポートフォリオ",
        "- 公開版には保有情報・私有リスク値を保存しません。",
        "- 同一実行内で private portfolio risk engine が成功した場合、私有版レポートに統合します。",
        "",
        "## 8. ガードレール",
        "- このレポートは売買指示ではなく、意思決定支援です。",
        "- 自動発注・自動因子ウェイト変更は行いません。",
        "- 『何もしない / 待つ』を常に有効な選択肢として扱います。",
    ]

    public_path = root / "data/integrated_report_latest.md"
    public_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    private_risk = root / ".private/portfolio_risk/portfolio_risk_latest.md"
    private_alerts = root / ".private/portfolio_risk/portfolio_alerts_latest.md"
    private_path: Path | None = None
    if private_risk.exists() or private_alerts.exists():
        private_path = root / ".private/integrated_report_private_latest.md"
        private_path.parent.mkdir(parents=True, exist_ok=True)
        private_lines = lines + ["", "# PRIVATE PORTFOLIO APPENDIX", ""]
        if private_risk.exists():
            private_lines += [private_risk.read_text(encoding="utf-8"), ""]
        if private_alerts.exists():
            private_lines += [private_alerts.read_text(encoding="utf-8"), ""]
        private_lines += ["PRIVATE: never commit or upload to public Actions artifacts."]
        private_path.write_text("\n".join(private_lines), encoding="utf-8")

    return public_path, private_path
