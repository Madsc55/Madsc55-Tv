"""Validate literal RFC3339 history timestamps, not permissive ISO variants."""
import unittest
from madsc.maintenance import assess_failure_history


class StrictTimestampTests(unittest.TestCase):
    def evaluate(self, stamp):
        run = {"id": 19, "head_branch": "main", "status": "completed",
               "conclusion": "success", "created_at": stamp}
        return assess_failure_history(
            [{"total_count": 1, "workflow_runs": [run]}],
            current_run_id=19, branch="main")

    def test_noncanonical_shapes_rejected(self):
        invalid = (
            "20261022T20:30:00Z", "2026-10-22T203000Z",
            "2026-10-22 20:30:00Z", "2026-10-22T20:30Z",
            "2026-10-22T20:30:00+0000", "2026-10-22T20:30:00+00",
            "2026-10-22T20:30:00.Z", "2026-10-22T20:30:00.1234567Z",
            "2026-10-22T20:30:00z", "2026-10-22T20:30:00Zjunk",
        )
        for stamp in invalid:
            with self.subTest(stamp=stamp):
                with self.assertRaisesRegex(ValueError, "timestamp"):
                    self.evaluate(stamp)

    def test_valid_utc_and_offset_shapes(self):
        for stamp in ("2026-10-22T20:30:00Z",
                      "2026-10-22T20:30:00.123456Z",
                      "2026-10-22T20:30:00+02:00",
                      "2026-10-22T20:30:00.1-03:30"):
            with self.subTest(stamp=stamp):
                self.assertFalse(self.evaluate(stamp)["blocked"])


if __name__ == "__main__":
    unittest.main()
