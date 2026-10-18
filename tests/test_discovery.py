import unittest
from madsc.discovery import classify_candidates, normalize_url

class DiscoveryTests(unittest.TestCase):
    def test_deduplicate_without_leaking_urls(self):
        data = [{"name":"A","url":"https://example.org/live"},
                {"name":"A again","url":"https://EXAMPLE.ORG/live"},
                {"name":"Bad","url":"file:///etc/passwd"}]
        result = classify_candidates(data)
        self.assertEqual((len(result["candidates"]), len(result["duplicates"]), len(result["rejected"])), (1,1,1))
        self.assertFalse(result["production_playlist_modified"])
        self.assertFalse(result["device_verified"])
        self.assertNotIn("https://example.org/live", str(result))
    def test_credentials_rejected(self):
        with self.assertRaises(ValueError):
            normalize_url("https://user:pass@example.org/live")
