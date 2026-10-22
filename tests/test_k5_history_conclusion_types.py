"""K5 failure history conclusions must use exact string types."""
import unittest
from madsc.maintenance import assess_failure_history


class ConclusionTypeTests(unittest.TestCase):
    def test_non_string_completed_conclusions_rejected(self):
        for conclusion in (None, True, False, 0, 1, [], {}, b"success"):
            with self.subTest(conclusion=conclusion):
                current = {
                    "id": 10, "head_branch": "main",
                    "status": "completed", "conclusion": conclusion,
                    "created_at": "2026-10-22T20:10:00Z",
                }
                with self.assertRaisesRegex(ValueError, "invalid conclusion"):
                    assess_failure_history(
                        [{"total_count": 1, "workflow_runs": [current]}],
                        current_run_id=10, branch="main",
                    )


if __name__ == "__main__":
    unittest.main()
