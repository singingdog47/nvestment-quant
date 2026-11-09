import unittest
from src.earnings_event_gate import assess_event_gate

NOW = "2026-11-09T00:15:00Z"

class EarningsEventGateTests(unittest.TestCase):
    def test_missing_calendar_fails_closed(self):
        r = assess_event_gate("8136", NOW)
        self.assertEqual(r["state"], "EVENT_UNVERIFIED")
    def test_sanrio_recent_earnings_requires_review(self):
        r = assess_event_gate("8136", NOW, NOW, "EVENT_FOUND", "2026-11-06T06:30:00Z")
        self.assertEqual(r["state"], "EVENT_REVIEW_REQUIRED")
    def test_sanrio_reviewed_not_autotrade(self):
        r = assess_event_gate("8136", NOW, NOW, "EVENT_FOUND", "2026-11-06T06:30:00Z", True)
        self.assertEqual(r["decision_gate"], "ALLOW_FURTHER_REVIEW_NOT_AUTOTRADE")
    def test_stale_check_is_unverified(self):
        r = assess_event_gate("6701", NOW, "2026-11-06T00:00:00Z", "NO_EVENT_CONFIRMED")
        self.assertEqual(r["state"], "EVENT_UNVERIFIED")
    def test_future_check_is_unverified(self):
        r = assess_event_gate("6701", NOW, "2026-11-10T00:00:00Z", "NO_EVENT_CONFIRMED")
        self.assertEqual(r["state"], "EVENT_UNVERIFIED")

if __name__ == "__main__":
    unittest.main()
