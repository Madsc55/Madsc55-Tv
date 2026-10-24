"""Offline, fail-closed comparison of independently captured legacy/new workflow evidence.

This tool never runs workflows, accesses the network, or writes production data.
Evidence must come from separately executed, isolated fixture runs.
"""
import argparse
import json
import re
from pathlib import Path, PurePosixPath

FIELDS = ("exit_code", "stdout_sha256", "stderr_sha256", "artifacts", "side_effects", "timed_out", "retry_count")
DIGEST = set("0123456789abcdef")
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$")


def _digest(value):
    return isinstance(value, str) and len(value) == 64 and set(value) <= DIGEST


def _safe_relative_name(name):
    if (not isinstance(name, str) or not name or len(name) > 1024
            or any(ord(char) < 32 or ord(char) == 127 for char in name)
            or chr(92) in name):
        return False
    path = PurePosixPath(name)
    return (not path.is_absolute() and all(part not in ("", ".", "..") for part in name.split("/"))
            and path.as_posix() == name)


def _valid(record):
    if not isinstance(record, dict) or set(record) != set(FIELDS):
        return False
    if type(record["exit_code"]) is not int or type(record["retry_count"]) is not int or record["retry_count"] < 0:
        return False
    if record["retry_count"] > 100 or not (-255 <= record["exit_code"] <= 255):
        return False
    if type(record["timed_out"]) is not bool:
        return False
    if not _digest(record["stdout_sha256"]) or not _digest(record["stderr_sha256"]):
        return False
    for field in ("artifacts", "side_effects"):
        value = record[field]
        if (not isinstance(value, dict) or len(value) > 10000
                or any(not _safe_relative_name(k) or not _digest(v) for k, v in value.items())):
            return False
    return True


def compare(document):
    errors = []
    if not isinstance(document, dict) or set(document) != {"workflow", "fixture_sha256", "legacy", "new", "independent_runs", "isolated_fixture", "legacy_run_id", "new_run_id", "legacy_commit_sha", "new_commit_sha"}:
        return {"matched_evidence": False, "accepted": False,
                "requires_independent_execution_verification": False,
                "errors": ["invalid_evidence_schema"]}
    workflow = document["workflow"]
    if (not _safe_relative_name(workflow) or not workflow.endswith((".yml", ".yaml"))
            or not workflow.startswith(".github/workflows/")
            or len(PurePosixPath(workflow).parts) != 3):
        errors.append("invalid_workflow")
    if not _digest(document["fixture_sha256"]):
        errors.append("invalid_fixture_digest")
    if document["independent_runs"] is not True or document["isolated_fixture"] is not True:
        errors.append("independence_or_isolation_unproven")
    for field in ("legacy_run_id", "new_run_id"):
        value = document[field]
        if not isinstance(value, str) or not RUN_ID_PATTERN.fullmatch(value):
            errors.append("invalid_" + field)
    if document.get("legacy_run_id") == document.get("new_run_id"):
        errors.append("run_ids_not_independent")
    for field in ("legacy_commit_sha", "new_commit_sha"):
        value = document[field]
        if not isinstance(value, str) or len(value) != 40 or any(c not in DIGEST for c in value):
            errors.append("invalid_" + field)
    for side in ("legacy", "new"):
        if not _valid(document[side]):
            errors.append("invalid_" + side + "_record")
    if not errors:
        for side in ("legacy", "new"):
            record = document[side]
            if record["timed_out"] and record["exit_code"] == 0:
                errors.append("inconsistent_timeout:" + side)
        for field in FIELDS:
            if document["legacy"][field] != document["new"][field]:
                errors.append("mismatch:" + field)
    # A JSON claim cannot attest that two executions were actually independent.
    # Only a separately verified execution harness may grant behavioral acceptance.
    return {"matched_evidence": not errors, "accepted": False,
            "requires_independent_execution_verification": not errors, "errors": errors}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.evidence.read_text(encoding="utf-8"))
        result = compare(document)
    except (OSError, ValueError) as exc:
        result = {"matched_evidence": False, "accepted": False,
                  "requires_independent_execution_verification": False,
                  "errors": ["unreadable_evidence:" + type(exc).__name__]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["accepted"] else 1)


if __name__ == "__main__":
    main()
