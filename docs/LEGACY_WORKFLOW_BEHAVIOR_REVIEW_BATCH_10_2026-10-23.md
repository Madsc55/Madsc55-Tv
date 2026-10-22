# Legacy workflow behavior review — Batch 10
Date: 2026-10-23 (Europe/Stockholm)
Scope: read-only review of three frozen workflow sources in `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`. No legacy repository writes, workflow dispatch, live probes, or production changes were performed.

## 1. `.github/workflows/vod-guncelle.yml`
- Workflow blob SHA: `78c3b8aa8e27b9f25e439337e2e94be9468b6f3b`.
- Direct script: `scripts/vod_guncelle.py`, blob SHA `94f83bb6a04d20a90dcb21fd117d8635c6e9dbac`.
- Trigger: daily cron `17 7 * * *` (GitHub Actions cron is UTC) plus manual dispatch; job runs only on `refs/heads/main`; `contents: write`; shared publish concurrency group with cancellation disabled. No explicit job timeout or network retry/backoff is defined.
- Script requests TVMaze's Turkish episode schedule for 15 dates (today -7 through +7), each with a 20-second request timeout. It catches each request/parse exception, prints a skipped-day message, and continues. Afterward it unconditionally replaces `vod/guncel-bolumler.json` with whatever records were gathered, even when one or more dates failed. The workflow stages only that JSON path and may commit/rebase/push it.
- Risk/required parity: a partial API outage can publish a silently incomplete date window. The output replacement is not atomic, no expected-date coverage threshold is enforced, and there is no explicit output schema/duplicate validation before the write. An equivalent safe implementation should stage in an isolated file, validate complete/acceptable coverage, and only publish on an explicit pass. No playlist write was observed in the script; its docstring explicitly says it must not change `CALISANLAR.m3u`.
- Status: source-reviewed only; no runtime parity acceptance.

## 2. `.github/workflows/yedek-geri-yukleme-tatbikat.yml`
- Workflow blob SHA: `08a38be283550147e0e267f72fcc1291bfc9f88c`.
- Direct script: `scripts/restore_dry_run.py`, blob SHA `5985b9fc48e41aaaf4f9bb5166015fb17f3cf03c`.
- Triggers: manual dispatch and pushes touching the workflow or script. `contents: read`, checkout credentials disabled, 8-minute timeout; uploads `RESTORE-DRY-RUN-REPORT.json` with `if: always()` and `if-no-files-found: error`.
- Script reads two fixed local backup fixtures, parses playlist structure, copies each byte-for-byte to a temporary directory, compares SHA-256 and parsed rows, and includes a malformed-playlist negative test. It snapshots hashes of `CALISANLAR.m3u` and `YENILER.m3u`, then checks they remained unchanged. The report is written to the runner workspace, not the temporary restore directory.
- Limits: this is a local sandbox restore rehearsal, not an independent external-backup restore. If an input is missing or parsing/restoration fails before the final checks, the script can exit before writing a report; the always-run upload then fails because the artifact is required. The protected-input check is not in a `finally` path, so failure diagnostics do not always contain the final integrity result.
- Status: source-reviewed only; no external restore or behavioral parity accepted.

## 3. `.github/workflows/publish-iptv-png-logos.yml`
- Workflow blob SHA: `7b8fa621b2cfaf151e26855d92a6ccbc326d6ed3`.
- Trigger: manual dispatch and pushes to `logos/duzeltilmis-*.svg`; shared publish concurrency group with cancellation disabled; main-branch-only job; `contents: write`; checkout credentials persist by default.
- It installs CairoSVG, converts matching SVGs into PNGs in the same `logos/` directory, stages generated PNGs, then invokes `tools/protected_write_gate.py --base HEAD` before committing/pushing. The gate blob is `11b257e1e5862de49486f6982057c2fa75530812`.
- Deterministic contract conflict: `blocked_paths()` rejects every path under the `logos/` prefix, while this workflow's generated outputs are under `logos/`. Therefore, whenever generated PNG changes are staged, the gate is expected to deny the workflow's intended publication. This is not evidence that the workflow succeeds; it is a static contradiction between publisher scope and gate policy. The intended safe fix must be decided in the replacement design, not by weakening the legacy gate or modifying the legacy repository.
- Status: source-reviewed only; no logo conversion/publication was run.

## Batch summary
- Three distinct frozen workflow sources and their direct scripts/guard were inspected by exact blob SHA.
- Cumulative static source review: **30/92**; **62/92** remain, subject to canonical exclusions and deduplication.
- Behavioral parity accepted this batch: **0/3**; overall behavioral parity remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- Follow-up priorities: (1) make VOD metadata publication reject incomplete date coverage and write atomically; (2) guarantee restore integrity diagnostics on failure while keeping the restore isolated; (3) reconcile logo output scope with the replacement write policy without broadening protected-path exceptions.
- These findings are evidence for migration design only. No legacy repo files were modified; no workflow was dispatched; no live IPTV/EPG, device, protected playlist, favorites, logo, backup, or production archive was changed.
