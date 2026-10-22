"""Five-stage inventory is derived from real repository contracts, not guesses."""
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.five_stage_installation import assess_installation


ROOT = Path(__file__).resolve().parent.parent


class InstallationInventoryTests(unittest.TestCase):
    def test_complete_static_inventory_never_claims_production(self):
        report = assess_installation(ROOT)
        self.assertEqual(set(report["stages"]), {"K1", "K2", "K3", "K4", "K5"})
        self.assertEqual(report["main_workflows_installed"], 5)
        self.assertEqual(report["legacy_behavior_workflows"], 92)
        self.assertEqual(report["task_count"], 22)
        self.assertIsNone(report["current_project_progress_verified_percent"])
        self.assertFalse(report["production_ready"])
        self.assertFalse(report["github_actions_triggered"])
        self.assertFalse(report["production_writes"])
        for row in report["stages"].values():
            self.assertFalse(row["runtime_verified"])
            self.assertFalse(row["production_accepted"])

    def test_k1_writer_inventory_includes_os_open_descriptor_writes(self):
        from madsc.five_system_installation import inspect_installation
        report = inspect_installation(ROOT)
        descriptor_writes = [row for row in report["writer_callsite_candidates"]
                             if row["operation"] == "open"
                             and row["classification"] == "write"
                             and row["file"] == "madsc/k4_evidence.py"]
        self.assertTrue(descriptor_writes, "os.open(O_CREAT) writer missing from K1 inventory")
        descriptor_stream_writes = [row for row in report["writer_callsite_candidates"]
                                    if row["operation"] == "fdopen"
                                    and row["classification"] == "write"
                                    and row["file"] == "madsc/k4_evidence.py"]
        self.assertTrue(descriptor_stream_writes,
                        "os.fdopen(..., 'w') writer missing from K1 inventory")
        self.assertFalse(report["all_writer_callsites_manually_verified"])
        self.assertFalse(report["production_ready"])

    def test_missing_workflow_fails_closed(self):
        from madsc.five_stage_installation import consolidation_plan
        with patch("madsc.five_stage_installation.consolidation_plan",
                   return_value={"main_workflows": {}, "auxiliary_count": 10}):
            with self.assertRaises((ValueError, KeyError)):
                assess_installation(ROOT)
