from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from release_status import SYSTEM_VERSION


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def _number(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _percent(value: Any, digits: int = 1) -> str:
    number = _number(value)
    return "算出不能" if number is None else f"{number * 100:.{digits}f}%"


def _signed(value: Any, digits: int = 1) -> str:
    number = _number(value)
    return "算出不能" if number is None else f"{number:+.{digits}f}"


def _candidate_name(row: dict[str, Any]) -> str:
    return str(row.get("name") or row.get("ticker") or row.get("code") or row.get("symbol") or "名称不明")


def _regime_delta(root: Path, current: dict[str, Any]) -> tuple[dict[str, float], str]:
    history = _load_csv(root / "data/regime/market_regime_history.csv")
    if len(history) < 2:
        return {}, "前回との比較データはまだ十分ではありません。"
    previous = history[-2]
    current_row = history[-1]
    keys = {
        "score": "score",
        "trend": "component_trend",
        "stress": "component_stress",
        "participation": "component_participation",
        "liquidity": "component_liquidity",
        "positioning": "component_positioning",
    }
    delta: dict[str, float] = {}
    for out_key, csv_key in keys.items():
        before = _number(previous.get(csv_key))
        after = _number(current_row.get(csv_key))
        if before is not None and after is not None:
            delta[out_key] = after - before

    current_label = str(current.get("regime_label") or current_row.get("label") or "不明")
    previous_label = str(previous.get("label") or "不明")
    if current_label != previous_label:
        summary = f"市場レジームは前回の{previous_label}から{current_label}へ変わりました。"
    elif delta.get("liquidity", 0) <= -3:
        summary = "地合いの分類は変わっていませんが、流動性が前回より低下しています。"
    elif delta.get("score", 0) >= 2:
        summary = "市場レジームは維持され、総合状態は前回より改善しています。"
    elif delta.get("score", 0) <= -2:
        summary = "市場レジームは維持されていますが、総合状態は前回より悪化しています。"
    else:
        summary = "市場レジームは前回からほぼ横ばいです。"
    return delta, summary


def _theme_summary(rows: list[dict[str, str]]) -> tuple[dict[str, Counter[str]], str]:
    counts: dict[str, Counter[str]] = {}
    fragments: list[str] = []
    for market, label in (("JP", "日本"), ("US", "米国")):
        subset = [r for r in rows if str(r.get("market")) == market]
        subset.sort(key=lambda r: _number(r.get("market_rank"), 1e9) or 1e9)
        counter = Counter(str(r.get("theme") or "Other") for r in subset[:20])
        counts[market] = counter
        top = [(theme, n) for theme, n in counter.most_common(2) if theme != "Other"]
        if top:
            fragments.append(f"{label}は" + "、".join(f"{theme}が{n}銘柄" for theme, n in top))
    if not fragments:
        return counts, "上位銘柄に明確なテーマ集中は検出されていません。"
    return counts, "。".join(fragments) + "で、上位銘柄に偏りがあります。"


def _rank_change_story(rows: list[dict[str, str]]) -> str:
    movers: list[tuple[float, dict[str, str]]] = []
    for row in rows:
        value = _number(row.get("rank_change"))
        if value is not None and value >= 15:
            movers.append((value, row))
        elif str(row.get("daily_change") or "").lower() in {"rank_up", "new", "surged"}:
            movers.append((value or 0.0, row))
    movers.sort(key=lambda item: item[0], reverse=True)
    if not movers:
        return "上位候補に大きな順位上昇はなく、新しい強いトレンドが出たというより、既存の選好が続いています。"
    names = "、".join(_candidate_name(row) for _, row in movers[:3])
    return f"{names}の順位上昇が目立ちます。材料と現在価格を確認する優先候補です。"


def _public_story(root: Path) -> tuple[list[str], dict[str, Any]]:
    ctx = _load_json(root / "data/decision_context_latest.json")
    quality_file = _load_json(root / "data/quality_report.json")
    regime = _load_json(root / "data/regime/market_regime_latest.json")
    alerts = _load_json(root / "data/alerts/alerts_latest.json")
    rows = _load_csv(root / "data/screening_latest.csv")
    quality = ctx.get("quality") or {}
    policy = ctx.get("policy_guardrails") or {}
    components = regime.get("components") or {}
    evidence = regime.get("evidence") or {}
    delta, delta_story = _regime_delta(root, regime)
    theme_counts, theme_story = _theme_summary(rows)
    rank_story = _rank_change_story(rows)

    score = _number(regime.get("regime_score"))
    vix = _number(evidence.get("vix"))
    liquidity = _number(components.get("liquidity"))
    gate = str(policy.get("decision_gate") or "UNKNOWN")
    actionable = bool(quality.get("actionable"))
    highest = str(alerts.get("highest_severity") or "INFO")
    concentrated = any(sum(n for theme, n in counter.items() if theme != "Other") >= 7 for counter in theme_counts.values())

    if not actionable or gate.startswith("BLOCK"):
        headline = "今日は売買判断を止め、データ品質の確認を優先します。"
        action = "新規注文は保留です。欠損や時刻を確認し、正常なデータで再実行してください。"
    elif highest in {"CRITICAL", "WARNING"}:
        headline = "新規購入より、既存ポジションのリスク確認を優先する日です。"
        action = "警告対象と保有銘柄の重なりを確認し、解消するまで新規資金は入れません。"
    elif (liquidity is not None and liquidity < 40) or concentrated:
        headline = "相場は落ち着いていますが、今日は買い急がず候補を絞る日です。"
        action = "現状維持を基本に、保有テーマと重ならない候補だけを1銘柄ずつ調べます。"
    else:
        headline = "地合いは前向きです。分散を改善する候補だけを選別します。"
        action = "一度に複数を買わず、最新決算と現在価格を確認した候補だけを小さく検討します。"

    if vix is not None and vix < 20 and liquidity is not None and liquidity < 40:
        interpretation = "VIXは落ち着いている一方、売買の厚みは弱めです。指数が穏やかでも、個別株では値が飛びやすい状態です。"
    elif vix is not None and vix >= 30:
        interpretation = "市場の恐怖感が高く、通常より値動きが荒い状態です。"
    else:
        interpretation = "市場のストレスと参加の広がりを見ながら、個別銘柄を選別する局面です。"

    alerts_lines: list[str] = []
    for alert in (alerts.get("alerts") or [])[:4]:
        alerts_lines.append(f"- **{alert.get('severity', 'INFO')}** {alert.get('title', '詳細不明')} — 売買指示ではなく確認対象です。")
    if not alerts_lines:
        alerts_lines.append("- 売買判断を変える例外は検出されていません。")

    leaders: list[str] = []
    for market, label in (("JP", "日本"), ("US", "米国")):
        subset = [r for r in rows if str(r.get("market")) == market and str(r.get("research_status", "research_candidate")) == "research_candidate"]
        subset.sort(key=lambda r: _number(r.get("market_rank"), 1e9) or 1e9)
        names = "、".join(_candidate_name(r) for r in subset[:4]) or "候補なし"
        leaders.append(f"- {label}：{names}")

    scored = quality_file.get("scored_count", "不明")
    universe = quality_file.get("universe_count", "不明")
    missing_rate = _number(quality_file.get("price_missing_rate"))
    quality_score = _number(quality.get("quality_score"))
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"# 朝の投資ブリーフ {SYSTEM_VERSION}",
        "",
        "## 3分で読む結論",
        "",
        f"**{headline}**",
        "",
        f"市場レジームは**{regime.get('regime_label', '不明')}**、総合スコアは{score:.1f}です。" if score is not None else f"市場レジームは**{regime.get('regime_label', '不明')}**です。",
        f"{delta_story}{interpretation}",
        "",
        "## 前回から何が変わった？",
        "",
        f"- 総合スコア：{_signed(delta.get('score'))}ポイント",
        f"- トレンド：{_signed(delta.get('trend'))}ポイント",
        f"- 市場参加の広がり：{_signed(delta.get('participation'))}ポイント",
        f"- 流動性：{_signed(delta.get('liquidity'))}ポイント",
        f"- {rank_story}",
        "",
        "## 今の相場を人間の言葉で",
        "",
        f"{theme_story}{interpretation}",
        "同じテーマの上位銘柄を複数買うと、銘柄数が増えても実質的な分散にならない点に注意してください。",
        "",
        "## 今日の注意点",
        "",
        *alerts_lines,
        "",
        "## 調査の入口",
        "",
        *leaders,
        "",
        "上記は買いリストではありません。現在価格、最新決算、開示、保有資産との重複を確認するための調査対象です。",
        "",
        "## 今日の戦略",
        "",
        f"**{action}**",
        "買う場合も、候補1銘柄をポートフォリオの2%で試算し、β・VaR・集中度が改善するものを優先します。",
        "",
        "## あなたのポートフォリオ",
        "",
        "保有情報を含む分析は、同一実行内の非公開版で生成します。公開版には銘柄名・比率・個人リスク値を保存しません。",
        "",
        "## 判断の確からしさ",
        "",
        f"データ品質は{_percent(quality_score)}。{universe}銘柄中{scored}銘柄を採点し、価格欠損率は{_percent(missing_rate)}です。",
        "公式財務データが不足する場合は、証券会社画面と企業の公式開示を確認するまで注文しません。",
        "",
        f"生成時刻（UTC）：{generated}",
    ]
    context = {
        "headline": headline,
        "action": action,
        "gate": gate,
        "actionable": actionable,
        "highest": highest,
    }
    return lines, context


def _private_story(root: Path, public_lines: list[str], context: dict[str, Any]) -> list[str] | None:
    risk = _load_json(root / ".private/portfolio_risk/portfolio_risk_latest.json")
    if not risk:
        return None
    private_alerts = _load_json(root / ".private/portfolio_risk/portfolio_alerts_latest.json")
    portfolio = risk.get("portfolio") or {}
    metrics = portfolio.get("metrics") or {}
    concentration = portfolio.get("concentration") or {}
    exposures = portfolio.get("metadata_exposures") or {}
    holdings = portfolio.get("holdings", "不明")

    top5 = _number(concentration.get("top5_weight"))
    largest = _number(concentration.get("largest_weight"))
    effective = _number(concentration.get("effective_holdings"))
    if top5 is not None and top5 >= 0.5:
        concentration_story = "上位5銘柄への集中が高く、次の追加投資は分散改善を最優先にします。"
    elif effective is not None and effective < 10:
        concentration_story = "保有銘柄数に比べて実質分散が弱く、値動きは一部銘柄に左右されやすい状態です。"
    else:
        concentration_story = "集中度は直ちに防御行動を必要とする水準ではありません。"

    exposure_lines: list[str] = []
    for key, label in (("sector", "業種"), ("currency", "通貨"), ("region", "地域"), ("style", "スタイル")):
        values = exposures.get(key) or {}
        if isinstance(values, dict) and values:
            top = sorted(values.items(), key=lambda item: _number(item[1], 0.0) or 0.0, reverse=True)[:3]
            exposure_lines.append(f"- {label}：" + "、".join(f"{name} {_percent(weight)}" for name, weight in top))
    if not exposure_lines:
        exposure_lines.append("- 業種・通貨などの属性データは不足しているため、推測しません。")

    impacts = [x for x in (risk.get("candidate_impact") or []) if x.get("status") == "ok"]
    improves = [x for x in impacts if x.get("verdict") == "IMPROVES"]
    worsens = [x for x in impacts if x.get("verdict") == "WORSENS"]
    neutral = [x for x in impacts if x.get("verdict") == "NEUTRAL"]

    candidate_lines: list[str] = []
    for title, items in (("分散改善候補", improves), ("中立", neutral), ("リスク悪化候補", worsens)):
        if not items:
            continue
        candidate_lines.append(f"### {title}")
        for item in items[:5]:
            candidate_lines.append(
                f"- {_candidate_name(item)}：相関{_number(item.get('correlation_to_portfolio')) or 0:.2f}、"
                f"年率ボラ変化{_percent(item.get('delta_annualized_volatility'), 2)}、"
                f"1日VaR変化{_percent(item.get('delta_var_1d'), 2)}"
            )
    if not candidate_lines:
        candidate_lines.append("- 候補追加効果を判定できるだけの市場データがありません。")

    alert_items = private_alerts.get("alerts") or []
    private_alert_lines = [f"- **{a.get('severity', 'INFO')}** {a.get('title', a.get('code', '詳細不明'))}：{a.get('message', '')}" for a in alert_items]
    if not private_alert_lines:
        private_alert_lines.append("- ポートフォリオ固有の例外は検出されていません。")

    private = list(public_lines)
    private += [
        "",
        "# 非公開：あなたのポートフォリオへの影響",
        "",
        f"現在の保有は{holdings}銘柄です。{concentration_story}",
        "",
        "## まず確認するリスク",
        "",
        f"- 市場β：{_number(metrics.get('beta')) if _number(metrics.get('beta')) is not None else '算出不能'}",
        f"- 年率ボラティリティ：{_percent(metrics.get('annualized_volatility'))}",
        f"- 1日VaR（通常の悪い日）：{_percent(metrics.get('var_1d'))}",
        f"- 1日CVaR（さらに悪い日の平均）：{_percent(metrics.get('cvar_1d'))}",
        f"- 過去最大ドローダウン：{_percent(metrics.get('max_drawdown'))}",
        f"- 最大銘柄比率：{_percent(largest)}／上位5銘柄比率：{_percent(top5)}",
        f"- 実質保有銘柄数：{effective:.1f}" if effective is not None else "- 実質保有銘柄数：算出不能",
        "",
        "## 偏り",
        "",
        *exposure_lines,
        "",
        "## 候補を2%加えた場合",
        "",
        *candidate_lines,
        "",
        "候補評価は分散効果だけの判定です。事業価値・決算・現在価格を確認するまでは買い判断にしません。",
        "",
        "## ポートフォリオ固有の注意",
        "",
        *private_alert_lines,
        "",
        "## あなた向けの今日の行動",
        "",
        f"**{context['action']}**",
        "分散改善候補があっても、既存の同一テーマ保有を確認し、必要なら入れ替えで対応します。銘柄数を増やすこと自体は目的にしません。",
        "",
        "PRIVATE：このファイルは公開リポジトリや公開Actions artifactへ保存しません。",
    ]
    return private


def build_mobile_brief(root: str | Path = ".") -> tuple[Path, Path | None]:
    root = Path(root)
    public_lines, context = _public_story(root)
    public_path = root / "data/mobile_brief_latest.md"
    public_path.parent.mkdir(parents=True, exist_ok=True)
    public_path.write_text("\n".join(public_lines) + "\n", encoding="utf-8")

    private_lines = _private_story(root, public_lines, context)
    private_path: Path | None = None
    if private_lines is not None:
        private_path = root / ".private/mobile_brief_private_latest.md"
        private_path.parent.mkdir(parents=True, exist_ok=True)
        private_path.write_text("\n".join(private_lines) + "\n", encoding="utf-8")
    return public_path, private_path
