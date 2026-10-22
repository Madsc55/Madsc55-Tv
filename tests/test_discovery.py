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
    def test_invalid_hosts_and_ports_rejected(self):
        for url in ("https://example.org:abc/live", "https://example.org:0/live",
                    "https://bad host/live", "https://[broken/live"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                normalize_url(url)

    def test_invalid_tvg_id_is_rejected_without_writes(self):
        result = classify_candidates([{"name": "A", "url": "https://example.org/live", "tvg_id": []}])
        self.assertEqual(len(result["rejected"]), 1)
        self.assertFalse(result["production_playlist_modified"])

    def test_control_character_url_injection_rejected(self):
        for url in ("https://example.org/live\\n#EXTINF:-1,Injected",
                    "\\nhttps://example.org/live",
                    "https://example.org/stream\\rmore",
                    "https://example.org/stream\\tmore"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                normalize_url(url)

    def test_url_injection_cannot_enter_candidate_catalog(self):
        result = classify_candidates([{
            "name": "A", "url": "https://example.org/live\\n#EXTINF:-1,Injected"}])
        self.assertEqual(result["candidates"], [])
        self.assertEqual(len(result["rejected"]), 1)

    def test_metadata_control_characters_rejected_per_candidate(self):
        fields = ("name", "tvg_id", "tvg_logo", "group_title")
        for field in fields:
            with self.subTest(field=field):
                rows = [{"name": "Safe", "url": "https://example.org/safe"},
                        {"name": "Injected", "url": "https://example.org/unsafe",
                         field: "bad\\n#EXTINF:-1,Injected"}]
                result = classify_candidates(rows)
                self.assertEqual(len(result["candidates"]), 1)
                self.assertEqual(len(result["rejected"]), 1)
                self.assertFalse(result["production_playlist_modified"])

    def test_encoded_line_breaks_and_nul_are_rejected(self):
        for url in ("https://example.org/live%0a#EXTINF",
                    "https://example.org/live%0Dnext",
                    "https://example.org/live%00",
                    "https://example.org/live?x=%0a"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                normalize_url(url)
        result = classify_candidates([{"name": "Unsafe", "url": "https://example.org/live%0a"}])
        self.assertEqual(result["candidates"], [])
        self.assertEqual(len(result["rejected"]), 1)
        self.assertFalse(result["production_playlist_modified"])
