# İlk 12 eski workflow: yürütme zinciri ve davranış ayrıştırması

Sabit kaynak `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. **12 YAML'ın tam metni GitHub'dan okunarak** tetikleyici, komut sırası, izin, artifact ve koşul ayrıştırıldı. Bu çalışma kaynak davranışı çözümlemesidir; çalıştırma kanıtı değildir.

| Workflow | Aday K | Tetikleyici | Gerçek komut zinciri | Çıktılar | Koşul / sınır | Açık eşdeğerlik ihtiyacı |
|---|---|---|---|---|---|---|
| 390-aday-tekrar-test | K3 | push/dispatch | yedekler/tekrar_test_390.py; ffmpeg; TEST_WORKERS=10 | yedekler/TEKRAR_TEST_2026-10-09.csv; TEKNIK_DOGRULANANLAR_2026-10-09.m3u | 90 dk; artifact always; contents read | Canlı yayın testleri fixture dışı; artifact gerçek kanıtı yok |
| aday-bekletme | K2/K3/K5 | push/dispatch | yeni_kanal_tara → aday_tekrar_raporu → gelismis_medya_testi → aday_bekletme → akilli_tekrar_test_takvimi → altinci_aday_tekrar_test → kaynak_guven_puani → aday_oncelik_raporu | aday_bekletme/* raporları; YENILER_TARAMA_RAPORU.csv | 90 dk; concurrency cancel=false; artifact always | Sekiz betiğin sırası ve state/geçmiş zinciri korunmalı |
| aday-logo-epg-test | K1/K3 | push/dispatch | py_compile; candidate_epg_logo_join; CALISANLAR sha256 before/after | madsc_kesif/candidate_epg_logo_join.json | 10 dk; 5 pilot EPG kanalı ve onay=false assert | Ana liste hash kontrolü var; cihaz doğrulaması yok |
| aday-oncelik-kontrol | K2/K5 | push/dispatch | aday_oncelik_raporu.py izole $RUNNER_TEMP fixture | ADAY_ONCELIK_RAPORU.csv geçici | iki aday 1 ve 5 öncelik assert | Üretim verisi değil, fixture davranışı |
| aday-yedekleme | K4/K1 | push/dispatch | yedekler/teknik_adaylari_aktar.py; GH_TOKEN env | yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u | 30 dk; artifact always; contents read | Yedek taslağı onay bekler; ana listeye geçiş yok |
| akilli-aday-puanlama | K2/K3/K5 | push/dispatch | yeni_kanal_tara SCAN_BATCH=-1 → oncelikli_kanal_dogrula → akilli_aday_puanla | AKILLI_ADAY_PUANLARI.csv; AKILLI_ADAY_OZET.json; ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv; ONCELIKLI_OZET.json | 55 dk; artifact required; 30 gün | Gerçek ffprobe gerektirir, bu oturumda çalıştırılmadı |
| altinci-aday-tekrar-test | K3/K5 | push/dispatch | py_compile; unittest.mock HLS ve ffprobe; sonra gerçek altinci_aday_tekrar_test.py RETEST_LIMIT=5 | aday_bekletme/ALTINCI_TEKRAR_TEST.csv | 20 dk; artifact always | Mock birim kontrolü ve canlı tekrar testini ayır |
| automatic-png-logos | K1/K3 | dispatch | logo_deneme/audit.py → automatic_png_logos.py → logo_visual_evidence.py; git restore CALISANLAR | logos/auto/; logo_deneme/*.json; visual_frames | 15 dk; artifact always; git restore sadece CALISANLAR | Korunan listeyi geri alma yan etki, tüm yazmaları bloke ettiği anlamına gelmez |
| besinci-zaman-asimi-test | K3/K5 | push/dispatch | gelismis_medya_testi.check mock TimeoutExpired(65) | assert BELIRSIZ/BELIRSIZ; TEKRAR_TEST_BEKLIYOR | İzole unit test | Timeout yayın bozuk sayılmamalı |
| birlesik-aday-raporu | K2/K3/K5 | push/dispatch | cache restore → yeni_kanal_tara → oncelikli_kanal_dogrula → genel_aday_medya_test → akilli_aday_puanla → kanal_kararlilik_takip → birlesik_aday_raporu | BIRLESIK_ADAY_ONAY_RAPORU.csv; BIRLESIK_ADAY_OZET.json; medya raporları | 60 dk; artifact required | KARARLILIK_GECMISI.json cache geçmişi ve canlı probe bağımlılığı |
| birlesik-durum-raporu | K5/K2 | push/dispatch | guncel_test_durum_ozeti → eksik_turk_kanal_takibi → kaynak_kapsam_denetimi → genel_sistem_bakimi | combined-status.json; missing-turkish-channels.json; source-inventory-audit.json; weekly_health.json | 5 dk; artifact 30 gün | Yayın test etmeden durum raporu; fixture ile ayrıştırılabilir |
| dokuzuncu-akilli-tekrar-test | K5/K2 | push/dispatch | python3 -m unittest -v test_akilli_tekrar_test_takvimi.py | test çıktısı | contents read; push paths | Zamanlama unit testi, gerçek dispatch kanıtı değil |

## Kesinleşen ayrımlar

- `aday-bekletme` ve `birlesik-aday-raporu` tek betik değil; sıraya bağımlı çok adımlı zincirler. Salt fonksiyon eşlemesi tam workflow eşdeğerliği sayılmaz.
- `automatic-png-logos` içindeki `git restore -- CALISANLAR.m3u`, o dosyadaki unstaged değişikliği geri alır; tüm dosya yazmalarını önleyen genel koruma değildir.
- `aday-logo-epg-test` pilot EPG sayısını 5 olarak assert eder, playlist approval false kontrolü yapar; cihaz üstünde IBO kabulü yapmaz.
- `besinci-zaman-asimi-test` timeout'u bozuk yayın olarak işaretlemez; tekrar test bekleme davranışı K3 için korunmalı.
- `birlesik-durum-raporu` canlı medya test etmez, diğer canlı ffprobe workflow'larından ayrı güvenlik sınıfıdır.
- `aday-yedekleme` M3U dosyasını artifact olarak saklar; ana listeye yayınlama/onay işlemi olarak yorumlanmamalı.

**Kabul:** 12/92 kaynak YAML zinciri bu raporda ayrıştırıldı; 0/92 davranışsal eşdeğerlik kabulü. Önceki beş riskli workflow raporuyla kapsam kısmen örtüşmez; betiklerin derin dolaylı çağrı incelemesi ve gerçek kanıt eksik. Korunan dosyalara yazılmadı, workflow çalıştırılmadı.
