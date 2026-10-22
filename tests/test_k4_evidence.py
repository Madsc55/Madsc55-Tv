import unittest
import json
import os
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

    def test_cli_fails_closed_without_nofollow(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "valid.json"
            report.write_text(json.dumps(GOOD))
            output = root / "result.json"
            args = ["k4_evidence", "--report", str(report), "--output", str(output)]
            with patch("sys.argv", args), patch("madsc.k4_evidence.os") as mocked_os:
                del mocked_os.O_NOFOLLOW
                with self.assertRaises(ValueError):
                    main()
            self.assertFalse(output.exists())

    def test_cli_rejects_hardlinked_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = root / "original.json"
            original.write_text(json.dumps(GOOD))
            hardlink = root / "hardlink.json"
            os.link(original, hardlink)
            output = root / "result.json"
            args = ["k4_evidence", "--report", str(hardlink), "--output", str(output)]
            with patch("sys.argv", args), self.assertRaises(ValueError):
                main()
            self.assertFalse(output.exists())
            self.assertEqual(json.loads(original.read_text()), GOOD)

    def test_cli_rejects_duplicate_json_keys_and_symlinked_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "duplicate.json"
            report.write_text(json.dumps(GOOD)[:-1] + ', "files_checked": 99}')
            real_dir = root / "real"
            real_dir.mkdir()
            real_report = real_dir / "valid.json"
            real_report.write_text(json.dumps(GOOD))
            alias_dir = root / "alias"
            alias_dir.symlink_to(real_dir, target_is_directory=True)
            for candidate in (report, alias_dir / "valid.json"):
                with self.subTest(candidate=candidate):
                    output = root / "result.json"
                    args = ["k4_evidence", "--report", str(candidate), "--output", str(output)]
                    with patch("sys.argv", args), self.assertRaises(ValueError):
                        main()
                    self.assertFalse(output.exists())

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

    def test_cli_writes_isolated_result_once_without_production_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = root / "evidence.json"
            output = root / "verified.json"
            report.write_text(json.dumps(GOOD))
            args = ["k4_evidence", "--report", str(report), "--output", str(output)]
            with patch("sys.argv", args):
                main()
            result = json.loads(output.read_text())
            self.assertTrue(result["k4_isolated_restore_verified"])
            self.assertFalse(result["production_ready"])
            self.assertFalse(result["external_storage_proven"])
            with patch("sys.argv", args), self.assertRaises(ProtectedWriteRejected):
                main()
            self.assertEqual(json.loads(output.read_text()), result)

if __name__ == "__main__":
    unittest.main()
