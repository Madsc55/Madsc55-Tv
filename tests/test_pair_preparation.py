"""Pinned source identities and same-input requirements cannot grant parity."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from madsc.legacy_parity_evidence import compare_provenance_bound_batch, reconcile_legacy_scope
from madsc.legacy_parity_cli import run


class PairPreparationTests(unittest.TestCase):
    def setUp(self):
        self.inventory = json.loads((Path(__file__).resolve().parents[1] /
                                     'docs/LEGACY_SOURCE_SCOPE.json').read_text())

    def test_all_92_missing_pairs_have_exact_pinned_source_and_open_requirements(self):
        report = compare_provenance_bound_batch(self.inventory, {})
        by_path = {row['path']: row for row in self.inventory['workflows']}
        self.assertEqual(report['pair_preparation_rows'], 92)
        self.assertEqual(len({row['path'] for row in report['rows']}), 92)
        self.assertEqual(report['missing_pairs'], 92)
        for row in report['rows']:
            prepared = row['pair_preparation']
            identity = prepared['source_identity']
            self.assertEqual(identity['workflow_blob_sha'], by_path[row['path']]['git_blob_sha'])
            self.assertEqual(identity['workflow_bytes'], by_path[row['path']]['bytes'])
            self.assertEqual(identity['commit_sha'], self.inventory['source_commit'])
            self.assertIsNone(prepared['same_input_sha256'])
            self.assertEqual(len(prepared['independent_evidence_missing']), 6)
            self.assertFalse(prepared['production_ready'])
            self.assertFalse(row['behavioral_parity_accepted'])
        excluded = set(reconcile_legacy_scope(self.inventory)['excluded_from_92'])
        self.assertFalse(excluded & {row['path'] for row in report['rows']})

    def test_valid_shape_forged_blob_size_tree_or_source_script_is_rejected(self):
        for field in ('git_blob_sha', 'bytes', 'path', 'source_tree_sha', 'scope_script_blob_sha'):
            changed = copy.deepcopy(self.inventory)
            if field == 'git_blob_sha': changed['workflows'][0][field] = 'f' * 40
            elif field == 'bytes': changed['workflows'][0][field] += 1
            elif field == 'path': changed['workflows'][0][field] = '.github/workflows/forged.yml'
            else: changed[field] = 'f' * 40
            with self.subTest(field=field), self.assertRaises(ValueError):
                compare_provenance_bound_batch(changed, {})

    def test_catalog_order_does_not_change_source_binding(self):
        report = compare_provenance_bound_batch(self.inventory, {})
        self.inventory['workflows'].reverse()
        reordered = compare_provenance_bound_batch(self.inventory, {})
        self.assertEqual(report, reordered)

    def test_matching_pair_metadata_keeps_independent_proofs_open(self):
        from tests import test_legacy_parity_evidence as fixtures
        path = reconcile_legacy_scope(self.inventory)['legacy_paths'][0]
        blob = next(row['git_blob_sha'] for row in self.inventory['workflows'] if row['path'] == path)
        pair = fixtures.LegacyScopeTests.provenance_pair(path, blob)
        report = compare_provenance_bound_batch(self.inventory, {path: pair})
        row = next(row for row in report['rows'] if row['path'] == path)
        self.assertEqual(row['pair_preparation']['same_input_sha256'], 'c' * 64)
        self.assertEqual(len(row['pair_preparation']['independent_evidence_missing']), 6)
        self.assertFalse(row['behavioral_parity_accepted'])
        self.assertFalse(row['pair_preparation']['production_ready'])

    def test_existing_cli_publishes_missing_requirements_without_fabricated_pairs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory = root / 'source.json'
            inventory.write_text(json.dumps(self.inventory))
            pairs = root / 'pairs.json'
            pairs.write_text(json.dumps({'schema': 'madsc-legacy-provenance-pairs-v1', 'pairs': {}}))
            output = root / 'report.json'
            result = run(inventory, pairs, output)
            self.assertEqual(json.loads(output.read_text()), result)
            self.assertEqual(result['pair_preparation_rows'], 92)
            self.assertEqual(result['behavioral_parity_accepted'], 0)
