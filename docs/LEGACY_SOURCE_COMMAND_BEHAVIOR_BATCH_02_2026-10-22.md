# Legacy workflow source commands — batch 02

Source: `Madsc55/madsc-tv` branch `madsc/bes-sistem-toplu-birlestirme`. 32 YAML sources directly inspected; names are source workflow identities. Descriptions are YAML command-level observations, not complete script-level behavioral parity.

| Workflow | Source behavior / risk |
|---|---|
| `madsc-01-guvenlik.yml` | K1 protected integrity snapshot/check, 26-rule evidence, unit suites |
| `madsc-02-kesif.yml` | K2 history restore, archive before/after, discovery, candidate EPG/logo join, wide scan |
| `madsc-03-kanal-test.yml` | K3 logo/EPG, IBO trial, ffmpeg media, scoring, main playlist health |
| `madsc-04-arsiv-yedek.yml` | K4 archive/backup and isolated restore tests |
| `madsc-05-genel-bakim.yml` | K5 shared controls, 92-workflow audit, Actions evidence, cutover readiness |
| `madsc-11599-yedek-geri-yukle.yml` | 11599 backup diagnostic |
| `madsc-ana-liste-saglik.yml` | Protected playlist health test, ffmpeg |
| `madsc-arsiv-yedek-aktarim.yml` | Archive transfer orchestration; no direct Python command found |
| `madsc-aylik-merkezi-denetim.yml` | Central write gate, inventory, IBO, backup, source and test audits |
| `madsc-birlesik-kesif.yml` | Discovery, archive before/after, EPG/logo, report, git push RISK |
| `madsc-cuma-ana-liste-denetimi.yml` | Friday playlist audit and warning summary |
| `madsc-documentation-check.yml` | Documentation checks; no direct Python command found |
| `madsc-genis-kaynak-kontrol.yml` | Wide source scan, report, git push RISK |
| `madsc-hizli-on-kontrol.yml` | Five-system cutover preflight and 92 audit |
| `madsc-ibo-3-5281.yml` | IBO case orchestration; no direct Python command found |
| `madsc-ibo-354-classify.yml` | IBO backup classification, protected CALISANLAR.m3u write and push RISK |
| `madsc-ibo-364-355-364.yml` | IBO foreign backup archive, protected write and push RISK |
| `madsc-ibo-398-16-49.yml` | IBO foreign backup archive, protected write and push RISK |
| `madsc-ibo-530-archive.yml` | IBO backup archive 399 onward, protected write and push RISK |
| `madsc-ibo-6115-second.yml` | IBO second session archive, protected write and push RISK |
| `madsc-ibo-ilk-239.yml` | IBO first 239 decisions, protected write and push RISK |
| `madsc-ibo-kararlar-grup1.yml` | IBO group1 decisions, protected write and push RISK |
| `madsc-ibo-second-voice.yml` | IBO voice decisions, protected write and push RISK |
| `madsc-otomatik-devam.yml` | Auto-continuation orchestration; no direct Python command found |
| `madsc-rule24-test.yml` | Rule24 failure gate unit test |
| `madsc-sistem-saglik-denetimi.yml` | System health audit and evidence |
| `madsc-son-kontrol-kurtarma-teshis.yml` | Final validation diagnostic |
| `madsc-son-kontrol.yml` | Final validation and report git push RISK |
| `madsc-toplu-butunluk.yml` | Bulk integrity gate |
| `madsc-tum-sistem-yedek.yml` | Repository settings inventory, full system backup |
| `madsc-turk-kanal-geri-sec.yml` | Restore Turkish backup channels, protected write and push RISK |
| `madsc-uc-asama.yml` | Three-stage verification, candidate report git push RISK |

**Protection gate:** Any workflow writing `CALISANLAR.m3u`, backups, archives, or pushing commits is a blocked side-effect until explicit permission and independently verified equivalence. Do not auto-dispatch old workflows. Excluded central workflows are source references, not part of the 92 acceptance scope. Verified parity remains 0/92.
