"""Offline regression for the same bounded K2/K3 source snapshot."""
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from madsc import live_discovery_pilot as k2
from madsc import k3_live_manifest_pilot as k3


class SharedSnapshotTests(unittest.TestCase):
    def test_both_pilots_use_identical_bytes_without_network_fetch(self):
        raw = (b"#EXTM3U\n"
               b"#EXTINF:-1,One\nhttps://example.org/one\n"
               b"#EXTINF:-1,Two\nhttps://example.org/two\n")
        with TemporaryDirectory() as d:
            snapshot = Path(d) / "snapshot.m3u"
            snapshot.write_bytes(raw)
            k3_evidence = {}
            with patch.object(k2, "urlopen", side_effect=AssertionError("K2 fetched source")), \
                 patch.object(k3, "urlopen", side_effect=AssertionError("K3 fetched source")), \
                 patch.object(k2, "write_fixture_report") as k2_write:
                k2.run(snapshot)
                self.assertEqual(k2_write.call_count, 1)
                k2_report = __import__("json").loads(k2_write.call_args.args[2])
                rows = list(k3.candidates(k3_evidence, snapshot))
            self.assertEqual(len(rows), 2)
            self.assertEqual(k2_report["source_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(k2_report["source_sha256"], k3_evidence["source_sha256"])
            self.assertEqual(k2_report["source_bytes"], k3_evidence["source_bytes"])

    def test_rejects_oversize_shared_snapshot(self):
        with TemporaryDirectory() as d:
            snapshot = Path(d) / "oversize.m3u"
            snapshot.write_bytes(b"#EXTM3U\n" + b"x" * (k2.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                k2.run(snapshot)
            with self.assertRaises(ValueError):
                list(k3.candidates({}, snapshot))

    def test_rejects_symlink_snapshot(self):
        with TemporaryDirectory() as d:
            real = Path(d) / "real.m3u"
            real.write_bytes(b"#EXTM3U\n")
            link = Path(d) / "link.m3u"
            link.symlink_to(real)
            with self.assertRaises(ValueError):
                k2.run(link)
            with self.assertRaises(ValueError):
                list(k3.candidates({}, link))


if __name__ == "__main__":
    unittest.main()
