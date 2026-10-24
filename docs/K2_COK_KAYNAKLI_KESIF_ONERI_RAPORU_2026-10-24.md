# K2 — Çok kaynaklı keşif öneri raporu (24 Ekim 2026)

**Dal:** `k2/multisource-discovery-evidence-20261024`  
**Durum:** Salt okunur, inceleme önerisi; hiçbir kanal otomatik eklenmedi.

## Kapsam ve kanıt sınırları
- Resmî yayıncı sayfaları, lisansı açık M3U/M3U8 katalogları, TV rehberleri, resmî YouTube canlı sayfaları ve ücretsiz lisanslı platformlar için **offline aday sınıflandırma** eklendi.
- Kaynak sayfası / yayın URL'si / hak kanıtı ayrı tutuluyor. Bir web sayfasının herkese açık olması yeniden dağıtım izni anlamına gelmez.
- Aynı yayın URL'si ve mevcut URL envanteri karşılaştırılarak tekrarlar eleniyor; farklı URL'lerin aynı yayını taşıyabileceği için operatör bağımsızlığı kanıtlanmış sayılmıyor.
- Gerçek oynatma, çözünürlük, codec, DRM veya lisans doğrulaması yapılmadı; raporda bu alanlar **false**. Üretim yazımı kapalı.

## Araştırılmış aday kaynaklar — doğrulama bekleyen başvurular

| Kaynak | Tür | Kamuya açık kanıt | Değerlendirme |
|---|---|---|---|
| SVT Play | Resmî yayıncı | https://www.svt.se/kontakt/ljud-och-bildkvalitet-pa-svt-play | Resmî teknik belge canlı yayınlarda HLS/DASH ve 720p/1080p profillerini tanımlar. Tekil kanalın mevcut çözünürlüğü veya yeniden dağıtım hakkı **doğrulanmadı**. 4K için canlı yayın kanıtı yok. |
| MDR Fernsehen | Resmî yayıncı | https://www.mdr.de/tv/empfang/faq-tv-livestreaming-mdr-100.html | Resmî site ücretsiz HLS canlı yayınlarını açıklar. Kanal URL'si, codec, gerçek çözünürlük ve yeniden dağıtım hakkı **doğrulanmadı**. |
| MAVISE | Yayıncı/operatör rehberi | https://mavise.obs.coe.int/advanced-search | Düzenleyici envanteri; yayın URL'si ve yeniden dağıtım izni sağlamaz. |
| Doubo TV metadata | TV dizini | https://doubo.tv/en/data/free-tv-channels/ | Kanal kimliği ve resmî web sitesi eşleştirmesi için olası kaynak; veri setinde yayın URL'si yok. |
| Teleonline | Toplu liste | https://github.com/teleonline/listas/blob/main/README.en.md | Proje resmî/izinli kaynak kullandığını beyan ediyor; tekil yayın hakları bağımsızca doğrulanmadı. |
| OpenIPTV | TV izleme dizini | https://openiptv.org/about | Üçüncü taraf HLS/YouTube embed kullanır; kendi açıklaması yeniden dağıtım iznini garanti etmediğini belirtir. |

## 1.039 girdilik liste ve kalite alternatifleri

**Mevcut liste içeriği ve 1.039 sayısı bu dalda kaynak dosya üzerinden doğrulanamadı.** Bu nedenle kanal bazında eksik kanal, 720p/1080p/4K alternatif, codec ve gerçek akış sonuçları üretilmedi. Bunlar için yalnız yetkili/izinli envanterin salt okunur kopyası, hak kanıtı ve açık izinli teknik ölçüm gerekir. Bir platformun genel 1080p profili, listedeki tekil kanalın 1080p olduğunu göstermez.

## Kabul ve sonraki adım
1. Korumalı playlist'e dokunmadan, salt okunur envanterin URL hash'leri ve tvg-id'leriyle eşleştirme.
2. Her aday için yayıncı resmî kaynak sayfası ve yeniden dağıtım izni belgesini bağımsız doğrulama.
3. Yalnız açıkça izinli URL'lerde ffprobe/ffmpeg ölçümü; ölçüm UTC zamanı, gerçek video boyutu, codec, örnek sayısı ve kaynak hash'i.
4. K2→K3 üç ayrı gerçek ölçüm ve IBO Player Pro cihaz kabulünü ayrı kanıt kapısı olarak tutma.

**Sonuç:** Kod düzeyinde çok kaynaklı, güvenli ve otomatik ekleme yapmayan keşif ön elemesi hazır. Gerçek kanal kalite iyileştirmesi, lisans, canlı doğrulama ve üretim kabulü **tamamlanmadı**.
