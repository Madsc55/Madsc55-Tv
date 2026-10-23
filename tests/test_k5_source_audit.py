"""Offline regression tests for K5 frozen-source coverage and tamper detection."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.k5_source_audit import audit


class K5SourceAuditTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]

    def test_all_92_source_rows_pinned(self):
        result = audit(self.root)
        self.assertEqual(result["expected"], 92)
        self.assertEqual(result["recorded"], 92)
        self.assertEqual(result["verified_source_rows"], 92)
        self.assertTrue(result["source_audit_passed"], result["errors"])
        self.assertFalse(result["production_accepted"])
        self.assertEqual(result["behavioral_parity_accepted"], 0)
        self.assertEqual(result["behavioral_evidence_missing"], 92)
        self.assertEqual(result["independent_old_new_execution_pairs"], 0)
        self.assertEqual(result["yaml_signal_counts"]["push"], 21)
        self.assertEqual(result["yaml_signal_counts"]["write"], 20)

    def test_malformed_inventory_digest_fails_closed(self):
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            value = original(path, *args, **kwargs)
            if str(path).endswith("LEGACY_SOURCE_SCOPE.json"):
                data = json.loads(value)
                data["workflows"][0]["git_blob_sha"] = "invalid"
                return json.dumps(data)
            return value

        with patch.object(Path, "read_text", read_text):
            result = audit(self.root)
        self.assertFalse(result["source_audit_passed"])
        self.assertIn("invalid_inventory_row", result["errors"])

    def test_missing_excluded_workflow_fails_closed(self):
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            value = original(path, *args, **kwargs)
            if str(path).endswith("LEGACY_SOURCE_SCOPE.json"):
                data = json.loads(value)
                data["workflows"] = [r for r in data["workflows"]
                                     if not r["path"].endswith("/madsc-01-guvenlik.yml")]
                return json.dumps(data)
            return value

        with patch.object(Path, "read_text", read_text):
            result = audit(self.root)
        self.assertFalse(result["source_audit_passed"])
        self.assertIn("excluded_scope_mismatch", result["errors"])

    def test_invalid_part_json_type_fails_closed(self):
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            if str(path).endswith("K5_KAYNAK_DOGRULAMA_91_92.json"):
                return "[]"
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", read_text):
            result = audit(self.root)
        self.assertFalse(result["source_audit_passed"])
        self.assertIn("invalid_part_object:91_92", result["errors"])

    def test_missing_batch_fails_closed(self):
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            if str(path).endswith("K5_KAYNAK_DOGRULAMA_91_92.json"):
                raise FileNotFoundError("simulated missing evidence")
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", read_text):
            result = audit(self.root)
        self.assertFalse(result["source_audit_passed"])
        self.assertTrue(any("missing_or_invalid_part:91_92" in x for x in result["errors"]))

    def test_malformed_stage_mapping_fails_closed(self):
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            value = original(path, *args, **kwargs)
            if str(path).endswith("K5_KAYNAK_DOGRULAMA_91_92.json"):
                data = json.loads(value)
                data["rows"][0]["candidate_stages"] = ["K6"]
                return json.dumps(data)
            return value

        with patch.object(Path, "read_text", read_text):
            result = audit(self.root)
        self.assertFalse(result["source_audit_passed"])
        self.assertTrue(any(x.startswith("invalid_signals:") for x in result["errors"]))

    def test_tampered_source_sha_fails_closed(self):
        original = Path.read_text

        def read_text(path, *args, **kwargs):
            value = original(path, *args, **kwargs)
            if str(path).endswith("K5_KAYNAK_DOGRULAMA_91_92.json"):
                data = json.loads(value)
                data["rows"][0]["sha"] = "0" * 40
                return json.dumps(data)
            return value

        with patch.object(Path, "read_text", read_text):
            result = audit(self.root)
        self.assertFalse(result["source_audit_passed"])
        self.assertTrue(any(x.startswith("sha_mismatch:") for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
