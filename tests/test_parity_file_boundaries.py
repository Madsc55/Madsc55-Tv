"""Real parity entrypoints must not hang on FIFOs or certify changing files."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.parity_manifest_cli import produce_from_files
from madsc.parity_snapshot_writer import write_execution_snapshot


class ParityFileBoundaryTests(unittest.TestCase):
    def test_fifo_without_writer_fails_promptly_in_both_entrypoints(self):
        for mode in ('manifest', 'snapshot'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                fifo = root / 'input'
                os.mkfifo(fifo)
                code = '''
import sys
from pathlib import Path
from madsc.parity_manifest_cli import produce_from_files
from madsc.parity_snapshot_writer import write_execution_snapshot
root = Path(sys.argv[1])
try:
    if sys.argv[2] == 'manifest':
        produce_from_files(input_path=root/'input', snapshot_path=root/'absent.json',
            output_root=root, repository='Madsc55/Madsc55-Tv', branch='main',
            workflow_path='.github/workflows/madsc-02-kesif.yml', run_id=123,
            head_sha='a'*40)
    else:
        write_execution_snapshot(root, exit_code=0, timed_out=False,
            outputs=[('result', root/'input')], side_effects=[])
except PermissionError:
    sys.exit(0)
sys.exit(2)
'''
                result = subprocess.run([sys.executable, '-c', code, str(root), mode],
                                        capture_output=True, timeout=5, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse((root / 'reports').exists())

    def test_input_mutation_during_manifest_read_creates_no_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'input'
            source.write_bytes(b'initial input')
            snapshot = root / 'snapshot.json'
            snapshot.write_text(json.dumps({'exit_code': 0, 'timed_out': False,
                                           'outputs': {'result': 'a'*64}, 'side_effects': {}}))
            real_read = os.read
            changed = False
            def mutate(fd, size):
                nonlocal changed
                chunk = real_read(fd, size)
                if not changed:
                    changed = True
                    source.write_bytes(b'different input size')
                return chunk
            with patch('madsc.parity_manifest_cli.os.read', side_effect=mutate):
                with self.assertRaises(ValueError):
                    produce_from_files(input_path=source, snapshot_path=snapshot,
                        output_root=root, repository='Madsc55/Madsc55-Tv', branch='main',
                        workflow_path='.github/workflows/madsc-02-kesif.yml', run_id=123,
                        head_sha='a'*40)
            self.assertFalse((root / 'reports').exists())

    def test_observation_mutation_during_snapshot_read_creates_no_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'output'
            source.write_bytes(b'first output')
            real_read = os.read
            changed = False
            def mutate(fd, size):
                nonlocal changed
                chunk = real_read(fd, size)
                if not changed:
                    changed = True
                    source.write_bytes(b'changed output length')
                return chunk
            with patch('madsc.parity_snapshot_writer.os.read', side_effect=mutate):
                with self.assertRaises(ValueError):
                    write_execution_snapshot(root, exit_code=0, timed_out=False,
                        outputs=[('result', source)], side_effects=[])
            self.assertFalse((root / 'reports').exists())

    def test_path_replacement_with_equal_size_is_not_certified(self):
        for mode in ('manifest', 'snapshot'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                source = root / 'input'
                source.write_bytes(b'original')
                snapshot = root / 'snapshot.json'
                snapshot.write_text(json.dumps({'exit_code': 0, 'timed_out': False,
                                               'outputs': {'result': 'a'*64}, 'side_effects': {}}))
                real_read = os.read
                changed = False
                def replace(fd, size):
                    nonlocal changed
                    chunk = real_read(fd, size)
                    if not changed:
                        changed = True
                        source.unlink()
                        source.write_bytes(b'replaced')
                    return chunk
                module = 'madsc.parity_manifest_cli' if mode == 'manifest' else 'madsc.parity_snapshot_writer'
                with patch(module + '.os.read', side_effect=replace):
                    with self.assertRaises(ValueError):
                        if mode == 'manifest':
                            produce_from_files(input_path=source, snapshot_path=snapshot,
                                output_root=root, repository='Madsc55/Madsc55-Tv', branch='main',
                                workflow_path='.github/workflows/madsc-02-kesif.yml', run_id=123,
                                head_sha='a'*40)
                        else:
                            write_execution_snapshot(root, exit_code=0, timed_out=False,
                                outputs=[('result', source)], side_effects=[])
                self.assertFalse((root / 'reports').exists())
