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
