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

    def test_nfkc_equivalent_source_labels_are_ambiguous(self):
        feed = "#EXTM3U\\n#EXTINF:-1,Test\\nhttps://example.org/live\\n"
        sources = {"Feed": feed, "Ｆｅｅｄ": feed}
        for entrypoint in (corroborate_sources, build_m3u8_preview):
            with self.subTest(entrypoint=entrypoint.__name__):
                with self.assertRaisesRegex(ValueError, "Ambiguous duplicate source names"):
                    entrypoint(sources)

    def test_invisible_unicode_source_labels_rejected(self):
        feed = "#EXTM3U\n#EXTINF:-1,News\nhttps://example.org/live\n"
        for bad_label in ("feed\u202e", "feed\u200b", "feed\u2028"):
            with self.subTest(label=repr(bad_label)):
                with self.assertRaises(ValueError):
                    parse_m3u(feed, bad_label)
                for entrypoint in (corroborate_sources, build_m3u8_preview):
                    with self.assertRaises(ValueError):
                        entrypoint({bad_label: feed})

    def test_preview_rejects_invisible_source_label_before_parsing(self):
        for label in ("feed\u202e", "feed\u200b", "feed\u2028"):
            with self.subTest(label=repr(label)):
                with self.assertRaisesRegex(ValueError, "(Invalid source name|Source name contains control characters)"):
                    build_m3u8_preview({label: "not an M3U feed"})

    def test_known_urls_reject_invisible_unicode(self):
        feed = "#EXTM3U\n#EXTINF:-1,News\nhttps://example.org/live\n"
        for url in ("https://example.org/\u200blive",
                    "https://example.org/\u202elive",
                    "https://example.org/\u2028live"):
            with self.subTest(url=repr(url)):
                with self.assertRaisesRegex(ValueError, "control characters"):
                    corroborate_sources({"source": feed}, known_urls={url})

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
                         ["orphan_url", "empty_channel_name"])

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

    def test_m3u_header_rejects_whitespace_aliases(self):
        for header in (" #EXTM3U", "#EXTM3U ", "#EXTM3U\t"):
            with self.subTest(header=repr(header)):
                with self.assertRaisesRegex(ValueError, "Missing M3U header"):
                    parse_m3u(header + "\n", "fixture")

    def test_lookalike_identity_metadata_is_rejected(self):
        for key in ("xtvg-id", "xtvg-logo", "xgroup-title"):
            with self.subTest(key=key):
                feed = (
                    '#EXTM3U\n#EXTINF:-1 ' + key +
                    '="forged" tvg-id="real",Channel\n'
                    'https://example.org/live\n'
                )
                report = parse_m3u(feed, "fixture")
                self.assertEqual(report["entries"], 0)
                self.assertEqual(
                    report["parse_errors"][0]["reason"],
                    "invalid_metadata_attribute",
                )

    def test_metadata_attributes_require_token_boundaries(self):
        feed = ("#EXTM3U\n"
                '#EXTINF:-1 xtvg-id="forged" tvg-id="real",Channel\n'
                "https://example.org/live\n")
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 0)
        self.assertEqual(report["parse_errors"][0]["reason"], "invalid_metadata_attribute")
        self.assertEqual(report["candidates"], [])

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

    def test_preview_rejects_aggregate_candidate_overflow(self):
        first = "#EXTM3U\n" + "".join(
            f"#EXTINF:-1,Channel {i}\nhttps://a.example/{i}\n" for i in range(10001))
        second = "#EXTM3U\n" + "".join(
            f"#EXTINF:-1,Channel {i}\nhttps://b.example/{i}\n" for i in range(10000))
        with self.assertRaisesRegex(ValueError, "Combined sources exceed bounded candidate limit"):
            build_m3u8_preview({"first": first, "second": second})

    def test_preview_rejects_combined_input_size_before_parsing(self):
        # Individually under the 8-million-character source limit.
        feeds = {"a": "#EXTM3U\n" + " " * 4_000_000,
                 "b": "#EXTM3U\n" + " " * 4_000_000}
        with self.assertRaisesRegex(ValueError, "Combined source text"):
            build_m3u8_preview(feeds)

    def test_corroboration_rejects_aggregate_candidate_overflow(self):
        first = "#EXTM3U\n" + "".join(
            f"#EXTINF:-1,Channel {i}\nhttps://a.example/{i}\n" for i in range(10001))
        second = "#EXTM3U\n" + "".join(
            f"#EXTINF:-1,Channel {i}\nhttps://b.example/{i}\n" for i in range(10000))
        with self.assertRaisesRegex(ValueError, "Combined sources exceed bounded candidate limit"):
            corroborate_sources({"first": first, "second": second})

    def test_corroboration_rejects_combined_source_text_before_parsing(self):
        feeds = {"a": "#EXTM3U\n" + " " * 4_000_000, "b": "#EXTM3U\n" + " " * 4_000_000}
        with self.assertRaisesRegex(ValueError, "Combined source text"):
            corroborate_sources(feeds)

    def test_duplicate_metadata_attributes_are_rejected(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="first" TVG-ID="second",Ambiguous\n'
                'https://example.org/live.m3u8\n'
                '#EXTINF:-1 tvg-id="valid",Valid\n'
                'https://example.org/valid.m3u8\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["tvg_id"], "valid")
        self.assertEqual(
            [error["reason"] for error in report["parse_errors"]],
            ["duplicate_metadata_attribute"],
        )

    def test_metadata_attribute_names_are_case_insensitive(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 TVG-ID="news.tv" GROUP-TITLE="News",News TV\n'
                'https://example.org/news.m3u8\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["tvg_id"], "news.tv")
        self.assertEqual(report["candidate_rows"][0]["group_title"], "News")

    def test_identical_feed_bodies_do_not_count_as_independent_sources(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="news.tv",News TV\n'
                'https://example.org/news.m3u8\n')
        report = corroborate_sources({"source-a": feed, "source-b": feed})
        self.assertEqual(report["sources_checked"], 2)
        self.assertEqual(len(report["identity_candidates"]), 1)
        candidate = report["identity_candidates"][0]
        self.assertEqual(candidate["source_count"], 1)
        self.assertEqual(candidate["sources"], ["source-a", "source-b"])

    def test_transport_formatting_does_not_inflate_feed_independence(self):
        feed_lf = ('#EXTM3U\n'
                   '#EXTINF:-1 tvg-id="news.tv",News TV\n'
                   'https://example.org/news.m3u8\n')
        feed_crlf = ('\ufeff#EXTM3U\r\n'
                     '\r\n'
                     '#EXTINF:-1 tvg-id="news.tv",News TV   \r\n'
                     'https://example.org/news.m3u8  \r\n')
        report = corroborate_sources({"source-lf": feed_lf, "source-crlf": feed_crlf})
        candidate = report["identity_candidates"][0]
        self.assertEqual(candidate["source_count"], 1)
        self.assertEqual(candidate["sources"], ["source-crlf", "source-lf"])

    def test_reordered_semantically_identical_feeds_do_not_inflate_votes(self):
        feed_a = ('#EXTM3U\n'
                  '# comment from mirror A\n'
                  '#EXTINF:-1 tvg-id="news.tv",News TV\n'
                  'https://example.org/news.m3u8\n'
                  '#EXTINF:-1 tvg-id="sports.tv",Sports TV\n'
                  'https://example.org/sports.m3u8\n')
        feed_b = ('\ufeff#EXTM3U\r\n'
                  '# mirror B has different comments\r\n'
                  '#EXTINF:-1 tvg-id="sports.tv",Sports TV\r\n'
                  'https://example.org/sports.m3u8\r\n'
                  '#EXTINF:-1 tvg-id="news.tv",News TV\r\n'
                  'https://example.org/news.m3u8\r\n')
        report = corroborate_sources({"source-a": feed_a, "source-b": feed_b})
        self.assertEqual(len(report["identity_candidates"]), 2)
        self.assertTrue(all(row["source_count"] == 1
                            for row in report["identity_candidates"]))
        self.assertTrue(all(row["sources"] == ["source-a", "source-b"]
                            for row in report["identity_candidates"]))
        self.assertFalse(report["source_independence_verified"])
        self.assertEqual(
            report["source_count_semantics"],
            "distinct_semantic_feed_inventories_not_verified_origins",
        )
        self.assertTrue(all(not row["source_independence_verified"]
                            for row in report["identity_candidates"]))


    def test_known_urls_count_is_bounded_in_corroboration(self):
        known = {f"https://example.org/{i}" for i in range(20001)}
        with self.assertRaisesRegex(ValueError, "Too many known URLs"):
            corroborate_sources({"source": "#EXTM3U"}, known_urls=known)

    def test_unquoted_or_malformed_identity_metadata_is_rejected(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id=news.tv,Malformed\n'
                'https://example.org/malformed\n'
                '#EXTINF:-1 tvg-id="valid.tv",Valid\n'
                'https://example.org/valid\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["tvg_id"], "valid.tv")
        self.assertEqual(
            [row["reason"] for row in report["parse_errors"]],
            ["invalid_metadata_attribute"],
        )
        preview = build_m3u8_preview({"fixture": feed})
        self.assertEqual(preview["channel_count"], 1)
        self.assertEqual(preview["rejected"], 1)
        self.assertFalse(preview["production_writes"])



    def test_rejected_extinf_consumes_its_url_without_orphan_noise(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="bad"\n'
                'https://example.org/missing-name\n'
                '#EXTINF:-1 tvg-id="bad",   \n'
                'https://example.org/empty-name\n'
                '#EXTINF:-1 tvg-id="bad" group-title="oops,Malformed\n'
                'https://example.org/unbalanced\n'
                '#EXTINF:-1 tvg-id="good",Good\n'
                'https://example.org/good\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["tvg_id"], "good")
        self.assertEqual(
            [error["reason"] for error in report["parse_errors"]],
            ["missing_channel_name", "empty_channel_name", "missing_channel_name"],
        )
        self.assertEqual(build_m3u8_preview({"fixture": feed})["channel_count"], 1)



    def test_surrogate_codepoints_fail_closed_before_downstream_hashing(self):
        malformed = "#EXTM3U\n#EXTINF:-1,Bad\nhttps://example.org/\ud800\n"
        with self.assertRaisesRegex(ValueError, "valid UTF-8"):
            parse_m3u(malformed, "fixture")
        with self.assertRaisesRegex(ValueError, "valid UTF-8"):
            corroborate_sources({"fixture": malformed})
        with self.assertRaisesRegex(ValueError, "valid UTF-8"):
            build_m3u8_preview({"fixture": malformed})
        with self.assertRaisesRegex(ValueError, "valid UTF-8"):
            parse_m3u("#EXTM3U\n", "bad\ud800")



    def test_control_characters_in_source_labels_fail_closed(self):
        feed = "#EXTM3U\n#EXTINF:-1,Safe\nhttps://example.org/safe\n"
        for source in ("bad\nlabel", "bad\tlabel", "bad\x00label", "bad\x7flabel"):
            with self.subTest(source=repr(source)):
                with self.assertRaisesRegex(ValueError, "control characters"):
                    parse_m3u(feed, source)
                with self.assertRaisesRegex(ValueError, "control characters"):
                    corroborate_sources({source: feed})
                with self.assertRaisesRegex(ValueError, "control characters"):
                    build_m3u8_preview({source: feed})



    def test_invalid_provenance_label_rejected_before_known_url_normalization(self):
        feed = "#EXTM3U\n#EXTINF:-1,Safe\nhttps://example.org/safe\n"
        with self.assertRaisesRegex(ValueError, "Invalid source name"):
            corroborate_sources(
                {"bad\nlabel": feed},
                known_urls={"https://example.org:bad-port/live"},
            )
        with self.assertRaisesRegex(ValueError, "Invalid source name"):
            corroborate_sources(
                {"bad\ud800label": feed},
                known_urls={"https://example.org:bad-port/live"},
            )



    def test_source_name_length_is_bounded_across_k2_entrypoints(self):
        feed = "#EXTM3U\n#EXTINF:-1,Safe\nhttps://example.org/safe\n"
        valid_name = "s" * 256
        too_long = "s" * 257
        self.assertEqual(parse_m3u(feed, valid_name)["source"], valid_name)
        for source in (too_long,):
            with self.assertRaisesRegex(ValueError, "bounded length"):
                parse_m3u(feed, source)
            with self.assertRaisesRegex(ValueError, "bounded length"):
                corroborate_sources({source: feed})
            with self.assertRaisesRegex(ValueError, "bounded length"):
                build_m3u8_preview({source: feed})



    def test_mirrored_tvg_id_feeds_do_not_gain_votes_from_display_metadata(self):
        feed_a = ('#EXTM3U\n#EXTINF:-1 tvg-id="shared" tvg-logo="https://img.example/a.png" '
                  'group-title="News",First label\nhttps://example.org/live\n')
        feed_b = ('#EXTM3U\n#EXTINF:-1 tvg-id="SHARED" tvg-logo="https://img.example/b.png" '
                  'group-title="Sports",Different label\nhttps://example.org/live\n')
        result = corroborate_sources({"first": feed_a, "mirror": feed_b})
        self.assertEqual(len(result["identity_candidates"]), 1)
        candidate = result["identity_candidates"][0]
        self.assertEqual(candidate["source_count"], 1)
        self.assertEqual(candidate["sources"], ["first", "mirror"])
        self.assertFalse(candidate["source_independence_verified"])

    def test_name_only_identity_changes_still_distinguish_feed_inventories(self):
        feed_a = ('#EXTM3U\n#EXTINF:-1 group-title="News",Same\n'
                  'https://example.org/live\n')
        feed_b = ('#EXTM3U\n#EXTINF:-1 group-title="Sports",Same\n'
                  'https://example.org/live\n')
        result = corroborate_sources({"first": feed_a, "second": feed_b})
        self.assertEqual(len(result["identity_candidates"]), 2)



    def test_known_urls_reject_oversized_or_surrogate_values(self):
        feed = "#EXTM3U\n#EXTINF:-1,Safe\nhttps://example.org/safe\n"
        for known in ("https://example.org/" + "a" * 8192,
                      "https://example.org/\ud800"):
            with self.subTest(known=repr(known[:40])):
                with self.assertRaisesRegex(ValueError, "oversized or invalid Unicode"):
                    corroborate_sources({"source": feed}, known_urls={known})
        result = corroborate_sources(
            {"source": feed}, known_urls={"https://example.org/safe"})
        self.assertEqual(result["identity_candidates"], [])



    def test_known_urls_reject_control_characters_before_normalization(self):
        feed = "#EXTM3U\n#EXTINF:-1,Safe\nhttps://example.org/safe\n"
        for known in ("https://example.org/\nattack",
                      "https://example.org/\x00attack",
                      "https://example.org/\tattack",
                      "https://example.org/\x7fattack"):
            with self.subTest(known=repr(known)):
                with self.assertRaisesRegex(ValueError, "control characters"):
                    corroborate_sources({"source": feed}, known_urls={known})



    def test_known_channels_cannot_manufacture_independent_feed_votes(self):
        shared = '#EXTINF:-1 tvg-id="new.channel",New\nhttps://example.org/new\n'
        known_a = '#EXTINF:-1 tvg-id="old.one",Old\nhttps://example.org/old-one\n'
        known_b = '#EXTINF:-1 tvg-id="old.two",Old\nhttps://example.org/old-two\n'
        result = corroborate_sources(
            {"feed-a": "#EXTM3U\n" + shared + known_a,
             "feed-b": "#EXTM3U\n" + shared + known_b},
            known_urls={"https://example.org/old-one", "https://example.org/old-two"},
        )
        self.assertEqual(len(result["identity_candidates"]), 1)
        row = result["identity_candidates"][0]
        self.assertEqual(row["source_count"], 1)
        self.assertEqual(row["sources"], ["feed-a", "feed-b"])
        self.assertEqual(row["url_variants"], 1)


    def test_large_source_fails_closed(self):
        with self.assertRaises(ValueError):
            parse_m3u("#EXTM3U" + "x" * 8_000_001, "a")


    def test_malformed_extinf_rows_count_toward_source_limit(self):
        feed = "#EXTM3U\n" + ("#EXTINF:-1,\nhttps://example.org/rejected\n" * 3)
        with self.assertRaisesRegex(ValueError, "bounded candidate limit"):
            parse_m3u(feed, "source", max_entries=2)

    def test_valid_extinf_rows_still_fit_source_limit(self):
        feed = "#EXTM3U\n#EXTINF:-1,One\nhttps://example.org/one\n"
        self.assertEqual(parse_m3u(feed, "source", max_entries=1)["entries"], 1)

    def test_extinf_control_characters_are_rejected_without_url_leak(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="bad\x00id",Bad\n'
                'https://example.org/bad\n'
                '#EXTINF:-1 tvg-id="good",Good\n'
                'https://example.org/good\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["tvg_id"], "good")
        self.assertEqual([error["reason"] for error in report["parse_errors"]],
                         ["invalid_metadata_control"])

    def test_extinf_bidi_format_character_is_rejected(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="news\u202e",News\n'
                'https://example.org/bad\n'
                '#EXTINF:-1 tvg-id="safe",Safe\n'
                'https://example.org/safe\n')
        result = parse_m3u(feed, "fixture")
        self.assertEqual(result["entries"], 1)
        self.assertEqual(result["candidate_rows"][0]["tvg_id"], "safe")
        self.assertEqual([row["reason"] for row in result["parse_errors"]],
                         ["invalid_metadata_control"])
        self.assertFalse(result["production_writes"])

    def test_nonstandard_line_separators_cannot_split_extinf_metadata(self):
        for separator in ("\x0b", "\x0c", "\x1c", "\x1d", "\x1e",
                          "\x85", "\u2028", "\u2029"):
            with self.subTest(separator=repr(separator)):
                feed = ('#EXTM3U\n'
                        '#EXTINF:-1 tvg-id="bad' + separator + 'id",Bad\n'
                        'https://example.org/bad\n')
                with self.assertRaisesRegex(ValueError, "unsupported line separators"):
                    parse_m3u(feed, "fixture")

    def test_crlf_line_endings_remain_supported(self):
        feed = ('#EXTM3U\r\n'
                '#EXTINF:-1 tvg-id="good",Good\r\n'
                'https://example.org/good\r\n')
        self.assertEqual(parse_m3u(feed, "fixture")["entries"], 1)

    def test_nonstandard_separators_fail_closed_across_batch_entrypoints(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="bad\u2028id",Bad\n'
                'https://example.org/bad\n')
        for entrypoint in (corroborate_sources, build_m3u8_preview):
            with self.subTest(entrypoint=entrypoint.__name__):
                with self.assertRaisesRegex(ValueError, "unsupported line separators"):
                    entrypoint({"fixture": feed})

    def test_extinf_controls_stripped_at_edges_are_still_rejected(self):
        for malformed in ('#EXTINF:-1,Bad\t',
                          '\t#EXTINF:-1,Bad',
                          '#EXTINF:-1,Bad\x00'):
            with self.subTest(malformed=repr(malformed)):
                feed = ('#EXTM3U\n' + malformed + '\n'
                        'https://example.org/bad\n'
                        '#EXTINF:-1,Good\nhttps://example.org/good\n')
                report = parse_m3u(feed, "fixture")
                self.assertEqual(report["entries"], 1)
                self.assertEqual(report["candidate_rows"][0]["name"], "Good")
                self.assertIn("invalid_metadata_control",
                              [error["reason"] for error in report["parse_errors"]])

    def test_url_controls_are_rejected_before_strip(self):
        for url in ('https://example.org/bad\t',
                    '\thttps://example.org/bad',
                    'https://example.org/bad\x00'):
            with self.subTest(url=repr(url)):
                feed = ('#EXTM3U\n#EXTINF:-1,Bad\n' + url + '\n'
                        '#EXTINF:-1,Good\nhttps://example.org/good\n')
                report = parse_m3u(feed, "fixture")
                self.assertEqual(report["entries"], 1)
                self.assertEqual(report["candidate_rows"][0]["name"], "Good")
                self.assertIn("invalid_url_control",
                              [error["reason"] for error in report["parse_errors"]])

    def test_bare_carriage_return_cannot_split_extinf_metadata(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1 tvg-id="bad\rid",Bad\n'
                'https://example.org/bad\n')
        with self.assertRaisesRegex(ValueError, "unsupported bare carriage returns"):
            parse_m3u(feed, "fixture")

    def test_mixed_lf_and_crlf_remains_supported(self):
        feed = ('#EXTM3U\r\n'
                '#EXTINF:-1,Good\n'
                'https://example.org/good\r\n')
        self.assertEqual(parse_m3u(feed, "fixture")["entries"], 1)

    def test_padded_extinf_metadata_is_not_silently_accepted(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1,Bad\u00a0\n'
                'https://example.org/bad\n'
                '#EXTINF:-1,Good\n'
                'https://example.org/good\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["name"], "Good")
        self.assertIn("invalid_metadata_whitespace",
                      [error["reason"] for error in report["parse_errors"]])

    def test_crlf_does_not_exempt_non_ascii_metadata_padding(self):
        feed = ('#EXTM3U\r\n'
                '#EXTINF:-1,Bad\u00a0\r\n'
                'https://example.org/bad\r\n'
                '#EXTINF:-1,Good\r\n'
                'https://example.org/good\r\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["name"], "Good")
        self.assertIn("invalid_metadata_whitespace",
                      [error["reason"] for error in report["parse_errors"]])

    def test_padded_invalid_extinf_counts_toward_source_limit(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1,Bad\u00a0\n'
                'https://example.org/bad\n'
                '#EXTINF:-1,Good\n'
                'https://example.org/good\n')
        with self.assertRaisesRegex(ValueError, "bounded candidate limit"):
            parse_m3u(feed, "fixture", max_entries=1)

    def test_padded_metadata_reports_previous_missing_url(self):
        feed = ('#EXTM3U\n'
                '#EXTINF:-1,First\n'
                '#EXTINF:-1,Bad\u00a0\n'
                'https://example.org/bad\n'
                '#EXTINF:-1,Good\n'
                'https://example.org/good\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["name"], "Good")
        self.assertEqual([error["reason"] for error in report["parse_errors"]],
                         ["missing_url", "invalid_metadata_whitespace"])

    def test_leading_space_before_extinf_is_rejected(self):
        feed = ('#EXTM3U\n'
                ' #EXTINF:-1,Bad\n'
                'https://example.org/bad\n'
                '#EXTINF:-1,Good\n'
                'https://example.org/good\n')
        report = parse_m3u(feed, "fixture")
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["candidate_rows"][0]["name"], "Good")
        self.assertIn("invalid_metadata_whitespace",
                      [error["reason"] for error in report["parse_errors"]])

    def test_leading_space_metadata_consumes_candidate_limit(self):
        feed = ('#EXTM3U\n'
                ' #EXTINF:-1,Bad\n'
                'https://example.org/bad\n'
                '#EXTINF:-1,Good\n'
                'https://example.org/good\n')
        with self.assertRaisesRegex(ValueError, "bounded candidate limit"):
            parse_m3u(feed, "fixture", max_entries=1)
