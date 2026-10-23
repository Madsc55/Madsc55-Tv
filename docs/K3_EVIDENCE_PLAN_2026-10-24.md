# K3 EPG / HLS Denetim Kanıt Planı — 2026-10-24

Durum: K3-13 AÇIK; bu belge test sonucu veya canlı yayın kabulü değildir.

İncelenen main blob'ları:
- madsc/epg.py: abc8bbf1842b6bfd6f37c4b5d35132e296060eca
- tests/test_epg.py: b678eae7158551c1fc910c3c8009476a1e762187

## Ayrı doğrulama katmanları
1. Offline: `python -m unittest tests.test_epg -v` ve proje genel regresyon kapısı. Komutun gerçek çıkış kodunu ve commit SHA'sını kaydet.
2. M3U: malformed EXTINF, duplicate header, missing URI, invalid scheme/port, duplicate tvg-id. Hatalar fail-closed kalmalı.
3. XMLTV: root, duplicate/missing channel id, missing programme channel, unmatched references, XML entity/DOCTYPE reddi.
4. Canlı pilot: yalnız yetkili, zararsız okuma ile HTTPS manifest erişimi, segment video/ses kanıtı, yönlendirme ve hata günlükleri. Kimlik bilgilerini loglama.
5. Süreklilik: bağımsız zaman damgalı >=6 saatlik ölçüm; kısa probe veya CI ile ikame etme.
6. Pages/XMLTV/logo: yayınlanan gerçek URL ve kanal kimliklerinin karşılıklı tutarlılığını doğrula.
7. Son kabul: IBO Player Pro kullanıcı cihaz testi en son; kullanıcıdan şimdi isteme.

## İnceleme bulgusu / takip
- `check_epg_mapping` yapısal eşleşme sonucunu `matching_verified` ile, cihaz kabulünü `device_verified=False` ile ayrı tutuyor.
- `urlsplit` sözdizimsel URI denetimidir; erişilebilirlik/oynatma kanıtı değildir.
- Testler bu belge oluşturulurken çalıştırılmadı. Güncel main için başarılı CI kanıtı bu turda teyit edilmedi.

## Koruma
Üretim playlist, XMLTV, logo, favori, yedek, arşiv ve cihaz verilerini değiştirme. PR #71'i birleştirme. K1/K2/K4/K5 kapsamına dokunma. K3-13'ü canlı ve cihaz kanıtları tamamlanana dek açık tut.
