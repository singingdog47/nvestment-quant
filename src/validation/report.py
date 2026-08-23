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

    def stats(group: list[dict[str, Any]]) -> dict[str, Any]:
        vals: list[float] = []
        excess: list[float] = []
        for r in group:
            try:
                vals.append(float(r["return"]))
            except (KeyError, TypeError, ValueError):
                pass
            try:
                if r.get("excess_return") not in (None, ""):
                    excess.append(float(r["excess_return"]))
            except (TypeError, ValueError):
                pass
        return {
            "n": len(vals),
            "average_return": mean(vals) if vals else None,
            "win_rate": (sum(v > 0 for v in vals) / len(vals)) if vals else None,
            "benchmark_n": len(excess),
            "average_excess_return": mean(excess) if excess else None,
            "outperform_rate": (sum(v > 0 for v in excess) / len(excess)) if excess else None,
        }

    lines = [
        "# Investment Quant Validation Report v2.1",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "This report evaluates recorded decisions ex post. It is diagnostic evidence, not a trading instruction.",
        "Benchmark-relative metrics are preferred for judging signal quality; missing benchmark data is not imputed.",
        "",
        "## Screening outcome by horizon",
        "",
        "| Horizon | N | Avg return | Win rate | Benchmark N | Avg excess return | Outperform rate |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for horizon in ("1w", "1m", "3m"):
        s = stats(by_horizon.get(horizon, []))
        lines.append(
            f"| {horizon} | {s['n']} | {_fmt_pct(s['average_return'])} | {_fmt_pct(s['win_rate'])} | "
            f"{s['benchmark_n']} | {_fmt_pct(s['average_excess_return'])} | {_fmt_pct(s['outperform_rate'])} |"
        )

    lines += [
        "",
        "## Outcome by market regime",
        "",
        "| Regime | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for (regime, horizon), group in sorted(by_regime.items()):
        s = stats(group)
        lines.append(
            f"| {regime} | {horizon} | {s['n']} | {_fmt_pct(s['average_return'])} | {s['benchmark_n']} | "
            f"{_fmt_pct(s['average_excess_return'])} | {_fmt_pct(s['outperform_rate'])} |"
        )

    lines += [
        "",
        "## Outcome by recommended action",
        "",
        "| Action | Horizon | N | Avg return | Benchmark N | Avg excess | Outperform |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for (action, horizon), group in sorted(by_action.items()):
        s = stats(group)
        lines.append(
            f"| {action} | {horizon} | {s['n']} | {_fmt_pct(s['average_return'])} | {s['benchmark_n']} | "
            f"{_fmt_pct(s['average_excess_return'])} | {_fmt_pct(s['outperform_rate'])} |"
        )

    lines += [
        "",
        "## Interpretation guardrails",
        "",
        "- Japanese equities use 1306.T as the TOPIX-linked benchmark proxy; explicit US markets use SPY.",
        "- Unknown markets are left without benchmark attribution rather than guessed.",
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
        metrics["horizons"][horizon] = stats(by_horizon.get(horizon, []))
    (root / "data/validation/validation_metrics_latest.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return out
