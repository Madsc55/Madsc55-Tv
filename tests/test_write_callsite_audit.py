import unittest

from madsc.write_callsite_audit import scan_python_source


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
        self.assertEqual([row["api"] for row in rows], ["path.open", "write"])
        self.assertTrue(all(row["review_required"] for row in rows))

    def test_file_object_write_and_writelines_are_inventory_candidates(self):
        source = '''\ndef emit(handle):\n    handle.write("one")\n    handle.writelines(["two", "three"])\n'''
        rows = scan_python_source(source, "file_writer.py")
        self.assertEqual([row["api"] for row in rows], ["write", "writelines"])
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

    def test_invalid_python_fails_instead_of_silently_skipping(self):
        with self.assertRaises(SyntaxError):
            scan_python_source("def broken(:")


if __name__ == "__main__":
    unittest.main()
