"""Read-only conservative K1 audit of proposed Git paths.

Mirrors legacy protected_write_gate path policy; does not enforce Git pushes.
"""
from __future__ import annotations
from pathlib import Path, PurePosixPath
import unicodedata

PROTECTED_EXACT = frozenset({
    "CALISANLAR.m3u", "CALISMAYANLAR.txt", "YENILER.m3u",
    "YABANCI_KANALLAR.m3u", "GUVENLIK_KURALLARI.md", "AGENTS.md",
    "xmltv.xml", "playlist.m3u8",
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
        normalized = unicodedata.normalize("NFKC", name).casefold()
        duplicate = normalized in seen
        seen.add(normalized)
        parts = name.split("/")
        folded = normalized
        normalized_parts = folded.split("/")
        if (duplicate or chr(92) in raw or not name or name.startswith("/")
            or any(part in ("", ".", "..") for part in parts)
            or any(part in ("", ".", "..") for part in normalized_parts)
            or folded.startswith("/") or folded.startswith("~")
            or any(part.endswith((" ", ".")) for part in normalized_parts)
            or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw)
            or any(part.endswith((" ", ".")) for part in parts)
            or ":" in name
            or "\x00" in name
            or name.startswith("~")
            or folded in {item.casefold() for item in PROTECTED_EXACT}
            or any(part in {item.casefold() for item in PROTECTED_EXACT}
                   for part in normalized_parts)
            or any(folded.startswith(prefix.casefold()) for prefix in PROTECTED_PREFIXES)
            or PurePosixPath(folded).suffix in (".m3u", ".m3u8")
            or any(part in ("favoriler", "hepsi", "yedekler",
                                      "epg", "logolar", "logos", "arsiv") for part in normalized_parts)):
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


def enforce_local_output_path(destination: Path, *, allowed_root: Path | None = None) -> dict:
    """K1 local output preflight; reject protected ancestors and symlinks.

    Does not authorize production writes or intercept unrelated callers.
    """
    path = Path(destination)
    if not path.is_absolute():
        raise ProtectedWriteRejected("Output must be an absolute path")
    if any(part in (".", "..") for part in path.parts) or str(path) != str(path.absolute()):
        raise ProtectedWriteRejected("Ambiguous or traversing output path")
    if path.exists() or path.is_symlink():
        raise ProtectedWriteRejected("Output already exists or is a symlink")
    parent = path.parent
    if not parent.is_dir():
        raise ProtectedWriteRejected("Output parent must exist")
    for ancestor in (parent, *parent.parents):
        if ancestor.is_symlink():
            raise ProtectedWriteRejected("Symlinked output ancestor")
    if allowed_root is not None:
        root = Path(allowed_root)
        if not root.is_absolute() or not root.is_dir() or root.is_symlink():
            raise ProtectedWriteRejected("Invalid allowed output root")
        if not path.is_relative_to(root) or path == root:
            raise ProtectedWriteRejected("Output outside allowed root")
        relative = path.relative_to(root).as_posix()
    else:
        relative = path.relative_to(path.anchor).as_posix()
    enforce_write_paths([relative])
    return {"path_checked": True, "production_writes": False,
            "production_write_allowed": False}
