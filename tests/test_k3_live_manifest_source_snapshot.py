"""K3 snapshot regression tests: bounded probes, full source identity."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from madsc import k3_live_manifest_pilot as pilot
from madsc.live_discovery_pilot import MAX_BYTES


class K3SourceSnapshotTests(unittest.TestCase):
    def test_byte_limits_match_k2(self):
        self.assertEqual(pilot.SOURCE_MAX_BYTES, MAX_BYTES)

    def test_k3_hashes_full_source_and_probes_at_most_twelve(self):
        data = b"#EXTM3U\\n" + b"#EXTINF:-1,Example\\nhttps://example.org/live\\n" * 25
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return data[:size]
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            def fake_write(_root, path, content):
                (root / path).write_text(content)
            with (patch.object(pilot, "urlopen", return_value=Response()),
                  patch.object(pilot, "probe", return_value={
                      "url_sha256": "a" * 64, "hls_manifest_seen": False}),
                  patch.object(pilot, "write_fixture_report", side_effect=fake_write),
                  patch.object(pilot.Path, "cwd", return_value=root)):
                pilot.run()
            report = json.loads((root / "reports/k3-real-manifest-pilot.json").read_text())
            self.assertEqual(report["source_sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(report["source_bytes"], len(data))
            self.assertEqual(report["probed"], pilot.LIMIT)
            self.assertFalse(report["production_playlist_modified"])

    def test_k3_rejects_oversize_source(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return b"#EXTM3U\\n" + b"x" * (size + 1)
        with patch.object(pilot, "urlopen", return_value=Response()):
            with self.assertRaises(ValueError):
                list(pilot.candidates())


if __name__ == "__main__":
    unittest.main()
