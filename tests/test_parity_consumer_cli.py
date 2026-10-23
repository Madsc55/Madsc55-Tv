"""Exercise measured workflow bodies offline, including real timeout snapshots."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from madsc.parity_consumer_cli import CONSUMERS, DIAGNOSTICS, run_consumer
from madsc.parity_workflow_readiness import preflight_replacement_execution
from tests.test_parity_input_receipt import ROOT, run_body, steps_for
from tests.test_parity_workflow_preflight import pair_for

WORKFLOWS = {'k1': '.github/workflows/madsc-01-guvenlik.yml',
             'k4': '.github/workflows/madsc-04-yedek.yml',
             'k5': '.github/workflows/madsc-05-bakim.yml'}


def prepare(root, key):
    source = root / CONSUMERS[key][0]
    source.parent.mkdir(parents=True, exist_ok=True)
    payload = {'k1': (ROOT / 'config/shadow_manifest.json').read_bytes(),
               'k4': b'isolated restore sample',
               'k5': b'#EXTM3U\n#EXTINF:-1,Fixture\nhttps://example.org/fixture.m3u8\n'}[key]
    source.write_bytes(payload)
    (root / 'reports').mkdir(exist_ok=True)
    return source


def environment():
    return {**os.environ, 'PYTHONPATH': str(ROOT), 'RUN_ID': '123', 'COMMIT_SHA': 'a'*40,
            'GITHUB_REPOSITORY': 'Madsc55/Madsc55-Tv', 'GITHUB_REF_NAME': 'main',
            'GITHUB_RUN_ID': '123', 'GITHUB_SHA': 'a'*40}


class ParityConsumerTests(unittest.TestCase):
    def execute(self, body, root):
        return subprocess.run(['bash', '-e', '-o', 'pipefail', '-c',
                               body.replace('${{ inputs.allow_parity_evidence }}', 'true')],
                              cwd=root, env=environment(), capture_output=True, timeout=5)

    def test_three_real_workflow_timeout_bodies_keep_failure_and_publishable_manifest(self):
        for key, workflow in WORKFLOWS.items():
            with self.subTest(consumer=key), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = prepare(root, key)
                if key == 'k4':
                    # The real K4 workflow creates its fixture exclusively.
                    # Starting with an existing file correctly trips K1's
                    # no-overwrite guard before the timeout consumer runs.
                    source.unlink()
                steps = steps_for(workflow)
                consumer = next(step for step in steps if 'id: parity_consumer' in step)
                result = self.execute(run_body(consumer).replace('--timeout-seconds 120',
                                                                '--timeout-seconds 0.000001'), root)
                self.assertEqual(result.returncode, 124, result.stderr)
                snapshot = json.loads((root / 'reports/madsc-parity-snapshot.json').read_text())
                self.assertTrue(snapshot['timed_out'])
                self.assertEqual(snapshot['exit_code'], 124)
                self.assertEqual(set(snapshot['outputs']), set(DIAGNOSTICS))
                for label, relative in DIAGNOSTICS.items():
                    self.assertEqual(snapshot['outputs'][label], hashlib.sha256((root / relative).read_bytes()).hexdigest())
                # On failure the success-snapshot step is skipped by GitHub's
                # implicit success() condition. Run the actual always-chain bodies.
                for identity in ('parity_input_before', 'parity_manifest', 'parity_input_after'):
                    step = next(step for step in steps if f'id: {identity}' in step)
                    measured = self.execute(run_body(step), root)
                    self.assertEqual(measured.returncode, 0, measured.stderr)
                manifest = json.loads((root / 'reports/madsc-parity-evidence.json').read_text())
                self.assertEqual(manifest['snapshot'], snapshot)
                self.assertEqual(manifest['input_sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
                origin = pair_for(workflow)['replacement']
                origin.update(snapshot=snapshot, input_sha256=manifest['input_sha256'])
                checked = preflight_replacement_execution(ROOT, origin)
                self.assertEqual(checked['snapshot_observation_mode'], 'failure_diagnostics')
                self.assertIsNone(checked['contracted_output_sha256'])
                self.assertFalse(checked['behavioral_parity_accepted'])
                # Real consumer failure stays failure even if evidence steps pass.
                self.assertNotEqual(result.returncode, 0)

    def test_real_nonzero_without_normal_output_keeps_stderr_and_failure_snapshot(self):
        for key in ('k1', 'k5'):
            with self.subTest(consumer=key), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = prepare(root, key)
                source.write_bytes(b'\xff')
                with patch.dict(os.environ, environment()):
                    code = run_consumer(key, root=root)
                self.assertNotEqual(code, 0)
                snapshot = json.loads((root / 'reports/madsc-parity-snapshot.json').read_text())
                self.assertFalse(snapshot['timed_out'])
                self.assertEqual(snapshot['exit_code'], code)
                self.assertTrue((root / DIAGNOSTICS['process_stderr']).read_bytes())
                if key == 'k5':
                    self.assertFalse((root / CONSUMERS[key][1]).exists())

    def test_normal_child_124_has_false_timeout_through_real_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            (root / 'src').mkdir()
            (root / 'src/__init__.py').write_text('')
            (root / 'src/madsc_guard.py').write_text("import sys; print('measured stderr',file=sys.stderr); raise SystemExit(124)")
            result = self.execute('python -m madsc.parity_consumer_cli --consumer k1 --timeout-seconds 2', root)
            self.assertEqual(result.returncode, 124)
            outcome = json.loads((root / DIAGNOSTICS['process_outcome']).read_text())
            self.assertFalse(outcome['timed_out'])
            self.assertIn(b'measured stderr', (root / DIAGNOSTICS['process_stderr']).read_bytes())

    def test_controlled_timeout_keeps_real_pre_timeout_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            (root / 'src').mkdir()
            (root / 'src/__init__.py').write_text('')
            (root / 'src/madsc_guard.py').write_text(
                "import os,time; os.write(2,b'before controlled timeout'); time.sleep(10)")
            result = self.execute('python -m madsc.parity_consumer_cli --consumer k1 --timeout-seconds .25', root)
            self.assertEqual(result.returncode, 124)
            snapshot = json.loads((root / 'reports/madsc-parity-snapshot.json').read_text())
            self.assertTrue(snapshot['timed_out'])
            self.assertEqual((root / DIAGNOSTICS['process_stderr']).read_bytes(), b'before controlled timeout')

    def test_existing_evidence_prevents_consumer_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            old = root / DIAGNOSTICS['process_stdout']
            old.write_bytes(b'previous evidence')
            with patch('madsc.parity_consumer_cli.observe_process') as execute:
                with self.assertRaises((ValueError, PermissionError)):
                    run_consumer('k1', root=root)
                execute.assert_not_called()
            self.assertEqual(old.read_bytes(), b'previous evidence')

    def test_writer_failure_cannot_replace_measured_consumer_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1').write_bytes(b'\xff')
            with patch.dict(os.environ, environment()), patch('madsc.parity_consumer_cli._exclusive_bytes', side_effect=OSError('disk fixture')):
                self.assertEqual(run_consumer('k1', root=root), 2)
            self.assertFalse((root / 'reports/madsc-parity-snapshot.json').exists())

    def test_failure_evidence_input_mutation_blocks_publication_chain(self):
        workflow = WORKFLOWS['k1']
        steps = steps_for(workflow)
        consumer = next(step for step in steps if 'id: parity_consumer' in step)
        before = next(step for step in steps if 'id: parity_input_before' in step)
        manifest = next(step for step in steps if 'id: parity_manifest' in step)
        after = next(step for step in steps if 'id: parity_input_after' in step)
        for mutation in ('before_manifest', 'after_manifest'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = prepare(root, 'k1')
                result = self.execute(run_body(consumer).replace('--timeout-seconds 120', '--timeout-seconds .000001'), root)
                self.assertEqual(result.returncode, 124)
                if mutation == 'before_manifest':
                    source.write_bytes(source.read_bytes() + b'changed')
                    self.assertNotEqual(self.execute(run_body(before), root).returncode, 0)
                    self.assertFalse((root / 'reports/madsc-parity-evidence.json').exists())
                else:
                    self.assertEqual(self.execute(run_body(before), root).returncode, 0)
                    self.assertEqual(self.execute(run_body(manifest), root).returncode, 0)
                    source.write_bytes(source.read_bytes() + b'changed')
                    self.assertNotEqual(self.execute(run_body(after), root).returncode, 0)
                # Publication's source condition requires the after-check success;
                # diagnostic logs remain usable even when the manifest is blocked.
                self.assertTrue((root / DIAGNOSTICS['process_outcome']).exists())

    def test_failure_preflight_rejects_missing_diagnostics_and_success_role_substitution(self):
        origin = pair_for(WORKFLOWS['k4'])['replacement']
        origin['snapshot'].update(exit_code=23, timed_out=False)
        with self.assertRaisesRegex(ValueError, 'diagnostic'):
            preflight_replacement_execution(ROOT, origin)
        origin['snapshot']['outputs'] = {label: 'd'*64 for label in DIAGNOSTICS}
        del origin['snapshot']['outputs']['process_stderr']
        with self.assertRaisesRegex(ValueError, 'diagnostic'):
            preflight_replacement_execution(ROOT, origin)
