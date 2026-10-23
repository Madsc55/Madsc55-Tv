import unittest
from madsc.offline_five_gate import assess_all


class OfflineFiveGateTests(unittest.TestCase):
    def test_five_fixture_checks_pass_without_production_approval(self):
        result = assess_all(lambda category: {"isolated": True})
        self.assertTrue(result["fixture_gate_passed"])
        self.assertEqual(result["categories_checked"], 5)
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["production_writes"])

    def test_failed_check_blocks_batch(self):
        result = assess_all(lambda category: {"isolated": category != "k3"})
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(result["categories"]["k3"], "failure")

    def test_exception_blocks_batch(self):
        def executor(category):
            if category == "k2":
                raise RuntimeError("failure")
            return {"isolated": True}
        result = assess_all(executor)
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(result["categories_checked"], 5)
        self.assertEqual(result["errors"]["k2"], "RuntimeError")

    def test_truthy_nonboolean_is_rejected(self):
        result = assess_all(lambda category: {"isolated": 1})
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(len(result["errors"]), 5)

    def test_one_stage_failure_does_not_skip_other_stages(self):
        visited = []
        def executor(category):
            visited.append(category)
            if category == "k2":
                raise RuntimeError("failed")
            return {"isolated": True}
        result = assess_all(executor)
        self.assertEqual(visited, ["k1", "k2", "k3", "k4", "k5"])
        self.assertFalse(result["fixture_gate_passed"])

    def test_real_k1_to_k5_fixture_integration(self):
        # Unlike mocked decision tests, exercise the actual five stage executors.
        result = assess_all()
        self.assertEqual(result["categories_checked"], 5)
        self.assertEqual(set(result["categories"]), {"k1", "k2", "k3", "k4", "k5"})
        self.assertTrue(result["fixture_gate_passed"], result["errors"])
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["production_writes"])
        self.assertEqual(result["legacy_92_behavioral_acceptance"], 0)
        self.assertEqual(result["runtime_security_26_acceptance"], 0)

    def test_real_k5_joins_candidate_and_independent_restore(self):
        from madsc.core import execute
        checks = execute("k5")
        self.assertIs(checks["k2_k3_k4_k5_candidate_restore_review"], True)
        self.assertIs(checks["k4_corruption_blocks_k5_review"], True)
        self.assertIs(checks["k1_guards_k5_report_write"], True)

    def test_real_k5_archive_preview_is_checked_by_gate(self):
        from madsc.core import execute
        checks = execute("k5")
        self.assertIs(checks["archive_classification_preview_read_only"], True)

    def test_k5_archive_preview_failure_blocks_five_stage_gate(self):
        from unittest.mock import patch
        with patch("madsc.core.classify_archive_positions", side_effect=ValueError("bad fixture")):
            result = assess_all()
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(result["categories"]["k5"], "failure")
        self.assertEqual(result["errors"]["k5"], "ValueError")
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["production_writes"])

    def test_wrong_archive_positions_with_correct_counts_fail_gate(self):
        from dataclasses import replace
        from unittest.mock import patch
        from madsc.k5_archive_preview import classify_archive_positions

        original = classify_archive_positions
        def swapped_positions(scenario, entries):
            result = original(scenario, entries)
            if scenario != "354":
                return result
            return replace(result,
                           kept_positions=(1, 3),
                           archived_positions=(2,) + tuple(range(4, 355)))
        with patch("madsc.core.classify_archive_positions", side_effect=swapped_positions):
            report = assess_all()
        self.assertFalse(report["fixture_gate_passed"])
        self.assertEqual(report["categories"]["k5"], "failure")
        self.assertFalse(report["production_ready"])

    def test_wrong_364_classification_metadata_fails_gate(self):
        from dataclasses import replace
        from unittest.mock import patch
        from madsc.k5_archive_preview import classify_archive_positions

        original = classify_archive_positions
        def bad_metadata(scenario, entries):
            result = original(scenario, entries)
            if scenario == "364":
                return replace(result, user_classified_foreign_positions=())
            return result
        with patch("madsc.core.classify_archive_positions", side_effect=bad_metadata):
            report = assess_all()
        self.assertFalse(report["fixture_gate_passed"])
        self.assertEqual(report["categories"]["k5"], "failure")
        self.assertFalse(report["production_ready"])

    def test_all_archive_scenarios_reject_swapped_positions(self):
        from dataclasses import replace
        from unittest.mock import patch
        from madsc.k5_archive_preview import classify_archive_positions

        original = classify_archive_positions
        for target in ("354", "364", "398"):
            with self.subTest(scenario=target):
                def wrong_partition(scenario, entries):
                    preview = original(scenario, entries)
                    if scenario != target:
                        return preview
                    kept = list(preview.kept_positions)
                    archived = list(preview.archived_positions)
                    kept[-1], archived[0] = archived[0], kept[-1]
                    return replace(preview, kept_positions=tuple(kept),
                                   archived_positions=tuple(archived))
                with patch("madsc.core.classify_archive_positions", side_effect=wrong_partition):
                    report = assess_all()
                self.assertFalse(report["fixture_gate_passed"])
                self.assertEqual(report["categories"]["k5"], "failure")
                self.assertFalse(report["production_ready"])

    def test_all_archive_scenarios_reject_wrong_metadata(self):
        from dataclasses import replace
        from unittest.mock import patch
        from madsc.k5_archive_preview import classify_archive_positions

        original = classify_archive_positions
        for target in ("354", "364", "398"):
            with self.subTest(scenario=target):
                def wrong_metadata(scenario, entries):
                    preview = original(scenario, entries)
                    if scenario == target:
                        return replace(preview, user_classified_foreign_positions=())
                    return preview
                with patch("madsc.core.classify_archive_positions", side_effect=wrong_metadata):
                    report = assess_all()
                self.assertFalse(report["fixture_gate_passed"])
                self.assertEqual(report["categories"]["k5"], "failure")
                self.assertFalse(report["production_writes"])

    def test_stage_inventory_is_exact_five(self):
        from unittest.mock import patch
        with patch("madsc.offline_five_gate.CATEGORIES", ("k1", "k2", "k3", "k4", "k4")):
            result = assess_all(lambda category: {"isolated": True})
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(result["errors"]["inventory"], "invalid_five_stage_inventory")

    def test_missing_checks_block_batch(self):
        result = assess_all(lambda category: {})
        self.assertFalse(result["fixture_gate_passed"])


if __name__ == "__main__":
    unittest.main()
