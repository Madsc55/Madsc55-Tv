"""Strict read-only download and extraction of an independently verified GitHub artifact."""
import hashlib
import io
import json
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

from madsc.history_pair_store import KEYS
from madsc.history_pair_bridge import import_legacy_pair


def extract_verified_history(archive, expected_hashes, destination):
    if not isinstance(expected_hashes, dict) or set(expected_hashes) != set(KEYS):
        raise ValueError("Missing expected SHA256 hashes")
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError("Destination must not exist")
    if len(archive) > 16 * 1024 * 1024:
        raise ValueError("Oversized history artifact")
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        files = z.infolist()
        if len(files) != len(KEYS) or {x.filename for x in files} != set(KEYS):
            raise ValueError("Unexpected artifact files")
        validated = {}
        for entry in files:
            if entry.is_dir() or entry.file_size > 8 * 1024 * 1024:
                raise ValueError("Unsafe history entry")
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Symlink in history archive")
            raw = z.read(entry)
            if hashlib.sha256(raw).hexdigest() != expected_hashes[entry.filename]:
                raise ValueError("History artifact content mismatch")
            validated[entry.filename] = raw
    # Validate all bytes before any file is written.
    decoded = {name: json.loads(raw) for name, raw in validated.items()}
    if not all(isinstance(value, dict) for value in decoded.values()):
        raise ValueError("Invalid history JSON")
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in validated.items():
        (destination / name).write_bytes(raw)
    return import_legacy_pair(destination)


def download_verified_history_artifact(*, repository, artifact_id, token, expected_hashes,
                                       destination, opener=urlopen):
    if repository != "Madsc55/Madsc55-Tv" or type(artifact_id) is not int or artifact_id <= 0:
        raise ValueError("Unexpected repository or artifact")
    if not token:
        raise ValueError("GitHub token required for artifact download")
    url = f"https://api.github.com/repos/{repository}/actions/artifacts/{artifact_id}/zip"
    request = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "User-Agent": "madsc55-history-source"}, method="GET")
    with opener(request, timeout=30) as response:
        archive = response.read(16 * 1024 * 1024 + 1)
    return extract_verified_history(archive, expected_hashes, destination)
