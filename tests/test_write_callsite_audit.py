import unittest
import tempfile
from pathlib import Path

from madsc.write_callsite_audit import scan_python_source, scan_python_tree


class WriteCallsiteAuditTests(unittest.TestCase):
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
        self.assertTrue(all(row["review_required"] for row in rows))

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

    def test_tree_scan_rejects_symlinked_python_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root / "real.py"
            outside.write_text("def write(path):\\n    path.write_text('x')\\n", encoding="utf-8")
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

    def test_invalid_python_fails_instead_of_silently_skipping(self):
        with self.assertRaises(SyntaxError):
            scan_python_source("def broken(:")


if __name__ == "__main__":
    unittest.main()
