"""K1 rejection before K4 source reads and shared report directory creation."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.backup import backup_to_new_sandbox, restore_to_new_sandbox
from madsc.fixture_report_writer import write_stage_report

class K4WritePreflightTests(unittest.TestCase):
    def test_copy_writers_reject_protected_roots_before_source_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            source.mkdir()
            (source / 'a.txt').write_text('original')
            for writer in (backup_to_new_sandbox, restore_to_new_sandbox):
                for name in ('EPG', 'FAVORILER', 'YEDEKLER', 'logos', 'playlist.m3u8'):
                    target = root / name
                    with self.subTest(writer=writer.__name__, name=name):
                        with patch('madsc.backup.snapshot_manifest') as snapshot:
                            with self.assertRaises(PermissionError):
                                writer(source, target, ['a.txt'])
                            snapshot.assert_not_called()
                        self.assertFalse(target.exists())
            self.assertEqual((source / 'a.txt').read_text(), 'original')

    def test_copy_writers_reject_protected_ancestor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, protected = root / 'source', root / 'EPG'
            source.mkdir()
            protected.mkdir()
            for writer in (backup_to_new_sandbox, restore_to_new_sandbox):
                with self.assertRaises(PermissionError):
                    writer(source, protected / 'new-copy', ['missing.txt'])
            self.assertEqual(list(protected.iterdir()), [])

    def test_stage_writers_reject_before_creating_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'FAVORILER'
            root.mkdir()
            for stage in ('k3', 'k4', 'k5'):
                with self.subTest(stage=stage), self.assertRaises(PermissionError):
                    write_stage_report(root, stage, {'category': stage,
                        'production_writes': False, 'production_ready': False})
            self.assertEqual(list(root.iterdir()), [])
