import unittest
from datetime import datetime, timedelta, timezone
from madsc.legacy_stability import evaluate_legacy_stability


class LegacyStabilityTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 19, 12, tzinfo=timezone.utc)

    def observation(self, hours, state="VIDEO_SES_VAR"):
        return {"at": (self.now - timedelta(hours=hours)).isoformat(), "state": state}

    def test_two_independent_good_measurements_24_hours_apart(self):
        result = evaluate_legacy_stability([self.observation(25), self.observation(1)], self.now)
        self.assertEqual(result["24_SAAT_KARARLI"], "EVET")
        self.assertEqual(result["BASARILI_ARALIK_SAAT"], 24)
        self.assertFalse(result["network_probed"])

    def test_repeated_measurement_does_not_fake_stability(self):
        observation = self.observation(25)
        result = evaluate_legacy_stability([observation, observation], self.now)
        self.assertEqual(result["GOZLEM_SAYISI"], 1)
        self.assertEqual(result["24_SAAT_KARARLI"], "HAYIR")

    def test_failure_stale_and_short_span_not_stable(self):
        cases = [
            [self.observation(25), self.observation(1), self.observation(2, "VIDEO_YOK")],
            [self.observation(50), self.observation(25)],
            [self.observation(10), self.observation(1)],
        ]
        for observations in cases:
            with self.subTest(observations=observations):
                self.assertEqual(evaluate_legacy_stability(observations, self.now)["24_SAAT_KARARLI"], "HAYIR")

    def test_conflicting_or_future_or_naive_measurements_rejected(self):
        bad = [
            [self.observation(1), self.observation(1, "VIDEO_YOK")],
            [{"at": "2026-10-19T11:00:00", "state": "VIDEO_SES_VAR"}],
            [{"at": (self.now + timedelta(minutes=6)).isoformat(), "state": "VIDEO_SES_VAR"}],
        ]
        for observations in bad:
            with self.subTest(observations=observations), self.assertRaises(ValueError):
                evaluate_legacy_stability(observations, self.now)

    def test_untested_state_cannot_be_recorded_as_measurement(self):
        with self.assertRaises(ValueError):
            evaluate_legacy_stability([self.observation(1, "TEST_EDILMEDI")], self.now)


    def test_24_hour_boundary_requires_fresh_independent_measurement(self):
        cases = [
            ([self.observation(48), self.observation(24)], "EVET"),
            ([self.observation(48), self.observation(24 + 1 / 3600)], "HAYIR"),
            ([self.observation(24), self.observation(0)], "EVET"),
            ([self.observation(23.999), self.observation(0)], "HAYIR"),
        ]
        for observations, expected in cases:
            with self.subTest(observations=observations):
                report = evaluate_legacy_stability(observations, self.now)
                self.assertEqual(report["24_SAAT_KARARLI"], expected)
                self.assertFalse(report["production_writes"])

    def test_old_history_and_timezone_aliases_cannot_inflate_observation_count(self):
        old = self.observation(24 * 8)
        same_in_utc = self.observation(25)
        same_in_plus_two = {
            "at": (self.now - timedelta(hours=25)).astimezone(
                timezone(timedelta(hours=2))).isoformat(),
            "state": "VIDEO_SES_VAR",
        }
        report = evaluate_legacy_stability(
            [old, same_in_utc, same_in_plus_two, self.observation(1)], self.now)
        self.assertEqual(report["GOZLEM_SAYISI"], 2)
        self.assertEqual(report["24_SAAT_KARARLI"], "EVET")
        self.assertFalse(report["network_probed"])
