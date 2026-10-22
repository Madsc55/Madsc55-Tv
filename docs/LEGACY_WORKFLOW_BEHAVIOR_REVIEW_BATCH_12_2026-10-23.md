# Legacy workflow behavior review — Batch 12
Date: 2026-10-23 (Europe/Stockholm)
Scope: read-only review of three more legacy workflows in `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`, frozen tree `ca374df3b9585c0d76a078db9536150ebbc260f7`. No legacy-repository writes, workflow dispatch, live probes, or production/device changes were performed.

## 1. `.github/workflows/madsc-04-arsiv-yedek.yml`
- Workflow blob SHA: `7b4d62f33c6438236f418f8e60f779a22d05a9d3`.
- Direct scripts/blob SHAs: `scripts/central_isolated_git_restore.py` `c64b177f5405208a2a610eeaff41c4d6e0260e00`; `scripts/central_backup_evidence.py` `be445a569f79241612cba082824469d425c90c28`; `scripts/central_archive_consistency.py` `eaa987998d3a79a2f27edbbad7bfe66a5a23f5cb`; `scripts/disaster_recovery_dry_run.py` `a9ba4b5d21e5a845ac2b6ed1c2ec1c10f3a2dad4`.
- Manual/reusable triggers, read-only GitHub permissions, checkout credentials disabled, 60-minute timeout. It compares current protected files to Git HEAD blobs in a temporary directory, runs a temporary corruption-and-restore simulation for two tracked playlists, generates backup/protected-file evidence, and requires an explicit report check plus regressions. The final gate fails closed on report, acceptance, or regression failure.
- Important limit: this validates the checked-out Git commit and an in-run temporary restore, not an independent offsite backup or historical restore. The evidence report correctly keeps `off_github_copy` unverified and `historical_recovery_verified=false`. Existing file hash snapshots establish current fingerprints, not prior-state immutability. A missing input can make the dry-run fail before its final report is created, so diagnostics still depend on the workflow's always-run artifact step and should never be interpreted as restore acceptance when absent.
- Status: source-reviewed only; no external backup/restore acceptance.

## 2. `.github/workflows/madsc-05-genel-bakim.yml`
- Workflow blob SHA: `32560f27ff29830f16f41f7a1ed0b8476f0b362f`.
- Direct evidence scripts/blob SHAs: `scripts/category_evidence_collect.py` `c8006d31f21ee5dd01da2ca274352569a613e671`; `scripts/central_actions_evidence.py` `1f7366ae7d11cdf10ec0a4a0ccc425161ee0046f`.
- Daily schedule, manual dispatch, and path-filtered pushes to the legacy integration branch. It sequentially calls the four category workflows, requires each category result to succeed, checks same-run artifact provenance/commit identity, performs a large set of independent reports, validates the 92-row migration matrix, and runs a final fail-closed summary/gate. GitHub permissions are read-only; checkout credentials are disabled.
- Strong design control: `category_evidence_collect.py` verifies the parent run, head SHA/branch/repository, expected workflow path/event, exactly one completed successful category job per K1–K4, and exactly one unexpired artifact from that same run/commit before importing named JSON reports. It explicitly leaves `overall_run_verified=false`, migration approval false, and IBO approval false at collection time.
- Limits: this is strict artifact/provenance validation, not proof that a live channel works or that external backup, source licensing, broadcast identity, or device playback passed. The parent workflow intentionally fails when any category or audit is failed/skipped. The action-evidence sampler reads only the last 100 runs and attempts job details for at most 20 failures, so older/unlisted runs remain unknown; its report must not be presented as exhaustive history.
- Status: source-reviewed only; no end-to-end five-system acceptance.

## 3. `.github/workflows/madsc-ana-liste-saglik.yml`
- Workflow blob SHA: `6ba3cc60b74f26d3e7dcfecdf84d0cd2ce85baf7`.
- Direct script/test blob SHAs: `scripts/ana_liste_saglik.py` `852f726d6da74166283fdc94a49c1c2f5e347c3c`; `test_ana_liste_saglik.py` `4c610d1b2bf20e8580136ab3975f29929e8b87a8`.
- Manual and twice-monthly schedule, `contents: read`, checkout credentials disabled, 35-minute timeout. It hashes the protected playlist and other source files before running offline unit tests and a 50-channel ffprobe batch; then it verifies those hashes and uploads a report. The script writes JSON/Markdown only to a report directory and explicitly records that technical errors do not authorize channel deletion/change or imply IBO acceptance.
- Defect in the frozen legacy test fixture: `test_parallel_probe_results_keep_playlist_order` constructs its M3U with double-escaped newline sequences (`\\n` in the Python source literal), unlike the other fixtures' real newline characters. That fixture therefore does not reliably model a valid multi-row M3U; its assertion for 12 parsed rows is expected to fail or the test will exercise malformed input instead of parser ordering. Fix in the replacement repository only by using actual newline characters and add an assertion that 12 source rows were parsed before checking parallel order. Do not change this legacy repository.
- The rotating batch covers only 50 entries per run by default; it must not be described as whole-list validation unless the report says tested count equals total. ffprobe network results are transient and do not verify long-duration playback, identity, licensing, or IBO device behavior.
- Status: source-reviewed only; no live probe or playlist modification performed.

## Batch summary
- Three more workflows reviewed against exact frozen blob SHAs. The new actionable migration issue is a malformed newline fixture in the legacy channel-health regression test.
- Cumulative static source-review ledger advances from 33/92 to **36/92**; **56/92** remain, subject to canonical exclusions/deduplication. (The 99-YAML tree and 92-workflow parity scope are different inventories.)
- Behavioral parity accepted this batch: **0/3**; total remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- Keep production playlists, EPG, favorites, logos, external backups and real devices untouched. Review evidence and isolated unit tests do not grant migration or production approval.
