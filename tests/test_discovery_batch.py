import unittest

from madsc.discovery_batch import parse_m3u, corroborate_sources, build_m3u8_preview


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

    def test_m3u8_preview_integrates_k2_k3_k5_without_live_publishing(self):
        feeds = {"a": '#EXTM3U\n#EXTINF:-1 tvg-id="news.tv" group-title="Haber",News TV\nhttps://example.org/news.m3u8\n',
                 "b": '#EXTM3U\n#EXTINF:-1 tvg-id="news.tv" group-title="Haber",News TV\nhttps://example.org/news.m3u8\n'}
        result = build_m3u8_preview(feeds)
        self.assertEqual(result["filename"], "playlist.m3u8")
        self.assertEqual(result["channel_count"], 1)
        self.assertEqual(result["duplicates"], 1)
        self.assertIn('tvg-id="news.tv"', result["content"])
        self.assertIn("https://example.org/news.m3u8", result["content"])
        self.assertTrue(result["content"].startswith("#EXTM3U\n"))
        self.assertFalse(result["production_writes"])
        self.assertFalse(result["ibo_device_verified"])

    def test_known_urls_requires_set(self):
        with self.assertRaises(ValueError):
            corroborate_sources({"a": "#EXTM3U"}, known_urls=["https://example.org/a"])

    def test_preview_rejects_unsafe_candidate(self):
        feed = ("#EXTM3U\n#EXTINF:-1,Unsafe\nfile:///tmp/channel\n"
                "#EXTINF:-1,Safe\nhttps://example.org/live.m3u8\n")
        result = build_m3u8_preview({"source": feed})
        self.assertEqual(result["channel_count"], 1)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["status"], "SANDBOX_PREVIEW_ONLY")
        self.assertFalse(result["production_writes"])

    def test_bad_feed_keys_fail_closed_in_both_entrypoints(self):
        for invalid in (None, 17, ""):
            with self.subTest(invalid=invalid):
                feed = {invalid: "#EXTM3U"}
                with self.assertRaises(ValueError):
                    corroborate_sources(feed)
                with self.assertRaises(ValueError):
                    build_m3u8_preview(feed)

    def test_known_url_excluded_from_ranking(self):
        feed = "#EXTM3U\n#EXTINF:-1,News\nhttps://example.org/news.m3u8\n"
        result = corroborate_sources({"a": feed}, known_urls={"https://example.org/news.m3u8"})
        self.assertEqual(result["identity_candidates"], [])

    def test_empty_name_and_orphan_url_are_reported(self):
        feed = ("#EXTM3U\nhttps://example.org/orphan\n"
                "#EXTINF:-1,   \nhttps://example.org/unnamed\n"
                "#EXTINF:-1,Valid\nhttps://example.org/valid\n")
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(len(report["candidates"]), 1)
        self.assertEqual([e["reason"] for e in report["parse_errors"]],
                         ["orphan_url", "empty_channel_name", "orphan_url"])

    def test_invalid_limits_and_known_url_types_fail_closed(self):
        for limit in (True, 1.5, "10", None):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                parse_m3u("#EXTM3U", "fixture", max_entries=limit)
        with self.assertRaises(ValueError):
            corroborate_sources({"a": "#EXTM3U"}, known_urls={None})

    def test_leading_blank_line_is_not_a_valid_m3u_header(self):
        with self.assertRaises(ValueError):
            parse_m3u("\n#EXTM3U\n#EXTINF:-1,Channel\nhttps://example.org/live", "fixture")

    def test_ambiguous_source_names_rejected(self):
        feeds = {"Source": "#EXTM3U", " source ": "#EXTM3U"}
        for entrypoint in (corroborate_sources, build_m3u8_preview):
            with self.subTest(entrypoint=entrypoint.__name__), self.assertRaises(ValueError):
                entrypoint(feeds)

    def test_preview_rejects_ambiguous_source_names(self):
        feeds = {"Feed": "#EXTM3U", " feed ": "#EXTM3U"}
        with self.assertRaises(ValueError):
            build_m3u8_preview(feeds)

    def test_extinf_quoted_commas_preserve_channel_identity(self):
        feed = ('#EXTM3U\n#EXTINF:-1 tvg-id="news,tr" group-title="News, World",News, HD\n'
                'https://example.org/news.m3u8\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["name"], "News, HD")
        self.assertEqual(report["candidate_rows"][0]["tvg_id"], "news,tr")
        self.assertEqual(report["candidate_rows"][0]["group_title"], "News, World")

    def test_extinf_unclosed_quote_fails_closed(self):
        feed = ('#EXTM3U\n#EXTINF:-1 tvg-id="broken,Channel\n'
                'https://example.org/news.m3u8\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 0)
        self.assertEqual(report["parse_errors"][0]["reason"], "missing_channel_name")

    def test_unbalanced_metadata_quote_is_rejected(self):
        feed = ('#EXTM3U\n#EXTINF:-1 tvg-id="broken" group-title="oops,Channel\n'
                'https://example.org/live.m3u8\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 0)
        self.assertEqual(report["parse_errors"][0]["reason"], "missing_channel_name")

    def test_non_text_source_rejected_by_both_batch_paths(self):
        for entrypoint in (corroborate_sources, build_m3u8_preview):
            with self.subTest(entrypoint=entrypoint.__name__), self.assertRaises(ValueError):
                entrypoint({"feed": None})

    def test_quoted_comma_round_trip_in_preview(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="tr,news" group-title="News, World",News, HD\n'
                'https://example.org/live.m3u8\n')
        result = build_m3u8_preview({"source": feed})
        self.assertEqual(result["channel_count"], 1)
        self.assertIn("NEWS, HD", result["content"])
        self.assertIn('tvg-id="tr,news"', result["content"])
        self.assertIn('group-title="News, World"', result["content"])
        self.assertFalse(result["production_ready"])

    def test_large_source_fails_closed(self):
        with self.assertRaises(ValueError):
            parse_m3u("#EXTM3U" + "x" * 8_000_001, "a")
