# K5 — Altı sabit eski workflow için YAML-temelli statik sözleşme karşılaştırması

Tarih: 2026-10-23. Kaynak depo `Madsc55/madsc-tv`, sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Altı workflow doğrudan GitHub'dan okunarak blob SHA'ları doğrulandı. Buradaki K aşaması atamaları **kaynak YAML'dan türetilmiş aday karşılıklardır**, kabul edilmiş uygulama eşdeğerliği değildir. Python script'lerinin tüm içerikleri ve yürütme artifact'ları ayrıca incelenmedi.

| Sabit eski workflow / blob SHA | Kaynakta doğrulanan iş sözleşmesi | Yeni beşli sistemde aday karşılık ve eksik kanıt |
|---|---|---|
| `.github/workflows/aday-oncelik-kontrol.yml` / `1c2aa765b59ebad5ddbe3f0a06fcc9ead088e52b` | Manuel veya iki dosyada push; izole örnek CSV'de güçlü aday öncelik 1, zayıf aday öncelik 5; ana liste değişmeden test | K2 aday sıralama, K5 fixture test; gerçek sıralama girdisi ve CSV şeması eşdeğerliği eksik |
| `.github/workflows/aday-yedekleme.yml` / `6ee9e08cc161b1fc975a8108fa102867de2d9690` | Manuel veya belirtilen komut dosyası değişiminde main push; 30 dk timeout; GH_TOKEN ile teknik aday aktarım script'i; onay bekleyen M3U taslağı artifact | K3 teknik sonuç, K4 taslak yedek, K1 güvenli çıktı; token kullanımının script yan etkileri ve artifact SHA doğrulanmadı |
| `.github/workflows/akilli-aday-puanlama.yml` / `8efd3656127031ebd3d73ca32d13ae55f9e22cb8` | Manuel veya iki dosyada push; 55 dk timeout; SCAN_BATCH=-1; gerçek ffprobe; iki CSV girdisiyle puanlama; dört rapor, 30 gün saklama ve eksik dosyada hata | K2 keşif/puanlama, K3 canlı teknik doğrulama, K5 rapor; canlı kaynak/lisans ve gerçek skor eşdeğerliği eksik |
| `.github/workflows/altinci-aday-tekrar-test.yml` / `268e05a82df328090ccf61c6335197350df8b99b` | Manuel veya üç dosyada push; 20 dk timeout; mock HLS/ffprobe birim testi, RETEST_LIMIT=5, hata halinde TEKRAR_TEST_BEKLIYOR; CSV artifact if:always | K3 retest, K5 retry/rapor; HLS iki zamanlı süreklilik ve retry durumu için aynı girdili kanıt eksik |
| `.github/workflows/automatic-png-logos.yml` / `3d321b81f023647d1cd29c99f015d296a34df525` | Yalnız manuel; Pillow/CairoSVG ve ffmpeg ile görsel kanıt; CALISANLAR.m3u çalışma ağacı değişimini geri alır, stage değişimini reddeder; 30 günlük rapor artifact | K3 logo/EPG, K1 korunan yazma, K5 artifact; gerçek görsel kanıt ve tüm yan etkiler bağımsız doğrulanmadı |
| `.github/workflows/besinci-zaman-asimi-test.yml` / `d36327a5b8846deab730e02043b3abc6a689ca63` | Manuel veya iki dosyada push; subprocess.TimeoutExpired(timeout=65) mock; durum TEKRAR_TEST_BEKLIYOR, teknik değerler BELIRSIZ, yayın bozuk sayılmıyor | K3 teknik timeout, K5 retry kararı; gerçek timeout ve tekrar test artifact karşılaştırması eksik |

## Kabul sınırı

- Altı YAML'ın kaynak kimliği ve tetik/adım/artifact sözleşmeleri statik olarak karşılaştırıldı. Bu altı satır önceki 45 ayrıntılı statik incelemeye dahil olabilir; tekil kayıt mutabakatı yapılmadan **45/92** sayısı yükseltilmedi.
- 92 eski workflow'un envanter matrisi: `docs/K5_92_WORKFLOW_KAPSAM_KARSILASTIRMA_2026-10-23.md`.
- Bağımsız eski/yeni aynı-girdi run ID, input SHA256, çıktı/yan etki/timeout/retry/artifact SHA ve incelemeci onayı yok. **Davranışsal kabul 0/92**; üretim geçişi bloke.
- Üretim dosyalarına yazılmadı, workflow dispatch ve canlı cihaz testi yapılmadı.
