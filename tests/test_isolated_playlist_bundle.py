import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from madsc.isolated_playlist_bundle import export_isolated_previews


class IsolatedPlaylistBundleTests(unittest.TestCase):
    def test_creates_five_real_m3u_files_and_manifest_without_overwrite(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "input.m3u"
            source.write_text("#EXTM3U\n#EXTINF:-1,Test TV\nhttps://example.org/live.m3u8\n")
            out = root / "drafts"
            manifest = export_isolated_previews(source, out)
            self.assertEqual(len(manifest["files"]), 5)
            self.assertFalse(manifest["production_writes"])
            self.assertTrue(all((out / name).read_text().startswith("#EXTM3U")
                                for name in manifest["files"]))
            self.assertTrue((out / "manifest.json").is_file())
            self.assertEqual(json.loads((out / "manifest.json").read_text())["files"],
                             manifest["files"])
            with self.assertRaises(FileExistsError):
                export_isolated_previews(source, out)

    def test_rejects_source_tree_and_symlinked_destination(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            source = root / "source.m3u"
            source.write_text("#EXTM3U\n")
            with self.assertRaises(PermissionError):
                export_isolated_previews(source, root / "nested")
            target = root / "target"
            target.mkdir()
            alias = root / "alias"
            alias.symlink_to(target, target_is_directory=True)
            with self.assertRaises(FileExistsError):
                export_isolated_previews(source, alias)


if __name__ == "__main__":
    unittest.main()
