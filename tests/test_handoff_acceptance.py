import unittest
from madsc.discovery import classify_candidates
from madsc.artifact_handoff import pack
from madsc.handoff_acceptance import verify

class HandoffAcceptanceTests(unittest.TestCase):
    def setUp(self):
        discovery = classify_candidates([{"name": "A", "url": "https://example.org/a.m3u8"}])
        self.k2 = pack(discovery, "123", "a" * 40)
        self.report = {"schema": "madsc-handoff-verification-v1", "run_id": "123",
                       "commit_sha": "a" * 40, "source_digest": self.k2["digest"],
                       "candidate_count": 1, "read_only": True,
                       "network_probed": False, "production_ready": False}

    def test_same_run_accepted_without_production_claim(self):
        result = verify(self.k2, self.report, self.report, "123", "a" * 40)
        self.assertTrue(result["k2_k3_k5_same_run_verified"])
        self.assertFalse(result["production_ready"])

    def test_wrong_run_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, self.report, "124", "a" * 40)

    def test_mismatched_k5_digest_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, {**self.report, "source_digest": "f" * 64}, "123", "a" * 40)

    def test_false_production_claim_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, {**self.report, "production_ready": True}, self.report, "123", "a" * 40)

    def test_mismatched_candidate_count_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, {**self.report, "candidate_count": 2}, "123", "a" * 40)

    def test_extra_fields_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, {**self.report, "extra": True}, self.report, "123", "a" * 40)

    def test_false_network_probe_claim_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, {**self.report, "network_probed": True}, "123", "a" * 40)

    def test_mismatched_k3_commit_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, {**self.report, "commit_sha": "b" * 40}, self.report, "123", "a" * 40)


    def test_k2_payload_tampering_rejected_across_categories(self):
        changed = {**self.k2, "discovery": {**self.k2["discovery"], "candidates": []}}
        with self.assertRaises(ValueError):
            verify(changed, self.report, self.report, "123", "a" * 40)

    def test_k3_and_k5_run_identity_mismatch_rejected(self):
        for field, value in (("run_id", "999"), ("commit_sha", "b" * 40)):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    verify(self.k2, {**self.report, field: value},
                           self.report, "123", "a" * 40)
                with self.assertRaises(ValueError):
                    verify(self.k2, self.report,
                           {**self.report, field: value}, "123", "a" * 40)

    def test_k3_and_k5_must_not_claim_live_probing(self):
        for field, value in (("read_only", False), ("network_probed", True),
                             ("production_ready", True)):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    verify(self.k2, {**self.report, field: value},
                           self.report, "123", "a" * 40)

    def test_duplicate_json_keys_rejected(self):
        import tempfile
        from pathlib import Path
        from madsc.handoff_acceptance import load
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "duplicate.json"
            path.write_text('{"run_id":"123","run_id":"999"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load(path)

    def test_symlink_evidence_file_rejected(self):
        import json
        import tempfile
        from pathlib import Path
        from madsc.handoff_acceptance import load
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "report.json"
            target.write_text(json.dumps(self.report), encoding="utf-8")
            link = Path(d) / "link.json"
            link.symlink_to(target)
            with self.assertRaises(ValueError):
                load(link)
