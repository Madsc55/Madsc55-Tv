# K5 — 10 ek workflow: gerçek yazma ve no-op davranış karşılaştırması

Tarih: 2026-10-23. Eski kaynak `Madsc55/madsc-tv` commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. On YAML doğrudan GitHub'dan okundu; sabit blob SHA doğrulandı. K aşamaları yalnızca **aday statik eşleştirme**dir.

| Sabit eski workflow / blob SHA | Aday K | Kaynak YAML sözleşmesi | Kabul boşluğu |
|---|---|---|---|
| `.github/workflows/madsc-documentation-check.yml` / `0678a8a201eb194503f9097265fe37e68b1e4d3d` | K1/K5 | Manuel; üç proje belgesi, Kural 25 ve playlist #EXTM3U doğrulaması | Doküman fixture eşdeğerliği |
| `.github/workflows/madsc-genis-kaynak-kontrol.yml` / `396d33dd8d5f3440dc81ae76abb91fc0d43f6a94` | K1/K2/K5 | Manuel; write yetkileri, 155 kaynak taraması, 5 push retry, ardından başka workflow dispatch | Yüksek risk: git push ve zincir dispatch, aynı-girdi izole kanıt yok |
| `.github/workflows/madsc-ibo-3-5281.yml` / `4b0745614a11625f020baa39b832983ce5fc42ca` | K1/K5 | Yalnız dry-run uyarısı; korunan playlist mutasyonu kapalı | No-op güvenli davranış korunmalı |
| `.github/workflows/madsc-ibo-530-archive.yml` / `85bb9898838d253c99bc10f7d98468d71a522a37` | K1/K4/K5 | 399–530 konum arşivi; CALISANLAR.m3u değiştirip main push | Üretim yazma engeli; 132 konum arşiv sınıflandırma fixture eksik |
| `.github/workflows/madsc-ibo-6115-second.yml` / `4591be38fed55b81e6bf8d3a22319c262f11c01b` | K1/K4/K5 | 6115 ikinci karar turu; playlist+arşiv+CSV+JSON commit ve push | Karar girdisi, SHA ve yan etki kanıtı eksik |
| `.github/workflows/madsc-ibo-ilk-239.yml` / `7cfc6061bb1714c08cd52ff130a54c36bcee15c7` | K1/K4/K5 | İlk 239 kullanıcı kararı; playlist ve arşiv raporu commit/push | 239 kararın onayı ve kayıpsız arşiv kanıtı eksik |
| `.github/workflows/madsc-ibo-kararlar-grup1.yml` / `d79a157a13c667d6dd60a0c4837cca2c1da4f220` | K1/K4/K5 | 36 çalışmayan Türk ve 197 yabancı IBO kararına dayalı arşiv; main push | Kullanıcı kararı kökeni, korunan yazma izni ve çıktı SHA eksik |
| `.github/workflows/madsc-ibo-second-voice.yml` / `ad14d3daf071f8503651581ba93f6b6008fa0aee` | K1/K4/K5 | 6115 ikinci sesli ayırma; playlist ve kayıpsız arşiv push | Girdi/yan etki ve ikinci sesli karar eşdeğerliği eksik |
| `.github/workflows/madsc-otomatik-devam.yml` / `4cf99f3ce1801588c24082c2122b1d781192e7dd` | K5 | Yalnız açıklama echo; yeni tur başlatmaz | No-op sözleşmesi ve çift tetikleme engeli |
| `.github/workflows/madsc-rule24-test.yml` / `8092ea97979380e7af71aaa9383dc28f41c86ab8` | K1/K5 | Ardışık hata güvenlik kapısı için unittest | Hata zinciri fixture eşdeğerliği |

## K5 kritik ayrım

- **Yazma riski:** `madsc-genis-kaynak-kontrol.yml` kaynak taramasından sonra `main` push ve `madsc-uc-asama.yml` dispatch eder. `madsc-ibo-530-archive.yml`, `madsc-ibo-6115-second.yml`, `madsc-ibo-ilk-239.yml`, `madsc-ibo-kararlar-grup1.yml`, `madsc-ibo-second-voice.yml` korunan `CALISANLAR.m3u` dosyasını git add/commit/push zincirine sokar. Bunlar **çalıştırılmadı**.
- **No-op korunmalı:** `madsc-ibo-3-5281.yml` ve `madsc-otomatik-devam.yml` fiilen uyarı/echo adımıdır; yeni sistemde yanlışlıkla gerçek playlist mutasyonuna veya ek tarama tetiklemeye dönüştürülmemelidir.
- **Eksik K5 fixture:** 399–530 arşiv konumları, 239 karar ve 6115 ikinci tur sözleşmeleri mevcut 354/364/398 salt-okunur önizlemesinden ayrıdır. Sayısal konumlar gerçek kanal kimliği, lisans veya kullanıcı onayı kanıtı değildir.

Bu 10 kaynak önceki statik incelemelerle çakışabilir; doğrulanmış 45/92 statik sayısı artırılmadı. Bağımsız eski/yeni run, aynı input SHA, artifact SHA, timeout/retry ve yan etki karşılaştırması **0/92 kabul**; üretim geçişi bloke. Korunan dosyalara yazılmadı.
