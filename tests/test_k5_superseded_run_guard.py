"""A stale workflow run cannot be treated as the latest retry target."""
import unittest
from madsc.maintenance import assess_failure_history


def record(identifier, branch, minute):
    return {"id": identifier, "head_branch": branch, "status": "completed",
            "conclusion": "failure",
            "created_at": f"2026-10-22T20:{minute:02d}:00Z"}


class SupersededRunGuardTests(unittest.TestCase):
    def test_newer_same_branch_run_rejected(self):
        rows = [record(12, "main", 12), record(11, "main", 11)]
        with self.assertRaisesRegex(ValueError, "supersedes"):
            assess_failure_history(
                [{"total_count": 2, "workflow_runs": rows}],
                current_run_id=11, branch="main")

    def test_newer_other_branch_does_not_supersede(self):
        rows = [record(12, "feature", 12), record(11, "main", 11)]
        result = assess_failure_history(
            [{"total_count": 2, "workflow_runs": rows}],
            current_run_id=11, branch="main")
        self.assertFalse(result["blocked"])


if __name__ == "__main__":
    unittest.main()
