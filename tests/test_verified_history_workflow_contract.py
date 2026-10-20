"""Guardrails for the optional real-history workflow (no production writes)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VerifiedHistoryWorkflowContractTests(unittest.TestCase):
    def test_manual_only_and_independent_of_five_system_ci(self):
        verified = (ROOT / ".github/workflows/madsc-k2-verified-history.yml").read_text()
        main = (ROOT / ".github/workflows/madsc-05-bakim.yml").read_text()
        self.assertIn("workflow_dispatch:", verified)
        self.assertNotIn("\n  push:", verified)
        self.assertNotIn("\n  schedule:", verified)
        self.assertNotIn("madsc-k2-verified-history.yml", main)
        self.assertIn("contents: read", verified)
        self.assertIn("actions: read", verified)
        self.assertNotIn("contents: write", verified)
        self.assertIn("persist-credentials: false", verified)

    def test_missing_real_source_fails_closed_without_fixture(self):
        verified = (ROOT / ".github/workflows/madsc-k2-verified-history.yml").read_text()
        self.assertIn("test -f verified-history-source/manifest.json", verified)
        self.assertIn("exit 1", verified)
        self.assertIn("history_verified_workflow", verified)
        self.assertNotIn("history_transport produce", verified)
        self.assertNotIn("fixture", verified.lower())
        self.assertIn("if: ${{ success() }}", verified)
        self.assertIn("if-no-files-found: error", verified)

    def test_five_system_history_is_explicitly_fixture_not_real_source(self):
        main = (ROOT / ".github/workflows/madsc-05-bakim.yml").read_text()
        self.assertIn("K2 fixture history input", main)
        self.assertIn("history_transport produce", main)
        self.assertNotIn("history_verified_workflow", main)


if __name__ == "__main__":
    unittest.main()
