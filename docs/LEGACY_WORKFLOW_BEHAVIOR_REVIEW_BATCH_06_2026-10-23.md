# Legacy workflow behavioral review — batch 06 (2026-10-23)

Frozen legacy source: `Madsc55/madsc-tv`, baseline `ca374df3b9585c0d76a078db9536150ebbc260f7`. Static workflow/source inspection only; no live stream candidates or production playlists were changed.

## 1. `.github/workflows/besinci-zaman-asimi-test.yml`

Observed contract:
- Manual trigger and push when the workflow or `gelismis_medya_testi.py` changes.
- Runs a mocked `subprocess.run` timeout test: timeout must produce `BELIRSIZ/BELIRSIZ`, `TEKRAR_TEST_BEKLIYOR`, a message that the stream is not considered corrupt, and exact timeout 65 seconds.
- Script's actual probe runs ffmpeg for up to 20 seconds of media with a 65-second process timeout and 12-second rw_timeout; candidate limit is clamped to 0–10 and defaults to 5.
- Only candidates with technical-flow and video/audio evidence are selected. This is not proof of channel identity or rights; the script does not edit the main playlist.

Parity evidence needed: same frozen CSV fixture, output CSV schema and rows, candidate ordering and limit, ffmpeg missing, timeout, nonzero exit, invalid URL, and no protected playlist mutation. Status: reviewed-source, not accepted.

## 2. `.github/workflows/dokuzuncu-akilli-tekrar-test.yml`

Observed contract:
- Manual and push triggers on scheduler code, tests, or workflow; contents read; no network permission escalation.
- Runs `python3 -m unittest -v test_akilli_tekrar_test_takvimi.py`.
- Scheduler reads `aday_bekletme/gecmis.json`, writes `aday_bekletme/AKILLI_TEKRAR_TEST_TAKVIMI.csv`, orders by URL, and chooses retry interval 2 hours for unverified candidates, 6/12 hours for candidates with technical+media evidence and two or fewer successes, 24 hours for three or more successes.
- The inspected test also verifies due-only retry calls and that the scheduler does not mutate the input records.
- Timestamp parsing uses `datetime.fromisoformat(...).astimezone(UTC)`; naive timestamps are implicitly interpreted in the runner's local timezone, and future timestamps are treated as not due. For deterministic behavior, naive-time handling should be made explicit and timezone-independent before acceptance.

Parity evidence needed: fixed clock/timezone, invalid and naive timestamps, future and exact-due boundaries, missing state, successful-run thresholds, deterministic output order, and byte/hash proof that input history and protected playlists remain unchanged. Status: reviewed-source, not accepted.

## 3. `.github/workflows/onikinci-hata-siniflandirma-test.yml`

Observed contract:
- Manual and push triggers; contents read; five-minute timeout.
- Exercises 5 conservative classifications: 401/403 access issue, possible geographic block, possible transient timeout, technical+media success with identity still unverified, and unknown reason.
- Creates a temporary CSV, invokes the real script, then asserts the generated report has the expected row/classification.
- Classification text explicitly avoids claiming a 401/403 proves token expiry, a single timeout proves permanent outage, or technical flow proves channel identity.
- Output is `aday_bekletme/ADAY_HATA_SINIFLANDIRMA.csv`; the script does not alter playlists.

Parity evidence needed: differential rows covering all recognized terms, precedence when multiple classes match, Turkish/English case variations, empty/malformed CSV, BOM/encoding, missing input, exact output schema, and proof no playlist write. Status: reviewed-source, not accepted.

## Batch summary
- Source YAMLs reviewed in this batch: 3.
- Cumulative source reviews documented in batches 01–06: 18 workflow YAMLs.
- Accepted behavioral parity in this batch: 0/3; overall accepted legacy workflow parity remains 0/92.
- Static review is not runtime parity; no live workflow was dispatched by this review.
