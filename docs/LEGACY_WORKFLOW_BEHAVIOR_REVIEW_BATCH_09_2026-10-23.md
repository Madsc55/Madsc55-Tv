# Legacy workflow behavior review — batch 09 (2026-10-23)

Frozen legacy source inventory: `Madsc55/madsc-tv`, tree `ca374df3b9585c0d76a078db9536150ebbc260f7`. This is read-only source review; none of these workflows was dispatched and no playlist or device data was changed.

## 1. `.github/workflows/ibo-yedek-kalite.yml`

- Workflow blob SHA: `da48c5195c35094a2a519feafd6b51f20f526edc`.
- Triggers: manual dispatch and path-filtered push; `contents: read`; checkout uses `persist-credentials: false`; 25-minute timeout; installs ffmpeg and always uploads a CSV quality report (missing artifact warns).
- Script `yedekler/ibo_yedek_kalite_tespit.py` blob SHA: `3539c625acc1070248b442782076283c2a0e0a31`.
- It reads `CALISANLAR.m3u`, selects backup-group entries, calls ffprobe concurrently (12 workers; 14-second per-call timeout), then **rewrites `CALISANLAR.m3u` in the runner workspace**, changing display-name quality suffixes. It preserves the URL lines and non-backup entries by intended logic, but it still writes a protected production playlist path. It writes the report to `yedekler/IBO_YEDEK_KALITE_RAPORU_2026-10-09.csv`.
- The workflow uploads only the CSV, not the rewritten playlist, and does not git-push; so this is not evidence of a persistent remote write. Nonetheless the workflow label understates the script's local mutation and any later step in the same job would see the modified file.
- Acceptance requires source/output separation (read protected playlist, write only an isolated copy or report), offline fixtures for no backup rows, ffprobe failures/timeouts, malformed EXTINF metadata, and byte-for-byte proof the input remains unchanged. **Status: reviewed-source, not accepted.**

## 2. `.github/workflows/iptv-test.yml`

- Workflow blob SHA: `5cd014cb94e68be22f5f68b07618920c82fee740`.
- Triggers: manual dispatch, every Wednesday at 06:30 UTC, and main-branch pushes touching `.github/commands/genel-guncelleme.txt`; concurrency group cancels in-progress runs; `contents: read`; 60-minute timeout; checkout explicitly selects `main`.
- Script `iptv_test.py` blob SHA: `14d0311951259c421be9afcfeb6fa41c50ce4aeb`.
- Despite the workflow name **“IPTV Salt Okunur Kanal Testi”**, the script reads the input `MADSC_TV_47_LISTE_ADAY.m3u` and an existing `CALISANLAR.m3u` for previous/favorite mappings, probes candidate streams via network and ffprobe, then writes/overwrites `CALISANLAR.m3u`, `CALISMAYANLAR.txt`, and `TEST_RAPORU.csv`.
- The workflow uploads the working/candidate playlist and diagnostics as artifacts for 30 days; it does not define a git push. This is a consequential generated artifact and local protected-file overwrite, not a read-only test. It also tests external live streams, so results are time-dependent and cannot be reproduced from code inspection alone.
- High-priority migration defect: replacement must treat the existing playlist as immutable input and write generated M3U/failed list/report to a dedicated isolated output directory; the final playlist must not be accepted or published without separate evidence and user/device approval. Add a regression test that hashes protected inputs before and after execution, including exceptions/timeouts, and proves outputs are isolated. **Status: reviewed-source; behavioral parity not accepted.**

## 3. `.github/workflows/k1-protected-write-tests.yml`

- Workflow blob SHA: `52bad78597f6df07b530167a21a6256d6107bd6b`.
- Triggers on relevant K1/security files and manual dispatch; `contents: read`; checkout credentials disabled; 35-minute timeout.
- It snapshots protected tracked files, runs the 26-rule/92-workflow acceptance suite, uploads acceptance diagnostics, runs a read-only workflow risk inventory and static workflow audit, then checks protected-file integrity even on earlier failure. The integrity-diff step is `continue-on-error: true`, but a later `if: always() && steps.protected_integrity.outcome == 'failure'` step exits nonzero, so the gate is designed to fail closed.
- Direct scripts and frozen SHAs: `scripts/acceptance_26_92.py` `1e8dedc80e79d898b645e6506e325f2d75469526`; `scripts/k1_protected_integrity.py` `8a73368752bcb0c3b39febfa74c2c42d70ae16d3`; `scripts/k1_workflow_risk_inventory.py` `46de76cb910ed4cfa125e320b9f2dc86fa3d7831`; `scripts/audit_workflow_security.py` `97fdd41816a3cfac671cd9e9e9d6f5d33858ec68`.
- `acceptance_26_92.py` runs named offline suites and records independent runtime/legacy parity counters; it correctly warns that unit tests are not production/device/parity proof. However its normal exit code is based on regression suites and audit errors, not `acceptance_complete`; the separate `--require-full-acceptance` flag is needed to fail the process when full acceptance is required. This distinction must remain explicit in workflow labels and downstream decisions.
- Integrity snapshots are a before/after workspace guard, not a proof against transient mutations that are restored before the final check. The static risk inventory is text/regex evidence, not execution proof. **Status: reviewed-source, not accepted.**

## Batch summary

- Three more workflows and their directly invoked scripts reviewed against frozen blob SHAs.
- Cumulative static source review: **27/92**; **65/92** remain, subject to canonical exclusions. (99 YAML inventory includes workflows outside the 92-item legacy parity acceptance scope.)
- Behavioral parity accepted this batch: **0/3**; total remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- Highest-priority actionable defect: two legacy jobs modify `CALISANLAR.m3u` in the runner workspace despite quality/read-only labels. They do not define a git push, but input/output separation is required before migration parity can be claimed.
- Next: inspect the replacement workflow/script path in `Madsc55/Madsc55-Tv`; add isolated regression tests for protected-input immutability and output path separation without modifying or executing the legacy repository. Do not dispatch live probes or accept playlist/device changes without authorization and independent evidence.
