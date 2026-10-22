"""Supplied history pages cannot hide omitted failures behind reordered success."""
import unittest
from madsc.maintenance import assess_failure_history


def record(i, conclusion=None, status='completed', timestamp='2026-10-22T00:00:00Z'):
    return {'id': i, 'head_branch': 'main', 'created_at': timestamp,
            'status': status, 'conclusion': conclusion}


class FailureHistoryOrderTests(unittest.TestCase):
    def assess(self, pages, limit=2):
        return assess_failure_history(pages, current_run_id=5, branch='main', limit=limit)

    def test_reordered_partial_page_cannot_use_success_as_boundary(self):
        rows = [record(5, status='in_progress'), record(2, 'success'), record(4, 'failure')]
        with self.assertRaisesRegex(ValueError, 'order'):
            self.assess([{'total_count': 4, 'workflow_runs': rows}])

    def test_reordered_pages_cannot_use_success_as_boundary(self):
        pages = [{'total_count': 4, 'workflow_runs': [record(5, status='in_progress'), record(2, 'success')]},
                 {'total_count': 4, 'workflow_runs': [record(4, 'failure')]}]
        with self.assertRaisesRegex(ValueError, 'order'):
            self.assess(pages)

    def test_ignored_active_record_still_needs_valid_timestamp(self):
        rows = [record(5, status='in_progress'), record(4, status='queued', timestamp=None),
                record(3, 'success')]
        with self.assertRaises(ValueError):
            self.assess([{'total_count': 3, 'workflow_runs': rows}])

    def test_timestamp_order_is_checked_not_only_numeric_id(self):
        rows = [record(5, status='in_progress'),
                record(4, 'success', timestamp='2026-10-23T00:00:00Z')]
        with self.assertRaisesRegex(ValueError, 'order'):
            self.assess([{'total_count': 2, 'workflow_runs': rows}])

    def test_ordered_prefix_boundary_and_full_threshold_keep_existing_policy(self):
        current = record(5, status='in_progress')
        allowed = self.assess([{'total_count': 8, 'workflow_runs':
                              [current, record(4, 'failure'), record(3, 'success')]}])
        self.assertFalse(allowed['blocked'])
        self.assertFalse(allowed['history_complete'])
        blocked = self.assess([{'total_count': 3, 'workflow_runs':
                              [current, record(4, 'failure'), record(3, 'timed_out')]}])
        self.assertTrue(blocked['blocked'])
        self.assertFalse(blocked['runtime_history_origin_verified'])
