# K4 — Harici yedek ve izole geri yükleme kabul kapısı
Tarih: 23 Ekim 2026 (Europe/Stockholm)
Kanonik depo/dal: Madsc55/Madsc55-Tv / main

## Bu kaydın amacı
Bu belge K4-15, K4-16, K4-17 ve K4-18 için gerçek kanıt gereksinimlerini sabitler. Bir test fixture'ının yeşil olması, harici depolama, üretim arşivi/VOD veya takvim davranışını kanıtlamaz. Bu belge tek başına hiçbir kabul sayacını artırmaz.

## Mevcut doğrulanmış kod kapsamı
- `madsc/backup.py`: kaynak dosyaları no-follow/dirfd ile açma; normal dosya ve tek link kontrolü; SHA-256 + byte manifesti; bağımsız sandbox kopya ve üç ağaçlı kaynak/yedek/geri-yükleme karşılaştırması; yalnızca yeni sandbox dizinine restore; başarısız kopyada oluşturulan inode ile eşleşen ağacı temizleme.
- `tests/test_backup.py` ve `tests/test_backup_manifest_hardening.py`: symlink, path traversal, yinelenen isim, hard-link, bozuk hash/byte, değişmiş içerik, nested tree ve sandbox restore regresyonları içeriyor.
- Raporlar kasıtlı olarak `external_storage_proven=false`, `production_restore_verified=false` ve `production_writes=false` döndürüyor. Bu bayrakları yalnız fixture ile true yapmak yasaktır.
- En son eldeki genel offline CI kaydı 990 test için başarıdır: Actions 39865933101, test edilen SHA a4c70f7277be8aad73cdd95d027115b7bcab469d. Bu, K4 için harici yedek kabulü değildir. Bu kayıt yazılırken güncel main HEAD ayrıca b08490dbd6552e18926062a3c6e2450a92239e47 olarak kontrol edildi; yeni bir Actions çalıştırması başlatılmadı.

## K4-15 — Bağımsız harici yedek oluşturma
Kabul için gereken asgari kanıt:
1. Harici hedef sağlayıcı/türünün adı ve hedefin üretim kaynağından bağımsız olduğunu doğrulayan metadata.
2. Yedek işinin gerçek zaman damgası, run/işlem kimliği ve kaynak commit/manifest kimliği.
3. Her dosyanın göreli yolu, byte sayısı ve SHA-256 değeri; eksik/fazla/duplicate dosya kontrolü.
4. Hedef sistemin kendi tarafından üretilmiş yazım/nesne kimliği veya değişmez makbuz; yalnızca yerel simülasyon çıktısı yeterli değil.
5. Gizli URL, token, parola veya kişisel veri içermeyen, bağımsız olarak doğrulanabilir kanıt paketi.

## K4-16 — Harici yedekten gerçek izole geri yükleme
Kabul için gereken asgari kanıt:
1. K4-15'teki harici yedek kimliğinin aynısı.
2. Üretimden bağımsız, temiz ve izole bir hedefe gerçek geri yükleme run kimliği ve zaman damgası.
3. Geri yüklenen her dosya için yol/byte/SHA-256 eşleşmesi; beklenen kapsam listesi ile bulunan dosya listesi birebir aynı.
4. Kaynak, harici yedek ve restore ağaçlarının farklı kökler ve farklı inode'lar olduğunun kanıtı; hard-link veya iç içe ağaç olmamalı.
5. Başarısız/bozuk kopyanın kabul edilmediğini ve üretim yollarına yazılmadığını gösteren negatif kontrol.
6. Bağımsız inceleyici veya harici sağlayıcı kanıtı. Üç yerel fixture dizini yalnızca sandbox testidir.

## K4-17 — Korunan arşivler ve VOD
- Gerçek arşiv/VOD kapsam envanteri, boyut/metadata/hash ve beklenen saklama/erişim semantiği sabitlenmeden eşdeğerlik iddia edilmez.
- Üretim arşivi/VOD üzerinde yazma, silme, taşıma, yeniden adlandırma veya restore deneyi yapılmaz.
- Kabul, üretim verisine dokunmayan yetkili test kopyası ve bağımsız içerik/metadata karşılaştırması ister.

## K4-18 — Ayın 1'i ve 15'i yedek davranışı
- Workflow/cron tetik tanımı ve timezone, DST, ay sonu, tekrar çalıştırma/idempotency ve hata/timeout/retry davranışı kaynak kodundan sabitlenmeli.
- Takvim simülasyonları yalnız statik/fixture kanıtıdır; gerçek scheduler run kaydı olmadan davranışsal eşdeğerlik kabul edilmez.
- 1. ve 15. gün tetiklerinin gerçek run/artifact kimliği, exit code ve bağımsız inceleme sonucu gereklidir. Manuel Actions dispatch yapılmadı ve bu belge nedeniyle yapılmayacak.

## Şimdiki karar
- K4-15: pending — harici hedef yazım makbuzu yok.
- K4-16: in_progress — sandbox restore fixture mevcut; harici kaynaktan gerçek restore yok.
- K4-17: pending — korunan arşiv/VOD için bağımsız kapsam ve kabul kanıtı yok.
- K4-18: pending — ayın 1'i/15'i gerçek scheduler eşdeğerliği kanıtı yok.
- Genel kabul sayaçları değişmez: 92 eski workflow 0/92; 26 runtime güvenlik kuralı 0/26; 22 ana görev 0/22.

## Güvenlik sınırları
Gerçek playlist/M3U, XMLTV/EPG, FAVORILER, YENILER, YEDEKLER, HEPSI, logolar, cihaz verileri, üretim arşivi/VOD değiştirilmez. Harici servis, kullanıcı cihazı veya üretim hesabına erişim varsayılmaz. Actions dispatch/rerun, merge ve PR #71 merge yapılmaz. Her yeni yazımdan önce canlı HEAD ve hedef blob SHA tekrar kontrol edilir.
