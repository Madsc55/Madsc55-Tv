"""Exact K1 preflight contracts for fixed read-only helper processes."""
from __future__ import annotations

import os
import stat
import sys
import tempfile
from pathlib import Path

from madsc.write_path_audit import ProtectedWriteRejected


DNS_RESOLVER = (
    "import json,socket,sys; "
    "a=socket.getaddrinfo(sys.argv[1],443,type=socket.SOCK_STREAM,"
    "proto=socket.IPPROTO_TCP); "
    "print(json.dumps([x[4][0] for x in a]))"
)


def _safe_argument(value: str) -> bool:
    return (isinstance(value, str) and bool(value) and "\x00" not in value
            and not any(ord(char) < 0x20 or ord(char) == 0x7f for char in value))


def enforce_dns_resolver_process(command, host: str) -> None:
    """Allow only the fixed isolated resolver child and one safe host argument."""
    expected = [sys.executable, "-I", "-B", "-c", DNS_RESOLVER, host]
    if not _safe_argument(host) or command != expected:
        raise ProtectedWriteRejected("Unsafe DNS resolver process contract")


def enforce_reachability_curl_process(command, url: str, resolve: str) -> None:
    """Allow the fixed stdout-only curl used by the manifest reachability pilot."""
    expected = [
        "curl", "-q", "--silent", "--show-error", "--fail", "--noproxy", "*",
        "--proto", "=https", "--max-time", "9", "--connect-timeout", "4",
        "--max-filesize", "65536", "--range", "0-65535",
        "--resolve", resolve, url,
    ]
    if not _safe_argument(url) or not _safe_argument(resolve) or command != expected:
        raise ProtectedWriteRejected("Unsafe reachability curl process contract")


def enforce_bounded_curl_process(command, url: str, resolve: str,
                                 byte_limit: int) -> None:
    """Allow the fixed stdout-only curl used for HLS manifests and segments."""
    if (isinstance(byte_limit, bool) or not isinstance(byte_limit, int)
            or not 1 <= byte_limit <= 1_500_000):
        raise ProtectedWriteRejected("Unsafe curl byte limit")
    expected = [
        "curl", "-q", "-fsS", "--noproxy", "*", "--proto", "=https",
        "--max-time", "9", "--connect-timeout", "4", "--max-filesize",
        str(byte_limit), "--resolve", resolve, url,
    ]
    if not _safe_argument(url) or not _safe_argument(resolve) or command != expected:
        raise ProtectedWriteRejected("Unsafe bounded curl process contract")


def enforce_ffprobe_read_process(command, segment: Path) -> None:
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
            or os.path.commonpath((str(segment), str(workspace))) != str(workspace)):
        raise ProtectedWriteRejected("Unsafe ffprobe read process contract")
