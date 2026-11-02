"""Human-readable, fail-closed health snapshot for no-money quant research.

This is a reporting layer, NOT an order executor or an automatic data repairer.
ChatGPT's condition-watch automation can read data/health/latest.json and the
underlying ledgers, and notify only on meaningful incident transitions.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from jpx_market_calendar import is_jpx_session

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "challenger1": "data/shadow_challenger/latest.json",
    "challenger2": "data/shadow_challenger2/latest.json",
    "ai_ma": "data/ai_ma_shadow/latest.json",
    "regime": "data/regime/market_regime_latest.json",
}
ARCHIVED_V2 = "data/shadow_swing_v2/latest.json"
DATA_CODES = (
    "missing", "unavailable", "stale", "outdated", "invalid",
    "fetch", "error", "failed", "timeout", "benchmark", "no_bar",
)
RISK_CODES = ("market_stress", "risk_", "drawdown", "exposure_limit")


def read_json(path: Path):
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
        return value if isinstance(value, dict) else None
    except (OSError, ValueError, UnicodeError):
        return None


def classify_blocker(code: str) -> str:
    name = code.lower()
    if name.startswith(RISK_CODES):
        return "RISK_CONTROL"
    if any(fragment in name for fragment in DATA_CODES):
        return "DATA_INCIDENT"
    return "UNKNOWN_BLOCKER"


def completed_jpx_sessions(observed, now: datetime) -> int:
    """Count completed cash-market sessions, not holidays or the pre-close day."""
    from datetime import timedelta
    jst = now.astimezone(ZoneInfo("Asia/Tokyo"))
    last = jst.date() if (jst.hour, jst.minute) >= (23, 45) else jst.date() - timedelta(days=1)
    count = 0
    day = observed + timedelta(days=1)
    while day <= last:
        if is_jpx_session(day):
            count += 1
        day += timedelta(days=1)
    return count



def read_pipeline_report(path: Path):
    """Read only the post-close report generation timestamp, never infer trades."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    match = re.search(r"^Generated \\(UTC\\):\\s*(\\S+)", content, re.MULTILINE)
    if not match:
        return None
    try:
        generated = datetime.fromisoformat(match.group(1))
        if generated.tzinfo is None:
            return None
        jst = generated.astimezone(ZoneInfo("Asia/Tokyo"))
    except (ValueError, TypeError, OverflowError):
        return None
    return {
        "date": jst.date().isoformat(),
        "after_close": (jst.hour, jst.minute) >= (15, 30),
    }


def summarize(now: datetime, inputs: dict) -> dict:
    """Pure function: stable issue keys enable transition-only ChatGPT alerts."""
    incidents = []
    components = {}
    for component, path in INPUTS.items():
        data = inputs.get(component)
        if data is None:
            incidents.append({
                "key": component + ":snapshot_missing",
                "component": component,
                "severity": "CRITICAL",
                "kind": "DATA_INCIDENT",
                "message_ja": "実行結果を読み取れません。データ更新またはファイルを確認してください。",
            })
            components[component] = {"status": "UNAVAILABLE", "as_of_date": None}
            continue

        day = data.get("as_of_date") or data.get("date_jst") or data.get("date")
        blockers = data.get("market_data_blockers", data.get("data_blockers", []))
        if not isinstance(blockers, list):
            blockers = ["invalid_blocker_schema"]
        if component == "regime" and data.get("data_status") not in (None, "ok"):
            blockers = blockers + ["regime_data_status_invalid:" + str(data.get("data_status"))]
        if component.startswith("challenger"):
            if data.get("mode") != "SHADOW_ONLY":
                blockers = blockers + ["invalid_paper_mode"]
            if data.get("screen_fresh") is False:
                blockers = blockers + ["screen_stale"]
            if data.get("nav_jpy") is None:
                blockers = blockers + ["nav_missing"]
            unpriced = data.get("unpriced_symbols") or []
            if not isinstance(unpriced, list):
                blockers = blockers + ["invalid_unpriced_schema"]
            else:
                blockers = blockers + ["missing_holding_bar:" + str(symbol) for symbol in unpriced]
        component_incidents = []
        for code in sorted(set(str(x) for x in blockers)):
            kind = classify_blocker(code)
            if kind == "RISK_CONTROL":
                continue  # This is a strategy decision, not a technical outage.
            component_incidents.append({
                "key": component + ":" + code,
                "component": component,
                "severity": "CRITICAL" if kind == "UNKNOWN_BLOCKER" else "WARNING",
                "kind": kind,
                "message_ja": "検証用データまたは実行条件に問題があります: " + code,
            })
        incidents.extend(component_incidents)
        components[component] = {
            "status": "DATA_IMPAIRED" if component_incidents else (
                "RISK_PAUSE" if blockers else "HEALTHY"),
            "as_of_date": day,
            "blockers": blockers,
            "mode": data.get("mode"),
        }

    # Two completed JPX sessions without a snapshot warrant investigation.
    # An archived v2 is intentionally excluded from freshness checks.
    for component, meta in components.items():
        day = meta.get("as_of_date")
        if not day:
            continue
        try:
            observed = datetime.strptime(day, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            continue
        if component != "regime" and not is_jpx_session(observed):
            incidents.append({
                "key": component + ":invalid_session_date",
                "component": component,
                "severity": "WARNING",
                "kind": "DATA_INCIDENT",
                "message_ja": "仮想運用の日付がJPX休場日です。約定や評価の対象日を確認してください。",
            })
            meta["status"] = "DATA_IMPAIRED"
        if completed_jpx_sessions(observed, now) >= 2:
            if meta["status"] in ("HEALTHY", "RISK_PAUSE"):
                meta["status"] = "STALE"
            incidents.append({
                "key": component + ":snapshot_lag",
                "component": component,
                "severity": "WARNING",
                "kind": "DATA_INCIDENT",
                "message_ja": "最新結果がJPXの完了した2営業日以上更新されていません。実行履歴を確認してください。",
            })

    # Optional post-close observer: missing one completed JPX session is material.
    # Do not treat pre-close, weekends or public holidays as completed sessions.
    if "pipeline" in inputs:
        pipeline = inputs["pipeline"]
        if not isinstance(pipeline, dict) or not pipeline.get("date"):
            components["pipeline"] = {"status": "UNAVAILABLE", "as_of_date": None}
            incidents.append({
                "key": "pipeline:snapshot_missing",
                "component": "pipeline",
                "severity": "CRITICAL",
                "kind": "DATA_INCIDENT",
                "message_ja": "統合レポートの生成日時を確認できません。",
            })
        else:
            day = pipeline["date"]
            status = "HEALTHY"
            try:
                observed = datetime.strptime(day, "%Y-%m-%d").date()
                lag = completed_jpx_sessions(observed, now)
            except (ValueError, TypeError):
                lag = None
            if lag is None or not pipeline.get("after_close", False):
                status = "DATA_IMPAIRED"
                incidents.append({
                    "key": "pipeline:invalid_generation_time",
                    "component": "pipeline",
                    "severity": "WARNING",
                    "kind": "DATA_INCIDENT",
                    "message_ja": "統合レポートの生成日時が不正、または引け前です。",
                })
            elif lag >= 1:
                status = "STALE"
                incidents.append({
                    "key": "pipeline:snapshot_lag",
                    "component": "pipeline",
                    "severity": "WARNING",
                    "kind": "DATA_INCIDENT",
                    "message_ja": "直近の完了営業日について統合レポートが更新されていません。",
                })
            components["pipeline"] = {"status": status, "as_of_date": day}

    archived = read_json(ROOT / ARCHIVED_V2)
    components["shadow_v2"] = {
        "status": "ARCHIVED",
        "as_of_date": (archived or {}).get("as_of_date"),
        "mode": (archived or {}).get("mode"),
        "blockers": [],
    }

    incidents.sort(key=lambda x: x["key"])
    signature = hashlib.sha256(
        json.dumps([(x["key"], x["severity"]) for x in incidents],
                   ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema_version": "1.0",
        "generated_at_utc": now.astimezone(timezone.utc).isoformat(),
        "mode": "OBSERVATION_ONLY",
        "overall_status": ("ACTION_REQUIRED" if incidents else
                           "RISK_PAUSE" if any(x["status"] == "RISK_PAUSE"
                                               for x in components.values()) else "HEALTHY"),
        "incident_signature": signature,
        "incidents": incidents,
        "components": components,
        "notification_policy": {
            "channel": "ChatGPT condition watch",
            "trigger": "new, worsened, or resolved incident only",
            "repeat_unchanged": False,
            "human_review": "Check underlying GitHub Actions before attributing cause.",
        },
        "user_action": "不要。実際の証券口座への操作はありません。",
    }


def main():
    now = datetime.now(timezone.utc)
    data = {name: read_json(ROOT / path) for name, path in INPUTS.items()}
    data["pipeline"] = read_pipeline_report(ROOT / "data/integrated_report_latest.md")
    report = summarize(now, data)
    output = ROOT / "data/health/latest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(json.dumps({
        "overall_status": report["overall_status"],
        "incident_signature": report["incident_signature"],
        "incident_count": len(report["incidents"]),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
