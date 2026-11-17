import unittest
from src.event_user_consent import apply_user_consent, review_fingerprint

P={"as_of_utc":"2026-11-09T00:15:00Z","approval_required":True,
   "positions":[{"symbol":"8136","state":"EVENT_UNVERIFIED",
                 "decision_gate":"BLOCK_CAUSAL_CLAIMS_AND_NEW_TRADES"}]}

class ConsentTests(unittest.TestCase):
    def test_missing_consent_prompts(self):
        r=apply_user_consent(P)
        self.assertEqual(r["state"],"ASK_USER")
        self.assertFalse(r["provisional_analysis_allowed"])
    def test_explicit_consent_allows_provisional_not_execution(self):
        r=apply_user_consent(P,{"approved":True,"review_fingerprint":review_fingerprint(P)})
        self.assertEqual(r["state"],"PROVISIONAL_USER_APPROVED")
        self.assertTrue(r["provisional_analysis_allowed"])
        self.assertFalse(r["trade_execution_allowed"])
    def test_stale_consent_is_rejected(self):
        q=dict(P,as_of_utc="2026-11-09T00:16:00Z")
        r=apply_user_consent(q,{"approved":True,"review_fingerprint":review_fingerprint(P)})
        self.assertEqual(r["state"],"ASK_USER")
    def test_decline_is_rejected(self):
        r=apply_user_consent(P,{"approved":False,"review_fingerprint":review_fingerprint(P)})
        self.assertFalse(r["provisional_analysis_allowed"])

if __name__=="__main__": unittest.main()
