import tempfile
import unittest
from pathlib import Path
from madsc.preflight import preflight

class PreflightTests(unittest.TestCase):
    def test_m3u8_xmltv_pair(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="se.demo",Demo\nhttps://example.org/live.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="se.demo"/></tv>', encoding="utf-8")
            original = (p.read_bytes(), e.read_bytes())
            result = preflight(p, e)
            self.assertTrue(result["ready_for_device_test"])
            self.assertFalse(result["production_approved"])
            self.assertEqual(original, (p.read_bytes(), e.read_bytes()))
    def test_wrong_names_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                preflight(Path(d)/"playlist.m3u", Path(d)/"xmltv.xml")
