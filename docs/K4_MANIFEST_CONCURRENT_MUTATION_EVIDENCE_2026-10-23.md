# K4 — manifest sırasında kaynak değişikliği koruması (2026-10-23)

Repository: `Madsc55/Madsc55-Tv`, branch `main`.
GitHub HEAD before evidence record: `f1268a6914446267622eb1cc955432dcea039a47`.

## Fix and regression
- Code commit `5dfb571a946e00f474c8b480814bbd4b4b555704` in `madsc/backup.py`: `snapshot_manifest` compares descriptor identity, size, `st_mtime_ns` and `st_ctime_ns` before and after hashing, and checks bytes read against final file size. A changed source fails closed with `ValueError` instead of emitting a possibly mixed-time manifest.
- Test commit `9299b18d666720c6f6ad827e9feffd30c2686974` in `tests/test_backup_manifest_hardening.py`: a deterministic patched `os.fstat` path changes the file timestamp between the initial and final descriptor checks. It expects rejection.
- GitHub Actions [39868739848](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39868739848) completed **success** for exact test commit `9299b18d666720c6f6ad827e9feffd30c2686974`. Its offline job log reports `tests_discovered=1020`, `tests_passed=true`, `five_stage_fixture_gate_passed=true`, and `all_offline_gates_passed=true`. This proves the offline suite only, not production readiness.
- Separately, source-only commit `5dfb571a...` passed in run [39868713283](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39868713283). Newer parallel K1–K5 commits after `9299b18d...` need their own matching CI evidence.

## Scope and remaining acceptance
- This is a TOCTOU detection hardening, not an atomic filesystem snapshot or a proof against adversarial mutation that leaves all checked metadata identical.
- No external storage, real restore, IPTV/EPG, device, protected playlist, production archive, or legacy repository was accessed or modified by this change.
- K4-15 external write receipt, K4-16 genuinely isolated external restore, K4-17 archive/VOD equivalence, K4-18 first/fifteenth scheduler evidence are not accepted.
- Acceptance counters remain `0/92` legacy behavioral parity, `0/26` independent runtime security, and `0/22` independent main-task acceptance.

Next: independent offsite provider write receipt and isolated restore evidence under explicit authorization; do not promote sandbox fixtures to production acceptance.

## Additional K4 exact-inventory sandbox restore gate
- Code commit `653b531aba7f8565d24c164421f3c3c1cb332602` updates `madsc/k4_restore_gate.py` to withhold sandbox acceptance when any source/backup/restore tree contains an unexpected file, directory, or symlink. Earlier comparison checked only the caller's named subset; an extra file could be left unnoticed. The lower-level named-file comparison API retains its existing subset semantics; the stricter rule is applied at the K4 acceptance gate.
- Test commit `205ad1bf6f094a36600a0ad5872f228fc74fe850` adds regressions for extra restored files, unexpected empty directories, and a symlink in the original tree.
- GitHub Actions [39869009399](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39869009399) completed **success** on the exact test commit. Logs: `tests_discovered=1027`, `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`, `production_ready=false`.
- This is exact-inventory validation of isolated fixture trees, **not** an independently sourced offsite restore. K4 external acceptance remains open, as do the `0/92`, `0/26`, and `0/22` acceptance counters.
