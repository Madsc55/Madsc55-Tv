"""Exercise real acceptance CLI boundaries before evidence work or network."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc import batch_acceptance, handoff_acceptance, history_origin_cli


class AcceptanceOutputGuardsTests(unittest.TestCase):
    def invoke(self, module, root, output):
        if module is batch_acceptance:
            options = ['--reports', str(root / 'inputs')]
        elif module is handoff_acceptance:
            options = [part for key in ('k2', 'k3', 'k5')
                       for part in ('--' + key, str(root / (key + '.json')))]
            options += ['--run-id', '123', '--commit-sha', 'a' * 40]
        else:
            options = ['--source-folder', str(root / 'inputs'), '--manifest',
                       str(root / 'manifest.json'), '--current-sha', 'a' * 40]
        with patch('sys.argv', ['report'] + options + ['--output', str(output)]):
            module.main()

    def test_protected_existing_and_symlink_targets_fail_before_work(self):
        for module, operation in ((batch_acceptance, 'collect'),
                                  (handoff_acceptance, 'verify'),
                                  (history_origin_cli, 'verify_live_github_origin')):
            with self.subTest(module=module.__name__), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                outside = root / 'outside'
                outside.mkdir()
                (root / 'alias').symlink_to(outside, target_is_directory=True)
                existing = root / 'existing.json'
                existing.write_bytes(b'original evidence')
                targets = [root / 'xmltv.xml', root / 'playlist.m3u8',
                           root / 'alias' / 'result.json', existing]
                for target in targets:
                    with patch.object(module, operation) as work:
                        with self.assertRaises(PermissionError):
                            self.invoke(module, root, target)
                        work.assert_not_called()
                self.assertEqual(existing.read_bytes(), b'original evidence')
                self.assertEqual(list(outside.iterdir()), [])
                self.assertFalse((root / 'xmltv.xml').exists())

    def test_batch_report_uses_exclusive_safe_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'result.json'
            with patch.object(batch_acceptance, 'collect', return_value={
                    'production_ready': False}), patch('builtins.print'):
                self.invoke(batch_acceptance, root, output)
            self.assertEqual(json.loads(output.read_text()), {'production_ready': False})
            with self.assertRaises(PermissionError):
                self.invoke(batch_acceptance, root, output)
