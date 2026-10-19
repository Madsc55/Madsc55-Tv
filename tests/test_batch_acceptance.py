import json
import tempfile
import unittest
from pathlib import Path
from madsc.batch_acceptance import collect, CATEGORIES, MODULES

class BatchAcceptanceTests(unittest.TestCase):
    def make_report(self, directory, key):
        path = Path(directory) / ("madsc-batch-" + key) / (key + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"category": key, "module": MODULES[key], "mode": "isolated_read_only",
                "production_writes": False, "legacy_workflows_executed": False,
                "status": "isolated_fixture_checks_passed_not_production_verified",
                "fixture_checks": {"sample": True},
                "checks": {"isolation": True, "runtime_rule_evidence": False,
                           "legacy_behavioral_equivalence": False}}
        path.write_text(json.dumps(data), encoding="utf-8")
        return path
    def test_five_reports_are_not_production_approval(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                self.make_report(d, key)
            result = collect(Path(d))
            self.assertTrue(result["five_isolated_reports_valid"])
            self.assertTrue(result["k5_fixture_evidence_verified"])
            self.assertFalse(result["production_ready"])
            self.assertFalse(result["legacy_92_behavioral_equivalence_verified"])
    def test_false_fixture_check_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            path = paths["k3"]
            data = json.loads(path.read_text(encoding="utf-8"))
            data["fixture_checks"]["sample"] = False
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_unexpected_json_report_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                self.make_report(d, key)
            (Path(d) / "unexpected.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_missing_category_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES[:-1]:
                self.make_report(d, key)
            with self.assertRaises(ValueError):
                collect(Path(d))
    def test_mutation_claim_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                path = self.make_report(d, key)
            data = json.loads(path.read_text(encoding="utf-8"))
            data["production_writes"] = True
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))
    def test_malformed_report_shapes_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            for malformed in ([], None, "unexpected"):
                paths["k3"].write_text(json.dumps(malformed), encoding="utf-8")
                with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                    collect(Path(d))

    def test_duplicate_evidence_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                self.make_report(d, key)
            self.make_report(Path(d) / "extra", "k1")
            with self.assertRaises(ValueError):
                collect(Path(d))
    def test_symlinked_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            for key in CATEGORIES:
                self.make_report(d, key)
            external = Path(outside) / "external.json"
            external.write_text("{}", encoding="utf-8")
            (Path(d) / "external.json").symlink_to(external)
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_non_directory_evidence_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / "evidence.txt"
            file.write_text("invalid", encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(file)
    def test_empty_fixture_check_name_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            path = paths["k2"]
            data = json.loads(path.read_text(encoding="utf-8"))
            data["fixture_checks"] = {"": True}
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_directory_named_as_report_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            paths["k4"].unlink()
            paths["k4"].mkdir()
            with self.assertRaises(ValueError):
                collect(Path(d))
    def test_report_in_wrong_artifact_directory_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            wrong = Path(d) / "madsc-batch-k3" / "k2.json"
            paths["k2"].rename(wrong)
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_report_outside_artifact_directory_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            paths["k1"].rename(Path(d) / "k1.json")
            with self.assertRaises(ValueError):
                collect(Path(d))
    def test_extra_non_json_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                self.make_report(d, key)
            (Path(d) / "madsc-batch-k1" / "notes.txt").write_text("unexpected", encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_nested_evidence_directory_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                self.make_report(d, key)
            nested = Path(d) / "madsc-batch-k2" / "nested"
            nested.mkdir()
            (nested / "extra.txt").write_text("unexpected", encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))
    def test_mismatched_module_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            paths = {key: self.make_report(d, key) for key in CATEGORIES}
            path = paths["k3"]
            data = json.loads(path.read_text(encoding="utf-8"))
            data["module"] = "backup"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(Path(d))

    def test_fixture_check_names_are_visible_in_acceptance_report(self):
        with tempfile.TemporaryDirectory() as d:
            for key in CATEGORIES:
                self.make_report(d, key)
            report = collect(Path(d))
            self.assertEqual(report["categories"]["k1"]["module"], "security")
            self.assertEqual(report["categories"]["k1"]["fixture_check_names"], ["sample"])
            self.assertFalse(report["runtime_rules_verified"])
