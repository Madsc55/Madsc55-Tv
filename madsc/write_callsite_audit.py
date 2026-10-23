"""Read-only AST inventory of Python filesystem mutation callsites.

This is a review aid, not a proof of repository-wide enforcement. It records
mutating API candidates and whether a recognized K1 guard appears earlier in
the same lexical function. Dynamic aliases, helper contracts, shell commands,
and cross-function control flow require human review.
"""
from __future__ import annotations

import ast
import hashlib
import stat
from pathlib import Path

_GUARDS = {
    "enforce_write_paths",
    "enforce_local_output_path",
    "enforce_local_append_path",
    "enforce_local_turkish_tv_test_playlist",
}
_MUTATING_METHODS = {
    # File-object writes matter too: an open(..., "w") may be wrapped or
    # passed through a helper, so inventory write()/writelines() callsites.
    "write", "writelines", "write_text", "write_bytes", "unlink", "mkdir", "makedirs", "rmdir",
    "removedirs", "rename", "replace", "symlink_to", "hardlink_to", "link_to",
    "touch", "truncate", "copy", "copy2", "copyfile", "copytree",
    "move", "rmtree", "remove", "chmod", "lchmod", "chown", "lchown",
    "extract", "extractall", "unpack_archive", "make_archive",
}
_OS_MUTATORS = {
    "remove", "unlink", "rename", "replace", "mkdir", "makedirs",
    "rmdir", "removedirs", "symlink", "link", "truncate",
    "write", "writev", "pwrite", "pwritev", "ftruncate",
    "chmod", "lchmod", "fchmod", "chown", "lchown", "fchown", "utime",
    "mkfifo", "mknod", "setxattr", "fsetxattr", "lsetxattr",
    "removexattr", "fremovexattr", "lremovexattr", "chflags", "lchflags",
}
# Process launchers can perform writes outside Python's filesystem APIs (cp,
# mv, redirection, scripts, etc.). Record them for command-level review.
_PROCESS_LAUNCHERS = {
    "subprocess.run", "subprocess.call", "subprocess.Popen",
    "subprocess.check_call", "subprocess.check_output",
    "os.system", "os.popen",
}
_GUARDED_OPEN_FLAGS = {"O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"}
_READ_ONLY_OPEN_FLAGS = {
    "O_RDONLY", "O_NOFOLLOW", "O_NONBLOCK", "O_CLOEXEC", "O_DIRECTORY",
    "O_PATH", "O_BINARY", "O_TEXT", "O_NOINHERIT", "O_NOCTTY",
}
_TEXT_METHODS = {
    "casefold", "capitalize", "center", "expandtabs", "format", "format_map",
    "join", "ljust", "lower", "lstrip", "removeprefix", "removesuffix",
    "replace", "rjust", "rstrip", "strip", "swapcase", "title", "translate",
    "upper", "zfill",
}
# These helpers create files even without an explicit writable open() mode.
_TEMPFILE_CREATORS = {
    "tempfile.NamedTemporaryFile", "tempfile.TemporaryFile",
    "tempfile.mkstemp", "tempfile.mkdtemp", "tempfile.TemporaryDirectory",
    "tempfile.SpooledTemporaryFile",
}


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        base = _call_name(func.value) if isinstance(func.value, ast.Call) else (
            func.value.id if isinstance(func.value, ast.Name) else
            func.value.attr if isinstance(func.value, ast.Attribute) else "")
        return f"{base}.{func.attr}" if base else func.attr
    return ""


def _flag_names(node: ast.AST) -> set[str] | None:
    """Return statically-known os.open flag names, or None for uncertainty."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        left = _flag_names(node.left)
        right = _flag_names(node.right)
        return None if left is None or right is None else left | right
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        if node.value.id in {"os", "posix"} and node.attr.startswith("O_"):
            return {node.attr}
        return None
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        # getattr(os, "O_NONBLOCK", 0) is a common portable, read-only modifier.
        if (node.func.id == "getattr" and len(node.args) in {2, 3}
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id in {"os", "posix"}
                and isinstance(node.args[1], ast.Constant)
                and isinstance(node.args[1].value, str)
                and node.args[1].value.startswith("O_")
                and (len(node.args) == 2
                     or isinstance(node.args[2], ast.Constant)
                     and node.args[2].value == 0)):
            return {node.args[1].value}
        return None
    if isinstance(node, ast.Constant) and type(node.value) is int and node.value == 0:
        return set()
    return None


def _is_proven_text_receiver(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return True
    return (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in _TEXT_METHODS
            and _is_proven_text_receiver(node.func.value))


def _is_proven_text_replace(node: ast.Call) -> bool:
    """Recognize only receivers whose expression proves string semantics."""
    if not isinstance(node.func, ast.Attribute) or node.func.attr != "replace":
        return False
    receiver = node.func.value
    if isinstance(receiver, ast.Constant) and isinstance(receiver.value, str):
        return True
    # A method name alone does not prove a string receiver: user-defined
    # objects can implement lower()/strip() and return a pathlib-like writer.
    # Only a chain rooted in a literal string is safe to exclude.
    if isinstance(receiver, ast.Call) and isinstance(receiver.func, ast.Attribute):
        return (receiver.func.attr in _TEXT_METHODS
                and _is_proven_text_receiver(receiver.func.value))
    return False


def _classify_call(node: ast.Call) -> tuple[str, str]:
    name = _call_name(node)
    leaf = name.rsplit(".", 1)[-1]
    if leaf == "replace" and _is_proven_text_replace(node):
        return "proven_non_filesystem_text_transform", name
    if leaf in _MUTATING_METHODS:
        return "write_candidate", name
    if name in _TEMPFILE_CREATORS:
        return "write_candidate", name + " [temporary filesystem creation requires review]"
    # os.open uses flags, not a text mode; handle it before generic *.open
    # so the generic branch cannot swallow it and miss O_WRONLY/O_CREAT.
    if name in {"os.open", "posix.open"}:
        flags = node.args[1] if len(node.args) > 1 else None
        for kw in node.keywords:
            if kw.arg == "flags":
                flags = kw.value
        # **options may supply or override flags, even when a literal
        # O_RDONLY argument appears. Never certify such a call read-only.
        if any(kw.arg is None for kw in node.keywords):
            return "write_candidate", name + " [dynamic flags require review]"
        names = _flag_names(flags) if flags is not None else None
        if (names is not None and names and names <= _READ_ONLY_OPEN_FLAGS
                and names & {"O_RDONLY", "O_PATH"}):
            return "proven_read_only_descriptor", name
        if names is not None and names & _GUARDED_OPEN_FLAGS:
            return "write_candidate", name + " [flags require review]"
        if isinstance(flags, (ast.BinOp, ast.Name, ast.Attribute)):
            return "write_candidate", name + " [flags require review]"
        if isinstance(flags, ast.Constant) and isinstance(flags.value, int):
            # Conservatively record numeric flags; platform constants vary.
            return "write_candidate", name + " [numeric flags require review]"
        if flags is None:
            return "write_candidate", name + " [missing or dynamic flags require review]"
        # Calls, conditionals, unary expressions and other AST forms can
        # evaluate to O_CREAT/O_TRUNC; an unrecognized expression is NOT read-only.
        return "write_candidate", name + " [flags require review]"
    # os.fdopen wraps a descriptor and may expose a writable file object.
    # Include the wrapper's mode even if its later write() is in a helper.
    if name == "os.fdopen":
        if any(isinstance(arg, ast.Starred) for arg in node.args):
            return "write_candidate", name + " [dynamic mode]"
        mode = node.args[1] if len(node.args) > 1 else None
        for kw in node.keywords:
            if kw.arg == "mode":
                mode = kw.value
        if any(kw.arg is None for kw in node.keywords):
            # Unpacked keywords may provide/override the descriptor mode.
            return "write_candidate", name + " [dynamic mode]"
        if mode is None:
            return "not_relevant", ""
        if not isinstance(mode, ast.Constant) or not isinstance(mode.value, str):
            return "write_candidate", name + " [dynamic mode]"
        if any(flag in mode.value for flag in "wax+"):
            return "write_candidate", name
        return "not_relevant", ""
    is_builtin_open = name in {"open", "builtins.open", "io.open"}
    is_path_open = (isinstance(node.func, ast.Attribute) and leaf == "open"
                    and name not in {"os.open", "posix.open", "builtins.open", "io.open"})
    if is_builtin_open or is_path_open:
        # *args may supply a writable mode even when no explicit mode is seen.
        if any(isinstance(arg, ast.Starred) for arg in node.args):
            return "write_candidate", name + " [dynamic mode]"
        mode = None
        # Path.open(mode) takes mode as its first argument; builtins.open and
        # io.open take (file, mode), as does the unqualified built-in open().
        mode_index = 0 if is_path_open else 1
        mode_supplied = len(node.args) > mode_index
        dynamic_mode = mode_supplied and not isinstance(node.args[mode_index], ast.Constant)
        if mode_supplied and isinstance(node.args[mode_index], ast.Constant):
            mode = node.args[mode_index].value
        for kw in node.keywords:
            if kw.arg is None:
                # **options can override a literal read-only mode with "w".
                dynamic_mode = True
            if kw.arg == "mode":
                mode_supplied = True
                if isinstance(kw.value, ast.Constant):
                    mode = kw.value.value
                    dynamic_mode = False
                else:
                    dynamic_mode = True
        if any(kw.arg is None for kw in node.keywords):
            dynamic_mode = True
        if isinstance(mode, str) and any(flag in mode for flag in "wax+"):
            return "write_candidate", name
        # A nonliteral positional or keyword mode can enable writing.
        if dynamic_mode:
            return "write_candidate", name + " [dynamic mode]"
        return "not_relevant", ""
    if name.startswith("os.") and leaf in _OS_MUTATORS:
        return "write_candidate", name
    if name in _PROCESS_LAUNCHERS:
        return "write_candidate", name + " [process command requires review]"
    return "not_relevant", ""


def _is_mutating_call(node: ast.Call) -> tuple[bool, str]:
    """Backward-compatible predicate used by earlier callers/tests."""
    classification, api = _classify_call(node)
    return classification == "write_candidate", api




class _ScopeCalls(ast.NodeVisitor):
    """Collect calls in one scope without accidentally inheriting nested guards."""
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        self.calls.append(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        return

    def visit_Lambda(self, node):
        # Deferred lambda calls must not contribute guards to the enclosing
        # function's lexical guard inventory.
        return

    def visit_AsyncFunctionDef(self, node):
        return

    def visit_ClassDef(self, node):
        return


class _Scanner(ast.NodeVisitor):
    def __init__(self, path: str, source: str):
        self.path = path
        self.source = source
        self.source_file_sha256 = hashlib.sha256(source.encode("utf-8")).hexdigest()
        self.scope: list[tuple[str, list[int]]] = []
        self.rows: list[dict] = []
        self.dispositions: list[dict] = []

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

    def _visit_definition_expressions(self, node):
        # Decorators, base classes and default arguments execute in the
        # enclosing scope when the definition is evaluated, not in its body.
        for decorator in node.decorator_list:
            self.visit(decorator)
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                self.visit(base)
            for keyword in node.keywords:
                self.visit(keyword.value)
        else:
            for default in (*node.args.defaults, *node.args.kw_defaults):
                if default is not None:
                    self.visit(default)
            for annotation in (*node.args.posonlyargs, *node.args.args,
                               *node.args.kwonlyargs):
                if annotation.annotation is not None:
                    self.visit(annotation.annotation)
            if node.args.vararg and node.args.vararg.annotation is not None:
                self.visit(node.args.vararg.annotation)
            if node.args.kwarg and node.args.kwarg.annotation is not None:
                self.visit(node.args.kwarg.annotation)
            if node.returns is not None:
                self.visit(node.returns)

    def visit_FunctionDef(self, node):
        self._visit_definition_expressions(node)
        self._visit_scope(node, node.name)

    def visit_AsyncFunctionDef(self, node):
        self._visit_definition_expressions(node)
        self._visit_scope(node, node.name)

    def visit_ClassDef(self, node):
        self._visit_definition_expressions(node)
        self._visit_scope(node, node.name)

    def visit_Lambda(self, node):
        # Lambda defaults execute immediately in the enclosing scope;
        # only the lambda body is deferred until invocation.
        for default in (*node.args.defaults, *node.args.kw_defaults):
            if default is not None:
                self.visit(default)
        collector = _ScopeCalls()
        collector.visit(node.body)
        guards = sorted(n.lineno for n in collector.calls
                        if _call_name(n).rsplit(".", 1)[-1] in _GUARDS)
        self.scope.append((f"<lambda@{node.lineno}>", guards))
        self.visit(node.body)
        self.scope.pop()

    def visit_Call(self, node):
        classification, api = _classify_call(node)
        if classification in {"write_candidate", "proven_non_filesystem_text_transform",
                              "proven_read_only_descriptor"}:
            function, guards = self.scope[-1] if self.scope else ("<module>", [])
            earlier = any(line < node.lineno for line in guards)
            segment = ast.get_source_segment(self.source, node) or ""
            base = {
                "path": self.path,
                "line": node.lineno,
                "scope": function,
                "api": api,
                "source_file_sha256": self.source_file_sha256,
                "source_segment_sha256": hashlib.sha256(segment.encode("utf-8")).hexdigest(),
            }
            if classification != "write_candidate":
                self.dispositions.append({
                    **base,
                    "disposition": classification,
                    "review_required": False,
                })
            else:
                self.rows.append({
                    **base,
                    "recognized_guard_precedes_write_in_scope": earlier,
                    "guard_lines_in_scope": guards,
                    # Lexical order is not proof that a guard dominates a write:
                    # it may live in a conditional, loop, or exception branch.
                    "guard_control_flow_verified": False,
                    "guard_assessment": "lexical-only; manual control-flow review required",
                    "review_required": True,
                })
        self.generic_visit(node)


def scan_python_source(source: str, path: str = "<memory>") -> list[dict]:
    """Return deterministic, line-ordered mutation candidates for human review."""
    if not isinstance(source, str):
        raise TypeError("Python source must be text")
    tree = ast.parse(source, filename=path)
    scanner = _Scanner(path, source)
    scanner.visit(tree)
    return sorted(scanner.rows, key=lambda row: (row["line"], row["api"]))


def scan_python_tree(root: Path, *, include_tests: bool = False) -> dict:
    """Scan repository Python sources without executing or changing any file."""
    requested_root = Path(root)
    if requested_root.is_symlink():
        raise ValueError("Symlinked source root requires review")
    root = requested_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Source root must be a directory")
    # pathlib.rglob("*.py") may not descend into symlinked directories.
    # Reject linked directories before enumerating sources, rather than
    # silently declaring an incomplete inventory.
    for entry in root.rglob("*"):
        if entry.is_symlink():
            # is_dir() is False for dangling links; they must not disappear
            # from a supposedly complete source inventory either.
            raise ValueError(f"Symlinked source entry requires review: {entry.relative_to(root)}")
    files = sorted(root.rglob("*.py"))
    rows = []
    dispositions = []
    scanned = []
    for file in files:
        relative = file.relative_to(root).as_posix()
        if not include_tests and (relative.startswith("tests/") or relative.startswith(".venv/")):
            continue
        if any(part in {".git", "__pycache__"} for part in file.parts):
            continue
        # Never follow a linked source file outside the audited tree.
        # Reject rather than silently omitting an untrusted Python entry.
        if file.is_symlink():
            raise ValueError(f"Symlinked Python source requires review: {relative}")
        if not stat.S_ISREG(file.stat(follow_symlinks=False).st_mode):
            raise ValueError(f"Non-regular Python source requires review: {relative}")
        scanned.append(relative)
        source = file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=relative)
        scanner = _Scanner(relative, source)
        scanner.visit(tree)
        rows.extend(scanner.rows)
        dispositions.extend(scanner.dispositions)
    return {
        "schema": "madsc-k1-write-callsite-inventory-v2",
        "source_root": ".",
        "files_scanned": len(scanned),
        "candidate_callsite_count": len(rows),
        "callsite_inventory": rows,
        "non_write_disposition_count": len(dispositions),
        "non_write_dispositions": sorted(
            dispositions, key=lambda row: (row["path"], row["line"], row["api"])),
        "limitations": [
            "Static AST candidates only; not a runtime enforcement proof.",
            "Guard ordering is lexical and does not prove branch dominance or caller contracts.",
            "Dynamic aliases, subprocess/shell writes, generated code and non-Python writers need separate review.",
            "Every candidate remains review_required until individually dispositioned.",
            "Non-write dispositions are limited to source-hash-bound syntactic proofs.",
        ],
        "runtime_gate_enforced": False,
        "production_writes": False,
    }
