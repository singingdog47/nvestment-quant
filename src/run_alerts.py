from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

from alert_engine import detect_public_alerts


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# Exception Alerts v1.9",
        "",
        f"Generated: {report.get('generated_at')}",
        f"Highest severity: **{report.get('highest_severity')}**",
        "",
        "## Counts",
    ]
    counts = report.get("counts") or {}
    for severity in ("CRITICAL", "WARNING", "WATCH", "INFO"):
        lines.append(f"- {severity}: {counts.get(severity, 0)}")
    lines += ["", "## Alerts"]
    alerts = report.get("alerts") or []
    if not alerts:
        lines.append("- No exception alerts detected.")
    else:
        for a in alerts:
            entity = f" [{a.get('entity')}]" if a.get("entity") else ""
            lines.append(f"- **{a.get('severity')}** {a.get('category')}/{a.get('code')}{entity}: {a.get('title')}")
            lines.append(f"  - {a.get('message')}")
    lines += ["", "## Governance"]
    for rule in report.get("rules") or []:
        lines.append(f"- {rule}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    regime = _read_json(Path("data/regime/market_regime_latest.json"))
    quality = _read_json(Path("data/intelligence/data_quality_latest.json"))
    snapshot = _read_csv(Path("data/intelligence/company_snapshot_latest.csv"))
    events = _read_csv(Path("data/intelligence/company_events_new.csv"))

    out_dir = Path(os.getenv("ALERT_OUTPUT_DIR", "data/alerts"))
    out_dir.mkdir(parents=True, exist_ok=True)
    state_path = out_dir / "alert_state_latest.json"
    previous = _read_json(state_path)

    report = detect_public_alerts(
        regime,
        quality,
        snapshot,
        events,
        previous,
        rank_jump_threshold=float(os.getenv("RANK_ALERT_THRESHOLD", "15")),
        vix_watch=float(os.getenv("ALERT_VIX_WATCH", "20")),
        vix_warning=float(os.getenv("ALERT_VIX_WARNING", "30")),
        vix_critical=float(os.getenv("ALERT_VIX_CRITICAL", "35")),
    )

    public_report = {k: v for k, v in report.items() if k != "state"}
    (out_dir / "alerts_latest.json").write_text(
        json.dumps(public_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    _write_markdown(public_report, out_dir / "alerts_latest.md")
    state_path.write_text(json.dumps(report.get("state") or {}, ensure_ascii=False, indent=2), encoding="utf-8")

    # Public-safe execution metadata only.
    print(json.dumps({
        "version": report.get("version"),
        "status": "ok",
        "highest_severity": report.get("highest_severity"),
        "alert_count": len(report.get("alerts") or []),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
