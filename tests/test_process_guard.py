import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.fixture_report_writer import write_exclusive_bytes
from madsc.process_guard import (
    DNS_RESOLVER,
    FIXED_TOOL_ENV,
    enforce_bounded_curl_process,
    enforce_dns_resolver_process,
    enforce_ffprobe_read_process,
    enforce_parity_consumer_process,
    enforce_reachability_curl_process,
)
from madsc.temp_workspace import guarded_temporary_directory
from madsc.write_path_audit import ProtectedWriteRejected


class ProcessGuardTests(unittest.TestCase):
    def test_dns_contract_is_exact_and_disables_bytecode(self):
        command = [sys.executable, "-I", "-B", "-c", DNS_RESOLVER, "example.org"]
        enforce_dns_resolver_process(command, "example.org")
        for changed in (command[:-1], command + ["extra"],
                        [*command[:2], "-c", *command[3:]]):
            with self.subTest(changed=changed), self.assertRaises(ProtectedWriteRejected):
                enforce_dns_resolver_process(changed, "example.org")

    def test_reachability_curl_contract_rejects_output_switch(self):
        url, resolve = "https://example.org/live.m3u8", "example.org:443:8.8.8.8"
        command = [
            "curl", "-q", "--silent", "--show-error", "--fail", "--noproxy", "*",
            "--proto", "=https", "--max-time", "9", "--connect-timeout", "4",
            "--max-filesize", "65536", "--range", "0-65535", "--resolve", resolve, url,
        ]
        enforce_reachability_curl_process(command, url, resolve,
                                          cwd=Path("/"), env=dict(FIXED_TOOL_ENV))
        with self.assertRaises(ProtectedWriteRejected):
            enforce_reachability_curl_process(
                command[:-1] + ["-o", "out", url], url, resolve,
                cwd=Path("/"), env=dict(FIXED_TOOL_ENV))

    def test_bounded_curl_contract_is_limit_bound(self):
        url, resolve, limit = "https://example.org/a.ts", "example.org:443:8.8.8.8", 188
        command = [
            "curl", "-q", "-fsS", "--noproxy", "*", "--proto", "=https",
            "--max-time", "9", "--connect-timeout", "4", "--max-filesize", "188",
            "--resolve", resolve, url,
        ]
        enforce_bounded_curl_process(command, url, resolve, limit,
                                     cwd=Path("/"), env=dict(FIXED_TOOL_ENV))
        with self.assertRaises(ProtectedWriteRejected):
            enforce_bounded_curl_process(command, url, resolve, limit + 1,
                                         cwd=Path("/"), env=dict(FIXED_TOOL_ENV))
        with self.assertRaises(ProtectedWriteRejected):
            enforce_bounded_curl_process(command, url, resolve, limit,
                                         cwd=Path("/"), env={**FIXED_TOOL_ENV, "HOME": "/tmp"})
        with patch("madsc.process_guard.shutil.which", return_value=None), \
             self.assertRaises(ProtectedWriteRejected):
            enforce_bounded_curl_process(command, url, resolve, limit,
                                         cwd=Path("/"), env=dict(FIXED_TOOL_ENV))

    def test_ffprobe_contract_requires_identity_bound_guarded_sample(self):
        with guarded_temporary_directory("madsc-k3-video-") as workspace:
            segment = workspace / "sample.ts"
            write_exclusive_bytes(segment, b"x" * 188, allowed_root=workspace)
            command = ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                       "-of", "json", str(segment)]
            enforce_ffprobe_read_process(command, segment, cwd=workspace,
                                         env=dict(FIXED_TOOL_ENV))
            with self.assertRaises(ProtectedWriteRejected):
                enforce_ffprobe_read_process(
                    command[:-2] + ["default=nw=1", str(segment)], segment,
                    cwd=workspace, env=dict(FIXED_TOOL_ENV))

    def test_ffprobe_rejects_ordinary_temp_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            segment = Path(folder) / "sample.ts"
            segment.write_bytes(b"x" * 188)
            command = ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                       "-of", "json", str(segment)]
            with self.assertRaises(ProtectedWriteRejected):
                enforce_ffprobe_read_process(command, segment, cwd=Path(folder),
                                             env=dict(FIXED_TOOL_ENV))

    def test_parity_consumers_are_exact_and_repository_rooted(self):
        root = Path(__file__).resolve().parents[1]
        k1 = [sys.executable, "-m", "src.madsc_guard", "config/shadow_manifest.json"]
        enforce_parity_consumer_process(k1, consumer="k1", root=root)
        k5 = [sys.executable, "-m", "madsc.artifact_transport", "produce", "--path",
              "reports/k2-candidates.json", "--source", "reports/k2-input.m3u",
              "--run-id", "123", "--commit-sha", "a" * 40]
        enforce_parity_consumer_process(k5, consumer="k5", root=root,
                                        run_id="123", commit_sha="a" * 40)
        with self.assertRaises(ProtectedWriteRejected):
            enforce_parity_consumer_process(k1 + ["--extra"], consumer="k1", root=root)
        with self.assertRaises(ProtectedWriteRejected):
            enforce_parity_consumer_process(k5, consumer="k5", root=root,
                                            run_id="123", commit_sha="A" * 40)


if __name__ == "__main__":
    unittest.main()
