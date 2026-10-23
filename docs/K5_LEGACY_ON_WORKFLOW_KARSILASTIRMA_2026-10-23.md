# K5 — On eski workflow'un doğrudan YAML sözleşme karşılaştırması

Tarih: 2026-10-23. Kaynak: `Madsc55/madsc-tv` sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Aşağıdaki **10 eski YAML dosyası** doğrudan GitHub'dan okunmuş, blob kimlikleri envanterle eşleşmiştir. K aşaması karşılıkları statik adaydır; eski/yeni yürütme eşdeğerliği değildir.

| Eski workflow / blob SHA | Aday beşli aşama | Doğrudan YAML'da doğrulanan sözleşme | Kabul için eksik |
|---|---|---|---|
| `.github/workflows/birlesik-aday-raporu.yml` / `26c0cb7bfc5af366d462eeb72461fb4ca2f9ff23` | K2+K3+K5 | 60 dk; geçmiş cache, SCAN_BATCH=-1, gerçek ffprobe, ADAY_TEST_GRUBU=0, skor/istikrar, 4 artifact (30 gün) | cache geçmişi ve 4 artifact aynı-girdi eşdeğerliği |
| `.github/workflows/birlesik-durum-raporu.yml` / `cfd859aa1c5d474749edd09d99506b006ab0f82b` | K2+K5 | main push veya manuel; Python 3.11; 5 dk; akış testi başlatmadan 155 kaynak envanteri, eksik Türk kanal, haftalık bakım JSON'ları | 155 kaynak kapsamı ve dört raporun şeması |
| `.github/workflows/dokuzuncu-akilli-tekrar-test.yml` / `ad54773ea6d7bb46d0c5deb51454fe8189f87c32` | K3+K5 | push veya manuel; akıllı tekrar test takvimi unittest | takvim zamanlama fixture eşdeğerliği |
| `.github/workflows/epg-gunluk.yml` / `d43d5c469b54b8ef89794e8fcc2c2cee9b0d84b9` | K1+K3 | 03:25 UTC günlük cron veya manuel; contents:write; EPG XMLTV oluşturur, korunan yazma kapısı öncesi ve rebase sonrası; main'e push | gerçek üretim yazma yolu ve zamanlama güvenliği; canlı çalıştırma YASAK |
| `.github/workflows/epg-pages.yml` / `00e956c71c389d015209293b5de5b325cd4cb116` | K3+K5 | başarılı EPG workflow_run veya manuel; Pages deploy; pilot 5 kanal, XMLTV program kontrolü; yayın URL SHA256 eşitliğini 20 kez kontrol | Pages gerçek yayın ve artifact SHA eşdeğerliği |
| `.github/workflows/felaket-kurtarma-tatbikati.yml` / `53081c63ade88138049d8da1fef43ecfab588b5f` | K1+K4 | 8 dk; korunan listeler için geçici dry-run; DISASTER-RECOVERY-REPORT.json if:always ve eksikse hata | harici yedek ve bağımsız geri yükleme hash zinciri |
| `.github/workflows/genel-aday-medya-test.yml` / `8d313fa5936799f86fd026831a3a149cbb0c250b` | K2+K3 | 40 dk; SCAN_BATCH=-1; ADAY_TEST_GRUBU=0; gerçek ffprobe; CSV+JSON 30 gün | gerçek lisans/köken, canlı A/V ve rapor karşılaştırması |
| `.github/workflows/genis-kanal-tarama.yml` / `ffea4c826bf1ea9f2b586ddbd279d169f930b9b1` | K2+K3 | 55 dk; main komut push veya manuel; çok kaynaklı tarama; CSV artifact if:always | gerçek kaynak/keşif ve hata halinde artifact eşdeğerliği |
| `.github/workflows/ibo-bagimsiz-test-listesi.yml` / `be63acf659a9b50c68a8b01ff5434a3151877a8f` | K2+K3 | 40 dk; gerçek medya testi; izole IBO M3U + CSV + JSON, 30 gün | cihaz testi en son; bağımsız liste hash/kimlik eşdeğerliği |
| `.github/workflows/ibo-epg-kimlik-denetimi.yml` / `67ffc18c6cd79a5ea0960de72aeeecbc98fab7d7` | K1+K3 | 10 dk; CALISANLAR.m3u ile beş kanal XMLTV kimlik eşleştirme; runner temp JSON, 14 gün | canlı XMLTV kimlik ve korunan liste SHA kanıtı |

## Risk ve kabul

**Kritik yazma riski:** `epg-gunluk.yml` gerçek `contents: write`, commit ve `git push` içerir. Salt-okunur statik inceleme dışında **dispatch edilmedi**. `epg-pages.yml` dış Pages yayını yapar ve yayın SHA kontrolü içerir; o da çalıştırılmadı.

Bu kaynak incelemesi, çağrılan script'lerin tüm yan etkilerini veya gerçek yayın/CI sonuçlarını doğrulamaz. Önceki 45/92 ayrıntılı statik inceleme ile örtüşme olabileceği için sayı **45/92** olarak korunur. Aynı-girdi bağımsız eski/yeni koşu ve artifact SHA kanıtı **0/92**; üretim kabulü **verilmedi**. Korunan playlist, EPG, logo ve yedeklere yazılmadı.
