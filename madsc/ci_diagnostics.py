"""Summarize unittest failures from a single CI run without hiding the failing exit code."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

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
    report = diagnose(args.log.read_text(encoding="utf-8", errors="replace")
                      if args.log.exists() else "")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.summary:
        with args.summary.open("a", encoding="utf-8") as handle:
            handle.write("\n### Regresyon hata teşhisi\n")
            handle.write(f"- Test sayısı: {report['tests_run']}\n")
            handle.write(f"- Sonuç: {report['result']}\n")
            for case in report["failed_cases"]:
                handle.write(f"- {case['kind']}: `{case['suite']}.{case['test']}`\n")
            handle.write("- Kök neden ve kod düzeltmesi ayrıca doğrulanmalıdır.\n")


if __name__ == "__main__":
    main()
