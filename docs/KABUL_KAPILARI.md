# Kabul kapıları — başlangıç durumu

Bu sürüm yalnız izole ve salt-okunur iskelet oluşturur. Beş kategori rapor üretir, gerçek kanal aramaz/test etmez, yedek almaz ve korunan dosyaları değiştirmez.

- Eski 92 workflow'un işlevleri: referans envanter; 0/92 davranışsal doğrulama.
- Güvenlik: kaynak belgedeki 1–24 maddeler incelendi; toplam 26 kuralın tam listesi ve 26/26 çalışma zamanı kanıtı henüz yok.
- Beş workflow: manuel tetikleme, salt-okunur token, izole rapor artifact'ı.
- EPG/IBO cihaz onayı: ertelendi.
- Üretime geçiş: yasak; ayrıca kullanıcı onayı gerekir.
- Gerçek K2–K5 iş mantığı, kanıt matrisi, hata devre kesici ve toplu kabul sonraki geliştirme işidir.


## 19 Ekim 2026 — notlardan yeniden doğrulanan kabul sırası
- Eski `Madsc55/madsc-tv` salt-okunur referanstır; eski 92 workflow kodu/cron'u yeni depoya kopyalanmaz.
- K1: 26 güvenlik kuralının kaynak, negatif test ve gerçek çalışma kanıtı ayrı ayrı tutulur. 1–24 kaynak metni biliniyor; 25–26 doğrulanmadan 26/26 denmez.
- K2: M3U ve M3U8 dosyalarından aday çıkarılır; keşif, teknik doğrulama ve ana listeye ekleme farklı aşamalardır.
- K3: Teknik sonuç ile kullanıcının IBO Player cihaz sonucu ayrı alanlardır. IBO'da çalıştığı doğrulanan kanal, teknik test başarısızlığı yüzünden silinemez veya bozuk olarak kesinleştirilemez.
- K4: FAVORİLER, YEDEKLER, YENİLER, mevcut kanallar, EPG, URL, logo, isim, kimlik, kategori ve sıralama korunur; bağımsız yedek ve izole geri yükleme kanıtı olmadan geçiş yoktur.
- K5: K1–K4 hata raporları, fail-closed davranış, devre kesici, tekrar deneme ve toplu kabul raporları birleştirilir.
- Yeni ana liste standardı `playlist.m3u8`, EPG standardı `xmltv.xml`; gerçek cihaz uyumluluğu ayrıca doğrulanır.
- Kullanıcı onayı olmadan üretim dosyası değiştirme, otomatik kanal silme, YEDEKLER'e ekleme, cron açma, eski otomasyon kapatma veya üretime geçiş yoktur.
- Mevcut K2/K3/IBO modülleri ve test dosyaları başlangıç uygulamalarıdır; CI başarı kanıtı ve canlı davranışsal eşdeğerlik henüz yoktur.

## Toplu kabul sırası
1. 92 davranışın envanterini ve 26 kuralın eksiksiz kaynağını doğrula.
2. K1 koruma/negatif testlerini ve IBO cihaz sonucu önceliğini tüm kanal kararlarına bağla.
3. K2 keşif -> K3 teknik test -> cihaz onayı ayrımını uçtan uca test et.
4. K4 bağımsız yedek/geri yükleme tatbikatını izole ortamda doğrula.
5. K5 üzerinden beş workflow'un Actions koşu kanıtını, hata senaryolarını ve kabul matrisini tamamla.
6. Yalnız açık üretim geçiş onayı sonrası canlı yazma/yayınlama değerlendir.


## Görev öncesi zorunlu kaynak notu kontrolü (19 Ekim 2026)
- Kaynak hafıza: eski depodaki `DEVAM_NOTU.md`, `810 dosya notu.md`, `AGENTS.md`, 9 ek inceleme notu, yedek/raporlar ve ilgili kaynak dosyaları. Bu dosyaların tek yerde eksiksiz birleştiği henüz kanıtlanmış değildir.
- **Her kod değişikliğinden önce** o göreve ait not, ilgili ek not ve önceki test/rapor okunur. Bulgular YAPILACAK / YAPILMAYACAK / KANIT BEKLEYEN olarak ayrılır; zaten yapılmış işler tekrarlanmaz.
- İnceleme sayaçları farklı tarihlerden: ana `810 dosya notu.md` 361/810 diyor; daha sonraki ek notlarda 823 toplam ve 450 görsel olmayan dosya incelendiği bildirildi. Kaynak ağaç ve benzersiz yollar uzlaştırılmadan kesin toplam ilan edilmez; görsellerin 373'ü ayrı doğrulama bekliyor.
- Eski depodaki notlara yalnız salt-okunur erişim; yeni depoda görev bazlı uygulanabilir kontrol/test ve kanıt matrisi oluşturulur.
- K3 için kaynak notunda üç aşama, 5 dakikalık süreklilik, 7/30 gün kararlılık, kimlik, EPG/logo ve IBO cihaz onayı ayrı alanlardır. IBO'da çalışan kanal otomatik teknik test nedeniyle silinmez.
- K4 için Git HEAD'den geri yükleme harici yedek sayılmaz; SHA256 manifest, bağımsız kopya ve izole restore kanıtı gerekir.
- Bir GitHub commit'i veya yeşil test, 26/26 güvenlik ve 92/92 davranışsal kabulün yerine geçmez.

 
## Not kapsamı — tek dosyayla sınırlama yok
Ana giriş `DEVAM_NOTU.md` (yaklaşık 691 bin karakter) ve `810 dosya notu.md` (yaklaşık 741 bin karakter) olup **tamamı** tek kısa özet sayılmaz. İlgili görev için bağlantılı tüm notlar ve kaynak kanıtlar ayrıca okunur: `AGENTS.md`, `OZELLIK_ENVANTERI.md`, `IPTV_PROJE_HAFIZASI.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `GUVENLIK_KURALLARI.md`, `TOPLU_DURUM_RAPORU.md`, `SEKIZ_GOREV_TOPLU_DENETIM.md`, `BES_SISTEM_GECIS_KONTROL.md`, `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md`, `MADSC-IKI-TOPLU-KABUL-PLANI.md`, `MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`, `YENI_KANAL_ARAMA_TALEPLERI.md` ve başka atıf yapılan kayıtlar. Liste kapalı değildir; dosyaların mevcut dalda varlığı ve en güncel sürümü ayrıca kontrol edilir.
Öncelik: en güncel açık kullanıcı kararı > doğrulanmış güncel kaynak/test > eski tarihli tarihsel not. Kaynakların tamamen birleştirilmiş olduğu varsayılmaz; okunmayan notlar okunmuş gibi gösterilmez.


## 19 Ekim 2026 — Kanıta dayalı geçiş matrisi (güncel)

Bu bölüm başlangıç durumundan sonra oluşan kanıtları ayırır. **Yeşil CI koşusu, canlı üretim kabulü değildir.**

| Kapı | Doğrulanan kanıt | Eksik kanıt / karar |
|---|---|---|
| Kapsam 99 → 92 | Eski audit kodundaki 7 hariç tutma tanımı; 99/99 YAML ilk kaynak incelemesi; `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` | 92/92 davranışsal parity: **0 onay**, kaynak audit her satırı `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` işaretliyor |
| K1 güvenlik | Yeni depoda salt-okunur workflow statik denetimleri ve CI regresyonları | 26/26 kuralın gerçek enforcement ve branch/runner izinleri doğrulanmadı |
| K2 keşif | URL SHA256 ile aday ayrımı ve orphan kanıt reddi fixture testleri | Canlı kaynak keşfi, kalıcı tarihçe ve eski tetik/çıktı parity |
| K3 kanal/IBO | Teknik sonuç ile kullanıcıdan gelen IBO sonucu ayrımı; 24 saatlik sağlanan geçmişin sınır testleri; K2→K3 kanıt izolasyonu | Gerçek ffprobe ağ ölçümü, IBO Player cihaz kabulü, 5 dakika/7 gün/30 gün saha gözlemi |
| K4 yedek | Üç bağımsız sandbox ağacında SHA256 dosya bütünlüğü, bozulma ve symlink negatif testleri | Dış depolama kaynağı ve gerçek offsite restore kanıtı |
| K5 toplu kabul | Actions #197–#203 koşularında altı işin tamamı başarılı olarak ayrı ayrı doğrulandı | 92 eski işin tetik, hata, çıktı ve bağımlılık bazlı karşılaştırmalı kabulü |

**Sıradaki somut kanıt zinciri:** Her eski YAML için (1) kaynak tetik/izin, (2) çağrılan script ve yazma riski, (3) üretilen artefakt şeması, (4) K1–K5 hedef uygulaması, (5) negatif/pozitif test bağlantısı, (6) canlı veya bağımsız koşu kanıtı, (7) açık kullanıcı onayı gereksinimi tutulmalı. Herhangi biri eksikse durum `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` kalır. Eski 92 işi sırf test sayısı arttı diye otomatik `VERIFIED` yapma.

**Kesin yasak:** Korunan ana liste/YEDEKLER/YENİLER/FAVORİLER, EPG, logo, URL/ID/sıra değişiklikleri; eski depoda yazma; cron/push açma; main merge; PR #71'i birleştirme; kullanıcı onayı olmadan üretim geçişi.
