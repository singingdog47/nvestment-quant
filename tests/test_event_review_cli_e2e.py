"""End-to-end CLI smoke tests with synthetic private inputs; never upload real holdings."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.event_user_consent import review_fingerprint
from src.portfolio_event_preflight import evaluate_portfolio_events

AS_OF = "2026-11-09T00:15:00Z"

class PrivateEventReviewCLITests(unittest.TestCase):
    def test_unknown_requires_consent_and_approval_is_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            symbols=root/"positions.csv"
            manifest=root/"manifest.json"
            output=root/"review.json"
            consent=root/"consent.json"
            symbols.write_text("symbol\n8136\n6701\n",encoding="utf-8")
            manifest.write_text("[]",encoding="utf-8")
            base=[sys.executable,"-m","src.decision_event_review_bridge",
                  "--symbols",str(symbols),"--manifest",str(manifest),
                  "--as-of-utc",AS_OF,"--output",str(output)]
            first=subprocess.run(base,capture_output=True,text=True,check=False)
            self.assertEqual(first.returncode,3,first.stderr)
            report=json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["analysis_mode"],"AWAITING_USER_CONFIRMATION")
            self.assertFalse(report["may_finalize_trade_recommendations"])
            self.assertFalse(report["may_execute_orders"])
            self.assertEqual(set(report["user_confirmation"]["unverified_symbols"]),{"8136","6701"})
            fingerprint=review_fingerprint(evaluate_portfolio_events(["8136","6701"],[],AS_OF))
            consent.write_text(json.dumps({"approved":True,"review_fingerprint":fingerprint}),encoding="utf-8")
            second=subprocess.run(base+["--consent",str(consent)],capture_output=True,text=True,check=False)
            self.assertEqual(second.returncode,0,second.stderr)
            approved=json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(approved["analysis_mode"],"PROVISIONAL_WITH_EXPLICIT_UNVERIFIED_FLAGS")
            self.assertFalse(approved["may_execute_orders"])
            # A new review timestamp invalidates the old approval.
            new_base=base.copy()
            new_base[new_base.index("--as-of-utc")+1]="2026-11-09T00:16:00Z"
            stale=subprocess.run(new_base+["--consent",str(consent)],capture_output=True,text=True,check=False)
            self.assertEqual(stale.returncode,3,stale.stderr)

    def test_free_feed_wrapper_remains_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"symbols.csv").write_text("symbol\n8136\n",encoding="utf-8")
            (root/"feed.json").write_text(json.dumps({
                "primary_verified":False,"all_symbols_unverified":True,
                "manifest":[{"symbol":"8136","status":"NO_EVENT_CONFIRMED","reviewed":True,
                             "checked_at_utc":AS_OF,"source_kind":"JPX_TDNET",
                             "source_url":"https://www.jpx.co.jp/",
                             "coverage_start_utc":"2026-10-29T00:00:00Z"}]
            }),encoding="utf-8")
            out=root/"out.json"
            p=subprocess.run([sys.executable,"-m","src.decision_event_review_bridge",
                "--symbols",str(root/"symbols.csv"),"--manifest",str(root/"feed.json"),
                "--as-of-utc",AS_OF,"--output",str(out)],
                capture_output=True,text=True,check=False)
            self.assertEqual(p.returncode,3,p.stderr)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["analysis_mode"],
                             "AWAITING_USER_CONFIRMATION")

if __name__=="__main__":
    unittest.main()
