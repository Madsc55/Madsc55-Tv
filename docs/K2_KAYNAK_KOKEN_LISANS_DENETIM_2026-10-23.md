# K2 — Kaynak kökeni, lisans ve keşif davranışı denetimi (23 Ekim 2026)

## Denetim kapsamı ve sınırlama
Bu belge üretim kanallarını veya URL'leri doğrulanmış saymaz. İnceleme yalnızca depo içindeki K2 keşif mantığı ve kamuya açık kaynakların beyanları üzerindedir. Canlı IPTV URL isteği, ffprobe, üretim yazımı, yayınlama veya workflow tetikleme yapılmadı.

## Kamuya açık örnek: iptv-org/iptv
- Proje: https://github.com/iptv-org/iptv
- Kaynak beyanı: README, bağlantıların kullanıcılarca sağlandığını; akışları barındırmadığını ve hedef sunucuları kontrol etmediğini bildirir.
- Kod/veri deposu lisans beyanı: README CC0 rozeti gösterir; ancak bağlantıdaki LICENSE dosyası açıkça **The Unlicense** metnini içerir. Bu dosya tek tek üçüncü taraf yayınların yeniden dağıtım, gösterim veya ticari kullanım haklarını **kanıtlamaz**.
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


## 23 Ekim 2026 — Kamuya açık birincil kaynak kontrolü

Kaynaklar: https://github.com/iptv-org/iptv/blob/master/README.md ve https://github.com/iptv-org/iptv/blob/master/CONTRIBUTING.md ve https://github.com/iptv-org/iptv/blob/master/LICENSE

| Kanıt / iddia | Doğrulanan durum | K2 kararı |
| --- | --- | --- |
| Playlist yayımlayıcısı | `iptv-org/iptv` deposu, kullanıcı katkılı bağlantı listesi olduğunu kendi README'sinde bildiriyor | **Liste yayımlayıcısı belirli** |
| Tekil yayın sunucusunun işletmecisi | README, bağlantıların hedefini kontrol etmediğini açıkça bildiriyor | **Doğrulanmadı** |
| Depo lisansı | README CC0 rozeti gösteriyor; doğrudan incelenen LICENSE dosyası **The Unlicense** metnidir. Bu tutarsızlık kaynak lisans kanıtında ayrıca not edilmiştir; üçüncü taraf yayın haklarını kapsadığı varsayılamaz | **Depo lisans beyanı mevcut; yayın lisansı değil** |
| Tekil akış yeniden dağıtım izni | README/CONTRIBUTING, her akış için hak sahibinden yazılı izin sunmuyor | **Doğrulanmadı** |
| Akışların çalışma durumu | CONTRIBUTING katkıcıların akış stabilitesi, coğrafi kısıt ve token kontrolü yapmasını istiyor; bu, bu denetimde bağımsız teknik örnek alındığı anlamına gelmez | **Doğrulanmadı** |
| Farklı feed bağımsızlığı | Aynı organizasyondaki playlist, database, API ve site birbirine bağlı veri ürünleri olabilir | **Bağımsız kaynak olarak sayılamaz** |

**Lisans ayrımı:** CC0/Unlicense gibi depo lisans beyanları, üçüncü taraf yayın hak sahibinin akışın yeniden dağıtımına izin verdiğini ispatlamaz. Kamuya açık erişim, hak sahipliği ve lisans uygunluğu birbirinden ayrı üç iddiadır.

**Keşif kabul testi sözleşmesi:** Yerel/izinli M3U metni ile `parse_m3u` ve `corroborate_sources` çalıştırılmalı; girdinin SHA-256'sı, UTC zaman damgası, kaynak sahibi, parse_errors/rejected/duplicates ve aynı envanterin tekrar sayılmadığı kaydedilmelidir. Testte ağ isteği veya üretim playlist yazımı yapılmamalıdır. Bu çalıştırma bu denetim sırasında yapılmadı; CI yeşil veya canlı yayın çalışıyor denemez.

**Sonuç:** Bu örnekte sadece liste yayımlayıcısının kamuya açık beyanı doğrulandı. Tekil yayınların kökeni, kullanım lisansı ve çalışma durumu **kanıtlanmadı**; K2 kabul kapısı kapalı kalır.


## 23 Ekim 2026 — Lisans dosyası doğrudan karşılaştırması
- Birincil kaynak README: https://raw.githubusercontent.com/iptv-org/iptv/master/README.md — son satırdaki lisans rozeti **CC0** etiketli.
- Birincil kaynak LICENSE: https://github.com/iptv-org/iptv/blob/master/LICENSE — dosya **The Unlicense** metnini içerir ve unlicense.org adresine yönlendirir.
- **Kanıt uyuşmazlığı:** Rozet CC0, LICENSE metni Unlicense. Depo lisansını tek ve tartışmasız bir CC0 lisansı olarak sınıflandırma; dosya metni ile README işaretini ayrı sakla. Bu durum tekil üçüncü taraf yayınların kullanım haklarını zaten doğrulamaz.
- Bu incelemede yayın URL'lerine erişilmedi; yalnızca kamuya açık proje belge sayfaları okundu. Teknik yayın doğrulaması ve yayıncı yazılı izni hâlâ bekliyor.
