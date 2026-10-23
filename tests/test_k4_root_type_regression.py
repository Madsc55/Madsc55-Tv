"""K4: non-directory sandbox roots must never be accepted.

Uses only disposable temporary files and no production paths.
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.k4_restore_gate import audit_k4_restore


class K4RootTypeRegressionTests(unittest.TestCase):
    def test_fifo_root_rejected_before_manifest_read(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO not supported on this platform")
        with tempfile.TemporaryDirectory(prefix="k4-root-type-") as temporary:
            base = Path(temporary)
            source = base / "source"
            backup = base / "backup"
            restored = base / "restored"
            source.mkdir()
            backup.mkdir()
            os.mkfifo(restored, 0o600)
            with patch("madsc.k4_restore_gate.snapshot_manifest") as manifest:
                with self.assertRaisesRegex(ValueError, "real directory"):
                    audit_k4_restore(source, backup, restored, ["file.txt"])
                manifest.assert_not_called()

    def test_regular_file_root_rejected_before_manifest_read(self):
        with tempfile.TemporaryDirectory(prefix="k4-root-type-") as temporary:
            base = Path(temporary)
            source = base / "source"
            backup = base / "backup"
            restored = base / "restored"
            source.mkdir()
            backup.mkdir()
            restored.write_bytes(b"not a directory")
            with patch("madsc.k4_restore_gate.snapshot_manifest") as manifest:
                with self.assertRaisesRegex(ValueError, "real directory"):
                    audit_k4_restore(source, backup, restored, ["file.txt"])
                manifest.assert_not_called()


if __name__ == "__main__":
    unittest.main()
