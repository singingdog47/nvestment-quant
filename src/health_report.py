"""Human-readable, fail-closed health snapshot for no-money quant research.

This is a reporting layer, NOT an order executor or an automatic data repairer.
ChatGPT's condition-watch automation can read data/health/latest.json and the
underlying ledgers, and notify only on meaningful incident transitions.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "shadow_v2": "data/shadow_swing_v2/latest.json",
    "ai_ma": "data/ai_ma_shadow/latest.json",
    "regime": "data/regime/market_regime_latest.json",
}
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

        day = data.get("as_of_date") or data.get("date_jst")
        blockers = data.get("market_data_blockers", data.get("data_blockers", []))
        if not isinstance(blockers, list):
            blockers = ["invalid_blocker_schema"]
        if component == "regime" and data.get("data_status") not in (None, "ok"):
            blockers = blockers + ["regime_data_status_invalid:" + str(data.get("data_status"))]
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

    # Do not mistake weekend/holiday delays for outages. Detect sustained
    # staleness only after two or more elapsed weekdays; the ChatGPT watcher
    # also checks exchange holidays and workflow schedules before alerting.
    jst = now.astimezone(ZoneInfo("Asia/Tokyo"))
    for component, meta in components.items():
        day = meta.get("as_of_date")
        if not day:
            continue
        try:
            observed = datetime.strptime(day, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            continue
        weekdays = sum(
            datetime.fromordinal(observed.toordinal() + offset).weekday() < 5
            for offset in range(1, max(1, (jst.date() - observed).days) + 1)
        )
        if weekdays >= 2 and jst.hour >= 22:
            incidents.append({
                "key": component + ":snapshot_lag",
                "component": component,
                "severity": "WARNING",
                "kind": "DATA_INCIDENT",
                "message_ja": "最新結果が複数営業日更新されていません。休場日と実行履歴を確認してください。",
            })

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
