# K1-K5 — Altı Python betiğinin gerçek işlem zinciri

Sabit kaynak `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Aşağıdaki betiklerin kaynak metinleri okundu. Çalıştırma yapılmadı.

| Betik | Okuma/ağ | Yazma/yan etki | Önemli sınır |
|---|---|---|---|
| `scripts/vod_guncelle.py` | TVMaze TR schedule API, bugün ±7 gün, her istek 20 sn | `vod/guncel-bolumler.json` yazar; workflow ayrıca commit/push yapar | API hatalarını atlayarak kısmi/boş veri de yazabilir; izlenmeli |
| `scripts/restore_dry_run.py` | İki sabit `yedekler/` kaydı ve korunan `CALISANLAR.m3u`, `YENILER.m3u` SHA256 | Yedekleri geçici dizine byte-identical kopyalar, M3U parse eder, negatif bozuk yedek testi, `RESTORE-DRY-RUN-REPORT.json` yazar | Üretime restore yapmaz; sabit iki yedek dışında genel restore kanıtı yok |
| `scripts/yedekler_yeniler_medya_kontrol.py` | `CALISANLAR.m3u` içinde YEDEKLER/YENİLER grupları, 8 iş parçacığı, ffprobe timeout 16 sn | `YEDEKLER_YENILER_MEDYA_TEST.csv` ve `YEDEKLER_YENILER_MEDYA_OZET.json` | Teknik ses/video sinyali oynatıcı uyumluluğu veya kanal kimliği kanıtı değildir |
| `yeni_aday_on_test.py` | Korunan ana liste, iptv-org TR M3U, logo API; 12 paralel ffprobe, 14 sn timeout | `YENI_ADAY_ON_TEST.csv` | İsim normalizasyonu ve URL tekrar filtresi; doğrulama yalnız codec türü varlığı |
| `kaynak_kesfet.py` | GitHub arama API 5 sorgu; en fazla 60 depo, 120 kaynak, 90 gün; 12 sn ağ timeout | `YENI_KAYNAK_ONERILERI.csv`, `KAYNAK_KESIF_HATALARI.txt` | Keşfedilen kaynaklar yalnız öneri; üretim listeye otomatik eklenmez |
| `yeni_kanal_tara.py` | Sabit kaynaklar ve keşif CSV'si; SCAN_BATCH çevre değişkeni; M3U/HLS ve ffprobe | `YENILER_TARAMA_RAPORU.csv`, `YENILER_KAYNAK_HATALARI.txt`, `aday_bekletme/HAM_ADAY_KAYNAKLARI.csv` | Kendi başına üretim listeye push etmez; HLS teknik erişim kanal kimliği kanıtı değildir |

## İşlevsel eşdeğerlik için zorunlu testler

1. VOD API başarısız olduğunda mevcut sağlıklı JSON'un korunup korunmadığını sınamak.
2. Restore dry-run için yedek bulunmaması, bozuk M3U, hash uyuşmazlığı ve üretim dosyalarının değişmezliği.
3. Tarama ve ffprobe için ağ zaman aşımı, hatalı URL, çoklu aday, yinelenen isim/URL, boş kaynak ve rapor şeması.
4. 66 matrix işinde kaynak keşif artifact aktarımı, grup kapsamı, toplam eşzamanlılık ve sonuç birleştirme.

Bu belge betiklerin kaynak analizidir; gerçek koşu veya davranışsal kabul değildir. Doğrulanmış davranışsal eşdeğerlik **0/92**.
