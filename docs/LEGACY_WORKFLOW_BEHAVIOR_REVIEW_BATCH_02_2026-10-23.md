# Legacy workflow behavioral review — batch 02 (2026-10-23)

Source repository: `Madsc55/madsc-tv`, frozen source commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Three YAML files were read without executing or modifying the legacy workflows. This is source behavior analysis only; it does not establish runtime parity.

## 1. `.github/workflows/aday-logo-epg-test.yml`

Observed contract:
- Triggers manually and on push to this workflow or `scripts/candidate_epg_logo_join.py`.
- `contents: read`, 10-minute job timeout.
- Compiles the candidate logo/EPG join script.
- Hashes `CALISANLAR.m3u` before and after running the script and requires exact SHA256 equality.
- Reads `madsc_kesif/candidate_epg_logo_join.json`; requires exactly five pilot EPG channels and forbids both `playlist_approved` and `ready_for_playlist` on every candidate result.
- Uploads that JSON report as artifact `aday-logo-epg-birlesim-test`.

Potential replacement: current `madsc/epg.py`, `madsc/epg_inventory.py`, and candidate evidence modules cover portions of validation, but the exact join report schema and protected playlist hash invariant must be mapped and tested. No parity acceptance yet.

Required evidence: before/after playlist hash equality; five-channel pilot; candidate approvals always false; JSON schema and artifact presence; syntax failure and missing-input cases fail closed.

## 2. `.github/workflows/aday-oncelik-kontrol.yml`

Observed contract:
- Manual and push triggers for `aday_oncelik_raporu.py` or its workflow.
- Compiles the priority script.
- Creates an isolated temporary fixture CSV with two candidates: a strong candidate with `VIDEO_SES_VAR` and a weak alternative with no media test.
- Runs the script in a temporary working directory.
- Requires two output rows and exact order/priority: Güçlü is priority 1, Zayıf is priority 5.
- No explicit permissions block or timeout is declared in the YAML.

Potential replacement: K2 candidate ranking/alternative mapping is a candidate, not yet proven equivalent. Need compare every score input, tie-break, missing-data behavior, stable ordering, output columns and priority values. The current two-row fixture is insufficient for full equivalence.

Required evidence: differential cases for all candidate types, ties, duplicate source, absent metadata, invalid media evidence, Turkish text/case normalization, stable output ordering, and unchanged protected playlist.

## 3. `.github/workflows/aday-bekletme.yml`

Observed contract:
- Manual and push triggers for the workflow and eight related candidate scripts.
- `contents: read`; concurrency group `aday-bekletme-main`, `cancel-in-progress: false`; 90-minute timeout.
- Checkout with `persist-credentials: false`; installs ffmpeg.
- Ordered pipeline: discover new channels; report duplicates; test audio/video; update quarantine records; build smart retest schedule; retest due candidates with `RETEST_LIMIT=5`; calculate source reliability scores; prioritize candidates.
- Uploads ten CSV/TXT/JSON report paths with `if: always()`; missing artifacts warn rather than fail upload.
- Because the artifact step uses `always()`, diagnostics should remain available even when an earlier command fails.

Potential replacement: K2/K3 candidate, duplicate-reason, probe, history, retest and ranking modules may correspond to individual stages. A single combined module or passing isolated tests does not establish ordering, persistent history semantics, retry limits, ffmpeg behavior or always-upload diagnostics parity.

Required evidence: stage-by-stage inputs/outputs; 5-candidate retest cap; ffmpeg unavailable/invalid media/timeout cases; history persistence; no protected playlist writes; concurrency serialization; partial failure still uploads all artifacts that were actually produced; exact exit and timeout semantics.

## Batch summary
- Source YAML behavior reviewed: 3/3 in this batch.
- Overall source reviews documented in batches 01 and 02: 6 workflow YAMLs.
- Accepted behavioral parity in this batch: 0/3.
- Overall accepted legacy workflow parity remains 0/92. No acceptance counter is raised by static source review alone.
- No Actions were dispatched; no legacy source, playlist, EPG, device data, or backups were changed.
