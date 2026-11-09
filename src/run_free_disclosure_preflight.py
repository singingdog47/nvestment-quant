"""Operator-invoked free candidate collection. No broker holdings are committed.

Run: python -m src.run_free_disclosure_preflight --symbols /private/codes.csv --output /private/events.json
CSV has symbol column only. Candidate output is NOT a verified event manifest.
"""
import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from .yanoshin_disclosure_adapter import fetch_candidate_atom
from .disclosure_candidates import parse_disclosure_candidates, candidate_manifest

def collect(symbols, fetcher=fetch_candidate_atom, delay_seconds=1.0, sleeper=time.sleep):
    out=[]
    failures={}
    for i, code in enumerate(symbols):
        if i:
            sleeper(delay_seconds)
        try:
            feed=fetcher(code)
            candidates=parse_disclosure_candidates(feed["candidate_disclosures"], [code])
            out.extend(candidate_manifest(candidates, datetime.now(timezone.utc).isoformat()))
        except Exception as exc:
            failures[code]=type(exc).__name__
            out.extend(candidate_manifest({code: []}, datetime.now(timezone.utc).isoformat()))
    return {"source":"YANOSHIN_UNOFFICIAL_ATOM", "primary_verified":False,
            "all_symbols_unverified":True, "failures":failures, "manifest":out}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--symbols",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--delay-seconds",type=float,default=1.0)
    args=p.parse_args()
    if args.delay_seconds < 1.0:
        p.error("Minimum 1 second between requests")
    with open(args.symbols,encoding="utf-8-sig",newline="") as f:
        symbols=list(dict.fromkeys(r["symbol"].strip().upper() for r in csv.DictReader(f)
                                  if r.get("symbol","").strip()))
    if not symbols:
        p.error("No symbols")
    result=collect(symbols,delay_seconds=args.delay_seconds)
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Candidate checks {len(symbols)}, failures {len(result['failures'])}; all require primary verification")
    return 2 if result["failures"] else 0

if __name__=="__main__":
    raise SystemExit(main())
