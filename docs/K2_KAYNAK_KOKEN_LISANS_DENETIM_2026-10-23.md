# K2 — Kaynak kökeni, lisans ve keşif davranışı denetimi (23 Ekim 2026)

## Denetim kapsamı ve sınırlama
Bu belge üretim kanallarını veya URL'leri doğrulanmış saymaz. İnceleme yalnızca depo içindeki K2 keşif mantığı ve kamuya açık kaynakların beyanları üzerindedir. Canlı IPTV URL isteği, ffprobe, üretim yazımı, yayınlama veya workflow tetikleme yapılmadı.

## Kamuya açık örnek: iptv-org/iptv
- Proje: https://github.com/iptv-org/iptv
- Kaynak beyanı: README, bağlantıların kullanıcılarca sağlandığını; akışları barındırmadığını ve hedef sunucuları kontrol etmediğini bildirir.
- Kod/veri deposu lisans beyanı: README'deki LICENSE bağlantısı (CC0/Unlicense göstergeleri); bu lisans tek tek üçüncü taraf yayınların yeniden dağıtım, gösterim veya ticari kullanım haklarını **kanıtlamaz**.
- Sonuç: **Liste kökeni kamuya açık, tekil yayın kökeni/lisansı doğrulanmamış.** K2 kabulüne veya otomatik üretim yayınına yükseltilemez.
- İnceleme referansları: https://github.com/iptv-org/iptv/blob/master/README.md ; https://github.com/iptv-org/iptv/blob/master/CONTRIBUTING.md

## K2 keşif davranışı (kod incelemesi)
- `madsc/discovery_batch.py:parse_m3u`: yerel M3U metnini okur, metadata ve URL adaylarını ayrıştırır; ağ isteği yoktur.
- `corroborate_sources`: kaynak adlarını ve semantik liste envanterlerini karşılaştırır; aynı/mirror envanterleri bağımsız oy saymaz.
- `source_count`: **farklı semantik envanter sayısıdır**; gerçek yayıncı, mülkiyet veya lisanslı bağımsız kaynak sayısı değildir.
- `source_independence_verified=False`, `live_verified=False`, `production_writes=False`: bu durumlar bilinçli olarak korunmalıdır.
- `build_m3u8_preview`: yalnızca bellek içi `TEST_BEKLIYOR` taslağı üretir; üretime yayın yapmaz.
- Liste URL'sinin herkese açık olması ve HTTP 200 dönmesi hak sahipliğini veya yeniden dağıtım iznini kanıtlamaz.

## Gerçek kaynak kabulü için gerekli kanıt alanları
Her kaynak için aşağıdakiler bağımsız kanıt bağlantılarıyla ve kontrol tarihiyle kaydedilmelidir:
1. Listeyi yayınlayan kuruluş, resmi site ve liste URL'sinin bu kuruluşa bağlandığı kanıt.
2. Akışın gerçek yayıncısı/hak sahibi ve varsa resmi yayın sayfası.
3. İçeriğe özel kullanım, indeksleme, yeniden dağıtım ve ticari kullanım izinleri; coğrafi ve süre sınırları.
4. Lisans belgesinin açık bağlantısı veya hak sahibinin yazılı izni; belge kapsamının **tekil akışı** içerdiği kanıt.
5. Liste/akışın upstream/fork/mirror ilişkisi, yayıncı sahipliği ve bağımsız işletmeci kanıtı.
6. Teknik keşif örneğinin zamanı, kaynak SHA-256'sı, hata/aday/tekrar sayıları; kişisel token ve sırlar rapora yazılmamalı.
7. K3'e devir için ayrıca üç teknik örnek (en az altı saat aralıklı), ffprobe/ffmpeg çıktısı ve kullanıcı cihaz kabulü.

## Kabul kararı
- Kaynak kökeni: **DOĞRULANMADI** (tekil gerçek kaynak işletmecisi için kanıt yok).
- Akış kullanım/yeniden dağıtım lisansı: **DOĞRULANMADI**.
- Kaynak bağımsızlığı: **DOĞRULANMADI** (envanter farkı bağımsızlık değildir).
- Keşif kodunun salt okunur mimarisi: **STATİK OLARAK İNCELENDİ**; güncel CI/test sonucu ayrıca gereklidir.
- Gerçek keşif yürütümü: **YAPILMADI**; gerçek feed girdisi ve izin verilmiş gözlem kaydı yok.
- K2→K3 canlı kabul: **BEKLİYOR**.

Bu alanlar kanıtlanmadan kaynak veya kanal `verified`, `licensed`, `independent` veya `production_ready` olarak işaretlenmemelidir.
