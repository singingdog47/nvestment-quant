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

    def test_unverified_free_feed_cannot_self_certify(self):
        wrapper={"primary_verified":False,"all_symbols_unverified":True,
                 "manifest":[{"symbol":"8136","status":"NO_EVENT_CONFIRMED",
                              "reviewed":True,"checked_at_utc":NOW,
                              "source_kind":"JPX_TDNET",
                              "source_url":"https://www.jpx.co.jp/",
                              "coverage_start_utc":"2026-10-30T00:00:00Z"}]}
        r=prepare_decision_review(["8136"],wrapper,NOW)
        self.assertEqual(r["analysis_mode"],"AWAITING_USER_CONFIRMATION")
        self.assertFalse(r["may_finalize_trade_recommendations"])

if __name__=="__main__":unittest.main()
