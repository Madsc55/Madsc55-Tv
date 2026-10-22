# Legacy workflow behavior review — Batch 11
Date: 2026-10-23 (Europe/Stockholm)
Scope: read-only source review of three previously unreviewed workflow files in `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`, frozen at tree `ca374df3b9585c0d76a078db9536150ebbc260f7`. No workflow dispatch, live probe, legacy-repository write, or production/device change was performed.

## 1. `.github/workflows/madsc-01-guvenlik.yml`
- Workflow blob SHA: `ae91b6c47745fe46659105f96cd28e6aca9d44d9`.
- Direct audit scripts and blob SHAs: `scripts/k1_24_rule_evidence.py` `bd8058b4ebe4aa8136f0bc9ac44a32ae0e73e054`; `scripts/central_protected_write_gate.py` `e5663a6e57bb3174ff95e3aeac5acc2f85dfe38e`; `scripts/central_consolidation_audit.py` `3dd9258bdc8db64f13a9df8daa51d2e685f3a820`; `scripts/five_category_92_workflow_audit.py` `9a35ecd797e5c1c595d6796cfffba6cd8a289853`.
- Manual dispatch and reusable workflow-call triggers; `contents: read`, `actions: read`; checkout has `persist-credentials: false`; 60-minute timeout. It snapshots protected files, runs reports, explicitly requires 26/26 security rules to have runtime enforcement verified, executes regressions even after earlier failures, then verifies protected-file hashes and snapshot integrity in an always-run fail-closed gate.
- Static contract: the 26-rule evidence script explicitly distinguishes inventory completeness from runtime enforcement, which is appropriate. Its runtime-evidence requirement intentionally blocks acceptance while any rules lack independent evidence. Snapshot/hash checks detect persistent mutations, but by themselves cannot prove no transient write was made and reverted during a job.
- Status: source-reviewed only; no runtime security acceptance claimed.

## 2. `.github/workflows/madsc-02-kesif.yml`
- Workflow blob SHA: `f9970a874258c1cbd1c59f73fa427136ff2d53d4`.
- Direct scripts and blob SHAs: `scripts/discovery_history_restore.py` `b56a17a8b4c9b9238cefba5984f4f54b287c9c93`; `scripts/discovery_archive.py` `22274f17f34a501f691bedb5e3667bb1fe00bf32`; `madsc_akilli_kesif.py` `d8673dbd763c7411878bd27fa432b455c15c9b31`; `scripts/candidate_epg_logo_join.py` `d62a513375c279bbd2682386e15decf658040c69`; `scripts/four_stage_discovery_report.py` `c8d0ece165ee5043a034bf276658b2be0eb79917`; `scripts/wide_source_scan.py` `2d66fd296314c9507cd9f0e54b491f979cda4904`.
- Two scheduled runs are configured at 05:17/17:17 UTC plus manual dispatch and reusable workflow call. The job is read-only at GitHub permission level and disables checkout credentials; it downloads prior run artifacts/history, fetches multiple external playlists, probes candidate URLs, runs ffprobe, and writes a large set of discovery/history/logo/quality reports under its report workspace. Weekly/monthly wide scans are separately controlled by an input.
- High-risk parity details: source availability and media results are inherently time-dependent; a passing scan cannot establish channel identity, licensing, stable playback, or IBO device acceptance. Persistent history restore/merge logic must reject malformed, stale, or untrusted artifact provenance rather than letting a report overwrite newer observations. Reports and candidate playlists must remain isolated and must never be promoted into `CALISANLAR.m3u` without separate approval.
- Static protection includes before/after snapshots for `CALISANLAR.m3u`, `AGENTS.md`, `GUVENLIK_KURALLARI.md` and K1 integrity manifest. These guards protect those paths at end of job, but do not prove all intermediate side effects are absent. Discovery/archive code writes report/history files; those are expected outputs, not proof of source parity.
- Status: source-reviewed only; no source independence, production behavior, or discovery parity accepted.

## 3. `.github/workflows/madsc-03-kanal-test.yml`
- Workflow blob SHA: `228d53500e99bc9953ab6d535b7809523a1854f0`.
- Direct scripts and blob SHAs: `scripts/ana_liste_saglik.py` `852f726d6da74166283fdc94a49c1c2f5e347c3c`; `scripts/export_ibo_two_stage_trial.py` `64a0ef2bbbe4f9b77523a15a877b6ca331a0f91f`; `tools/logo_epg_audit.py` `b8ac681c42b5db1f29023f93468900269edd2334`; `scripts/category_candidate_media.py` `0686bb49be9cba0dff20785ded88a4b8e0036db9`; `scripts/category_candidate_scoring.py` `2a4bba5009fdd442f5e15b49aeee12e8456d30a8`.
- Scheduled daily, manual, reusable call, and path-filtered pushes on the legacy feature branch. Explicit `contents: read` and `actions: read`, checkout credentials disabled, protected playlist/rules hashes captured and checked. It probes a rotating subset of existing playlist URLs, emits separate health and IBO trial reports, reads EPG/logo metadata, downloads prior run artifacts for scoring, and stores generated reports as artifacts.
- The IBO trial exporter reads the production playlist only to exclude already-present URLs, and writes a separate candidate M3U plus JSON evidence to its specified output path. It labels candidates as trial material, not an automatic production update. This must remain isolated; three technical passes do not by themselves prove broadcast identity, rights, or real IBO playback.
- Several steps use `continue-on-error: true`; a final explicit gate checks reports, media, scoring, EPG/logo, IBO, coverage, and regression outcomes. That final gate is essential because intermediate step status alone is not acceptance. Live HTTP/ffprobe results are non-deterministic; unit tests need fixed offline fixtures and provenance checks.
- Status: source-reviewed only; no live playback, IBO device, or behavioral parity accepted.

## Batch summary
- Three additional unique legacy workflows reviewed against frozen source blob SHAs.
- The repository's documented cumulative static-review count advances from 30/92 to **33/92**; **59/92** remain subject to canonical exclusions and deduplication. (The 99-file YAML tree is not identical to the 92-item legacy behavioral-parity scope.)
- Behavioral parity accepted this batch: **0/3**; overall remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- Key migration requirements: retain fail-closed gates; distinguish static report success from runtime enforcement; pin artifact/source provenance for history restoration; keep candidate M3U and logo/EPG reports isolated; never infer IBO playback or source licensing from network probe success.
- This document is evidence of source review only. Do not modify the legacy repository or run live discovery as part of static review.
