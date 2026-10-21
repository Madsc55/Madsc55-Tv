import unittest
from madsc.k3_three_stage_gate import assess_three_stage_probes


def sample(at, digest="a" * 64, status=200):
    return {"captured_at": at, "probe": {
        "url_sha256": digest, "http_status": status,
        "video": True, "audio": True, "duration_seconds": 31}}


class K3ThreeStageGateTests(unittest.TestCase):
    def test_three_samples_six_hours_apart(self):
        rows = [sample("2026-10-20T00:00:00Z"),
                sample("2026-10-20T06:00:00Z"),
                sample("2026-10-20T12:00:00Z")]
        result = assess_three_stage_probes(rows)
        self.assertTrue(result["three_stage_preliminary_pass"])
        self.assertFalse(result["actual_network_measurements_verified"])
        self.assertFalse(result["production_change_allowed"])

    def test_short_spacing_rejected(self):
        with self.assertRaises(ValueError):
            assess_three_stage_probes([
                sample("2026-10-20T00:00:00Z"),
                sample("2026-10-20T05:59:59Z"),
                sample("2026-10-20T12:00:00Z")])

    def test_mixed_fingerprint_rejected(self):
        with self.assertRaises(ValueError):
            assess_three_stage_probes([
                sample("2026-10-20T00:00:00Z"),
                sample("2026-10-20T06:00:00Z", "b" * 64),
                sample("2026-10-20T12:00:00Z")])

    def test_one_failed_sample_prevents_preliminary_pass(self):
        result = assess_three_stage_probes([
            sample("2026-10-20T00:00:00Z"),
            sample("2026-10-20T06:00:00Z", status=503),
            sample("2026-10-20T12:00:00Z")])
        self.assertEqual(result["preliminary_passes"], 2)
        self.assertFalse(result["three_stage_preliminary_pass"])

    def test_naive_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            assess_three_stage_probes([
                sample("2026-10-20T00:00:00"),
                sample("2026-10-20T06:00:00Z"),
                sample("2026-10-20T12:00:00Z")])


if __name__ == "__main__":
    unittest.main()
