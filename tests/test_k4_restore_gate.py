import tempfile
import unittest
from pathlib import Path

from madsc.k4_restore_gate import audit_k4_restore


class K4RestoreGateTests(unittest.TestCase):
    def test_independent_matching_trees_pass_sandbox_only(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            for name in ("source", "backup", "restored"):
                (base / name).mkdir()
                (base / name / "fixture.txt").write_bytes(b"original bytes")
            result = audit_k4_restore(base / "source", base / "backup",
                                      base / "restored", ["fixture.txt"])
            self.assertTrue(result["sandbox_restore_accepted"])
            self.assertFalse(result["production_restore_approved"])
            self.assertFalse(result["external_storage_proven"])
            self.assertFalse(result["production_writes"])

    def test_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            for name in ("source", "backup", "restored"):
                (base / name).mkdir()
                (base / name / "fixture.txt").write_bytes(b"original bytes")
            (base / "restored" / "fixture.txt").write_bytes(b"corrupt")
            result = audit_k4_restore(base / "source", base / "backup",
                                      base / "restored", ["fixture.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

    def test_nested_tree_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            for name in ("source", "backup"):
                (base / name).mkdir()
            (base / "backup" / "restored").mkdir()
            with self.assertRaises(ValueError):
                audit_k4_restore(base / "source", base / "backup",
                                 base / "backup" / "restored", ["fixture.txt"])


if __name__ == "__main__":
    unittest.main()
