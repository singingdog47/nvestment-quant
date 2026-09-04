from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from market_regime.market_data import fetch_market_history


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def _num(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        value = float(value)
        if math.isnan(value) or math.isinf(value):
            return default
        return value
    except (TypeError, ValueError):
        return default


def load_config(root: str | Path = ".") -> dict[str, Any]:
    return json.loads((Path(root) / "config/paypay_swing_v1.json").read_text(encoding="utf-8"))


def _row(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    return next((r for r in rows if str(r.get("series")) == key), {})


def _momentum(r: dict[str, Any]) -> float:
    if not r:
        return 0.0
    score = 50.0
    r20, r60 = _num(r.get("ret_20d")), _num(r.get("ret_60d"))
    close = _num(r.get("close"))
    if r20 is not None:
        score += _clamp(r20 * 120.0, -20.0, 20.0)
    if r60 is not None:
        score += _clamp(r60 * 60.0, -20.0, 20.0)
    for ma_key, bonus in (("ma20", 4.0), ("ma50", 5.0), ("ma200", 6.0)):
        ma = _num(r.get(ma_key))
        if close is not None and ma is not None:
            score += bonus if close >= ma else -bonus
    return _clamp(score)


def _trend(r: dict[str, Any]) -> float:
    if not r:
        return 0.0
    score = 50.0
    close = _num(r.get("close"))
    for ma_key, weight in (("ma20", 10.0), ("ma50", 12.0), ("ma200", 16.0)):
        ma = _num(r.get(ma_key))
        if close is not None and ma is not None:
            score += weight if close >= ma else -weight
    ma20, ma50, ma200 = _num(r.get("ma20")), _num(r.get("ma50")), _num(r.get("ma200"))
    if ma20 is not None and ma50 is not None:
        score += 6.0 if ma20 >= ma50 else -6.0
    if ma50 is not None and ma200 is not None:
        score += 6.0 if ma50 >= ma200 else -6.0
    drawdown = _num(r.get("drawdown_52w"))
    if drawdown is not None:
        score -= min(18.0, max(0.0, -drawdown * 60.0))
    return _clamp(score)


def _risk(r: dict[str, Any]) -> float:
    if not r:
        return 0.0
    score = 100.0
    vol, drawdown = _num(r.get("vol20_ann")), _num(r.get("drawdown_52w"))
    score -= min(65.0, vol * 75.0) if vol is not None else 25.0
    if drawdown is not None:
        score -= min(30.0, max(0.0, -drawdown * 70.0))
    return _clamp(score)


def _macro(course: str, macro: dict[str, dict[str, Any]], market: dict[str, dict[str, Any]]) -> float:
    score = 50.0
    us10y = _num((macro.get("US10Y") or {}).get("ret_20d"))
    dxy = _num((macro.get("DXY") or {}).get("ret_20d"))
    vix = _num((macro.get("VIX") or {}).get("close"))
    spy20 = _num((market.get("STANDARD") or {}).get("ret_20d"))
    qqq20 = _num((market.get("TECH") or {}).get("ret_20d"))
    if course == "GOLD":
        if us10y is not None:
            score += _clamp(-us10y * 180.0, -15.0, 15.0)
        if dxy is not None:
            score += _clamp(-dxy * 220.0, -15.0, 15.0)
        if vix is not None and vix >= 20:
            score += 3.0 if vix < 25 else 8.0
    elif course == "TECH":
        if us10y is not None:
            score += _clamp(-us10y * 150.0, -13.0, 13.0)
        if dxy is not None:
            score += _clamp(-dxy * 100.0, -6.0, 6.0)
        if vix is not None:
            score += 10.0 if vix < 20 else (-20.0 if vix >= 30 else -5.0 if vix >= 25 else 0.0)
        if spy20 is not None:
            score += 6.0 if spy20 > 0 else -6.0
    elif course == "STANDARD":
        if us10y is not None:
            score += _clamp(-us10y * 90.0, -8.0, 8.0)
        if vix is not None:
            score += 12.0 if vix < 20 else (-18.0 if vix >= 30 else -6.0 if vix >= 25 else 0.0)
        if spy20 is not None:
            score += 8.0 if spy20 > 0 else -8.0
    elif course == "BTC":
        if dxy is not None:
            score += _clamp(-dxy * 180.0, -12.0, 12.0)
        if vix is not None:
            score += 10.0 if vix < 20 else (-22.0 if vix >= 30 else -8.0 if vix >= 25 else 0.0)
        if qqq20 is not None:
            score += 10.0 if qqq20 > 0 else -10.0
    return _clamp(score)


def _cost(entry_pct: float, exit_pct: float) -> tuple[float, float]:
    entry, exit_ = max(0.0, entry_pct) / 100.0, max(0.0, exit_pct) / 100.0
    round_trip = (1.0 - (1.0 - entry) * (1.0 - exit_)) * 100.0
    return _clamp(100.0 - round_trip * 9.0), round_trip


def score_rows(config: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    market = {key: _row(rows, key) for key in config["courses"]}
    macro = {key: _row(rows, key) for key in config["macro_symbols"]}
    w = config["weights"]
    out: list[dict[str, Any]] = []
    for key, spec in config["courses"].items():
        r = market[key]
        mom, mac, tr, risk = _momentum(r), _macro(key, macro, market), _trend(r), _risk(r)
        cost, round_trip = _cost(float(spec.get("entry_cost_pct", 0)), float(spec.get("exit_cost_pct", 0)))
        total = mom*w["momentum"] + mac*w["macro"] + tr*w["trend"] + risk*w["risk"] + cost*w["cost"]
        out.append({
            "key": key,
            "label": spec["label"],
            "ticker": spec["ticker"],
            "close": _num(r.get("close")),
            "data_date": r.get("date"),
            "momentum": round(mom, 2),
            "macro": round(mac, 2),
            "trend": round(tr, 2),
            "risk": round(risk, 2),
            "cost": round(cost, 2),
            "round_trip_cost_pct": round(round_trip, 2),
            "total": round(total, 2),
        })
    return sorted(out, key=lambda x: x["total"], reverse=True)


def _research_status(ranking: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    if not ranking:
        return {"status": "DATA_UNAVAILABLE", "leader": None, "reason": "データ未取得"}
    top = ranking[0]
    second = ranking[1] if len(ranking) > 1 else None
    margin = top["total"] - (second["total"] if second else 0.0)
    gate = config["entry_gate"]
    minimum = max(float(gate["minimum_score"]), float(config["courses"][top["key"]].get("minimum_score", 0.0)))
    if top["total"] < minimum or top["momentum"] < gate["minimum_momentum"] or top["trend"] < gate["minimum_trend"]:
        status = "WAIT_RESEARCH"
        reason = f"首位{top['label']}は{top['total']:.1f}点だが確認閾値未達"
    elif margin < gate["minimum_margin"]:
        status = "WAIT_RESEARCH"
        reason = f"首位と2位の差が{margin:.1f}点で優位性が弱い"
    else:
        status = "REVIEW_LEADER"
        reason = f"{top['label']}が{top['total']:.1f}点、2位との差{margin:.1f}点。週次レビュー候補"
    return {"status": status, "leader": top["key"] if status == "REVIEW_LEADER" else None, "reason": reason, "margin": round(margin, 2)}


def _write_history(path: Path, date_key: str, ranking: list[dict[str, Any]]) -> None:
    fields = ["date", "course", "ticker", "close", "total", "momentum", "macro", "trend", "risk", "cost"]
    old: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            old = [x for x in csv.DictReader(f) if x.get("date") != date_key]
    for r in ranking:
        old.append({k: str(r.get(k, "")) for k in fields if k != "date"} | {"date": date_key, "course": r["key"]})
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(old)


def _table(ranking: list[dict[str, Any]]) -> list[str]:
    lines = ["|順位|コース|総合|Momentum|Macro|Trend|Risk|Cost|往復コスト概算|", "|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
    for i, r in enumerate(ranking, 1):
        lines.append(f"|{i}|{r['label']}|{r['total']:.1f}|{r['momentum']:.1f}|{r['macro']:.1f}|{r['trend']:.1f}|{r['risk']:.1f}|{r['cost']:.1f}|{r['round_trip_cost_pct']:.1f}%|")
    return lines


def run(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    config = load_config(root)
    now = datetime.now(ZoneInfo(config.get("review_timezone", "Asia/Tokyo")))
    symbols = {key: spec["ticker"] for key, spec in config["courses"].items()} | config["macro_symbols"]
    metrics, _hist, health = fetch_market_history(symbols, period="1y", interval="1d")
    rows = metrics.to_dict(orient="records") if not metrics.empty else []
    ranking = score_rows(config, rows)
    status = _research_status(ranking, config)
    failed = [h for h in health if h.get("status") != "ok"]
    data_status = "ok" if ranking and not failed else ("partial" if ranking else "unavailable")
    review_day = now.weekday() == int(config.get("weekly_review_weekday", 4))
    payload = {
        "generated_at_jst": now.isoformat(timespec="seconds"),
        "data_status": data_status,
        "review_day": review_day,
        "research_status": status,
        "ranking": ranking,
        "source_health": health,
        "guardrails": {
            "automatic_ordering": False,
            "daily_role": "monitoring",
            "weekly_role": "human_review_support",
            "wait_is_valid": True,
            "crypto_spread_is_variable": True
        }
    }
    out = root / "data/paypay_swing"
    out.mkdir(parents=True, exist_ok=True)
    (out / "paypay_swing_latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_history(out / "history.csv", now.date().isoformat(), ranking)

    daily = [
        "# PayPayポイント運用 数か月スイング 日次監視", "",
        f"- 生成時刻: {payload['generated_at_jst']}",
        f"- データ状態: **{data_status}**",
        f"- 監視判定: **{status['status']}** — {status['reason']}",
        "- 日次は監視のみ。数か月スイングなので日々のノイズで判断を変更しません。", "",
        "## 現在ランキング", "", *_table(ranking), "",
        "## コスト注意", "",
        "- 通常コースは100pt以上の追加時に1.0%相当を前提。引き出しは原則無料。",
        "- BTC等は追加・引き出し時にそれぞれ通常4.5%程度で、市況により変動します。",
        "- PayPayのコース価格は参照ETF・暗号資産と完全一致しません。"
    ]
    (out / "paypay_swing_daily_latest.md").write_text("\n".join(daily) + "\n", encoding="utf-8")

    weekly = [
        "# PayPayポイント運用 数か月スイング 週次レビュー", "",
        f"- 本日が週次レビュー日: **{review_day}**",
        f"- 研究候補: **{status['leader'] or 'なし / WAIT'}**",
        f"- 根拠: {status['reason']}", "",
        "## ランキング", "", *_table(ranking), "",
        "## ルール", "",
        "- Momentum 35% / Macro 25% / Trend 20% / Risk 10% / Cost 10%。",
        "- 首位でも最低点・Momentum・Trend・2位との差を満たさなければWAIT。",
        "- BTCは往復スプレッドが大きいため通常コースより高い確認閾値を設定。",
        "- 最終的な売買判断は自動化せず、PayPay画面の実際のスプレッドと市場材料を確認します。", "",
        "## ブラインドスポット", "",
        "- yfinanceは二次データでありPayPayの実際のコース価格ではありません。",
        "- 実質金利や暗号資産固有需給など代理指標で捉えきれない要因があります。",
        "- 履歴を蓄積し、1/3/6か月後の成績でモデルの有効性を検証します。"
    ]
    (out / "paypay_swing_weekly_latest.md").write_text("\n".join(weekly) + "\n", encoding="utf-8")
    return payload


def compact_markdown(payload: dict[str, Any]) -> str:
    status = payload.get("research_status") or {}
    ranking = payload.get("ranking") or []
    leaders = " / ".join(f"{r['label']} {r['total']:.1f}" for r in ranking[:3]) if ranking else "データ未取得"
    return "\n".join([
        "## PayPay Swing",
        "",
        f"- 監視判定: **{status.get('status', 'DATA_UNAVAILABLE')}** — {status.get('reason', '判定不能')}",
        f"- 上位: {leaders}",
        "- 数か月スイングのため日次は監視、週次でまとめて再評価。WAITを常に有効な選択肢とします。",
        "- 暗号資産コースはスプレッド負担をコストスコアに反映しています。"
    ])


def inject_into_reports(root: str | Path = ".") -> None:
    root = Path(root)
    src = root / "data/paypay_swing/paypay_swing_latest.json"
    if not src.exists():
        return
    block = compact_markdown(json.loads(src.read_text(encoding="utf-8")))
    start, end = "<!-- PAYPAY_SWING_START -->", "<!-- PAYPAY_SWING_END -->"
    wrapped = f"{start}\n{block}\n{end}\n"
    for path, marker in [
        (root / "data/mobile_brief_latest.md", "## 判断の確からしさ"),
        (root / "data/integrated_report_latest.md", "## 8. 開発状況 / 復旧準備")
    ]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if start in text and end in text:
            text = text.split(start, 1)[0] + text.split(end, 1)[1].lstrip("\n")
        text = text.replace(marker, wrapped + "\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + wrapped
        path.write_text(text, encoding="utf-8")
