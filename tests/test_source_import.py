import tempfile
import os
import unittest
from pathlib import Path
from madsc.source_import import extract_candidates

class SourceImportTests(unittest.TestCase):
    def test_both_formats_and_duplicates(self):
        for suffix in (".m3u", ".m3u8"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as d:
                p = Path(d) / ("source" + suffix)
                p.write_text("#EXTM3U\n#EXTINF:-1,One\nhttps://example.org/a.m3u8\n#EXTINF:-1,Duplicate\nhttps://example.org/a.m3u8\n#EXTINF:-1,Bad\nfile:///bad\n", encoding="utf-8")
                before = p.read_bytes()
                result = extract_candidates(p)
                self.assertEqual((len(result["candidates"]), len(result["duplicates"]), len(result["rejected"])), (1, 1, 1))
                self.assertEqual(result["source_format"], suffix)
                self.assertFalse(result["production_playlist_modified"])
                self.assertEqual(before, p.read_bytes())
    def test_header_with_utf8_bom(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text("\ufeff#EXTM3U\n#EXTINF:-1,One\nhttps://example.org/one\n", encoding="utf-8")
            result = extract_candidates(p)
            self.assertEqual(len(result["candidates"]), 1)
            self.assertFalse(result["production_playlist_modified"])

    def test_invalid_candidate_url_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1,One\nfile:///local\n", encoding="utf-8")
            result = extract_candidates(p)
            self.assertEqual(len(result["candidates"]), 0)
            self.assertEqual(len(result["rejected"]), 1)

    def test_invalid_extinf_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            for metadata in ("#EXTINF:-1", "#EXTINF:-1,"):
                p.write_text("#EXTM3U\n" + metadata + "\nhttps://example.org/one\n", encoding="utf-8")
                with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                    extract_candidates(p)

    def test_tvg_id_preserved_for_epg_handoff(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u8"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tv",TRT 1\nhttps://example.org/live\n', encoding="utf-8")
            result = extract_candidates(p)
            self.assertEqual(result["candidates"][0]["tvg_id"], "trt1.tv")
            self.assertEqual(result["candidates"][0]["name"], "TRT 1")

    def test_missing_url_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1,One\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_candidates(p)
    def test_quoted_commas_preserve_epg_logo_and_group_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u8"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt,1" tvg-logo="https://example.org/a,b.png" group-title="News, TR",TRT 1\nhttps://example.org/live\n', encoding="utf-8")
            before = p.read_bytes()
            result = extract_candidates(p)
            item = result["candidates"][0]
            self.assertEqual(item["name"], "TRT 1")
            self.assertEqual(item["tvg_id"], "trt,1")
            self.assertEqual(item["tvg_logo"], "https://example.org/a,b.png")
            self.assertEqual(item["group_title"], "News, TR")
            self.assertEqual(before, p.read_bytes())

    def test_both_formats_preserve_logo_and_group(self):
        for suffix in (".m3u", ".m3u8"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as d:
                p = Path(d) / ("source" + suffix)
                p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt" tvg-logo="https://example.org/logo.png" group-title="Haber",TRT\nhttps://example.org/live\n', encoding="utf-8")
                item = extract_candidates(p)["candidates"][0]
                self.assertEqual(item["tvg_logo"], "https://example.org/logo.png")
                self.assertEqual(item["group_title"], "Haber")
    def test_channel_name_with_commas_survives_full_handoff(self):
        from madsc.handoff import assess_candidates
        for suffix in (".m3u", ".m3u8"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as d:
                p = Path(d) / ("source" + suffix)
                p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1" tvg-logo="https://example.org/logo.png" group-title="News, TR",TRT 1, HD\nhttps://example.org/live\n', encoding="utf-8")
                original = p.read_bytes()
                discovery = extract_candidates(p)
                assessed = assess_candidates(discovery, {})["assessed"][0]
                self.assertEqual(assessed["name"], "TRT 1, HD")
                self.assertEqual(assessed["tvg_id"], "trt1")
                self.assertEqual(assessed["tvg_logo"], "https://example.org/logo.png")
                self.assertEqual(assessed["group_title"], "News, TR")
                self.assertEqual(assessed["technical_status"], "UNTESTED")
                self.assertFalse(assessed["ibo_device_verified"])
                self.assertEqual(p.read_bytes(), original)

    def test_duplicate_metadata_attributes_rejected_case_insensitively(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            for metadata in (
                '#EXTINF:-1 tvg-id="first" tvg-id="second",Channel',
                '#EXTINF:-1 tvg-id="first" TVG-ID="second",Channel',
                '#EXTINF:-1 group-title="News" group-title="Sports",Channel',
            ):
                p.write_text("#EXTM3U\n" + metadata + "\nhttps://example.org/live\n",
                             encoding="utf-8")
                with self.subTest(metadata=metadata), self.assertRaisesRegex(
                        ValueError, "Duplicate metadata attribute"):
                    extract_candidates(p)

    def test_uppercase_metadata_attributes_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u8"
            p.write_text('#EXTM3U\n#EXTINF:-1 TVG-ID="upper.id" TVG-LOGO="https://example.org/logo.png" GROUP-TITLE="News",Upper\nhttps://example.org/live\n', encoding="utf-8")
            result = extract_candidates(p)
            candidate = result["candidates"][0]
            self.assertEqual(candidate["tvg_id"], "upper.id")
            self.assertEqual(candidate["tvg_logo"], "https://example.org/logo.png")
            self.assertEqual(candidate["group_title"], "News")

    def test_unbalanced_attribute_quotes_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="broken,Channel\nhttps://example.org/live\n', encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_candidates(p)

    def test_quoted_channel_name_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text('#EXTM3U\n#EXTINF:-1,Channel "HD"\nhttps://example.org/live\n', encoding="utf-8")
            result = extract_candidates(p)
            self.assertEqual(result["candidates"][0]["name"], 'Channel "HD"')

    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            original = Path(d) / "original.m3u"
            original.write_text("#EXTM3U\n", encoding="utf-8")
            link = Path(d) / "linked.m3u"
            link.symlink_to(original)
            with self.assertRaises(ValueError):
                extract_candidates(link)

    def test_hardlinked_and_oversized_sources_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "original.m3u"
            source.write_text("#EXTM3U\n", encoding="utf-8")
            os.link(source, root / "hardlink.m3u")
            with self.assertRaises(ValueError):
                extract_candidates(source)
            oversized = root / "oversized.m3u8"
            with oversized.open("wb") as stream:
                stream.truncate(16 * 1024 * 1024 + 1)
            with self.assertRaises(ValueError):
                extract_candidates(oversized)

    def test_invalid_utf8_source_rejected_cleanly(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_bytes(b"#EXTM3U\n#EXTINF:-1,Channel\nhttps://example.org/live\n\xff")
            with self.assertRaisesRegex(ValueError, "valid UTF-8"):
                extract_candidates(p)

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                extract_candidates(Path(d) / "missing.m3u8")

    def test_string_path_supported_without_mutating_source(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1,One\nhttps://example.org/one\n", encoding="utf-8")
            before = p.read_bytes()
            result = extract_candidates(str(p))
            self.assertEqual(len(result["candidates"]), 1)
            self.assertEqual(before, p.read_bytes())
            self.assertFalse(result["production_playlist_modified"])
