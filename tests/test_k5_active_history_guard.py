"""K5 retry assessment must not skip older active workflow runs."""
import unittest
from madsc.maintenance import assess_failure_history


class K5ActiveHistoryGuardTests(unittest.TestCase):
    def test_prior_active_run_blocks_retry_assessment(self):
        current = {
            "id": 10, "head_branch": "main", "status": "completed",
            "conclusion": "failure", "created_at": "2026-10-22T21:10:00Z",
        }
        for status in ("queued", "in_progress", "waiting", "pending", "requested"):
            with self.subTest(status=status):
                prior = {
                    "id": 9, "head_branch": "main", "status": status,
                    "conclusion": None, "created_at": "2026-10-22T21:09:00Z",
                }
                with self.assertRaisesRegex(ValueError, "Incomplete prior run"):
                    assess_failure_history(
                        [{"total_count": 2, "workflow_runs": [current, prior]}],
                        current_run_id=10, branch="main",
                    )

    def test_active_run_on_other_branch_does_not_block(self):
        current = {
            "id": 10, "head_branch": "main", "status": "completed",
            "conclusion": "failure", "created_at": "2026-10-22T21:10:00Z",
        }
        unrelated = {
            "id": 9, "head_branch": "dev", "status": "queued",
            "conclusion": None, "created_at": "2026-10-22T21:09:00Z",
        }
        result = assess_failure_history(
            [{"total_count": 2, "workflow_runs": [current, unrelated]}],
            current_run_id=10, branch="main",
        )
        self.assertFalse(result["blocked"])


if __name__ == "__main__":
    unittest.main()
