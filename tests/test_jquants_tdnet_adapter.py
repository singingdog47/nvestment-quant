import io
import unittest
from src.jquants_tdnet_adapter import fetch_tdnet_list

class _Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): self.close()

class JQuantsAdapterTests(unittest.TestCase):
    def test_missing_key_blocks(self):
        with self.assertRaises(RuntimeError):
            fetch_tdnet_list("8136", "2026-11-01", "2026-11-09", api_key="")
    def test_reject_bad_code(self):
        with self.assertRaises(ValueError):
            fetch_tdnet_list("8136;rm", "2026-11-01", "2026-11-09", api_key="test")
    def test_response_contract(self):
        def mock(req, timeout):
            self.assertEqual(req.get_header("X-api-key"), "test")
            return _Response(b'{"data":[{"Code":"81360","Title":"earnings"}]}')
        rows=fetch_tdnet_list("8136","2026-11-01","2026-11-09",api_key="test",opener=mock)
        self.assertEqual(len(rows),1)
    def test_unexpected_response_blocks(self):
        with self.assertRaises(RuntimeError):
            fetch_tdnet_list("8136","2026-11-01","2026-11-09",api_key="test",
                             opener=lambda req,timeout:_Response(b'{}'))

if __name__ == "__main__": unittest.main()
