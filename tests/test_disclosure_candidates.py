import unittest
from src.disclosure_candidates import parse_disclosure_candidates, candidate_manifest

class DisclosureCandidateTests(unittest.TestCase):
    def test_sanrio_disclosure_detected_without_auto_clearance(self):
        x = parse_disclosure_candidates([
            {"code":"8136","title":"2027年3月期 第2四半期決算短信",
             "published_at":"2026-11-06T06:30:00Z","url":"https://example.org/disclosure"}
        ], ["8136","6701"])
        self.assertEqual(x["8136"][0]["category"], "EARNINGS_OR_FORECAST")
        m = candidate_manifest(x, "2026-11-09T00:15:00Z")
        self.assertTrue(all(i["status"]=="UNKNOWN" for i in m))
    def test_no_results_is_not_no_event(self):
        m = candidate_manifest(parse_disclosure_candidates([], ["8136"]), "2026-11-09T00:15:00Z")
        self.assertEqual(m[0]["status"], "UNKNOWN")
    def test_other_company_ignored(self):
        x = parse_disclosure_candidates([{"code":"7203","title":"決算短信"}], ["8136"])
        self.assertEqual(x["8136"], [])

if __name__=="__main__":
    unittest.main()
