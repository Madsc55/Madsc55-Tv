"""Reject inconsistent GitHub Actions status/conclusion evidence."""
import unittest
from madsc.maintenance import assess_failure_history


def entry(identifier, status, conclusion, minute):
    return {"id": identifier, "head_branch": "main",
            "status": status, "conclusion": conclusion,
            "created_at": f"2026-10-22T20:{minute:02d}:00Z"}


class HistoryStatusConsistencyTests(unittest.TestCase):
    def assess(self, rows):
        return assess_failure_history(
            [{"total_count": len(rows), "workflow_runs": rows}],
            current_run_id=3, branch="main")

    def test_active_runs_cannot_have_premature_conclusion(self):
        for status in ("in_progress", "queued", "requested", "waiting", "pending"):
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, "premature conclusion"):
                    self.assess([entry(3, status, "success", 53)])

    def test_completed_runs_require_known_conclusion(self):
        for conclusion in (None, "", "unknown", True):
            with self.subTest(conclusion=conclusion):
                with self.assertRaisesRegex(ValueError, "invalid conclusion"):
                    self.assess([entry(3, "completed", conclusion, 53)])

    def test_valid_current_active_and_previous_success(self):
        result = self.assess([
            entry(3, "in_progress", None, 53),
            entry(2, "completed", "success", 52),
        ])
        self.assertFalse(result["blocked"])


if __name__ == "__main__":
    unittest.main()
