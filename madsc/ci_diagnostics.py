"""Summarize unittest failures from a single CI run without hiding the failing exit code."""
from __future__ import annotations

import argparse
import json
import re
import os
import stat
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path, enforce_local_append_path

CASE = re.compile(r"^(FAIL|ERROR): (.+?) \((.+?)\)$", re.MULTILINE)
TOTAL = re.compile(r"Ran (\d+) tests? in ([\d.]+)s")
FAILURES = re.compile(r"FAILED \(([^)]+)\)")


def diagnose(log: str) -> dict:
    cases = [{"kind": kind, "test": name, "suite": suite}
             for kind, name, suite in CASE.findall(log)]
    total = TOTAL.search(log)
    failure = FAILURES.search(log)
    return {
        "mode": "unittest_log_only",
        "tests_run": int(total.group(1)) if total else None,
        "result": "failed" if failure or cases else ("passed" if "OK" in log and total else "unknown"),
        "failure_counts": failure.group(1) if failure else "",
        "failed_cases": cases,
        "root_cause_confirmed": False,
        "automatic_code_fix_applied": False,
        "requires_review": bool(failure or cases or not total),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    enforce_local_output_path(args.output.absolute())
    if args.summary:
        if args.summary.absolute() == args.output.absolute():
            raise PermissionError("Summary and JSON report must be separate")
        enforce_local_append_path(args.summary.absolute())
    report = diagnose(args.log.read_text(encoding="utf-8", errors="replace")
                      if args.log.exists() else "")
    enforce_local_output_path(args.output.absolute())
    with args.output.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    if args.summary:
        enforce_local_append_path(args.summary.absolute())
        descriptor = os.open(args.summary, os.O_WRONLY | os.O_APPEND | os.O_CREAT |
                             os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
        with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
            metadata = os.fstat(handle.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise PermissionError("Summary must be an independent regular file")
            handle.write("\n### Regresyon hata teşhisi\n")
            handle.write(f"- Test sayısı: {report['tests_run']}\n")
            handle.write(f"- Sonuç: {report['result']}\n")
            for case in report["failed_cases"]:
                handle.write(f"- {case['kind']}: `{case['suite']}.{case['test']}`\n")
            handle.write("- Kök neden ve kod düzeltmesi ayrıca doğrulanmalıdır.\n")


if __name__ == "__main__":
    main()
