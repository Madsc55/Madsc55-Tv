"""Prevent a fixture-only K4 drill from being mistaken for production backup."""
from pathlib import Path
import unittest


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/madsc-04-yedek.yml"


class K4WorkflowSafetyContractTests(unittest.TestCase):
    def test_fixture_workflow_has_no_automatic_or_production_trigger(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", source)
        self.assertNotIn("  schedule:", source)
        self.assertNotIn("  push:", source)
        self.assertNotIn("  pull_request:", source)
        self.assertNotIn("  workflow_call:", source)
        self.assertIn("K4_EXTERNAL_BACKUP_ENABLED: 'false'", source)
        self.assertIn("K4_PRODUCTION_RESTORE_ENABLED: 'false'", source)
        self.assertIn("Confirm K4 is an isolated fixture-only workflow", source)

    def test_opt_in_parity_does_not_require_missing_restore_drill_artifact(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("      - name: Upload K4 restore drill evidence\n        if: ${{ inputs.allow_parity_evidence != true }}\n        uses: actions/upload-artifact@v4", source)
        self.assertIn("      - name: Upload K4 parity manifest (explicit opt-in only)", source)

    def test_fixture_workflow_cannot_gain_write_capability_or_external_upload(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        # Fixture evidence may be uploaded to Actions, but no external provider
        # credentials or cloud-storage copy steps belong in this workflow.
        self.assertIn("persist-credentials: false", source)
        self.assertIn("cancel-in-progress: false", source)
        self.assertIn("timeout-minutes: 10", source)
        self.assertNotIn("secrets.", source)
        self.assertNotIn("aws-actions/configure-aws-credentials", source)
        self.assertNotIn("google-github-actions/auth", source)
        self.assertNotIn("azure/login", source)
        self.assertNotIn("actions/checkout@v4\n        with:\n          persist-credentials: true", source)

    def test_fixture_workflow_does_not_claim_external_acceptance(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("madsc.restore_drill", source)
        self.assertIn("reports/k4-source/nested/sample.txt", source)
        self.assertIn("permissions:\n  contents: read", source)
        self.assertNotIn("contents: write", source)
        self.assertNotIn("id-token: write", source)


if __name__ == "__main__":
    unittest.main()
