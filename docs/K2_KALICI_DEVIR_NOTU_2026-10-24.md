# K2 — Kalıcı çalışma ve devir notu (24 Ekim 2026)

## Doğrulanmış kaynak ve sayımlar
- Kaynak: `main:MADSC55_TV_IBO_CALISANLAR_TEST.m3u8`; salt okunur metin analizi.
- 1.039 `#EXTINF` kaydı ve 1.039 HTTP(S) yayın URL satırı.
- 376 benzersiz tam URL; 663 yinelenen URL satırı.
- 382 benzersiz görünen ad; 657 yinelenen ad kaydı.
- 708 dolu `tvg-id` kaydı, bunlarda 106 benzersiz kimlik; 331 boş/eksik `tvg-id`.
- 784 HTTPS ve 255 HTTP yayın adresi satırı.
- `tvg-logo` ve `group-title` alanlarının varlık kontrolünde boş/eksik alan sayısı sıfır; erişilebilirlik/semantik doğrulama yapılmadı.
- Sayılar tam metin eşitliği ve alan varlığına dayanır; 1.039 bağımsız yayın, 376 çalışan kaynak veya 106 gerçek kanal iddiası değildir.

## K2 kod ve PR
- Dal: `k2/multisource-discovery-evidence-20261024`; taslak PR: https://github.com/Madsc55/Madsc55-Tv/pull/18
- `madsc/multisource_discovery.py`: yalnız çevrimdışı aday ön elemesi, güvenli URL/ad kontrolleri, tekrar ayırımı; lisans/kalite/canlı durum için doğrulanmamış bayraklar.
- `tests/test_multisource_discovery.py`: regresyon testleri.
- Önceki doğrulanmış bütünleşik CI: https://github.com/Madsc55/Madsc55-Tv/actions/runs/40072347524 ; commit `4e5e7cdc1dc72fab9b774075758ab1fad47937c5`, **başarılı**.
- Envanter raporu commitleri `ce3eed3`, `6d7724a` için görülen CI çalışmaları **iptal**; bunları başarılı sayma.
- Yeni workflow ekleme: korumalı 92 workflow envanterini bozduğu için geri alındı.

## Eksikler ve kabul kapıları
1. Her kanal için ad, URL, `tvg-id`, grup ve varyant ilişkisini salt okunur eşleştir; aynı URL/ad/id otomatik silme gerekçesi değildir.
2. 255 HTTP satırı için güvenli HTTPS alternatifleri ancak resmî kaynak ve yayın hakları kanıtıyla değerlendir; otomatik URL değiştirme.
3. 331 boş/eksik `tvg-id` için güvenilir EPG kimlik eşleştirmesi; tahmini ID atama yok.
4. Hak/yeniden dağıtım iznini tekil kaynak bazında doğrula; herkese açık yayın yeniden dağıtım izni değildir.
5. Yalnız izinli akışlarda ölçüm (çözünürlük, codec, UTC zaman damgası, örnek sayısı, kaynak hash'i); canlı oynatma, DRM, cihaz/K3 kabulü ayrı kapılardır.
6. En son PR HEAD üzerinde bütünleşik CI başarısını doğrula; başka çalışma dalı güncellerse eski HEAD'e yazma.

## Güvenlik ve değişiklik sınırı
- Ana dal, üretim playlist/EPG/logo/favoriler, yedekler ve cihaz verileri değiştirilmez.
- Yetkisiz yayın isteği, DRM atlatma, otomatik kanal ekleme ve üretime birleştirme yapılmaz.
- Bu not salt okunur inceleme ve K2 devri içindir; gerçek canlı kanal doğrulaması yapılmış gibi sunulamaz.
