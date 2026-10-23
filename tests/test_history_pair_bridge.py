"""K2 history bridge: legacy inputs stay unchanged, envelope stays coherent."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.history_pair_bridge import bridge_legacy_pair, merge_into_envelope
from madsc.history_pair_store import decode_pair, encode_pair


def pair(time, runs, state):
    row = {"last_test": time, "runs": runs, "last_result": state,
           "decision": "MANUAL_ONLY"}
    return {"gecmis.json": {"history": {"candidate": dict(row)}},
            "ana_liste_test_gecmisi.json": {"channels": {"candidate": dict(row)}}}


class HistoryPairBridgeTests(unittest.TestCase):
    def test_import_and_merge_keeps_legacy_bytes_and_manual_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / "legacy"
            legacy.mkdir()
            original = pair("2026-10-19T12:00:00Z", 2, "PASS")
            before = {}
            for name, document in original.items():
                path = legacy / name
                path.write_text(json.dumps(document), encoding="utf-8")
                before[name] = path.read_bytes()
            dest = root / "pair.json"
            self.assertEqual(bridge_legacy_pair(legacy, dest), original)
            incoming = pair("2026-10-20T12:00:00Z", 3, "FAIL")
            changes = merge_into_envelope(dest, incoming)
            self.assertEqual(changes["gecmis.json"]["updated"], 1)
            merged = decode_pair(dest.read_text(encoding="utf-8"))
            self.assertEqual(merged["gecmis.json"]["history"]["candidate"]["last_result"], "FAIL")
            self.assertEqual(merged["gecmis.json"]["history"]["candidate"]["decision"], "MANUAL_ONLY")
            for name in before:
                self.assertEqual((legacy / name).read_bytes(), before[name])

    def test_rejected_merge_and_replace_failure_keep_envelope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / "legacy"
            legacy.mkdir()
            original = pair("2026-10-19T12:00:00Z", 2, "PASS")
            for name, document in original.items():
                (legacy / name).write_text(json.dumps(document), encoding="utf-8")
            dest = root / "pair.json"
            bridge_legacy_pair(legacy, dest)
            before = dest.read_bytes()
            conflict = pair("2026-10-19T12:00:00Z", 2, "FAIL")
            with self.assertRaises(ValueError):
                merge_into_envelope(dest, conflict)
            self.assertEqual(dest.read_bytes(), before)
            with patch("madsc.history_pair_store.os.replace",
                       side_effect=OSError("injected failure")):
                with self.assertRaises(OSError):
                    merge_into_envelope(dest, pair("2026-10-20T12:00:00Z", 3, "FAIL"))
            self.assertEqual(dest.read_bytes(), before)

    def test_malformed_history_payload_types_rejected(self):
        for payload in (None, [], "invalid", 7):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    encode_pair(payload)
                raw = json.dumps({"schema": 1, "payload": payload, "sha256": "0" * 64})
                with self.assertRaises(ValueError):
                    decode_pair(raw)

    def test_history_envelope_rejects_boolean_schema_and_bad_digests(self):
        import hashlib
        payload = pair("2026-10-19T12:00:00Z", 2, "PASS")
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        for schema, checksum in ((True, digest), (1, None), (1, 123), (1, "x" * 64), (1, digest.upper())):
            with self.subTest(schema=schema, checksum=checksum):
                raw = json.dumps({"schema": schema, "payload": payload, "sha256": checksum})
                with self.assertRaises(ValueError):
                    decode_pair(raw)

    def test_duplicate_json_keys_rejected_even_when_digest_is_valid(self):
        import hashlib
        payload = pair("2026-10-19T12:00:00Z", 2, "PASS")
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        envelope = json.dumps({"schema": 1, "payload": payload, "sha256": digest})
        duplicated = envelope.replace('"schema": 1', '"schema": 1, "schema": 1', 1)
        with self.assertRaisesRegex(ValueError, "Duplicate history JSON key"):
            decode_pair(duplicated)
        nested = envelope.replace('"history": {', '"history": {}, "history": {', 1)
        with self.assertRaisesRegex(ValueError, "Duplicate history JSON key"):
            decode_pair(nested)

    def test_nonfinite_history_numbers_are_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                invalid = pair("2026-10-19T12:00:00Z", value, "PASS")
                with self.assertRaisesRegex(ValueError, "valid JSON"):
                    encode_pair(invalid)
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                raw = '{"schema":1,"payload":' + constant + ',"sha256":"' + "0" * 64 + '"}'
                with self.assertRaisesRegex(ValueError, "Non-finite"):
                    decode_pair(raw)

    def test_unpaired_surrogate_history_data_rejected_cleanly(self):
        import hashlib
        invalid = pair("2026-10-19T12:00:00Z", 2, "PASS")
        invalid["gecmis.json"]["history"]["candidate"]["last_result"] = chr(0xD800)
        with self.assertRaisesRegex(ValueError, "valid JSON"):
            encode_pair(invalid)
        raw_payload = json.dumps(invalid, ensure_ascii=True)
        # The JSON decoder accepts escaped lone surrogates, but UTF-8 hashing must not.
        raw = json.dumps({"schema": 1, "payload": json.loads(raw_payload), "sha256": "0" * 64})
        with self.assertRaisesRegex(ValueError, "Invalid history payload JSON"):
            decode_pair(raw)

    def test_symlink_legacy_input_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / "legacy"
            legacy.mkdir()
            (legacy / "gecmis.json").write_text("{}")
            (legacy / "ana_liste_test_gecmisi.json").symlink_to(legacy / "gecmis.json")
            with self.assertRaises(ValueError):
                bridge_legacy_pair(legacy, root / "pair.json")


if __name__ == "__main__":
    unittest.main()
