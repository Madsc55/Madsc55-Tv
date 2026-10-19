import tempfile
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

    def test_missing_url_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1,One\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                extract_candidates(p)
