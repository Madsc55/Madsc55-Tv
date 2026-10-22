import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from madsc.online_evidence_reconcile import reconcile


class OnlineEvidenceReconcileTests(unittest.TestCase):
    def setUp(self):
        self.digest = "a" * 64
        self.k2 = {"mode": "REAL_REMOTE_SOURCE_READ_ONLY", "source": "https://example.org/channels.m3u",
                   "production_playlist_modified": False, "source_sha256": "b" * 64, "source_bytes": 1024, "stream_reachability_tested": False, "device_verified": False, "candidate_hashes": [self.digest]}
        self.k3 = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT", "source": self.k2["source"],
                   "production_playlist_modified": False, "source_sha256": "b" * 64, "source_bytes": 1024,
                   "probed": 1, "manifest_seen": 1, "audio_video_verified": 0,
                   "results": [{"url_sha256": self.digest, "hls_manifest_seen": True}]}

    def test_matches_digest_without_claiming_playback(self):
        report = reconcile(self.k2, self.k3)
        self.assertEqual(report["matched_manifest_seen"], 1)
        self.assertFalse(report["audio_video_verified"])
        self.assertFalse(report["production_ready"])

    def test_rejects_cross_source_evidence(self):
        self.k3["source"] = "https://example.org/other.m3u"
        with self.assertRaises(ValueError):
            reconcile(self.k2, self.k3)

    def test_rejects_different_source_snapshot(self):
        self.k3["source_sha256"] = "c" * 64
        with self.assertRaises(ValueError):
            reconcile(self.k2, self.k3)

    def test_rejects_forged_probe_totals(self):
        self.k3["probed"] = 2
        with self.assertRaisesRegex(ValueError, "probe count"):
            reconcile(self.k2, self.k3)
        self.k3["probed"] = 1
        self.k3["manifest_seen"] = 0
        with self.assertRaisesRegex(ValueError, "manifest count"):
            reconcile(self.k2, self.k3)

    def test_rejects_playback_verification_claims(self):
        self.k2["stream_reachability_tested"] = True
        with self.assertRaises(ValueError):
            reconcile(self.k2, self.k3)
        self.k2["stream_reachability_tested"] = False
        self.k3["audio_video_verified"] = 1
        with self.assertRaises(ValueError):
            reconcile(self.k2, self.k3)

    def test_cli_rejects_symlink_and_nonregular_input(self):
        from madsc.online_evidence_reconcile import main
        with TemporaryDirectory() as directory:
            root = Path(directory)
            k2_path = root / "k2.json"
            k3_path = root / "k3.json"
            k2_path.write_text(json.dumps(self.k2), encoding="utf-8")
            k3_path.write_text(json.dumps(self.k3), encoding="utf-8")
            with self.assertRaises(ValueError):
                main([str(root), str(k3_path)])
            link = root / "k2-link.json"
            link.symlink_to(k2_path)
            with self.assertRaises(ValueError):
                main([str(link), str(k3_path)])

    def test_cli_rejects_oversized_evidence(self):
        from madsc.online_evidence_reconcile import main
        with TemporaryDirectory() as directory:
            root = Path(directory)
            k2_path = root / "k2.json"
            k3_path = root / "k3.json"
            k2_path.write_bytes(b"x" * 2_000_001)
            k3_path.write_text(json.dumps(self.k3), encoding="utf-8")
            with self.assertRaises(ValueError):
                main([str(k2_path), str(k3_path)])

    def test_rejects_production_mutation(self):
        self.k2["production_playlist_modified"] = True
        with self.assertRaises(ValueError):
            reconcile(self.k2, self.k3)


if __name__ == "__main__":
    unittest.main()
