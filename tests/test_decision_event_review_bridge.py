import unittest
from src.decision_event_review_bridge import prepare_decision_review
from src.event_user_consent import review_fingerprint
from src.portfolio_event_preflight import evaluate_portfolio_events

NOW="2026-11-09T00:15:00Z"

class BridgeTests(unittest.TestCase):
    def test_missing_disclosures_prompt_user(self):
        r=prepare_decision_review(["8136"],[],NOW)
        self.assertEqual(r["analysis_mode"],"AWAITING_USER_CONFIRMATION")
        self.assertFalse(r["may_finalize_trade_recommendations"])
        self.assertFalse(r["may_execute_orders"])
    def test_approval_allows_provisional_recommendation_not_order(self):
        pf=evaluate_portfolio_events(["8136"],[],NOW)
        r=prepare_decision_review(["8136"],[],NOW,
            {"approved":True,"review_fingerprint":review_fingerprint(pf)})
        self.assertEqual(r["analysis_mode"],"PROVISIONAL_WITH_EXPLICIT_UNVERIFIED_FLAGS")
        self.assertTrue(r["may_finalize_trade_recommendations"])
        self.assertFalse(r["may_execute_orders"])
    def test_consent_not_reused_for_other_review(self):
        pf=evaluate_portfolio_events(["8136"],[],NOW)
        r=prepare_decision_review(["8136","6701"],[],NOW,
            {"approved":True,"review_fingerprint":review_fingerprint(pf)})
        self.assertEqual(r["analysis_mode"],"AWAITING_USER_CONFIRMATION")

if __name__=="__main__":unittest.main()
