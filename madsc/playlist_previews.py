"""K5 offline M3U previews from K2/K3 catalog; never write live playlists."""
from __future__ import annotations

from madsc.discovery import normalize_url
from hashlib import sha256

BUCKETS = ("IBO_ONAYLI_CALISAN", "CALISAN_ADAY", "CALISMAYAN_ADAY",
           "YABANCI", "TEST_BEKLIYOR")


def _attribute(value: str) -> str:
    if not isinstance(value, str) or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError("Unsafe M3U metadata")
    return value.replace("&", "&amp;").replace('"', "&quot;")


def render_playlist_previews(catalog: dict, source_rows: list[dict]) -> dict:
    """Return separate in-memory drafts; never treat preliminary tests as acceptance."""
    if not isinstance(catalog, dict) or not isinstance(source_rows, list):
        raise ValueError("Invalid catalog or source rows")
    if catalog.get("production_writes") is not False or catalog.get("production_ready") is not False:
        raise ValueError("Playlist preview requires a read-only, non-production catalog")
    entries = catalog.get("channels")
    if not isinstance(entries, list):
        raise ValueError("Missing catalog channels")
    output = {bucket: ["#EXTM3U"] for bucket in BUCKETS}
    seen_indices = set()
    seen_digests = set()
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("bucket") not in output:
            raise ValueError("Unknown channel category")
        index = entry.get("source_index")
        if type(index) is not int or not 0 <= index < len(source_rows):
            raise ValueError("Invalid source reference")
        if index in seen_indices:
            raise ValueError("Duplicate catalog source reference")
        seen_indices.add(index)
        source = source_rows[index]
        if not isinstance(source, dict):
            raise ValueError("Invalid source row")
        url = normalize_url(source["url"])
        digest = sha256(url.encode("utf-8")).hexdigest()
        if digest != entry.get("url_sha256"):
            raise ValueError("Catalog and source fingerprint mismatch")
        if digest in seen_digests:
            raise ValueError("Duplicate stream in playlist preview")
        seen_digests.add(digest)
        for key in ("display_name", "tvg_id", "group_title"):
            if not isinstance(entry.get(key), str):
                raise ValueError("Invalid channel metadata")
        name = entry["display_name"]
        if not isinstance(name, str) or not name or "\\" in name or any(ord(ch) < 32 or ord(ch) == 127 for ch in name):
            raise ValueError("Unsafe channel name")
        logo = entry.get("logo_url") or ""
        if logo and (entry.get("logo_verified") is not True or
                     not isinstance(logo, str) or not logo.startswith("https://")):
            raise ValueError("Unverified logo")
        attrs = (f'tvg-id="{_attribute(entry["tvg_id"])}" '
                 f'tvg-logo="{_attribute(logo)}" '
                 f'group-title="{_attribute(entry["group_title"])}"')
        output[entry["bucket"]].extend([f"#EXTINF:-1 {attrs},{name}", url])
    return {"drafts": {bucket: "\n".join(lines) + "\n" for bucket, lines in output.items()},
            "counts": {bucket: (len(lines) - 1) // 2 for bucket, lines in output.items()},
            "preview_only": True, "device_verified_by_this_function": False,
            "production_writes": False, "production_change_allowed": False}


def preview_imported_m3u(source, *, measurements=None, logos=None,
                         ibo_results=None, probes=None, three_stage=None) -> dict:
    """Read a local M3U and produce K2/K3/K5 drafts without any file writes or probes.

    Evidence is caller-supplied, never inferred from an unverified stream.
    """
    from madsc.source_import import extract_candidates
    from madsc.channel_catalog import prepare_channel_catalog

    inventory = extract_candidates(source)
    rows = inventory["source_rows"]
    catalog = prepare_channel_catalog(rows, measurements=measurements, logos=logos,
                                      ibo_results=ibo_results, probes=probes,
                                      three_stage=three_stage)
    previews = render_playlist_previews(catalog, rows)
    return {"source_channel_count": inventory["source_channel_count"],
            "duplicate_count": inventory["duplicate_channel_count"],
            "rejected_count": inventory["rejected_channel_count"],
            "catalog_summary": catalog["summary"], **previews}


def main(argv=None) -> int:
    """Offline CLI: print preview JSON to stdout, never write source or output files."""
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Offline K2/K3/K5 M3U playlist previews")
    parser.add_argument("source", type=Path, help="Local read-only .m3u/.m3u8 source")
    args = parser.parse_args(argv)
    report = preview_imported_m3u(args.source)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
