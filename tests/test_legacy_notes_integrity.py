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

    def test_remove_archived_notes_is_rejected_before_output_or_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "docs/eski_depo_not_arsivi"
            archive.mkdir(parents=True)
            source = archive / "AGENTS.md"
            source.write_text("Old rules\n", encoding="utf-8")
            merged = root / "merged.md"
            with patch.object(merger, "ARCHIVE", archive), patch.object(merger, "OUTPUT", merged):
                with self.assertRaisesRegex(PermissionError, "removal is prohibited"):
                    merger.build(remove=True)
            self.assertEqual(source.read_text(encoding="utf-8"), "Old rules\n")
            self.assertFalse(merged.exists())

    def test_symlinked_temporary_output_is_rejected_without_external_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "archive"
            archive.mkdir()
            (archive / "AGENTS.md").write_text("Old rules\n", encoding="utf-8")
            merged = root / "merged.md"
            outside = root / "outside.md"
            outside.write_text("preserve", encoding="utf-8")
            merged.with_suffix(".md.tmp").symlink_to(outside)
            with patch.object(merger, "ARCHIVE", archive), patch.object(merger, "OUTPUT", merged):
                with self.assertRaises(PermissionError):
                    merger.build()
            self.assertEqual(outside.read_text(encoding="utf-8"), "preserve")
            self.assertFalse(merged.exists())

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
