"""A declared behavior mapping binds sources and dataflow, never grants acceptance."""
import json
import tempfile
import unittest
from pathlib import Path
from madsc.legacy_parity_evidence import compare_provenance_bound_batch, reconcile_legacy_scope
from madsc.parity_workflow_readiness import audit_parity_workflow_readiness
from madsc.legacy_parity_cli import run

ROOT = Path(__file__).resolve().parents[1]

class BehaviorMappingBindingTests(unittest.TestCase):
    def setUp(self):
        self.source = json.loads((ROOT / 'docs/LEGACY_SOURCE_SCOPE.json').read_text())
        self.path = reconcile_legacy_scope(self.source)['legacy_paths'][0]
        source_row = next(row for row in self.source['workflows'] if row['path'] == self.path)
        contract = next(row for row in audit_parity_workflow_readiness(ROOT)['rows']
                        if row['workflow_path'] == '.github/workflows/madsc-01-guvenlik.yml')
        self.mapping = {'legacy_workflow_blob_sha': source_row['git_blob_sha'],
                        'replacement_workflow_path': contract['workflow_path'],
                        'replacement_workflow_blob_sha': contract['workflow_blob_sha'],
                        **contract['declared_file_binding']}

    def assess(self, mapping, pairs=None, root=ROOT):
        return compare_provenance_bound_batch(self.source, pairs or {},
            replacement_workflow_root=root, behavior_mappings={self.path: mapping})

    def test_matching_fixture_declaration_remains_review_required_and_pair_missing(self):
        report = self.assess(self.mapping)
        row = next(row for row in report['rows'] if row['path'] == self.path)
        self.assertTrue(row['pair_preparation']['replacement_source_mapping_bound'])
        self.assertTrue(row['pair_preparation']['replacement_mapping_review_required'])
        self.assertEqual(report['source_mappings_bound'], 1)
        self.assertEqual(report['source_mappings_independently_reviewed'], 0)
        self.assertEqual(report['missing_pairs'], 92)
        self.assertEqual(report['behavioral_parity_accepted'], 0)

    def test_wrong_source_consumer_or_role_is_rejected(self):
        for field in self.mapping:
            mapping = dict(self.mapping)
            mapping[field] = 'incorrect'
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.assess(mapping)

    def test_external_input_or_missing_root_does_not_accept_mapping(self):
        with self.assertRaises(ValueError):
            self.assess(self.mapping, root=None)
        catalog = audit_parity_workflow_readiness(ROOT)
        blocked = next(row for row in catalog['rows'] if row['input_classification'] == 'external_or_live_input_blocked')
        mapping = {**self.mapping, 'replacement_workflow_path': blocked['workflow_path'],
                   'replacement_workflow_blob_sha': blocked['workflow_blob_sha']}
        with self.assertRaises(ValueError):
            self.assess(mapping)

    def test_pair_cannot_silently_select_other_replacement(self):
        from tests import test_legacy_parity_evidence as fixtures
        pair = fixtures.LegacyScopeTests.provenance_pair(self.path, self.mapping['legacy_workflow_blob_sha'])
        with self.assertRaisesRegex(ValueError, 'differs from source-bound mapping'):
            self.assess(self.mapping, {self.path: pair})

    def test_bound_mapping_and_pair_reach_existing_preflight_without_acceptance(self):
        from tests import test_legacy_parity_evidence as fixtures
        pair = fixtures.LegacyScopeTests.provenance_pair(self.path, self.mapping['legacy_workflow_blob_sha'])
        pair['replacement']['workflow_path'] = self.mapping['replacement_workflow_path']
        pair['replacement']['workflow_blob_sha'] = self.mapping['replacement_workflow_blob_sha']
        for role in ('legacy', 'replacement'):
            pair[role]['snapshot']['outputs'] = {self.mapping['output_label']: 'd' * 64}
        report = self.assess(self.mapping, {self.path: pair})
        row = next(row for row in report['rows'] if row['path'] == self.path)
        self.assertTrue(row['replacement_workflow_contract_checked'])
        self.assertTrue(row['pair_preparation']['replacement_source_mapping_bound'])
        self.assertTrue(row['pair_preparation']['replacement_mapping_review_required'])
        self.assertEqual(report['behavioral_parity_accepted'], 0)

    def test_unknown_paths_or_forged_approval_fields_rejected(self):
        for mapping in ({**self.mapping, 'approved': True}, None, [], {'legacy_workflow_blob_sha': 'a' * 40}):
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                self.assess(mapping)
        with self.assertRaises(ValueError):
            compare_provenance_bound_batch(self.source, {}, replacement_workflow_root=ROOT,
                behavior_mappings={'.github/workflows/madsc-01-guvenlik.yml': self.mapping})

    def test_cli_carries_mapping_and_rejects_bad_mapping_without_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); pairs = root / 'pairs.json'
            payload = {'schema': 'madsc-legacy-provenance-pairs-v1', 'pairs': {},
                       'behavior_mappings': {self.path: self.mapping}}
            pairs.write_text(json.dumps(payload))
            output = root / 'report.json'
            report = run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', pairs, output, replacement_workflow_root=ROOT)
            self.assertEqual(report['source_mappings_bound'], 1)
            payload['behavior_mappings'][self.path]['output_label'] = 'wrong'
            pairs.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', pairs, root / 'bad.json', replacement_workflow_root=ROOT)
            self.assertFalse((root / 'bad.json').exists())
