# K2–K3 devir notu — 2026-10-22

Kapsam: K2 uzak M3U keşfi ile K3 HTTPS HLS manifest pilotunun salt-okunur kanıt eşleştirmesi. Diğer üç sohbet doğrudan kilitli/bağlı değildir; koordinasyon GitHub main HEAD ve dosya SHA ile yapılır. Korunan canlı listeler, FAVORILER, YEDEKLER, EPG/XMLTV, cihaz verileri, PR #71 değiştirilmedi.

## Bu sohbetin kayıtları
02acf7f4: manuel online evidence join workflow; b7b50b79: kaynak SHA ve eşleştirme; 4ca79052: 2 MB kaynak sınırı; 0e44eac9: aday dolaşımı; b04862b4: kaynak regresyonları; ea549dbc: test satır sonları; d56610a0: URL tekilleştirme; 5989487a: tekrar regresyonu; 4b87b25f: test satır sonu düzeltmesi; debc4025: K3 kimliğini K2 normalize_url ile hizalama; d686a73e: 12 probe sınırı testine 25 ayrı URL.

## Doğrulama ve açık işler
- Son değişikliklerin offline testlerinin başarılı koştuğu bu sohbet içinde doğrulanmadı; GitHub Actions dispatch yapılmadı.
- K2/K3 harici kaynağı ayrı indiriyor; değişen kaynak SHA uyuşmazlığı yaratabilir. Aynı boyut sınırlı snapshot'u iki pilota verme tasarımı değerlendirilmeli.
- K2 ilk 100 satırı değerlendiriyor, K3 en fazla 12 benzersiz URL'yi sondalıyor. Reconcile kesişimi üretim/cihaz/oynatma onayı değildir.
- K5 gerçek kanıt aktarımı, 92 eski workflow davranış eşdeğerliği, 26 güvenlik kuralı, 22 kurulum görevi, IBO cihaz testi henüz bu sohbet tarafından doğrulanmadı.
- Paralel K2/K4 DEVAM_NOTU.md kaydında 816 testlik tam kapıda 5 failure + 3 error olduğu belirtiliyor. Diğer sohbetin sahip olduğu dosyalara dokunma.
- Yeni sohbette güncel main, YENI_SOHBET_DEVIR_2026-10-22.md ve DEVAM_NOTU.md okunmalı; gerçek offline testler çalıştırılmalı; sadece kanıtlanmış sonuçlar aktarılmalı. [skip ci] kullan, Actions tetikleme.

## Birleştirme öncesi güncel devir — 2026-10-22 gece

Bu bölüm önceki tarihsel notu günceller: K2 ve K3 artık `--source-file` destekliyor; manuel `.github/workflows/madsc-online-evidence-join.yml` tek ve 2 MB ile sınırlandırılmış M3U snapshot'u indirip iki pilota veriyor. Kaynak SHA-256 ve bayt sayısı eşleşmeden `madsc.online_evidence_reconcile` kabul etmiyor. Workflow **dispatch edilmedi**.

### Bu sohbetten sonraki doğrulanmış GitHub commitleri
- `79e00d8`: ilk K2–K3 koordinasyon notu.
- `5a12e76`: K2 `--source-file` ve kaynak boyutu/symlink kontrolü.
- `000af6c`, `4842c19`: ortak snapshot testleri ve birleştirici uçtan uca regresyon taslağı.
- `ffef077`, `28d6f1f`, `90cc2fe`: kaynak bayt sayısı bütünlüğü ve test fixtürleri.
- `16b169a`, `f580ac8`, `65027d9`: K3 probe/manifest sayacı tutarlılığı ve sınır testleri.
- `3a210ef`, `46f1f9d`, `ab971e3`: sahte oynatma/cihaz doğrulaması iddialarını reddetme ve fixtür güncellemesi.
- `a2fd8b9`: ortak snapshot testindeki eksik K2 doğrulama bayrakları.
- `a11e67a`: K2–K3 kanıt JSON dosyalarını O_NOFOLLOW, fstat ve 2 MB sınırıyla okuma.
- `4d2213b`: symlink, dizin ve büyük kanıt girdisi regresyonları.
- `10d5bf0`: geçersiz dosya açma hatalarını ValueError olarak raporlama.
- `cf0aa97`: eksik kanıt dosyası regresyonu.
- `2c3a3b1`: K3 `audio_video_verified=False` değerinin Python'da `0` gibi kabul edilmesini engelleme.
- `5d7935b`: boolean doğrulama sayacı regresyon testi. Bu sohbetin son kaydedilmiş kod/test commit'i.

### Gerçek durum / yapılacaklar
1. **Yeni sohbet başlangıcı:** `main` HEAD ve `DEVAM_NOTU.md`, `YENI_SOHBET_DEVIR_2026-10-22.md`, bu dosya ile ilgili son commitleri yeniden oku. Paralel sohbetler HEAD'i değiştiriyor; bu listedeki commitleri en yeni HEAD sanma.
2. **Önce test:** `python -m unittest tests.test_online_evidence_reconcile tests.test_k2_k3_shared_snapshot tests.test_k3_live_manifest_source_snapshot tests.test_online_evidence_join_workflow` (gerekirse discovery yolu ile). Testler bu sohbet içinde **çalıştırılıp geçti diye doğrulanmadı**. Son eklenen `False` sayacı ve eksik kanıt dosyası regresyonları da koşulmalı.
3. **K2/K3 açık mantık kontrolleri:** K2 `accepted`, `pilot_evaluated`, `duplicates`, `rejected` sayaçlarının hash listesiyle tutarlılığını değerlendir; K3 manifest işaretinin `https_reachable` ile tutarlılığını ve K2 ilk 100 satır / K3 12 probe kapsam uyumunu kontrol et. Yeni katı kontrollerden önce mevcut test fixtürlerini güncelle.
4. **K5 gerçek kanıt tüketimi:** birleşik K2/K3 JSON'un K5 tarafından gerçekten alınıp işlendiğini test et; yalnız `evidence_only` sonucu üretim veya cihaz onayı değildir. Beşli K1–K5 uçtan uca kabul, 92 eski workflow davranış eşdeğerliği, 26 güvenlik kuralı, 22 kurulum görevi ve IBO cihaz doğrulaması tamamlanmış sayılmamalı.
5. **Koruma/koordinasyon:** korunan canlı playlistler, FAVORILER, YEDEKLER, EPG/XMLTV, cihaz favorileri, logolar, yedekler, PR #71 ve üretim verilerine dokunma; Actions dispatch etme. Sohbetler doğrudan senkronize değil: her yazımdan hemen önce güncel dosya SHA'sını çek, 409 çatışmasında yeniden oku ve değişiklikleri uzlaştır, üzerine yazma. `[skip ci]` kullan.

Not: Başka sohbetlerin test/commit iddiaları bu sohbet tarafından bağımsız doğrulanmadı; yeni sohbette GitHub'ın güncel durumunu esas al.
