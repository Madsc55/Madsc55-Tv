# Legacy workflow behavioral review — batch 03 (2026-10-23)

Frozen legacy source: `Madsc55/madsc-tv`, commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Reviewed exact workflow YAMLs read-only. Static review is not execution parity.

## 1. `.github/workflows/felaket-kurtarma-tatbikati.yml`

Observed contract:
- Manual trigger and push changes to this workflow or `scripts/disaster_recovery_dry_run.py`.
- `contents: read`; checkout with `persist-credentials: false`, `fetch-depth: 1`; 8-minute timeout.
- Runs a dry-run disaster recovery script against protected lists in a temporary environment.
- Always uploads `DISASTER-RECOVERY-REPORT.json` under artifact name `MADSC-FELAKET-KURTARMA-DOGRULAMA`; missing report is a hard upload error.
- No production write permission is granted by the workflow.

Potential replacement mapping: `madsc/restore_drill.py` uses temporary backup/restore sandboxes and explicitly reports that external storage and production restoration are not proven. It is conceptually related, but the legacy script's exact file allowlist, report schema, path handling, restore semantics and exit behavior need differential comparison.

Acceptance evidence required: same fixture inputs; byte-for-byte source hash preservation; restored output hashes; report schema; missing report hard failure; unsafe path/symlink rejection; timeouts; no production path touched. Status: reviewed-source; not accepted.

## 2. `.github/workflows/madsc-11599-yedek-geri-yukle.yml`

Observed contract:
- Push trigger when this workflow file changes; no manual dispatch trigger.
- `contents: write`; concurrency group `madsc-11599-yedek-geri-yukle`, `cancel-in-progress: false`; 15-minute timeout.
- Fetches origin/main and hard-resets the checked-out workspace to it before restoration.
- Runs `scripts/restore_all_11599_backups.py`.
- Requires `YABANCI_KANALLAR.m3u` and `madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u` to have no diff after restore.
- Stages only `CALISANLAR.m3u` and `madsc_kesif/yedek_11599_geri_yukleme_raporu.json`; if no staged diff, exits successfully; otherwise commits and pushes to main.

Risk boundary: this is a real production write workflow with write permissions and hard reset. It must not be automatically invoked as part of a read-only parity test. Any replacement must have an explicit approval boundary and prove the exact write allowlist and protected-file invariants before a controlled write can be considered.

Potential replacement mapping: `madsc/backup.py` and `madsc/restore_drill.py` explicitly operate on new sandbox paths and do not perform this main-branch restore/commit. They are safety analogues, not behaviorally equivalent replacements.

Acceptance evidence required: frozen backup manifest and provenance; exact 11599-file selection and precedence; restore diff against reference output; protected files unchanged; allowlist-only staging; no-op idempotency; concurrent run behavior; failed restore produces no commit; explicit human approval for any production write. Status: reviewed-source; not accepted; production execution not attempted.

## 3. `.github/workflows/ibo-epg-kimlik-denetimi.yml`

Observed contract:
- Manual and push triggers for the workflow and `scripts/ibo_epg_kimlik_denetimi.py`.
- `contents: read`; 10-minute timeout.
- Compiles the Python script, validates `CALISANLAR.m3u` against `epg/ibo-test-epg.xml`, writing the report only to `$RUNNER_TEMP/ibo_epg_identity_audit.json`.
- Requires positive `playlist_entries`, `xmltv_channels`, `xmltv_programmes`, and `matching_entries_with_programmes`.
- Prints scalar report fields and uploads the report for 14 days as `ibo-epg-identity-audit`.

Potential replacement mapping: `madsc/epg.py` checks M3U tvg-id values against XMLTV channel IDs and orphaned programme IDs; `madsc/epg_inventory.py` checks duplicate/empty IDs, matched playlist IDs, orphaned programmes and missing times. These are related checks but do not prove the exact legacy report schema or identical matching rules.

Acceptance evidence required: compare report keys/counts on identical playlist/XMLTV fixtures; missing tvg-id, duplicate channel IDs, orphaned programmes, zero-programme, malformed XML, UTF-8 BOM and case/whitespace behavior; ensure output remains outside the repository; verify artifact retention/presence. Status: reviewed-source; not accepted.

## Batch summary
- Source YAMLs reviewed in this batch: 3.
- Cumulative documented source review in batches 01–03: 9 workflow YAMLs.
- Accepted behavioral parity in batch 03: 0/3; overall accepted legacy workflow parity remains 0/92.
- No workflow was dispatched; no production restore, commit, playlist, EPG, device data, or backup was changed.
