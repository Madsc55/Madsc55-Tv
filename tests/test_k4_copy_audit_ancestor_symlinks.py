"""Copy audit must not accept roots reached through symlinked ancestors."""
import tempfile
import unittest
from pathlib import Path

from madsc.backup import compare_copy, verify_sandbox_restore


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
                    with self.assertRaisesRegex(ValueError, "symlinked ancestors"):
                        compare_copy(source, destination, ["sample.txt"])
                    with self.assertRaisesRegex(ValueError, "symlinked ancestors"):
                        verify_sandbox_restore(source, destination, ["sample.txt"])


if __name__ == "__main__":
    unittest.main()
