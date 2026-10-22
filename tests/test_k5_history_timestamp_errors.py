"""K5 rejects invalid and timezone-naive workflow timestamps."""
import unittest
from madsc.maintenance import assess_failure_history


class HistoryTimestampErrorTests(unittest.TestCase):
    def test_invalid_timestamp_fails_closed(self):
        for stamp in ("not-a-date", "2026-99-22T21:00:00Z",
                      "2026-10-22T21:00:00", ""):
            with self.subTest(stamp=stamp):
                run = {"id": 1, "head_branch": "main", "status": "completed",
                       "conclusion": "success", "created_at": stamp}
                with self.assertRaisesRegex(ValueError, "history timestamp"):
                    assess_failure_history(
                        [{"total_count": 1, "workflow_runs": [run]}],
                        current_run_id=1, branch="main")


if __name__ == "__main__":
    unittest.main()
