"""Pair preparation must use current replacement sources, never cached readiness."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from madsc.legacy_parity_evidence import compare_provenance_bound_batch
from madsc.legacy_parity_cli import run

ROOT = Path(__file__).resolve().parents[1]


class PairReplacementContractTests(unittest.TestCase):
    def setUp(self):
        self.source = json.loads((ROOT / 'docs/LEGACY_SOURCE_SCOPE.json').read_text())

    def test_absent_root_never_claims_contracts_checked(self):
        report = compare_provenance_bound_batch(self.source, {})
        self.assertFalse(report['replacement_contract_catalog_checked'])
        self.assertIsNone(report['replacement_contract_catalog'])
        self.assertTrue(all(not row['pair_preparation']['replacement_contract_catalog_checked']
                            for row in report['rows']))

    def test_actual_five_sources_expose_three_isolated_and_two_external_contracts(self):
        report = compare_provenance_bound_batch(self.source, {}, replacement_workflow_root=ROOT)
        catalog = report['replacement_contract_catalog']
        self.assertTrue(report['replacement_contract_catalog_checked'])
        self.assertEqual(catalog['workflow_count'], 5)
        self.assertEqual(catalog['static_file_bindings_complete'], 3)
        self.assertEqual(catalog['external_or_live_input_blockers'], 2)
        for row in catalog['rows']:
            self.assertEqual(len(row['workflow_blob_sha']), 40)
            if row['static_file_binding_complete']:
                binding = row['declared_file_binding']
                self.assertTrue(all(binding.get(k) for k in
                                    ('consumer_command', 'input_path', 'output_label', 'output_path')))
            else:
                self.assertTrue(row['dataflow_blocker'])
            self.assertFalse(row['behavioral_parity_accepted'])
        self.assertTrue(all(row['pair_preparation']['replacement_mapping_review_required']
                            for row in report['rows']))
        self.assertEqual(report['behavioral_parity_accepted'], 0)

    def test_changed_source_changes_blob_and_cannot_keep_old_readiness(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / '.github/workflows', root / '.github/workflows')
            before = compare_provenance_bound_batch(self.source, {}, replacement_workflow_root=root)
            target = root / '.github/workflows/madsc-01-guvenlik.yml'
            target.write_text(target.read_text().replace('config/shadow_manifest.json', 'config/other.json'))
            after = compare_provenance_bound_batch(self.source, {}, replacement_workflow_root=root)
            key = '.github/workflows/madsc-01-guvenlik.yml'
            a = next(row for row in before['replacement_contract_catalog']['rows'] if row['workflow_path'] == key)
            b = next(row for row in after['replacement_contract_catalog']['rows'] if row['workflow_path'] == key)
            self.assertNotEqual(a['workflow_blob_sha'], b['workflow_blob_sha'])
            self.assertFalse(b['static_file_binding_complete'])
            self.assertFalse(after['production_ready'])

    def test_missing_source_fails_before_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pairs = root / 'pairs.json'
            pairs.write_text(json.dumps({'schema': 'madsc-legacy-provenance-pairs-v1', 'pairs': {}}))
            output = root / 'report.json'
            with self.assertRaises((PermissionError, ValueError)):
                run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', pairs, output,
                    replacement_workflow_root=root)
            self.assertFalse(output.exists())
