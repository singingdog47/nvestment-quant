"""Unit tests for the observer: no orders, no invented fills."""
import unittest
from datetime import datetime, timezone

from health_report import classify_blocker, summarize, completed_jpx_sessions

NOW = datetime(2026, 10, 20, 13, 45, tzinfo=timezone.utc)


def healthy():
    return {
        "challenger1": {"date": "2026-10-20", "mode": "SHADOW_ONLY", "status": "OK", "nav_jpy": 1000000, "screen_fresh": True, "unpriced_symbols": []},
        "challenger2": {"date": "2026-10-20", "mode": "SHADOW_ONLY", "status": "OK", "nav_jpy": 5000000, "screen_fresh": True, "unpriced_symbols": []},
        "ai_ma": {"as_of_date": "2026-10-20", "data_blockers": []},
        "regime": {"date_jst": "2026-10-20", "data_status": "ok"},
    }


class HealthReportTests(unittest.TestCase):
    def test_risk_pause_is_not_incident(self):
        inputs = healthy()
        inputs["challenger1"]["market_data_blockers"] = ["market_stress_no_new_entries"]
        result = summarize(NOW, inputs)
        self.assertEqual(result["overall_status"], "RISK_PAUSE")
        self.assertEqual(result["incidents"], [])

    def test_data_failure_separated_from_market_pause(self):
        inputs = healthy()
        inputs["challenger1"]["market_data_blockers"] = [
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
        inputs["challenger1"]["market_data_blockers"] = ["novel_bad_state"]
        result = summarize(NOW, inputs)
        self.assertEqual(result["incidents"][0]["severity"], "CRITICAL")

    def test_weekend_does_not_raise_immediate_stale_alert(self):
        inputs = healthy()
        inputs["challenger1"]["date"] = "2026-10-16"
        saturday = datetime(2026, 10, 17, 14, tzinfo=timezone.utc)
        result = summarize(saturday, inputs)
        self.assertFalse(any(x["key"].endswith("snapshot_lag") for x in result["incidents"]))

    def test_active_challenger_date_and_missing_prices_are_monitored(self):
        inputs = healthy()
        inputs["challenger2"]["unpriced_symbols"] = ["3932.T"]
        result = summarize(NOW, inputs)
        self.assertEqual(result["components"]["challenger2"]["as_of_date"], "2026-10-20")
        self.assertIn("challenger2:missing_holding_bar:3932.T", [x["key"] for x in result["incidents"]])
        self.assertEqual(result["components"]["shadow_v2"]["status"], "ARCHIVED")

    def test_jpx_holiday_not_counted_as_completed_session(self):
        from datetime import date
        on_holiday = datetime(2026, 11, 3, 15, 0, tzinfo=timezone.utc)
        self.assertEqual(completed_jpx_sessions(date(2026, 11, 2), on_holiday), 0)
        inputs = healthy()
        for key in ("challenger1", "challenger2", "ai_ma", "regime"):
            inputs[key]["date" if key.startswith("challenger") else "as_of_date" if key == "ai_ma" else "date_jst"] = "2026-11-02"
        self.assertFalse(any(x["key"].endswith(":snapshot_lag") for x in summarize(on_holiday, inputs)["incidents"]))

    def test_two_completed_sessions_trigger_lag_not_one(self):
        from datetime import date
        tuesday_morning = datetime(2026, 11, 3, 1, 0, tzinfo=timezone.utc)
        self.assertEqual(completed_jpx_sessions(date(2026, 10, 29), tuesday_morning), 2)
        inputs = healthy()
        inputs["challenger2"]["date"] = "2026-10-29"
        result = summarize(tuesday_morning, inputs)
        self.assertIn("challenger2:snapshot_lag", [x["key"] for x in result["incidents"]])
        self.assertEqual(result["components"]["challenger2"]["status"], "STALE")

    def test_ai_ma_weekend_snapshot_is_invalid_not_a_valid_trading_day(self):
        inputs = healthy()
        inputs["ai_ma"]["as_of_date"] = "2026-10-31"
        result = summarize(datetime(2026, 11, 2, 15, 0, tzinfo=timezone.utc), inputs)
        self.assertIn("ai_ma:invalid_session_date", [x["key"] for x in result["incidents"]])
        self.assertEqual(result["components"]["ai_ma"]["status"], "DATA_IMPAIRED")


if __name__ == "__main__":
    unittest.main()
