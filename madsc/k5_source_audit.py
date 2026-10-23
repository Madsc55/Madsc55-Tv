"""Fail-closed K5 frozen-source inventory audit (no network, no workflow dispatch)."""
import json
from pathlib import Path

PARTS = ("01_18", "19_36", "37_54", "55_72", "73_90", "91_92")
EXCLUDED = {
    "madsc-01-guvenlik.yml", "madsc-02-kesif.yml", "madsc-03-kanal-test.yml",
    "madsc-04-arsiv-yedek.yml", "madsc-05-genel-bakim.yml",
    "k1-protected-write-tests.yml", "madsc-hizli-on-kontrol.yml",
}


def audit(root):
    root = Path(root)
    inventory = json.loads((root / "docs/LEGACY_SOURCE_SCOPE.json").read_text(encoding="utf-8"))
    expected = {r["path"]: r["git_blob_sha"] for r in inventory["workflows"]
                if Path(r["path"]).name not in EXCLUDED}
    errors = []
    rows = []
    for part in PARTS:
        path = root / ("docs/K5_KAYNAK_DOGRULAMA_" + part + ".json")
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append("missing_or_invalid_part:" + part + ":" + type(exc).__name__)
            continue
        if doc.get("source_commit") != inventory["source_commit"]:
            errors.append("wrong_commit:" + part)
        if not isinstance(doc.get("rows"), list):
            errors.append("invalid_rows:" + part)
            continue
        rows.extend(doc["rows"])
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("invalid_row")
            continue
        path = row.get("path")
        if path in seen:
            errors.append("duplicate:" + str(path))
        seen.add(path)
        if path not in expected:
            errors.append("unknown:" + str(path))
        elif (row.get("sha") != expected[path]
              or row.get("expected_sha") != expected[path]
              or row.get("verified") is not True):
            errors.append("sha_mismatch:" + path)
        if not isinstance(row.get("signals"), dict) or not isinstance(row.get("candidate_stages"), list):
            errors.append("invalid_signals:" + str(path))
    for path in sorted(set(expected) - seen):
        errors.append("missing:" + path)
    if len(inventory["workflows"]) != 99 or len(expected) != 92 or len(rows) != 92:
        errors.append("wrong_scope_count")
    return {
        "source_commit": inventory["source_commit"],
        "expected": len(expected), "recorded": len(rows),
        "verified_source_rows": sum(1 for r in rows if isinstance(r, dict)
                                    and r.get("path") in expected
                                    and r.get("sha") == expected[r["path"]]
                                    and r.get("expected_sha") == expected[r["path"]]
                                    and r.get("verified") is True),
        "source_audit_passed": not errors,
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
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["source_audit_passed"] else 1)


if __name__ == "__main__":
    main()
