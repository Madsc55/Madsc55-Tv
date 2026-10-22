"""Pure functions for aggregate status and bounded retry decisions."""
from __future__ import annotations
from datetime import datetime


def assess_failure_history(pages: list[dict], *, current_run_id: int,
                           branch: str, limit: int = 3) -> dict:
    """Apply the existing retry policy to bounded, supplied history pages.

    Offline only: the caller must supply authenticated history separately.
    Incomplete evidence cannot be interpreted as a zero-failure history.
    Pages must preserve descending creation-time/id order, including active runs.
    """
    retry_decision(0, limit)
    if (type(current_run_id) is not int or current_run_id <= 0
            or not isinstance(branch, str) or not branch
            or not isinstance(pages, list) or not 1 <= len(pages) <= 10):
        raise ValueError("Invalid failure history request")
    runs = {}
    received = 0
    total = None
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("workflow_runs"), list):
            raise ValueError("Invalid failure history page")
        count = page.get("total_count")
        batch = page["workflow_runs"]
        if type(count) is not int or count < 0 or len(batch) > 100:
            raise ValueError("Invalid failure history total")
        if total is not None and total != count:
            raise ValueError("Failure history changed during pagination")
        total = count
        if not batch and received < total:
            raise ValueError("Truncated failure history")
        if received + len(batch) > 1000:
            raise ValueError("Failure history exceeds bounded review capacity")
        for run in batch:
            if (not isinstance(run, dict) or type(run.get("id")) is not int
                    or run["id"] <= 0 or run["id"] in runs
                    or not isinstance(run.get("head_branch"), str)
                    or run.get("status") not in ("completed", "in_progress", "queued", "requested", "waiting", "pending")):
                raise ValueError("Invalid or duplicate failure history run")
            if (run["status"] == "completed" and
                    (type(run.get("conclusion")) is not str or run["conclusion"] not in
                     ("success", "failure", "timed_out", "cancelled", "skipped",
                      "neutral", "action_required", "stale"))):
                raise ValueError("Completed run has invalid conclusion")
            if run["status"] != "completed" and run.get("conclusion") is not None:
                raise ValueError("Active run has premature conclusion")
            runs[run["id"]] = run
        received += len(batch)
    if received > total:
        raise ValueError("Failure history total mismatch")
    current = runs.get(current_run_id)
    if current is None or current.get("head_branch") != branch:
        raise ValueError("Current run missing from branch history")

    def timestamp(run):
        raw = run.get("created_at")
        if not isinstance(raw, str):
            raise ValueError("Missing failure history timestamp")
        try:
            value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("Invalid failure history timestamp") from exc
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Ambiguous failure history timestamp")
        return value

    # Validate the supplied page sequence before filtering or sorting. Otherwise
    # an out-of-order older success could falsely terminate a partial history.
    orders = {run["id"]: (timestamp(run), run["id"]) for run in runs.values()}
    sequence = list(orders.values())
    if any(previous <= following for previous, following in zip(sequence, sequence[1:])):
        raise ValueError("Failure history page order is not descending")
    current_order = orders[current_run_id]
    prior = []
    for run in runs.values():
        if run["id"] == current_run_id or run.get("head_branch") != branch:
            continue
        order = orders[run["id"]]
        if order > current_order:
            # A newer same-branch run means this is not the current retry decision.
            raise ValueError("Newer branch run supersedes current history target")
        if order < current_order:
            if run.get("status") != "completed":
                # An older still-running job makes the failure sequence uncertain.
                raise ValueError("Incomplete prior run in failure history")
            prior.append((order, run))
    prior.sort(key=lambda item: item[0], reverse=True)
    streak = 0
    boundary = False
    for _, run in prior:
        conclusion = run.get("conclusion")
        if conclusion in ("failure", "timed_out"):
            streak += 1
            if streak >= limit:
                break
        elif conclusion == "success":
            boundary = True
            break
        elif conclusion in ("cancelled", "skipped", "neutral", "action_required", "stale"):
            # Non-successful runs cannot reset a consecutive-failure guard.
            # Fail closed instead of interpreting them as a successful boundary.
            raise ValueError("Indeterminate non-success run in failure history")
        else:
            raise ValueError("Unknown failure history conclusion")
    complete = received == total
    if not complete and not boundary and streak < limit:
        raise ValueError("More failure history pages required before retry")
    return {**retry_decision(streak, limit), "consecutive_failures": streak,
            "history_pages_checked": len(pages), "history_complete": complete,
            "runtime_history_origin_verified": False}

def retry_decision(consecutive_failures: int, limit: int = 3) -> dict:
    if type(consecutive_failures) is not int or consecutive_failures < 0 or type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("Invalid failure count or retry limit")
    blocked = consecutive_failures >= limit
    return {"blocked": blocked, "next_action": "HALT_AND_REPORT" if blocked else "RETRY_LATER",
            "production_writes": False, "state_persisted": False}

def aggregate(reports: list[dict]) -> dict:
    if not isinstance(reports, list) or any(not isinstance(r, dict) for r in reports):
        raise ValueError("Invalid batch reports")
    categories = {report.get("category") for report in reports if isinstance(report.get("category"), str)}
    expected = {"k1", "k2", "k3", "k4", "k5"}
    complete = categories == expected and len(reports) == 5
    # A report that only declares read-only status is not runtime evidence.
    # Reject duplicate/unknown categories and require explicit five-way identity.
    identity_valid = (len(reports) == 5 and
                      all(type(report.get("category")) is str and
                          report["category"] in expected for report in reports) and
                      len(categories) == 5)
    complete = complete and identity_valid
    safe = complete and all(report.get("production_writes") is False for report in reports)
    successful = safe and all(report.get("status") == "success" for report in reports)
    return {"all_five_present": complete, "all_read_only": safe,
            "all_five_successful": successful,
            "all_reports_explicitly_read_only": safe,
            "production_ready": False, "runtime_evidence_verified": False}


def summarize_batch(reports: list[dict]) -> dict:
    """Read-only per-category failure summary for coordinated maintenance."""
    if not isinstance(reports, list) or any(not isinstance(r, dict) for r in reports):
        raise ValueError("Invalid batch reports")
    base = aggregate(reports)
    expected = {"k1", "k2", "k3", "k4", "k5"}
    failures = sorted(str(r.get("category", "unknown")) for r in reports
                      if r.get("status") != "success" or (not isinstance(r.get("category"), str) or r.get("category") not in expected))
    missing = sorted(expected - {r.get("category") for r in reports if isinstance(r.get("category"), str)})
    counts = {category: sum(r.get("category") == category for r in reports) for category in expected}
    duplicates = sorted(category for category, count in counts.items() if count > 1)
    unexpected = sum(not isinstance(r.get("category"), str) or r.get("category") not in expected for r in reports)
    unsafe = sorted(str(r.get("category", "unknown")) for r in reports
                    if r.get("production_writes") is not False)
    return {**base, "failed_categories": failures, "missing_categories": missing,
            "duplicate_categories": duplicates, "unexpected_category_count": unexpected,
            "unsafe_or_unverified_write_categories": unsafe,
            "requires_review": bool(failures) or bool(missing) or bool(duplicates) or bool(unexpected) or not base["all_read_only"],
            "production_writes": False}


def verify_fixture_evidence(reports: list[dict]) -> dict:
    """Require explicit, true fixture checks without claiming production validation."""
    summary = summarize_batch(reports)
    missing_evidence = []
    failed_checks = []
    for report in reports:
        category = str(report.get("category", "unknown"))
        checks = report.get("fixture_checks")
        if (not isinstance(checks, dict) or not checks
                or any(type(key) is not str or not key.strip() for key in checks)):
            missing_evidence.append(category)
        elif any(value is not True for value in checks.values()):
            failed_checks.append(category)
    return {**summary, "missing_fixture_evidence": sorted(missing_evidence),
            "failed_fixture_checks": sorted(failed_checks),
            "fixture_evidence_verified": not summary["requires_review"]
            and not missing_evidence and not failed_checks,
            "production_ready": False, "runtime_evidence_verified": False}


def review_candidate_batch(coordination: dict, backup_evidence: dict) -> dict:
    """K5 cross-check K2/K3 candidate decisions and K4 restore evidence.

    This is a read-only review package, never an authorization to modify lists.
    """
    if not isinstance(coordination, dict) or not isinstance(backup_evidence, dict):
        raise ValueError("Invalid cross-system evidence")
    candidates = coordination.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("Missing K2/K3 candidates")
    # Bound unauthenticated evidence before iterating and building a review.
    if len(candidates) > 10000:
        raise ValueError("Candidate evidence exceeds safe review limit")
    seen = set()
    for item in candidates:
        if not isinstance(item, dict):
            raise ValueError("Malformed candidate evidence")
        if len(item) > 32:
            raise ValueError("Oversized candidate evidence record")
        digest = item.get("url_sha256")
        if (not isinstance(digest, str) or len(digest) != 64
                or any(c not in "0123456789abcdef" for c in digest) or digest in seen):
            raise ValueError("Invalid or repeated candidate identity")
        seen.add(digest)
        if (item.get("production_change_allowed") is not False
                or item.get("delete_allowed") is not False
                or type(item.get("hold")) is not bool
                or type(item.get("protected_working")) is not bool):
            raise ValueError("Unsafe candidate decision evidence")
    if (coordination.get("production_writes") is not False
            or coordination.get("production_ready") is not False
            or coordination.get("network_probed") is not False):
        raise ValueError("Unverified or unsafe coordination evidence")
    if (backup_evidence.get("production_writes") is not False
            or backup_evidence.get("production_restore_verified") is not False
            or backup_evidence.get("external_storage_proven") is not False):
        raise ValueError("Unsafe or overstated backup evidence")
    restore_matches = backup_evidence.get("independent_sandbox_restore_matches") is True
    return {
        "candidate_count": len(candidates),
        "held_count": sum(item["hold"] for item in candidates),
        "protected_ibo_working_count": sum(item["protected_working"] for item in candidates),
        "k4_independent_sandbox_restore_matches": restore_matches,
        "review_evidence_complete": restore_matches and bool(candidates),
        "production_ready": False, "production_writes": False,
        "device_verified": False, "external_storage_proven": False,
        "legacy_behavioral_equivalence_verified": False,
    }
