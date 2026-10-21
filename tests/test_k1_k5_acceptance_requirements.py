import unittest

from madsc.k1_k5_acceptance_requirements import REQUIREMENTS, assess_task_evidence


class K1K5AcceptanceRequirementsTests(unittest.TestCase):
    def sample(self):
        return [{"id": tid, "stage": tid[:2], "title": tid,
                 "status": "pending" if n < 17 else "in_progress", "evidence": []}
                for n, tid in enumerate(REQUIREMENTS)]

    def test_all_22_fail_closed_without_real_evidence(self):
        report = assess_task_evidence(self.sample())
        self.assertEqual(report["total"], 22)
        self.assertEqual(report["requirements_missing_tasks"], 22)
        self.assertFalse(report["production_ready"])
        self.assertFalse(report["github_actions_triggered"])
        self.assertFalse(report["tests_executed"])

    def test_duplicate_task_rejected(self):
        tasks = self.sample()
        tasks[1] = dict(tasks[0])
        with self.assertRaises(ValueError):
            assess_task_evidence(tasks)

    def test_unknown_evidence_rejected(self):
        with self.assertRaises(ValueError):
            assess_task_evidence(self.sample(), {"K3-12": {"not_a_real_requirement": True}})

    def test_partial_claim_does_not_mark_production_accepted(self):
        report = assess_task_evidence(
            self.sample(), {"K3-12": {"ibo_real_device_user_acceptance": True}})
        item = next(row for row in report["tasks"]["K3"] if row["id"] == "K3-12")
        self.assertEqual(item["missing_evidence"], [])
        self.assertFalse(item["production_acceptance_proven_by_this_report"])
        self.assertFalse(report["production_ready"])

    def test_missing_stage_and_wrong_status_rejected(self):
        tasks = self.sample()
        tasks[0]["stage"] = "K2"
        with self.assertRaises(ValueError):
            assess_task_evidence(tasks)
        tasks = self.sample()
        tasks[0]["status"] = "done"
        with self.assertRaises(ValueError):
            assess_task_evidence(tasks)


if __name__ == "__main__":
    unittest.main()
