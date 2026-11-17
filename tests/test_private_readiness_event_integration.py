"""Private readiness integration: real normalized holdings format, synthetic values."""
import csv
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from src.private_runtime_readiness import write_private_event_review

class PrivateReadinessEventTests(unittest.TestCase):
    def test_private_holdings_codes_and_unknowns(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            portfolio=directory/"portfolio.csv"
            with portfolio.open("w",encoding="utf-8",newline="") as handle:
                writer=csv.DictWriter(handle,fieldnames=["code","asset_type","ticker"])
                writer.writeheader()
                writer.writerows([
                    {"code":"8136","asset_type":"国内株式","ticker":"8136.T"},
                    {"code":"8136","asset_type":"国内株式","ticker":"8136.T"},
                    {"code":"6701","asset_type":"国内株式","ticker":"6701.T"},
                    {"code":"VTI","asset_type":"米国株式","ticker":"VTI"},
                ])
            result=write_private_event_review(portfolio,directory,
                now=datetime(2026,11,9,1,0,tzinfo=timezone.utc))
            self.assertEqual(result["total"],2)
            self.assertEqual(result["unverified"],2)
            self.assertEqual(result["analysis_mode"],"AWAITING_USER_CONFIRMATION")
            self.assertFalse(result["may_execute_orders"])
            saved=json.loads((directory/"event_review_latest.json").read_text(encoding="utf-8"))
            self.assertEqual([p["symbol"] for p in saved["event_preflight"]["positions"]],
                             ["8136","6701"])
            self.assertEqual((directory/"event_review_latest.json").stat().st_mode & 0o777,0o600)
    def test_malformed_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            (directory/"portfolio.csv").write_text("code\n8136\n",encoding="utf-8")
            (directory/"event_disclosures_verified.json").write_text('{"verified":true}',encoding="utf-8")
            with self.assertRaises(ValueError):
                write_private_event_review(directory/"portfolio.csv",directory,
                    now=datetime(2026,11,9,1,0,tzinfo=timezone.utc))

if __name__=="__main__":
    unittest.main()
