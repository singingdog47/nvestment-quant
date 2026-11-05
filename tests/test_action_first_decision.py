"""Risk-first decisions remain independent of the neutral regime score."""
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from action_first_watch import decide

NOW = datetime(2026, 11, 6, tzinfo=timezone.utc)

def quote(pct, price=100):
    return {"status": "OK", "change_pct": pct, "price": price}

class TestActionFirst(unittest.TestCase):
    def test_future_crash_overrides_neutral(self):
        self.assertEqual(decide({"NIKKEI_FUT": quote(-5.8), "VIX": quote(1, 16)}, NOW)["risk_level"], "CRITICAL")
    def test_sp500_crash(self):
        self.assertEqual(decide({"SP500": quote(-4.4)}, NOW)["risk_level"], "CRITICAL")
    def test_nasdaq_defensive(self):
        self.assertEqual(decide({"NASDAQ": quote(-3.1)}, NOW)["risk_level"], "DEFENSIVE")
    def test_vix_defensive(self):
        self.assertEqual(decide({"VIX": quote(10, 26)}, NOW)["risk_level"], "DEFENSIVE")
    def test_no_sources_does_not_mean_safe(self):
        self.assertEqual(decide({"NIKKEI_FUT": {"status": "UNVERIFIED"}}, NOW)["risk_level"], "UNVERIFIED")
    def test_normal_is_not_buy(self):
        self.assertEqual(decide({"SP500": quote(0.8)}, NOW)["market_decision"], "NO_FORCED_TRADE")
    def test_never_trades_or_exposes_private_holdings(self):
        x = decide({"NIKKEI_FUT": quote(-5.8)}, NOW)
        self.assertEqual(x["execution"], "ADVISORY_ONLY")
        self.assertIs(x["private_portfolio_used"], False)

if __name__ == "__main__":
    unittest.main()
