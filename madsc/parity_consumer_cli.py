"""Observe only the three isolated file consumers used by parity workflows."""
import argparse
import json
import os
from pathlib import Path
import sys

from madsc.fixture_report_writer import _exclusive_bytes, _prepare_fixture_root
from madsc.parity_manifest_cli import _read_regular_file
from madsc.parity_process import observe_process
from madsc.parity_snapshot_writer import OUTPUT_PATH, write_execution_snapshot
from madsc.write_path_audit import enforce_local_output_path, enforce_write_paths

DIAGNOSTICS = {
    'process_stdout': 'reports/parity-process-stdout.log',
    'process_stderr': 'reports/parity-process-stderr.log',
    'process_outcome': 'reports/parity-process-outcome.json',
}
CONSUMERS = {
    'k1': ('config/shadow_manifest.json', 'reports/k1-guard.txt',
           ['-m', 'src.madsc_guard', 'config/shadow_manifest.json']),
    'k4': ('reports/k4-source/nested/sample.txt', 'reports/k4-restore-drill.json',
           ['-m', 'madsc.restore_drill', '--source', 'reports/k4-source',
            '--file', 'nested/sample.txt', '--output', 'reports/k4-restore-drill.json']),
    'k5': ('reports/k2-input.m3u', 'reports/k2-candidates.json',
           ['-m', 'madsc.artifact_transport', 'produce', '--path', 'reports/k2-candidates.json',
            '--source', 'reports/k2-input.m3u']),
}


def run_consumer(consumer, *, root, timeout_seconds=120):
    if consumer not in CONSUMERS:
        raise ValueError('Unknown isolated consumer')
    # A ceiling below the 10-minute job timeout leaves time for evidence upload.
    if (type(timeout_seconds) not in (int, float) or not 0 < timeout_seconds <= 120):
        raise ValueError('Consumer timeout must be between 0 and 120 seconds')
    root = _prepare_fixture_root(Path(root))
    input_path, output_path, arguments = CONSUMERS[consumer]
    _read_regular_file(root / input_path, 2 * 1024 * 1024)
    paths = [*DIAGNOSTICS.values(), OUTPUT_PATH, output_path]
    enforce_write_paths(paths)
    for path in paths:
        enforce_local_output_path(root / path, allowed_root=root)
    argv = [sys.executable, *arguments]
    if consumer == 'k5':
        run_id, head_sha = os.environ.get('RUN_ID', ''), os.environ.get('COMMIT_SHA', '')
        if (not run_id.isascii() or not run_id.isdigit() or len(run_id) > 20
                or len(head_sha) != 40 or any(c not in '0123456789abcdef' for c in head_sha)):
            raise ValueError('Missing isolated K5 execution identity')
        argv += ['--run-id', run_id, '--commit-sha', head_sha]
    result = observe_process(argv, cwd=root, timeout_seconds=timeout_seconds)
    code = result['exit_code']
    shell_code = code if code >= 0 else 128 - code
    try:
        _exclusive_bytes(root / DIAGNOSTICS['process_stdout'], result['stdout'])
        _exclusive_bytes(root / DIAGNOSTICS['process_stderr'], result['stderr'])
        outcome = {'schema': 'madsc-local-process-outcome-v1', 'consumer': consumer,
                   'exit_code': code, 'timed_out': result['timed_out'],
                   'behavioral_parity_accepted': False, 'production_ready': False}
        _exclusive_bytes(root / DIAGNOSTICS['process_outcome'],
                         (json.dumps(outcome, sort_keys=True) + '\n').encode())
        if consumer == 'k1':
            _exclusive_bytes(root / output_path, result['stdout'])
        if code != 0 or result['timed_out']:
            write_execution_snapshot(root, exit_code=code, timed_out=result['timed_out'],
                outputs=[(label, root / path) for label, path in DIAGNOSTICS.items()],
                side_effects=[])
    except Exception as exc:
        print(f'Execution evidence unavailable: {type(exc).__name__}: {exc}', file=sys.stderr)
        # Never replace a measured consumer failure with an evidence writer error.
        return shell_code if shell_code else 1
    return shell_code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--consumer', choices=sorted(CONSUMERS), required=True)
    parser.add_argument('--timeout-seconds', type=float, default=120)
    args = parser.parse_args(argv)
    return run_consumer(args.consumer, root=Path.cwd(), timeout_seconds=args.timeout_seconds)


if __name__ == '__main__':
    raise SystemExit(main())
