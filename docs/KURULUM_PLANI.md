# MADSC55-TV — Sıfırdan Beşli Sistem

Başlangıç: 19 Ekim 2026. Eski depo `Madsc55/madsc-tv` yalnız salt-okunur işlev ve güvenlik referansıdır. Eski workflow, cron, kod, geçmiş karar veya otomatik yazma mekanizmaları kopyalanmaz.

## Beş yeni GitHub Actions otomasyonu
1. K1 Güvenlik: 26 kuralın uygulanabilir denetimi, izin ve değişmezlik kapıları.
2. K2 Keşif: yayın kaynağı araştırması, aday havuzu ve kanıt.
3. K3 Kanal testi: bağlantı, HLS sürekliliği, kimlik ve cihaz-onay ayrımı.
4. K4 Arşiv/Yedek: bağımsız yedek, saklama ve izole geri yükleme testi.
5. K5 Genel bakım: toplu rapor, sağlık, mükerrer tetikleme kontrolü ve koordinasyon.

## Değişmez kurallar
- Eski 92 workflow'un **gerekli davranışları** tek tek envanterlenip yeni beş otomasyona işlev olarak atanacak; eski workflow dosyaları taşınmayacak.
- 26 güvenlik kuralı, kaynak kod, negatif test ve çalışma zamanı kanıtı ile ayrı ayrı kabul edilecek. Kanıt yoksa tamamlandı denmeyecek.
- Eski depodaki playlistler, favoriler, URL/logo/kimlik/sıralama, EPG, yedek ve arşivler değiştirilmez.
- Yeni depoda dahi üretim playlisti yayınlama, otomatik silme/değiştirme, eski otomasyonları durdurma, canlı kesinti veya üretime geçiş **ayrı açık onay** olmadan yasak.
- EPG/IBO cihaz uyumluluğu ertelenmiştir; gerçek cihaz testi olmadan onay yok.
- İlk kurulum yalnız `contents: read`, izole rapor/artifact ve manuel tetikleme ile başlayacak. Beş workflow için toplu kabulden önce cron/üretim yazma izni açılmaz.

## Kabul matrisi (henüz doğrulanmadı)
| Alan | Başlangıç |
|---|---|
| 92 eski işlevin envanteri ve K1–K5 eşleştirmesi | Bekliyor |
| 26 kuralın çalışma zamanı kanıtı | 0/26 doğrulandı |
| 5 yeni workflow'un oluşturulması | Bekliyor |
| Tetikleyici/izin/artifact/yan etki/geri dönüş eşdeğerliği | Bekliyor |
| Toplu izole testler ve GitHub Actions run kanıtı | Bekliyor |
| Üretime geçiş | KAPALI |

## Sonraki adım
Eski depodan salt-okunur 92 işlev ve 26 güvenlik kuralı envanterini çıkar; beş yeni bağımsız uygulama ve workflow'u tasarla; her aşamayı test ve commit SHA ile kaydet.
