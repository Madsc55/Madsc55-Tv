"""Ensure the offline gate runs for code-changing pull requests as well as pushes.

This static contract does not bypass GitHub's [skip ci] behavior and does not
substitute for administrator-owned required checks or branch protection.
"""
from pathlib import Path
import re
import unittest


WORKFLOW = (Path(__file__).resolve().parents[1] /
            ".github/workflows/madsc-unit-tests.yml")


class OfflineCITriggerContractTests(unittest.TestCase):
    def test_pr_and_push_watch_same_code_paths(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        trigger_section = source.split("permissions:", 1)[0]
        expected_paths = (
            ".github/workflows/madsc-unit-tests.yml",
            "madsc/**",
            "tests/**",
            "docs/LEGACY_SOURCE_SCOPE.json",
            "docs/K1_K5_KANITLI_GOREV_DEFTERI.json",
        )
        for event in ("pull_request", "push"):
            with self.subTest(event=event):
                match = re.search(
                    rf"(?ms)^  {event}:\\n(.*?)(?=^  [a-z_]+:\\n|\\Z)",
                    trigger_section,
                )
                self.assertIsNotNone(match, f"Missing {event} trigger")
                body = match.group(1)
                self.assertIn("    paths:\\n", body)
                for path in expected_paths:
                    self.assertIn(f"      - '{path}'", body)

    def test_pr_gate_stays_read_only_and_offline(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions:\\n  contents: read", source)
        self.assertIn("persist-credentials: false", source)
        self.assertIn("python -m madsc.offline_gate", source)
        self.assertNotIn("pull_request_target:", source)
        self.assertNotIn("id-token: write", source)
        self.assertNotIn("contents: write", source)


if __name__ == "__main__":
    unittest.main()
