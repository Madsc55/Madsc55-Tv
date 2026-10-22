import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from madsc.parity_process import observe_process, MAX_CAPTURE_BYTES
from madsc.parity_snapshot_writer import write_execution_snapshot


class ParityProcessTests(unittest.TestCase):
    def run_python(self, source, timeout=3):
        return observe_process([sys.executable, '-c', source], cwd='.', timeout_seconds=timeout)

    def test_nonzero_keeps_binary_streams_and_is_not_timeout(self):
        result = self.run_python("import os; os.write(1,b'out\\x00'); os.write(2,b'err\\xff'); raise SystemExit(23)")
        self.assertEqual(result, dict(exit_code=23, timed_out=False, stdout=b'out\0', stderr=b'err\xff'))

    def test_child_124_is_not_timeout(self):
        self.assertFalse(self.run_python('raise SystemExit(124)')['timed_out'])

    def test_real_timeout_preserves_diagnostics_into_snapshot(self):
        result = self.run_python("import os,time; os.write(2,b'before timeout'); time.sleep(10)", timeout=.25)
        self.assertTrue(result['timed_out'])
        self.assertEqual(result['exit_code'], 124)
        self.assertEqual(result['stderr'], b'before timeout')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / 'stderr.log'
            log.write_bytes(result['stderr'])
            written = write_execution_snapshot(root, exit_code=result['exit_code'],
                timed_out=result['timed_out'], outputs=[('stderr', log)], side_effects=[])
            self.assertTrue(written['isolated_report_written'])
            self.assertFalse(written['behavioral_parity_accepted'])

    def test_timeout_reaps_parent_and_kills_descendant(self):
        # getpid() may belong to a nested PID namespace while /proc is mounted
        # from its host. Identify the actual procfs entry and start time inside
        # each child; otherwise /proc/<getpid()> can be an unrelated host job.
        source = ("import os,time; from pathlib import Path; p=os.fork(); "
                  "s=Path('/proc/self/stat').read_text().split(); "
                  "os.write(1,(s[0]+' '+s[21]+'\\n').encode()); time.sleep(30)")
        result = self.run_python(source, timeout=2)
        self.assertTrue(result['timed_out'])
        identities = [line.split() for line in result['stdout'].decode().splitlines()]
        self.assertEqual(len(identities), 2, 'Both processes must start before timeout')
        self.assertEqual(len({pid for pid, _ in identities}), 2)
        for pid, started in identities:
            status = Path('/proc') / pid / 'stat'
            deadline = time.monotonic() + 5
            while True:
                try:
                    fields = status.read_text().split()
                except FileNotFoundError:
                    break
                if fields[21] != started or fields[2] in ('Z', 'X'):
                    break
                self.assertLess(time.monotonic(), deadline, 'Descendant survived group timeout')
                time.sleep(.005)

    def test_overflow_rejected_without_truncated_evidence(self):
        with self.assertRaisesRegex(ValueError, 'capture limit'):
            self.run_python(f"import os; os.write(1,b'x'*{MAX_CAPTURE_BYTES + 1})")

    def test_both_pipes_drained_without_deadlock(self):
        result = self.run_python("import os; [(os.write(1,b'o'*8192),os.write(2,b'e'*8192)) for _ in range(20)]")
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(len(result['stdout']), 20*8192)
        self.assertEqual(len(result['stderr']), 20*8192)

    def test_invalid_timeout_does_not_start_process(self):
        for timeout in (True, 0, -1, float('nan'), float('inf')):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                self.run_python('raise SystemExit(0)', timeout=timeout)

    def test_k1_tee_failure_cannot_become_success(self):
        source = (Path(__file__).resolve().parents[1] / '.github/workflows/madsc-01-guvenlik.yml').read_text()
        start = source.index('          pipeline_status=')
        end = source.index('          set -e', start)
        capture = '\n'.join(line[10:] for line in source[start:end].splitlines())
        for first, second, expected in ((0, 7, 7), (23, 7, 23), (0, 0, 0)):
            script = f'set +e\n(exit {first}) | (cat >/dev/null; exit {second})\n{capture}\nexit "$consumer_status"'
            self.assertEqual(subprocess.run(['bash', '-c', script]).returncode, expected)
