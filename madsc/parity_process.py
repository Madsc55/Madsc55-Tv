"""Observe a local subprocess; does not authorize commands or production writes.

Caller owns command selection. No shell is used. A timeout is measured by a
monotonic deadline, never inferred from a child's exit code of 124.
"""
import math
import os
import selectors
import signal
import subprocess
import time

MAX_CAPTURE_BYTES = 1024 * 1024


def observe_process(argv, *, cwd, timeout_seconds):
    """Return actual bounded stdout/stderr bytes and process outcome.

    Output overflow raises rather than producing truncated parity evidence.
    The process group is killed on deadline, overflow, and observer failure.
    This POSIX observer is a building block, not a workflow acceptance gate.
    """
    if (not isinstance(argv, (list, tuple)) or not argv
            or any(not isinstance(arg, str) or not arg or '\0' in arg for arg in argv)):
        raise ValueError('Expected nonempty command argument strings')
    if (isinstance(timeout_seconds, bool)
            or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(timeout_seconds) or timeout_seconds <= 0):
        raise ValueError('Expected finite positive timeout')
    if os.name != 'posix':
        raise RuntimeError('Process-group observation requires POSIX')
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    deadline = time.monotonic() + timeout_seconds
    timed_out = False
    with subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          start_new_session=True) as process:
        def kill_group():
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            with selectors.DefaultSelector() as selector:
                for name, pipe in (('stdout', process.stdout), ('stderr', process.stderr)):
                    os.set_blocking(pipe.fileno(), False)
                    selector.register(pipe, selectors.EVENT_READ, name)
                while selector.get_map() or process.poll() is None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        timed_out = True
                        kill_group()
                        process.wait()
                        # Drain bytes already in the pipes after killing all writers.
                        for key in list(selector.get_map().values()):
                            while True:
                                chunk = os.read(key.fd, 65536)
                                if not chunk:
                                    break
                                buffers[key.data].extend(chunk)
                                if len(buffers[key.data]) > MAX_CAPTURE_BYTES:
                                    raise ValueError('Parity process output exceeds capture limit')
                        break
                    for key, _ in selector.select(min(remaining, 0.05)):
                        chunk = os.read(key.fd, 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            continue
                        buffers[key.data].extend(chunk)
                        if len(buffers[key.data]) > MAX_CAPTURE_BYTES:
                            raise ValueError('Parity process output exceeds capture limit')
                returncode = process.wait()
        finally:
            # Also stop descendants that closed their inherited pipes and outlived
            # a successful parent; local observation must not leave background jobs.
            kill_group()
    return {'exit_code': 124 if timed_out else returncode,
            'timed_out': timed_out,
            'stdout': bytes(buffers['stdout']), 'stderr': bytes(buffers['stderr'])}
