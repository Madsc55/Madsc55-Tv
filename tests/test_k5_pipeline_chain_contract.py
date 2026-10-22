"""K5 regression: manual five-stage workflow must preserve fail-closed ordering.

Static contract only; this does not certify Actions execution or legacy parity.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/madsc-05-bakim.yml"


class K5PipelineChainContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_manual_only_and_read_permissions(self):
        header = self.source.split("\njobs:", 1)[0]
        self.assertRegex(header, r"(?m)^  workflow_dispatch:\s*$")
        self.assertNotRegex(header, r"(?m)^  (schedule|push|pull_request|workflow_run):")
        self.assertRegex(header, r"(?m)^  contents: read\s*$")
        self.assertRegex(header, r"(?m)^  actions: read\s*$")
        self.assertNotRegex(header, r"(?m)^\s+(contents|actions): write\s*$")

    def test_sequential_jobs_fail_closed(self):
        source = self.source
        for stage, prerequisite in (("k2", "k1"), ("k3", "k2"),
                                    ("k4", "k3"), ("k5", "k4")):
            pattern = (r"(?ms)^  " + stage + r":\s*\n"
                       r"    if: \$\{\{ needs\." + prerequisite +
                       r"\.result == 'success' \}\}\s*\n"
                       r".*?^    needs: " + prerequisite + r"\s*$")
            self.assertRegex(source, pattern)

    def test_aggregate_gate_rejects_failed_or_skipped_evidence(self):
        aggregate = self.source.split("\n  toplu-kabul:\n", 1)[1]
        self.assertIn("if: ${{ always() && !cancelled() }}", aggregate)
        for step_id in ("history-chain", "k2-handoff", "cross-handoff",
                        "k4-restore", "kabul"):
            self.assertRegex(aggregate, r"(?m)^        id: " + step_id + r"\s*$")
            self.assertIn("steps." + step_id + ".outcome", aggregate)
        for status in ("K1", "K2", "K3", "K4", "K5",
                       "KABUL", "K2_HANDOFF", "CROSS_HANDOFF",
                       "HISTORY_CHAIN", "K4_RESTORE"):
            self.assertIn(status, aggregate)
        self.assertIn('if [ "$durum" != success ]; then hata=1; fi', aggregate)
        self.assertIn('exit "$hata"', aggregate)

    def test_k5_cross_stage_evidence_is_required(self):
        k5 = self.source.split("\n  k5:\n", 1)[1]
        for command in ("madsc.handoff_acceptance", "madsc.k5_channel_gate",
                        "madsc.batch_acceptance"):
            self.assertIn(command, k5)
        self.assertIn("madsc-k3-guarded-evidence", k5)
        self.assertIn("madsc-k2-candidate-handoff", k5)


if __name__ == "__main__":
    unittest.main()
