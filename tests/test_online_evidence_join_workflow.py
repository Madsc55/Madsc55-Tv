from pathlib import Path
import unittest


class OnlineEvidenceJoinWorkflowTests(unittest.TestCase):
    def test_manual_readonly_single_job_with_join(self):
        path = Path(__file__).resolve().parents[1] / ".github/workflows/madsc-online-evidence-join.yml"
        text = path.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("  push:", text)
        self.assertNotIn("  schedule:", text)
        self.assertIn("contents: read", text)
        self.assertNotIn("contents: write", text)
        commands = ["python -m madsc.offline_gate",
                    "python -m madsc.live_discovery_pilot",
                    "python -m madsc.k3_live_manifest_pilot",
                    "python -m madsc.online_evidence_reconcile"]
        positions = [text.index(cmd) for cmd in commands]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("reports/k2-k3-joined-evidence.json", text)
        self.assertIn("Download one bounded public source snapshot", text)
        self.assertIn("data = response.read(MAX_BYTES + 1)", text)
        snapshot = "--source-file reports/k2-k3-source-snapshot.m3u"
        self.assertEqual(text.count(snapshot), 2)
        self.assertLess(text.index("Download one bounded public source snapshot"),
                        text.index("python -m madsc.live_discovery_pilot"))


if __name__ == "__main__":
    unittest.main()
