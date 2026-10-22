import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from madsc.k4_evidence import main
from madsc.write_path_audit import ProtectedWriteRejected
from madsc.k4_evidence import verify

GOOD = {
    "drill_executed": True, "temporary_backup_created": True,
    "temporary_restore_created": True, "source_unchanged": True,
    "independent_sandbox_restore_matches": True,
    "backup_verified_against_source": True, "restore_verified_against_backup": True,
    "external_storage_proven": False, "production_restore_verified": False,
    "production_writes": False, "files_checked": 2,
}

class K4EvidenceTests(unittest.TestCase):
    def test_isolated_restore_acceptance_never_implies_production(self):
        result = verify(GOOD)
        self.assertTrue(result["k4_isolated_restore_verified"])
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["external_storage_proven"])

    def test_fail_closed_for_missing_or_forged_evidence(self):
        for key in GOOD:
            with self.subTest(key=key):
                tampered = dict(GOOD)
                tampered.pop(key)
                with self.assertRaises(ValueError):
                    verify(tampered)
        for change in ({"source_unchanged": False},
                       {"production_writes": True},
                       {"external_storage_proven": True},
                       {"files_checked": 0},
                       {"files_checked": True}):
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    verify({**GOOD, **change})

    def test_cli_rejects_existing_output_before_reading_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "exists.json"
            output.write_text("unchanged")
            args = ["k4_evidence", "--report", str(root / "missing.json"), "--output", str(output)]
            with patch("sys.argv", args), self.assertRaises(ProtectedWriteRejected):
                main()
            self.assertEqual(output.read_text(), "unchanged")

    def test_cli_rejects_symlink_and_oversized_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real.json"
            real.write_text(json.dumps(GOOD))
            alias = root / "alias.json"
            alias.symlink_to(real)
            huge = root / "huge.json"
            huge.write_bytes(b"x" * (1024 * 1024 + 1))
            for report in (alias, huge):
                with self.subTest(report=report):
                    output = root / "result.json"
                    args = ["k4_evidence", "--report", str(report), "--output", str(output)]
                    with patch("sys.argv", args), self.assertRaises(ValueError):
                        main()
                    self.assertFalse(output.exists())

if __name__ == "__main__":
    unittest.main()
