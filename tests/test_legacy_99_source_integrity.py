"""Source audit must reject forged workflow blobs before reporting."""
import base64
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc import legacy_99_bulk_audit as audit


class Legacy99SourceIntegrityTests(unittest.TestCase):
    def test_all_99_blobs_verified_byte_exactly(self):
        raw = b"name: sample\non: workflow_dispatch\n"
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        entries = [{"path": f".github/workflows/{i:03d}.yml",
                    "type": "blob", "size": len(raw), "sha": sha}
                   for i in range(99)]
        def fake_github(url, token):
            if "/git/trees/" in url:
                return {"tree": entries, "sha": "source-tree", "truncated": False}
            return {"sha": sha, "encoding": "base64",
                    "content": base64.b64encode(raw).decode()}
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, "github", side_effect=fake_github):
            path = Path(temp) / "audit.json"
            audit.run(path, "")
            import json
            report = json.loads(path.read_text())
            self.assertEqual(report["source_workflow_count"], 99)
            self.assertTrue(report["candidate_mapping_only"])
            self.assertEqual(len(report["workflows"]), 99)
            self.assertTrue(all(not x["stage_mapping_reviewed"] for x in report["workflows"]))
            self.assertEqual(report["source_tree_sha"], "source-tree")
            self.assertEqual(report["behavioral_parity_verified_count"], 0)
            self.assertEqual(report["blocked_workflow_count"], 99)
            self.assertTrue(all(row["failure_circuit_source_scope"]["runtime_verified"] is False
                                for row in report["workflows"]))
            self.assertTrue(all("jobs" in row["failure_circuit_source_scope"]
                                for row in report["workflows"]))
            self.assertEqual(set(report["missing_evidence_by_type"].values()), {99})
            self.assertTrue(all(row["behavioral_evidence_status"] ==
                                "BLOCKED_NEEDS_BEHAVIOR_EVIDENCE"
                                for row in report["workflows"]))
            self.assertTrue(all(len(row["evidence_missing"]) == 6
                                for row in report["workflows"]))

    def test_unsafe_output_rejected_before_network(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, "github") as network:
            root = Path(temp)
            with self.assertRaises(PermissionError):
                audit.run(root / "xmltv.xml", "")
            network.assert_not_called()
            outside = root / "outside"
            outside.mkdir()
            (root / "alias").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(PermissionError):
                audit.run(root / "alias" / "audit.json", "")
            network.assert_not_called()
            self.assertEqual(list(outside.iterdir()), [])

    def test_blocker_summary_rejects_forged_acceptance(self):
        missing = ["legacy_execution", "new_execution", "input_output_comparison",
                   "side_effect_comparison", "failure_timeout_comparison",
                   "reviewer_approval"]
        row = {"behavioral_parity_verified": False, "evidence_missing": missing}
        self.assertEqual(audit.summarize_blockers([row])["legacy_execution"], 1)
        with self.assertRaises(ValueError):
            audit.summarize_blockers([dict(row, behavioral_parity_verified=True)])
        with self.assertRaises(ValueError):
            audit.summarize_blockers([dict(row, evidence_missing=missing[:-1])])

    def test_stage_hints_remain_provisional(self):
        self.assertEqual(audit.candidate_stages("epg-gunluk.yml"), ["K3"])
        self.assertEqual(audit.candidate_stages("madsc-tum-sistem-yedek.yml"), ["K4"])
        self.assertEqual(audit.candidate_stages("unmapped.yml"), ["UNCLASSIFIED"])

    def test_forged_blob_is_rejected(self):
        raw = b"name: sample\n"
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        entries = [{"path": f".github/workflows/{i:03d}.yml",
                    "type": "blob", "size": len(raw), "sha": sha}
                   for i in range(99)]
        def fake_github(url, token):
            if "/git/trees/" in url:
                return {"tree": entries, "truncated": False}
            return {"sha": sha, "encoding": "base64",
                    "content": base64.b64encode(b"evil payload!").decode()}
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, "github", side_effect=fake_github):
            with self.assertRaises(ValueError):
                audit.run(Path(temp) / "audit.json", "")


if __name__ == "__main__":
    unittest.main()
