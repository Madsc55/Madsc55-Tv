"""Batch safety regression coverage for read-only legacy K2/K3/K5 adapters."""
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from madsc.legacy_candidate_merge import merge_legacy_candidate_rows
from madsc.legacy_priority_retest import priority_rows, retest_rows
from madsc.legacy_stability import evaluate_legacy_stability
from madsc.legacy_unified_report import legacy_unified_rows
from madsc.legacy_epg_logo import join_pilot


class LegacyBatchBoundsTests(unittest.TestCase):
    def test_candidate_merge_limits(self):
        with self.assertRaises(ValueError):
            merge_legacy_candidate_rows([("A", [])] * 201)
        with self.assertRaises(ValueError):
            merge_legacy_candidate_rows([("A", [{}] * 20001)])

    def test_priority_and_retest_limits(self):
        with self.assertRaises(ValueError):
            priority_rows([{}] * 20001)
        with self.assertRaises(ValueError):
            retest_rows({str(i): {} for i in range(20001)}, datetime.now(timezone.utc))

    def test_history_and_unified_limits(self):
        now = datetime.now(timezone.utc)
        with self.assertRaises(ValueError):
            evaluate_legacy_stability([{}] * 20001, now)
        with self.assertRaises(ValueError):
            legacy_unified_rows([{}] * 20001, [])
        with self.assertRaises(ValueError):
            legacy_unified_rows([], [], history={str(i): [] for i in range(20001)}, now=now)

    def test_xmltv_source_and_evidence_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pilot.xml"
            path.write_text('<tv><channel id="sample"/></tv>', encoding="utf-8")
            with self.assertRaises(ValueError):
                join_pilot([{}] * 20001, [], path)
            with self.assertRaises(ValueError):
                join_pilot([], [{}] * 20001, path)
            result = join_pilot([{"channel_id": "sample", "stream_sha256": "a" * 64}], [], path)
            self.assertEqual(result["candidate_results"][0]["epg_pilot_status"], "PILOT_ID_NO_PROGRAMMES")
            self.assertFalse(result["production_writes"])
            alias = Path(directory) / "alias.xml"
            alias.symlink_to(path)
            with self.assertRaises(ValueError):
                join_pilot([], [], alias)
