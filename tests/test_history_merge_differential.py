"""Compare pinned old and new history merge for H01/H02/H04 decisions."""
import importlib.util
import unittest
from copy import deepcopy
from pathlib import Path

from madsc.legacy_history_merge import merge_pair

FIXTURE = Path(__file__).parent / "fixtures" / "legacy_discovery_history_restore.py"


def pair(record):
    return {"gecmis.json": {"history": {"candidate": deepcopy(record)}},
            "ana_liste_test_gecmisi.json": {"channels": {"candidate": deepcopy(record)}}}


class HistoryMergeDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("pinned_history_restore", FIXTURE)
        cls.legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.legacy)

    def test_newer_failure_wins_and_metadata_survives(self):
        base = pair({"last_test": "2026-10-19T12:00:00Z", "runs": 2,
                     "last_result": "PASS", "decision": "MANUAL_ONLY",
                     "source_history": ["a"]})
        incoming = pair({"last_test": "2026-10-20T12:00:00Z", "runs": 3,
                         "last_result": "FAIL", "source_history": ["b"]})
        expected = self.legacy.merge_pair(deepcopy(base), incoming)
        actual = merge_pair(deepcopy(base), incoming)
        self.assertEqual(expected, actual)
        for document, key in (("gecmis.json", "history"),
                              ("ana_liste_test_gecmisi.json", "channels")):
            row = actual[0][document][key]["candidate"]
            self.assertEqual(row["last_result"], "FAIL")
            self.assertEqual(row["decision"], "MANUAL_ONLY")
            self.assertEqual(row["source_history"], ["a", "b"])
        self.assertEqual(base["gecmis.json"]["history"]["candidate"]["last_result"], "PASS")

    def test_same_time_conflict_and_regressed_runs_rejected(self):
        base = pair({"last_test": "2026-10-19T12:00:00Z", "runs": 5,
                     "last_result": "PASS"})
        cases = [
            pair({"last_test": "2026-10-19T12:00:00Z", "runs": 5,
                  "last_result": "FAIL"}),
            pair({"last_test": "2026-10-20T12:00:00Z", "runs": 4,
                  "last_result": "FAIL"}),
        ]
        for incoming in cases:
            with self.subTest(incoming=incoming):
                for impl in (self.legacy.merge_pair, merge_pair):
                    with self.assertRaises(ValueError):
                        impl(deepcopy(base), incoming)
                self.assertEqual(base["gecmis.json"]["history"]["candidate"]["runs"], 5)

    def test_older_observation_cannot_replace_newer_result(self):
        base = pair({"last_test": "2026-10-20T12:00:00Z", "runs": 5,
                     "last_result": "FAIL"})
        incoming = pair({"last_test": "2026-10-19T12:00:00Z", "runs": 4,
                         "last_result": "PASS"})
        self.assertEqual(self.legacy.merge_pair(deepcopy(base), incoming),
                         merge_pair(deepcopy(base), incoming))


if __name__ == "__main__":
    unittest.main()
