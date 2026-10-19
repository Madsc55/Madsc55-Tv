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
