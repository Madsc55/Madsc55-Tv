"""CLI fails closed: absent real source cannot create an acceptance report."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.history_origin_cli import main


class HistoryOriginCliTests(unittest.TestCase):
    def test_missing_source_never_calls_github_or_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "accepted.json"
            argv = ["history_origin_cli", "--source-folder", str(root / "missing"),
                    "--manifest", str(root / "missing.json"), "--current-sha",
                    "a" * 40, "--output", str(output)]
            with patch("sys.argv", argv), patch(
                    "madsc.history_origin_cli.verify_live_github_origin") as api:
                with self.assertRaises(ValueError):
                    main()
                api.assert_not_called()
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
