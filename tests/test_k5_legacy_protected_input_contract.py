"""K5 regression: isolated playlist export must never mutate its source input."""
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from madsc.isolated_playlist_bundle import export_isolated_previews


class K5LegacyProtectedInputContractTests(unittest.TestCase):
    def test_successful_export_preserves_source_bytes_and_writes_only_separate_outputs(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "CALISANLAR.m3u"
            original = (
                b'#EXTM3U\n'
                b'#EXTINF:-1 tvg-id="example",Example TV\n'
                b'https://example.org/live.m3u8\n'
            )
            source.write_bytes(original)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            destination = root / "isolated-drafts"

            manifest = export_isolated_previews(source, destination)

            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)
            self.assertEqual(source.read_bytes(), original)
            self.assertTrue(manifest["preview_only"])
            self.assertFalse(manifest["production_ready"])
            self.assertFalse(manifest["production_writes"])
            self.assertTrue(all((destination / name).is_file()
                                for name in manifest["files"]))
            self.assertFalse(any((source_dir / name).exists()
                                 for name in manifest["files"]))

    def test_rejected_destination_preserves_source_bytes(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "CALISANLAR.m3u"
            original = b"\n".join((b"#EXTM3U", b"#EXTINF:-1,Protected input", b"https://example.org/live", b""))
            source.write_bytes(original)
            before = hashlib.sha256(source.read_bytes()).hexdigest()
            protected_destination = root / "FAVORILER"

            with self.assertRaises(PermissionError):
                export_isolated_previews(source, protected_destination)

            self.assertFalse(protected_destination.exists())
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)
            self.assertEqual(source.read_bytes(), original)


    def test_manifest_serialization_failure_cleans_partial_bundle_and_preserves_source(self):
        from unittest.mock import patch
        import madsc.isolated_playlist_bundle as bundle

        with TemporaryDirectory() as directory:
            root = Path(directory)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "CALISANLAR.m3u"
            original = b"#EXTM3U\n#EXTINF:-1,Protected\nhttps://example.org/live\n"
            source.write_bytes(original)
            destination = root / "isolated-drafts"

            def partial_then_fail(manifest, handle, **kwargs):
                handle.write('{"partial":')
                raise OSError("simulated manifest serialization failure")

            with patch.object(bundle.json, "dump", side_effect=partial_then_fail):
                with self.assertRaisesRegex(OSError, "simulated manifest serialization failure"):
                    export_isolated_previews(source, destination)

            self.assertEqual(source.read_bytes(), original)
            self.assertFalse(destination.exists(),
                             "failed export must not leave a partial evidence directory")


if __name__ == "__main__":
    unittest.main()
