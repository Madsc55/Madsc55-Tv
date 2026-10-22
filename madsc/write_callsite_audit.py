"""Read-only AST inventory of Python filesystem mutation callsites.

This is a review aid, not a proof of repository-wide enforcement. It records
mutating API candidates and whether a recognized K1 guard appears earlier in
the same lexical function. Dynamic aliases, helper contracts, shell commands,
and cross-function control flow require human review.
"""
from __future__ import annotations

import ast
from pathlib import Path

_GUARDS = {
    "enforce_write_paths",
    "enforce_local_output_path",
    "enforce_local_append_path",
    "enforce_local_turkish_tv_test_playlist",
}
_MUTATING_METHODS = {
    "write_text", "write_bytes", "unlink", "mkdir", "makedirs", "rmdir",
    "removedirs", "rename", "replace", "symlink_to", "hardlink_to",
    "touch", "truncate", "copy", "copy2", "copyfile", "copytree",
    "move", "rmtree", "remove",
}
_OS_MUTATORS = {
    "remove", "unlink", "rename", "replace", "mkdir", "makedirs",
    "rmdir", "removedirs", "symlink", "link", "truncate",
}
_GUARDED_OPEN_FLAGS = {"O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"}


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        base = _call_name(ast.Call(func=func.value, args=[], keywords=[])) if isinstance(func.value, ast.Call) else (
            func.value.id if isinstance(func.value, ast.Name) else
            func.value.attr if isinstance(func.value, ast.Attribute) else "")
        return f"{base}.{func.attr}" if base else func.attr
    return ""


def _is_mutating_call(node: ast.Call) -> tuple[bool, str]:
    name = _call_name(node)
    leaf = name.rsplit(".", 1)[-1]
    if leaf in _MUTATING_METHODS:
        return True, name
    if name in {"open", "builtins.open", "io.open"} or leaf == "open":
        mode = None
        mode_index = 0 if isinstance(node.func, ast.Attribute) else 1
        if len(node.args) > mode_index and isinstance(node.args[mode_index], ast.Constant):
            mode = node.args[mode_index].value
        for kw in node.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = kw.value.value
        if isinstance(mode, str) and any(flag in mode for flag in "wax+"):
            return True, name
        if mode is None and any(kw.arg == "mode" for kw in node.keywords):
            return True, name + " [dynamic mode]"
        return False, ""
    if name in {"os.open", "posix.open"}:
        flags = node.args[1] if len(node.args) > 1 else None
        if isinstance(flags, ast.BinOp) or isinstance(flags, ast.Name):
            return True, name + " [flags require review]"
        if isinstance(flags, ast.Constant) and isinstance(flags.value, int):
            # Conservatively record numeric flags; platform constants vary.
            return True, name + " [numeric flags require review]"
    if name.startswith("os.") and leaf in _OS_MUTATORS:
        return True, name
    return False, ""




class _ScopeCalls(ast.NodeVisitor):
    """Collect calls in one scope without accidentally inheriting nested guards."""
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        self.calls.append(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        return

    def visit_AsyncFunctionDef(self, node):
        return

    def visit_ClassDef(self, node):
        return


class _Scanner(ast.NodeVisitor):
    def __init__(self, path: str):
        self.path = path
        self.scope: list[tuple[str, list[int]]] = []
        self.rows: list[dict] = []

    def _visit_scope(self, node, name: str):
        collector = _ScopeCalls()
        for child in node.body:
            collector.visit(child)
        guards = sorted(n.lineno for n in collector.calls
                        if _call_name(n).rsplit(".", 1)[-1] in _GUARDS)
        self.scope.append((name, guards))
        for child in node.body:
            self.visit(child)
        self.scope.pop()

    def visit_FunctionDef(self, node):
        self._visit_scope(node, node.name)

    def visit_AsyncFunctionDef(self, node):
        self._visit_scope(node, node.name)

    def visit_ClassDef(self, node):
        self._visit_scope(node, node.name)

    def visit_Call(self, node):
        mutating, api = _is_mutating_call(node)
        if mutating:
            function, guards = self.scope[-1] if self.scope else ("<module>", [])
            earlier = any(line < node.lineno for line in guards)
            self.rows.append({
                "path": self.path,
                "line": node.lineno,
                "scope": function,
                "api": api,
                "recognized_guard_precedes_write_in_scope": earlier,
                "guard_lines_in_scope": guards,
                "review_required": True,
            })
        self.generic_visit(node)


def scan_python_source(source: str, path: str = "<memory>") -> list[dict]:
    """Return deterministic, line-ordered mutation candidates for human review."""
    if not isinstance(source, str):
        raise TypeError("Python source must be text")
    tree = ast.parse(source, filename=path)
    scanner = _Scanner(path)
    scanner.visit(tree)
    return sorted(scanner.rows, key=lambda row: (row["line"], row["api"]))


def scan_python_tree(root: Path, *, include_tests: bool = False) -> dict:
    """Scan repository Python sources without executing or changing any file."""
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Source root must be a directory")
    files = sorted(root.rglob("*.py"))
    rows = []
    scanned = []
    for file in files:
        relative = file.relative_to(root).as_posix()
        if not include_tests and (relative.startswith("tests/") or relative.startswith(".venv/")):
            continue
        if any(part in {".git", "__pycache__"} for part in file.parts):
            continue
        scanned.append(relative)
        rows.extend(scan_python_source(file.read_text(encoding="utf-8"), relative))
    return {
        "schema": "madsc-k1-write-callsite-inventory-v1",
        "source_root": ".",
        "files_scanned": len(scanned),
        "candidate_callsite_count": len(rows),
        "callsite_inventory": rows,
        "limitations": [
            "Static AST candidates only; not a runtime enforcement proof.",
            "Guard ordering is lexical and does not prove branch dominance or caller contracts.",
            "Dynamic aliases, subprocess/shell writes, generated code and non-Python writers need separate review.",
            "Every candidate remains review_required until individually dispositioned."
        ],
        "runtime_gate_enforced": False,
        "production_writes": False,
    }
