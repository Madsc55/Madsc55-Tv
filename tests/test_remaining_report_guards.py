"""Exercise real report writers and summary append without network access."""
import io
import json
import os
import tempfile
import unittest
from contextlib import ExitStack, contextmanager
from pathlib import Path
from unittest.mock import patch

from madsc import ci_diagnostics
from madsc import live_discovery_pilot, legacy_multisource_discovery
from madsc import k3_live_manifest_pilot, k3_turkish_tv_video_pilot
from madsc import progress_scorecard, k5_channel_gate
from madsc.write_path_audit import enforce_local_append_path


@contextmanager
def in_folder(root):
    previous = Path.cwd()
    os.chdir(root)
    try:
        yield
    finally:
        os.chdir(previous)


class RemainingReportGuardsTests(unittest.TestCase):
    def diagnostic(self, root, output, summary=None):
        args = ['diagnostics', '--log', str(root / 'missing.log'), '--output', str(output)]
        if summary is not None:
            args += ['--summary', str(summary)]
        with patch('sys.argv', args):
            ci_diagnostics.main()

    def test_summary_appends_without_replacing_existing_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = root / 'summary.md'
            summary.write_text('existing summary\n')
            self.diagnostic(root, root / 'report.json', summary)
            self.assertTrue(summary.read_text().startswith('existing summary\n'))
            self.assertIn('Regresyon hata teşhisi', summary.read_text())
            self.assertEqual(json.loads((root / 'report.json').read_text())['result'], 'unknown')
            before = summary.read_bytes()
            with self.assertRaises(PermissionError):
                self.diagnostic(root, root / 'report.json', summary)
            self.assertEqual(summary.read_bytes(), before)

    def test_invalid_summary_cannot_create_json_or_modify_protected_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = root / 'xmltv.xml'
            original.write_bytes(b'<tv/>')
            outside = root / 'outside'
            outside.mkdir()
            (root / 'alias').symlink_to(outside, target_is_directory=True)
            fifo = root / 'fifo'
            os.mkfifo(fifo)
            linked = root / 'linked.md'
            os.link(original, linked)
            summaries = [original, root / 'playlist.m3u8', root / 'alias' / 'summary.md',
                         fifo, linked, root]
            for summary in summaries:
                with self.subTest(summary=summary), self.assertRaises(PermissionError):
                    self.diagnostic(root, root / 'report.json', summary)
                self.assertFalse((root / 'report.json').exists())
            self.assertEqual(original.read_bytes(), b'<tv/>')
            self.assertEqual(list(outside.iterdir()), [])

    def test_new_summary_and_report_cannot_share_a_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / 'report.json'
            with self.assertRaises(PermissionError):
                self.diagnostic(root, target, target)
            self.assertFalse(target.exists())
            enforce_local_append_path(root / 'safe-summary.md')

    def test_scorecard_and_k5_gate_reject_targets_before_loading_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for module, options, worker in (
                (progress_scorecard, [], 'scorecard'),
                (k5_channel_gate, ['--k2', 'missing2.json', '--k3', 'missing3.json',
                                   '--run-id', '123', '--commit-sha', 'a' * 40],
                 'evaluate_k3_evidence')):
                with patch('sys.argv', ['report', '--output', str(root / 'xmltv.xml')] + options), \
                        patch.object(module, worker) as work:
                    with self.assertRaises(PermissionError):
                        module.main()
                    work.assert_not_called()
            self.assertFalse((root / 'xmltv.xml').exists())

    def test_four_pilots_write_once_and_reject_symlinked_reports(self):
        modules = [live_discovery_pilot, legacy_multisource_discovery,
                   k3_live_manifest_pilot, k3_turkish_tv_video_pilot]
        for module in modules:
            with self.subTest(module=module.__name__), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                with in_folder(root), ExitStack() as stack:
                    stack.enter_context(patch('builtins.print'))
                    if module is live_discovery_pilot:
                        response = stack.enter_context(patch.object(module, 'urlopen'))
                        response.return_value.__enter__.side_effect = lambda: io.BytesIO(b'#EXTM3U\n')
                    elif module is legacy_multisource_discovery:
                        stack.enter_context(patch.object(module, 'SOURCES', {}))
                    else:
                        stack.enter_context(patch.object(module, 'candidates', return_value=[]))
                    module.run()
                    reports = list((root / 'reports').glob('*.json'))
                    self.assertEqual(len(reports), 1)
                    original = reports[0].read_bytes()
                    data = json.loads(original)
                    if module is k3_turkish_tv_video_pilot:
                        self.assertEqual(data['reason_counts'], {})
                    with self.assertRaises(FileExistsError):
                        module.run()
                    self.assertEqual(reports[0].read_bytes(), original)
                    reports[0].unlink()
                    (root / 'reports').rmdir()
                    outside = root / 'outside'
                    outside.mkdir()
                    (root / 'reports').symlink_to(outside, target_is_directory=True)
                    with self.assertRaises(PermissionError):
                        module.run()
                    self.assertEqual(list(outside.iterdir()), [])

    def test_transport_targets_rejected_before_evidence_work_or_directory_creation(self):
        from madsc import artifact_transport, history_transport
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / 'outside'
            outside.mkdir()
            (root / 'alias').symlink_to(outside, target_is_directory=True)
            for module, options, worker in (
                (artifact_transport, ['produce', '--path'], 'pack'),
                (history_transport, ['produce', '--output'], 'pack_history')):
                for target in (root / 'EPG' / 'new' / 'result.json',
                               root / 'alias' / 'result.json'):
                    argv = ['transport'] + options + [str(target), '--run-id', '123',
                                                      '--commit-sha', 'a' * 40]
                    with patch('sys.argv', argv), patch.object(module, worker) as work:
                        with self.assertRaises(PermissionError):
                            module.main()
                        work.assert_not_called()
                self.assertFalse((root / 'EPG').exists())
                self.assertEqual(list(outside.iterdir()), [])

    def test_history_archive_output_guard_runs_before_download(self):
        from madsc.history_artifact_download import download_verified_history_artifact
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch('urllib.request.urlopen') as opener:
                with self.assertRaises(PermissionError):
                    download_verified_history_artifact(
                        repository='Madsc55/Madsc55-Tv', artifact_id=123, token='test-only',
                        expected_hashes={}, destination=root / 'xmltv.xml', opener=opener)
                opener.assert_not_called()
            self.assertFalse((root / 'xmltv.xml').exists())

    def test_legacy_export_rejects_symlink_parent_without_creating_output(self):
        from madsc.legacy_report_export import export_legacy_report
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / 'outside'
            outside.mkdir()
            (root / 'alias').symlink_to(outside, target_is_directory=True)
            scores, stable = root / 'scores.csv', root / 'stable.csv'
            scores.write_text('YAYIN_URL,PUAN\n')
            stable.write_text('YAYIN_URL,24_SAAT_KARARLI\n')
            with self.assertRaises(PermissionError):
                export_legacy_report(scores, stable, root / 'alias' / 'report')
            self.assertEqual(list(outside.iterdir()), [])
