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
    seen = set()
    for raw in paths:
        if not isinstance(raw, str):
            raise ValueError("Invalid repository path")
        name = raw.replace(chr(92), "/")
        duplicate = name.casefold() in seen
        seen.add(name.casefold())
        parts = name.split("/")
        folded = name.casefold()
        if (duplicate or chr(92) in raw or not name or name.startswith("/")
            or any(part in ("", ".", "..") for part in parts)
            or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw)
            or any(part.endswith((" ", ".")) for part in parts)
            or ":" in name
            or "\\x00" in name
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


class ProtectedWriteRejected(PermissionError):
    """Fail-closed refusal before any proposed protected repository write."""


def enforce_write_paths(paths: list[str]) -> dict:
    """Call immediately before a repository write; never grants user approval.

    This is a reusable runtime guard for callers that explicitly invoke it.
    It does not intercept independent GitHub Actions or direct git pushes.
    """
    report = audit_write_paths(paths)
    if report["blocked"]:
        raise ProtectedWriteRejected(
            "Protected or ambiguous write paths rejected: " +
            ", ".join(report["rejected"])
        )
    return {"blocked": False, "checked_paths": list(paths),
            "write_performed": False, "runtime_gate_enforced": True}
