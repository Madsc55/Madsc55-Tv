import tempfile
import unittest
from pathlib import Path
from madsc.epg import check_epg_mapping

class EpgTests(unittest.TestCase):
    def test_empty_playlist_is_not_reported_as_matching(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text("#EXTM3U\\n", encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertEqual(result["playlist_channels"], 0)
            self.assertFalse(result["matching_verified"])

    def test_playlist_m3u8_and_xmltv_match(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/index.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"><display-name>TRT 1</display-name></channel><programme channel="trt1.tr" start="20261019010000 +0000" stop="20261019020000 +0000"><title>Test</title></programme></tv>', encoding="utf-8")
            original = p.read_bytes()
            result = check_epg_mapping(p, e)
            self.assertTrue(result["matching_verified"])
            self.assertFalse(result["device_verified"])
            self.assertEqual(p.read_bytes(), original)
            e.write_text('<tv><channel id="other"/></tv>', encoding="utf-8")
            self.assertFalse(check_epg_mapping(p, e)["matching_verified"])
