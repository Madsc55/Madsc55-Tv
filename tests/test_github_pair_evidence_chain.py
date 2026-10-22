"""The existing batch CLI binds independent API records to real local ZIP bytes."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from urllib.request import Request

from madsc.github_legacy_pair_client import (
    _ArtifactRedirectHandler, download_execution_artifact,
    verify_provenance_pair_evidence)
from madsc.legacy_pair_artifact import MAX_ARCHIVE_BYTES
from madsc.legacy_parity_cli import run
from madsc.legacy_parity_evidence import reconcile_legacy_scope
from tests.test_legacy_pair_artifact import execution, archive_for

ROOT = Path(__file__).resolve().parents[1]


class GithubPairEvidenceChainTests(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads((ROOT / 'docs/LEGACY_SOURCE_SCOPE.json').read_text())
        self.path = reconcile_legacy_scope(self.inventory)['legacy_paths'][0]
        self.blob = next(r['git_blob_sha'] for r in self.inventory['workflows']
                         if r['path'] == self.path)
        self.pair = {
            'legacy': execution('Madsc55/madsc-tv', 'madsc/bes-sistem-toplu-birlestirme',
                               self.path, self.blob, 11, 21),
            'replacement': execution('Madsc55/Madsc55-Tv', 'main',
                '.github/workflows/madsc-01-guvenlik.yml', '2' * 40, 12, 22)}
        self.archives = {role: archive_for(origin) for role, origin in self.pair.items()}
        self.api_calls, self.download_calls = [], []

    def fetch(self, url, *, token):
        self.api_calls.append(url)
        role = 'legacy' if '/Madsc55/madsc-tv/' in url else 'replacement'
        origin = self.pair[role]
        if '/artifacts?' in url:
            return {'total_count': 1, 'artifacts': [{
                'id': origin['artifact']['id'], 'name': origin['artifact']['name'],
                'expired': False, 'digest': 'sha256:' + origin['artifact']['sha256'],
                'workflow_run': {'id': origin['run_id'], 'head_sha': origin['head_sha']}}]}
        if '/contents/' in url:
            return {'type': 'file', 'path': origin['workflow_path'],
                    'sha': origin['workflow_blob_sha']}
        return {'id': origin['run_id'], 'run_attempt': origin['run_attempt'],
                'head_sha': origin['head_sha'], 'head_branch': origin['branch'],
                'path': origin['workflow_path'], 'event': origin['event'],
                'status': 'completed', 'conclusion': origin['conclusion'],
                'repository': {'full_name': origin['repository']},
                'head_repository': {'full_name': origin['repository']}}

    def download(self, origin, *, token):
        self.download_calls.append(origin['artifact']['id'])
        role = 'legacy' if origin['repository'] == 'Madsc55/madsc-tv' else 'replacement'
        def opener(request, timeout):
            self.assertEqual(timeout, 30)
            self.assertEqual(request.full_url,
                f"https://api.github.com/repos/{origin['repository']}/actions/artifacts/{origin['artifact']['id']}/zip")
            return io.BytesIO(self.archives[role])
        return download_execution_artifact(origin, token=token, opener=opener)

    def cli(self, root, **kwargs):
        (root / 'inventory.json').write_text(json.dumps(self.inventory))
        (root / 'pairs.json').write_text(json.dumps({
            'schema': 'madsc-legacy-provenance-pairs-v1', 'pairs': {self.path: self.pair}}))
        return run(root / 'inventory.json', root / 'pairs.json', root / 'report.json',
                   fetch=self.fetch, download=self.download, **kwargs)

    def test_existing_batch_cli_checks_six_api_records_and_both_zip_manifests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.cli(root, verify_github_artifacts=True, token='fixture')
            self.assertEqual(len(self.api_calls), 6)
            self.assertEqual(self.download_calls, [21, 22])
            proof = result['github_artifact_verification']['proofs'][self.path]
            self.assertTrue(proof['api_bound_artifact_bytes_verified'])
            self.assertTrue(proof['same_input_artifacts_verified'])
            self.assertEqual(result['missing_pairs'], 91)
            self.assertEqual(result['behavioral_parity_accepted'], 0)
            self.assertFalse(proof['production_ready'])
            self.assertEqual(json.loads((root / 'report.json').read_text()), result)

    def test_default_batch_mode_does_not_call_api_or_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.cli(Path(tmp))
            self.assertNotIn('github_artifact_verification', result)
        self.assertEqual(self.api_calls, [])
        self.assertEqual(self.download_calls, [])

    def test_corrupt_zip_or_wrong_api_origin_never_writes_report(self):
        for problem in ('zip', 'api'):
            with self.subTest(problem=problem), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                if problem == 'zip':
                    self.archives['replacement'] += b'changed'
                else:
                    self.archives['replacement'] = archive_for(self.pair['replacement'])
                    original_fetch = self.fetch
                    def bad_fetch(url, **kwargs):
                        record = original_fetch(url, **kwargs)
                        if '/contents/' in url:
                            record['sha'] = 'f' * 40
                        return record
                    self.fetch = bad_fetch
                    self.download_calls.clear()
                with self.assertRaises(ValueError):
                    self.cli(root, verify_github_artifacts=True, token='fixture')
                self.assertFalse((root / 'report.json').exists())
                if problem == 'api':
                    self.assertEqual(self.download_calls, [])

    def test_k1_and_missing_token_reject_before_external_reads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                self.cli(root, verify_github_artifacts=True)
            with self.assertRaises(PermissionError):
                run(root / 'inventory.json', root / 'pairs.json', root / 'playlist.m3u8',
                    verify_github_artifacts=True, token='fixture', fetch=self.fetch,
                    download=self.download)
        self.assertEqual(self.api_calls, [])
        self.assertEqual(self.download_calls, [])

    def test_downloader_rejects_oversize_and_invalid_identity(self):
        observed_limits = []
        class LargeResponse(io.BytesIO):
            def read(self, limit):
                observed_limits.append(limit)
                return b'x' * limit
        with self.assertRaisesRegex(ValueError, 'size'):
            download_execution_artifact(self.pair['legacy'], token='fixture',
                opener=lambda *a, **k: LargeResponse())
        self.assertEqual(observed_limits, [MAX_ARCHIVE_BYTES + 1])
        invalid = copy.deepcopy(self.pair['legacy'])
        invalid['artifact']['id'] = True
        with self.assertRaises(ValueError):
            download_execution_artifact(invalid, token='fixture',
                opener=lambda *a, **k: self.fail('Invalid identity reached network'))

    def test_storage_redirect_strips_token_and_rejects_http(self):
        handler = _ArtifactRedirectHandler()
        request = Request('https://api.github.com/repos/example/artifacts/1/zip',
                          headers={'Authorization': 'Bearer fixture'})
        redirected = handler.redirect_request(request, None, 302, '', {},
                                             'https://storage.example/signed.zip')
        self.assertIsNone(redirected.get_header('Authorization'))
        self.assertEqual(request.get_header('Authorization'), 'Bearer fixture')
        with self.assertRaises(ValueError):
            handler.redirect_request(request, None, 302, '', {}, 'http://storage.example/a')

    def test_opt_in_requires_pairs_instead_of_claiming_empty_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'inventory.json').write_text(json.dumps(self.inventory))
            (root / 'pairs.json').write_text(json.dumps({
                'schema': 'madsc-legacy-provenance-pairs-v1', 'pairs': {}}))
            with self.assertRaises(ValueError):
                run(root / 'inventory.json', root / 'pairs.json', root / 'report.json',
                    verify_github_artifacts=True, token='fixture', fetch=self.fetch)
            self.assertFalse((root / 'report.json').exists())
        self.assertEqual(self.api_calls, [])
