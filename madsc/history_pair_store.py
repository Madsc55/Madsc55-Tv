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
    path = Path(destination)
    if path.is_symlink() or not path.parent.is_dir():
        raise ValueError("Unsafe history destination")
    raw = encode_pair(pair)
    staged = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as handle:
            staged = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
        staged = None
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)
