"""Read-only conservative K1 audit of proposed Git paths.

Mirrors legacy protected_write_gate path policy; does not enforce Git pushes.
"""
from __future__ import annotations
from pathlib import Path, PurePosixPath
import unicodedata
import stat

PROTECTED_EXACT = frozenset({
    "CALISANLAR.m3u", "CALISMAYANLAR.txt", "YENILER.m3u",
    "YABANCI_KANALLAR.m3u", "GUVENLIK_KURALLARI.md", "AGENTS.md",
    "xmltv.xml", "playlist.m3u8",
})
PROTECTED_PREFIXES = ("yedekler/", "YEDEKLER/", "FAVORILER/", "HEPSI/",
                      "EPG/", "logolar/", "logos/", "arsiv/")

def audit_write_paths(paths: list[str]) -> dict:
    if not isinstance(paths, list) or not paths:
        raise ValueError("Paths must be a nonempty list")
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
        if (duplicate or chr(92) in raw or chr(92) in normalized
            or normalized.count("/") != name.count("/")
            or not name or name.startswith("/")
            or any(part in ("", ".", "..") for part in parts)
            or any(part in ("", ".", "..") for part in normalized_parts)
            or folded.startswith("/") or folded.startswith("~")
            or any(part.endswith((" ", ".")) for part in normalized_parts)
            # Windows treats these stems as devices, even with extensions;
            # reject them on every platform to avoid path aliasing.
            or any(part.split(".", 1)[0].rstrip(" ") in
                   ({"con", "prn", "aux", "nul"} |
                    {f"com{i}" for i in range(1, 10)} |
                    {f"lpt{i}" for i in range(1, 10)})
                   for part in normalized_parts)
            or any(unicodedata.category(ch) in ("Cc", "Zl", "Zp") for ch in raw)
            # Format controls (bidi overrides, zero-width joins) can disguise
            # protected filenames in reviews and logs; reject them outright.
            or any(unicodedata.category(ch) in ("Cf", "Cs") for ch in raw)
            # Unicode noncharacters have no interchange meaning; fail closed
            # before paths reach filesystems or external Git APIs.
            or any(0xFDD0 <= ord(ch) <= 0xFDEF or
                   (ord(ch) & 0xFFFE) == 0xFFFE for ch in raw)
            or any(part.endswith((" ", ".")) for part in parts)
            # Never allow the guarded writer to alter Git internals or
            # repository automation configuration via a proposed data path.
            or any(part in (".git", ".github") for part in normalized_parts)
            or any(part in (".gitmodules", ".gitattributes", ".gitignore",
                            ".mailmap") for part in normalized_parts)
            # NFKC can turn fullwidth/compatibility punctuation into a colon.
            # Windows interprets colons as alternate data stream separators.
            or ":" in name or ":" in folded
            or "\x00" in name
            or name.startswith("~")
            or folded in {item.casefold() for item in PROTECTED_EXACT}
            or any(part in {item.casefold() for item in PROTECTED_EXACT}
                   for part in normalized_parts)
            or any(folded.startswith(prefix.casefold()) for prefix in PROTECTED_PREFIXES)
            or PurePosixPath(folded).suffix in (".m3u", ".m3u8")
            or PurePosixPath(folded).stem in ("favoriler", "favorites", "hepsi")
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


def _enforce_local_path(destination: Path, *, allowed_root: Path | None,
                        allow_existing_regular_file: bool) -> dict:
    """K1 local output preflight; reject protected ancestors and symlinks.

    Does not authorize production writes or intercept unrelated callers.
    """
    # Validate the caller's lexical path before pathlib normalizes dot segments.
    raw = str(destination)
    raw_parts = raw.replace(chr(92), "/").split("/")
    if (chr(92) in raw or any(unicodedata.category(ch) in ("Cc", "Cf", "Cs", "Zl", "Zp") for ch in raw)
            or any(part in (".", "..") for part in raw_parts)):
        raise ProtectedWriteRejected("Ambiguous or traversing output path")
    path = Path(destination)
    if not path.is_absolute():
        raise ProtectedWriteRejected("Output must be an absolute path")
    if any(part in (".", "..") for part in path.parts) or str(path) != str(path.absolute()):
        raise ProtectedWriteRejected("Ambiguous or traversing output path")
    if path.is_symlink():
        raise ProtectedWriteRejected("Symlink output")
    if path.exists():
        metadata = path.lstat()
        if (not allow_existing_regular_file or not stat.S_ISREG(metadata.st_mode)
                or metadata.st_nlink != 1):
            raise ProtectedWriteRejected("Existing, nonregular or hardlinked output")
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
        # An allowed root nested below a symlink must not bypass the
        # ancestor check merely because the root itself is not a link.
        if any(ancestor.is_symlink() for ancestor in root.parents):
            raise ProtectedWriteRejected("Symlinked allowed output root ancestor")
        if not path.is_relative_to(root) or path == root:
            raise ProtectedWriteRejected("Output outside allowed root")
        relative = path.relative_to(root).as_posix()
    else:
        relative = path.relative_to(path.anchor).as_posix()
    # A caller-chosen allowed root must not hide protected ancestor names.
    enforce_write_paths([path.relative_to(path.anchor).as_posix()])
    enforce_write_paths([relative])
    return {"path_checked": True, "production_writes": False,
            "production_write_allowed": False}


def enforce_local_output_path(destination: Path, *, allowed_root: Path | None = None) -> dict:
    """Validate a new evidence path; never permit replacing existing data."""
    return _enforce_local_path(destination, allowed_root=allowed_root,
                               allow_existing_regular_file=False)


def enforce_local_append_path(destination: Path, *, allowed_root: Path | None = None) -> dict:
    """Preflight a summary append, optionally confined to an explicit sandbox.

    Existing targets must be regular files with a single hardlink. Callers
    should pass allowed_root for isolated writes; this is not an atomic writer
    and does not authorize production writes or intercept other processes.
    """
    return _enforce_local_path(destination, allowed_root=allowed_root,
                               allow_existing_regular_file=True)


def enforce_local_turkish_tv_test_playlist(destination: Path, *, allowed_root: Path) -> dict:
    """Permit one isolated K3 artifact without weakening the general M3U ban."""
    root = Path(allowed_root).absolute()
    expected = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
    if Path(destination) != expected:
        raise ProtectedWriteRejected("Only the fixed isolated K3 test playlist is permitted")
    # Reuse all local boundary checks, substituting a harmless JSON name solely
    # for the repository-path suffix policy.  The exact real destination was
    # checked above and is returned in the evidence.
    policy_probe = root / "reports/turkish-tv-test-playlist-boundary.json"
    result = _enforce_local_path(policy_probe, allowed_root=root,
                                 allow_existing_regular_file=False)
    if expected.exists() or expected.is_symlink():
        raise ProtectedWriteRejected("Existing test playlist evidence")
    return {**result, "path_checked": True, "isolated_test_playlist": True}
