"""Isolated K1 acceptance evidence: test 26 externally specified checks, fail closed."""
from __future__ import annotations

from datetime import datetime, timezone


def assess_26_rules(observations: list[dict]) -> dict:
    """Do not count offline assertions as runtime acceptance."""
    if not isinstance(observations, list):
        raise ValueError("Observations must be a list")
    ids = [f"K1-R{i:02d}" for i in range(1, 27)]
    by_id = {}
    for row in observations:
        if not isinstance(row, dict) or row.get("rule_id") not in ids:
            raise ValueError("Invalid rule observation")
        rule_id = row["rule_id"]
        if rule_id in by_id:
            raise ValueError("Duplicate rule observation")
        if row.get("result") not in ("pass", "fail", "unverified"):
            raise ValueError("Invalid rule result")
        if row["result"] == "pass" and not (
            row.get("runtime_executed") is True
            and isinstance(row.get("independent_evidence"), str)
            and row["independent_evidence"].strip()
        ):
            raise ValueError("Passing runtime rule requires independent evidence")
        by_id[rule_id] = row
    details = []
    for rule_id in ids:
        row = by_id.get(rule_id, {})
        details.append({"rule_id": rule_id, "result": row.get("result", "unverified"),
                        "runtime_executed": row.get("runtime_executed") is True,
                        "independent_evidence": row.get("independent_evidence", "")})
    passed = sum(x["result"] == "pass" for x in details)
    return {"schema": "k1_26_runtime_observations_v1",
            "observed_pass_claims": passed, "total_rules": 26,
            "all_claimed_pass": passed == 26,
            "independently_accepted": False,
            "production_ready": False,
            "observations": details,
            "note": "Caller claims are not independent proof; review runtime logs and evidence."}
