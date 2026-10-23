"""Copy audit must not accept roots reached through symlinked ancestors."""
import tempfile
import unittest
from pathlib import Path

from madsc.backup import compare_copy, verify_sandbox_restore, verify_independent_restore


class CopyAuditAncestorSymlinkTests(unittest.TestCase):
    def test_rejects_aliased_source_or_destination_ancestor(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            left = base / "left"
            right = base / "right"
            left.mkdir()
            right.mkdir()
            (left / "sample.txt").write_bytes(b"same")
            (right / "sample.txt").write_bytes(b"same")
            alias = base / "alias"
            try:
                alias.symlink_to(left, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Directory symlinks unavailable")
            self.assertTrue(compare_copy(left, right, ["sample.txt"]))
            for source, destination in ((alias, right), (right, alias)):
                with self.subTest(source=source, destination=destination):
                    with self.assertRaisesRegex(ValueError, "symlinked ancestors|requires real directories|must be real directories"):
                        compare_copy(source, destination, ["sample.txt"])
                    with self.assertRaisesRegex(ValueError, "symlinked ancestors|requires real directories|must be real directories"):
                        verify_sandbox_restore(source, destination, ["sample.txt"])


    def test_three_tree_restore_rejects_aliased_ancestor(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "sample.txt").write_bytes(b"same")
            alias = base / "alias"
            try:
                alias.symlink_to(roots[1], target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Directory symlinks unavailable")
            with self.assertRaisesRegex(ValueError, "symlinked ancestors|requires real directories|must be real directories"):
                verify_independent_restore(roots[0], alias, roots[2], ["sample.txt"])


if __name__ == "__main__":
    unittest.main()
