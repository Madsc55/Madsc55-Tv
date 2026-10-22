"""K5 must not reset its failure halt on inconclusive workflow runs."""
import unittest
from madsc.maintenance import assess_failure_history


def run(run_id, conclusion, minute):
    return {
        "id": run_id, "head_branch": "main", "status": "completed",
        "conclusion": conclusion,
        "created_at": f"2026-10-22T21:{minute:02d}:00Z",
    }


class K5FailureHistoryIndeterminateTests(unittest.TestCase):
    def test_indeterminate_run_cannot_reset_failures(self):
        for conclusion in ("cancelled", "skipped", "neutral",
                           "action_required", "stale"):
            with self.subTest(conclusion=conclusion):
                history = [
                    run(5, "failure", 55),
                    run(4, conclusion, 54),
                    run(3, "failure", 53),
                    run(2, "failure", 52),
                ]
                with self.assertRaisesRegex(ValueError, "Indeterminate"):
                    assess_failure_history(
                        [{"total_count": 4, "workflow_runs": history}],
                        current_run_id=5, branch="main",
                    )

    def test_actual_success_is_valid_boundary(self):
        history = [run(5, "failure", 55), run(4, "success", 54)]
        result = assess_failure_history(
            [{"total_count": 2, "workflow_runs": history}],
            current_run_id=5, branch="main",
        )
        self.assertFalse(result["blocked"])
        self.assertFalse(result["runtime_history_origin_verified"])


if __name__ == "__main__":
    unittest.main()
