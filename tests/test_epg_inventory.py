import tempfile
import unittest
from pathlib import Path
from madsc.epg_inventory import inspect_xmltv

class EpgInventoryTests(unittest.TestCase):
    def test_channel_matching_and_orphan_programme(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "epg.xml"
            p.write_text('<tv><channel id="tr.one"/><programme channel="tr.one"/><programme channel="missing"/></tv>')
            before = p.read_bytes()
            report = inspect_xmltv(p, {"tr.one", "tr.two"})
            self.assertEqual(report["matched_playlist_ids"], 1)
            self.assertEqual(report["unmatched_playlist_ids"], ["tr.two"])
            self.assertEqual(report["orphaned_programmes"], 1)
            self.assertFalse(report["device_verified"])
            self.assertEqual(before, p.read_bytes())

    def test_duplicate_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "epg.xml"
            p.write_text('<tv><channel id="dup"/><channel id="dup"/></tv>')
            with self.assertRaises(ValueError):
                inspect_xmltv(p, {"dup"})
