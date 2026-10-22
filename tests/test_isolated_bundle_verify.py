import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from madsc.isolated_playlist_bundle import export_isolated_previews
from madsc.isolated_bundle_verify import verify_bundle


class IsolatedBundleVerifyTests(unittest.TestCase):
    def test_five_files_verify_and_mutation_fails(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "channels.m3u"
            source.write_text("#EXTM3U\\n#EXTINF:-1,Test\\nhttps://example.org/live\\n")
            output = root / "output"
            export_isolated_previews(source, output)
            self.assertTrue(verify_bundle(output)["verified"])
            path = output / "TEST_BEKLIYOR.m3u"
            path.write_bytes(path.read_bytes() + b"tampered")
            self.assertFalse(verify_bundle(output)["verified"])

    def test_manifest_cannot_claim_production_acceptance(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            source_dir = root / "source"
            source_dir.mkdir()
            source = source_dir / "channels.m3u"
            source.write_text("#EXTM3U\\n")
            output = root / "output"
            export_isolated_previews(source, output)
            manifest_path = output / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["production_ready"] = True
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                verify_bundle(output)


if __name__ == "__main__":
    unittest.main()
