"""K1/K5 fail-closed behavioral parity evidence ledger for legacy workflows.

Inventory is not proof. Only independently supplied evidence can advance acceptance.
"""
REQUIRED = ("legacy_execution", "new_execution", "input_output_comparison",
            "side_effect_comparison", "failure_timeout_comparison", "reviewer_approval")
def validate_inventory(inventory):
    if not isinstance(inventory, dict):
        raise ValueError("Inventory must be an object")
    rows = inventory.get("workflows")
    if not isinstance(rows, list) or len(rows) != 99:
        raise ValueError("Expected exactly 99 source workflow rows")
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError("Workflow rows must be objects")
    paths = [row.get("path") for row in rows]
    if (not all(isinstance(x, str) for x in paths) or len(set(paths)) != 99
            or not all(x.startswith(".github/workflows/") and x.endswith((".yml", ".yaml"))
                       and x.count("/") == 2 and ".." not in x and "\\" not in x
                       for x in paths)):
        raise ValueError("Invalid or duplicate workflow paths")
    if inventory.get("source_repository") != "Madsc55/madsc-tv":
        raise ValueError("Wrong legacy source repository")
    if inventory.get("source_branch") != "madsc/bes-sistem-toplu-birlestirme":
        raise ValueError("Wrong legacy source branch")
    return rows

def ledger(inventory, evidence=None):
    rows = validate_inventory(inventory)
    evidence = {} if evidence is None else evidence
    if not isinstance(evidence, dict) or set(evidence) - {r["path"] for r in rows}:
        raise ValueError("Unknown workflow evidence")
    if any(not isinstance(proofs, dict) or set(proofs) - set(REQUIRED)
           for proofs in evidence.values()):
        raise ValueError("Invalid proof keys")
    output = []
    for row in rows:
        path = row["path"]
        proofs = evidence.get(path, {})
        if not isinstance(proofs, dict) or set(proofs) - set(REQUIRED):
            raise ValueError("Invalid proof keys")
        valid_proofs = all(
            isinstance(proofs.get(key), dict)
            and isinstance(proofs[key].get("sha256"), str)
            and len(proofs[key]["sha256"]) == 64
            and all(c in "0123456789abcdef" for c in proofs[key]["sha256"])
            and type(proofs[key].get("run_id")) is int
            and proofs[key]["run_id"] > 0
            for key in REQUIRED
        )
        # Evidence metadata alone cannot certify behavior. An independent
        # verifier must supply a future approval token; this ledger is blocked.
        accepted = False
        invalid = [k for k in REQUIRED if k in proofs and not (
            isinstance(proofs[k], dict)
            and isinstance(proofs[k].get("sha256"), str)
            and len(proofs[k]["sha256"]) == 64
            and all(ch in "0123456789abcdef" for ch in proofs[k]["sha256"])
            and type(proofs[k].get("run_id")) is int
            and proofs[k]["run_id"] > 0
        )]
        output.append({"path": path, "stages": row.get("candidate_k_stages", []),
                       "accepted": accepted, "evidence_metadata_complete": valid_proofs,
                       "missing": [k for k in REQUIRED if k not in proofs],
                       "invalid": invalid,
                       "independent_verification": "not_implemented"})
    return {"total": len(rows),
            "metadata_complete": sum(r["evidence_metadata_complete"] for r in output),
            "missing_evidence_fields": sum(len(r["missing"]) for r in output),
            "invalid_evidence_fields": sum(len(r["invalid"]) for r in output),
            "accepted": sum(r["accepted"] for r in output),
            "blocked": sum(not r["accepted"] for r in output), "rows": output}


def compare_execution_snapshots(legacy, replacement):
    """Compare independently captured, bounded execution facts without running either workflow.

    Caller supplies snapshots from separate executions. Matching snapshots are
    comparison evidence only, never approval or proof of execution provenance.
    """
    required = ("exit_code", "timed_out", "outputs", "side_effects")
    for snapshot in (legacy, replacement):
        if not isinstance(snapshot, dict) or set(snapshot) != set(required):
            raise ValueError("Incomplete execution snapshot")
        if type(snapshot["exit_code"]) is not int or not -255 <= snapshot["exit_code"] <= 255:
            raise ValueError("Invalid exit code")
        if type(snapshot["timed_out"]) is not bool:
            raise ValueError("Invalid timeout flag")
        for field in ("outputs", "side_effects"):
            values = snapshot[field]
            if not isinstance(values, dict) or len(values) > 1000:
                raise ValueError("Invalid snapshot field")
            if any(not isinstance(key, str) or not key or len(key) > 512
                   or not isinstance(value, str) or len(value) != 64
                   or any(char not in "0123456789abcdef" for char in value)
                   for key, value in values.items()):
                raise ValueError("Snapshot values must be SHA256 digests")
    differences = {}
    for field in required:
        if legacy[field] != replacement[field]:
            if field in ("outputs", "side_effects"):
                keys = sorted(set(legacy[field]) | set(replacement[field]))
                differences[field] = [key for key in keys
                                      if legacy[field].get(key) != replacement[field].get(key)]
            else:
                differences[field] = {"legacy": legacy[field], "replacement": replacement[field]}
    return {"snapshot_fields_match": not differences, "differences": differences,
            "behavioral_parity_accepted": False, "provenance_verified": False}
