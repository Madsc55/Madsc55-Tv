"""Run pinned legacy K3 EPG/logo join in a disposable tree and compare outputs."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from madsc.legacy_epg_logo import join_pilot

LEGACY = Path(__file__).parent / "fixtures" / "legacy_candidate_epg_logo_join.py"


class LegacyEpgLogoDifferentialTests(unittest.TestCase):
    def test_old_and_new_same_epg_logo_decisions(self):
        cases = [
            (
                [{"channel": "One", "channel_id": "a", "stream_sha256": "h1"},
                 {"channel": "Two", "channel_id": "b", "stream_sha256": "h2"},
                 {"channel": "Three", "channel_id": "unknown", "stream_sha256": "h3"}],
                [{"stream_sha256": "h1", "status": "PREPARED",
                  "visual_match": "NOT_VERIFIED"}],
                '<tv><channel id="a"/><channel id="b"/><programme channel="a"/></tv>',
            ),
            ([], [], "<tv/>"),
            (
                [{"channel": "Repeat", "channel_id": "x", "stream_sha256": "same"},
                 {"channel": "Repeat", "channel_id": "x", "stream_sha256": "different"}],
                [{"stream_sha256": "different", "status": "READY_FOR_REVIEW"}],
                '<tv><channel id="x"/><programme channel="x"/><programme channel="x"/></tv>',
            ),
        ]
        for candidates, logos, xml in cases:
            with self.subTest(candidates=len(candidates)), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "scripts").mkdir()
                (root / "madsc_kesif").mkdir()
                (root / "epg").mkdir()
                script = root / "scripts" / "candidate_epg_logo_join.py"
                script.write_bytes(LEGACY.read_bytes())
                (root / "madsc_kesif" / "logo_candidates.json").write_text(
                    json.dumps(candidates), encoding="utf-8")
                (root / "madsc_kesif" / "candidate_logos.json").write_text(
                    json.dumps({"results": logos}), encoding="utf-8")
                xml_path = root / "epg" / "ibo-test-epg.xml"
                xml_path.write_text(xml, encoding="utf-8")
                old = subprocess.run([sys.executable, str(script)], cwd=root,
                                     capture_output=True, text=True, timeout=10)
                self.assertEqual(old.returncode, 0, old.stderr)
                old_report = json.loads(
                    (root / "madsc_kesif" / "candidate_epg_logo_join.json").read_text(
                        encoding="utf-8"))
                new = join_pilot(candidates, logos, xml_path)
                for key in ("source_candidates", "candidate_results", "pilot_epg_channels"):
                    self.assertEqual(old_report[key], new[key])
                self.assertFalse(new["production_writes"])
                self.assertFalse(new["production_ready"])
                self.assertTrue(all(not row["playlist_approved"]
                                    for row in old_report["candidate_results"]))


if __name__ == "__main__":
    unittest.main()
