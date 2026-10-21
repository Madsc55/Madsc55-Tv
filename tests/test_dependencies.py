import unittest
from madsc.dependencies import plan_task, validate_batch

class DependencyTests(unittest.TestCase):
    def test_discovery_handoff_reaches_testing_backup_and_maintenance(self):
        plan = plan_task("candidate_discovery")
        self.assertEqual(plan["involved_categories"], ["k2", "k3", "k4", "k5"])
        self.assertEqual(plan["independent_extra_triggers"], 0)
        self.assertFalse(plan["schedule_activation_allowed"])
    def test_ibo_protection_is_cross_category(self):
        self.assertEqual(plan_task("ibo_device_decision")["involved_categories"],
                         ["k1", "k3", "k4", "k5"])
    def test_duplicate_task_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_batch(["candidate_discovery", "candidate_discovery"])
    def test_unknown_task_requires_review(self):
        with self.assertRaises(ValueError):
            plan_task("unknown")
    def test_batch_does_not_authorize_production(self):
        result = validate_batch(["candidate_discovery", "backup_restore"])
        self.assertFalse(result["ready_for_production"])
        self.assertEqual(result["independent_extra_triggers"], 0)

    def test_invalid_batch_inputs(self):
        for value in ([], [None], [123], ["candidate_discovery", None]):
            with self.assertRaises(ValueError):
                validate_batch(value)
