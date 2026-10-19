"""Static checks for repository-owned GitHub Actions security defaults.

This is not a proof of runtime GitHub permissions or branch protection.
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class WorkflowSecurityTests(unittest.TestCase):
    def test_all_workflows_are_read_only_and_do_not_persist_credentials(self):
        workflows = sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))
        self.assertTrue(workflows, "No workflows discovered")
        for path in workflows:
            with self.subTest(workflow=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertRegex(content, r"(?m)^permissions:\s*\n\s+contents:\s*read\s*$")
                self.assertNotRegex(content, r"(?mi)^\s*contents:\s*write\s*$")
                self.assertNotRegex(content, r"(?mi)^\s*(?:id-token|actions|packages|pull-requests):\s*write\s*$")
                self.assertNotRegex(content, r"(?mi)^\s*persist-credentials:\s*true\s*$")
                if re.search(r"uses:\s*actions/checkout@", content):
                    self.assertRegex(content, r"(?m)^\s+persist-credentials:\s*false\s*$")

    def test_no_scheduled_or_pull_request_target_workflows(self):
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                content = path.read_text(encoding="utf-8")
                self.assertNotRegex(content, r"(?m)^\s+(?:schedule|pull_request_target|workflow_run):\s*$")
