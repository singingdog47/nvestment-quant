from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from release_status import DEVELOPMENT_STATUS, ROLLBACK_READY, STABLE_FALLBACK_BRANCH, SYSTEM_VERSION


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _screening_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _numeric(row: dict[str, str], key: str, default: float = -1e9) -> float:
    try:
        return float(row.get(key) or default)
    except Exception:
        return default


def _candidate_label(r: dict[str, str]) -> str:
    return str(r.get("name") or r.get("ticker") or r.get("code") or "unknown")


def _leaders(rows: list[dict[str, str]], market: str, limit: int = 5) -> list[dict[str, str]]:
    subset = [r for r in rows if str(r.get("market")) == market and str(r.get("research_status", "research_candidate")) == "research_candidate"]
    return sorted(subset, key=lambda r: (_numeric(r, "market_rank", 1e9), -_numeric(r, "total_score")))[:limit]


def _cross_market(rows: list[dict[str, str]], limit: int = 10) -> list[dict[str, str]]:
    subset = [r for r in rows if str(r.get("research_status", "research_candidate")) == "research_candidate"]
    return sorted(subset, key=lambda r: (-_numeric(r, "cross_market_score"), -_numeric(r, "total_score")))[:limit]


def build_final_report(root: str | Path = ".") -> tuple[Path, Path | None]:
    root = Path(root)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ctx = _load_json(root / "data/decision_context_latest.json")
    regime = _load_json(root / "data/regime/market_regime_latest.json")
    alerts = _load_json(root / "data/alerts/alerts_latest.json")
    learning = _load_json(root / "data/validation/learning_latest.json")
    rows = _screening_rows(root / "data/screening_latest.csv")
    quality = ctx.get("quality") or {}
    policy = ctx.get("policy_guardrails") or {}
    gate = str(policy.get("decision_gate") or "UNKNOWN")
    quality_actionable = bool(quality.get("actionable"))
    regime_actionable = bool(regime.get("actionable"))
    if not quality_actionable or gate.startswith("BLOCK"):
        analysis_mode = "BLOCKED"
    elif not regime_actionable:
        analysis_mode = "REVIEW_ONLY_PARTIAL_REGIME"
    else:
        analysis_mode = "OPEN_FOR_ANALYSIS"
    highest = alerts.get("highest_severity") or "INFO"
    if analysis_mode == "BLOCKED":
        priority = "WAIT / DATA QUALITY REVIEW"
    elif highest in {"CRITICAL", "WARNING"}:
        priority = "RISK REVIEW BEFORE NEW ACTION"
    elif not regime_actionable:
        priority = "PARTIAL REGIME / REVIEW ONLY"
    else:
        priority = "SELECTIVE REVIEW OF TOP CANDIDATES"

    evidence = regime.get("evidence") or {}
    lines = [f"# Investment Quant Daily Integrated Report {SYSTEM_VERSION}", "", f"Generated (UTC): {now}", "", "## 1. 結論 / 今日の優先アクション", f"- **{priority}**", f"- Decision gate: `{gate}`", f"- Screening / intelligence data actionable: `{quality_actionable}`", f"- Regime context actionable: `{regime_actionable}`", f"- Overall analysis mode: `{analysis_mode}`", "", "## 2. 市場レジーム", f"- Regime: **{regime.get('regime_label', 'unknown')}**", f"- Score: {regime.get('regime_score', 'n/a')}", f"- Confidence: {regime.get('confidence', 'n/a')}", f"- Data status: {regime.get('data_status', 'unknown')}", f"- Actionability reasons: {', '.join((regime.get('actionability') or {}).get('reasons') or []) or 'none'}", f"- VIX: {evidence.get('vix', 'n/a')}", f"- Treasury realized-vol proxy (not ICE MOVE): {evidence.get('treasury_volatility_proxy', 'n/a')} bps annualized; percentile={evidence.get('treasury_volatility_percentile_rank', 'n/a')}", f"- Flags: {', '.join(regime.get('regime_flags') or []) or 'none'}", "", "## 3. 例外検知 / アラート", f"- Highest severity: **{highest}**", f"- Counts: {alerts.get('counts', {})}"]
    for a in (alerts.get("alerts") or [])[:8]:
        lines.append(f"- [{a.get('severity')}] {a.get('category')} / {a.get('title')}")
    lines += ["", "## 4. スクリーニング上位候補", "", "### 日本株（市場内順位）"]
    jp = _leaders(rows, "JP")
    lines += [f"- {i}. {_candidate_label(r)} {r.get('ticker') or r.get('code') or ''} | market_rank={r.get('market_rank','n/a')} | raw={r.get('total_score','n/a')} | cross_pct={r.get('cross_market_score','n/a')}" for i, r in enumerate(jp, 1)] or ["- データ未取得"]
    lines += ["", "### 米国株（市場内順位）"]
    us = _leaders(rows, "US")
    lines += [f"- {i}. {_candidate_label(r)} {r.get('ticker') or r.get('code') or ''} | market_rank={r.get('market_rank','n/a')} | raw={r.get('total_score','n/a')} | cross_pct={r.get('cross_market_score','n/a')}" for i, r in enumerate(us, 1)] or ["- データ未取得"]
    lines += ["", "### 市場横断リサーチ候補（市場内パーセンタイル比較）"]
    cross = _cross_market(rows)
    lines += [f"- {i}. [{r.get('market','?')}] {_candidate_label(r)} | cross_pct={r.get('cross_market_score','n/a')} | raw={r.get('total_score','n/a')}" for i, r in enumerate(cross, 1)] or ["- データ未取得"]
    lines.append("- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。")
    change = learning.get("change_gate") or {}
    lines += ["", "## 5. 過去判断の検証 / 学習", f"- Matured observations: {change.get('matured_observations', 0)}", f"- Eligible for model-change review: {change.get('eligible_for_model_change_review', False)}"]
    for f in (learning.get("findings") or [])[:6]:
        lines.append(f"- [{f.get('severity')}] {f.get('dimension')} / {f.get('segment')}: {f.get('message')}")
    lines += ["", "## 6. データ品質 / 反証", f"- Quality score: {quality.get('quality_score', 'n/a')}", f"- Primary source health (configured feeds only): {quality.get('primary_source_health', 'n/a')}", f"- Primary fundamental coverage: {quality.get('primary_fundamental_coverage', quality.get('fundamental_coverage', 'n/a'))}", f"- Secondary fundamental coverage: {quality.get('secondary_fundamental_coverage', 'n/a')}", f"- Effective fundamental coverage: {quality.get('effective_fundamental_coverage', 'n/a')}", f"- Fundamental evidence tier: {quality.get('fundamental_evidence_tier', 'n/a')}"]
    optional = quality.get("optional_primary_sources_unconfigured") or quality.get("missing_primary_configuration") or []
    if optional:
        lines.append("- Optional primary feeds not configured (confidence booster; not a hard decision blocker):")
        for item in optional:
            lines.append(f"  - {item.get('source')}: {item.get('reason')}")
    lines += ["- Missing data must not be converted into unsupported buy/sell conclusions.", "", "## 7. ポートフォリオ", "- 公開版には保有情報・私有リスク値を保存しません。", "- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。", "- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。", "", "## 8. 開発状況 / 復旧準備", f"- System version: {SYSTEM_VERSION}", f"- Development: {DEVELOPMENT_STATUS}", f"- Stable fallback branch: `{STABLE_FALLBACK_BRANCH}`", f"- Rollback ready: `{ROLLBACK_READY}`", "- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。", "", "## 9. ガードレール", "- このレポートは売買指示ではなく、意思決定支援です。", "- 自動発注・自動因子ウェイト変更は行いません。", "- 『何もしない / 待つ』を常に有効な選択肢として扱います。"]
    public_path = root / "data/integrated_report_latest.md"
    public_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    private_risk = root / ".private/portfolio_risk/portfolio_risk_latest.md"
    private_alerts = root / ".private/portfolio_risk/portfolio_alerts_latest.md"
    private_valuation = root / ".private/portfolio_risk/portfolio_valuation_latest.md"
    private_monthly = root / ".private/portfolio_risk/portfolio_monthly_latest.md"
    private_path: Path | None = None
    private_sections = [private_risk, private_valuation, private_monthly, private_alerts]
    if any(path.exists() for path in private_sections):
        private_path = root / ".private/integrated_report_private_latest.md"
        private_path.parent.mkdir(parents=True, exist_ok=True)
        private_lines = lines + ["", "# PRIVATE PORTFOLIO APPENDIX", ""]
        for path in private_sections:
            if path.exists():
                private_lines += [path.read_text(encoding="utf-8"), ""]
        private_lines += ["PRIVATE: never commit or upload to public Actions artifacts."]
        private_path.write_text("\n".join(private_lines), encoding="utf-8")
    return public_path, private_path
