"""Regression cases for source provenance and history replay."""
import unittest
from datetime import datetime, timezone
from madsc.legacy_history_merge import merge_pair, stamp
from madsc.legacy_history_provenance import select_ancestor_run
from madsc.legacy_retest_390 import parse_entries


def bundle(records):
    return {"gecmis.json": {"history": records},
            "ana_liste_test_gecmisi.json": {"channels": {}}}


class LegacyReplayTests(unittest.TestCase):
    def test_timezone_normalization(self):
        self.assertEqual(stamp("2026-10-22T12:00:00+02:00"),
                         stamp("2026-10-22T10:00:00Z"))

    def test_invalid_new_history_timestamp_fails(self):
        with self.assertRaises(ValueError):
            merge_pair(bundle({}), bundle({"stream": {"last_test": "not-a-date"}}))

    def test_newer_run_count_cannot_regress(self):
        old = bundle({"stream": {"last_test": "2026-10-21T10:00:00Z", "runs": 5}})
        new = bundle({"stream": {"last_test": "2026-10-22T10:00:00Z", "runs": 4}})
        with self.assertRaises(ValueError):
            merge_pair(old, new)

    def test_history_update_does_not_mutate_input(self):
        old = bundle({"stream": {"last_test": "2026-10-21T10:00:00Z", "runs": 1}})
        new = bundle({"stream": {"last_test": "2026-10-22T10:00:00Z", "runs": 2}})
        merged, changes = merge_pair(old, new)
        self.assertEqual(merged["gecmis.json"]["history"]["stream"]["runs"], 2)
        self.assertEqual(old["gecmis.json"]["history"]["stream"]["runs"], 1)
        self.assertEqual(changes["gecmis.json"]["updated"], 1)

    def test_ancestry_callback_must_be_boolean(self):
        run = {"id": 1, "head_branch": "main", "status": "completed",
               "conclusion": "success", "head_repository": {"full_name": "owner/repo"},
               "path": ".github/workflows/source.yml", "event": "push",
               "head_sha": "a" * 40}
        with self.assertRaises(ValueError):
            select_ancestor_run([run], repo="owner/repo", branch="main",
                                current_run=2, ancestor_check=lambda _: "yes",
                                workflows=["source.yml"])

    def test_retest_parser_rejects_headerless_input(self):
        with self.assertRaises(ValueError):
            parse_entries("#EXTINF:-1,Example\\nhttps://example.org/live")
        self.assertEqual(len(parse_entries("#EXTM3U\\n#EXTINF:-1,Example\\nhttps://example.org/live")), 1)
