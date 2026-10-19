"""Fail-closed read-only K1 audit of proposed repository paths."""
from __future__ import annotations
from pathlib import PurePosixPath

PROTECTED = ("CALISANLAR.m3u", "YENILER", "YEDEKLER", "HEPSI", "FAVORILER", "epg", "logolar")

def audit_write_paths(paths: list[str]) -> dict:
    if not isinstance(paths, list):
        raise ValueError("Paths must be a list")
    rejected = []
    for value in paths:
        if not isinstance(value, str) or not value or "\\" in value:
            raise ValueError("Invalid repository path")
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or "." in value.split("/"):
            raise ValueError("Unsafe repository path")
        parts = path.parts
        if not parts:
            raise ValueError("Empty path")
        if any(part in PROTECTED for part in parts):
            rejected.append(value)
    return {"rejected": rejected, "blocked": bool(rejected),
            "write_performed": False, "runtime_gate_enforced": False}
