import io
import unittest
from src.yanoshin_disclosure_adapter import fetch_candidate_atom

XML=b'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>2027年3月期 第2四半期決算短信</title>
<published>2026-11-06T15:30:00+09:00</published>
<link href="https://example.com/issuer/earnings.pdf"/></entry></feed>'''

class FakeResponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self,*args): self.close()

class YanoshinAdapterTests(unittest.TestCase):
    def test_sanrio_candidate_not_primary_verified(self):
        result=fetch_candidate_atom("8136", opener=lambda req,timeout: FakeResponse(XML))
        self.assertEqual(result["candidate_disclosures"][0]["published_at"],
                         "2026-11-06T06:30:00+00:00")
        self.assertFalse(result["primary_verified"])
        self.assertFalse(result["complete"])
    def test_invalid_code_rejected(self):
        with self.assertRaises(ValueError):
            fetch_candidate_atom("8136/../")
    def test_bad_feed_fails_closed(self):
        with self.assertRaises(RuntimeError):
            fetch_candidate_atom("8136",opener=lambda req,timeout:FakeResponse(b"<html/>"))
    def test_empty_feed_does_not_prove_no_event(self):
        empty=b'<feed xmlns="http://www.w3.org/2005/Atom"/>'
        r=fetch_candidate_atom("8136",opener=lambda req,timeout:FakeResponse(empty))
        self.assertEqual(r["candidate_disclosures"], [])
        self.assertFalse(r["complete"])

if __name__=="__main__": unittest.main()
