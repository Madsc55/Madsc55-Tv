"""Fail-closed K5 frozen-source inventory audit (no network, no workflow dispatch)."""
import json
from pathlib import Path

from madsc.fixture_report_writer import write_exclusive_bytes
from madsc.write_path_audit import enforce_local_output_path

PARTS = ("01_18", "19_36", "37_54", "55_72", "73_90", "91_92")
EXCLUDED = {
    "madsc-01-guvenlik.yml", "madsc-02-kesif.yml", "madsc-03-kanal-test.yml",
    "madsc-04-arsiv-yedek.yml", "madsc-05-genel-bakim.yml",
    "k1-protected-write-tests.yml", "madsc-hizli-on-kontrol.yml",
}


def write_source_audit_report(destination: Path, payload: str) -> None:
    """Create one K1-guarded audit report without following output links."""
    destination = Path(destination).absolute()
    enforce_local_output_path(destination)
    write_exclusive_bytes(destination, payload.encode("utf-8"))


def audit(root):
    root = Path(root)
    errors = []
    try:
        inventory = json.loads((root / "docs/LEGACY_SOURCE_SCOPE.json").read_text(encoding="utf-8"))
        if not isinstance(inventory, dict):
            raise ValueError("inventory must be an object")
    except (OSError, ValueError) as exc:
        return {"source_audit_passed": False, "production_accepted": False,
                "behavioral_parity_accepted": 0,
                "errors": ["missing_or_invalid_inventory:" + type(exc).__name__]}
    source_rows = inventory.get("workflows", [])
    if not isinstance(source_rows, list):
        source_rows = []
        errors.append("invalid_inventory")
    inventory_paths = [r.get("path") for r in source_rows if isinstance(r, dict)]
    if any(not isinstance(path, str) for path in inventory_paths):
        errors.append("invalid_inventory_path")
    if (len(inventory_paths) != len(source_rows)
            or len({str(path) for path in inventory_paths}) != len(inventory_paths)):
        errors.append("invalid_or_duplicate_inventory_paths")
    for row in source_rows:
        if (not isinstance(row, dict)
                or not isinstance(row.get("path"), str)
                or not isinstance(row.get("git_blob_sha"), str)
                or len(row["git_blob_sha"]) != 40
                or any(c not in "0123456789abcdef" for c in row["git_blob_sha"])):
            errors.append("invalid_inventory_row")
    excluded_seen = {Path(path).name for path in inventory_paths
                     if isinstance(path, str) and Path(path).name in EXCLUDED}
    if excluded_seen != EXCLUDED:
        errors.append("excluded_scope_mismatch")
    expected = {r["path"]: r["git_blob_sha"] for r in source_rows
                if isinstance(r, dict) and isinstance(r.get("path"), str)
                and isinstance(r.get("git_blob_sha"), str)
                and Path(r["path"]).name not in EXCLUDED}
    rows = []
    for part in PARTS:
        path = root / ("docs/K5_KAYNAK_DOGRULAMA_" + part + ".json")
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append("missing_or_invalid_part:" + part + ":" + type(exc).__name__)
            continue
        if not isinstance(doc, dict):
            errors.append("invalid_part_object:" + part)
            continue
        if doc.get("source_commit") != inventory.get("source_commit"):
            errors.append("wrong_commit:" + part)
        if not isinstance(doc.get("rows"), list):
            errors.append("invalid_rows:" + part)
            continue
        rows.extend(doc["rows"])
    seen = set()
    verified_paths = set()
    allowed_stages = {"K1", "K2", "K3", "K4", "K5"}
    required_signals = {"write", "push", "dispatch", "playlist", "epg",
                        "live", "backup", "artifact", "gate"}
    for row in rows:
        if not isinstance(row, dict):
            errors.append("invalid_row")
            continue
        path = row.get("path")
        if not isinstance(path, str):
            errors.append("invalid_path")
            continue
        if path in seen:
            errors.append("duplicate:" + str(path))
        seen.add(path)
        if path not in expected:
            errors.append("unknown:" + str(path))
        elif (row.get("sha") != expected[path]
              or row.get("expected_sha") != expected[path]
              or row.get("verified") is not True):
            errors.append("sha_mismatch:" + path)
        if (path in expected and row.get("sha") == expected[path]
                and row.get("expected_sha") == expected[path]
                and row.get("verified") is True):
            verified_paths.add(path)
        signals = row.get("signals")
        stages = row.get("candidate_stages")
        if (not isinstance(signals, dict) or set(signals) != required_signals
                or any(type(value) is not bool for value in signals.values())
                or not isinstance(stages, list) or not stages
                or len(set(map(str, stages))) != len(stages)
                or any(type(stage) is not str or stage not in allowed_stages for stage in stages)):
            errors.append("invalid_signals:" + str(path))
    if set(inventory_paths) != set(expected) | {path for path in inventory_paths if isinstance(path, str) and Path(path).name in EXCLUDED}:
        errors.append("inventory_scope_inconsistent")
    for path in sorted(set(expected) - seen):
        errors.append("missing:" + path)
    if len(source_rows) != 99 or len(expected) != 92 or len(rows) != 92:
        errors.append("wrong_scope_count")
    signal_counts = {key: sum(1 for row in rows
                              if isinstance(row, dict)
                              and isinstance(row.get("signals"), dict)
                              and row["signals"].get(key) is True)
                     for key in sorted(required_signals)}
    return {
        "source_commit": inventory.get("source_commit"),
        "expected": len(expected), "recorded": len(rows),
        "verified_source_rows": len(verified_paths),
        "source_audit_passed": not errors,
        "yaml_signal_counts": signal_counts,
        "static_mapping_only": True,
        "independent_old_new_execution_pairs": 0,
        "behavioral_evidence_missing": len(expected),
        "behavioral_parity_accepted": 0,
        "production_accepted": False,
        "errors": errors,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = audit(args.root)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        write_source_audit_report(Path(args.output), payload)
    print(payload, end="")
    raise SystemExit(0 if result["source_audit_passed"] else 1)


if __name__ == "__main__":
    main()
