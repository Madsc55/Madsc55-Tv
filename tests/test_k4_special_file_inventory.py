"""K4 sandbox inventory special-file regression.

This fixture never touches production paths or external storage.
"""
import os
import tempfile
import unittest
from pathlib import Path

from madsc.k4_restore_gate import audit_k4_restore


@unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO support required")
class K4SpecialFileInventoryTests(unittest.TestCase):
    def test_unexpected_fifo_in_restored_tree_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix="k4-fifo-") as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "fixture.txt").write_bytes(b"unchanged")
            os.mkfifo(roots[2] / "unexpected.pipe", 0o600)
            result = audit_k4_restore(*roots, ["fixture.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertFalse(result["external_storage_proven"])
            self.assertFalse(result["production_restore_approved"])
            self.assertFalse(result["production_writes"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")


if __name__ == "__main__":
    unittest.main()
