"""Fail-closed, read-only review of proposed legacy-to-K1..K5 behavior mappings.

A mapping is a review candidate, never runtime evidence or parity acceptance.
"""
from madsc.legacy_parity_evidence import (CENTRAL_REPLACEMENT_WORKFLOWS,
                                         reconcile_legacy_scope, validate_inventory)
from madsc.parity_workflow_readiness import audit_parity_workflow_readiness


def review_replacement_mappings(inventory, mapping_rows, replacement_workflow_root):
    """Bind proposed mappings to pinned legacy blobs and current source contracts.

    Refuse duplicate, unknown, excluded, or stale source identities. No inferred
    mapping from workflow names or K-stage hints is allowed.
    """
    scope = reconcile_legacy_scope(inventory)
    catalog = {row["path"]: row for row in validate_inventory(inventory)}
    eligible = set(scope["legacy_paths"])
    if not isinstance(mapping_rows, list) or len(mapping_rows) > len(eligible):
        raise ValueError("Invalid mapping rows")
    readiness = audit_parity_workflow_readiness(replacement_workflow_root)
    if not isinstance(readiness, dict) or not isinstance(readiness.get("rows"), list):
        raise ValueError("Missing replacement workflow catalog")
    workflow_rows = readiness["rows"]
    required_contract = {"workflow_path", "workflow_blob_sha", "declared_file_binding",
                         "marker_contract_complete", "static_file_binding_complete",
                         "input_digest_binding_complete"}
    if (len(workflow_rows) != len(CENTRAL_REPLACEMENT_WORKFLOWS)
            or any(not isinstance(row, dict)
                   or not required_contract <= row.keys()
                   or not isinstance(row["workflow_path"], str)
                   or row["workflow_path"] not in CENTRAL_REPLACEMENT_WORKFLOWS
                   or not isinstance(row["workflow_blob_sha"], str)
                   or len(row["workflow_blob_sha"]) != 40
                   or any(ch not in "0123456789abcdef" for ch in row["workflow_blob_sha"])
                   or any(type(row[field]) is not bool for field in (
                       "marker_contract_complete", "static_file_binding_complete",
                       "input_digest_binding_complete"))
                   or (row["declared_file_binding"] is not None
                       and (not isinstance(row["declared_file_binding"], dict)
                            or not {"input_path", "output_label", "output_path"}
                            <= row["declared_file_binding"].keys()))
                   for row in workflow_rows)):
        raise ValueError("Malformed replacement workflow catalog")
    current = {row["workflow_path"]: row for row in workflow_rows}
    if len(current) != len(CENTRAL_REPLACEMENT_WORKFLOWS):
        raise ValueError("Replacement workflow catalog is incomplete or ambiguous")
    seen = set()
    results = []
    required = {"legacy_path", "legacy_blob_sha", "replacement_workflow_path",
                "replacement_blob_sha", "input_role", "output_role", "review_rationale"}
    for candidate in mapping_rows:
        if not isinstance(candidate, dict) or set(candidate) != required:
            raise ValueError("Incomplete replacement mapping")
        path = candidate["legacy_path"]
        if not isinstance(path, str) or path not in eligible or path in seen:
            raise ValueError("Unknown, excluded or duplicate legacy mapping")
        seen.add(path)
        if candidate["legacy_blob_sha"] != catalog[path].get("git_blob_sha"):
            raise ValueError("Legacy source blob differs from pinned inventory")
        replacement_path = candidate["replacement_workflow_path"]
        if (not isinstance(replacement_path, str)
                or replacement_path not in CENTRAL_REPLACEMENT_WORKFLOWS
                or replacement_path not in current):
            raise ValueError("Invalid replacement workflow")
        contract = current[replacement_path]
        if candidate["replacement_blob_sha"] != contract["workflow_blob_sha"]:
            raise ValueError("Replacement workflow source blob has changed")
        for field in ("input_role", "output_role", "review_rationale"):
            value = candidate[field]
            if not isinstance(value, str) or not value.strip() or len(value) > 1024:
                raise ValueError("Missing or invalid mapping review rationale/role")
        binding = contract["declared_file_binding"]
        role_matches = bool(
            binding and candidate["input_role"] == binding["input_path"]
            and candidate["output_role"] ==
            binding["output_label"] + "=" + binding["output_path"]
        )
        static_contract_complete = bool(
            role_matches and contract["marker_contract_complete"]
            and contract["static_file_binding_complete"]
            and contract["input_digest_binding_complete"]
        )
        results.append({
            "legacy_path": path,
            "replacement_workflow_path": replacement_path,
            "source_identities_match": True,
            "declared_roles_match": role_matches,
            "static_contract_complete": static_contract_complete,
            "review_rationale": candidate["review_rationale"],
            "status": ("static_candidate_needs_independent_evidence"
                       if static_contract_complete else "mapping_contract_blocked"),
            "independent_execution_evidence_verified": False,
            "behavioral_parity_accepted": False,
        })
    return {
        "schema": "madsc-legacy-replacement-mapping-review-v1",
        "legacy_scope": len(eligible),
        "mapping_candidates_supplied": len(results),
        "unmapped_legacy_workflows": len(eligible) - len(results),
        "static_contract_candidates": sum(r["static_contract_complete"] for r in results),
        "behavioral_parity_accepted": 0,
        "production_ready": False,
        "rows": results,
    }
