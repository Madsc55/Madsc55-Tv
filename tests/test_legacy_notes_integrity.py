"""Bulk legacy archive verification, positive and tampering regression."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc import legacy_notes_integrity
from scripts import birlestir_eski_sistem_notlari as merger


class LegacyNotesIntegrityTests(unittest.TestCase):
    def test_merge_all_sources_and_reject_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "archive"
            archive.mkdir()
            (archive / "AGENTS.md").write_text("Old rules\n", encoding="utf-8")
            (archive / "notes.txt").write_text("Historical decisions\n", encoding="utf-8")
            (archive / "decision.json").write_text('{"approved":false}\n', encoding="utf-8")
            merged = root / "merged.md"
            with patch.object(merger, "ARCHIVE", archive), patch.object(merger, "OUTPUT", merged):
                merger.build(include_structured=True, remove=False)
            report = root / "report.json"
            result = legacy_notes_integrity.verify(merged, archive, report)
            self.assertTrue(result["verified"])
            self.assertEqual(result["sources"], 3)
            before = merged.read_bytes()
            with self.assertRaises(PermissionError):
                legacy_notes_integrity.verify(merged, archive, root / "xmltv.xml")
            self.assertFalse((root / "xmltv.xml").exists())
            self.assertEqual(merged.read_bytes(), before)

            self.assertTrue((archive / "AGENTS.md").exists())
            self.assertTrue((archive / "decision.json").exists())
            merged.write_text(merged.read_text().replace("Historical decisions", "TAMPERED"), encoding="utf-8")
            with self.assertRaises(ValueError):
                legacy_notes_integrity.verify(merged, archive, root / "bad-report.json")
            self.assertFalse((root / "bad-report.json").exists())

    def test_unmarked_injected_text_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "archive"
            archive.mkdir()
            (archive / "AGENTS.md").write_text("Rules\n", encoding="utf-8")
            merged = root / "merged.md"
            with patch.object(merger, "ARCHIVE", archive), patch.object(merger, "OUTPUT", merged):
                merger.build(include_structured=True, remove=False)
            original = merged.read_text(encoding="utf-8")
            merged.write_text(original + "\nINJECTED APPROVAL\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unexpected text"):
                legacy_notes_integrity.verify(merged, archive, root / "report.json")
            self.assertFalse((root / "report.json").exists())

    def test_missing_archive_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                legacy_notes_integrity.verify(root / "missing.md", root / "missing", root / "report.json")


if __name__ == "__main__":
    unittest.main()
