# Legacy workflow source commands — final batch 03

Source: `Madsc55/madsc-tv` branch `madsc/bes-sistem-toplu-birlestirme`. Last 43 YAML sources directly inspected. These are YAML command-level observations, **not** full script-level behavior or parity proof.

| Workflow | Observed command-level responsibility |
|---|---|
| `madsc-yedek-turk-ayir.yml` | Keep Turkish backups; writes CALISANLAR.m3u, git push — BLOCKED |
| `madsc-yedekler-aktarim-test.yml` | Backup transfer unit test |
| `madsc-yedekler-sayi-duzelt.yml` | Sync YEDEKLER count; writes CALISANLAR.m3u, git push — BLOCKED |
| `oncelikli-kanal-dogrulama.yml` | ffprobe priority candidate verification |
| `onikinci-hata-siniflandirma-test.yml` | Inline Python failure classification test |
| `publish-iptv-png-logos.yml` | Generate PNG logos, git push — BLOCKED |
| `sekizinci-tekrar-raporu-test.yml` | Candidate scan/repeat report syntax and test |
| `sozcu-akit-ozel-test.yml` | Dedicated Sözcü/Akit ffprobe verification |
| `test-13-kaynak-degisiklik.yml` | Inline source-change regression test |
| `test-14-istikrar.yml` | Inline stability regression test |
| `test-15-logo-epg.yml` | Protected playlist logo/EPG audit |
| `test-16-workflow-safety.yml` | Workflow safety regression |
| `test-17-candidate-summary.yml` | Candidate summary regression |
| `test-18-change-simulation.yml` | Change simulation regression |
| `test-19-integration.yml` | Integration inline regression |
| `test-20-full-integration.yml` | Full Python unittest discovery |
| `test-21-functional-e2e.yml` | Functional E2E inline regression |
| `test-22-real-playlist.yml` | Real playlist inline test; protected source read |
| `test-23-live-stream.yml` | Live stream inline test |
| `test-24-system-audit.yml` | PyYAML and full unittest system audit |
| `test-25-full-project-readonly.yml` | Read-only project audit and full unittest |
| `test-26-automation-safety.yml` | PyYAML automation safety checks |
| `test-27-pipeline-contract.yml` | Pipeline contract inline checks |
| `test-28-approval-gate.yml` | Approval gate inline checks |
| `test-29-write-path-audit.yml` | Write-path PyYAML audit |
| `test-30-write-risk-report.yml` | Write-risk report |
| `test-31-protected-write-gate.yml` | Protected write gate |
| `test-32-unapproved-write-regression.yml` | Unapproved backup git push regression |
| `test-33-all-write-paths.yml` | All write paths audit |
| `test-34-protected-write-regression.yml` | Protected write regression |
| `test-35-remaining-write-gate.yml` | Remaining write gate and artifact requirement |
| `test-36-system-integration-audit.yml` | System integration audit |
| `test-37-indirect-write-audit.yml` | Indirect write audit |
| `test-38-audit-selftest.yml` | Audit self-test and unsafe push detection |
| `test-39-protected-playlist.yml` | Protected playlist audit |
| `test-kanal-adaylari.yml` | Candidate test report |
| `toplu-sistem-kontrol.yml` | Bulk system audit, all unit tests and git push warnings |
| `vod-guncelle.yml` | VOD episode metadata update and git push — BLOCKED |
| `yedek-geri-yukleme-tatbikat.yml` | Restore dry run |
| `yedekler-yeniler-medya-kontrol.yml` | Backup/new candidates ffprobe |
| `yeni-aday-on-test.yml` | New candidate pretest ffmpeg |
| `yeni-kanal-arama-2026.yml` | New channel scan ffprobe |
| `yeniler-guvenli-arama.yml` | Source discovery → artifact download → scan → report |

## Cumulative scope

- First batch: 23 YAML command chains (includes one repeated row in batch 02).
- Second batch: 32 YAML command chains (contains 5 central workflows excluded from the 92 behavior scope).
- Final batch: 43 YAML command chains.
- **99 unique source YAMLs read across batches**, with `kaynak-puanlama-kontrol.yml` overlapping batches 01 and 02. All 99 pinned in `docs/LEGACY_99_PINNED_WORKFLOW_SCOPE_2026-10-22.md`.
- Real behavior parity independently accepted: **0/92**.

All source workflow writes to protected playlists, backups, favorites, archives, logo data or GitHub pushes remain **blocked** absent user permission. No workflow dispatch or protected file mutation was performed.
