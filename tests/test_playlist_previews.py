import unittest
from madsc.channel_catalog import prepare_channel_catalog
from madsc.playlist_previews import render_playlist_previews


class PlaylistPreviewTests(unittest.TestCase):
    def test_five_drafts_preserve_original_groups_and_ibo(self):
        rows = [{"name": "izmir tv", "url": "https://example.org/stream",
                 "group_title": "Haber", "tvg_id": "izmir.tv"}]
        catalog = prepare_channel_catalog(rows)
        digest = catalog["channels"][0]["url_sha256"]
        catalog = prepare_channel_catalog(rows, ibo_results={digest: "WORKING"})
        result = render_playlist_previews(catalog, rows)
        self.assertEqual(len(result["drafts"]), 5)
        self.assertEqual(result["counts"]["IBO_ONAYLI_CALISAN"], 1)
        self.assertIn('group-title="Haber"', result["drafts"]["IBO_ONAYLI_CALISAN"])
        self.assertIn("İZMİR TV", result["drafts"]["IBO_ONAYLI_CALISAN"])
        self.assertEqual(result["drafts"]["YABANCI"], "#EXTM3U\n")
        self.assertFalse(result["production_writes"])

    def test_mismatched_source_rejected(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        catalog = prepare_channel_catalog(rows)
        with self.assertRaises(ValueError):
            render_playlist_previews(catalog, [{"name": "A", "url": "https://example.org/b"}])

    def test_malicious_metadata_rejected(self):
        rows = [{"name": "A", "url": "https://example.org/a", "group_title": "Haber"}]
        catalog = prepare_channel_catalog(rows)
        catalog["channels"][0]["group_title"] = 'x"\n#EXTINF:evil'
        with self.assertRaises(ValueError):
            render_playlist_previews(catalog, rows)

    def test_playlist_preview_rejects_invalid_channel_name_delimiters(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        for name in ("", None, 42, "A\\nB"):
            catalog = prepare_channel_catalog(rows)
            catalog["channels"][0]["display_name"] = name
            with self.subTest(name=name), self.assertRaises(ValueError):
                render_playlist_previews(catalog, rows)

    def test_duplicate_catalog_channels_cannot_enter_multiple_playlists(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        catalog = prepare_channel_catalog(rows)
        catalog["channels"].append(dict(catalog["channels"][0], bucket="YABANCI"))
        with self.assertRaises(ValueError):
            render_playlist_previews(catalog, rows)

    def test_distinct_channels_render_into_separate_buckets(self):
        rows = [{"name": "A", "url": "https://example.org/a"},
                {"name": "B", "url": "https://example.org/b", "foreign": True}]
        catalog = prepare_channel_catalog(rows)
        result = render_playlist_previews(catalog, rows)
        self.assertEqual(result["counts"]["TEST_BEKLIYOR"], 1)
        self.assertEqual(result["counts"]["YABANCI"], 1)
        self.assertEqual(sum(result["counts"].values()), 2)
        self.assertFalse(result["production_writes"])

    def test_catalog_cannot_claim_production_write_or_readiness(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        for field, value in (("production_writes", True),
                             ("production_ready", True),
                             ("production_writes", 0),
                             ("production_ready", 0)):
            catalog = prepare_channel_catalog(rows)
            catalog[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                render_playlist_previews(catalog, rows)

    def test_channel_name_with_comma_roundtrips_as_valid_m3u(self):
        rows = [{"name": "TRT 1, HD", "url": "https://example.org/live"}]
        catalog = prepare_channel_catalog(rows)
        report = render_playlist_previews(catalog, rows)
        self.assertIn(",TRT 1, HD\nhttps://example.org/live",
                      report["drafts"]["TEST_BEKLIYOR"])

    def test_import_to_five_playlists_end_to_end_offline(self):
        import tempfile
        from pathlib import Path
        from madsc.playlist_previews import preview_imported_m3u
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.m3u"
            source.write_text('#EXTM3U\\n#EXTINF:-1 tvg-id="trt" group-title="Haber",TRT 1, HD\\nhttps://example.org/a\\n#EXTINF:-1,Yabancı\\nhttps://example.org/b\\n#EXTINF:-1,Tekrar\\nhttps://example.org/a\\n', encoding="utf-8")
            original = source.read_bytes()
            result = preview_imported_m3u(source)
            self.assertEqual(result["source_channel_count"], 3)
            self.assertEqual(result["duplicate_count"], 1)
            self.assertEqual(result["counts"]["TEST_BEKLIYOR"], 2)
            self.assertIn("TRT 1, HD", result["drafts"]["TEST_BEKLIYOR"])
            self.assertIn('tvg-id="trt"', result["drafts"]["TEST_BEKLIYOR"])
            self.assertEqual(original, source.read_bytes())
            self.assertFalse(result["production_writes"])

    def test_offline_cli_emits_five_drafts_without_writing_files(self):
        import contextlib
        import io
        import json
        import tempfile
        from pathlib import Path
        from madsc.playlist_previews import main
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.m3u8"
            source.write_text("#EXTM3U\\n#EXTINF:-1,One\\nhttps://example.org/a\\n", encoding="utf-8")
            before = source.read_bytes()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main([str(source)]), 0)
            report = json.loads(out.getvalue())
            self.assertEqual(len(report["drafts"]), 5)
            self.assertEqual(report["counts"]["TEST_BEKLIYOR"], 1)
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual({p.name for p in Path(directory).iterdir()}, {"input.m3u8"})

    def test_unverified_logo_rejected(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        catalog = prepare_channel_catalog(rows)
        catalog["channels"][0]["logo_url"] = "https://example.org/logo.png"
        with self.assertRaises(ValueError):
            render_playlist_previews(catalog, rows)


if __name__ == "__main__":
    unittest.main()
