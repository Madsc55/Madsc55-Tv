import unittest

from madsc.discovery_batch import parse_m3u, corroborate_sources


class DiscoveryBatchTests(unittest.TestCase):
    def test_parse_m3u_extracts_metadata_and_rejects_bad_urls(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="tr.news" group-title="Haber",Haber TV\n'
                'https://example.org/news.m3u8\n'
                '#EXTINF:-1,Bad\nfile:///etc/passwd\n')
        report = parse_m3u(feed, "source-a")
        self.assertEqual(report["entries"], 2)
        self.assertEqual(len(report["candidates"]), 1)
        self.assertEqual(len(report["rejected"]), 1)
        self.assertEqual(report["candidates"][0]["tvg_id"], "tr.news")
        self.assertFalse(report["live_verified"])

    def test_two_sources_vote_once_per_identity(self):
        a = '#EXTM3U\n#EXTINF:-1 tvg-id="TR.ONE",One\nhttps://a.example/one\n'
        b = ('#EXTM3U\n#EXTINF:-1 tvg-id="tr.one",One\nhttps://b.example/one\n'
             '#EXTINF:-1 tvg-id="tr.one",One\nhttps://c.example/one\n')
        report = corroborate_sources({"a": a, "b": b})
        self.assertEqual(len(report["identity_candidates"]), 1)
        self.assertEqual(report["identity_candidates"][0]["source_count"], 2)
        self.assertEqual(report["identity_candidates"][0]["url_variants"], 3)
        self.assertFalse(report["live_verified"])

    def test_invalid_header_and_bounded_source(self):
        with self.assertRaises(ValueError):
            parse_m3u("not m3u", "x")
        with self.assertRaises(ValueError):
            parse_m3u("#EXTM3U", "x", max_entries=20001)

    def test_no_automatic_live_acceptance(self):
        report = corroborate_sources({"a": "#EXTM3U\n#EXTINF:-1,Test\nhttps://example.org/a\n"})
        self.assertEqual(report["identity_candidates"][0]["status"], "REVIEW_REQUIRED_NOT_LIVE_VERIFIED")
        self.assertFalse(report["production_writes"])
