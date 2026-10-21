"""History chain tampering, wrong-run, and false-approval negative tests."""
import unittest
from madsc.history_handoff import pack_history, unpack_history, verify_history_chain


def pair():
    return {"gecmis.json": {"history": {"fixture": {"runs": 2}}},
            "ana_liste_test_gecmisi.json": {"channels": {"fixture": {"runs": 2}}}}


class HistoryHandoffTests(unittest.TestCase):
    def setUp(self):
        self.k2 = pack_history(pair(), "123", "a" * 40)
        self.report = {"schema": "madsc-history-handoff-v1", "run_id": "123",
                       "commit_sha": "a" * 40, "source_digest": self.k2["digest"],
                       "read_only": True, "production_ready": False}

    def test_same_run_same_commit_and_read_only(self):
        self.assertEqual(unpack_history(self.k2, "123", "a" * 40), pair())
        self.assertTrue(verify_history_chain(self.k2, self.report, self.report,
                                             "123", "a" * 40)["history_chain_verified"])

    def test_wrong_run_commit_or_payload_rejected(self):
        for run_id, sha in (("999", "a" * 40), ("123", "b" * 40)):
            with self.assertRaises(ValueError):
                unpack_history(self.k2, run_id, sha)
        changed = {**self.k2, "history_envelope": {
            **self.k2["history_envelope"], "sha256": "f" * 64}}
        with self.assertRaises(ValueError):
            unpack_history(changed, "123", "a" * 40)

    def test_k3_k5_tampering_or_false_approval_rejected(self):
        for field, value in (("run_id", "999"), ("commit_sha", "b" * 40),
                             ("source_digest", "f" * 64), ("production_ready", True),
                             ("read_only", False)):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    verify_history_chain(self.k2, {**self.report, field: value},
                                         self.report, "123", "a" * 40)
                with self.assertRaises(ValueError):
                    verify_history_chain(self.k2, self.report,
                                         {**self.report, field: value}, "123", "a" * 40)


if __name__ == "__main__":
    unittest.main()
