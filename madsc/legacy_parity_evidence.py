"""K1/K5 fail-closed behavioral parity evidence ledger for legacy workflows.

Inventory is not proof. Only independently supplied evidence can advance acceptance.
"""
REQUIRED = ("legacy_execution", "new_execution", "input_output_comparison",
            "side_effect_comparison", "failure_timeout_comparison", "reviewer_approval")
def validate_inventory(inventory):
    rows = inventory.get("workflows")
    if not isinstance(rows, list) or len(rows) != 99:
        raise ValueError("Expected exactly 99 source workflow rows")
    paths = [row.get("path") for row in rows]
    if len(set(paths)) != 99 or not all(isinstance(x, str) and x.startswith(".github/workflows/") for x in paths):
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
        output.append({"path": path, "stages": row.get("candidate_k_stages", []),
                       "accepted": accepted, "evidence_metadata_complete": valid_proofs,
                       "missing": [k for k in REQUIRED if k not in proofs],
                       "independent_verification": "not_implemented"})
    return {"total": len(rows), "accepted": sum(r["accepted"] for r in output),
            "blocked": sum(not r["accepted"] for r in output), "rows": output}
