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
    if any(type(row.get("candidate_k_stages", [])) is not list
           or any(type(stage) is not str or stage not in {"K1", "K2", "K3", "K4", "K5"}
                  for stage in row.get("candidate_k_stages", []))
           for row in rows):
        raise ValueError("Invalid candidate K stage mapping")
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


def compare_snapshot_batch(inventory, snapshots):
    """Compare provided execution pairs for all 99 inventoried workflows.

    Unsubmitted pairs remain blocked; even matching pairs cannot prove origin
    or authorize production acceptance.
    """
    rows = validate_inventory(inventory)
    paths = {row["path"] for row in rows}
    if not isinstance(snapshots, dict) or set(snapshots) - paths:
        raise ValueError("Unknown snapshot workflow")
    # Validate every supplied pair before generating any report rows.
    comparisons = {}
    for path, pair in snapshots.items():
        if not isinstance(pair, dict) or set(pair) != {"legacy", "replacement"}:
            raise ValueError("Incomplete execution pair")
        comparisons[path] = compare_execution_snapshots(pair["legacy"], pair["replacement"])
    results = []
    for row in rows:
        path = row["path"]
        if path not in snapshots:
            results.append({"path": path, "status": "missing_execution_pair",
                            "behavioral_parity_accepted": False})
            continue
        comparison = comparisons[path]
        results.append({"path": path,
                        "status": ("snapshot_match_unverified" if comparison["snapshot_fields_match"]
                                   else "snapshot_mismatch"),
                        **comparison})
    return {"total": len(rows), "pairs_supplied": len(snapshots),
            "snapshot_matches": sum(r["status"] == "snapshot_match_unverified" for r in results),
            "snapshot_mismatches": sum(r["status"] == "snapshot_mismatch" for r in results),
            "missing_pairs": sum(r["status"] == "missing_execution_pair" for r in results),
            "behavioral_parity_accepted": 0, "rows": results}


CENTRAL_REPLACEMENT_WORKFLOWS = frozenset({
    f".github/workflows/madsc-0{stage}-{name}.yml"
    for stage, name in ((1, "guvenlik"), (2, "kesif"), (3, "kanal-test"),
                        (4, "yedek"), (5, "bakim"))
})


def _lower_hex(value, size):
    return (isinstance(value, str) and len(value) == size
            and all(char in "0123456789abcdef" for char in value))


def _validate_execution_origin(origin, *, role, legacy_path, legacy_blob_sha):
    required = {"repository", "branch", "workflow_path", "workflow_blob_sha",
                "run_id", "run_attempt", "head_sha", "event", "conclusion",
                "artifact", "input_sha256", "snapshot"}
    if not isinstance(origin, dict) or set(origin) != required:
        raise ValueError("Incomplete execution origin")
    expected_repository = "Madsc55/madsc-tv" if role == "legacy" else "Madsc55/Madsc55-Tv"
    expected_branch = "madsc/bes-sistem-toplu-birlestirme" if role == "legacy" else "main"
    if origin["repository"] != expected_repository or origin["branch"] != expected_branch:
        raise ValueError("Execution repository or branch mismatch")
    if any(type(origin[key]) is not str for key in
           ("repository", "branch", "workflow_path", "event", "conclusion")):
        raise ValueError("Invalid execution identity types")
    if role == "legacy":
        if (not _lower_hex(legacy_blob_sha, 40)
                or origin["workflow_path"] != legacy_path
                or origin["workflow_blob_sha"] != legacy_blob_sha):
            raise ValueError("Legacy workflow is not bound to pinned source")
    elif (origin["workflow_path"] not in CENTRAL_REPLACEMENT_WORKFLOWS
          or not _lower_hex(origin["workflow_blob_sha"], 40)):
        raise ValueError("Replacement workflow is not one of the five central systems")
    if (type(origin["run_id"]) is not int or origin["run_id"] <= 0
            or type(origin["run_attempt"]) is not int or origin["run_attempt"] <= 0
            or not _lower_hex(origin["head_sha"], 40)
            or origin["event"] not in {"workflow_dispatch", "workflow_call", "push", "schedule"}
            or origin["conclusion"] not in {"success", "failure", "cancelled", "timed_out"}
            or not _lower_hex(origin["input_sha256"], 64)):
        raise ValueError("Invalid execution identity")
    artifact = origin["artifact"]
    if (not isinstance(artifact, dict)
            or set(artifact) != {"id", "name", "repository", "run_id", "head_sha", "sha256"}
            or type(artifact["id"]) is not int or artifact["id"] <= 0
            or not isinstance(artifact["name"], str) or not artifact["name"]
            or len(artifact["name"]) > 256
            or artifact["repository"] != origin["repository"]
            or artifact["run_id"] != origin["run_id"]
            or artifact["head_sha"] != origin["head_sha"]
            or not _lower_hex(artifact["sha256"], 64)):
        raise ValueError("Artifact is not bound to its execution origin")
    compare_execution_snapshots(origin["snapshot"], origin["snapshot"])
    return origin


def compare_provenance_bound_pair(legacy_path, legacy_blob_sha, pair, *,
                                  replacement_workflow_root=None):
    """Validate a same-input, separately originated legacy/replacement pair.

    Supplied metadata is structurally bound but is not independently verified
    against GitHub APIs here, so this function can never grant acceptance.
    """
    if not isinstance(pair, dict) or set(pair) != {"legacy", "replacement"}:
        raise ValueError("Incomplete provenance-bound execution pair")
    legacy = _validate_execution_origin(
        pair["legacy"], role="legacy", legacy_path=legacy_path,
        legacy_blob_sha=legacy_blob_sha)
    replacement = _validate_execution_origin(
        pair["replacement"], role="replacement", legacy_path=legacy_path,
        legacy_blob_sha=legacy_blob_sha)
    if legacy["input_sha256"] != replacement["input_sha256"]:
        raise ValueError("Execution pair does not use the same input hash")
    legacy_execution = (legacy["repository"], legacy["run_id"], legacy["run_attempt"])
    replacement_execution = (replacement["repository"], replacement["run_id"],
                             replacement["run_attempt"])
    legacy_artifact = (legacy["artifact"]["repository"], legacy["artifact"]["id"])
    replacement_artifact = (replacement["artifact"]["repository"],
                            replacement["artifact"]["id"])
    if legacy_execution == replacement_execution or legacy_artifact == replacement_artifact:
        raise ValueError("Execution and artifact origins must be independent")
    preflight = None
    if replacement_workflow_root is not None:
        from madsc.parity_workflow_readiness import preflight_replacement_execution
        preflight = preflight_replacement_execution(replacement_workflow_root, replacement)
    comparison = compare_execution_snapshots(legacy["snapshot"], replacement["snapshot"])
    return {
        "same_input_sha256": legacy["input_sha256"],
        "replacement_workflow_contract_checked": preflight is not None,
        "replacement_static_preflight": preflight,
        "execution_origins_distinct": True,
        "artifact_origins_distinct": True,
        "origin_binding_complete": True,
        "independent_origin_api_verified": False,
        **comparison,
        "provenance_verified": False,
        "behavioral_parity_accepted": False,
    }


def compare_provenance_bound_batch(inventory, pairs, *, replacement_workflow_root=None):
    """Compare only the pinned 92 behavior workflows with origin-bound pairs."""
    scope = reconcile_legacy_scope(inventory)
    legacy_paths = set(scope["legacy_paths"])
    if not isinstance(pairs, dict) or set(pairs) - legacy_paths:
        raise ValueError("Unknown or excluded workflow pair")
    by_path = {row["path"]: row for row in validate_inventory(inventory)}
    comparisons = {
        path: compare_provenance_bound_pair(
            path, by_path[path].get("git_blob_sha"), pair,
            replacement_workflow_root=replacement_workflow_root)
        for path, pair in pairs.items()
    }
    rows = []
    for path in scope["legacy_paths"]:
        if path not in comparisons:
            rows.append({"path": path, "status": "missing_provenance_bound_pair",
                         "behavioral_parity_accepted": False})
            continue
        comparison = comparisons[path]
        rows.append({"path": path,
                     "status": ("snapshot_match_origin_unverified"
                                if comparison["snapshot_fields_match"]
                                else "snapshot_mismatch_origin_unverified"),
                     **comparison})
    return {
        "schema": "madsc-legacy-provenance-pairs-v1",
        "total": 92,
        "pairs_supplied": len(pairs),
        "origin_bindings_complete": sum(
            row.get("origin_binding_complete") is True for row in rows),
        "snapshot_matches": sum(
            row["status"] == "snapshot_match_origin_unverified" for row in rows),
        "snapshot_mismatches": sum(
            row["status"] == "snapshot_mismatch_origin_unverified" for row in rows),
        "missing_pairs": sum(
            row["status"] == "missing_provenance_bound_pair" for row in rows),
        "replacement_workflow_contracts_checked": sum(
            row.get("replacement_workflow_contract_checked") is True for row in rows),
        "independent_origins_api_verified": 0,
        "behavioral_parity_accepted": 0,
        "production_ready": False,
        "rows": rows,
    }


# Exact exclusions from pinned legacy five_category_92_workflow_audit.py.
# Count reconciliation is source evidence, never behavioral acceptance.
SCOPE_EXCLUSIONS = frozenset({
    "madsc-01-guvenlik.yml", "madsc-02-kesif.yml", "madsc-03-kanal-test.yml",
    "madsc-04-arsiv-yedek.yml", "madsc-05-genel-bakim.yml",
    "k1-protected-write-tests.yml", "madsc-hizli-on-kontrol.yml",
})


def reconcile_legacy_scope(inventory):
    rows = validate_inventory(inventory)
    if inventory.get("source_commit") != "ca374df3b9585c0d76a078db9536150ebbc260f7":
        raise ValueError("Legacy scope must use the pinned source commit")
    if any(not _lower_hex(row.get("git_blob_sha"), 40)
           or type(row.get("bytes")) is not int or row["bytes"] <= 0
           for row in rows):
        raise ValueError("Legacy scope requires source blob identities and sizes")
    by_name = {row["path"].rsplit("/", 1)[1]: row["path"] for row in rows}
    if not SCOPE_EXCLUSIONS <= by_name.keys():
        raise ValueError("Missing legacy scope exclusions")
    # Reject additional central-prefix files rather than silently expanding
    # the exclusion rule beyond the seven source-verified files.
    central = {name for name in by_name if any(
        name.startswith(f"madsc-0{i}-") for i in range(1, 6))}
    if central != {name for name in SCOPE_EXCLUSIONS if name.startswith("madsc-0")}:
        raise ValueError("Legacy central workflow scope drift")
    excluded = sorted(by_name[name] for name in SCOPE_EXCLUSIONS)
    legacy = sorted(set(by_name.values()) - set(excluded))
    if len(legacy) != 92:
        raise ValueError("Expected 92 legacy behavior workflows")
    return {"source_workflows": 99, "legacy_behavior_workflows": 92,
            "excluded_from_92": excluded, "legacy_paths": legacy,
            "behavioral_parity_accepted": 0, "production_ready": False}
