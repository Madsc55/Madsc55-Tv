# Legacy workflow behavior review — Batch 15
Date: 2026-10-23 (Europe/Stockholm)
Scope: read-only review of three backup-classification workflows and direct scripts in frozen legacy tree `ca374df3b9585c0d76a078db9536150ebbc260f7`, repository `Madsc55/madsc-tv`. No workflow dispatch, legacy write, live probe, or production/device change was performed.

## 1. `.github/workflows/madsc-ibo-354-classify.yml`
- Workflow blob SHA: `165bb7fc69775be790beab972dc68e92cf40c2c3`; direct script `scripts/archive_backups_354_classified.py`, blob SHA `65f5faf61cc69d5babecacdca1db9faa84881210`.
- Push-triggered on workflow-file changes, main-branch-gated, `contents: write`, checkout credentials persist by default. Script requires exactly 354 entries in the `YEDEKLER` group, retains positions 1–2, archives positions 3–334 as user-reported nonworking Turkish entries and 335–354 as foreign, then rewrites `CALISANLAR.m3u` and creates two archive M3Us plus a JSON report.
- The report labels the 332 Turkish channels `KULLANICI_BILDIRIMI_TEST_EDILMEDI`, correctly saying the claim was not tested; this is not technical or IBO playback evidence. Nevertheless, the workflow stages `CALISANLAR.m3u` and invokes the protected-write gate, whose frozen policy rejects every `.m3u` path. Thus the intended commit/push is statically expected to be denied after the runner workspace was modified. The production repository is not shown to have changed.
- Migration requirement: keep classification/archive previews isolated from the protected playlist and require explicit independent approval before any replacement workflow may propose a main-list change.

## 2. `.github/workflows/madsc-ibo-364-355-364.yml`
- Workflow blob SHA: `7dff039f081b93c0efab2ced1ab8e873f021e496`; direct script `scripts/archive_backups_355_364.py`, blob SHA `1f01c548d872dfcce086018e58c996c5a3d2a2f2`.
- Push-triggered on workflow-file changes, main-branch-gated, `contents: write`; no explicit checkout credential disable. The script requires 364 backup entries, removes positions 355–364 into an archive, updates the count to 354, rewrites `CALISANLAR.m3u`, and writes a JSON report. It marks classification as user-identified foreign but explicitly leaves playback `BELIRTILMEDI`.
- It verifies `YABANCI_KANALLAR.m3u` was unchanged, but that does not protect `CALISANLAR.m3u`. The subsequent protected-write gate rejects staged M3U changes, so the publish step is expected to fail closed; there is no report artifact step to preserve the runner-generated evidence if the gate fails.
- Migration requirement: generate candidate archive/report in a separate output folder, do not rewrite the source playlist, upload diagnostics with `if: always()`, and distinguish user classification from confirmed identity/playback.

## 3. `.github/workflows/madsc-ibo-398-16-49.yml`
- Workflow blob SHA: `7b3dd19eb1fc1651e4f921e5b4f1c79fa0c91dc1`; direct script `scripts/archive_backups_16_49.py`, blob SHA `411a7b3f9665cd7882cdd2b37d614c16d7aabd8a`.
- Push-triggered on workflow-file changes, main-branch-gated, `contents: write`. It requires 398 backup entries, archives positions 16–49 as user-classified foreign, rewrites `CALISANLAR.m3u` to 364 entries and writes archive/report files. The report says `YABANCI_KULLANICI_TESPITI` and playback `BELIRTILMEDI`.
- As with the 355–364 workflow, the main playlist mutation conflicts with the protected-write gate and is expected to be blocked before push. The workflow lacks explicit checkout credential disable and an always-run artifact upload, so failed runs may leave no easy-to-download diagnostic evidence.
- Migration requirement: isolated draft-only archive and report; no automatic main-list rewrite; explicit approval plus separate source/identity/playback evidence before any eventual promotion.

## Batch summary
- Three more frozen workflow/script pairs reviewed; the common defect is a mismatch between legacy scripts that rewrite `CALISANLAR.m3u` and the fail-closed protected-write gate that blocks all M3U changes.
- Cumulative static source review advances from 42/92 to **45/92**; **47/92** remain subject to canonical exclusions and deduplication.
- Behavioral parity accepted this batch: **0/3**; overall remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- No legacy repo files, protected playlists, EPG, favorites, logos, backups or real devices were changed. Static review does not prove whether any prior run reached a remote push; current source policy indicates these staged M3U mutations should be denied.