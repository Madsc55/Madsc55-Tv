"""K5 enforces bounded failure history input."""
import unittest
from madsc.maintenance import assess_failure_history


class HistoryCapacityTests(unittest.TestCase):
    def test_more_than_ten_pages_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid failure history request"):
            assess_failure_history([{}] * 11, current_run_id=1, branch="main")

    def test_more_than_hundred_runs_per_page_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid failure history total"):
            assess_failure_history(
                [{"total_count": 101, "workflow_runs": [{}] * 101}],
                current_run_id=1, branch="main")

    def test_inconsistent_totals_rejected(self):
        pages = [
            {"total_count": 2, "workflow_runs": [
                {"id": 2, "head_branch": "main", "status": "completed",
                 "conclusion": "success", "created_at": "2026-10-22T20:02:00Z"}]},
            {"total_count": 3, "workflow_runs": []},
        ]
        with self.assertRaisesRegex(ValueError, "changed during pagination"):
            assess_failure_history(pages, current_run_id=2, branch="main")


if __name__ == "__main__":
    unittest.main()
