"""Offline regression checks for source-bound replacement mapping review."""
import unittest
from unittest.mock import patch

from madsc.legacy_replacement_mapping_review import review_replacement_mappings
from madsc.legacy_parity_evidence import CENTRAL_REPLACEMENT_WORKFLOWS

LEGACY = ".github/workflows/old.yml"
REPLACEMENT = ".github/workflows/madsc-01-guvenlik.yml"


class MappingReviewTests(unittest.TestCase):
    def setUp(self):
        self.inventory = {"workflows": [{"path": LEGACY, "git_blob_sha": "a" * 40}]}
        self.readiness = {"rows": [{
            "workflow_path": REPLACEMENT, "workflow_blob_sha": "b" * 40,
            "declared_file_binding": {
                "input_path": "input.txt", "output_label": "guard",
                "output_path": "guard.txt"},
            "marker_contract_complete": True,
            "static_file_binding_complete": True,
            "input_digest_binding_complete": True,
            "controlled_process_contract_complete": True,
        }]}
        self.readiness["rows"].extend(
            {"workflow_path": path, "workflow_blob_sha": "c" * 40,
             "declared_file_binding": None,
             "marker_contract_complete": False,
             "static_file_binding_complete": False,
             "input_digest_binding_complete": False,
             "controlled_process_contract_complete": False}
            for path in sorted(CENTRAL_REPLACEMENT_WORKFLOWS - {REPLACEMENT}))
        self.row = {
            "legacy_path": LEGACY, "legacy_blob_sha": "a" * 40,
            "replacement_workflow_path": REPLACEMENT,
            "replacement_blob_sha": "b" * 40,
            "input_role": "input.txt", "output_role": "guard=guard.txt",
            "review_rationale": "Manual source-level behavior candidate",
        }

    def review(self, rows):
        with (patch("madsc.legacy_replacement_mapping_review.reconcile_legacy_scope",
                    return_value={"legacy_paths": [LEGACY]}),
              patch("madsc.legacy_replacement_mapping_review.validate_inventory",
                    return_value=self.inventory["workflows"]),
              patch("madsc.legacy_replacement_mapping_review.audit_parity_workflow_readiness",
                    return_value=self.readiness)):
            return review_replacement_mappings(self.inventory, rows, ".")

    def test_matching_static_candidate_never_accepted(self):
        result = self.review([self.row])
        self.assertEqual(result["static_contract_candidates"], 1)
        self.assertEqual(result["behavioral_parity_accepted"], 0)
        self.assertFalse(result["production_ready"])

    def test_empty_review_never_accepted(self):
        self.assertEqual(self.review([])["unmapped_legacy_workflows"], 1)

    def test_duplicate_mapping_rejected(self):
        with self.assertRaises(ValueError):
            self.review([self.row, self.row])

    def test_stale_legacy_blob_rejected(self):
        with self.assertRaises(ValueError):
            self.review([{**self.row, "legacy_blob_sha": "c" * 40}])

    def test_stale_replacement_blob_rejected(self):
        with self.assertRaises(ValueError):
            self.review([{**self.row, "replacement_blob_sha": "c" * 40}])

    def test_mismatched_role_blocks_without_approval(self):
        result = self.review([{**self.row, "output_role": "wrong=path"}])
        self.assertEqual(result["static_contract_candidates"], 0)
        self.assertEqual(result["rows"][0]["status"], "mapping_contract_blocked")

    def test_unknown_legacy_rejected(self):
        with self.assertRaises(ValueError):
            self.review([{**self.row, "legacy_path": ".github/workflows/unknown.yml"}])

    def test_missing_replacement_workflow_rejected(self):
        self.readiness["rows"].pop()
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_duplicate_replacement_workflow_rejected(self):
        self.readiness["rows"].append(dict(self.readiness["rows"][0]))
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_malformed_replacement_blob_rejected(self):
        self.readiness["rows"][0]["workflow_blob_sha"] = "not-a-git-sha"
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_missing_replacement_contract_field_rejected(self):
        del self.readiness["rows"][0]["input_digest_binding_complete"]
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_nonboolean_replacement_contract_flag_rejected(self):
        self.readiness["rows"][0]["marker_contract_complete"] = "true"
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_nonstring_replacement_path_rejected(self):
        self.readiness["rows"][0]["workflow_path"] = ["invalid"]
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_nonstring_binding_label_rejected(self):
        self.readiness["rows"][0]["declared_file_binding"]["output_label"] = []
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_empty_binding_path_rejected(self):
        self.readiness["rows"][0]["declared_file_binding"]["input_path"] = ""
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_uncontrolled_consumer_blocks_static_candidate(self):
        self.readiness["rows"][0]["controlled_process_contract_complete"] = False
        result = self.review([self.row])
        self.assertEqual(result["static_contract_candidates"], 0)
        self.assertEqual(result["rows"][0]["status"], "mapping_contract_blocked")

    def test_missing_controlled_process_contract_rejected(self):
        del self.readiness["rows"][0]["controlled_process_contract_complete"]
        with self.assertRaises(ValueError):
            self.review([self.row])

    def test_missing_rationale_rejected(self):
        with self.assertRaises(ValueError):
            self.review([{**self.row, "review_rationale": ""}])


if __name__ == "__main__":
    unittest.main()
