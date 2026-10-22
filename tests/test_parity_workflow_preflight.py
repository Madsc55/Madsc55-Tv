"""Bind comparison preflight to actual reviewed source and output roles."""
import copy
import io
import subprocess
import sys
import zipfile
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from madsc.legacy_parity_cli import run
from madsc.legacy_parity_evidence import compare_provenance_bound_pair, reconcile_legacy_scope
from madsc.legacy_pair_artifact import verify_provenance_pair_artifacts
from madsc.github_legacy_pair_client import verify_provenance_pair_api
from madsc.parity_workflow_readiness import (FILE_DATAFLOW_CONTRACTS,
    audit_parity_workflow_readiness, preflight_replacement_execution)
from tests.test_legacy_pair_artifact import execution, archive_for

ROOT = Path(__file__).resolve().parents[1]
LEGACY = '.github/workflows/example.yml'
BLOB = '1' * 40


def pair_for(workflow):
    source = (ROOT / workflow).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
    contract = FILE_DATAFLOW_CONTRACTS[workflow]
    label = contract['snapshot_output'].removeprefix('--output ').split('=', 1)[0]
    pair = {
        'legacy': execution('Madsc55/madsc-tv', 'madsc/bes-sistem-toplu-birlestirme',
                            LEGACY, BLOB, 11, 21),
        'replacement': execution('Madsc55/Madsc55-Tv', 'main', workflow, blob, 12, 22),
    }
    for role in pair.values():
        role['snapshot']['outputs'] = {label: 'd' * 64}
    return pair


class ParityWorkflowPreflightTests(unittest.TestCase):
    def test_three_source_bound_contracts_flow_through_artifact_verification(self):
        for workflow in FILE_DATAFLOW_CONTRACTS:
            with self.subTest(workflow=workflow):
                pair = pair_for(workflow)
                legacy, replacement = [archive_for(pair[role]) for role in ('legacy', 'replacement')]
                report = verify_provenance_pair_artifacts(
                    LEGACY, BLOB, pair, legacy, replacement, replacement_workflow_root=ROOT)
                self.assertTrue(report['replacement_workflow_contract_checked'])
                checked = report['replacement_static_preflight']
                self.assertEqual(checked['workflow_blob_sha'], pair['replacement']['workflow_blob_sha'])
                self.assertTrue(checked['static_workflow_contract_checked'])
                self.assertEqual(checked['contracted_output_sha256'], 'd' * 64)
                self.assertTrue(checked['file_binding']['input_path'])
                self.assertTrue(checked['file_binding']['output_path'])
                self.assertFalse(checked['input_bytes_independently_verified'])
                self.assertFalse(checked['runtime_origin_verified'])
                self.assertFalse(report['behavioral_parity_accepted'])

    def test_wrong_blob_missing_output_and_blocked_workflow_fail_before_api(self):
        workflow = '.github/workflows/madsc-01-guvenlik.yml'
        cases = []
        pair = pair_for(workflow)
        pair['replacement']['workflow_blob_sha'] = 'f' * 40
        cases.append(pair)
        pair = pair_for(workflow)
        pair['replacement']['snapshot']['outputs'] = {'wrong-label': 'd' * 64}
        cases.append(pair)
        for path in ('.github/workflows/madsc-02-kesif.yml',
                     '.github/workflows/madsc-03-kanal-test.yml'):
            pair = pair_for(workflow)
            pair['replacement']['workflow_path'] = path
            cases.append(pair)
        for pair in cases:
            with self.subTest(workflow=pair['replacement']['workflow_path']):
                fetch = Mock()
                with self.assertRaises(ValueError):
                    verify_provenance_pair_api(LEGACY, BLOB, pair, fetch=fetch,
                                              replacement_workflow_root=ROOT)
                fetch.assert_not_called()

    def test_source_drift_cannot_reuse_previous_reviewed_blob(self):
        workflow = '.github/workflows/madsc-01-guvenlik.yml'
        pair = pair_for(workflow)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = audit_parity_workflow_readiness(ROOT)
            for row in report['rows']:
                path = root / row['workflow_path']
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / row['workflow_path']).read_bytes())
            with (root / workflow).open('a') as stream:
                stream.write('\n# changed source after prior review\n')
            with self.assertRaises(ValueError):
                preflight_replacement_execution(root, pair['replacement'])

    def test_cli_provenance_batch_uses_preflight_without_granting_acceptance(self):
        inventory = json.loads((ROOT / 'docs/LEGACY_SOURCE_SCOPE.json').read_text())
        path = reconcile_legacy_scope(inventory)['legacy_paths'][0]
        blob = next(row['git_blob_sha'] for row in inventory['workflows'] if row['path'] == path)
        pair = pair_for('.github/workflows/madsc-01-guvenlik.yml')
        pair['legacy']['workflow_path'] = path
        pair['legacy']['workflow_blob_sha'] = blob
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'pairs.json'
            source.write_text(json.dumps({'schema': 'madsc-legacy-provenance-pairs-v1',
                                          'pairs': {path: pair}}))
            report = run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', source, root / 'result.json',
                         replacement_workflow_root=ROOT)
            self.assertEqual(report['replacement_workflow_contracts_checked'], 1)
            self.assertEqual(report['total'], 92)
            self.assertEqual(report['behavioral_parity_accepted'], 0)
            self.assertEqual(report['independent_origins_api_verified'], 0)
            pair['replacement']['workflow_blob_sha'] = 'e' * 40
            source.write_text(json.dumps({'schema': 'madsc-legacy-provenance-pairs-v1',
                                          'pairs': {path: pair}}))
            with self.assertRaises(ValueError):
                run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', source, root / 'rejected.json',
                    replacement_workflow_root=ROOT)
            self.assertFalse((root / 'rejected.json').exists())

    def test_unrequested_preflight_is_explicitly_unchecked(self):
        pair = pair_for('.github/workflows/madsc-01-guvenlik.yml')
        report = compare_provenance_bound_pair(LEGACY, BLOB, pair)
        self.assertFalse(report['replacement_workflow_contract_checked'])
        self.assertIsNone(report['replacement_static_preflight'])
        self.assertFalse(report['behavioral_parity_accepted'])

    def test_real_k1_consumer_snapshot_manifest_archive_and_preflight_chain(self):
        from madsc.parity_manifest_cli import produce_from_files
        from madsc.parity_snapshot_writer import write_execution_snapshot
        workflow = '.github/workflows/madsc-01-guvenlik.yml'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            actual_input = root / 'config' / 'shadow_manifest.json'
            actual_input.parent.mkdir()
            actual_input.write_bytes((ROOT / 'config/shadow_manifest.json').read_bytes())
            measured = subprocess.run(
                [sys.executable, '-m', 'src.madsc_guard', str(actual_input)],
                cwd=ROOT, capture_output=True, timeout=5, check=True)
            (root / 'reports').mkdir()
            output = root / 'reports/k1-guard.txt'
            output.write_bytes(measured.stdout)
            write_execution_snapshot(root, exit_code=measured.returncode, timed_out=False,
                                     outputs=[('guard', output)], side_effects=[])
            produce_from_files(input_path=actual_input,
                snapshot_path=root / 'reports/madsc-parity-snapshot.json', output_root=root,
                repository='Madsc55/Madsc55-Tv', branch='main', workflow_path=workflow,
                run_id=12, head_sha='b' * 40)
            manifest_path = root / 'reports/madsc-parity-evidence.json'
            manifest = json.loads(manifest_path.read_text())
            pair = pair_for(workflow)
            # The legacy side is a fixture here, never a claimed legacy execution.
            for origin in pair.values():
                origin['input_sha256'] = manifest['input_sha256']
                origin['snapshot'] = copy.deepcopy(manifest['snapshot'])
            legacy = archive_for(pair['legacy'])
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as bundle:
                bundle.write(manifest_path, 'madsc-parity-evidence.json')
            replacement = buffer.getvalue()
            pair['replacement']['artifact']['sha256'] = hashlib.sha256(replacement).hexdigest()
            verified = verify_provenance_pair_artifacts(LEGACY, BLOB, pair, legacy, replacement,
                                                       replacement_workflow_root=ROOT)
            self.assertEqual(verified['replacement_static_preflight']['contracted_output_sha256'],
                             hashlib.sha256(measured.stdout).hexdigest())
            self.assertTrue(verified['snapshot_fields_match'])
            self.assertFalse(verified['behavioral_parity_accepted'])
            self.assertFalse(verified['provenance_verified'])

    def test_api_origin_checks_preserve_separate_static_preflight_status(self):
        from tests.test_github_legacy_pair_client import GithubLegacyPairClientTests
        fixture = GithubLegacyPairClientTests()
        fixture.pair = pair_for('.github/workflows/madsc-01-guvenlik.yml')
        fetch, calls = fixture.fetcher()
        report = verify_provenance_pair_api(LEGACY, BLOB, fixture.pair, fetch=fetch,
                                           replacement_workflow_root=ROOT)
        self.assertEqual(len(calls), 6)
        self.assertTrue(report['independent_origin_api_verified'])
        self.assertTrue(report['replacement_workflow_contract_checked'])
        self.assertFalse(report['replacement_static_preflight']['runtime_origin_verified'])
        self.assertFalse(report['behavioral_parity_accepted'])
