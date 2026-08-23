from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


def _fmt_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.2f}%"


def build_validation_report(root: str | Path = ".") -> Path:
    root = Path(root)
    outcomes = root / "data/validation/outcomes.csv"
    rows: list[dict[str, Any]] = []
    if outcomes.exists():
        with outcomes.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))

    by_horizon: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_regime: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_action: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_horizon[row.get("horizon", "unknown")].append(row)
        by_regime[(row.get("market_regime", "unknown"), row.get("horizon", "unknown"))].append(row)
        by_action[(row.get("recommended_action", "unknown"), row.get("horizon", "unknown"))].append(row)

    def stats(group: list[dict[str, Any]]) -> tuple[int, float | None, float | None]:
        vals = []
        for r in group:
            try:
                vals.append(float(r["return"]))
            except (KeyError, TypeError, ValueError):
                pass
        if not vals:
            return 0, None, None
        return len(vals), mean(vals), sum(v > 0 for v in vals) / len(vals)

    lines = [
        "# Investment Quant v1.7 Validation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.",
        "",
        "## Screening outcome by horizon",
        "",
        "| Horizon | Observations | Average return | Win rate |",
        "|---|---:|---:|---:|",
    ]
    for horizon in ("1w", "1m", "3m"):
        n, avg, win = stats(by_horizon.get(horizon, []))
        lines.append(f"| {horizon} | {n} | {_fmt_pct(avg)} | {_fmt_pct(win)} |")

    lines += ["", "## Outcome by market regime", "", "| Regime | Horizon | N | Avg return | Win rate |", "|---|---|---:|---:|---:|"]
    for (regime, horizon), group in sorted(by_regime.items()):
        n, avg, win = stats(group)
        lines.append(f"| {regime} | {horizon} | {n} | {_fmt_pct(avg)} | {_fmt_pct(win)} |")

    lines += ["", "## Outcome by recommended action", "", "| Action | Horizon | N | Avg return | Win rate |", "|---|---|---:|---:|---:|"]
    for (action, horizon), group in sorted(by_action.items()):
        n, avg, win = stats(group)
        lines.append(f"| {action} | {horizon} | {n} | {_fmt_pct(avg)} | {_fmt_pct(win)} |")

    lines += [
        "",
        "## Interpretation guardrails",
        "",
        "- Do not change factor weights automatically from small samples.",
        "- Separate model error from data-quality failure and regime misclassification.",
        "- Promote a model change only after an explicit human review and version bump.",
        "- Human brokerage actions remain private and are joined by decision_id outside the public repository.",
    ]

    out = root / "data/validation/validation_report_latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(rows),
        "horizons": {},
    }
    for horizon in ("1w", "1m", "3m"):
        n, avg, win = stats(by_horizon.get(horizon, []))
        metrics["horizons"][horizon] = {"n": n, "average_return": avg, "win_rate": win}
    (root / "data/validation/validation_metrics_latest.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return out
