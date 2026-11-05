"""Lightweight, public-only, decision-first market risk watch.

No private positions, no broker execution. Missing/stale prices are UNVERIFIED.
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

FEEDS = {
    "NIKKEI_FUT": ("NIY=F", 150),  # CME yen futures proxy, NOT JPX Osaka
    "NASDAQ": ("^IXIC", 900),
    "SP500": ("^GSPC", 900),
    "VIX": ("^VIX", 900),
}


def fetch_one(name: str, symbol: str, max_age_minutes: int, now: datetime) -> dict:
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + quote(symbol, safe="") + "?range=5d&interval=5m")
    rec = {"name": name, "ticker": symbol,
           "source": "Yahoo Finance chart (unofficial, secondary)",
           "status": "UNVERIFIED"}
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0 research-risk-watch/1.0"})
        with urlopen(request, timeout=8) as response:
            payload = json.load(response)
        meta = payload["chart"]["result"][0]["meta"]
        price = float(meta["regularMarketPrice"])
        previous = meta.get("chartPreviousClose") or meta.get("previousClose")
        timestamp = int(meta["regularMarketTime"])
        age_minutes = (now.timestamp() - timestamp) / 60.0
        rec.update({
            "as_of_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
            "age_minutes": round(age_minutes, 1),
        })
        if previous is None:
            rec["reason"] = "previous close unavailable"
        elif not all(math.isfinite(x) and x > 0 for x in (price, float(previous))):
            rec["reason"] = "invalid quote"
        elif age_minutes < -5 or age_minutes > max_age_minutes:
            rec["reason"] = "stale or future timestamp; excluded from decisions"
        else:
            rec.update({"status": "OK", "price": price,
                        "previous_close": float(previous),
                        "change_pct": round(100 * (price / float(previous) - 1), 3)})
    except (ValueError, KeyError, IndexError, TypeError, OSError, TimeoutError) as exc:
        rec["reason"] = "feed unavailable: " + type(exc).__name__
    return rec


def decide(feeds: dict, now: datetime | None = None) -> dict:
    """Decide risk urgency independently of the daily NEUTRAL regime label."""
    now = now or datetime.now(timezone.utc)

    def change(key):
        row = feeds.get(key) or {}
        return row.get("change_pct") if row.get("status") == "OK" else None

    fut, nas, sp = (change(k) for k in ("NIKKEI_FUT", "NASDAQ", "SP500"))
    vix = feeds.get("VIX") or {}
    vix_price = vix.get("price") if vix.get("status") == "OK" else None
    evidence = [k for k in FEEDS if (feeds.get(k) or {}).get("status") == "OK"]
    drivers = []

    def flag(condition, message):
        if condition:
            drivers.append(message)
        return bool(condition)

    critical = (
        flag(fut is not None and fut <= -5, "日経円建て先物(CME)が-5%以下")
        | flag(nas is not None and nas <= -5, "NASDAQが-5%以下")
        | flag(sp is not None and sp <= -4, "S&P500が-4%以下")
        | flag(fut is not None and nas is not None and fut <= -3 and nas <= -3,
               "日経円建て先物とNASDAQが同時に-3%以下")
    )
    defensive = (
        flag(fut is not None and fut <= -3, "日経円建て先物(CME)が-3%以下")
        | flag(nas is not None and nas <= -3, "NASDAQが-3%以下")
        | flag(sp is not None and sp <= -2.5, "S&P500が-2.5%以下")
        | flag(vix_price is not None and vix_price >= 25, "VIXが25以上")
    )
    caution = (
        flag(fut is not None and fut <= -1.5, "日経円建て先物(CME)が-1.5%以下")
        | flag(nas is not None and nas <= -2, "NASDAQが-2%以下")
        | flag(sp is not None and sp <= -1.5, "S&P500が-1.5%以下")
        | flag(vix_price is not None and vix_price >= 20, "VIXが20以上")
    )
    if critical:
        level = "CRITICAL"
    elif defensive:
        level = "DEFENSIVE"
    elif caution:
        level = "CAUTION"
    elif evidence:
        level = "NORMAL"
    else:
        level = "UNVERIFIED"

    plans = {
        "CRITICAL": ["新規買い停止", "既存買い指値の取消を優先審査",
                     "下落に弱い保有銘柄の利益確定・縮小を寄り前に審査", "防衛資金維持"],
        "DEFENSIVE": ["新規買い原則停止", "未約定買い注文を再評価",
                      "保有銘柄の撤退条件と売却数量を決定"],
        "CAUTION": ["新規買いは期待値とリスクを再検討", "保有銘柄の損失制限条件を点検"],
        "NORMAL": ["新規注文はPF・最新株価・会社情報の別検証を条件に判断"],
        "UNVERIFIED": ["データ未確認。安全と断定しない",
                       "板・取引所の先物・信頼できる現在値で照合"],
    }
    return {
        "schema_version": "1.0",
        "generated_at_utc": now.isoformat(),
        "risk_level": level,
        "market_decision": ("RISK_REDUCTION_REVIEW" if level in ("CRITICAL", "DEFENSIVE")
                            else "VERIFY_DATA" if level == "UNVERIFIED"
                            else "NO_FORCED_TRADE"),
        "risk_drivers": list(dict.fromkeys(drivers)),
        "verified_feeds": evidence,
        "feeds": feeds,
        "recommended_actions": plans[level],
        "execution": "ADVISORY_ONLY",
        "private_portfolio_used": False,
        "limitations": [
            "No executable orders; private holdings/order status must be checked.",
            "NIY=F is a CME proxy, not JPX Osaka futures.",
            "Unofficial secondary quotes may be delayed.",
            "Automated schedules can be delayed; no realtime delivery guarantee.",
        ],
    }


def write_outputs(report: dict, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / "latest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = ["# 売買判断優先・市場急変チェック", "",
             f"生成（UTC）：{report['generated_at_utc']}",
             f"**危機判定：{report['risk_level']}**",
             f"**判断：{report['market_decision']}**", "",
             "## 急変要因"]
    lines += ["- " + s for s in report["risk_drivers"]] or [
        "- 確認済み急変トリガーなし。未取得データは安全の証拠ではない"
    ]
    lines += ["", "## データ基準時刻・品質"]
    for name, row in report["feeds"].items():
        lines.append(
            f"- {name}: {row.get('status')} / {row.get('change_pct', 'N/A')}% "
            f"/ {row.get('as_of_utc', '不明')} / {row.get('reason', '')}"
        )
    lines += ["", "## 売買判断まとめ"]
    lines += ["- " + s for s in report["recommended_actions"]]
    lines += ["", "**個別銘柄・数量・成行/指値は非公開PF、注文履歴、最新板を照合して決定。自動売買なし。**", ""]
    (target / "latest.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc)
    feeds = {name: fetch_one(name, ticker, age, now)
             for name, (ticker, age) in FEEDS.items()}
    result = decide(feeds, now)
    write_outputs(result, Path(os.getenv("ACTION_FIRST_OUTPUT_DIR", "data/action_first")))
    print(json.dumps({"risk_level": result["risk_level"],
                      "market_decision": result["market_decision"],
                      "verified_feeds": result["verified_feeds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
