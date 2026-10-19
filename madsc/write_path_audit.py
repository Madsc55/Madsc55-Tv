"""Read-only conservative K1 audit of proposed Git paths.

Mirrors legacy protected_write_gate path policy; does not enforce Git pushes.
"""
from __future__ import annotations
from pathlib import PurePosixPath

PROTECTED_EXACT = frozenset({
    "CALISANLAR.m3u", "CALISMAYANLAR.txt", "YENILER.m3u",
    "YABANCI_KANALLAR.m3u", "GUVENLIK_KURALLARI.md", "AGENTS.md",
})
PROTECTED_PREFIXES = ("yedekler/", "YEDEKLER/", "FAVORILER/", "HEPSI/",
                      "EPG/", "logolar/", "logos/", "arsiv/")

def audit_write_paths(paths: list[str]) -> dict:
    if not isinstance(paths, list):
        raise ValueError("Paths must be a list")
    rejected = []
    for raw in paths:
        if not isinstance(raw, str):
            raise ValueError("Invalid repository path")
        name = raw.replace(chr(92), "/")
        parts = name.split("/")
        folded = name.casefold()
        if (chr(92) in raw or not name or name.startswith("/")
            or any(part in ("", ".", "..") for part in parts)
            or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw)
            or any(part.endswith((" ", ".")) for part in parts)
            or ":" in name
            or name.startswith("~")
            or folded in {item.casefold() for item in PROTECTED_EXACT}
            or any(part.casefold() in {item.casefold() for item in PROTECTED_EXACT}
                   for part in parts)
            or any(folded.startswith(prefix.casefold()) for prefix in PROTECTED_PREFIXES)
            or PurePosixPath(name).suffix.casefold() in (".m3u", ".m3u8")
            or any(part.casefold() in ("favoriler", "hepsi", "yedekler",
                                      "epg", "logolar", "logos", "arsiv") for part in parts)):
            rejected.append(raw)
    return {"rejected": rejected, "blocked": bool(rejected),
            "write_performed": False, "runtime_gate_enforced": False}
