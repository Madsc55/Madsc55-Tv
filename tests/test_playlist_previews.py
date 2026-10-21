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

    def test_unverified_logo_rejected(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        catalog = prepare_channel_catalog(rows)
        catalog["channels"][0]["logo_url"] = "https://example.org/logo.png"
        with self.assertRaises(ValueError):
            render_playlist_previews(catalog, rows)


if __name__ == "__main__":
    unittest.main()
