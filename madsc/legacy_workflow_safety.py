"""Offline source-context evidence for legacy workflows; never executes or authorizes them."""
import re

WRITE = re.compile(r"(?:\bgit\s+push\b|curl[^\n]*(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE))", re.I)

GH_API = re.compile(r"\bgh\s+api\b[^\n]*", re.I)

GH_CLI_MUTATION = re.compile(r"\bgh\s+(?:workflow\s+(?:run|enable|disable)|run\s+rerun|release\s+(?:create|delete|edit|upload)|repo\s+(?:create|delete|edit)|pr\s+(?:merge|create|close)|issue\s+(?:create|close|edit))\b", re.I)

GIT_MUTATION = re.compile(r"\bgit\s+(?:(?:-c|--config)\s+\S+\s+)*(?:push|reset\s+--hard|clean\s+-(?=[A-Za-z]*f)[A-Za-z]+|checkout\s+--|restore\b)\b", re.I)

PYTHON_MUTATION = re.compile(r"\b(?:python3?|bash|sh)\s+(?:\S+/)*\S*(?:publish|upload|update|write|sync|deploy|delete|restore)\S*\.(?:py|sh)\b", re.I)

READ_ONLY_ACTIONS_API = re.compile(r"\brepos/\$\{GITHUB_REPOSITORY\}/actions/(?:runs|workflows)(?:\?[^\s\"]*)?", re.I)

GH_API_MUTATION_FLAGS = re.compile(r"(?<!\w)(?:-X|--method|-f|-F|--field|--raw-field|--input)(?:\s|=|$)", re.I)

def job_scope(source):
    """Conservative context for the repository's block-style jobs/steps.

    This is source evidence, not YAML/shell execution. Never grants clearance.
    Only command-shaped lines in run blocks count; embedded code still needs review.
    """
    jobs = []
    job = step = None
    run_indent = None
    in_jobs = False
    command = re.compile(r"(?:^|[;&|()])\s*(?:git\s+(?:(?:-c|--config)\s+\S+\s+)*push\b|gh\s+(?:workflow\s+(?:run|enable|disable)|run\s+rerun|api\b)|curl\b[^\n]*(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE))")
    for number, line in enumerate(source.splitlines(), 1):
        if re.match(r"^jobs:\s*(?:#.*)?$", line):
            in_jobs = True
            continue
        if re.match(r"^\S", line) and not line.startswith("#"):
            in_jobs = False
            job = step = None
        if not in_jobs:
            continue
        job_match = re.match(r"^  ([\w-]+):\s*$", line)
        if job_match:
            job = {"job": job_match[1], "line": number, "condition_signal": None, "steps": []}
            jobs.append(job)
            step = None
            run_indent = None
            continue
        if job is None:
            continue
        condition = re.match(r"^    if:\s*(.*)$", line)
        if condition:
            job["condition_signal"] = condition[1]
        reusable = re.match(r"^    uses:\s*(.*)$", line)
        if reusable:
            job["reusable_workflow_signal"] = reusable[1]
        step_match = re.match(r"^      - (name|uses|run):\s*(.*)$", line)
        if step_match:
            step = {"line": number, "name": step_match[2] if step_match[1] == "name" else "(unnamed)",
                    "failure_gate_call_lines": [], "mutation_signal_lines": [],
                    "script_mutation_name_lines": [], "continue_on_error_signal": False}
            job["steps"].append(step)
            run_indent = None
        if step is None:
            continue
        if re.match(r"^        continue-on-error:\s*true\s*(?:#.*)?$", line):
            step["continue_on_error_signal"] = True
        run_match = re.match(r"^(?:      - |        )run:\s*(.*)$", line)
        if run_match:
            body = run_match[1]
            run_indent = 8 if re.fullmatch(r"[|>][-+]?\s*(?:#.*)?", body) else None
            if run_indent is not None:
                continue
        elif run_indent is not None and (not line.strip() or len(line) - len(line.lstrip()) > run_indent):
            body = line.strip()
        else:
            run_indent = None
            continue
        if body.startswith("#"):
            continue
        if re.match(r"^python3?\s+tools/workflow_failure_gate\.py(?:\s|$)", body):
            step["failure_gate_call_lines"].append(number)
        readonly_api = (GH_API.search(body) and READ_ONLY_ACTIONS_API.search(body)
                        and not GH_API_MUTATION_FLAGS.search(body) and "graphql" not in body.casefold()
                        and not GIT_MUTATION.search(body) and not GH_CLI_MUTATION.search(body)
                        and not WRITE.search(body))
        if command.search(body) and not readonly_api:
            step["mutation_signal_lines"].append(number)
        if PYTHON_MUTATION.match(body):
            step["script_mutation_name_lines"].append(number)
    for job in jobs:
        gates = [line for step in job["steps"] if not step["continue_on_error_signal"]
                 for line in step["failure_gate_call_lines"]]
        mutations = [line for step in job["steps"]
                     for line in step["mutation_signal_lines"] + step["script_mutation_name_lines"]]
        job["mutation_lines_without_prior_failure_gate_signal"] = [line for line in mutations
                                                                   if not any(gate < line for gate in gates)]
        job["runtime_verified"] = False
    return jobs

def assess_workflow_source(source: str) -> dict:
    if not isinstance(source, str):
        raise ValueError("Workflow source must be text")
    jobs = job_scope(source)
    return {"scope": "static_job_step_evidence", "jobs": jobs,
            "mutation_signal_count": sum(len(job["mutation_lines_without_prior_failure_gate_signal"]) for job in jobs),
            "runtime_verified": False, "production_writes": False,
            "limitations": "Block-style source context only; dynamic shell, actions and called scripts need review."}
