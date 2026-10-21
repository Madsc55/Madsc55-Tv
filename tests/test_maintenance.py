import unittest
from madsc.maintenance import retry_decision, aggregate, summarize_batch, verify_fixture_evidence, review_candidate_batch

class MaintenanceTests(unittest.TestCase):
    def test_bounded_retry(self):
        self.assertEqual(retry_decision(3)["next_action"], "HALT_AND_REPORT")
        self.assertFalse(retry_decision(2)["blocked"])
        with self.assertRaises(ValueError):
            retry_decision(-1)
    def test_limit_boundary(self):
        self.assertFalse(retry_decision(2, 3)["blocked"])
        self.assertTrue(retry_decision(3, 3)["blocked"])
        self.assertTrue(retry_decision(4, 3)["blocked"])

    def test_noninteger_limit_rejected(self):
        for limit in (True, 2.5, "3"):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                retry_decision(1, limit)

    def test_batch_failure_summary(self):
        reports = [{"category": k, "production_writes": False, "status": "success"} for k in ("k1", "k2", "k3", "k4", "k5")]
        self.assertFalse(summarize_batch(reports)["requires_review"])
        reports[2]["status"] = "failure"
        summary = summarize_batch(reports)
        self.assertEqual(summary["failed_categories"], ["k3"])
        self.assertTrue(summary["requires_review"])
        self.assertFalse(summary["production_writes"])

    def test_missing_category_requires_review(self):
        reports = [{"category": "k1", "production_writes": False, "status": "success"}]
        summary = summarize_batch(reports)
        self.assertTrue(summary["requires_review"])
        self.assertEqual(summary["missing_categories"], ["k2", "k3", "k4", "k5"])

    def test_unknown_status_and_missing_status_fail_closed(self):
        reports = [{"category": k, "production_writes": False, "status": "success"} for k in ("k1", "k2", "k3", "k4", "k5")]
        reports[0]["status"] = "pending"
        reports[1].pop("status")
        summary = summarize_batch(reports)
        self.assertEqual(summary["failed_categories"], ["k1", "k2"])
        self.assertTrue(summary["requires_review"])

    def test_duplicate_and_unexpected_categories_flagged(self):
        reports = [{"category": k, "production_writes": False, "status": "success"} for k in ("k1", "k2", "k3", "k4", "k5")]
        reports.append({"category": "k1", "production_writes": False, "status": "success"})
        reports.append({"category": "unknown", "production_writes": False, "status": "success"})
        summary = summarize_batch(reports)
        self.assertEqual(summary["duplicate_categories"], ["k1"])
        self.assertEqual(summary["unexpected_category_count"], 1)
        self.assertTrue(summary["requires_review"])

    def test_all_five_successful_requires_explicit_status(self):
        reports = [{"category": k, "production_writes": False, "status": "success"} for k in ("k1", "k2", "k3", "k4", "k5")]
        self.assertTrue(aggregate(reports)["all_five_successful"])
        reports[0]["status"] = "pending"
        self.assertTrue(aggregate(reports)["all_five_present"])
        self.assertFalse(aggregate(reports)["all_five_successful"])
        reports[0].pop("status")
        self.assertFalse(aggregate(reports)["all_five_successful"])

    def test_unverified_or_true_production_writes_require_review(self):
        reports = [{"category": k, "production_writes": False, "status": "success"} for k in ("k1", "k2", "k3", "k4", "k5")]
        reports[1].pop("production_writes")
        reports[3]["production_writes"] = True
        summary = summarize_batch(reports)
        self.assertEqual(summary["unsafe_or_unverified_write_categories"], ["k2", "k4"])
        self.assertFalse(summary["all_five_successful"])
        self.assertTrue(summary["requires_review"])

    def test_fixture_evidence_requires_explicit_true_checks(self):
        reports = [{"category": k, "production_writes": False, "status": "success",
                    "fixture_checks": {"isolated": True}} for k in ("k1", "k2", "k3", "k4", "k5")]
        self.assertTrue(verify_fixture_evidence(reports)["fixture_evidence_verified"])
        reports[0].pop("fixture_checks")
        reports[1]["fixture_checks"]["isolated"] = False
        result = verify_fixture_evidence(reports)
        self.assertFalse(result["fixture_evidence_verified"])
        self.assertEqual(result["missing_fixture_evidence"], ["k1"])
        self.assertEqual(result["failed_fixture_checks"], ["k2"])
        self.assertFalse(result["production_ready"])

    def test_unhashable_category_fails_closed_without_type_error(self):
        for invalid in ([], {}, ["k1"]):
            with self.subTest(invalid=invalid):
                reports = [{"category": invalid, "production_writes": False, "status": "success"}]
                self.assertFalse(aggregate(reports)["all_five_present"])
                summary = summarize_batch(reports)
                self.assertTrue(summary["requires_review"])
                self.assertEqual(summary["unexpected_category_count"], 1)

    def test_missing_categories_never_ready(self):
        self.assertFalse(aggregate([{"category":"k1","production_writes":False}])["all_five_present"])

class CrossSystemReviewTests(unittest.TestCase):
    def setUp(self):
        self.coordination = {"candidates": [{
            "url_sha256": "a" * 64, "hold": True, "protected_working": True,
            "production_change_allowed": False, "delete_allowed": False}],
            "production_writes": False, "production_ready": False, "network_probed": False}
        self.backup = {"independent_sandbox_restore_matches": True,
                       "production_writes": False, "production_restore_verified": False,
                       "external_storage_proven": False}

    def test_k5_preserves_ibo_and_requires_k4(self):
        result = review_candidate_batch(self.coordination, self.backup)
        self.assertTrue(result["review_evidence_complete"])
        self.assertEqual(result["protected_ibo_working_count"], 1)
        self.assertFalse(result["production_ready"])
        self.backup["independent_sandbox_restore_matches"] = False
        self.assertFalse(review_candidate_batch(self.coordination, self.backup)["review_evidence_complete"])

    def test_unsafe_or_repeated_candidate_rejected(self):
        self.coordination["candidates"][0]["delete_allowed"] = True
        with self.assertRaises(ValueError):
            review_candidate_batch(self.coordination, self.backup)
        self.coordination["candidates"][0]["delete_allowed"] = False
        self.coordination["candidates"].append(dict(self.coordination["candidates"][0]))
        with self.assertRaises(ValueError):
            review_candidate_batch(self.coordination, self.backup)

    def test_external_restore_claim_rejected(self):
        self.backup["external_storage_proven"] = True
        with self.assertRaises(ValueError):
            review_candidate_batch(self.coordination, self.backup)

