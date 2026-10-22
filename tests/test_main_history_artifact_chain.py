"""Real local bytes through the main-K2 source contract; API replies are fixtures."""
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from madsc.github_history_client import verify_live_github_origin
from madsc.history_artifact_download import download_verified_history_artifact
from madsc.history_real_source_publish import publish_source
from madsc.history_verified_pipeline import produce_verified_history
from madsc.workflow_consolidation import AUXILIARY, MAIN, contract_gate

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Madsc55/Madsc55-Tv'
MAIN_SOURCE = '.github/workflows/madsc-02-kesif.yml'
A, B = 'a' * 40, 'b' * 40
FILES = {'gecmis.json': b'{"history":{}}',
         'ana_liste_test_gecmisi.json': b'{"channels":{}}'}


class MainHistoryArtifactChainTests(unittest.TestCase):
    def run_chain(self, root, *, artifact_name='madsc-k2-history-source',
                  source_path=MAIN_SOURCE, corrupt=False):
        source = root / 'independent-input'
        source.mkdir()
        for name, raw in FILES.items():
            (source / name).write_bytes(raw)
        published = root / 'published'
        publication = publish_source(source, published)
        bundle = io.BytesIO()
        with zipfile.ZipFile(bundle, 'w') as archive:
            for name in FILES:
                raw = (published / name).read_bytes()
                archive.writestr(name, raw + b' ' if corrupt else raw)
        manifest = root / 'manifest.json'
        manifest.write_text(json.dumps({
            'schema': 1, 'mode': 'VERIFIED_SOURCE', 'source_run_id': '123',
            'source_commit_sha': A, 'production_writes': False,
            'hashes': publication['source_sha256']}))
        calls = []
        def fetch(url, *, token):
            calls.append(url)
            if '/artifacts?' in url:
                return {'total_count': 1, 'artifacts': [{
                    'id': 456, 'name': artifact_name, 'expired': False,
                    'workflow_run': {'id': 123, 'head_sha': A}}]}
            if '/compare/' in url:
                return {'status': 'ahead'}
            return {'id': 123, 'head_sha': A, 'repository': {'full_name': REPO},
                    'head_repository': {'full_name': REPO}, 'head_branch': 'main',
                    'path': source_path, 'status': 'completed',
                    'conclusion': 'success', 'event': 'workflow_dispatch'}
        def verify(manifest, **kwargs):
            return verify_live_github_origin(manifest, fetch=fetch, **kwargs)
        def download(**kwargs):
            def opener(request, timeout):
                self.assertEqual(request.full_url,
                    f'https://api.github.com/repos/{REPO}/actions/artifacts/456/zip')
                return io.BytesIO(bundle.getvalue())
            return download_verified_history_artifact(opener=opener, **kwargs)
        result = produce_verified_history(manifest, root / 'handoff.json', current_sha=B,
            run_id='789', token='fixture', source_workflow_path=MAIN_SOURCE,
            verify_origin=verify, download=download)
        self.assertEqual(len(calls), 3)
        for name, raw in FILES.items():
            self.assertEqual((source / name).read_bytes(), raw)
            self.assertEqual((published / name).read_bytes(), raw)
        return result

    def test_main_k2_publish_zip_origin_download_and_handoff_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = self.run_chain(root)
            self.assertFalse(result['production_ready'])
            self.assertEqual(result['verified_artifact_id'], 456)
            handoff = json.loads((root / 'handoff.json').read_text())
            self.assertEqual(handoff['run_id'], '789')
            self.assertEqual(handoff['commit_sha'], B)

    def test_generic_bundle_wrong_origin_and_changed_bytes_produce_no_handoff(self):
        for change in ({'artifact_name': 'madsc-k2-isolated-evidence'},
                       {'source_path': '.github/workflows/madsc-05-bakim.yml'},
                       {'corrupt': True}):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                with self.assertRaises(ValueError):
                    self.run_chain(root, **change)
                self.assertFalse((root / 'handoff.json').exists())

    def test_unapproved_source_rejected_before_external_call(self):
        calls = []
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'Unapproved'):
                produce_verified_history(Path(tmp) / 'missing.json', Path(tmp) / 'out.json',
                    current_sha=B, run_id='789', token='fixture',
                    source_workflow_path='.github/workflows/madsc-05-bakim.yml',
                    verify_origin=lambda *a, **k: calls.append(k))
        self.assertEqual(calls, [])

    def test_all_nine_compatibility_artifact_contracts_and_opt_in_preserved(self):
        folder = ROOT / '.github/workflows'
        for source, (stages, _, _) in AUXILIARY.items():
            if source == '01-guvenlik.yml':
                continue
            body = (folder / MAIN[stages.split('+')[-1]]).read_text()
            block = body.split('      - name: Yardımcı paket sözleşmesini koru — ' + source + '\n')[1].split('      - name:', 1)[0]
            original = (folder / source).read_text()
            upload = original[original.index('        with:', original.index('uses: actions/upload-artifact@')):]
            self.assertIn(upload.rstrip(), block)
            self.assertIn('inputs.allow_', block)
        k2 = (folder / MAIN['K2']).read_text()
        publisher = k2.split('      - name: Bağımsız geçmiş çiftini kaynak paketi için doğrula')[1].split('      - name:', 1)[0]
        self.assertIn('inputs.allow_history_source_publish == true', publisher)
        self.assertNotIn('inputs.allow_verified_history', publisher)
        self.assertIn('--source-workflow "$HISTORY_SOURCE_WORKFLOW"', k2)
        self.assertTrue(contract_gate(ROOT)['pass'])
        self.assertEqual(contract_gate(ROOT)['static_gaps_total'], 0)

    def test_removed_source_artifact_identity_blocks_contract_gate(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / '.github/workflows', root / '.github/workflows')
            target = root / '.github/workflows' / MAIN['K2']
            target.write_text(target.read_text().replace(
                'name: madsc-k2-history-source', 'name: renamed-history-bundle'))
            gate = contract_gate(root)
            self.assertFalse(gate['pass'])
            self.assertEqual(gate['blocking_contract_gaps'], [{
                'source': 'madsc-k2-real-history-source.yml', 'gaps': ['artifact_name']}])
