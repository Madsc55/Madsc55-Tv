"""Additional offline regression checks for K4 schedule determinism and safety."""
import datetime as dt
import unittest
from unittest.mock import patch

from madsc.k4_schedule_plan import planned_slots


class K4AnnualScheduleRegression(unittest.TestCase):
    def test_every_month_is_exactly_first_and_fifteenth(self):
        for year in (2000, 2026, 2100):
            for month in range(1, 13):
                with self.subTest(year=year, month=month):
                    slots = planned_slots(year, month)
                    self.assertEqual(len(slots), 2)
                    self.assertEqual(
                        [dt.date.fromisoformat(s["local"][:10]).day for s in slots],
                        [1, 15],
                    )
                    self.assertEqual(len({s["idempotency_key"] for s in slots}), 2)
                    for slot in slots:
                        self.assertEqual(slot["mode"], "dry_run_only")
                        local = dt.datetime.fromisoformat(slot["local"])
                        utc = dt.datetime.fromisoformat(slot["utc"].replace("Z", "+00:00"))
                        self.assertEqual(local.astimezone(dt.timezone.utc), utc)

    def test_default_slot_is_not_affected_by_process_timezone(self):
        baseline = planned_slots(2026, 10)
        with patch.dict("os.environ", {"TZ": "Pacific/Honolulu"}):
            self.assertEqual(planned_slots(2026, 10), baseline)

    def test_idempotency_keys_are_stable_across_calls(self):
        first = planned_slots(2026, 10)
        second = planned_slots(2026, 10)
        self.assertEqual([s["idempotency_key"] for s in first],
                         [s["idempotency_key"] for s in second])


if __name__ == "__main__":
    unittest.main()
