#!/usr/bin/env python3
"""Research-only AI CDS dispersion monitor. No trades, risk budgets or live recommendations.

Input is an explicitly sourced, licensed CSV export; no fabricated or scraped CDS values.
Data contract: date,entity,group,cds_5y_bp,source,asof_utc
group must be ai or control. Each group must contain at least min_entities
distinct issuers on the same date. Outputs never contain private portfolio data.
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import median


def parse_date(value):
    return date.fromisoformat(value)


def load_panel(path, *, min_entities=3, max_age_days=7, today=None):
    today = today or datetime.now(timezone.utc).date()
    if not Path(path).is_file():
        return [], ["CDS_SOURCE_MISSING"]
    groups = defaultdict(lambda: {"ai": {}, "control": {}})
    warnings = []
    with open(path, encoding="utf-8-sig", newline="") as stream:
        for line_no, row in enumerate(csv.DictReader(stream), start=2):
            try:
                when = parse_date(row["date"].strip())
                entity = row["entity"].strip()
                group = row["group"].strip().lower()
                bp = float(row["cds_5y_bp"])
                source = row["source"].strip()
                asof = datetime.fromisoformat(row["asof_utc"].replace("Z", "+00:00"))
                if group not in ("ai", "control") or not entity or not source:
                    raise ValueError("invalid group/entity/source")
                if not math.isfinite(bp) or not 0 < bp < 5000:
                    raise ValueError("invalid spread")
                if asof.tzinfo is None or asof.astimezone(timezone.utc).date() < when:
                    raise ValueError("invalid source asof")
                if when > today or asof.date() > today:
                    raise ValueError("future observation")
                if entity in groups[when][group]:
                    raise ValueError("duplicate issuer/date/group")
                groups[when][group][entity] = bp
            except (KeyError, ValueError, TypeError) as exc:
                warnings.append(f"REJECT_ROW_{line_no}:{type(exc).__name__}")
    panel = []
    for when in sorted(groups):
        by_group = groups[when]
        a, c = by_group["ai"], by_group["control"]
        if len(a) < min_entities or len(c) < min_entities:
            warnings.append(f"INSUFFICIENT_COVERAGE:{when}")
            continue
        ai = median(a.values())
        control = median(c.values())
        panel.append({"date": when.isoformat(), "ai_median_bp": ai,
                      "control_median_bp": control, "ai_minus_control_bp": ai - control,
                      "ai_count": len(a), "control_count": len(c)})
    if panel and (today - parse_date(panel[-1]["date"])).days > max_age_days:
        warnings.append("STALE_CDS_DATA")
    if not panel:
        warnings.append("NO_COMPARABLE_OBSERVATIONS")
    return panel, warnings


def evaluate(panel, warnings, *, baseline_days=20, min_history=20):
    latest = panel[-1] if panel else None
    result = {"mode": "research_only", "actionable": False, "trade_signal": False,
              "predictive_value_validated": False, "data_status": "unavailable",
              "warnings": warnings, "latest": latest, "trend": None,
              "assessment": "insufficient_data"}
    if not panel or "STALE_CDS_DATA" in warnings:
        return result
    result["data_status"] = "usable_observation"
    if len(panel) <= max(baseline_days, min_history):
        result["assessment"] = "observing_not_enough_history"
        return result
    prior = panel[-(baseline_days + 1)]
    delta = latest["ai_minus_control_bp"] - prior["ai_minus_control_bp"]
    result["trend"] = {"lookback_observations": baseline_days,
                       "differential_change_bp": round(delta, 3)}
    # Diagnostic only. Not a classifier or verified prediction threshold.
    result["assessment"] = "relative_credit_widening" if delta > 0 else "not_widening"
    return result


def forward_study(panel, prices_path, *, horizon=5):
    """Observational 5-session prospective label; compare future close only.

    Signal for T is paired with close(T+1)/close(T), so the same-day return is
    never included. Unfinished windows remain unlabeled.
    """
    if not prices_path or not Path(prices_path).exists():
        return {"status": "price_data_missing", "samples": []}
    with open(prices_path, encoding="utf-8-sig", newline="") as stream:
        rows = sorted([(row["date"], float(row["close"])) for row in csv.DictReader(stream)])
    lookup = {d: i for i, (d, _) in enumerate(rows)}
    samples = []
    for obs in panel:
        i = lookup.get(obs["date"])
        if i is None or i + 1 + horizon >= len(rows) or rows[i + 1][1] <= 0:
            continue
        samples.append({"signal_date": obs["date"],
                        "ai_minus_control_bp": obs["ai_minus_control_bp"],
                        "forward_sessions": horizon,
                        "forward_return": round(rows[i + 1 + horizon][1] / rows[i + 1][1] - 1, 8)})
    return {"status": "unvalidated_observations", "samples": samples}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cds-csv", default="data/ai_credit/source_cds.csv")
    parser.add_argument("--price-csv", default="")
    parser.add_argument("--output", default="data/ai_credit/assessment.json")
    parser.add_argument("--min-entities", type=int, default=3)
    parser.add_argument("--max-age-days", type=int, default=7)
    args = parser.parse_args()
    if args.min_entities < 2 or args.max_age_days < 0:
        parser.error("invalid coverage or freshness requirements")
    panel, warnings = load_panel(args.cds_csv, min_entities=args.min_entities,
                                 max_age_days=args.max_age_days)
    result = evaluate(panel, warnings)
    result["study"] = forward_study(panel, args.price_csv)
    result["observations"] = len(panel)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"AI credit monitor: {result['data_status']} / {result['assessment']} "
          f"/ observations={len(panel)}")


if __name__ == "__main__":
    main()
