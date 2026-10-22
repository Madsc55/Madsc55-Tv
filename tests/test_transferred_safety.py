"""Offline integration of recovered K1 path and K5 history fixes in Madsc55-Tv."""
import tempfile
import unittest
from pathlib import Path
from madsc.write_path_audit import audit_write_paths, enforce_local_output_path, ProtectedWriteRejected
from src.madsc_guard import safe_relative_path
from madsc.maintenance import assess_failure_history


def record(i, result=None, status='completed', branch='main'):
    return {'id': i, 'head_branch': branch, 'created_at': '2026-10-22T00:00:00Z',
            'status': status, 'conclusion': result}


class TransferredSafetyTests(unittest.TestCase):
    def test_metadata_and_nested_protected_paths_in_both_k1_gates(self):
        for name in ('FAVORILER.json', 'nested/favorites.csv', 'cache/HEPSI.txt',
                     'cache/EPG/tv.xml', 'cache/logos/logo.png', 'cache/logolar/logo.png',
                     'cache/arsiv/history.json', 'cache/favorites.json'):
            with self.subTest(path=name):
                self.assertTrue(audit_write_paths([name])['blocked'])
                self.assertFalse(safe_relative_path('artifacts/' + name))

    def test_allowed_root_cannot_hide_protected_parent_and_original_bytes_survive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for directory in ('logos', 'EPG', 'arsiv', 'FAVORILER'):
                parent = root / directory
                parent.mkdir()
                original = parent / 'existing.json'
                original.write_bytes(b'keep original')
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_local_output_path(parent / 'new.json', allowed_root=parent)
                self.assertFalse((parent / 'new.json').exists())
                self.assertEqual(original.read_bytes(), b'keep original')
            enforce_local_output_path(root / 'safe.json', allowed_root=root)

    def test_second_page_failures_stop_k5_and_missing_page_is_not_zero_failures(self):
        first = [record(i, status='in_progress') for i in range(104, 4, -1)]
        pages = [{'total_count': 103, 'workflow_runs': first},
                 {'total_count': 103, 'workflow_runs': [record(i, 'failure') for i in (4, 3, 2)]}]
        with self.assertRaisesRegex(ValueError, 'More failure history'):
            assess_failure_history(pages[:1], current_run_id=104, branch='main')
        result = assess_failure_history(pages, current_run_id=104, branch='main')
        self.assertTrue(result['blocked'])
        self.assertEqual(result['history_pages_checked'], 2)
        self.assertFalse(result['runtime_history_origin_verified'])

    def test_rerun_does_not_count_later_failures_and_success_resets(self):
        rows = [record(7, 'failure'), record(6, 'failure'), record(5, status='in_progress'),
                record(4, 'failure'), record(3, 'success'), record(2, 'failure')]
        result = assess_failure_history([{'total_count': len(rows), 'workflow_runs': rows}],
                                        current_run_id=5, branch='main')
        self.assertFalse(result['blocked'])
        self.assertEqual(result['consecutive_failures'], 1)

    def test_missing_duplicate_ambiguous_history_denied(self):
        current = record(4, status='in_progress')
        for page in ({'total_count': 1, 'workflow_runs': [record(3, 'success')]},
                     {'total_count': 2, 'workflow_runs': [current, current]},
                     {'total_count': 1, 'workflow_runs': []},
                     {'total_count': True, 'workflow_runs': [current]},
                     {'total_count': 2, 'workflow_runs': [current, {**record(3, 'failure'), 'created_at': None}]}):
            with self.subTest(page=page), self.assertRaises(ValueError):
                assess_failure_history([page], current_run_id=4, branch='main')
