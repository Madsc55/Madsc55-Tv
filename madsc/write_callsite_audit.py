"""Read-only AST inventory of Python filesystem mutation callsites.

This is a review aid, not a proof of repository-wide enforcement. It records
mutating API candidates and whether a recognized K1 guard appears earlier in
the same lexical function. Dynamic aliases, helper contracts, shell commands,
and cross-function control flow require human review.
"""
from __future__ import annotations

import ast
import os
import unicodedata
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
    "touch", "truncate", "copy", "copy2", "copyfile", "copyfileobj", "copytree", "copymode", "copystat",
    "move", "rmtree", "remove", "chmod", "lchmod", "chown", "lchown",
    "setxattr", "removexattr", "utime", "writeheader", "writerow", "writerows",
    "extract", "extractall", "unpack_archive", "make_archive",
}
_OS_MUTATORS = {
    "remove", "unlink", "rename", "replace", "mkdir", "makedirs",
    "rmdir", "removedirs", "symlink", "link", "truncate",
    "write", "writev", "pwrite", "pwritev", "sendfile", "copy_file_range", "splice", "ftruncate",
    "chmod", "lchmod", "fchmod", "chown", "lchown", "fchown", "utime",
    "mkfifo", "mknod", "setxattr", "fsetxattr", "lsetxattr",
    "removexattr", "fremovexattr", "lremovexattr", "chflags", "lchflags",
}
# Process launchers can perform writes outside Python's filesystem APIs (cp,
# mv, redirection, scripts, etc.). Record them for command-level review.
_PROCESS_LAUNCHERS = {
    "subprocess.run", "subprocess.call", "subprocess.Popen",
    "subprocess.check_call", "subprocess.check_output",
    "subprocess.getoutput", "subprocess.getstatusoutput",
    "os.system", "os.popen", "os.startfile", "os.fork", "os.forkpty", "os.spawnl", "os.spawnle", "os.spawnlp", "os.spawnlpe",
    "os.spawnv", "os.spawnve", "os.spawnvp", "os.spawnvpe", "os.posix_spawn", "os.posix_spawnp",
    "os.execv", "os.execve", "os.execvp", "os.execvpe", "os.execl", "os.execle", "os.execlp", "os.execlpe",
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

_CURL_FILE_OUTPUT_OPTIONS = {
    "-o", "--output", "-O", "--remote-name", "--output-dir",
    "-c", "--cookie-jar", "--trace", "--trace-ascii",
    "-D", "--dump-header", "-K", "--config",
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


def _flag_names(node: ast.AST, bindings=None, resolving=frozenset()) -> set[str] | None:
    """Return statically-known os.open flag names, or None for uncertainty."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        left = _flag_names(node.left, bindings, resolving)
        right = _flag_names(node.right, bindings, resolving)
        return None if left is None or right is None else left | right
    if isinstance(node, ast.Name):
        if not bindings or node.id not in bindings or node.id in resolving:
            return None
        return _flag_names(bindings[node.id], bindings, resolving | {node.id})
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


class _LocalBindingCollector(ast.NodeVisitor):
    """Count local stores without inheriting deferred nested scopes."""
    def __init__(self):
        self.stores = {}
        self.external = set()
        self.dynamic_scope = False

    def _store(self, name):
        if name:
            self.stores[name] = self.stores.get(name, 0) + 1

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self._store(node.id)

    def visit_Import(self, node):
        for alias in node.names:
            self._store(alias.asname or alias.name.split(".", 1)[0])

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self._store(alias.asname or alias.name)

    def visit_MatchAs(self, node):
        self._store(node.name)
        self.generic_visit(node)

    def visit_MatchStar(self, node):
        self._store(node.name)

    def visit_MatchMapping(self, node):
        self._store(node.rest)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self._store(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "exec":
            self.dynamic_scope = True
        self.generic_visit(node)

    def visit_Global(self, node):
        self.external.update(node.names)

    def visit_Nonlocal(self, node):
        self.external.update(node.names)

    def visit_FunctionDef(self, node):
        return

    def visit_AsyncFunctionDef(self, node):
        return

    def visit_Lambda(self, node):
        return

    def visit_ClassDef(self, node):
        return


def _direct_local_flag_bindings(node) -> dict[str, ast.AST]:
    """Return single-assignment locals whose value dominates later statements."""
    collector = _LocalBindingCollector()
    for statement in node.body:
        collector.visit(statement)
    if collector.dynamic_scope:
        return {}
    nested_nonlocals = set()
    for statement in node.body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for descendant in ast.walk(statement):
                if isinstance(descendant, ast.Nonlocal):
                    nested_nonlocals.update(descendant.names)
    parameters = {
        arg.arg for arg in (*node.args.posonlyargs, *node.args.args,
                            *node.args.kwonlyargs)
    }
    if node.args.vararg:
        parameters.add(node.args.vararg.arg)
    if node.args.kwarg:
        parameters.add(node.args.kwarg.arg)
    direct = {}
    for statement in node.body:
        if (isinstance(statement, ast.Assign) and len(statement.targets) == 1
                and isinstance(statement.targets[0], ast.Name)):
            name, value = statement.targets[0].id, statement.value
        elif (isinstance(statement, ast.AnnAssign)
              and isinstance(statement.target, ast.Name)
              and statement.value is not None):
            name, value = statement.target.id, statement.value
        else:
            continue
        if (collector.stores.get(name) == 1 and name not in parameters
                and name not in collector.external and name not in nested_nonlocals):
            direct[name] = value
    return direct


def _direct_guard_line(statement) -> int | None:
    """Return a guard line only when the statement executes it unconditionally."""
    value = statement.value if isinstance(statement, ast.Expr) else None
    if isinstance(value, ast.Await):
        value = value.value
    if (isinstance(value, ast.Call)
            and _call_name(value).rsplit(".", 1)[-1] in _GUARDS):
        return value.lineno
    return None


def _resolve_local_expression(node: ast.AST | None, bindings, resolving=frozenset()):
    if isinstance(node, ast.Name) and bindings and node.id in bindings and node.id not in resolving:
        return _resolve_local_expression(bindings[node.id], bindings, resolving | {node.id})
    return node


def _process_contract(node: ast.Call, bindings=None) -> dict | None:
    """Record syntactic subprocess facts without claiming command safety."""
    name = _call_name(node)
    if name not in _PROCESS_LAUNCHERS:
        return None
    unpacked_keywords = any(keyword.arg is None for keyword in node.keywords)
    shell_value = next((keyword.value for keyword in node.keywords
                        if keyword.arg == "shell"), None)
    if name in {"os.system", "os.popen", "subprocess.getoutput", "subprocess.getstatusoutput"}:
        shell_status = "implicit_shell"
    elif unpacked_keywords:
        shell_status = "unknown_keyword_unpacking"
    elif shell_value is None:
        shell_status = "default_false"
    elif isinstance(shell_value, ast.Constant) and shell_value.value is False:
        shell_status = "explicit_false"
    elif isinstance(shell_value, ast.Constant) and shell_value.value is True:
        shell_status = "explicit_true"
    else:
        shell_status = "dynamic"
    original_command = node.args[0] if node.args else None
    command = _resolve_local_expression(original_command, bindings)
    command_source = ("direct_local_single_assignment"
                      if command is not original_command else
                      "unresolved_name" if isinstance(original_command, ast.Name) else
                      "direct_call_expression")
    argv_container = isinstance(command, (ast.List, ast.Tuple)) and bool(command.elts)
    literal_argv = (isinstance(command, (ast.List, ast.Tuple)) and bool(command.elts)
                    and all(isinstance(item, ast.Constant)
                            and isinstance(item.value, str) for item in command.elts))
    executable = None
    if (argv_container and isinstance(command.elts[0], ast.Constant)
            and isinstance(command.elts[0].value, str)):
        executable = command.elts[0].value
    elif (isinstance(command, (ast.List, ast.Tuple)) and command.elts
          and isinstance(command.elts[0], ast.Attribute)
          and isinstance(command.elts[0].value, ast.Name)
          and command.elts[0].value.id == "sys"
          and command.elts[0].attr == "executable"):
        executable = "sys.executable"
    keywords = {keyword.arg: keyword.value for keyword in node.keywords
                if keyword.arg is not None}

    argv_tokens = []
    if argv_container:
        for item in command.elts:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                argv_tokens.append(item.value)
            elif (isinstance(item, ast.Attribute)
                  and isinstance(item.value, ast.Name)
                  and item.value.id == "sys" and item.attr == "executable"):
                argv_tokens.append("sys.executable")
            else:
                argv_tokens.append(None)
    literal_options = [token for token in argv_tokens
                       if isinstance(token, str) and token.startswith("-")]
    literal_file_output_switches = []
    if executable == "curl":
        for option in literal_options:
            matched = next((candidate for candidate in _CURL_FILE_OUTPUT_OPTIONS
                            if option == candidate
                            or candidate.startswith("--")
                            and option.startswith(candidate + "=")), None)
            if matched and matched not in literal_file_output_switches:
                literal_file_output_switches.append(matched)

    if executable == "curl":
        effect_classification = "network_client"
    elif executable == "ffprobe":
        effect_classification = "media_inspector"
    elif executable == "sys.executable" and "-c" in literal_options:
        effect_classification = "python_inline_payload"
    elif executable == "sys.executable" and "-m" in literal_options:
        effect_classification = "python_module_payload"
    elif executable is None:
        effect_classification = "caller_controlled_command"
    else:
        effect_classification = "other_command"

    def keyword_source(keyword, literal_mapping=False):
        if unpacked_keywords:
            return "dynamic_keyword_unpacking"
        if keyword not in keywords:
            return "inherited"
        value = keywords[keyword]
        if literal_mapping:
            if (isinstance(value, ast.Dict)
                    and all(key is not None
                            and isinstance(key, ast.Constant)
                            and isinstance(key.value, str)
                            and isinstance(item, ast.Constant)
                            and isinstance(item.value, str)
                            for key, item in zip(value.keys, value.values))):
                return "explicit_literal_mapping"
            return "explicit_expression"
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            return "explicit_literal"
        return "explicit_expression"

    def subprocess_constant(keyword, attribute):
        value = keywords.get(keyword)
        return (isinstance(value, ast.Attribute)
                and isinstance(value.value, ast.Name)
                and value.value.id == "subprocess"
                and value.attr == attribute)

    capture_output = (isinstance(keywords.get("capture_output"), ast.Constant)
                      and keywords["capture_output"].value is True)
    stdin_status = ("devnull" if subprocess_constant("stdin", "DEVNULL") else
                    "inherited" if "stdin" not in keywords and not unpacked_keywords else
                    "dynamic")
    stdout_status = ("captured" if capture_output
                     or subprocess_constant("stdout", "PIPE")
                     or name == "subprocess.check_output" else
                     "inherited" if "stdout" not in keywords and not unpacked_keywords else
                     "dynamic")
    stderr_status = ("captured" if capture_output
                     or subprocess_constant("stderr", "PIPE") else
                     "inherited" if "stderr" not in keywords and not unpacked_keywords else
                     "dynamic")
    stdio_bounded = (shell_status in {"default_false", "explicit_false"}
                     and stdin_status == "devnull"
                     and stdout_status == "captured"
                     and stderr_status == "captured")
    return {
        "process_shell_status": shell_status,
        "process_shell_disabled_verified": shell_status in {"default_false", "explicit_false"},
        "process_command_source": command_source,
        "process_argv_container_verified": argv_container,
        "process_literal_argv_verified": literal_argv,
        "process_executable_syntax": executable,
        "process_argv_argument_count": len(argv_tokens) if argv_container else None,
        "process_argv_dynamic_argument_count": (
            sum(token is None for token in argv_tokens) if argv_container else None),
        "process_literal_options": literal_options,
        "process_literal_file_output_switches": literal_file_output_switches,
        "process_dynamic_arguments_require_review": (
            not argv_container or any(token is None for token in argv_tokens)),
        "process_command_effect_classification": effect_classification,
        "process_cwd_syntax": keyword_source("cwd"),
        "process_env_syntax": keyword_source("env", literal_mapping=True),
        "process_stdin_syntax": stdin_status,
        "process_stdout_syntax": stdout_status,
        "process_stderr_syntax": stderr_status,
        "process_stdio_bounded_verified": stdio_bounded,
        "process_effect_verified_read_only": False,
        "process_assessment": (
            "stdio is source-bound and bounded; filesystem/network command effects still require review"
            if stdio_bounded else
            "command stdio and effects require review even when shell use is disabled"),
    }


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


def _classify_call(node: ast.Call, flag_bindings=None) -> tuple[str, str]:
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
        names = _flag_names(flags, flag_bindings) if flags is not None else None
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
        self.flag_bindings: list[dict[str, ast.AST]] = []
        self.dominating_guards: list[list[int]] = []
        self.direct_name_calls: list[dict] = []
        self.rows: list[dict] = []
        self.dispositions: list[dict] = []

    def _visit_scope(self, node, name: str):
        collector = _ScopeCalls()
        for child in node.body:
            collector.visit(child)
        guards = sorted(n.lineno for n in collector.calls
                        if _call_name(n).rsplit(".", 1)[-1] in _GUARDS)
        self.scope.append((name, guards))
        bindings = (_direct_local_flag_bindings(node)
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else {})
        self.flag_bindings.append(bindings)
        self.dominating_guards.append([])
        for child in node.body:
            self.visit(child)
            guard_line = _direct_guard_line(child)
            if guard_line is not None:
                self.dominating_guards[-1].append(guard_line)
        self.dominating_guards.pop()
        self.flag_bindings.pop()
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
        self.flag_bindings.append({})
        self.dominating_guards.append([])
        self.visit(node.body)
        self.dominating_guards.pop()
        self.flag_bindings.pop()
        self.scope.pop()

    def visit_Call(self, node):
        bindings = {
            name: value for name, value in (self.flag_bindings[-1].items()
                                            if self.flag_bindings else ())
            if value.lineno < node.lineno
        }
        if isinstance(node.func, ast.Name):
            caller_scope = self.scope[-1][0] if self.scope else "<module>"
            caller_guards = list(self.dominating_guards[-1]
                                 if self.dominating_guards else ())
            segment = ast.get_source_segment(self.source, node) or ""
            self.direct_name_calls.append({
                "callee": node.func.id,
                "caller_scope": caller_scope,
                "line": node.lineno,
                "dominating_guard_lines_in_scope": caller_guards,
                "guard_control_flow_verified": bool(caller_guards),
                "source_segment_sha256": hashlib.sha256(
                    segment.encode("utf-8")).hexdigest(),
            })
        classification, api = _classify_call(node, bindings)
        if classification in {"write_candidate", "proven_non_filesystem_text_transform",
                              "proven_read_only_descriptor"}:
            function, guards = self.scope[-1] if self.scope else ("<module>", [])
            earlier = any(line < node.lineno for line in guards)
            dominating = list(self.dominating_guards[-1]
                              if self.dominating_guards else ())
            segment = ast.get_source_segment(self.source, node) or ""
            base = {
                "path": self.path,
                "line": node.lineno,
                "scope": function,
                "api": api,
                "source_file_sha256": self.source_file_sha256,
                "source_segment_sha256": hashlib.sha256(segment.encode("utf-8")).hexdigest(),
            }
            process_contract = _process_contract(node, bindings)
            if process_contract is not None:
                base.update(process_contract)
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
                    "dominating_guard_lines_in_scope": dominating,
                    "guard_control_flow_verified": bool(dominating),
                    "guard_assessment": (
                        "direct unconditional guard statement dominates this call; "
                        "callee/caller contract review still required"
                        if dominating else
                        "lexical-only; manual control-flow review required"),
                    "review_required": True,
                })
        self.generic_visit(node)

    def attach_direct_local_callers(self, tree: ast.Module) -> None:
        """Attach observed direct callers without claiming a closed call graph."""
        definitions = {}
        for statement in tree.body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                definitions[statement.name] = definitions.get(statement.name, 0) + 1
        module_bindings = _LocalBindingCollector()
        for statement in tree.body:
            if not isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                module_bindings.visit(statement)
        eligible = {name for name, count in definitions.items()
                    if count == 1 and not module_bindings.stores.get(name)
                    and name not in module_bindings.external
                    and not module_bindings.dynamic_scope}
        by_callee = {
            name: sorted(({
                "caller_scope": call["caller_scope"],
                "line": call["line"],
                "dominating_guard_lines_in_scope": call[
                    "dominating_guard_lines_in_scope"],
                "guard_control_flow_verified": call[
                    "guard_control_flow_verified"],
                "source_segment_sha256": call["source_segment_sha256"],
            } for call in self.direct_name_calls if call["callee"] == name),
                key=lambda row: (row["line"], row["caller_scope"]))
            for name in eligible
        }
        for row in self.rows:
            callers = by_callee.get(row["scope"], [])
            row["direct_local_callers"] = callers
            row["direct_local_callers_source_bound"] = bool(callers)
            row["caller_closure_verified"] = False


def scan_python_source(source: str, path: str = "<memory>") -> list[dict]:
    """Return deterministic, line-ordered mutation candidates for human review."""
    if not isinstance(source, str):
        raise TypeError("Python source must be text")
    tree = ast.parse(source, filename=path)
    scanner = _Scanner(path, source)
    scanner.visit(tree)
    scanner.attach_direct_local_callers(tree)
    return sorted(scanner.rows, key=lambda row: (row["line"], row["api"]))


def scan_python_tree(root: Path, *, include_tests: bool = False) -> dict:
    """Scan repository Python sources without executing or changing any file."""
    raw_root = str(root)
    normalized_root = unicodedata.normalize("NFKC", raw_root)
    requested_root = Path(root)
    if (chr(92) in normalized_root or
            normalized_root.count("/") != raw_root.count("/") or
            ":" in normalized_root or
            any(part in (".", "..") for part in normalized_root.split("/")) or
            any(unicodedata.category(ch) in ("Cc", "Cf", "Cs", "Zl", "Zp")
                or 0xFDD0 <= ord(ch) <= 0xFDEF
                or (ord(ch) & 0xFFFE) == 0xFFFE for ch in raw_root)):
        raise ValueError("Ambiguous or traversing source root requires review")
    if any(part in (".", "..") for part in str(root).replace(chr(92), "/").split("/")):
        raise ValueError("Ambiguous or traversing source root requires review")
    if any(ancestor.is_symlink() for ancestor in (requested_root, *requested_root.parents)):
        raise ValueError("Symlinked source root or ancestor requires review")
    root = requested_root.resolve(strict=True)
    root_stat = root.stat(follow_symlinks=False)
    if not stat.S_ISDIR(root_stat.st_mode) or root_stat.st_nlink < 1:
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
        source_stat = file.stat(follow_symlinks=False)
        if not stat.S_ISREG(source_stat.st_mode):
            raise ValueError(f"Non-regular Python source requires review: {relative}")
        if source_stat.st_nlink != 1:
            raise ValueError(f"Hardlinked Python source requires review: {relative}")
        # Bind the read to the validated file descriptor instead of reopening
        # the path after lstat; reject a replacement between those operations.
        with file.open("rb") as handle:
            descriptor_stat = os.fstat(handle.fileno())
            if (descriptor_stat.st_dev, descriptor_stat.st_ino) != (source_stat.st_dev, source_stat.st_ino):
                raise ValueError(f"Python source replaced before audit read: {relative}")
            if not stat.S_ISREG(descriptor_stat.st_mode) or descriptor_stat.st_nlink != 1:
                raise ValueError(f"Unsafe Python source descriptor during audit: {relative}")
            source_bytes = handle.read()
            descriptor_after = os.fstat(handle.fileno())
            if (descriptor_stat.st_dev, descriptor_stat.st_ino, descriptor_stat.st_size,
                    descriptor_stat.st_mtime_ns, descriptor_stat.st_ctime_ns) != (
                    descriptor_after.st_dev, descriptor_after.st_ino, descriptor_after.st_size,
                    descriptor_after.st_mtime_ns, descriptor_after.st_ctime_ns):
                raise ValueError(f"Python source changed during audit: {relative}")
            source = source_bytes.decode("utf-8")
        after_stat = file.stat(follow_symlinks=False)
        if not stat.S_ISREG(after_stat.st_mode) or after_stat.st_nlink != 1:
            raise ValueError(f"Python source changed to unsafe file type during audit: {relative}")
        identity = lambda metadata: (metadata.st_dev, metadata.st_ino, metadata.st_mode,
                                     metadata.st_nlink, metadata.st_size,
                                     metadata.st_mtime_ns, metadata.st_ctime_ns)
        if identity(source_stat) != identity(after_stat):
            raise ValueError(f"Python source changed during audit: {relative}")
        scanned.append(relative)
        tree = ast.parse(source, filename=relative)
        scanner = _Scanner(relative, source)
        scanner.visit(tree)
        scanner.attach_direct_local_callers(tree)
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
            "Direct guard dominance is structural only; caller closure and callee contracts remain unverified.",
            "Dynamic aliases, subprocess/shell writes, generated code and non-Python writers need separate review.",
            "Every candidate remains review_required until individually dispositioned.",
            "Non-write dispositions are limited to source-hash-bound syntactic proofs.",
        ],
        "runtime_gate_enforced": False,
        "production_writes": False,
    }
