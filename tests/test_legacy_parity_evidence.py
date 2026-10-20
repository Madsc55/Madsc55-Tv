import unittest
from madsc.legacy_parity_evidence import ledger

def inventory():
    return {"source_repository": "Madsc55/madsc-tv",
            "source_branch": "madsc/bes-sistem-toplu-birlestirme",
            "workflows": [{"path": f".github/workflows/w{i:02}.yml", "candidate_k_stages": ["K5"]}
                          for i in range(99)]}
class EvidenceLedgerTest(unittest.TestCase):
    def test_unproven_inventory_is_blocked(self):
        report = ledger(inventory())
        self.assertEqual((report["total"], report["accepted"], report["blocked"]), (99, 0, 99))
    def test_partial_proof_does_not_approve(self):
        report = ledger(inventory(), {".github/workflows/w00.yml":
                       {"legacy_execution": {"sha256": "a"*64, "run_id": 1}}})
        self.assertEqual(report["accepted"], 0)
    def test_forged_complete_evidence_stays_blocked(self):
        all_proofs = {key: {"sha256": "a"*64, "run_id": 123} for key in (
            "legacy_execution", "new_execution", "input_output_comparison",
            "side_effect_comparison", "failure_timeout_comparison", "reviewer_approval")}
        report = ledger(inventory(), {".github/workflows/w00.yml": all_proofs})
        self.assertEqual(report["accepted"], 0)
    def test_reject_unknown_workflow(self):
        with self.assertRaises(ValueError):
            ledger(inventory(), {"other": {}})
    def test_reject_incomplete_inventory(self):
        i = inventory()
        i["workflows"].pop()
        with self.assertRaises(ValueError):
            ledger(i)
if __name__ == "__main__":
    unittest.main()
