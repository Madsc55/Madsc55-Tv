import tempfile
import unittest
from pathlib import Path
from madsc.core import CATEGORIES, run

class IntegratedTests(unittest.TestCase):
    def test_all_five_execute_fixture_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            for category in CATEGORIES:
                report = run(category, Path(directory) / (category + ".json"))
                self.assertTrue(all(report["fixture_checks"].values()))
                self.assertFalse(report["production_writes"])
                self.assertFalse(report["checks"]["runtime_rule_evidence"])
                self.assertFalse(report["checks"]["legacy_behavioral_equivalence"])
                self.assertTrue((Path(directory) / (category + ".json")).is_file())

    def test_k2_k3_k5_two_candidates_and_ibo_preservation(self):
        """Fixture-only end-to-end handoff: identity, media, metadata, manual IBO hold."""
        from madsc.discovery import classify_candidates
        from madsc.handoff import assess_candidates
        from madsc.candidate_coordination import coordinate

        rows = [
            {"name": "Good", "url": "https://example.org/good.m3u8",
             "tvg_id": "good.tv", "tvg_logo": "https://example.org/good.png"},
            {"name": "IBO working", "url": "https://example.org/backup.m3u",
             "tvg_id": "backup.tv"},
        ]
        discovery = classify_candidates(rows)
        self.assertEqual(len(discovery["candidates"]), 2)
        by_id = {x["tvg_id"]: x["url_sha256"] for x in discovery["candidates"]}
        good, backup = by_id["good.tv"], by_id["backup.tv"]
        probes = {
            good: {"url_sha256": good, "http_status": 200, "video": True,
                   "audio": True, "duration_seconds": 40},
            backup: {"url_sha256": backup, "http_status": 503, "video": False,
                     "audio": False, "duration_seconds": 0},
        }
        ibo = {backup: "WORKING"}
        handoff = assess_candidates(discovery, probes, ibo)
        report = coordinate(rows, probes, {backup: 3},
                            {"good.tv"}, {"good.tv"}, ibo)
        h = {x["url_sha256"]: x for x in handoff["assessed"]}
        k5 = {x["url_sha256"]: x for x in report["candidates"]}
        self.assertEqual(set(h), set(k5))
        for digest in (good, backup):
            self.assertEqual(h[digest]["technical_status"], k5[digest]["technical_status"])
            self.assertFalse(h[digest]["production_change_allowed"])
            self.assertFalse(k5[digest]["production_change_allowed"])
            self.assertFalse(k5[digest]["delete_allowed"])
        self.assertEqual(k5[good]["score"], 80)
        self.assertTrue(k5[good]["hold"])  # No device approval
        self.assertTrue(k5[backup]["protected_working"])
        self.assertEqual(k5[backup]["next_action"], "PRESERVE_IBO_WORKING_AND_REVIEW")
        self.assertTrue(k5[backup]["hold"])
        self.assertFalse(report["production_writes"])
        self.assertFalse(report["network_probed"])
        self.assertFalse(report["ibo_device_verified"])

    def test_k2_k3_k5_orphan_media_evidence_fails_closed(self):
        from madsc.discovery import classify_candidates
        from madsc.handoff import assess_candidates
        from madsc.candidate_coordination import coordinate

        rows = [{"name": "A", "url": "https://example.org/a.m3u8"}]
        discovery = classify_candidates(rows)
        orphan = "f" * 64
        evidence = {orphan: {"url_sha256": orphan, "http_status": 200,
                             "video": True, "audio": True, "duration_seconds": 40}}
        with self.assertRaises(ValueError):
            assess_candidates(discovery, evidence)
        with self.assertRaises(ValueError):
            coordinate(rows, evidence, {})

if __name__ == "__main__":
    unittest.main()
