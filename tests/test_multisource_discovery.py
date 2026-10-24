import unittest

from madsc.multisource_discovery import evaluate_discovery


class MultiSourceDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.item = {"name": "Example Public Channel", "source_kind": "official_broadcaster",
                     "source_page": "https://example.org/watch",
                     "stream_url": "https://example.org/live.m3u8"}

    def test_review_only_even_with_claimed_license(self):
        row = dict(self.item, redistribution_permission_verified=True,
                   license_reference="https://example.org/rights")
        report = evaluate_discovery([row])
        candidate = report["candidates"][0]
        for flag in ("license_verified", "live_verified", "resolution_verified",
                     "codec_verified", "production_ready", "auto_add_allowed"):
            self.assertFalse(candidate[flag])
        self.assertFalse(report["network_probed"])
        self.assertFalse(report["production_writes"])

    def test_existing_stream_and_repeated_stream_are_deduplicated(self):
        rows = [self.item, dict(self.item, name="Mirror")]
        report = evaluate_discovery(rows)
        self.assertEqual(len(report["candidates"]), 1)
        self.assertEqual(len(report["duplicates"]), 1)
        existing = evaluate_discovery([self.item], {"https://example.org/live.m3u8"})
        self.assertEqual(len(existing["candidates"]), 0)

    def test_source_categories_and_watch_page_only(self):
        kinds = ("official_broadcaster", "licensed_m3u", "tv_directory",
                 "official_youtube", "licensed_free_platform")
        for kind in kinds:
            with self.subTest(kind=kind):
                report = evaluate_discovery([dict(self.item, source_kind=kind,
                                                   stream_url=None)])
                self.assertEqual(len(report["candidates"]), 1)
                self.assertIsNone(report["candidates"][0]["stream_url"])

    def test_invalid_inputs_fail_closed(self):
        for change in ({"source_kind": "pirated"},
                       {"source_page": "http://example.org"},
                       {"stream_url": "file:///etc/passwd"},
                       {"redistribution_permission_verified": "yes"},
                       {"license_reference": "http://example.org/rights"}):
            with self.subTest(change=change):
                report = evaluate_discovery([dict(self.item, **change)])
                self.assertEqual(len(report["rejected"]), 1)
                self.assertEqual(len(report["candidates"]), 0)

    def test_malformed_category_and_surrogate_name_are_rejected(self):
        for change in ({"source_kind": []}, {"source_kind": {}},
                       {"name": "Unsafe" + chr(0xD800) + "Channel"}):
            with self.subTest(change=repr(change)):
                result = evaluate_discovery([dict(self.item, **change)])
                self.assertEqual(result["candidates"], [])
                self.assertEqual(len(result["rejected"]), 1)

    def test_bounded_input(self):
        with self.assertRaises(ValueError):
            evaluate_discovery([self.item] * 20001)
