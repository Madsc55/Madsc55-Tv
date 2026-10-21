import unittest
from hashlib import sha256
from madsc.channel_catalog import prepare_channel_catalog


class ChannelCatalogTests(unittest.TestCase):
    def test_discovery_to_presentation_and_legacy_order(self):
        rows = [
            {"name": "izmir tv", "url": "https://example.org/1", "group_title": "Haber", "tvg_id": "a"},
            {"name": "yabancı kanal", "url": "https://example.org/2", "group_title": "Yabancı", "foreign": True},
            {"name": "tekrar", "url": "https://example.org/1", "group_title": "Haber"},
        ]
        digest = sha256(b"https://example.org/1").hexdigest()
        out = prepare_channel_catalog(
            rows,
            measurements={digest: {"verified": True, "width": 1920, "height": 1080,
                                   "technical_status": "NEEDS_REVIEW"}},
            logos={digest: {"url": "https://example.org/a.png", "identity_match": True, "reachable": True}},
            ibo_results={digest: "WORKING"})
        self.assertEqual(len(out["channels"]), 2)
        self.assertEqual(len(out["duplicates"]), 1)
        self.assertEqual(out["category_order"], ["Haber", "Yabancı"])
        self.assertEqual(out["channels"][0]["display_name"], "İZMİR TV FHD")
        self.assertEqual(out["channels"][0]["bucket"], "IBO_ONAYLI_CALISAN")
        self.assertTrue(out["channels"][0]["logo_verified"])
        self.assertFalse(out["production_writes"])

    def test_summary_counts_candidates_duplicates_and_ibo_without_claiming_device_test(self):
        rows = [
            {"name": "kanal", "url": "https://example.org/one"},
            {"name": "tekrar", "url": "https://example.org/one"},
            {"name": "yabanci", "url": "https://example.org/two", "foreign": True},
        ]
        digest = sha256(b"https://example.org/one").hexdigest()
        out = prepare_channel_catalog(rows, ibo_results={digest: "WORKING"})
        summary = out["summary"]
        self.assertEqual(summary["candidate_count"], 2)
        self.assertEqual(summary["duplicate_count"], 1)
        self.assertEqual(summary["technical_probe_count"], 0)
        self.assertEqual(summary["three_stage_evidence_count"], 0)
        self.assertEqual(summary["buckets"]["IBO_ONAYLI_CALISAN"], 1)
        self.assertFalse(summary["device_acceptance_proven"])

    def test_probe_evidence_drives_working_candidate(self):
        rows = [{"name": "kanal", "url": "https://example.org/ok", "group_title": "Haber"}]
        digest = sha256(b"https://example.org/ok").hexdigest()
        probe = {"url_sha256": digest, "http_status": 200, "video": True,
                 "audio": True, "duration_seconds": 31}
        out = prepare_channel_catalog(rows, probes={digest: probe})
        self.assertEqual(out["channels"][0]["technical_status"], "PRELIMINARY_PASS")
        self.assertEqual(out["channels"][0]["bucket"], "CALISAN_ADAY")
        self.assertFalse(out["network_probed"])

    def test_claimed_status_without_probe_is_not_accepted(self):
        rows = [{"name": "kanal", "url": "https://example.org/ok"}]
        digest = sha256(b"https://example.org/ok").hexdigest()
        out = prepare_channel_catalog(rows, measurements={
            digest: {"technical_status": "PRELIMINARY_PASS", "verified": False}})
        self.assertEqual(out["channels"][0]["technical_status"], "UNTESTED")
        self.assertEqual(out["channels"][0]["bucket"], "TEST_BEKLIYOR")

    def test_probe_fingerprint_mismatch_is_rejected(self):
        rows = [{"name": "kanal", "url": "https://example.org/ok"}]
        digest = sha256(b"https://example.org/ok").hexdigest()
        with self.assertRaises(ValueError):
            prepare_channel_catalog(rows, probes={digest: {"url_sha256": "0" * 64}})

    def test_three_stage_pass_cannot_override_failed_current_probe(self):
        rows = [{"name": "kanal", "url": "https://example.org/check"}]
        digest = sha256(b"https://example.org/check").hexdigest()
        stage = [
            {"captured_at": f"2026-10-20T{hour:02d}:00:00Z",
             "probe": {"url_sha256": digest, "http_status": 200,
                       "video": True, "audio": True, "duration_seconds": 31}}
            for hour in (0, 6, 12)
        ]
        current = {"url_sha256": digest, "http_status": 503,
                   "video": False, "audio": False, "duration_seconds": 0}
        with self.assertRaises(ValueError):
            prepare_channel_catalog(rows, probes={digest: current},
                                    three_stage={digest: stage})

    def test_unknown_fingerprint_rejected(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        with self.assertRaises(ValueError):
            prepare_channel_catalog(rows, measurements={"x" * 64: {"verified": True}})

    def test_orphan_probe_evidence_rejected(self):
        with self.assertRaises(ValueError):
            prepare_channel_catalog([{"name": "A", "url": "https://example.org/a"}],
                                    probes={"0" * 64: {}})

    def test_no_evidence_does_not_claim_live_checks(self):
        out = prepare_channel_catalog([{"name": "A", "url": "https://example.org/a"}])
        self.assertEqual(out["channels"][0]["bucket"], "TEST_BEKLIYOR")
        self.assertFalse(out["network_probed"])
        self.assertFalse(out["device_verified_by_this_function"])


if __name__ == "__main__":
    unittest.main()
