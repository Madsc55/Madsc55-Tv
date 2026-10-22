import hashlib
import io
import json
import unittest
import zipfile

from madsc.legacy_pair_artifact import (MANIFEST_NAME,
                                        verify_parity_artifact_manifest,
                                        verify_provenance_pair_artifacts)


PATH = ".github/workflows/example.yml"
BLOB = "1" * 40


def execution(repository, branch, workflow, workflow_blob, run_id, artifact_id):
    return {
        "repository": repository, "branch": branch,
        "workflow_path": workflow, "workflow_blob_sha": workflow_blob,
        "run_id": run_id, "run_attempt": 1,
        "head_sha": ("a" if run_id == 11 else "b") * 40,
        "event": "workflow_dispatch", "conclusion": "success",
        "artifact": {"id": artifact_id, "name": "parity", "repository": repository,
                     "run_id": run_id, "head_sha": ("a" if run_id == 11 else "b") * 40,
                     "sha256": "0" * 64},
        "input_sha256": "c" * 64,
        "snapshot": {"exit_code": 0, "timed_out": False,
                     "outputs": {"report": "d" * 64}, "side_effects": {}},
    }


def archive_for(origin, *, extra=None, mutate=None):
    manifest = {"schema": "madsc-parity-artifact-v1",
                "repository": origin["repository"], "run_id": origin["run_id"],
                "head_sha": origin["head_sha"], "workflow_path": origin["workflow_path"],
                "input_sha256": origin["input_sha256"], "snapshot": origin["snapshot"]}
    if mutate:
        mutate(manifest)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr(MANIFEST_NAME, json.dumps(manifest, sort_keys=True))
        if extra:
            bundle.writestr(extra, "unexpected")
    archive = output.getvalue()
    origin["artifact"]["sha256"] = hashlib.sha256(archive).hexdigest()
    return archive


class LegacyPairArtifactTests(unittest.TestCase):
    def setUp(self):
        self.pair = {
            "legacy": execution("Madsc55/madsc-tv", "madsc/bes-sistem-toplu-birlestirme",
                                PATH, BLOB, 11, 21),
            "replacement": execution("Madsc55/Madsc55-Tv", "main",
                                     ".github/workflows/madsc-05-genel-bakim.yml",
                                     "2" * 40, 12, 22),
        }

    def test_pair_manifests_bind_same_input_and_snapshots_without_acceptance(self):
        legacy = archive_for(self.pair["legacy"])
        replacement = archive_for(self.pair["replacement"])
        result = verify_provenance_pair_artifacts(
            PATH, BLOB, self.pair, legacy, replacement)
        self.assertTrue(result["artifact_manifests_verified"])
        self.assertTrue(result["same_input_artifacts_verified"])
        self.assertFalse(result["behavioral_parity_accepted"])
        self.assertFalse(result["production_ready"])

    def test_digest_extra_entry_and_manifest_mismatch_fail_closed(self):
        archive = archive_for(self.pair["legacy"])
        self.pair["legacy"]["artifact"]["sha256"] = "f" * 64
        with self.assertRaises(ValueError):
            verify_parity_artifact_manifest(self.pair["legacy"], archive)

        archive = archive_for(self.pair["legacy"], extra="extra.txt")
        with self.assertRaises(ValueError):
            verify_parity_artifact_manifest(self.pair["legacy"], archive)

        archive = archive_for(
            self.pair["legacy"], mutate=lambda value: value.update(input_sha256="e" * 64))
        with self.assertRaises(ValueError):
            verify_parity_artifact_manifest(self.pair["legacy"], archive)

    def test_duplicate_json_keys_are_rejected(self):
        origin = self.pair["legacy"]
        raw = ('{"schema":"madsc-parity-artifact-v1","schema":"duplicate",'
               '"repository":"x","run_id":1,"head_sha":"x",'
               '"workflow_path":"x","input_sha256":"x","snapshot":{}}')
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as bundle:
            bundle.writestr(MANIFEST_NAME, raw)
        archive = output.getvalue()
        origin["artifact"]["sha256"] = hashlib.sha256(archive).hexdigest()
        with self.assertRaises(ValueError):
            verify_parity_artifact_manifest(origin, archive)


if __name__ == "__main__":
    unittest.main()
