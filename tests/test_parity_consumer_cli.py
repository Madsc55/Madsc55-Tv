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
from madsc.parity_snapshot_cli import main as snapshot_main
from madsc.parity_workspace_guard import RECEIPT_PATH
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
    def test_consumer_command_drift_is_rejected_before_process_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            drifted = dict(CONSUMERS)
            source, output, arguments = drifted['k1']
            drifted['k1'] = (source, output, [*arguments, '--unexpected'])
            with patch('madsc.parity_consumer_cli.CONSUMERS', drifted), \
                 patch('madsc.parity_consumer_cli.observe_process') as execute:
                with self.assertRaises(PermissionError):
                    run_consumer('k1', root=root)
                execute.assert_not_called()

    def test_consumer_module_cannot_be_shadowed_from_workspace_cwd(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            (root / 'src').mkdir()
            (root / 'src/__init__.py').write_text('')
            (root / 'src/madsc_guard.py').write_text(
                "print('UNTRUSTED CWD SHADOW'); raise SystemExit(97)")
            code = run_consumer('k1', root=root, timeout_seconds=5)
            self.assertEqual(code, 0)
            output = (root / CONSUMERS['k1'][1]).read_bytes()
            self.assertIn(b'K1 read-only output gate: PASS', output)
            self.assertNotIn(b'UNTRUSTED CWD SHADOW', output)

    def test_three_real_consumers_allow_only_their_declared_output(self):
        for key in CONSUMERS:
            with self.subTest(consumer=key), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                prepare(root, key)
                with patch.dict(os.environ, environment()):
                    code = run_consumer(key, root=root, timeout_seconds=5)
                self.assertEqual(code, 0)
                self.assertTrue((root / CONSUMERS[key][1]).is_file())
                self.assertTrue((root / DIAGNOSTICS['process_outcome']).is_file())
                receipt = json.loads((root / RECEIPT_PATH).read_text())
                self.assertEqual(receipt['consumer'], key)
                self.assertFalse(receipt['external_effects_verified'])
                self.assertFalse(receipt['independent_execution_verified'])
                self.assertFalse(receipt['behavioral_parity_accepted'])
                expected = [] if key == 'k1' else [
                    'reports', CONSUMERS[key][1]]
                self.assertEqual(receipt['observed_changes'], expected)
                label = {'k1': 'guard', 'k4': 'restore', 'k5': 'candidates'}[key]
                self.assertEqual(snapshot_main([
                    '--exit-code', '0', '--output',
                    f'{label}={root / CONSUMERS[key][1]}', '--side-effect',
                    f'workspace_effect_receipt={root / RECEIPT_PATH}',
                    '--output-root', str(root)]), 0)
                snapshot = json.loads((root / 'reports/madsc-parity-snapshot.json').read_text())
                self.assertEqual(set(snapshot['side_effects']),
                                 {'workspace_effect_receipt'})

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
            fixture = dict(CONSUMERS)
            source, output, _ = fixture['k1']
            fixture['k1'] = (source, output, ['-m', 'tests._parity_child_fixture', 'exit-124'])
            with patch('madsc.parity_consumer_cli.CONSUMERS', fixture), \
                 patch('madsc.parity_consumer_cli.authorize_parity_consumer_process', return_value=object()), \
                 patch('madsc.parity_consumer_cli.parity_process_environment', return_value=dict(os.environ)), \
                 patch('madsc.parity_process.validate_parity_process_capability'):
                code = run_consumer('k1', root=root, timeout_seconds=2)
            self.assertEqual(code, 124)
            outcome = json.loads((root / DIAGNOSTICS['process_outcome']).read_text())
            self.assertFalse(outcome['timed_out'])
            self.assertIn(b'measured stderr', (root / DIAGNOSTICS['process_stderr']).read_bytes())

    def test_controlled_timeout_keeps_real_pre_timeout_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            fixture = dict(CONSUMERS)
            source, output, _ = fixture['k1']
            fixture['k1'] = (source, output, ['-m', 'tests._parity_child_fixture', 'timeout'])
            with patch('madsc.parity_consumer_cli.CONSUMERS', fixture), \
                 patch('madsc.parity_consumer_cli.authorize_parity_consumer_process', return_value=object()), \
                 patch('madsc.parity_consumer_cli.parity_process_environment', return_value=dict(os.environ)), \
                 patch('madsc.parity_process.validate_parity_process_capability'):
                code = run_consumer('k1', root=root, timeout_seconds=.25)
            self.assertEqual(code, 124)
            snapshot = json.loads((root / 'reports/madsc-parity-snapshot.json').read_text())
            self.assertTrue(snapshot['timed_out'])
            self.assertEqual((root / DIAGNOSTICS['process_stderr']).read_bytes(), b'before controlled timeout')
            self.assertFalse((root / RECEIPT_PATH).exists())

    def test_unexpected_child_write_turns_success_into_measured_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare(root, 'k1')
            fixture = dict(CONSUMERS)
            source, output, _ = fixture['k1']
            fixture['k1'] = (source, output,
                             ['-m', 'tests._parity_child_fixture', 'unexpected-write'])
            with patch('madsc.parity_consumer_cli.CONSUMERS', fixture), \
                 patch('madsc.parity_consumer_cli.authorize_parity_consumer_process', return_value=object()), \
                 patch('madsc.parity_consumer_cli.parity_process_environment', return_value=dict(os.environ)), \
                 patch('madsc.parity_process.validate_parity_process_capability'):
                code = run_consumer('k1', root=root, timeout_seconds=2)
            self.assertEqual(code, 125)
            self.assertFalse((root / output).exists())
            self.assertTrue((root / 'unexpected-child-write.txt').exists())
            stderr = (root / DIAGNOSTICS['process_stderr']).read_text()
            self.assertIn('Workspace side-effect rejected', stderr)
            self.assertFalse((root / RECEIPT_PATH).exists())
            snapshot = json.loads((root / 'reports/madsc-parity-snapshot.json').read_text())
            self.assertEqual(snapshot['exit_code'], 125)

    def test_rewritten_then_restored_input_identity_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = prepare(root, 'k1')
            original = source.read_bytes()
            fixture = dict(CONSUMERS)
            source_name, output, _ = fixture['k1']
            fixture['k1'] = (source_name, output,
                             ['-m', 'tests._parity_child_fixture', 'rewrite-revert', source_name])
            with patch('madsc.parity_consumer_cli.CONSUMERS', fixture), \
                 patch('madsc.parity_consumer_cli.authorize_parity_consumer_process', return_value=object()), \
                 patch('madsc.parity_consumer_cli.parity_process_environment', return_value=dict(os.environ)), \
                 patch('madsc.parity_process.validate_parity_process_capability'):
                code = run_consumer('k1', root=root, timeout_seconds=2)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(code, 125)
            self.assertFalse((root / output).exists())
            self.assertIn(b'config/shadow_manifest.json',
                          (root / DIAGNOSTICS['process_stderr']).read_bytes())
            self.assertFalse((root / RECEIPT_PATH).exists())

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
