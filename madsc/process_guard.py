"""Exact K1 preflight contracts for fixed read-only helper processes."""
from __future__ import annotations

import os
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from madsc.write_path_audit import ProtectedWriteRejected


DNS_RESOLVER = (
    "import json,socket,sys; "
    "a=socket.getaddrinfo(sys.argv[1],443,type=socket.SOCK_STREAM,"
    "proto=socket.IPPROTO_TCP); "
    "print(json.dumps([x[4][0] for x in a]))"
)
FIXED_TOOL_ENV = {
    "PATH": "/usr/local/bin:/usr/bin",
    "LANG": "C",
    "LC_ALL": "C",
}

_PARITY_CONSUMER_ARGUMENTS = {
    "k1": ["-m", "src.madsc_guard", "config/shadow_manifest.json"],
    "k4": ["-m", "madsc.restore_drill", "--source", "reports/k4-source",
           "--file", "nested/sample.txt", "--output", "reports/k4-restore-drill.json"],
    "k5": ["-m", "madsc.artifact_transport", "produce", "--path",
           "reports/k2-candidates.json", "--source", "reports/k2-input.m3u"],
}

_PARITY_CAPABILITY_SEAL = object()


@dataclass(frozen=True)
class _ParityProcessCapability:
    seal: object
    consumer: str
    argv: tuple[str, ...]
    cwd: str
    cwd_device: int
    cwd_inode: int
    code_root: str
    code_root_device: int
    code_root_inode: int
    environment: tuple[tuple[str, str], ...]
    timeout_seconds: float


def _safe_argument(value: str) -> bool:
    return (isinstance(value, str) and bool(value) and "\x00" not in value
            and not any(ord(char) < 0x20 or ord(char) == 0x7f for char in value))


def _fixed_runtime(cwd: Path, env: dict[str, str], expected_cwd: Path) -> bool:
    cwd, expected_cwd = Path(cwd), Path(expected_cwd)
    try:
        metadata = cwd.lstat()
    except OSError:
        return False
    return (env == FIXED_TOOL_ENV and cwd.is_absolute() and not cwd.is_symlink()
            and stat.S_ISDIR(metadata.st_mode) and metadata.st_nlink >= 1
            and cwd.resolve(strict=True) == expected_cwd.resolve(strict=True))


def _trusted_tool(name: str) -> bool:
    """Require a root-owned executable in the fixed, non-writable search path."""
    resolved = shutil.which(name, path=FIXED_TOOL_ENV["PATH"])
    if not resolved:
        return False
    executable = Path(resolved)
    try:
        metadata = executable.lstat()
        parent = executable.parent.lstat()
    except OSError:
        return False
    return (executable.is_absolute() and not executable.is_symlink()
            and stat.S_ISREG(metadata.st_mode) and metadata.st_nlink >= 1
            and metadata.st_uid == 0 and metadata.st_mode & 0o022 == 0
            and not executable.parent.is_symlink() and stat.S_ISDIR(parent.st_mode)
            and parent.st_uid == 0 and parent.st_mode & 0o022 == 0)


def enforce_dns_resolver_process(command, host: str) -> None:
    """Allow only the fixed isolated resolver child and one safe host argument."""
    expected = [sys.executable, "-I", "-B", "-c", DNS_RESOLVER, host]
    if not _safe_argument(host) or command != expected:
        raise ProtectedWriteRejected("Unsafe DNS resolver process contract")


def enforce_reachability_curl_process(command, url: str, resolve: str, *,
                                      cwd: Path, env: dict[str, str]) -> None:
    """Allow the fixed stdout-only curl used by the manifest reachability pilot."""
    expected = [
        "curl", "-q", "--silent", "--show-error", "--fail", "--noproxy", "*",
        "--proto", "=https", "--max-time", "9", "--connect-timeout", "4",
        "--max-filesize", "65536", "--range", "0-65535",
        "--resolve", resolve, url,
    ]
    if (not _safe_argument(url) or not _safe_argument(resolve) or command != expected
            or not _fixed_runtime(cwd, env, Path("/")) or not _trusted_tool("curl")):
        raise ProtectedWriteRejected("Unsafe reachability curl process contract")


def enforce_bounded_curl_process(command, url: str, resolve: str,
                                 byte_limit: int, *, cwd: Path,
                                 env: dict[str, str]) -> None:
    """Allow the fixed stdout-only curl used for HLS manifests and segments."""
    if (isinstance(byte_limit, bool) or not isinstance(byte_limit, int)
            or not 1 <= byte_limit <= 1_500_000):
        raise ProtectedWriteRejected("Unsafe curl byte limit")
    expected = [
        "curl", "-q", "-fsS", "--noproxy", "*", "--proto", "=https",
        "--max-time", "9", "--connect-timeout", "4", "--max-filesize",
        str(byte_limit), "--resolve", resolve, url,
    ]
    if (not _safe_argument(url) or not _safe_argument(resolve) or command != expected
            or not _fixed_runtime(cwd, env, Path("/")) or not _trusted_tool("curl")):
        raise ProtectedWriteRejected("Unsafe bounded curl process contract")


def enforce_ffprobe_read_process(command, segment: Path, *, cwd: Path,
                                 env: dict[str, str]) -> None:
    """Bind ffprobe to the one regular sample in a guarded K3 workspace."""
    segment = Path(segment)
    expected = [
        "ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
        "-of", "json", str(segment),
    ]
    temp_root = Path(tempfile.gettempdir())
    try:
        root_metadata = temp_root.lstat()
        workspace = segment.parent
        workspace_metadata = workspace.lstat()
        metadata = segment.lstat()
    except OSError as exc:
        raise ProtectedWriteRejected("Missing ffprobe input identity") from exc
    if (command != expected or not segment.is_absolute()
            or segment.name != "sample.ts" or segment.is_symlink()
            or not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1
            or not 188 <= metadata.st_size <= 1_500_000
            or temp_root.is_symlink() or not stat.S_ISDIR(root_metadata.st_mode)
            or temp_root.resolve(strict=True) != temp_root
            or workspace.parent != temp_root
            or not workspace.name.startswith("madsc-k3-video-")
            or workspace.is_symlink()
            or not stat.S_ISDIR(workspace_metadata.st_mode)
            or segment.resolve(strict=True) != segment
            or os.path.commonpath((str(segment), str(workspace))) != str(workspace)
            or not _fixed_runtime(cwd, env, workspace)
            or not _trusted_tool("ffprobe")):
        raise ProtectedWriteRejected("Unsafe ffprobe read process contract")


def enforce_parity_consumer_process(command, *, consumer: str, root: Path,
                                    run_id: str = "", commit_sha: str = "") -> None:
    """Allow only the three opt-in, repository-rooted parity consumers."""
    root = Path(root)
    arguments = _PARITY_CONSUMER_ARGUMENTS.get(consumer)
    if arguments is None:
        raise ProtectedWriteRejected("Unknown parity consumer process")
    expected = [sys.executable, *arguments]
    if consumer == "k5":
        if (not run_id.isascii() or not run_id.isdigit() or len(run_id) > 20
                or len(commit_sha) != 40
                or any(char not in "0123456789abcdef" for char in commit_sha)):
            raise ProtectedWriteRejected("Unsafe parity execution identity")
        expected += ["--run-id", run_id, "--commit-sha", commit_sha]
    elif run_id or commit_sha:
        raise ProtectedWriteRejected("Unexpected parity execution identity")
    try:
        metadata = root.lstat()
    except OSError as exc:
        raise ProtectedWriteRejected("Missing parity process root") from exc
    if (command != expected or not root.is_absolute() or root.is_symlink()
            or not stat.S_ISDIR(metadata.st_mode) or metadata.st_nlink < 1
            or root.resolve(strict=True) != root):
        raise ProtectedWriteRejected("Unsafe parity consumer process contract")


def authorize_parity_consumer_process(command, *, consumer: str, root: Path,
                                      timeout_seconds: float, run_id: str = "",
                                      commit_sha: str = "") -> _ParityProcessCapability:
    """Issue an identity-bound capability for one validated opt-in consumer."""
    if (type(timeout_seconds) not in (int, float)
            or not 0 < timeout_seconds <= 120):
        raise ProtectedWriteRejected("Unsafe parity consumer timeout")
    root = Path(root)
    enforce_parity_consumer_process(command, consumer=consumer, root=root,
                                    run_id=run_id, commit_sha=commit_sha)
    metadata = root.lstat()
    code_root = Path(__file__).resolve().parents[1]
    code_metadata = code_root.lstat()
    environment = {
        "PYTHONPATH": os.fspath(code_root),
        "PYTHONDONTWRITEBYTECODE": "1",
        "LANG": "C",
        "LC_ALL": "C",
    }
    return _ParityProcessCapability(
        seal=_PARITY_CAPABILITY_SEAL,
        consumer=consumer,
        argv=tuple(command),
        cwd=os.fspath(root),
        cwd_device=metadata.st_dev,
        cwd_inode=metadata.st_ino,
        code_root=os.fspath(code_root),
        code_root_device=code_metadata.st_dev,
        code_root_inode=code_metadata.st_ino,
        environment=tuple(sorted(environment.items())),
        timeout_seconds=float(timeout_seconds),
    )


def parity_process_environment(capability) -> dict[str, str]:
    """Return the fixed environment carried by a valid issued capability."""
    if (not isinstance(capability, _ParityProcessCapability)
            or capability.seal is not _PARITY_CAPABILITY_SEAL):
        raise ProtectedWriteRejected("Invalid parity process capability")
    return dict(capability.environment)


def validate_parity_process_capability(capability, command, *, cwd: Path,
                                       timeout_seconds: float,
                                       env: dict[str, str]) -> None:
    """Fail closed unless launch inputs still match the issued capability."""
    cwd = Path(cwd)
    try:
        metadata = cwd.lstat()
    except OSError as exc:
        raise ProtectedWriteRejected("Missing parity capability root") from exc
    try:
        code_metadata = Path(capability.code_root).lstat()
    except (AttributeError, OSError) as exc:
        raise ProtectedWriteRejected("Missing parity capability code root") from exc
    if (not isinstance(capability, _ParityProcessCapability)
            or capability.seal is not _PARITY_CAPABILITY_SEAL
            or tuple(command) != capability.argv
            or os.fspath(cwd) != capability.cwd
            or float(timeout_seconds) != capability.timeout_seconds
            or not isinstance(env, dict)
            or tuple(sorted(env.items())) != capability.environment
            or cwd.is_symlink() or not stat.S_ISDIR(metadata.st_mode)
            or (metadata.st_dev, metadata.st_ino)
            != (capability.cwd_device, capability.cwd_inode)
            or Path(capability.code_root).is_symlink()
            or not stat.S_ISDIR(code_metadata.st_mode)
            or (code_metadata.st_dev, code_metadata.st_ino)
            != (capability.code_root_device, capability.code_root_inode)
            or Path(capability.code_root).resolve(strict=True)
            != Path(capability.code_root)
            or cwd.resolve(strict=True) != cwd):
        raise ProtectedWriteRejected("Invalid parity process capability")
