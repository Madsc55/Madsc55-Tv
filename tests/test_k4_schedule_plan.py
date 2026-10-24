import datetime as dt
import unittest

from madsc.k4_schedule_plan import planned_slots


class K4SchedulePlanTests(unittest.TestCase):
    def test_first_and_fifteenth_only(self):
        slots = planned_slots(2026, 10)
        self.assertEqual(len(slots), 2)
        self.assertEqual([s["local"][:10] for s in slots], ["2026-10-01", "2026-10-15"])
        self.assertTrue(all(s["mode"] == "dry_run_only" for s in slots))
        self.assertEqual(len({s["idempotency_key"] for s in slots}), 2)
        self.assertEqual(slots, planned_slots(2026, 10))

    def test_dst_offsets_and_utc_roundtrip(self):
        winter = planned_slots(2026, 1)
        summer = planned_slots(2026, 7)
        self.assertTrue(all(s["local"].endswith("+01:00") for s in winter))
        self.assertTrue(all(s["local"].endswith("+02:00") for s in summer))
        for slot in winter + summer:
            local = dt.datetime.fromisoformat(slot["local"])
            utc = dt.datetime.fromisoformat(slot["utc"].replace("Z", "+00:00"))
            self.assertEqual(local.astimezone(dt.timezone.utc), utc)

    def test_leap_year_and_month_boundaries(self):
        for year, month in [(2024, 2), (2025, 2), (2026, 12), (2027, 1)]:
            self.assertEqual(len(planned_slots(year, month)), 2)

    def test_invalid_input_fails_closed(self):
        for year, month, hour in [(2026, 0, 3), (2026, 13, 3), (1999, 1, 3),
                                  (2101, 1, 3), (2026, 1, 24), (True, 1, 3),
                                  (2026, True, 3), (2026, 1, True)]:
            with self.subTest(year=year, month=month, hour=hour):
                with self.assertRaises(ValueError):
                    planned_slots(year, month, hour)


if __name__ == "__main__":
    unittest.main()
