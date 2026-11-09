import unittest
from src.portfolio_event_preflight import evaluate_portfolio_events

class PortfolioEventPreflightTests(unittest.TestCase):
    def test_all_positions_required(self):
        r = evaluate_portfolio_events(["8136", "6701"], [
            {"symbol":"8136", "status":"EVENT_FOUND",
             "checked_at_utc":"2026-11-09T00:15:00Z",
             "published_at_utc":"2026-11-06T06:30:00Z", "reviewed":True,
             "source_url":"https://www.jpx.co.jp/", "source_kind":"JPX_TDNET"}
        ], "2026-11-09T00:15:00Z")
        self.assertEqual(r["blocked"], 1)
        self.assertFalse(r["ready_for_further_review"])
        self.assertEqual(r["positions"][1]["state"], "EVENT_UNVERIFIED")
    def test_all_reviewed_allows_further_review_only(self):
        r = evaluate_portfolio_events(["8136"], [
            {"symbol":"8136", "status":"EVENT_FOUND",
             "checked_at_utc":"2026-11-09T00:15:00Z",
             "published_at_utc":"2026-11-06T06:30:00Z", "reviewed":True,
             "source_url":"https://www.jpx.co.jp/", "source_kind":"JPX_TDNET"}
        ], "2026-11-09T00:15:00Z")
        self.assertTrue(r["ready_for_further_review"])
    def test_duplicate_symbols_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_portfolio_events(["8136","8136"], [], "2026-11-09T00:15:00Z")

if __name__ == "__main__":
    unittest.main()
