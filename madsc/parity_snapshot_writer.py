"""Build bounded parity snapshots from files produced by a real execution."""
import hashlib
import json
import os
import stat
from pathlib import Path

from madsc.fixture_report_writer import write_fixture_report
from madsc.legacy_parity_evidence import compare_execution_snapshots


OUTPUT_PATH = "reports/madsc-parity-snapshot.json"
MAX_OBSERVED_FILE_BYTES = 2 * 1024 * 1024


def _sha256_regular_file(path):
    path = Path(path)
    if path.is_symlink():
        raise PermissionError("Symlink parity observation is forbidden")
    # Keep the portable read-only modifiers in one source-bound expression so
    # the K1 callsite audit can prove this descriptor is not a writer.
    flags = (os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
             | getattr(os, "O_NOFOLLOW", 0))
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if (not stat.S_ISREG(metadata.st_mode)
                or metadata.st_size > MAX_OBSERVED_FILE_BYTES):
            raise PermissionError("Parity observation must be a bounded regular file")
        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_OBSERVED_FILE_BYTES:
                raise PermissionError("Oversized parity observation")
            digest.update(chunk)
        # A digest of changing bytes must not become execution evidence.
        # Check both the open descriptor and the pathname: replacement/unlink
        # can leave an unchanged descriptor referring to an obsolete inode.
        after = os.fstat(descriptor)
        try:
            current = path.lstat()
        except OSError as exc:
            raise ValueError("Parity file disappeared during read") from exc
        def version(info):
            return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
                    info.st_ctime_ns, info.st_nlink)
        if version(metadata) != version(after) or version(after) != version(current):
            raise ValueError("Parity file changed during read")
        return digest.hexdigest()
    finally:
        os.close(descriptor)


def _digest_map(observations, field):
    if not isinstance(observations, list) or len(observations) > 1000:
        raise ValueError(f"Invalid {field} observations")
    result = {}
    for row in observations:
        if (not isinstance(row, tuple) or len(row) != 2
                or not isinstance(row[0], str) or not row[0]
                or len(row[0]) > 512 or row[0] in result
                or any(ord(char) < 32 or ord(char) == 127 for char in row[0])):
            raise ValueError(f"Invalid or duplicate {field} label")
        result[row[0]] = _sha256_regular_file(row[1])
    return result


def build_execution_snapshot(*, exit_code, timed_out, outputs, side_effects):
    """Hash actual execution files into the strict snapshot schema."""
    if type(exit_code) is not int or not -255 <= exit_code <= 255:
        raise ValueError("Invalid execution exit code")
    if type(timed_out) is not bool:
        raise ValueError("Invalid execution timeout flag")
    if not isinstance(outputs, list) or not outputs:
        raise ValueError("At least one real execution output is required")
    snapshot = {
        "exit_code": exit_code,
        "timed_out": timed_out,
        "outputs": _digest_map(outputs, "output"),
        "side_effects": _digest_map(side_effects, "side-effect"),
    }
    compare_execution_snapshots(snapshot, snapshot)
    return snapshot


def write_execution_snapshot(root, *, exit_code, timed_out, outputs, side_effects):
    snapshot = build_execution_snapshot(
        exit_code=exit_code, timed_out=timed_out,
        outputs=outputs, side_effects=side_effects)
    encoded = json.dumps(snapshot, sort_keys=True, separators=(",", ":")) + "\n"
    result = write_fixture_report(Path(root), OUTPUT_PATH, encoded)
    return {
        **result,
        "relative_path": OUTPUT_PATH,
        "output_count": len(snapshot["outputs"]),
        "side_effect_count": len(snapshot["side_effects"]),
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }
