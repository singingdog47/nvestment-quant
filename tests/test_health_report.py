"""Unit tests for the observer: no orders, no invented fills."""
import unittest
from datetime import datetime, timezone

from health_report import classify_blocker, summarize

NOW = datetime(2026, 10, 20, 13, 45, tzinfo=timezone.utc)


def healthy():
    return {
        "shadow_v2": {"as_of_date": "2026-10-20", "market_data_blockers": []},
        "ai_ma": {"as_of_date": "2026-10-20", "data_blockers": []},
        "regime": {"date_jst": "2026-10-20", "data_status": "ok"},
    }


class HealthReportTests(unittest.TestCase):
    def test_risk_pause_is_not_incident(self):
        inputs = healthy()
        inputs["shadow_v2"]["market_data_blockers"] = ["market_stress_no_new_entries"]
        result = summarize(NOW, inputs)
        self.assertEqual(result["overall_status"], "RISK_PAUSE")
        self.assertEqual(result["incidents"], [])

    def test_data_failure_separated_from_market_pause(self):
        inputs = healthy()
        inputs["shadow_v2"]["market_data_blockers"] = [
            "market_stress_no_new_entries", "benchmark_bar_unavailable",
            "screen_outdated_no_new_trades"]
        result = summarize(NOW, inputs)
        self.assertEqual(result["overall_status"], "ACTION_REQUIRED")
        self.assertEqual(len(result["incidents"]), 2)
        self.assertTrue(all(x["kind"] == "DATA_INCIDENT" for x in result["incidents"]))

    def test_missing_snapshot_is_critical(self):
        inputs = healthy()
        inputs["ai_ma"] = None
        result = summarize(NOW, inputs)
        self.assertEqual(result["incidents"][0]["severity"], "CRITICAL")

    def test_signature_stable_when_blockers_reordered(self):
        inputs = healthy()
        inputs["ai_ma"]["data_blockers"] = ["benchmark_price_unavailable", "entry_missing_bar:5351.T"]
        a = summarize(NOW, inputs)["incident_signature"]
        inputs["ai_ma"]["data_blockers"].reverse()
        b = summarize(NOW, inputs)["incident_signature"]
        self.assertEqual(a, b)

    def test_unrecognized_blocker_not_silently_ignored(self):
        self.assertEqual(classify_blocker("novel_bad_state"), "UNKNOWN_BLOCKER")
        inputs = healthy()
        inputs["shadow_v2"]["market_data_blockers"] = ["novel_bad_state"]
        result = summarize(NOW, inputs)
        self.assertEqual(result["incidents"][0]["severity"], "CRITICAL")

    def test_weekend_does_not_raise_immediate_stale_alert(self):
        inputs = healthy()
        inputs["shadow_v2"]["as_of_date"] = "2026-10-16"
        saturday = datetime(2026, 10, 17, 14, tzinfo=timezone.utc)
        result = summarize(saturday, inputs)
        self.assertFalse(any(x["key"].endswith("snapshot_lag") for x in result["incidents"]))


if __name__ == "__main__":
    unittest.main()
