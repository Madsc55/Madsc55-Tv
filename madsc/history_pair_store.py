"""K2 history pair stored as one versioned, atomically replaceable envelope.

This is an opt-in isolated artifact contract, not a migration of legacy files.
"""
import hashlib
import json
import os
import tempfile
from pathlib import Path

KEYS = ("gecmis.json", "ana_liste_test_gecmisi.json")


def encode_pair(pair):
    if set(pair) != set(KEYS):
        raise ValueError("Both history documents are required")
    for name, key in (("gecmis.json", "history"),
                      ("ana_liste_test_gecmisi.json", "channels")):
        if not isinstance(pair[name], dict) or not isinstance(pair[name].get(key), dict):
            raise ValueError("Invalid history document")
    body = json.dumps(pair, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return json.dumps({"schema": 1, "payload": pair,
                       "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest()},
                      ensure_ascii=False, sort_keys=True) + "\n"


def decode_pair(raw):
    envelope = json.loads(raw)
    if not isinstance(envelope, dict) or set(envelope) != {"schema", "payload", "sha256"}:
        raise ValueError("Invalid history envelope")
    if envelope["schema"] != 1:
        raise ValueError("Unsupported history envelope")
    canonical = json.dumps(envelope["payload"], sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"))
    if hashlib.sha256(canonical.encode("utf-8")).hexdigest() != envelope["sha256"]:
        raise ValueError("History digest mismatch")
    encode_pair(envelope["payload"])
    return envelope["payload"]


def atomic_write_pair(destination, pair):
    """One same-directory os.replace commit point, with cleanup on failure."""
    from madsc.write_path_audit import enforce_write_paths, enforce_local_append_path
    path = Path(destination)
    # K1 preflight also covers the atomic replacement entry point.
    enforce_write_paths([path.name])
    if (path.is_symlink() or not path.parent.is_dir()
            or any(parent.is_symlink() for parent in (path.parent, *path.parent.parents))):
        raise ValueError("Unsafe history destination")
    enforce_local_append_path(path.absolute())
    raw = encode_pair(pair)
    staged = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as handle:
            staged = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        enforce_local_append_path(path.absolute())
        os.replace(staged, path)
        staged = None
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


def write_isolated_history_pair(root, relative_path, pair):
    """K2 history artifact through K1 guard; never touches legacy histories."""
    from madsc.write_path_audit import enforce_write_paths, enforce_local_output_path
    if not isinstance(relative_path, str) or not relative_path.startswith("reports/"):
        raise PermissionError("Only isolated history reports are permitted")
    enforce_write_paths([relative_path])
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise PermissionError("Invalid history root")
    target = root.joinpath(*relative_path.split("/"))
    if target.is_symlink() or target.exists():
        raise PermissionError("Existing history evidence cannot be replaced")
    if target.parent.is_symlink() or not target.parent.is_dir():
        raise PermissionError("History report directory must already exist")
    if not target.parent.resolve().is_relative_to(root.resolve()):
        raise PermissionError("History report escapes root")
    raw = encode_pair(pair)
    enforce_local_output_path(target, allowed_root=root)
    with target.open("x", encoding="utf-8") as handle:
        handle.write(raw)
    return {"isolated_history_written": True, "production_write_allowed": False}
