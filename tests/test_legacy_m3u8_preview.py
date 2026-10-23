import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.legacy_m3u8_preview import build_legacy_m3u8_preview, SOURCE_FILES


class LegacyM3U8PreviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = []
        self.entries = []
        for filename in SOURCE_FILES:
            payload = '#EXTM3U\n#EXTINF:-1 group-title="Original",Test\nhttps://example.org/live.m3u8\n'
            (self.root / filename).write_text(payload, encoding="utf-8")
            self.manifest.append({"file": filename, "sha": hashlib.sha1(payload.encode()).hexdigest(), "count": 1})
            self.entries.append({"file": filename, "order": 0, "name": "Test"})
        self.snapshot = {"source_files": self.manifest, "entries": self.entries}

    def test_read_only_and_preserves_source_categories(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        with patch("madsc.legacy_m3u8_preview.load_historical_categories", return_value=self.snapshot):
            result = build_legacy_m3u8_preview(self.root)
        self.assertEqual(sum(result["counts"].values()), 3)
        self.assertIn('group-title="Original"', result["playlist_m3u8"])
        self.assertEqual(result["playlist_m3u8"].count("https://example.org/live.m3u8"), 3)
        self.assertFalse(result["network_probed"])
        self.assertFalse(result["production_ready"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_rejects_tampered_source(self):
        (self.root / SOURCE_FILES[0]).write_text("#EXTM3U\n", encoding="utf-8")
        with patch("madsc.legacy_m3u8_preview.load_historical_categories", return_value=self.snapshot):
            with self.assertRaisesRegex(ValueError, "SHA mismatch"):
                build_legacy_m3u8_preview(self.root)

    def test_rejects_symlinked_source(self):
        source = self.root / SOURCE_FILES[0]
        source.unlink()
        source.symlink_to(self.root / SOURCE_FILES[1])
        with patch("madsc.legacy_m3u8_preview.load_historical_categories", return_value=self.snapshot):
            with self.assertRaisesRegex(ValueError, "symlinked"):
                build_legacy_m3u8_preview(self.root)


if __name__ == "__main__":
    unittest.main()
