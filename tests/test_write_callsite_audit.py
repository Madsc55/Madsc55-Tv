import os
import unittest
import tempfile
from pathlib import Path

from madsc.write_callsite_audit import scan_python_source, scan_python_tree


class WriteCallsiteAuditTests(unittest.TestCase):
    def test_artifact_transport_writes_have_direct_k1_guard_dominance(self):
        source = (Path(__file__).resolve().parents[1] / "madsc" /
                  "artifact_transport.py").read_text(encoding="utf-8")
        rows = scan_python_source(source, "madsc/artifact_transport.py")
        self.assertEqual(rows, [])
        scope = source[source.index("def _write_json_exclusive"):
                       source.index("\n\ndef main")]
        policy_guard = scope.index("enforce_write_paths")
        local_guard = scope.index("enforce_local_output_path")
        descriptor_write = scope.index("write_exclusive_bytes")
        self.assertLess(policy_guard, descriptor_write)
        self.assertLess(local_guard, descriptor_write)

    def test_detects_mutations_and_marks_earlier_guard(self):
        source = '''
from pathlib import Path
from madsc.write_path_audit import enforce_write_paths

def guarded(root):
    enforce_write_paths(["reports/out.json"])
    (root / "out.json").write_text("ok")

def unguarded(root):
    (root / "other.json").write_bytes(b"x")
'''
        rows = scan_python_source(source, "sample.py")
        self.assertEqual([row["api"] for row in rows], ["write_text", "write_bytes"])
        self.assertTrue(rows[0]["recognized_guard_precedes_write_in_scope"])
        self.assertTrue(rows[0]["guard_control_flow_verified"])
        self.assertEqual(rows[0]["dominating_guard_lines_in_scope"], [6])
        self.assertFalse(rows[1]["recognized_guard_precedes_write_in_scope"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_nested_function_guard_does_not_cover_outer_write(self):
        source = '''
def outer(root):
    def inner():
        enforce_write_paths(["reports/safe.json"])
    (root / "out.json").write_text("not guarded")
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["recognized_guard_precedes_write_in_scope"])

    def test_lambda_guard_does_not_cover_outer_write(self):
        source = '''\ndef outer(root):\n    deferred = lambda: enforce_write_paths(["reports/safe.json"])\n    (root / "out.json").write_text("not guarded")\n'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["api"], "write_text")
        self.assertFalse(rows[0]["recognized_guard_precedes_write_in_scope"])
        self.assertEqual(rows[0]["scope"], "outer")

    def test_conditional_guard_is_never_claimed_as_control_flow_verified(self):
        source = '''
def maybe_guard(root, enabled):
    if enabled:
        enforce_write_paths(["reports/out.json"])
    (root / "out.json").write_text("review me")
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["recognized_guard_precedes_write_in_scope"])
        self.assertFalse(rows[0]["guard_control_flow_verified"])
        self.assertIn("manual control-flow review", rows[0]["guard_assessment"])
        self.assertTrue(rows[0]["review_required"])

    def test_direct_guard_dominates_write_nested_in_later_statement(self):
        source = '''
def guarded(root, enabled):
    enforce_write_paths(["reports/out.json"])
    if enabled:
        (root / "out.json").write_text("ok")
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["guard_control_flow_verified"])
        self.assertEqual(rows[0]["dominating_guard_lines_in_scope"], [3])

    def test_direct_local_callers_are_source_bound_without_claiming_closure(self):
        source = '''
def writer(path):
    path.write_text("data")

def guarded(path):
    enforce_write_paths(["reports/out.json"])
    writer(path)

def unguarded(path):
    writer(path)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        callers = rows[0]["direct_local_callers"]
        self.assertEqual([row["caller_scope"] for row in callers],
                         ["guarded", "unguarded"])
        self.assertTrue(callers[0]["guard_control_flow_verified"])
        self.assertFalse(callers[1]["guard_control_flow_verified"])
        self.assertTrue(rows[0]["direct_local_callers_source_bound"])
        self.assertFalse(rows[0]["caller_closure_verified"])

    def test_rebound_or_dynamic_module_function_has_no_local_caller_claim(self):
        source = '''
def writer(path):
    path.write_text("data")
writer = decorate(writer)
writer(target)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["direct_local_callers"], [])
        self.assertFalse(rows[0]["direct_local_callers_source_bound"])
        self.assertFalse(rows[0]["caller_closure_verified"])

    def test_guard_in_try_does_not_claim_control_flow_dominance(self):
        source = '''
def uncertain(root):
    try:
        enforce_write_paths(["reports/out.json"])
    except Exception:
        pass
    (root / "out.json").write_text("review")
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["recognized_guard_precedes_write_in_scope"])
        self.assertFalse(rows[0]["guard_control_flow_verified"])
        self.assertEqual(rows[0]["dominating_guard_lines_in_scope"], [])

    def test_read_only_open_is_not_a_mutation(self):
        source = '''
def read(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()
'''
        self.assertEqual(scan_python_source(source), [])

    def test_write_open_and_filesystem_mutators_are_detected(self):
        source = '''
def mutate(path, folder):
    open(path, "w")
    folder.mkdir()
    folder.unlink()
'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows], ["open", "folder.mkdir", "folder.unlink"])
        self.assertEqual([row["line"] for row in rows], [3, 4, 5])

    def test_pathlib_open_with_write_mode_is_detected(self):
        source = '''
def mutate(path):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("data")
'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows], ["path.open", "handle.write"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_file_object_write_and_writelines_are_inventory_candidates(self):
        source = '''\ndef emit(handle):\n    handle.write("one")\n    handle.writelines(["two", "three"])\n'''
        rows = scan_python_source(source, "file_writer.py")
        self.assertEqual([row["api"] for row in rows], ["handle.write", "handle.writelines"])
        self.assertEqual([row["line"] for row in rows], [3, 4])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_dynamic_positional_and_keyword_open_modes_are_reviewed(self):
        source = '''\ndef mutate(path, requested_mode):\n    open(path, requested_mode)\n    path.open(requested_mode)\n    open(path, mode=requested_mode)\n'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 3)
        self.assertEqual([row["api"] for row in rows],
                         ["open [dynamic mode]", "path.open [dynamic mode]",
                          "open [dynamic mode]"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_process_launchers_are_reviewed_for_external_writes(self):
        source = '''\nimport subprocess\ndef run_command():\n    subprocess.run(["cp", "source", "destination"])\n    os.system("echo data > output.txt")\n'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["subprocess.run [process command requires review]",
                          "os.system [process command requires review]"])
        self.assertEqual(rows[0]["process_shell_status"], "default_false")
        self.assertTrue(rows[0]["process_shell_disabled_verified"])
        self.assertTrue(rows[0]["process_literal_argv_verified"])
        self.assertEqual(rows[0]["process_executable_syntax"], "cp")
        self.assertEqual(rows[1]["process_shell_status"], "implicit_shell")
        self.assertFalse(rows[1]["process_shell_disabled_verified"])
        self.assertFalse(rows[1]["process_literal_argv_verified"])
        self.assertTrue(all(not row["process_effect_verified_read_only"] for row in rows))
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_process_shell_keyword_unpacking_and_dynamic_values_stay_unknown(self):
        source = '''\nimport subprocess\ndef run_commands(options, dynamic):\n    subprocess.run(["tool"], **options)\n    subprocess.Popen(["tool"], shell=dynamic)\n    subprocess.call(["tool"], shell=True)\n'''
        rows = scan_python_source(source)
        self.assertEqual([row["process_shell_status"] for row in rows],
                         ["unknown_keyword_unpacking", "dynamic", "explicit_true"])
        self.assertTrue(all(not row["process_shell_disabled_verified"] for row in rows))
        self.assertTrue(all(not row["process_effect_verified_read_only"] for row in rows))

    def test_process_executable_resolves_only_safe_direct_local_argv_binding(self):
        source = '''
import subprocess
def run_commands(url, dynamic):
    command = ["curl", url]
    subprocess.run(command)
    reassigned = ["safe", url]
    reassigned = dynamic
    subprocess.run(reassigned)
    if dynamic:
        conditional = ["conditional", url]
    subprocess.run(conditional)
'''
        rows = scan_python_source(source)
        self.assertEqual(rows[0]["process_command_source"],
                         "direct_local_single_assignment")
        self.assertTrue(rows[0]["process_argv_container_verified"])
        self.assertFalse(rows[0]["process_literal_argv_verified"])
        self.assertEqual(rows[0]["process_executable_syntax"], "curl")
        for row in rows[1:]:
            self.assertEqual(row["process_command_source"], "unresolved_name")
            self.assertFalse(row["process_argv_container_verified"])
            self.assertIsNone(row["process_executable_syntax"])
            self.assertFalse(row["process_effect_verified_read_only"])

    def test_builtin_and_io_open_use_the_correct_mode_argument(self):
        source = '''\nimport builtins\nimport io\ndef mutate():\n    builtins.open("output.txt", "w")\n    io.open("output2.txt", mode="a")\n    builtins.open("input.txt", "r")\n'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["builtins.open", "io.open"])

    def test_os_open_flags_are_not_swallowed_by_generic_open_detection(self):
        source = '''\nimport os\ndef mutate(flags):\n    os.open("output.txt", os.O_WRONLY | os.O_CREAT)\n    os.open("output2.txt", flags=flags)\n'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["os.open [flags require review]",
                          "os.open [flags require review]"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_os_open_complex_flags_are_always_reviewed(self):
        source = '''
import os
def mutate(path, flags, enabled):
    os.open(path, build_flags(flags))
    os.open(path, flags if enabled else os.O_RDONLY)
    os.open(path, flags=~flags)
    os.open(path, (flags,))
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 4)
        self.assertEqual([row["api"] for row in rows],
                         ["os.open [flags require review]"] * 4)
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_proven_read_only_os_open_is_dispositioned_out_of_candidates(self):
        source = '''
import os
def read(path):
    os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0))
'''
        self.assertEqual(scan_python_source(source), [])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "reader.py").write_text(source, encoding="utf-8")
            report = scan_python_tree(root)
        self.assertEqual(report["candidate_callsite_count"], 0)
        self.assertEqual(report["non_write_disposition_count"], 2)
        self.assertTrue(all(
            row["disposition"] == "proven_read_only_descriptor"
            and not row["review_required"]
            and len(row["source_file_sha256"]) == 64
            and len(row["source_segment_sha256"]) == 64
            for row in report["non_write_dispositions"]
        ))

    def test_dynamic_or_unknown_os_open_flags_remain_fail_closed(self):
        source = '''
import os
def read(path, flags):
    os.open(path, flags)
    os.open(path, os.O_RDONLY | custom_flag())
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_single_direct_local_read_only_flags_are_source_bound_dispositions(self):
        source = '''
import os
def read(path):
    base = os.O_RDONLY | os.O_NOFOLLOW
    flags = base | getattr(os, "O_NONBLOCK", 0)
    os.open(path, flags)
'''
        self.assertEqual(scan_python_source(source), [])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "reader.py").write_text(source, encoding="utf-8")
            report = scan_python_tree(root)
        self.assertEqual(report["candidate_callsite_count"], 0)
        self.assertEqual(report["non_write_disposition_count"], 1)
        row = report["non_write_dispositions"][0]
        self.assertEqual(row["disposition"], "proven_read_only_descriptor")
        self.assertEqual(len(row["source_file_sha256"]), 64)

    def test_unsafe_or_non_dominating_local_flag_bindings_remain_fail_closed(self):
        source = '''
import os
def parameter(path, flags):
    flags = os.O_RDONLY
    os.open(path, flags)
def reassigned(path):
    flags = os.O_RDONLY
    flags = os.O_RDWR
    os.open(path, flags)
def conditional(path, enabled):
    if enabled:
        flags = os.O_RDONLY
    os.open(path, flags)
def after(path):
    os.open(path, flags)
    flags = os.O_RDONLY
def external(path):
    global flags
    flags = os.O_RDONLY
    os.open(path, flags)
def imported(path):
    flags = os.O_RDONLY
    from os import O_WRONLY as flags
    os.open(path, flags)
def captured(path, value):
    flags = os.O_RDONLY
    match value:
        case flags:
            pass
    os.open(path, flags)
def closure(path):
    flags = os.O_RDONLY
    def change():
        nonlocal flags
        flags = os.O_WRONLY
    change()
    os.open(path, flags)
def dynamic(path):
    flags = os.O_RDONLY
    exec("flags = os.O_WRONLY")
    os.open(path, flags)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 9)
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_single_direct_local_write_flags_remain_write_candidates(self):
        source = '''
import os
def write(path):
    flags = os.O_WRONLY | os.O_CREAT
    os.open(path, flags)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertIn("flags require review", rows[0]["api"])

    def test_only_syntactically_proven_text_replace_is_dispositioned(self):
        source = '''
def transform(value, path):
    "literal".replace("a", "b")
    value.strip().replace("a", "b")
    path.replace(destination)
'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["value.strip.replace", "path.replace"])
        self.assertTrue(all(row["review_required"] for row in rows))
        self.assertTrue(all(len(row["source_file_sha256"]) == 64 for row in rows))
        self.assertTrue(all(len(row["source_segment_sha256"]) == 64 for row in rows))

    def test_fdopen_write_modes_and_tempfile_creation_are_reviewed(self):
        source = '''
import os
import tempfile
def mutate(fd, requested_mode):
    os.fdopen(fd, "wb")
    os.fdopen(fd, mode=requested_mode)
    os.fdopen(fd, "rb")
    tempfile.NamedTemporaryFile()
    tempfile.mkstemp()
'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows], [
            "os.fdopen",
            "os.fdopen [dynamic mode]",
            "tempfile.NamedTemporaryFile [temporary filesystem creation requires review]",
            "tempfile.mkstemp [temporary filesystem creation requires review]",
        ])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_open_keyword_unpacking_requires_review(self):
        source = '''
def write(path, options):
    open(path, **options)
    path.open(**options)
    open(path, "r", **options)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 3)
        self.assertTrue(all("[dynamic mode]" in row["api"] for row in rows))

    def test_fdopen_keyword_unpacking_requires_review(self):
        source = '''
import os
def mutate(fd, options):
    os.fdopen(fd, **options)
    os.fdopen(fd, "rb", **options)
    os.fdopen(fd, mode="rb", **options)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(row["api"] == "os.fdopen [dynamic mode]" for row in rows))

    def test_descriptor_level_writes_are_inventoried(self):
        source = '''
import os
def mutate(fd):
    os.write(fd, b"data")
    os.writev(fd, [b"data"])
    os.pwrite(fd, b"data", 0)
    os.pwritev(fd, [b"data"], 0)
    os.ftruncate(fd, 0)
'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["os.write", "os.writev", "os.pwrite",
                          "os.pwritev", "os.ftruncate"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_spooled_tempfile_creation_is_reviewed(self):
        source = '''
import tempfile
def create():
    tempfile.SpooledTemporaryFile(max_size=1)
'''
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["api"],
                         "tempfile.SpooledTemporaryFile [temporary filesystem creation requires review]")
        self.assertTrue(rows[0]["review_required"])

    def test_definition_time_mutations_are_inventoried_in_enclosing_scope(self):
        source = """
@decorator(path.write_text("decorator"))
def outer(value=path.write_bytes(b"default")):
    return value

class Example(factory(path.mkdir())):
    pass

async def async_outer(value=path.touch()):
    return value
"""
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["path.write_text", "path.write_bytes",
                          "path.mkdir", "path.touch"])
        self.assertTrue(all(row["scope"] == "<module>" for row in rows))
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_lambda_default_mutation_is_in_outer_scope(self):
        source = "def outer(path):\n    callback = lambda value=path.touch(): value\n"
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["api"], "path.touch")
        self.assertEqual(rows[0]["scope"], "outer")

    def test_special_file_and_extended_attribute_mutations(self):
        source = (
            "import os\n"
            "def change(path):\n"
            "    os.mkfifo(path)\n"
            "    os.mknod(path)\n"
            "    os.setxattr(path, 'user.flag', b'1')\n"
            "    os.removexattr(path, 'user.flag')\n"
            "    path.chown(1, 1)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["os.mkfifo", "os.mknod", "os.setxattr",
                          "os.removexattr", "path.chown"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_archive_extraction_and_legacy_hardlink_are_reviewed(self):
        source = (
            "import shutil\n"
            "def unpack(archive, folder, target):\n"
            "    shutil.unpack_archive(archive, folder)\n"
            "    archive.extractall(folder)\n"
            "    target.link_to(folder)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["shutil.unpack_archive", "archive.extractall",
                          "target.link_to"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_unknown_method_chain_replace_stays_reviewable(self):
        source = (
            "def check(candidate):\n"
            "    candidate.lower().replace('old', 'new')\n"
            "    'literal'.lower().replace('old', 'new')\n"
        )
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["api"], "candidate.lower.replace")
        self.assertTrue(rows[0]["review_required"])

    def test_os_open_unpacked_keywords_never_proven_read_only(self):
        source = (
            "import os\n"
            "def check(path, options):\n"
            "    os.open(path, os.O_RDONLY, **options)\n"
            "    os.open(path, flags=os.O_RDONLY, **options)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all("dynamic flags require review" in row["api"]
                            for row in rows))
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_tree_scan_rejects_symlinked_python_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root / "real.py"
            outside.write_text("def write(path):\n    path.write_text('x')\n", encoding="utf-8")
            (root / "linked.py").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "Symlinked source entry"):
                scan_python_tree(root)

    def test_tree_scan_rejects_symlinked_source_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            actual = root / "actual"
            actual.mkdir()
            (actual / "writer.py").write_text("print('ok')", encoding="utf-8")
            (root / "linked_dir").symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlinked source entry"):
                scan_python_tree(root)

    def test_tree_scan_rejects_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "missing_source").symlink_to(root / "does_not_exist")
            with self.assertRaisesRegex(ValueError, "Symlinked source entry"):
                scan_python_tree(root)

    def test_metadata_mutations_are_inventoried(self):
        source = '''
import os
from pathlib import Path
def mutate(path, fd):
    os.chmod(path, 0o600)
    os.fchmod(fd, 0o600)
    os.chown(path, 1, 1)
    os.utime(path, None)
    Path(path).chmod(0o600)
    Path(path).lchmod(0o600)
'''
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["os.chmod", "os.fchmod", "os.chown",
                          "os.utime", "Path.chmod", "Path.lchmod"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_tree_scan_rejects_symlinked_root(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            actual = parent / "actual"
            actual.mkdir()
            (parent / "linked_root").symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlinked source root"):
                scan_python_tree(parent / "linked_root")

    def test_starred_modes_are_reviewed(self):
        source = (
            'def check(path, fd, args):\n'
            '    open(path, *args)\n'
            '    path.open(*args)\n'
            '    os.fdopen(fd, *args)\n'
        )
        rows = scan_python_source(source)
        self.assertEqual(len(rows), 3)
        self.assertTrue(all('dynamic mode' in row['api'] for row in rows))
        self.assertTrue(all(row['review_required'] for row in rows))

    def test_tree_scan_rejects_fifo_python_source(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO is unavailable on this platform")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.mkfifo(root / "blocked.py")
            with self.assertRaisesRegex(ValueError, "Non-regular Python source"):
                scan_python_tree(root)

    def test_shutil_metadata_copy_mutations_are_inventoried(self):
        source = (
            "import shutil\n"
            "def mutate(source, target):\n"
            "    shutil.copymode(source, target)\n"
            "    shutil.copystat(source, target)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["shutil.copymode", "shutil.copystat"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_shutil_copyfileobj_write_is_inventoried(self):
        source = "import shutil\ndef transfer(source, target):\n    shutil.copyfileobj(source, target)\n"
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows], ["shutil.copyfileobj"])
        self.assertTrue(rows[0]["review_required"])

    def test_descriptor_transfer_writes_are_inventoried(self):
        source = (
            "import os\n"
            "def transfer(src, dst):\n"
            "    os.sendfile(dst, src, 0, 10)\n"
            "    os.copy_file_range(src, dst, 10)\n"
            "    os.splice(src, dst, 10)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["os.sendfile", "os.copy_file_range", "os.splice"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_os_process_launchers_are_reviewed(self):
        source = (
            "import os\n"
            "def run(program, argv, env):\n"
            "    os.posix_spawn(program, argv, env)\n"
            "    os.posix_spawnp(program, argv, env)\n"
            "    os.spawnv(0, program, argv)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"].split(" [")[0] for row in rows],
                         ["os.posix_spawn", "os.posix_spawnp", "os.spawnv"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_os_exec_process_replacements_are_reviewed(self):
        source = (
            "import os\n"
            "def replace_process(program, argv, env):\n"
            "    os.execv(program, argv)\n"
            "    os.execve(program, argv, env)\n"
            "    os.execl(program, program)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"].split(" [")[0] for row in rows],
                         ["os.execv", "os.execve", "os.execl"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_serializer_and_metadata_methods_are_reviewed(self):
        source = (
            "def emit(writer, path):\n"
            "    writer.writeheader()\n"
            "    writer.writerow(['a'])\n"
            "    writer.writerows([['b']])\n"
            "    path.setxattr('key', b'value')\n"
            "    path.removexattr('key')\n"
            "    path.utime(None)\n"
        )
        rows = scan_python_source(source)
        self.assertEqual([row["api"] for row in rows],
                         ["writer.writeheader", "writer.writerow", "writer.writerows",
                          "path.setxattr", "path.removexattr", "path.utime"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_invalid_python_fails_instead_of_silently_skipping(self):
        with self.assertRaises(SyntaxError):
            scan_python_source("def broken(:")


if __name__ == "__main__":
    unittest.main()
