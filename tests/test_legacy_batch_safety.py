"""Read-only legacy batch input boundaries, without network calls."""
import unittest
from datetime import datetime, timezone
from madsc.legacy_history_merge import merge_pair
from madsc.legacy_history_provenance import select_ancestor_run, verify_artifact_provenance
from madsc.legacy_retest_390 import parse_entries, evaluate_entries
from madsc.legacy_category_order import route_discovered_candidates


class LegacyBatchSafetyTests(unittest.TestCase):
    def test_history_bundle_requires_both_valid_documents(self):
        with self.assertRaises(ValueError):
            merge_pair({}, {})
        with self.assertRaises(ValueError):
            merge_pair(None, {})

    def test_source_run_and_artifact_validation(self):
        with self.assertRaises(ValueError):
            select_ancestor_run([None], repo="r", branch="b", current_run=1,
                                ancestor_check=lambda _: True, workflows=[])
        with self.assertRaises(ValueError):
            verify_artifact_provenance({}, [None], "bundle")

    def test_legacy_probe_limits_precede_execution(self):
        with self.assertRaises(ValueError):
            parse_entries(None)
        with self.assertRaises(ValueError):
            evaluate_entries([("meta", "https://example.org")] * 20001,
                             runner=lambda *_: self.fail("Unexpected probe"))

    def test_isolated_queue_limits(self):
        with self.assertRaises(ValueError):
            route_discovered_candidates([{"name": "Example"}] * 20001)
        report = route_discovered_candidates([{"name": "Example"}])
        self.assertFalse(report["production_writes"])
        self.assertTrue(report["queued"][0]["requires_user_ibo_decision"])
