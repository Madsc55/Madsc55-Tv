"""Static guard for the manual-only, read-only online pilot workflow."""
from pathlib import Path
import unittest


class OnlinePilotWorkflowTests(unittest.TestCase):
    def test_online_pilots_are_manual_and_gated_by_offline_suite(self):
        text = (Path(__file__).resolve().parents[1] /
                ".github/workflows/madsc-online-pilot-gates.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("  push:", text)
        self.assertNotIn("  schedule:", text)
        self.assertIn("contents: read", text)
        self.assertIn("needs: offline-regression", text)
        self.assertIn("python -m madsc.offline_gate", text)
        self.assertIn("python -m madsc.live_discovery_pilot", text)
        self.assertIn("python -m madsc.k3_live_manifest_pilot", text)
        self.assertNotIn("contents: write", text)


if __name__ == "__main__":
    unittest.main()
