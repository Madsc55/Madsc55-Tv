"""Pre-execution digest receipts must bind the bytes used by the manifest."""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from madsc.parity_manifest_cli import produce_from_files
from madsc.parity_workflow_readiness import (FILE_DATAFLOW_CONTRACTS,
                                            audit_parity_workflow_readiness)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = 'reports/parity-input-before.sha256'


def run_body(step):
    match = re.search(r'^        run: \|\n((?:          .*\n?)*)', step, re.MULTILINE)
    if match:
        return '\n'.join(line[10:] for line in match.group(1).splitlines())
    match = re.search(r'^        run: (.+)$', step, re.MULTILINE)
    if not match:
        raise AssertionError('Expected a real workflow run body')
    return match.group(1)


def steps_for(path):
    text = (ROOT / path).read_text()
    return re.split(r'(?=^      - name: )', text, flags=re.MULTILINE)


class ParityInputReceiptTests(unittest.TestCase):
    def arguments(self, root):
        source = root / 'input'
        source.write_bytes(b'actual input')
        snapshot = root / 'snapshot.json'
        snapshot.write_text(json.dumps({'exit_code': 0, 'timed_out': False,
                                       'outputs': {'guard': 'd'*64}, 'side_effects': {}}))
        return dict(input_path=source, snapshot_path=snapshot, output_root=root,
                    repository='Madsc55/Madsc55-Tv', branch='main',
                    workflow_path='.github/workflows/madsc-01-guvenlik.yml',
                    run_id=123, head_sha='a'*40)

    def test_actual_digest_receipt_is_matched_to_manifest_payload(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            args = self.arguments(root)
            receipt = root / 'before.sha256'
            digest = hashlib.sha256(args['input_path'].read_bytes()).hexdigest()
            receipt.write_text(digest + '  ' + str(args['input_path']) + '\n')
            result = produce_from_files(**args, input_digest_receipt=receipt)
            self.assertTrue(result['input_digest_receipt_matched'])
            manifest = json.loads((root / result['relative_path']).read_text())
            self.assertEqual(manifest['input_sha256'], digest)
            self.assertFalse(result['behavioral_parity_accepted'])

    def test_wrong_digest_path_and_malformed_receipt_never_create_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            args = self.arguments(root)
            digest = hashlib.sha256(args['input_path'].read_bytes()).hexdigest()
            record = digest + '  ' + str(args['input_path']) + '\n'
            receipt = root / 'before.sha256'
            invalid = [record.replace(digest, 'f'*64), record.replace(str(args['input_path']), 'other'),
                       record + record, record.rstrip('\n'), record.replace('  ', ' *', 1),
                       record.replace(digest, digest.upper())]
            for value in invalid:
                receipt.write_text(value)
                with self.subTest(receipt=value), self.assertRaises(ValueError):
                    produce_from_files(**args, input_digest_receipt=receipt)
                self.assertFalse((root / 'reports').exists())

    def test_workflow_bodies_stop_changed_input_and_bind_three_real_consumers(self):
        for path, contract in FILE_DATAFLOW_CONTRACTS.items():
            steps = steps_for(path)
            consumer = next(step for step in steps if contract['consumer'] in step)
            snapshot_steps = [step for step in steps
                              if 'run: python -m madsc.parity_snapshot_cli --exit-code 0 ' in step]
            self.assertEqual(len(snapshot_steps), 1)
            snapshot = snapshot_steps[0]
            manifest = next(step for step in steps if 'python -m madsc.parity_manifest_cli' in step)
            checks = [step for step in steps if 'run: sha256sum --check --status ' + RECEIPT in step]
            self.assertEqual(len(checks), 2)
            self.assertIn('--input-digest-receipt ' + RECEIPT, run_body(manifest))
            bodies = [run_body(step) for step in (consumer, snapshot, checks[0], manifest, checks[1])]
            input_relative = contract['manifest_input'].removeprefix('--input ')
            for scenario in ('stable', 'changed_after_consumer', 'changed_after_precheck', 'changed_after_manifest', 'opt_out'):
                with self.subTest(workflow=path, scenario=scenario), tempfile.TemporaryDirectory() as folder:
                    root = Path(folder)
                    (root / 'reports').mkdir()
                    source = root / input_relative
                    source.parent.mkdir(parents=True, exist_ok=True)
                    if path.endswith('madsc-01-guvenlik.yml'):
                        source.write_bytes((ROOT / input_relative).read_bytes())
                    elif path.endswith('madsc-05-bakim.yml'):
                        source.write_text('#EXTM3U\n#EXTINF:-1,Fixture\nhttps://example.org/fixture.m3u8\n')
                    env = {**os.environ, 'PYTHONPATH': str(ROOT), 'RUN_ID': '123', 'COMMIT_SHA': 'a'*40,
                           'GITHUB_REPOSITORY': 'Madsc55/Madsc55-Tv', 'GITHUB_REF_NAME': 'main',
                           'GITHUB_RUN_ID': '123', 'GITHUB_SHA': 'a'*40}
                    statuses = []
                    for index, body in enumerate(bodies):
                        if scenario == 'opt_out' and index > 0:
                            break
                        if ((scenario == 'changed_after_consumer' and index == 1)
                                or (scenario == 'changed_after_precheck' and index == 3)
                                or (scenario == 'changed_after_manifest' and index == 4)):
                            source.write_bytes(source.read_bytes() + b'changed input\n')
                        body = body.replace('${{ inputs.allow_parity_evidence }}',
                                            'false' if scenario == 'opt_out' else 'true')
                        result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', body], cwd=root,
                                                env=env, capture_output=True, text=True, timeout=10)
                        statuses.append(result.returncode)
                        if result.returncode:
                            break
                    published = root / 'reports/publish-simulation.txt'
                    if statuses == [0]*5:
                        published.write_text('local simulation only')
                    if scenario == 'stable':
                        self.assertEqual(statuses, [0]*5, result.stderr)
                        self.assertTrue(published.exists())
                        produced = json.loads((root / 'reports/madsc-parity-evidence.json').read_text())
                        self.assertEqual(produced['input_sha256'], hashlib.sha256(source.read_bytes()).hexdigest())
                    elif scenario == 'opt_out':
                        self.assertEqual(statuses, [0], result.stderr)
                        self.assertFalse((root / RECEIPT).exists())
                        self.assertFalse((root / 'reports/madsc-parity-evidence.json').exists())
                    else:
                        self.assertNotEqual(statuses[-1], 0)
                        self.assertFalse(published.exists())
                        self.assertEqual((root / 'reports/madsc-parity-evidence.json').exists(),
                                         scenario == 'changed_after_manifest')

    def test_readiness_requires_capture_checks_and_cli_receipt_binding(self):
        report = audit_parity_workflow_readiness(ROOT)
        self.assertEqual(report['input_digest_binding_contracts_complete'], 3)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for row in report['rows']:
                target = root / row['workflow_path']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / row['workflow_path']).read_bytes())
            k1 = root / '.github/workflows/madsc-01-guvenlik.yml'
            text = k1.read_text().replace('--input-digest-receipt ' + RECEIPT, '')
            k1.write_text(text)
            drifted = audit_parity_workflow_readiness(root)
            self.assertEqual(drifted['input_digest_binding_contracts_complete'], 2)
