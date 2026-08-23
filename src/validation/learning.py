from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any

VERSION = "2.1.0"
MIN_SEGMENT_N = 20
MIN_CHANGE_N = 60


def _f(v: Any) -> float | None:
    try:
        if v in (None, ""):
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def _stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    vals = [_f(r.get("return")) for r in rows]
    vals = [v for v in vals if v is not None]
    excess = [_f(r.get("excess_return")) for r in rows]
    excess = [v for v in excess if v is not None]
    downs = [_f(r.get("max_down")) for r in rows]
    downs = [v for v in downs if v is not None]
    return {
        "n": len(vals),
        "mean_return": mean(vals) if vals else None,
        "median_return": median(vals) if vals else None,
        "win_rate": (sum(v > 0 for v in vals) / len(vals)) if vals else None,
        "mean_max_down": mean(downs) if downs else None,
        "benchmark_n": len(excess),
        "mean_excess_return": mean(excess) if excess else None,
        "median_excess_return": median(excess) if excess else None,
        "outperform_rate": (sum(v > 0 for v in excess) / len(excess)) if excess else None,
        "benchmark_coverage": (len(excess) / len(vals)) if vals else 0.0,
    }


def _rank_bucket(rank: int | None) -> str:
    if rank is None:
        return "unknown"
    if rank == 1:
        return "top1"
    if rank <= 3:
        return "top3"
    if rank <= 10:
        return "top10"
    return "other"


def build_learning_summary(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    path = root / "data/validation/outcomes.csv"
    rows: list[dict[str, Any]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))

    by_horizon: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_action: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_regime: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_rank: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_model: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for r in rows:
        h = r.get("horizon") or "unknown"
        by_horizon[h].append(r)
        by_action[(r.get("recommended_action") or "unknown", h)].append(r)
        by_regime[(r.get("market_regime") or "unknown", h)].append(r)
        try:
            rank = int(float(r.get("rank") or 0)) or None
        except (TypeError, ValueError):
            rank = None
        by_rank[(_rank_bucket(rank), h)].append(r)
        by_model[(r.get("model_version") or "unknown", h)].append(r)

    segments = {
        "horizon": {k: _stats(v) for k, v in sorted(by_horizon.items())},
        "action": {f"{k[0]}|{k[1]}": _stats(v) for k, v in sorted(by_action.items())},
        "regime": {f"{k[0]}|{k[1]}": _stats(v) for k, v in sorted(by_regime.items())},
        "rank_bucket": {f"{k[0]}|{k[1]}": _stats(v) for k, v in sorted(by_rank.items())},
        "model_version": {f"{k[0]}|{k[1]}": _stats(v) for k, v in sorted(by_model.items())},
    }

    findings: list[dict[str, Any]] = []
    for dimension in ("action", "regime", "rank_bucket"):
        for key, s in segments[dimension].items():
            n = int(s.get("benchmark_n") or 0)
            if n < MIN_SEGMENT_N:
                continue
            avg = s.get("mean_excess_return")
            win = s.get("outperform_rate")
            if avg is not None and avg < 0 and win is not None and win < 0.45:
                findings.append({
                    "severity": "WATCH",
                    "dimension": dimension,
                    "segment": key,
                    "message": "Benchmark-relative performance is historically weak; review assumptions before increasing its influence.",
                    "n": n,
                    "metric": "excess_return",
                })
            elif avg is not None and avg > 0 and win is not None and win > 0.55:
                findings.append({
                    "severity": "INFO",
                    "dimension": dimension,
                    "segment": key,
                    "message": "Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.",
                    "n": n,
                    "metric": "excess_return",
                })

    matured_absolute = sum(int(x.get("n") or 0) for x in segments["horizon"].values())
    matured_relative = sum(int(x.get("benchmark_n") or 0) for x in segments["horizon"].values())
    change_gate = {
        "eligible_for_model_change_review": matured_relative >= MIN_CHANGE_N,
        "matured_observations": matured_absolute,
        "benchmark_relative_observations": matured_relative,
        "minimum_required": MIN_CHANGE_N,
        "basis": "benchmark_relative_observations",
        "rule": "Even when eligible, factor weights must not change automatically; require explicit human review, robustness checks, and a version bump.",
    }

    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rows": len(rows),
        "segments": segments,
        "findings": findings,
        "change_gate": change_gate,
        "known_limits": [
            "Benchmark assignment is deterministic: Japanese equities use 1306.T (TOPIX-linked ETF proxy); explicit US markets use SPY (S&P 500 ETF proxy). Unknown markets are left without a benchmark rather than inferred.",
            "Pre-v2.1 outcome rows may have blank benchmark fields and are excluded from benchmark-relative findings until new relative observations mature.",
            "Small samples can create false patterns; segment findings are suppressed below the minimum benchmark-relative sample threshold.",
            "The engine proposes review targets only and never changes weights or places orders automatically.",
        ],
    }


def write_learning_outputs(root: str | Path = ".") -> tuple[Path, Path]:
    root = Path(root)
    summary = build_learning_summary(root)
    out_dir = root / "data/validation"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "learning_latest.json"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Investment Quant Validation Learning v2.1",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "This is a diagnostic learning layer. It does not automatically change factor weights or issue orders.",
        "",
        "## Model-change gate",
        f"- Matured absolute-return observations: {summary['change_gate']['matured_observations']}",
        f"- Benchmark-relative observations: {summary['change_gate']['benchmark_relative_observations']}",
        f"- Minimum benchmark-relative observations for review: {summary['change_gate']['minimum_required']}",
        f"- Eligible for human model-change review: {summary['change_gate']['eligible_for_model_change_review']}",
        "",
        "## Findings",
    ]
    if summary["findings"]:
        for x in summary["findings"]:
            lines.append(f"- [{x['severity']}] {x['dimension']} / {x['segment']} (n={x['n']}): {x['message']}")
    else:
        lines.append("- No statistically gated benchmark-relative review finding yet.")
    lines += ["", "## Known limits"] + [f"- {x}" for x in summary["known_limits"]]
    md_path = out_dir / "learning_latest.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
