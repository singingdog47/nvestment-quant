"""AI/M&A hypothesis historical audit with strict point-in-time evidence.

Does NOT claim to backtest AI/M&A alpha from value-screen observations.
Scans immutable dated candidate snapshots + independently sourced corporate
action events. Missing history is a result, not license to backfill today.
"""
from __future__ import annotations
import csv
import json
import math
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

JST=ZoneInfo("Asia/Tokyo")
ROOT=Path("data")
OUT=ROOT/"ai_ma_shadow"/"historical"

def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig",newline="") as fh:
        return list(csv.DictReader(fh))

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}

def parse_time(value):
    if not value: return None
    try:
        x=datetime.fromisoformat(str(value).replace("Z","+00:00"))
        return x if x.tzinfo else None
    except ValueError:
        return None

def as_float(x):
    try:
        f=float(x)
        return f if math.isfinite(f) else None
    except (ValueError,TypeError): return None

def session_days(root):
    p=Path(root)/"ai_ma_shadow"/"history"
    if not p.exists(): return []
    return sorted(p.glob("????-??-??.json"))

def assess(root=ROOT):
    root=Path(root)
    decisions=read_csv(root/"validation"/"outcomes.csv")
    historical_snapshots=session_days(root)
    events=read_csv(root/"ai_ma_shadow"/"reference"/"verified_corporate_events.csv")
    count_1w=sum(x.get("horizon")=="1w" and as_float(x.get("excess_return")) is not None for x in decisions)
    count_1m=sum(x.get("horizon")=="1m" and as_float(x.get("excess_return")) is not None for x in decisions)
    first_outcome=min((x.get("captured_at") for x in decisions if parse_time(x.get("captured_at"))),default=None)
    last_outcome=max((x.get("captured_at") for x in decisions if parse_time(x.get("captured_at"))),default=None)
    issues=[]; valid_events=[]; invalid_events=[]
    for event in events:
        required=("symbol","announcement_date","event_type","source_url","source_published_at")
        if any(not event.get(k) for k in required):
            invalid_events.append({"symbol":event.get("symbol"),"reason":"missing_event_evidence"})
            continue
        dt=parse_time(event["source_published_at"])
        try: announced=date.fromisoformat(event["announcement_date"])
        except ValueError:
            invalid_events.append({"symbol":event.get("symbol"),"reason":"invalid_date"})
            continue
        if not dt or dt.astimezone(JST).date()<announced:
            invalid_events.append({"symbol":event.get("symbol"),"reason":"invalid_provenance_timing"})
            continue
        valid_events.append(event)
    sampled_snapshots=[]
    for path in historical_snapshots:
        doc=read_json(path)
        snapday=doc.get("as_of_date")
        if snapday!=path.stem or doc.get("mode")!="SHADOW_ONLY":
            issues.append({"snapshot":path.name,"problem":"mismatch_or_nonpaper"})
            continue
        for c in doc.get("candidates",[]):
            if not c.get("id") or not c.get("signal_date") and not c.get("eligible"):
                # Stored v1 summary does not include signal_date for each candidate,
                # so snapshot date is explicitly the only date available.
                continue
        sampled_snapshots.append({"date":snapday,"qualified":doc.get("qualified_count"),
            "count":doc.get("screened_jp_count")})
    # Historical outcome entries date back to Aug 2026 but lack the contemporaneous
    # AI/ownership/valuation score snapshots. Never pretend their rank was an AI signal.
    return {
        "version":"1.0.0","strategy":"AI_restructuring_and_MA_optional_value",
        "status":"INSUFFICIENT_POINT_IN_TIME_AI_MA_EVIDENCE",
        "historical_public_validation":{
            "first_prediction_captured_at":first_outcome,
            "last_prediction_captured_at":last_outcome,
            "usable_outcomes_1w":count_1w,"usable_outcomes_1m":count_1m,
            "is_AI_MA_target_labeled":False,
            "usable_for_market_baseline_only":True,
        },
        "paper_cohort_snapshots":{
            "usable_days":len(sampled_snapshots),"summary":sampled_snapshots[-12:],
            "issues":issues
        },
        "corporate_event_evidence":{
            "verified_events":len(valid_events),
            "unverified_or_invalid_events":len(invalid_events),
            "event_file_present":(root/"ai_ma_shadow"/"reference"/"verified_corporate_events.csv").exists(),
            "valid_events":valid_events[:30],"invalid_events":invalid_events[:30],
        },
        "historical_ai_operating_evidence":{
            "point_in_time_ai_adoption_and_sga_snapshots":0,
            "status":"MISSING",
            "reason":"Original financial disclosure date and company operations not tracked historically."
        },
        "matched_value_only_control":{
            "status":"NOT_ESTIMABLE",
            "reason":"No point-in-time full-universe valuation snapshots, survival history, delisting/TOB proceeds or return calendar for both strategies."
        },
        "alpha_estimate":None,"takeover_probability_estimate":None,
        "trial_result":"NO_STATISTICAL_CONCLUSION",
        "requirements_to_validate":[
            "Archived full-universe monthly constituent and delisted-ticker universe",
            "Financial fundamentals aligned to actual publication timestamps",
            "AI-intensity and SG&A cost model with evidence dated before signal",
            "Shareholder control/free float and approved M&A events with announcement dates",
            "Corporate-action adjusted total returns, TOB cash settlement and brokerage cost assumptions",
            "Risk/sector/cap/liquidity matched value-only control and purged walk-forward splits"
        ],
        "reason":"Existing 1w/1m outcomes measure prior standard screen, not causal incremental AI/M&A factors."
    }

def run(root=ROOT,out=OUT):
    payload=assess(root)
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    (out/"historical_audit_latest.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    l=["# AI/M&A historical audit — point-in-time evidence",
       "Result: **NO_STATISTICAL_CONCLUSION**; do not treat ordinary value factors as a validated AI/M&A model.",
       f"Standard historical 1w outcomes: {payload['historical_public_validation']['usable_outcomes_1w']}",
       f"Standard historical 1m outcomes: {payload['historical_public_validation']['usable_outcomes_1m']}",
       f"Prospective AI/M&A shadow historical snapshots: {payload['paper_cohort_snapshots']['usable_days']}",
       f"Verified corporate events: {payload['corporate_event_evidence']['verified_events']}",
       "", "## Blocking data gaps"]
    l+=["- "+x for x in payload["requirements_to_validate"]]
    (out/"historical_audit_latest.md").write_text("\n".join(l)+"\n",encoding="utf-8")
    return payload

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False))
