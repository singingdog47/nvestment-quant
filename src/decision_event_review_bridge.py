"""Private decision-review bridge. It never executes orders.

Use with verified manifest from operator. The response JSON is intended for a
human-facing reviewer, not for autonomous execution.
"""
import argparse
import csv
import json
from pathlib import Path
from .portfolio_event_preflight import evaluate_portfolio_events
from .event_user_consent import apply_user_consent

def prepare_decision_review(symbols, manifest, as_of_utc, consent=None):
    preflight=evaluate_portfolio_events(symbols,manifest,as_of_utc)
    gate=apply_user_consent(preflight,consent)
    return {
        "review_as_of_utc":as_of_utc,
        "event_preflight":preflight,
        "user_confirmation":gate,
        "analysis_mode":("PROVISIONAL_WITH_EXPLICIT_UNVERIFIED_FLAGS"
                         if gate["state"]=="PROVISIONAL_USER_APPROVED"
                         else "VERIFIED_ONLY" if gate["state"]=="VERIFIED_REVIEW"
                         else "AWAITING_USER_CONFIRMATION"),
        "may_finalize_trade_recommendations":bool(gate["provisional_analysis_allowed"]),
        "may_execute_orders":False,
        "instructions_ja":("未確認の銘柄・情報源・確認日時を明示し、ユーザーに質問してください。"
                           "回答がない場合、暫定的な売買判断を確定しないでください。")
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--symbols",required=True)
    p.add_argument("--manifest",required=True)
    p.add_argument("--as-of-utc",required=True)
    p.add_argument("--consent",help="Private explicit per-review consent JSON")
    p.add_argument("--output",required=True)
    a=p.parse_args()
    with open(a.symbols,encoding="utf-8-sig",newline="") as f:
        symbols=[r["symbol"].strip() for r in csv.DictReader(f) if r.get("symbol","").strip()]
    with open(a.manifest,encoding="utf-8") as f:
        manifest=json.load(f)
    consent=None
    if a.consent:
        with open(a.consent,encoding="utf-8") as f:
            consent=json.load(f)
    result=prepare_decision_review(symbols,manifest,a.as_of_utc,consent)
    out=Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(result["analysis_mode"])
    if result["user_confirmation"]["state"]=="ASK_USER":
        print(result["user_confirmation"]["question_ja"])
        return 3
    return 0

if __name__=="__main__":
    raise SystemExit(main())
