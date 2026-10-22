"""Review rationale must bind the same declared source and dataflow in the CLI."""
import json
import tempfile
import unittest
from pathlib import Path
from tests import test_behavior_mapping_binding as fixtures
from madsc.legacy_parity_cli import run
from madsc.legacy_parity_evidence import compare_provenance_bound_batch

ROOT = Path(__file__).resolve().parents[1]

class MappingReviewChainTests(unittest.TestCase):
    def setUp(self):
        fixture = fixtures.BehaviorMappingBindingTests()
        fixture.setUp()
        self.source, self.path, self.mapping = fixture.source, fixture.path, fixture.mapping
        self.review = {
            'legacy_path': self.path,
            'legacy_blob_sha': self.mapping['legacy_workflow_blob_sha'],
            'replacement_workflow_path': self.mapping['replacement_workflow_path'],
            'replacement_blob_sha': self.mapping['replacement_workflow_blob_sha'],
            'input_role': self.mapping['input_path'],
            'output_role': self.mapping['output_label'] + '=' + self.mapping['output_path'],
            'review_rationale': 'Synthetic integration fixture; no semantic equivalence asserted.',
        }

    def assess(self, rows, mappings=None, root=ROOT):
        return compare_provenance_bound_batch(self.source, {}, replacement_workflow_root=root,
            behavior_mappings={self.path: self.mapping} if mappings is None else mappings,
            mapping_review_rows=rows)

    def test_candidate_reaches_pair_preparation_without_approval(self):
        report = self.assess([self.review])
        row = next(r for r in report['rows'] if r['path'] == self.path)['pair_preparation']
        self.assertEqual(row['replacement_mapping_review_candidate']['review_rationale'],
                         self.review['review_rationale'])
        self.assertTrue(row['replacement_mapping_review_required'])
        self.assertEqual(report['source_mapping_review_candidates_bound'], 1)
        self.assertEqual(report['source_mappings_independently_reviewed'], 0)
        self.assertEqual(report['behavioral_parity_accepted'], 0)
        self.assertEqual(report['missing_pairs'], 92)

    def test_review_cannot_select_other_source_role_or_grant_approval(self):
        for field in self.review:
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.assess([{**self.review, field: ''}])
        for rows in ([{**self.review, 'approved': True}], [self.review, self.review],
                     [{**self.review, 'output_role': 'wrong=output'}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                self.assess(rows)
        with self.assertRaises(ValueError):
            self.assess([self.review], mappings={})
        with self.assertRaises(ValueError):
            self.assess([self.review], root=None)

    def test_absent_and_empty_review_are_distinct_without_acceptance(self):
        absent, empty = self.assess(None), self.assess([])
        self.assertIsNone(absent['source_mapping_review'])
        self.assertEqual(empty['source_mapping_review']['mapping_candidates_supplied'], 0)
        self.assertEqual(empty['behavioral_parity_accepted'], 0)

    def test_existing_cli_validates_review_before_any_report_write(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            payload = {'schema': 'madsc-legacy-provenance-pairs-v1', 'pairs': {},
                       'behavior_mappings': {self.path: self.mapping},
                       'mapping_review_rows': [self.review]}
            source = root / 'input.json'
            source.write_text(json.dumps(payload))
            report = run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', source,
                         root / 'report.json', replacement_workflow_root=ROOT)
            self.assertEqual(report['source_mapping_review_candidates_bound'], 1)
            payload['mapping_review_rows'][0]['output_role'] = 'wrong=path'
            source.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                run(ROOT / 'docs/LEGACY_SOURCE_SCOPE.json', source,
                    root / 'invalid.json', replacement_workflow_root=ROOT)
            self.assertFalse((root / 'invalid.json').exists())
