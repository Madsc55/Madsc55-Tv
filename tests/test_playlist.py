import tempfile
import unittest
from pathlib import Path
from madsc.playlist import inspect_playlist, compare_snapshots

class PlaylistTests(unittest.TestCase):
    def test_read_only_integrity_and_change_detection(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1 tvg-id=\"a\",A\nhttps://example.org/a\n")
            before = p.read_bytes()
            first = inspect_playlist(p)
            self.assertEqual(first["channel_count"], 1)
            self.assertEqual(before, p.read_bytes())
            self.assertTrue(compare_snapshots(first, inspect_playlist(p))["identical"])
            p.write_text("#EXTM3U\n#EXTINF:-1 tvg-id=\"b\",B\nhttps://example.org/b\n")
            self.assertFalse(compare_snapshots(first, inspect_playlist(p))["identical"])
    def test_invalid_playlist_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1,A\n")
            with self.assertRaises(ValueError):
                inspect_playlist(p)
