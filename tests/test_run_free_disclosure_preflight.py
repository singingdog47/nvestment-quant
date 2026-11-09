import unittest
from src.run_free_disclosure_preflight import collect

class FreePreflightTests(unittest.TestCase):
    def test_one_failure_does_not_hide_missing_event(self):
        def fetcher(code):
            if code=="8136":
                raise OSError("offline")
            return {"candidate_disclosures":[]}
        r=collect(["8136","6701"],fetcher=fetcher,sleeper=lambda n:None)
        self.assertEqual(r["failures"],{"8136":"OSError"})
        self.assertTrue(all(x["status"]=="UNKNOWN" for x in r["manifest"]))
    def test_detected_event_still_unverified(self):
        def fetcher(code):
            return {"candidate_disclosures":[{"code":code,"title":"決算短信",
                "published_at":"2026-11-06T06:30:00+00:00","url":None}]}
        r=collect(["8136"],fetcher=fetcher,sleeper=lambda n:None)
        self.assertEqual(r["manifest"][0]["candidate_count"],1)
        self.assertEqual(r["manifest"][0]["status"],"UNKNOWN")

if __name__=="__main__": unittest.main()
