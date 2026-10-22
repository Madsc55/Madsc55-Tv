import unittest
from madsc.legacy_parity_evidence import ledger

def inventory():
    return {"source_repository": "Madsc55/madsc-tv",
            "source_branch": "madsc/bes-sistem-toplu-birlestirme",
            "workflows": [{"path": f".github/workflows/w{i:02}.yml", "candidate_k_stages": ["K5"]}
                          for i in range(99)]}
class EvidenceLedgerTest(unittest.TestCase):
    def test_malformed_inventory_fails_with_value_error(self):
        for bad in (None, [], "not an inventory"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                ledger(bad)
        bad = inventory()
        bad["workflows"][0] = None
        with self.assertRaises(ValueError):
            ledger(bad)
        bad = inventory()
        bad["workflows"][0] = {"path": None}
        with self.assertRaises(ValueError):
            ledger(bad)

    def test_inventory_rejects_path_traversal_and_non_workflow_files(self):
        for path in (".github/workflows/../evil.yml", ".github/workflows/nested/a.yml",
                     ".github/workflows/README.md", ".github/workflows/a\\\\b.yml"):
            bad = inventory()
            bad["workflows"][0]["path"] = path
            with self.subTest(path=path), self.assertRaises(ValueError):
                ledger(bad)

    def test_invalid_evidence_fails_before_partial_ledger(self):
        with self.assertRaises(ValueError):
            ledger(inventory(), {".github/workflows/w98.yml": {"unknown": {}}})
        with self.assertRaises(ValueError):
            ledger(inventory(), {".github/workflows/w98.yml": None})

    def test_inventory_rejects_backslash_path(self):
        bad = inventory()
        bad["workflows"][0]["path"] = ".github/workflows/a\\\\b.yml"
        with self.assertRaises(ValueError):
            ledger(bad)

    def test_unproven_inventory_is_blocked(self):
        report = ledger(inventory())
        self.assertEqual((report["total"], report["accepted"], report["blocked"]), (99, 0, 99))
    def test_partial_proof_does_not_approve(self):
        report = ledger(inventory(), {".github/workflows/w00.yml":
                       {"legacy_execution": {"sha256": "a"*64, "run_id": 1}}})
        self.assertEqual(report["accepted"], 0)
    def test_forged_complete_evidence_stays_blocked(self):
        all_proofs = {key: {"sha256": "a"*64, "run_id": 123} for key in (
            "legacy_execution", "new_execution", "input_output_comparison",
            "side_effect_comparison", "failure_timeout_comparison", "reviewer_approval")}
        report = ledger(inventory(), {".github/workflows/w00.yml": all_proofs})
        self.assertEqual(report["accepted"], 0)
        self.assertTrue(report["rows"][0]["evidence_metadata_complete"])
        self.assertEqual(report["rows"][0]["independent_verification"], "not_implemented")
    def test_bool_run_id_not_accepted_as_metadata(self):
        proofs = {key: {"sha256": "a"*64, "run_id": True} for key in (
            "legacy_execution", "new_execution", "input_output_comparison",
            "side_effect_comparison", "failure_timeout_comparison", "reviewer_approval")}
        result = ledger(inventory(), {".github/workflows/w00.yml": proofs})
        self.assertFalse(result["rows"][0]["evidence_metadata_complete"])
    def test_reject_unknown_workflow(self):
        with self.assertRaises(ValueError):
            ledger(inventory(), {"other": {}})
    def test_reject_incomplete_inventory(self):
        i = inventory()
        i["workflows"].pop()
        with self.assertRaises(ValueError):
            ledger(i)

    def test_missing_and_invalid_proofs_are_counted_without_acceptance(self):
        from madsc.legacy_parity_evidence import REQUIRED
        partial = {
            "legacy_execution": {"sha256": "a" * 64, "run_id": 12},
            "new_execution": {"sha256": "bad", "run_id": 14},
            "reviewer_approval": {"sha256": "b" * 64, "run_id": True},
        }
        report = ledger(inventory(), {".github/workflows/w00.yml": partial})
        first = report["rows"][0]
        self.assertEqual(first["missing"], [key for key in REQUIRED if key not in partial])
        self.assertEqual(first["invalid"], ["new_execution", "reviewer_approval"])
        self.assertEqual(report["invalid_evidence_fields"], 2)
        self.assertEqual(report["missing_evidence_fields"], 99 * len(REQUIRED) - len(partial))
        self.assertEqual(report["metadata_complete"], 0)
        self.assertEqual(report["accepted"], 0)

    def test_complete_metadata_is_counted_but_never_accepted(self):
        from madsc.legacy_parity_evidence import REQUIRED
        proofs = {key: {"sha256": "c" * 64, "run_id": 123} for key in REQUIRED}
        report = ledger(inventory(), {".github/workflows/w00.yml": proofs})
        self.assertEqual(report["metadata_complete"], 1)
        self.assertEqual(report["accepted"], 0)
        self.assertEqual(report["blocked"], 99)


    def test_snapshot_comparison_detects_behavioral_differences(self):
        from madsc.legacy_parity_evidence import compare_execution_snapshots
        legacy = {"exit_code": 0, "timed_out": False,
                  "outputs": {"report": "a" * 64}, "side_effects": {}}
        replacement = {"exit_code": 1, "timed_out": True,
                       "outputs": {"report": "b" * 64}, "side_effects": {"write": "c" * 64}}
        result = compare_execution_snapshots(legacy, replacement)
        self.assertFalse(result["snapshot_fields_match"])
        self.assertEqual(set(result["differences"]),
                         {"exit_code", "timed_out", "outputs", "side_effects"})
        self.assertFalse(result["behavioral_parity_accepted"])

    def test_matching_snapshots_never_imply_acceptance(self):
        from madsc.legacy_parity_evidence import compare_execution_snapshots
        snapshot = {"exit_code": 0, "timed_out": False,
                    "outputs": {"report": "a" * 64}, "side_effects": {}}
        result = compare_execution_snapshots(snapshot, dict(snapshot))
        self.assertTrue(result["snapshot_fields_match"])
        self.assertFalse(result["provenance_verified"])
        self.assertFalse(result["behavioral_parity_accepted"])

    def test_snapshot_rejects_untrusted_shapes(self):
        from madsc.legacy_parity_evidence import compare_execution_snapshots
        good = {"exit_code": 0, "timed_out": False, "outputs": {}, "side_effects": {}}
        for invalid in (
            {**good, "exit_code": True},
            {**good, "timed_out": 0},
            {**good, "outputs": {"report": "not-a-digest"}},
            {**good, "side_effects": {"write": 123}},
            {**good, "unexpected": True},
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                compare_execution_snapshots(good, invalid)


    def test_batch_reports_missing_matching_and_mismatching_pairs(self):
        from madsc.legacy_parity_evidence import compare_snapshot_batch
        good = {"exit_code": 0, "timed_out": False, "outputs": {}, "side_effects": {}}
        bad = {**good, "exit_code": 1}
        report = compare_snapshot_batch(inventory(), {
            ".github/workflows/w00.yml": {"legacy": good, "replacement": dict(good)},
            ".github/workflows/w01.yml": {"legacy": good, "replacement": bad},
        })
        self.assertEqual((report["total"], report["pairs_supplied"],
                          report["snapshot_matches"], report["snapshot_mismatches"],
                          report["missing_pairs"], report["behavioral_parity_accepted"]),
                         (99, 2, 1, 1, 97, 0))

    def test_batch_validates_late_malformed_snapshot(self):
        from madsc.legacy_parity_evidence import compare_snapshot_batch
        good = {"exit_code": 0, "timed_out": False, "outputs": {}, "side_effects": {}}
        with self.assertRaises(ValueError):
            compare_snapshot_batch(inventory(), {
                ".github/workflows/w00.yml": {"legacy": good, "replacement": good},
                ".github/workflows/w98.yml": {"legacy": good, "replacement": {"exit_code": True}},
            })

    def test_batch_rejects_unknown_or_incomplete_pairs(self):
        from madsc.legacy_parity_evidence import compare_snapshot_batch
        for payload in ({"unknown": {}}, {".github/workflows/w00.yml": {"legacy": {}}}):
            with self.assertRaises(ValueError):
                compare_snapshot_batch(inventory(), payload)

if __name__ == "__main__":
    unittest.main()


class LegacyScopeTests(unittest.TestCase):
    @staticmethod
    def provenance_pair(path, blob):
        snapshot = {"exit_code": 0, "timed_out": False,
                    "outputs": {"report": "d" * 64}, "side_effects": {}}
        def origin(repository, branch, workflow, workflow_blob, run_id, artifact_id):
            return {
                "repository": repository, "branch": branch,
                "workflow_path": workflow, "workflow_blob_sha": workflow_blob,
                "run_id": run_id, "run_attempt": 1, "head_sha": "a" * 40,
                "event": "workflow_dispatch", "conclusion": "success",
                "artifact": {"id": artifact_id, "name": "comparison-evidence",
                             "repository": repository, "run_id": run_id,
                             "head_sha": "a" * 40, "sha256": "b" * 64},
                "input_sha256": "c" * 64, "snapshot": snapshot,
            }
        return {
            "legacy": origin("Madsc55/madsc-tv", "madsc/bes-sistem-toplu-birlestirme",
                             path, blob, 101, 201),
            "replacement": origin("Madsc55/Madsc55-Tv", "main",
                                  ".github/workflows/madsc-05-genel-bakim.yml",
                                  "e" * 40, 102, 202),
        }

    def test_provenance_bound_batch_uses_pinned_92_and_never_accepts_fixture(self):
        import json
        from pathlib import Path
        from madsc.legacy_parity_evidence import (compare_provenance_bound_batch,
                                                  reconcile_legacy_scope)
        source = json.loads((Path(__file__).resolve().parents[1] /
                             "docs/LEGACY_SOURCE_SCOPE.json").read_text())
        path = reconcile_legacy_scope(source)["legacy_paths"][0]
        blob = next(row["git_blob_sha"] for row in source["workflows"] if row["path"] == path)
        report = compare_provenance_bound_batch(
            source, {path: self.provenance_pair(path, blob)})
        self.assertEqual((report["total"], report["pairs_supplied"],
                          report["origin_bindings_complete"], report["snapshot_matches"],
                          report["missing_pairs"], report["behavioral_parity_accepted"]),
                         (92, 1, 1, 1, 91, 0))
        self.assertEqual(report["independent_origins_api_verified"], 0)

    def test_provenance_pair_rejects_input_and_artifact_origin_mismatch(self):
        import json
        from pathlib import Path
        from madsc.legacy_parity_evidence import compare_provenance_bound_batch, reconcile_legacy_scope
        source = json.loads((Path(__file__).resolve().parents[1] /
                             "docs/LEGACY_SOURCE_SCOPE.json").read_text())
        path = reconcile_legacy_scope(source)["legacy_paths"][0]
        blob = next(row["git_blob_sha"] for row in source["workflows"] if row["path"] == path)
        pair = self.provenance_pair(path, blob)
        pair["replacement"]["input_sha256"] = "f" * 64
        with self.assertRaises(ValueError):
            compare_provenance_bound_batch(source, {path: pair})
        pair = self.provenance_pair(path, blob)
        pair["replacement"]["artifact"]["run_id"] = 999
        with self.assertRaises(ValueError):
            compare_provenance_bound_batch(source, {path: pair})

    def test_pinned_source_scope_is_92_plus_seven(self):
        import json
        from pathlib import Path
        from madsc.legacy_parity_evidence import reconcile_legacy_scope
        inventory = json.loads((Path(__file__).resolve().parents[1] /
                                "docs/LEGACY_SOURCE_SCOPE.json").read_text())
        result = reconcile_legacy_scope(inventory)
        self.assertEqual(len(result["legacy_paths"]), 92)
        self.assertEqual(len(result["excluded_from_92"]), 7)
        self.assertEqual(result["behavioral_parity_accepted"], 0)
        self.assertFalse(result["production_ready"])
        inventory["workflows"][0]["path"] = ".github/workflows/madsc-01-unreviewed.yml"
        with self.assertRaises(ValueError):
            reconcile_legacy_scope(inventory)

    def test_missing_exclusion_does_not_silently_change_92_scope(self):
        import json
        from pathlib import Path
        from madsc.legacy_parity_evidence import reconcile_legacy_scope
        inventory = json.loads((Path(__file__).resolve().parents[1] /
                                "docs/LEGACY_SOURCE_SCOPE.json").read_text())
        for row in inventory["workflows"]:
            if row["path"].endswith("k1-protected-write-tests.yml"):
                row["path"] = ".github/workflows/unknown.yml"
        with self.assertRaises(ValueError):
            reconcile_legacy_scope(inventory)
