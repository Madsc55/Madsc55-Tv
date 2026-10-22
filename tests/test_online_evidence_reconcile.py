import unittest
from madsc.online_evidence_reconcile import reconcile


class OnlineEvidenceReconcileTests(unittest.TestCase):
    def setUp(self):
        self.digest = "a" * 64
        self.k2 = {"mode": "REAL_REMOTE_SOURCE_READ_ONLY", "source": "https://example.org/channels.m3u",
                   "production_playlist_modified": False, "source_sha256": "b" * 64, "candidate_hashes": [self.digest]}
        self.k3 = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT", "source": self.k2["source"],
                   "production_playlist_modified": False, "source_sha256": "b" * 64,
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

    def test_rejects_production_mutation(self):
        self.k2["production_playlist_modified"] = True
        with self.assertRaises(ValueError):
            reconcile(self.k2, self.k3)


if __name__ == "__main__":
    unittest.main()
