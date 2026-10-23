"""K3 bounded acceptance candidate limit regression tests."""
import unittest
from unittest.mock import patch
from madsc import k3_live_manifest_pilot as pilot


class K3ManifestLimitTests(unittest.TestCase):
    def test_rejects_invalid_limits_before_network(self):
        for limit in (0, -1, 76, "75", None):
            with self.subTest(limit=limit), patch.object(pilot, "candidates") as source:
                with self.assertRaises(ValueError):
                    pilot.run(limit=limit)
                source.assert_not_called()

    def test_default_and_ceiling(self):
        self.assertEqual(pilot.LIMIT, 12)
        self.assertEqual(pilot.MAX_LIMIT, 75)

    def test_shortfall_and_timestamp_are_recorded(self):
        import json
        with patch.object(pilot, "candidates", return_value=iter(())), \
             patch.object(pilot, "write_fixture_report") as writer:
            pilot.run(limit=75)
            report = json.loads(writer.call_args.args[2])
            self.assertEqual(report["candidate_limit"], 75)
            self.assertEqual(report["candidate_shortfall"], 75)
            self.assertEqual(report["probed"], 0)
            self.assertIn("measured_at_utc", report)
