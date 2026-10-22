"""K5 history timestamps require explicit RFC3339-style date/time boundaries."""
import unittest
from madsc.maintenance import assess_failure_history


class TimestampShapeTests(unittest.TestCase):
    def check(self, stamp):
        run = {"id": 7, "head_branch": "main", "status": "completed",
               "conclusion": "success", "created_at": stamp}
        return assess_failure_history(
            [{"total_count": 1, "workflow_runs": [run]}],
            current_run_id=7, branch="main")

    def test_noncanonical_shapes_rejected(self):
        for stamp in ("2026-10-22 20:30:00+00:00",
                      "2026-10-22", "2026-10-22T20:30:00",
                      "2026-10-22t20:30:00z"):
            with self.subTest(stamp=stamp):
                with self.assertRaisesRegex(ValueError, "timestamp"):
                    self.check(stamp)

    def test_standard_utc_timestamp_accepted(self):
        self.assertFalse(self.check("2026-10-22T20:30:00Z")["blocked"])


if __name__ == "__main__":
    unittest.main()
