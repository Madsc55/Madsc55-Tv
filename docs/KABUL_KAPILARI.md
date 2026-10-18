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
