# İlk davranışsal eşleme — 8 kaynak workflow (19 Ekim 2026)

Kaynak salt-okunur dal: `Madsc55/madsc-tv@madsc/bes-sistem-toplu-birlestirme`. Bu dosya **kanıt haritası**, tamamlandı/taşındı onayı değildir. Tetik, izin, script ve veri aktarımı gerçek eski YAML içeriklerinden kontrol edildi.

| Eski workflow | Tetik | İzin | Önemli gerçek işler / bağımlılık | K1–K5 hedefi | Durum |
|---|---|---|---|---|---|
| `madsc-01-guvenlik.yml` | dispatch, workflow_call | contents:read, actions:read | 26 kural runtime kanıt kapısı; protected snapshot/check; 92 eşdeğerlik audit; çoklu regresyon ve toplu hata kapısı | K1 + K5 | Eksik: 26/26 gerçek enforcement |
| `madsc-02-kesif.yml` | cron 05:17/17:17 ve 06:00/18:00 UTC, dispatch, call | contents:read, actions:read | geçmiş restore → discovery archive before/after → gerçek keşif → logo/EPG join → dört aşama; geniş tarama; toplu test | K2 → K3/K5 | Eksik: canlı keşif ve geçmiş aktarımı |
| `madsc-03-kanal-test.yml` | cron 06:40 UTC, sınırlı push, dispatch, call | contents:read, actions:read | ffmpeg; gerçek aday medya ölçümü → scoring; ana liste 100'lü salt-okunur health; logo/EPG, IBO artefakt; 10 adımlı sonuç kapısı | K3 → K5, K1 | Eksik: gerçek ffprobe ve zamanlı kanıt |
| `madsc-04-arsiv-yedek.yml` | dispatch, workflow_call | contents:read, actions:read | isolated git restore → backup evidence → archive consistency → disaster recovery dry run; `CALISANLAR.m3u`/`YENILER.m3u` kopyada restore; offsite `DOGRULANMADI`, historical restore false; 4 regresyon, toplu hata kapısı | K4 → K5, K1 | Eksik: gerçek offsite ve tarihsel restore |
| `madsc-05-genel-bakim.yml` | workflow_call / dispatch, diğer kategorilere needs | contents:read, actions:read (çağrılan işler) | K1→K2→K3→K4 needs; önceki kategori artefaktları; 92 satırlık karar matrisi (tamamı BLOCKED); toplu sonuç ve hata listesi | K5 (K1–K4 bağımlı) | Eksik: gerçek koşu bazlı kabul |
| `aday-bekletme.yml` | dispatch, paths push | contents:read | yeni_kanal_tara → tekrar raporu → gelişmiş medya testi → aday bekletme → akıllı takvim → RETEST_LIMIT=5 yeniden test → kaynak güven puanı → aday öncelik; 10 artefakt | K2 → K3 → K5 | Eksik: tüm yeniden test ve güven puanı davranışı |
| `akilli-aday-puanlama.yml` | dispatch, paths push | contents:read | SCAN_BATCH=-1 discovery → gerçek ffprobe öncelik testi → teknik score → 4 artefakt | K2 → K3 → K5 | Skor/CSV uyumluluğu fixture; canlı kanıt yok |
| `birlesik-aday-raporu.yml` | dispatch, paths push | contents:read | cache/restore geçmiş → discovery → priority/general ffprobe → scoring → stability → birleşik onay raporu; 4 artefakt | K2 → K3 → K5 | CSV/JSON uyumluluğu fixture; gerçek geçmiş toplama yok |

**Dikkat:** K5 eski workflow'u 92 satırın tamamının `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` olmasını şart koşuyor. Dolayısıyla 92 satırın varlığı **92 davranışın kabul edildiği** anlamına gelmiyor. Bu sekiz kaynak arasında gerçek çapraz bağımlılıklar var; tek tek fixture geçmesi yeterli değil.

**Sıradaki:** 99 dosyanın kalan 91'i için tetik/izin/çalışan script/çıktı sınıflandırmasını tamamla, 92 kapsam farkını kanıtla. Korunan listelere dokunma, üretim cron/yazma açma.


## İkinci grup — 8 eski YAML (salt-okunur gerçek kaynak incelemesi)

| Workflow | Tetik ve izin | Script / davranış | Hedef ve açık kanıt |
|---|---|---|---|
| `kanal-kararlilik.yml` | dispatch + paths push; contents:read | cache/restore `KARARLILIK_GECMISI.json` → ffprobe `oncelikli_kanal_dogrula.py` → `kanal_kararlilik_takip.py` → cache/save ve artifact | K3→K5; gerçek zamanlı kalıcı geçmiş zinciri eksik |
| `genel-aday-medya-test.yml` | dispatch + paths push; contents:read | `SCAN_BATCH=-1` aday keşfi, ffprobe, `ADAY_TEST_GRUBU=0` gerçek video/ses testi, CSV+JSON artifact | K2→K3; canlı ffprobe kanıtı eksik |
| `aday-logo-epg-test.yml` | dispatch + paths push; contents:read | `candidate_epg_logo_join.py`, `CALISANLAR.m3u` SHA256 önce/sonra; 5 pilot EPG, playlist onaysız; artifact | K2→K3/K5, K1; kimlik/EPG canlı uyum kabulü eksik |
| `aday-yedekleme.yml` | dispatch + main push (command file); contents:read | `yedekler/teknik_adaylari_aktar.py` teknik aday yedek **taslak** M3U artifact, listeye push yok | K4 + K2; YEDEKLER'e yazma yetkisi çıkarılamaz |
| `felaket-kurtarma-tatbikati.yml` | dispatch + paths push; contents:read | `scripts/disaster_recovery_dry_run.py`, geçici restore raporu artifact | K4; offsite/tarihsel bağımsız geri yükleme kanıtı değil |
| `madsc-birlesik-kesif.yml` | dispatch + 06/18 UTC cron; **contents:write, actions:write**; main koşulu | failure gate → discovery archive before/after → `madsc_akilli_kesif.py` → logo/EPG join → dört aşama → `protected_write_gate.py` → `git push origin HEAD:main` | K1+K2+K5 **yüksek yazma riski**; eski izinleri yeniye taşımak yasak, gerçek yazma yolları denetlenecek |
| `epg-gunluk.yml` | dispatch + 03:25 UTC cron; **contents:write**; main koşulu | `build_epg.py`, `build_ibo_epg_test.py`, `epg_tv_readiness.py`; belirli EPG çıktıları `git add`, protected write gate ve `git push` | K1+K3+K5; korunan EPG değişikliği yasak, üretim yayını yeni sisteme otomatik aktarılmaz |
| `epg-pages.yml` | dispatch + başarılı `EPG Günlük Güncelleme` workflow_run(main); contents:read, **pages:write, id-token:write** | EPG XML doğrula, `_site` hazırla, Pages dağıtımı; başarılı eski workflow sonucuna bağlı | K3+K5; yeni Pages dağıtımı yetkilendirilmedi, IBO EPG cihaz uyumu kanıtlanmadı |

**İkinci grup sonucu:** 16/99 eski YAML dosyasının kaynak içeriği ayrıntılı incelendi; **83 dosya** ayrıntılı inceleme bekliyor. Bu bir davranış eşdeğerliği onayı değil. İzinli eski cron, push ve Pages işlemleri **yeni depoda açılmadı**. Eski workflow'lar kapatılmadı.


## Üçüncü grup — 12 eski YAML (kaynak tetik/izin/komut taraması)

| Workflow | Tetik/izin | Gözlenen iş | K hedefi | Açık durum |
|---|---|---|---|---|
| `madsc-ana-liste-saglik.yml` | dispatch, schedule; contents:read | ana_liste_saglik.py --batch-size 50 --timeout 15, ffmpeg, unittest, rapor artefaktı | K3→K5 | gerçek 50'li saha ölçümü |
| `madsc-arsiv-yedek-aktarim.yml` | dispatch; contents:read | yalnız uyarı; otomatik korunan liste aktarımı kapalı | K4+K1 | bilerek kapalı işlev |
| `madsc-aylik-merkezi-denetim.yml` | dispatch, push, schedule; contents:read, actions:read | workflow envanteri, logo/EPG/IBO, restore, 8/18/6 alan, çoklu rapor ve regresyon | K1–K5 | toplu gerçek kabul |
| `madsc-cuma-ana-liste-denetimi.yml` | dispatch; contents:read | haftalık ana liste denetimi ve cuma uyarı özeti; JSON artifact | K3→K5 | periyodik denetim kanıtı |
| `madsc-documentation-check.yml` | dispatch; contents:read | belge kontrol adımı | K1+K5 | belge kapsam testi |
| `madsc-genis-kaynak-kontrol.yml` | dispatch; contents:write, actions:write | geniş kaynak taraması, artefakt, rapor adımları; izinler yüksek | K1+K2 | YÜKSEK: gerçek yazma yolları incelenmeli |
| `madsc-hizli-on-kontrol.yml` | dispatch, push; contents:read | cutover readiness, 92 workflow audit, preflight, regresyon ve rapor | K1+K5 | gerçek cutover kabulü |
| `madsc-otomatik-devam.yml` | dispatch; contents:read | otomatik devam bilgilendirme/uyarı adımı | K5 | üretim otomasyonu varsayılmayacak |
| `madsc-rule24-test.yml` | push, dispatch; contents:read | workflow_failure_gate unittest | K1 | gerçek hata kapısı uygulaması |
| `madsc-sistem-saglik-denetimi.yml` | dispatch, schedule; contents:read | sistem sağlık denetimi, unittest ve rapor artefaktı | K1+K3+K5 | gerçek planlı koşu |
| `madsc-son-kontrol.yml` | dispatch, schedule, workflow_run; contents:write, actions:write | failure gate, final_validation, ffmpeg, rapor; onaysız ana liste değiştirmeme uyarısı | K1+K3+K5 | YÜKSEK: write izinleri ve tüm yazma adımları ayrıca incelenecek |
| `madsc-toplu-butunluk.yml` | dispatch, push; contents:read | bulk_integrity_gate.py ve JSON artifact | K1+K5 | gerçek bütünlük kabulü |

**Toplam:** 28/99 kaynak YAML gözden geçirildi, 71 dosya açık. Bu üçüncü grup komut/izin odaklı ilk taramadır; özellikle `madsc-genis-kaynak-kontrol` ve `madsc-son-kontrol` içindeki tüm shell yazma yollarının satır satır denetimi ayrıca gereklidir. Yüksek izinli eski workflow'lar yeni sisteme taşınmadı.


## Dördüncü grup — 12 IBO workflow, kaynak YAML incelemesi

| Workflow | Tetik/izin | Gözlenen gerçek adım | K hedefi / risk |
|---|---|---|---|
| `madsc-ibo-3-5281.yml` | push + dispatch, contents:read | yalnız korunan liste mutasyonunun onaysız kapalı olduğunu bildirir | K1+K5 |
| `madsc-ibo-354-classify.yml` | push, contents:write, main | archive_backups_354_classified.py; git add CALISANLAR.m3u ve IBO arşivleri; gate ardından git push | K1+K4, YÜKSEK |
| `madsc-ibo-364-355-364.yml` | push, contents:write, main | archive_backups_355_364.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `madsc-ibo-398-16-49.yml` | push, contents:write, main | archive_backups_16_49.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `madsc-ibo-530-archive.yml` | push, contents:write, main | archive_backups_399_onward.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `madsc-ibo-6115-second.yml` | push + dispatch, contents:write, main | apply_ibo_6115_second.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `madsc-ibo-ilk-239.yml` | push, contents:write, main | apply_ibo_first_239_decisions.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `madsc-ibo-kararlar-grup1.yml` | push, contents:write, main | apply_ibo_decisions_group1.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `madsc-ibo-second-voice.yml` | push + dispatch, contents:write, main | apply_ibo_second_voice.py; CALISANLAR.m3u stage, gate, git push | K1+K4, YÜKSEK |
| `ibo-bagimsiz-test-listesi.yml` | push + dispatch, contents:read | aday keşfi → gerçek medya testi → ibo_bagimsiz_test_listesi.py; artifact | K2+K3 |
| `ibo-epg-kimlik-denetimi.yml` | push + dispatch, contents:read | ibo_epg_kimlik_denetimi.py; JSON rapor, artifact | K1+K3 |
| `ibo-yedek-kalite.yml` | push + dispatch, contents:read | ffmpeg → ibo_yedek_kalite_tespit.py; CSV artifact | K3+K4 |

**Kritik:** 8 IBO YAML'ında `contents:write`, `CALISANLAR.m3u` git staging, `protected_write_gate.py` ve `git push origin HEAD:main` vardır. Gate'in varlığı **gerçek güvenlik ihlali kanıtı da güvenli yazma onayı da değildir**; scriptlerin tüm dolaylı yazma yolları ve gate enforcement ayrıca incelenecek. Kullanıcının korunan liste değişmezliği kuralı nedeniyle yeni K1–K5'e bu yazma davranışları taşınamaz. IBO cihaz testi kullanıcı tarafından yapılacak.

**Toplam:** 40/99 YAML ilk davranış/izin incelemesi; 59 dosya açık. 92/99 farkı çözülmedi, 92/92 kabul verilmedi.


## Beşinci grup — numaralı test-13..39 (27 YAML)

Bu 27 dosyanın her birinin eski YAML kaynağı açılarak tetik, `permissions` ve adım isimleri incelendi. Tümü `contents:read` kullanıyor; `test-31` yalnız dispatch, diğerleri push+dispatch. **Önemli:** `test-23-live-stream` içindeki canlı erişim testi adı, yeni K3'ün gerçek canlı medya ölçümünü yaptığına kanıt değildir.

| Kaynak YAML | Tetik/izin | Odak | Hedef | Kabul |
|---|---|---|---|---|
| `test-13-kaynak-degisiklik.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-14-istikrar.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-15-logo-epg.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-16-workflow-safety.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-17-candidate-summary.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-18-change-simulation.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-19-integration.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-20-full-integration.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-21-functional-e2e.yml` | push/dispatch; contents:read | erken kaynak/kararlılık/entegrasyon regresyonu | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-22-real-playlist.yml` | push/dispatch; contents:read | gerçek liste/canlı erişim/proje salt-okunur denetim | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-23-live-stream.yml` | push/dispatch; contents:read | gerçek liste/canlı erişim/proje salt-okunur denetim | K1/K5+K3 | yalnız kaynak testi; üretim kanıtı değil |
| `test-24-system-audit.yml` | push/dispatch; contents:read | gerçek liste/canlı erişim/proje salt-okunur denetim | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-25-full-project-readonly.yml` | push/dispatch; contents:read | gerçek liste/canlı erişim/proje salt-okunur denetim | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-26-automation-safety.yml` | push/dispatch; contents:read | otomasyon izinleri/aday onay/yazma riski | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-27-pipeline-contract.yml` | push/dispatch; contents:read | otomasyon izinleri/aday onay/yazma riski | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-28-approval-gate.yml` | push/dispatch; contents:read | otomasyon izinleri/aday onay/yazma riski | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-29-write-path-audit.yml` | push/dispatch; contents:read | otomasyon izinleri/aday onay/yazma riski | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-30-write-risk-report.yml` | push/dispatch; contents:read | otomasyon izinleri/aday onay/yazma riski | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-31-protected-write-gate.yml` | dispatch; contents:read | korunan yazma kapısı ve regresyon | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-32-unapproved-write-regression.yml` | push/dispatch; contents:read | korunan yazma kapısı ve regresyon | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-33-all-write-paths.yml` | push/dispatch; contents:read | korunan yazma kapısı ve regresyon | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-34-protected-write-regression.yml` | push/dispatch; contents:read | korunan yazma kapısı ve regresyon | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-35-remaining-write-gate.yml` | push/dispatch; contents:read | korunan yazma kapısı ve regresyon | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-36-system-integration-audit.yml` | push/dispatch; contents:read | sistem/dolaylı yazma denetimi | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-37-indirect-write-audit.yml` | push/dispatch; contents:read | sistem/dolaylı yazma denetimi | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-38-audit-selftest.yml` | push/dispatch; contents:read | sistem/dolaylı yazma denetimi | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |
| `test-39-protected-playlist.yml` | push/dispatch; contents:read | korunan liste bütünlüğü | K1/K5 | yalnız kaynak testi; üretim kanıtı değil |

**Toplam:** 67/99 kaynak YAML ilk eşleme, **32 dosya** açık. Numaralı test workflow'ları da gerçek YAML dosyasıdır; 92/99 farkını çözmek için bunları gerekçesiz kapsam dışına atmayacağız. 92/92 davranışsal kabul hâlâ yok.


## Altıncı grup — 29 yeni kaynak YAML incelemesi

Tetikler, izinler ve yürütülen ana komutlar salt-okunur eski YAML dosyalarından alındı. Aşağıdaki `read` / `write` değerleri yalnız GitHub `contents` iznidir; gerçek script yan etkilerinin tam denetimi değildir.

| Workflow | contents izni | Komut/çıktı | Hedef/risk |
|---|---|---|---|
| `390-aday-tekrar-test.yml` | read | yedekler/tekrar_test_390.py; artifact | K2/K3 |
| `altinci-aday-tekrar-test.yml` | read | altinci_aday_tekrar_test.py; syntax/fixture + artifact | K2/K3 |
| `besinci-zaman-asimi-test.yml` | read | inline zaman aşımı denetimi | K2/K5 |
| `birlesik-durum-raporu.yml` | read | birleşik durum artifact | K5 |
| `dokuzuncu-akilli-tekrar-test.yml` | read | akıllı tekrar test takvimi unittest | K2/K5 |
| `genis-kanal-tarama.yml` | read | genis_kanal_tara.py; artifact | K2 |
| `iptv-test.yml` | read | iptv_test.py, aday M3U; cron | K3 |
| `kaynak-puanlama-kontrol.yml` | read | kaynak güven puanı syntax/unittest | K2 |
| `madsc-11599-yedek-geri-yukle.yml` | read | diagnose_11599_backups.py | K4 |
| `madsc-son-kontrol-kurtarma-teshis.yml` | read, actions:read | final_validation regresyon ve kurtarma teşhisi | K1/K4/K5 |
| `madsc-tum-sistem-yedek.yml` | read | repository_settings_inventory.py → full_system_backup.py; artifact, cron | K4 |
| `madsc-turk-kanal-geri-sec.yml` | **write** | recover_turkish_backups.py; git add CALISANLAR.m3u, gate, git push main | K1/K4 HIGH |
| `madsc-uc-asama.yml` | **write, actions:write** | verification_pipeline.py; git add madsc_dogrulama/, gate, push main | K1/K3/K5 HIGH |
| `madsc-yedek-turk-ayir.yml` | **write** | keep_turkish_backups.py; git add CALISANLAR.m3u, gate, push main | K1/K4 HIGH |
| `madsc-yedekler-aktarim-test.yml` | read | teknik aktarım unittest | K2/K4 |
| `madsc-yedekler-sayi-duzelt.yml` | **write** | sync_yedekler_category_count.py; git add CALISANLAR.m3u, gate, push main | K1/K4 HIGH |
| `oncelikli-kanal-dogrulama.yml` | read | oncelikli_kanal_dogrula.py; artifact | K3 |
| `onikinci-hata-siniflandirma-test.yml` | read | inline hata sınıflandırma testi | K5 |
| `sozcu-akit-ozel-test.yml` | read | yedekler/sozcu_akit_ozel_test.py; artifact | K3 |
| `toplu-sistem-kontrol.yml` | read | salt-okunur tüm workflow git push uyarı envanteri; artifact | K1/K5 |
| `vod-guncelle.yml` | **write** | VOD JSON stage, protected gate, git push | K1/K5 HIGH |
| `yedek-geri-yukleme-tatbikat.yml` | read | restore_dry_run.py; artifact | K4 |
| `yedekler-yeniler-medya-kontrol.yml` | read | yedekler_yeniler_medya_kontrol.py; artifact | K3/K4 |
| `yeni-aday-on-test.yml` | read | yeni_aday_on_test.py; artifact | K2/K3 |
| `yeni-kanal-arama-2026.yml` | read | yeni_kanal_tara.py; artifact | K2 |
| `yeniler-guvenli-arama.yml` | read | kaynak_kesfet.py → yeni_kanal_tara.py; artifact | K2 |
| `automatic-png-logos.yml` | read | PNG logo artifact üretimi; publish değil | K3/K5 |
| `publish-iptv-png-logos.yml` | **write** | logos/duzeltilmis-*.png stage, protected gate, git push | K1/K3 HIGH |
| `k1-protected-write-tests.yml` | read | protected_write_gate regresyon ve artifact | K1 |

**Kaynak dosya kapsamı:** Önceki 67 + 29 benzersiz YAML = **96/99**. `madsc-yedekler-aktarim-test`, `madsc-ibo-3-5281`, `madsc-son-kontrol-kurtarma-teshis` bu turda yeniden açıldı ancak **tekrar sayılmadı**. Açık kalan 3 YAML: `madsc-yedekler-aktarim-test` değil; kesin fark tam 99 dosya envanteriyle karşılaştırılarak bulunacak. **Yüksek riskli ek yazma yolları** `madsc-turk-kanal-geri-sec`, `madsc-uc-asama`, `madsc-yedek-turk-ayir`, `madsc-yedekler-sayi-duzelt`, `vod-guncelle`, `publish-iptv-png-logos`. Korunan dosyaları veya logoları değiştiren hiçbir yeni işlem yetkilendirilmedi.


## Son üç YAML — 99/99 kaynak ilk incelemesi tamamlandı

| Workflow | Tetik/izin | Gerçek davranış | K hedefi ve sınır |
|---|---|---|---|
| `aday-oncelik-kontrol.yml` | dispatch+paths push; contents:read | `aday_oncelik_raporu.py` syntax; geçici örnek CSV'de güçlü aday ONCELIK=1, zayıf aday ONCELIK=5 | K2/K5; fixture sıralama, üretim eşdeğerliği değil |
| `sekizinci-tekrar-raporu-test.yml` | dispatch+paths push; contents:read | `aday_tekrar_raporu.py` iki kaynak ve aynı kaynak URL tekrarını geçici dizinde CSV ile doğrular | K2; tekrar kanıtı fixture |
| `test-kanal-adaylari.yml` | main paths push+dispatch; contents:read | `scripts/test_kanal_adaylari.py` gerçek aday yanıt testi; `yedekler/TARAMA-TEST-SONUCLARI.m3u` ve JSON yalnız artifact/manual approval | K2/K3/K4; korunan YEDEKLER'e otomatik yazma onayı değil |

**Envanter uzlaştırması:** `docs/ESKI_WORKFLOW_99_ENVANTER.md` içindeki **99/99 benzersiz YAML adı** ile bu haritadaki kod biçiminde yazılmış dosya adları karşılaştırıldı; eksik 3 dosya tespit edilip kaynağından incelendi. Böylece **99/99 YAML dosyasının ilk tetik/izin/komut incelemesi tamamlandı**. Bu **92/92 gerçek davranışsal entegrasyon, 26/26 gerçek güvenlik kuralı, canlı yayın testi veya offsite restore kabulü değildir**. 92 sayısının eski 99 YAML içindeki tam tanımı hâlâ kaynak `five_category_92_workflow_audit.py` üzerinden çözülmelidir. Yüksek izinli eski workflow'ların yazma yolları için satır satır güvenlik incelemesi de açık.


## 92–99 farkı çözüldü — kaynak kod kanıtı

Eski salt-okunur `scripts/five_category_92_workflow_audit.py` içindeki `inspect()` fonksiyonu `.github/workflows/*.y*ml` dosyalarını sayarken **tam 7 YAML'ı kapsam dışında bırakıyor**:

1. `madsc-01-guvenlik.yml`
2. `madsc-02-kesif.yml`
3. `madsc-03-kanal-test.yml`
4. `madsc-04-arsiv-yedek.yml`
5. `madsc-05-genel-bakim.yml`
6. `k1-protected-write-tests.yml`
7. `madsc-hizli-on-kontrol.yml`

İlk beşi `new_category_files = {f"madsc-0{n}-" for n in range(1, 6)}` önekiyle, son ikisi `if path.name in (...) : continue` kuralıyla atlanır. Ardından `if len(items) != 92: raise SystemExit(...)` kabul kapısı bulunur. **99 kaynak YAML − 7 hariç tutulan = 92 eski kapsam YAML**. Bu fark artık belirsiz değildir; ancak kapsamın kendisi scriptteki **tarihsel statik tanım**dır, üretim davranışsal kabul değildir.

Aynı script her 92 iş akışında `behavioral_parity_verified=False`, `migration_decision=BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` üretir; script adı eşleşmelerinin yeterli olmadığını açıkça yazar. Dolayısıyla **92/92 gerçek entegrasyon henüz kanıtlanmamıştır**. Eski dalda hiçbir dosya değiştirilmedi.


## Sekiz eski IBO betiğinin gerçek yazma yolu denetimi

Salt-okunur kaynak: `Madsc55/madsc-tv@madsc/bes-sistem-toplu-birlestirme/scripts/`. Aşağıdaki **sekiz betiğin tamamı** doğrudan `CALISANLAR.m3u` üzerinde `Path.write_text(...)` yapar. Yalnızca YAML `git add` sinyali değil, **somut Python dosya mutasyonu** tespit edilmiştir. Hiçbiri yeni sistemde çalıştırılmadı.

| Betik | Ana liste mutasyonu | Ek çıktı | Sonuç |
|---|---|---|---|
| `archive_backups_354_classified.py` | `p.write_text` satır 32 | iki IBO M3U arşivi, JSON | BLOCKED |
| `archive_backups_355_364.py` | satır 26 | arşiv M3U, JSON | BLOCKED |
| `archive_backups_16_49.py` | satır 26 | arşiv M3U, JSON | BLOCKED |
| `archive_backups_399_onward.py` | satır 28 | arşiv M3U, JSON | BLOCKED |
| `apply_ibo_6115_second.py` | satır 40 | M3U, CSV, JSON | BLOCKED |
| `apply_ibo_first_239_decisions.py` | satır 40 | CSV, JSON | BLOCKED |
| `apply_ibo_decisions_group1.py` | satır 54 | M3U, CSV, JSON | BLOCKED |
| `apply_ibo_second_voice.py` | satır 41 | M3U, CSV, JSON | BLOCKED |

Betiğin `CALISANLAR.m3u` içindeki `📦 YEDEKLER` üyelerini sildiği/yeniden numaralandırdığı durumlar var. Kullanıcının **ana liste, YEDEKLER, YENİLER, FAVORİLER ve cihaz favorilerini değiştirmeme** talimatıyla çatışır. GitHub `protected_write_gate.py` çağrısı commit öncesi koruma amaçlıdır; Python betiği çağrıldığında **çalışma ağacını zaten değiştirebilir**. Bu nedenle güvenli alternatif: yeni K1–K5 yalnız **salt-okunur analiz ve rapor artefaktı** üretir, hiçbir listeye otomatik yazmaz. Betikler, kullanıcı ayrıca yetkilendirmedikçe K4'e aktarılmayacak. Gerçek geçmişte push yapılıp yapılmadığı bu incelemede kanıtlanmadı.


## Ek script seviyesi denetim — Türk YEDEKLER, sayı düzeltme, keşif ve K1 gate

Eski dalda salt-okunur kaynak satırları:

| Betik | Somut yazma yolu | Risk kararı |
|---|---|---|
| `scripts/recover_turkish_backups.py` | `CALISANLAR.m3u` `PLAY.write_text` satır 78; `yedek_ulke_inceleme.csv` satır 75 ve JSON satır 79 | **BLOCKED**: YEDEKLER üyelerini değiştirebilir |
| `scripts/keep_turkish_backups.py` | `CALISANLAR.m3u` `PLAYLIST.write_text` satır 68; ayrılanlar M3U satır 53, JSON satır 73 | **BLOCKED** |
| `scripts/sync_yedekler_category_count.py` | `CALISANLAR.m3u` `p.write_text` satır 18; grup sayısını yeniden yazar | **BLOCKED** |
| `tools/genis_kaynak_taramasi.py` | keşif aday inceleme/state/summary JSON ve CSV çıktıları satır 106–110; ana liste adları satır 68'de okunuyor | Rapor/keşif yazımı var, korunan listeye doğrudan yazma bu taramada bulunmadı; çıktı yolları ayrıca sınırlandırılmalı |
| `verification_pipeline.py` | `madsc_dogrulama/` state ve summary JSON satır 96, 98 | Rapor/state yazımı; çağrılan alt komutların etkisi ayrıca denetlenmeli |

`tools/protected_write_gate.py` kaynağı ayrıca tam okundu: `CALISANLAR.m3u`, `YENILER.m3u`, `YABANCI_KANALLAR.m3u`, `AGENTS.md` gibi adları; `yedekler/`, `FAVORILER/`, `EPG/`, `logolar/`, `logos/`, `arsiv/` öneklerini ve genel `.m3u/.m3u8` uzantılarını reddeder. Git `base..HEAD`, staged, unstaged, untracked ve ignored yollarını denetler; Git komutu başarısızsa **fail-closed** kod 2, korunan değişiklikte kod 1 döner. Bu kaynak davranışı **koruma tasarımı kanıtıdır**, GitHub branch ruleset veya üretimde çalışmış olduğu kanıtı değildir. `git add CALISANLAR.m3u` yapan eski workflow'ların koruma kapısından geçmesi beklenmez; geçmiş koşu sonucu ayrıca incelenmeden gerçek push iddia edilmez.

Bu 3 ek korunan liste yazarı da K1 güvenlik gereği yeni sisteme taşınmayacak. Yeni repo/korunan dosyalar değiştirilmedi.


## EPG, VOD, PNG yayımlama ve birleşik keşif — kod/iş akışı güvenlik karşılaştırması

Eski dalda YAML ve çağrılan betikler salt-okunur incelendi:

| İş akışı | Gerçek çalışma ve çıktı | GitHub yayımlama ve koruma kararı |
|---|---|---|
| `vod-guncelle.yml` | `scripts/vod_guncelle.py` `vod/guncel-bolumler.json` dosyasını yazar (satır 21); `CALISANLAR.m3u` değiştirme komutu bulunmadı | `contents:write`, cron 07:17 UTC, `git add vod/guncel-bolumler.json`, gate+commit+push. Korunan liste dışı VOD JSON yazma **var**; cron/push yeni sisteme aktarılmayacak |
| `publish-iptv-png-logos.yml` | `cairosvg.svg2png` ile `logos/duzeltilmis-*.png` üretir | `contents:write`, main üzerinde git add+gate+push. Gate `logos/` önekini reddettiğinden bu yol **tasarım gereği bloke** olmalı; eski Actions gerçek sonucu bilinmiyor. Yeni sistemde logo değişikliği yok |
| `epg-gunluk.yml` | `scripts/build_epg.py` bağımsız XMLTV/rapor, `scripts/build_ibo_epg_test.py` IBO test EPG, `scripts/epg_tv_readiness.py` JSON (satır 64) | `contents:write`, cron 03:25 UTC, `git add epg/*`, gate+commit+push. Gate `epg/` önekini reddeder: **tasarım gereği bloke**; IBO EPG cihaz kabulü yok |
| `madsc-birlesik-kesif.yml` | `madsc_akilli_kesif.py` ffprobe çağrısı (satır 54), `madsc_kesif/` CSV/JSON/logo adayları ve state; `scripts/discovery_archive.py` history/registry; `CALISANLAR.m3u` ve `YENILER.m3u` okuma | `contents:write`, `actions:write`, cron 06:00/18:00 UTC, `git reset --hard` yalnız runner checkout, raporları `madsc_kesif/` altında 10 denemeli `git push origin HEAD:main`; gate `madsc_kesif/` için genel koruma öneki içermiyor. **Rapor push yolu mevcut**, ama gerçek push başarısı doğrulanmadı. Yeni cron/push kapalı kalmalı |

**Önemli ayrım:** Gate çalışma ağacı/commit değişikliklerini reddeder; bu, yazıcı betiğin runner üzerinde dosya üretmediği anlamına gelmez. PNG ve EPG gate çağrılarının korunan dizinlere göre bloke edilmesi beklenir; bu **statik kaynak değerlendirmesi**, geçmiş koşu kanıtı değildir. VOD JSON ve `madsc_kesif/` rapor yolları gate kapsamındaki korunan dizinler arasında doğrudan yer almaz; bunların da otomatik `main` push'u yeni sistemde yetkisizdir. Korunan listelere, logolara, EPG'ye, VOD'a veya eski depoya yazılmadı.


## Derin betik incelemesi 1 — `aday-bekletme.yml` (19 Ekim 2026)

**Yöntem:** Eski salt-okunur daldaki workflow YAML ve çağırdığı **8 ayrı Python dosyasının gerçek kaynakları** okundu. Bu bölüm önceki yalnız YAML adı/adım taramasından daha derin bir girdi/çıktı haritasıdır. Hiçbir betik çalıştırılmadı.

| Çalışma sırası | Gerçek giriş betiği | Kaynakta gözlenen girdi/çıktı | K1–K5 tasarım karşılığı |
|---|---|---|---|
| 1 | `yeni_kanal_tara.py` | Dış M3U kaynakları için `fetch`, `parse`, `norm`, `hls_probe`, `ffprobe_stream`; `YENILER_TARAMA_RAPORU.csv` gibi tarama çıktıları | K2 keşif → K3 canlı medya |
| 2 | `aday_tekrar_raporu.py` | `aday_bekletme/HAM_ADAY_KAYNAKLARI.csv` → `TEKRAR_EDEN_ADAYLAR.csv`; `duplicate_groups` | K2 URL/aday tekrar ayrımı |
| 3 | `gelismis_medya_testi.py` | `YENILER_TARAMA_RAPORU.csv` → `GELISMIS_MEDYA_TESTI.csv`; `check` | K3 video/ses değerlendirme |
| 4 | `aday_bekletme.py` | Tarama CSV + `aday_bekletme/gecmis.json` → güncellenen `gecmis.json` ve `ADAY_DURUM_RAPORU.csv` | K2/K3 → K5 kalıcı aday durumu |
| 5 | `akilli_tekrar_test_takvimi.py` | `gecmis.json` → `AKILLI_TEKRAR_TEST_TAKVIMI.csv`; `plan` | K5 zamanlama/yeniden test |
| 6 | `altinci_aday_tekrar_test.py` | `gecmis.json` → `ALTINCI_TEKRAR_TEST.csv`; `eligible`, `check`, `load_probes`; YAML `RETEST_LIMIT=5` | K3 tekrar medya ölçümü + K5 sınır |
| 7 | `kaynak_guven_puani.py` | `gecmis.json` → `KAYNAK_GUVEN_PUANLARI.csv` | K2 kaynak güveni → K5 karar |
| 8 | `aday_oncelik_raporu.py` | `ADAY_DURUM_RAPORU.csv` → `ADAY_ONCELIK_RAPORU.csv`; `rank` | K5 aday önceliği |

**Davranış zinciri:** dış kaynak keşfi → tekrar kayıtları → teknik video/ses testi → geçmişe yazılan bekletme durumu → tekrar test takvimi → sınırlı tekrar test → kaynak güven puanı → aday öncelik raporu. YAML'da `contents:read`, manuel ve dosya değişimi tetikleri, `cancel-in-progress: false`, 90 dakikalık job sınırı, ffmpeg kurulumu ve `if: always()` artefakt yükleme var.

**Kritik bulgu:** Workflow GitHub deposuna push yapmasa bile betikler runner çalışma ağacında `aday_bekletme/gecmis.json` gibi **kalıcı olması amaçlanan durum dosyalarını yeniden yazar**. Bu, eski koşular arasında durumun gerçekten saklandığı anlamına gelmez; artifact/cache/commit üzerinden devamlılık ayrıca kanıtlanmalı. Yeni K2/K3 salt-okunur fixture testleri bu sekiz adımlı davranışın tamamını henüz karşılamıyor.

**Gerekli parity testleri:** kaynak/aday tekilleştirme; tarama CSV şeması; teknik sonuç ve IBO cihaz sonucunun ayrımı; geçmiş dosyasının önce/sonra kimliği; `RETEST_LIMIT=5` ve yeniden deneme takvimi; kaynak güven puanı ve öncelik sıralaması; eksik/bozuk geçmişte fail-closed; 10 artefaktın şema ve içerik eşlemesi; runner koşuları arasında gerçekten kalıcı durum kanıtı. Korunan ana liste, YEDEKLER, YENİLER, EPG, logo ve favorilere yazma **yasak**. **Karar: `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE`.**


## Derin kaynak incelemesi 2 — 12 YAML ve 13 çağrılan betik (19 Ekim 2026)

Eski salt-okunur dalda **12 YAML** ve bu işlerin kullandığı **13 Python betiği** ayrı ayrı açıldı; adım sırası, tetikler, girdi/çıktı dosyaları ve yazma sinyalleri kaynaklardan çıkarıldı. Önceki derin inceleme `aday-bekletme.yml` idi. Bu bölüm **kaynak işlev çözümlemesidir**, yeni sistemde davranışsal parity onayı değildir.

| Kaynak YAML | Gerçek işlev / girdi → çıktı | Risk / K1–K5 hedefi |
|---|---|---|
| `390-aday-tekrar-test.yml` | `yedekler/tekrar_test_390.py`: `CALISANLAR.m3u` ve 390 aday M3U kaynağı; ffmpeg tabanlı paralel 20 saniye video/ses testi → `TEKRAR_TEST_2026-10-09.csv` + `TEKNIK_DOGRULANANLAR_2026-10-09.m3u` | K3/K4; çıktı M3U **runner üzerinde üretilir**, korunan listeye yazma yetkisi değildir |
| `akilli-aday-puanlama.yml` | `scripts/akilli_aday_puanla.py`: teknik kanıt puanı → `AKILLI_ADAY_PUANLARI.csv`, `AKILLI_ADAY_OZET.json` | K2→K3→K5; puan eşikleri ve şema parity eksik |
| `birlesik-aday-raporu.yml` | gerçek aday keşfi + ffprobe → puanlama + `kanal_kararlilik_takip.py` + `birlesik_aday_raporu.py` → `BIRLESIK_ADAY_ONAY_RAPORU.csv`, `BIRLESIK_ADAY_OZET.json` | K2→K3→K5; **birleşik rapor onay vermekle eş anlamlı değildir** |
| `kanal-kararlilik.yml` | önceki `KARARLILIK_GECMISI.json` cache restore → gerçek ffprobe → `kanal_kararlilik_takip.py` → `KARARLILIK_RAPORU.csv`, `KARARLILIK_OZET.json` ve sonraki koşu için cache save | K3→K5; bu workflow'da cache mekanizması YAML'da açık, gerçek süreklilik koşu kanıtı eksik |
| `genel-aday-medya-test.yml` | keşif + ilk aday grubunda gerçek video/ses ffprobe → ayrı rapor artefaktı | K2→K3; canlı ölçüm parity eksik |
| `aday-logo-epg-test.yml` | `candidate_epg_logo_join.py`: aday logo JSON + `epg/ibo-test-epg.xml` okuma → `candidate_epg_logo_join.json` | K2/K3/K5; EPG/IBO kimlik eşleşmesi ve cihaz kabulü eksik |
| `aday-yedekleme.yml` | `yedekler/teknik_adaylari_aktar.py`: ana liste/aday CSV ve M3U referansları → teknik aday taslak M3U | K4; salt rapor/artifact, **YEDEKLER'e otomatik aktarım izni yok** |
| `felaket-kurtarma-tatbikati.yml` | `disaster_recovery_dry_run.py`: Git kaynaklı `CALISANLAR.m3u` / `YENILER.m3u` byte kopyası ve checksum → `DISASTER-RECOVERY-REPORT.json` | K4; geçici git restore, **offsite yedek kanıtı değil** |
| `epg-pages.yml` | EPG XML doğrulama → Pages yayını hazırlama; `workflow_run` tetik bağımlılığı, Pages dağıtım yetkisi | K3/K5; gerçek yayın/deploy davranışı yeni sistemde yetkisiz |
| `vod-guncelle.yml` | `vod_guncelle.py` dış veri `urlopen` → `vod/guncel-bolumler.json` → gate ve `git push`; cron + `contents:write` | K1/K5 **YÜKSEK**; yeni cron/push açılmayacak |
| `madsc-birlesik-kesif.yml` | `discovery_archive.py` geçmiş + aday CSV → `madsc_akilli_kesif.py` dış kaynak/ffprobe → logo/EPG join → `four_stage_discovery_report.py` birleşik JSON; gate + `git push` | K1/K2/K3/K5 **YÜKSEK**; rapor state'i ve çoklu push yolu ayrıca denetlenecek |
| `madsc-01-guvenlik.yml` | `k1_protected_integrity.py` Git/çalışma ağacı korunan dosya snapshot'ı ve değişmezlik kontrolü; `k1_24_rule_evidence.py` güvenlik belgesi/kanıt taraması; regresyon ve hata kapısı | K1/K5; **26/26 gerçek enforcement kanıtı değil** |

**Kaynak seviyesinde eklenen 13 betik:** `yedekler/tekrar_test_390.py`, `scripts/akilli_aday_puanla.py`, `scripts/kanal_kararlilik_takip.py`, `scripts/birlesik_aday_raporu.py`, `scripts/candidate_epg_logo_join.py`, `yedekler/teknik_adaylari_aktar.py`, `scripts/disaster_recovery_dry_run.py`, `scripts/vod_guncelle.py`, `scripts/discovery_archive.py`, `madsc_akilli_kesif.py`, `scripts/four_stage_discovery_report.py`, `scripts/k1_protected_integrity.py`, `scripts/k1_24_rule_evidence.py`.

**Bulgular:** Bazı işlerin davranışı yalnız YAML adından anlaşılmıyor: `birlesik-aday-raporu` ve `madsc-birlesik-kesif` birden çok K kategorisine bağımlı; `kanal-kararlilik` cache restore/save kullanırken `aday-bekletme` için aynı kalıcılık ayrı doğrulanmalı. `vod-guncelle` ve `madsc-birlesik-kesif` gerçek yazma/yayımlama yolları içeriyor; yeni salt-okunur K1–K5'e otomatik taşınmaları güvenli değil. Bu kaynak taramasında hiçbir script çalıştırılmadı; üretim dosyası, eski repo, cron ve Pages yayını değiştirilmedi.

**Kapsam:** 99 YAML ilk inceleme tamam; bu turda **12 YAML** kaynak + **13 betik** derin incelendi, önceki turdaki 1 YAML/8 betikten ayrı. Dolayısıyla toplam **13 benzersiz YAML derin çözümleme**, **21 betik kaynak incelemesi**; **86 YAML** henüz aynı derinlikte çözülmedi. 92 eski kapsamın kaçının bu 13 içinde olduğu ayrı sayılmalı (beşli kategori koordinatörü kapsam dışıdır). **92/92 parity onayı hâlâ 0**.


## Kritik derin kaynak bulgusu — `automatic-png-logos.yml` (19 Ekim 2026)

Eski salt-okunur YAML ve `scripts/automatic_png_logos.py`, `scripts/logo_visual_evidence.py`, `logo_deneme/audit.py` gerçek kaynakları açıldı. Workflow `contents:read` ve artefakt yükleme kullanıyor, ancak **betiklerin yerel dosya yazma etkisi GitHub token yetkisinden bağımsız**.

- `automatic_png_logos.py` içindeki `main()`, `CALISANLAR.m3u` okur; eksik `tvg-logo` alanlarını IPTV-org channel/logo API kaynaklarıyla eşlemeye çalışır; yalnız önceden saklanmış görsel doğrulama (`visual_match=True`), kaynak URL ve PNG SHA256 eşleşmesi varsa logo ekler. `approved_repairs.json` ile mevcut logo URL'si onarımı için ayrıca hash/önceki kaynak kontrolü uygular.
- `convert()`, `logos/auto/*.png` altına **`write_bytes`** yapabilir; 4 MB indirme, 16 milyon piksel ve 640×640 küçültme sınırları, SVG dış kaynak reddi var.
- `main()` **koşulsuz `playlist.write_text(updated)`** çağırır. `updated == raw` olsa bile çalışma ağacındaki korunan `CALISANLAR.m3u` dosyasını yeniden yazar. Ayrıca `logo_deneme/png_automation.json` üretir. `assert strip(updated)==strip(raw)` yalnız logo dışı metni karşılaştırır; **logo alanı değişimine izin verir**.
- `logo_visual_evidence.py` görsel inceleme raporu `logo_deneme/visual_review.json` yazar; `logo_deneme/audit.py` `rapor.json` ve `ozet.json` üretir.

**Sonuç:** `contents:read` olması, eski betiğin korunan listeyi çalışma ağacında değiştirmeyeceği anlamına **gelmez**. Yeni sistemde bu scriptin `main()` fonksiyonunu üretim ana listesi üzerinde çalıştırmak **BLOCKED**. Yalnız korunan dosyalara yazmayan izole fixture, hash karşılaştırması ve onaylı görsel kanıtla test edilmeli. Bu statik kod bulgusu geçmiş GitHub push veya fiili korunan liste değişikliği kanıtı değildir. K1/K3/K5 güvenlik ve logo kanıt eşlemesi henüz onaylanmadı.


## Derin kaynak incelemesi 3 — 10 YAML ve 11 Python betiği (19 Ekim 2026)

Eski salt-okunur daldan bu 10 YAML ve 11 Python betiği açıldı. Adım isimleri, tetikler, script girişleri ve kodun okuduğu/yazdığı dosyalar karşılaştırıldı. Bu **statik davranış çözümlemesidir**; betikler çalıştırılmadı ve üretim parity onayı verilmedi.

| YAML | Gerçek görev zinciri ve somut çıktı | K hedefi / risk |
|---|---|---|
| `besinci-zaman-asimi-test.yml` | YAML içi zaman aşımı davranışı doğrulaması; harici Python girişi yok | K1/K5; inline testin beklenen sonuçları ayrıca karşılaştırılmalı |
| `birlesik-durum-raporu.yml` | `guncel_test_durum_ozeti.py` önceki doğrulama özetlerini okur; `eksik_turk_kanal_takibi.py` ana liste/geçmişi inceler; `kaynak_kapsam_denetimi.py` kaynak erişim raporunu okur; `genel_sistem_bakimi.py` sistem özetleri ve notlardan `weekly_health.json` üretir | K1/K5; yeni test başlatmadan durum raporlama |
| `dokuzuncu-akilli-tekrar-test.yml` | YAML içi akıllı tekrar zamanlama doğrulaması, harici script yok | K3/K5; inline kural testi |
| `epg-gunluk.yml` | `build_epg.py` ana liste ve dış EPG XML kaynaklarını okuyup `epg/madsc-epg.xml` ve rapor üretir; `build_ibo_epg_test.py` 5 kanallık pilotu hazırlar; `epg_tv_readiness.py` cihaz bekleme raporu üretir; gate ardından `git push` | K1/K3/K5 **YÜKSEK**: `contents:write`, cron ve EPG yayımlama; IBO gerçek cihaz kabulü yok |
| `genis-kanal-tarama.yml` | `genis_kanal_tara.py` çoklu dış M3U kaynaklarını indirir, parse/normalize eder, yayınları probe eder → `GENIS_KANAL_TARAMA_RAPORU.csv` | K2/K3; canlı keşif ve medya kanıtı |
| `ibo-bagimsiz-test-listesi.yml` | Gerçek video/ses test raporu `GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv` → `ibo_bagimsiz_test_listesi.py` ile `IBO_BAGIMSIZ_TEST_ADAYLARI.m3u`, `IBO_TEST_ADAYLARI.csv`, `IBO_TEST_OZET.json` | K2/K3/K5; izole cihaz deneme listesi, ana liste değişikliği değil |
| `ibo-epg-kimlik-denetimi.yml` | `ibo_epg_kimlik_denetimi.py` ana liste ile `epg/madsc-epg.xml` pilotunun kanal kimlik eşleşmesini inceler, rapor yazar | K1/K3; XMLTV kimlik uyumu cihazda ayrıca sınanmalı |
| `ibo-yedek-kalite.yml` | YAML inline ffprobe yedek yayın ölçümü ve kalite raporu | K3/K4; gerçek yedek akış ölçümü eksik |
| `iptv-test.yml` | `iptv_test.py` ana liste ve dış medya/IBO denemeleri yapar, ardından **`Path('CALISANLAR.m3u').write_text(...)`**, `CALISMAYANLAR.txt` yazımı ve `TEST_RAPORU.csv` oluşturur | **K1/K3/K5 KRİTİK:** ana listeyi yeniden yazar, favori/kategori/sıra davranışını etkileyebilir; yeni sistemde doğrudan çalıştırılması **BLOCKED** |
| `kaynak-puanlama-kontrol.yml` | `kaynak_guven_puani.py` syntax ve kaynak güven puanı testleri | K2/K5; fixture/test sonucu gerçek kaynak güveni parity değildir |

**İncelenen 11 betik:** `tools/guncel_test_durum_ozeti.py`, `tools/eksik_turk_kanal_takibi.py`, `tools/kaynak_kapsam_denetimi.py`, `tools/genel_sistem_bakimi.py`, `scripts/build_epg.py`, `scripts/build_ibo_epg_test.py`, `scripts/epg_tv_readiness.py`, `genis_kanal_tara.py`, `scripts/ibo_bagimsiz_test_listesi.py`, `scripts/ibo_epg_kimlik_denetimi.py`, `iptv_test.py`.

**Güvenlik ayrımı:** YAML'da `contents:read` olsa da `iptv_test.py` runner çalışma ağacında korunan listeyi değiştirebilir. GitHub'a başarılı push yaptığı **kanıtlanmadı**; yerel dosya mutasyonu doğrudan koddan doğrulandı. EPG üretim cron/push davranışı ve cihaz onayı yeni sisteme taşınmadı.

**Kapsam:** Önceki 13 benzersiz YAML + bu 10 = **23/99 derin YAML incelemesi**; önceki 21 betik + bu 11 = **32 betik kaynak incelemesi** (bu turlarda benzersiz yollar). Kalan **76 YAML** aynı derinlikte bekliyor. 92 eski kapsam içinde bu 23'ten `madsc-01-guvenlik.yml` kapsam dışı, dolayısıyla **22/92** derin incelendi. **Davranışsal parity onayı 0/92**.
