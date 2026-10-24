import datetime as dt
import io
import json
from contextlib import redirect_stdout
from unittest.mock import patch
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

    def test_daylight_saving_transition_months(self):
        march = planned_slots(2026, 3)
        october = planned_slots(2026, 10)
        self.assertTrue(all(slot["local"].endswith("+01:00") for slot in march))
        self.assertTrue(all(slot["local"].endswith("+02:00") for slot in october))
        self.assertTrue(all(slot["mode"] == "dry_run_only" for slot in march + october))

    def test_transition_day_ambiguous_hour_rejected(self):
        # The planner must reject ambiguous local times if a future schedule
        # ever lands on a Stockholm DST fallback date.
        from unittest.mock import patch
        import madsc.k4_schedule_plan as planner
        with patch.object(planner, "DAYS", (25,)):
            with self.assertRaises(ValueError):
                planner.planned_slots(2026, 10, 2)

    def test_transition_day_nonexistent_hour_rejected(self):
        from unittest.mock import patch
        import madsc.k4_schedule_plan as planner
        with patch.object(planner, "DAYS", (29,)):
            with self.assertRaises(ValueError):
                planner.planned_slots(2026, 3, 2)

    def test_cli_reports_dry_run_without_enabling_scheduler(self):
        from madsc.k4_schedule_plan import main
        buffer = io.StringIO()
        with patch("sys.argv", ["k4_schedule_plan", "--year", "2026", "--month", "10"]):
            with redirect_stdout(buffer):
                main()
        report = json.loads(buffer.getvalue())
        self.assertIs(report["production_writes"], False)
        self.assertIs(report["scheduler_enabled"], False)
        self.assertEqual(len(report["slots"]), 2)
        self.assertTrue(all(s["mode"] == "dry_run_only" for s in report["slots"]))

    def test_cli_invalid_month_does_not_emit_success_json(self):
        from madsc.k4_schedule_plan import main
        buffer = io.StringIO()
        with patch("sys.argv", ["k4_schedule_plan", "--year", "2026", "--month", "13"]):
            with redirect_stdout(buffer):
                with self.assertRaises(ValueError):
                    main()
        self.assertEqual(buffer.getvalue(), "")

    def test_invalid_input_fails_closed(self):
        for year, month, hour in [(2026, 0, 3), (2026, 13, 3), (1999, 1, 3),
                                  (2101, 1, 3), (2026, 1, 24), (True, 1, 3),
                                  (2026, True, 3), (2026, 1, True)]:
            with self.subTest(year=year, month=month, hour=hour):
                with self.assertRaises(ValueError):
                    planned_slots(year, month, hour)


if __name__ == "__main__":
    unittest.main()
