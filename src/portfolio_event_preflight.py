"""Batch event preflight from a private position symbol list and verified event manifest.

No scraping; upstream must supply trustworthy event records and checked timestamps.
"""
import argparse
import csv
import json
from pathlib import Path
from .earnings_event_gate import assess_event_gate

def evaluate_portfolio_events(symbols, manifest, as_of_utc):
    if len(symbols) != len(set(symbols)):
        raise ValueError("duplicate symbols")
    if not isinstance(manifest, list):
        raise ValueError("manifest must be a JSON array of per-symbol records")
    manifest_symbols = [str(x["symbol"]) for x in manifest]
    if len(manifest_symbols) != len(set(manifest_symbols)):
        raise ValueError("duplicate manifest symbols; cannot select authoritative record")
    records = {str(x["symbol"]): x for x in manifest}
    out = []
    for symbol in symbols:
        rec = records.get(symbol, {})
        out.append(assess_event_gate(
            symbol, as_of_utc,
            event_checked_at_utc=rec.get("checked_at_utc"),
            event_status=rec.get("status", "UNKNOWN"),
            event_published_at_utc=rec.get("published_at_utc"),
            event_reviewed=rec.get("reviewed", False),
            source_url=rec.get("source_url"), source_kind=rec.get("source_kind"),
            coverage_start_utc=rec.get("coverage_start_utc"),
        ))
    blocked = [x for x in out if x["decision_gate"].startswith("BLOCK")]
    return {"as_of_utc": as_of_utc, "total": len(out),
            "approval_required": bool(blocked),
            "approval_question_ja": ("決算・適時開示が未確認の銘柄があります。未確認のまま暫定的な売買判断を続けてよいですか？" if blocked else None),
            "approval_scope": "THIS_REVIEW_ONLY",
            "approval_status": "PENDING" if blocked else "NOT_NEEDED",
            "verified": len(out)-len(blocked), "blocked": len(blocked),
            "ready_for_further_review": not blocked, "positions": out}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--symbols", required=True, help="Private CSV with symbol column")
    p.add_argument("--manifest", required=True, help="Private JSON array of verified event checks")
    p.add_argument("--as-of-utc", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    with open(a.symbols, encoding="utf-8-sig", newline="") as f:
        symbols = [str(r["symbol"]).strip() for r in csv.DictReader(f) if r["symbol"].strip()]
    with open(a.manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    result = evaluate_portfolio_events(symbols, manifest, a.as_of_utc)
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    Path(a.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Event gate: {result['verified']}/{result['total']} verified; {result['blocked']} blocked")
    return 0 if result["ready_for_further_review"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
