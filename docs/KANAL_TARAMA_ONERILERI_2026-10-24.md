# MADSC55 TV — 04:30 kanal/kalite taraması, ayrı öneri raporu

**Tarih:** 24 Ekim 2026 (Europe/Stockholm). **Depo HEAD:** `9ae8d0cf427e8e13d380f1dc706a340270ce59e2`. **Kapsam:** salt okunur M3U envanteri, K3 devir ve kanıt planı, resmî yayıncıların açık canlı izleme sayfaları. **Kabul:** YOK.

## Ölçülen envanter
- M3U `#EXTINF` girdisi: **1039**; farklı yayın URL'si: **376**; farklı görünen kanal etiketi: **382**; farklı `tvg-name`: **357**. Bunlar farklı yayıncı/kanal sayısı değildir; gruplar ve varyantlar yinelenir.
- Kanal adında **1080p etiketi 501**, **1440p etiketi 45**, **720p etiketi 386**, **4K/2160p etiketi 0**. Kalan 107 girdide SD/HD, başka çözünürlük veya çözünürlük yok. **Etiket ≠ gerçek yayın çözünürlüğü.**
- Aynı, boş olmayan `tvg-id` ve farklı URL altında daha yüksek çözünürlük **etiketi** bulunan **159 giriş** tespit edildi. Bunların **134 tanesinde** en az bir daha yüksek etiketli aday HTTPS ve erişim-belirteci biçimli yol filtresinden geçiyor; yine de **yayıncı yetkisi, codec ve kalite doğrulanmadı**. Her girdinin karşılığı ek envanterde yer alıyor.
- `http://` kullanılan **255 giriş** var; **194 giriş / 64 farklı URL** erişim belirteci olabilecek uzun yol parçaları içeriyor. Bunlar otomatik denenmeyecek, günlükte veya raporda tam URI olarak gösterilmeyecek.
- Resmî canlı sayfa varlığı bir HLS URL'sinin yeniden dağıtım/playlist kullanımına izin verildiği anlamına gelmez.

## Öncelikli kalite karşılaştırmaları (etiket bazlı, doğrulanmadı)
| Daha düşük etiket | Aynı tvg-id'deki yüksek etiket | Sonuç |
|---|---|---|
| TRT 1 5 720p | TRT 1 1440p | Yalnızca liste içi etiket farkı; resmî TRT manifesti/codec okunamadı |
| TRT HABER 4 720p | TRT HABER 1440p | Etiket farkı; 1440p kanıtlanmadı |
| NOW 2 720p | NOW 1080p | Etiket farkı; resmî kaynak/lisans doğrulanmadı |
| NTV 6 576p | NTV 1080p | Etiket farkı; gerçek video/codec bilinmiyor |
| ATV 6 360p | ATV 1080p | Etiket farkı; gerçek video/codec bilinmiyor |
| SHOW TV 4 720p | SHOW TV 1080p | Resmî canlı sayfa mevcut; M3U hakları ve manifest doğrulanmadı |
| TRT ÇOCUK 4 720p | TRT ÇOCUK 1 1440p | Etiket farkı; gerçek video/codec bilinmiyor |
| TRT MÜZİK 3 720p | TRT MÜZİK 1 1440p | Etiket farkı; gerçek video/codec bilinmiyor |

## Eksik kanal adayları (ekleme yok)
- **SÖZCÜ TV:** mevcut M3U kanal adları ve `tvg-name` alanlarında birebir eşleşme yok. Yayıncı canlı sayfası: https://www.sozcu.com.tr/sozcu-tv-canli-yayin-wp7630113 . HLS, çözünürlük, codec, playlist kullanım izni doğrulanmadı.
- **Euronews Türkçe:** mevcut M3U adlarında birebir eşleşme yok. Yayıncının Türkçe canlı sayfası: https://tr.euronews.com/live . HLS, çözünürlük, codec ve yeniden dağıtım izni doğrulanmadı.
- **TRT SPOR** ve **TRT 3** adlarıyla birebir eşleşme yok; **TRT SPOR YILDIZ** mevcut. Bu iki ad, güncel resmî yayın/dağıtım statüsü ayrıca teyit edilmeden 'eksik aktif kanal' sayılmamalıdır.
- BBC News, DW Türkçe, France 24, Al Jazeera English, NASA TV gibi uluslararası adlar da birebir bulunmadı; kullanıcı hedef kapsamı ve lisanslı playlist akışı bilinmediğinden yalnızca olası kapsam genişletme fikirleridir.

## Resmî kaynak incelemesi
- TRT 1: https://www.trt1.com.tr/Canli-izle
- TRT Haber: https://www.trthaber.com/canli-yayin-izle.html
- Show TV: https://www.showtv.com.tr/canli-yayin
- SÖZCÜ TV: https://www.sozcu.com.tr/sozcu-tv-canli-yayin-wp7630113
- Euronews Türkçe: https://tr.euronews.com/live

Bu sayfalar canlı izleme imkânına işaret eder; bu turda resmî HLS master playlist içeriği ve medya segmentleri **okunamadı**. Ağ erişimi sırasında resmî TRT manifest adresine yapılan salt okunur GET, DNS çözümlenemediği için sonuç vermedi. Diğer belirsiz/kimlik bilgisi biçimli URL'lere istek yapılmadı. **Doğrulanmış 720p/1080p/4K yeni URL sayısı: 0; doğrulanmış video/ses codec sayısı: 0.**

## K3 kabul kapıları
K3 devir ve `docs/K3_EVIDENCE_PLAN_2026-10-24.md` uyarınca: resmî yetki/köken, HTTPS master manifestin çözünürlük ve CODECS alanları, izinli kısa ses/video kanıtı, XMLTV eşleşmesi, en az 6 saat aralıklı bağımsız süreklilik ölçümleri ve en sonda IBO Player Pro cihaz kabulü açık. Otomatik ekleme, ana listeye yazma, canlı görev dispatch, DRM aşma ve yetkisiz URL testi yok.

## K1–K5 kısa koordinasyon durumu
- **K1:** dosya yazma güvenlik/regresyon çalışmaları var; çalışma zamanı nihai kabulü doğrulanmadı.
- **K2:** CRLF keşif düzeltmesi ve offline regresyon kanıtı var; gerçek kaynak keşif kabulü ayrı.
- **K3:** PR #10 offline CI başarılı, canlı HLS/codec/XMLTV/süreklilik/cihaz kabulü açık.
- **K4:** fixture-only güvenlik PR'ları ana dala alınmış; yetkili dış yedek ve bağımsız restore kanıtı açık.
- **K5:** kaynak envanteri 92/92; önceki merkez raporunda doğrudan YAML incelemesi 20/92 ve davranışsal kabul 0/92; canlı/üretim eşdeğerliği iddia edilmiyor.
- **CI:** en son görülen başarılı main CI #40049105625, SHA `22834dfcb9e36cdb72644507eefa61102623c564`. Bu raporun baz aldığı `main` daha yeni: `9ae8d0cf427e8e13d380f1dc706a340270ce59e2`; aynı HEAD için başarı kanıtı yok. `main` koruması açık sorun #13.
- **Açık PR:** #1, #2, #3, #6, #7, #10, #12 (7 adet); #12 iki CI koşusunda başarılı fakat taslak ve birleştirilmedi.

## Sıradaki işler
1. Resmî kaynak sahipliği ve M3U kullanım iznini tek tek belgelemek.
2. İzinli HLS manifestinden `RESOLUTION`, `CODECS`, `BANDWIDTH` alanlarını kanıtla; etiketleri gerçek değerlerle karşılaştır.
3. Önce aynı kanala ait 159 düşük etiketli girdinin mevcut alternatiflerini, ardından gerçekten eksik resmî kanalları izole pilotta denetle.
4. EPG/kimlik eşleşmesi, uzun süreli ses/video ve cihaz kabulünü birbirinden ayrı kaydet.
5. Hiçbir kanalı doğrulama/izin olmadan üretim listesine ekleme; mevcut kanalları otomatik silme.

**Ayrıntılı satır-satır envanter:** `docs/KANAL_KALITE_ENVANTERI_2026-10-24.md`. Kaynak URL'leri ve olası erişim belirteçleri rapora kopyalanmadı.
