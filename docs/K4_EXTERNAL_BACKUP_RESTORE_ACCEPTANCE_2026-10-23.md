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


## Ek kaynak incelemesi — K4 workflow tetik kapsamı (23 Ekim 2026)
İncelenen kaynak: `.github/workflows/madsc-04-yedek.yml` (blob `28910baa5840da87c97834a9fe4d2708db99a949`). Workflow yalnızca `workflow_dispatch` tetikleyicisine sahip; `schedule`/cron tanımı yok. `permissions: contents: read`, job 10 dakika ile sınırlı ve çıktılar 14 günlük GitHub Actions artifact'ları olarak yükleniyor. Akış gerçek bir dış sağlayıcıya yedek yazmıyor; yalnız `reports/k4-source/nested/sample.txt` test fixture'ı oluşturup izole restore drill / rapor çalıştırıyor. Bu nedenle mevcut K4 workflow'u gerçek ayın 1'i/15'i yedek scheduler'ı olarak kabul edilemez ve sadece cron ekleyerek üretim yedeklemesi haline getirilmemelidir.

K4-18'in eksikliği artık yalnızca run kanıtının yokluğu değil: incelenen K4 workflow'unda iki aylık tetik tanımı da yok. Çözüm, üretim/harici depolama hedefi ve yetkili kimlik bilgileri tasarlanıp ayrı güvenlik incelemesinden geçmeden scheduler'ı üretim gibi göstermemektir. Test fixture'ı gerçek veriye bağlanmamalı.


## 23 Ekim 2026 — K4 inode karşılaştırma TOCTOU onarımı
- `madsc/backup.py` içinde `compare_copy` ve `verify_independent_restore`, içerik manifestini güvenle oluşturduktan sonra inode karşılaştırmasını normal `Path.stat()` ile yapıyordu. Bir dosyanın bu iki aşama arasında symlink ile değiştirilmesi hâlinde son kimlik sorgusu linki takip edebilirdi.
- Kod commit `e4fa64bc6814c3cce65678fbd59a337881d67b9b` (`madsc/backup.py`) ile kimlik sorguları `_open_relative_file_nofollow` üzerinden `os.fstat()` yapacak şekilde değiştirildi. Normal dosya ve tek hard-link kontrolü korunuyor; dosya tanıtıcısı `finally` içinde kapanıyor.
- Yeni regresyon testleri: `tests/test_backup_manifest_hardening.py`, commit `3305e620b9186cdd3544a4962bd45303413cc7f4`. İki ağaçlı kopya ve üç ağaçlı restore kontrolünde manifestten sonra kaynak dosyanın symlink'e çevrilmesi simüle ediliyor; dış hedefin içeriği korunmalı, denetim başarısız olmalı.
- Kod commit CI: Actions `39868881731`, `success`. Test commitine ait Actions `39868921875`, paralel dal güncellemeleri nedeniyle `cancelled`; yeni iki test için tek başına tamamlanmış CI kanıtı yok. Sonraki main CI'de tüm testlerin geçtiği doğrulanmalı.
- Bu yalnızca izole kopya inode-denetim güvenliğini geliştirir; gerçek harici yedek makbuzu, bağımsız harici restore, VOD/arşiv kabulü ve ayın 1'i/15'i scheduler davranışı hâlâ eksik. Kabul sayaçları değişmedi.


## 23 Ekim 2026 — Kaynak dosya tanıtıcısı sızıntısı ve CI takibi
- `madsc/backup.py` commit `477bece204df03d1896b529e5368f3f2a3a8a819`: hem `backup_to_new_sandbox` hem `restore_to_new_sandbox` hedef oluşturma hatasında açık kaynak tanıtıcısını `os.close` ile kapatıyor. Hata önceki gibi geri alma mekanizmasına aktarılıyor.
- `tests/test_backup_manifest_hardening.py` commit `aae9e86fc2cd40fe6d08e6fcc9ab71efb0623044`: iki yeni hata enjeksiyonu testi kaynak tanıtıcısının kapandığını ve yarım hedefin temizlendiğini doğrulamak için eklendi.
- Actions `39869948785` **failure**: K4 testinde hatalı çok satırlı `with` sözdizimi (`SyntaxError`) ve ayrı K2 `test_empty_name_and_orphan_url_are_reported` beklenti uyuşmazlığı. Paralel `fix(ci): correct malformed multiline mock context managers` commitinin Actions `39870164408` çalıştırmasında artık K4 SyntaxError görülmüyor; **yalnız K2 testi başarısız**, toplam 1035 test. Bu nedenle henüz tam yeşil CI kabulü yok. K2 dosyası paralel sohbet tarafından düzeltiliyor, çakışma yaratmamak için burada tekrar değiştirilmedi.
- Gerçek harici yedek makbuzu, bağımsız dış restore, korunan VOD/arşiv eşdeğerliği ve ayın 1/15 zamanlayıcı kanıtı hâlâ yok. Üretim dosyaları değiştirilmedi.


## 23 Ekim 2026 — Sahte harici yedek kabul beyanlarını reddetme
- `madsc/backup.py` commit `7815f0c6e6d0a9e12783306f4a57e4c62c6adc06`: `verify_manifest`, yerel checksum manifestine eklenen `external_backup_verified`, `restore_verified` veya `production_writes` alanlarının `False` dışındaki değerlerini artık `ValueError` ile reddediyor. Özellikle Python'da `True == 1` olmasına rağmen `1` de kabul edilmiyor.
- `tests/test_backup_manifest_hardening.py` commit `1bb7aead06b252544bb3e2d41e89bd89840e4c5a`: her alan için `True`, `1`, `"true"` ve `None` sahte beyanlarını sınayan regresyon eklendi. Orijinal yerel manifestin geçerli kalması da doğrulanıyor.
- Bu değişiklik yerel checksum kanıtının gerçek harici yedek veya üretim restore kanıtıymış gibi sunulmasını engeller; gerçek dış servis makbuzu veya restore üretmez. Son gözlemde Actions `39870589190` paralel commit yüzünden `cancelled`; yeni regresyonun güncel tam CI başarısı ayrıca doğrulanmalı.
- IBO Player Pro cihaz kabulü kullanıcı talimatıyla en sona bırakıldı; gerçek cihaz testini kullanıcı yapıp bildirecek.


## 23 Ekim 2026 — Yerel manifest kayıt sayısı üst sınırı
- `madsc/backup.py` commit `49122e9a55a86b042db6c008b8d4d9e15a72b1f7`: `verify_manifest` doğrulaması 10.000'i aşan manifest girdilerini herhangi bir kaynak dosya taraması başlamadan reddediyor; boş manifest yine kabul edilmiyor.
- `tests/test_backup_manifest_hardening.py` commit `1394bcfc75eb716a947b56349ce8e7d5d2e44b39`: 10.001 girdili manifestin `snapshot_manifest` çağırmadan reddedildiğini ve normal tek dosyalı manifestin doğrulandığını test ediyor.
- Bu sınır yalnız yerel doğrulama kaynak tüketimini azaltır; gerçek harici yedek/restore kanıtı değildir. İlgili Actions `39870802547` paralel commit yüzünden `cancelled`; sonraki başarılı main CI'de yeni testin dahil olduğu ayrıca teyit edilmeli.
- IBO Player Pro gerçek cihaz doğrulaması kullanıcı tarafından en son yapılacak; cihaz kabulü henüz yapılmadı.


## 23 Ekim 2026 — Manifest yol uzunluğu sınırı
- `madsc/backup.py` commit `1b40b3d2014801140b5a5aa5ebc48346aa670534`: `verify_manifest`, dosya yolunun 4.096 karakteri aşmasını dosya sistemine erişmeden reddediyor.
- `tests/test_backup_manifest_hardening.py` commit `0e80fb7b9b9dd0048195b0d97b459eb080ebf0f5`: 4.097 karakterli sahte yolun `snapshot_manifest` çağırmadan reddedilmesini ve normal manifestin çalışmasını test ediyor.
- İlgili Actions `39871017628` paralel commit nedeniyle iptal edildi; daha sonraki başarılı entegre CI kanıtı bekleniyor. Harici yedek ve gerçek restore kanıtı hâlâ yok. IBO Player Pro cihaz testi en sona bırakıldı.


## 23 Ekim 2026 — Manifest oluşturma sırasında kaynak sınırları
- `madsc/backup.py` commit `1fdd72097cfcd84e135d34012362cf391d607106`: `snapshot_manifest` 10.000'i aşan farklı kaynak adı ve 4.096 karakteri aşan kaynak yolunu dosya içeriği okumadan reddediyor. Bu sınırlar mevcut `verify_manifest` sınırlarıyla tutarlı.
- `tests/test_backup_manifest_hardening.py` commit `3979d18da782cfdd73c92174a8f0058f93051ea7`: 10.001 benzersiz isim ve 4.097 karakterli yol için kaynak açılmadan reddetme testi, normal manifest için olumlu kontrol eklendi.
- İlgili Actions `39871237418` son kontrol sırasında `pending`; test henüz doğrulanmış yeşil değil. Harici yedek makbuzu, bağımsız dış geri yükleme ve üretim kabulü hâlâ açık. IBO Player Pro cihaz doğrulaması en son kullanıcı tarafından yapılacak.


## 23 Ekim 2026 — Manifest modu sahteciliğini engelleme
- `madsc/backup.py` commit `98080a00db69e66d2c0c9fe559ce3e46ffa96776`: `verify_manifest`, varsa `mode` alanını yalnız `manifest_only` kabul ediyor.
- `tests/test_backup_manifest_hardening.py` commit `2669060015c9f3f7cf670783761df6dbd71d7006`: sahte `external`, `verified_restore` ve geçersiz türleri reddetme regresyonu.
- Actions `39871548601` son kontrolde `queued`; yeni test için başarılı CI kanıtı henüz yok. Harici yedek ve bağımsız restore kabulü açık; IBO Player Pro gerçek cihaz testi en son kullanıcı tarafından yapılacak.


## 23 Ekim 2026 — Manifest mode tam tür kontrolü
- `madsc/backup.py` commit `57d508001bc904c3bbf35f0d9c308e17a6c68679`: varsa `mode` alanının türü tam `str` ve değeri `manifest_only` olmalı; özel `str` alt sınıfları da kabul edilmiyor.
- `tests/test_backup_manifest_hardening.py` commit `791d87c24a49b1b4e7937d56b623c6ba2bf29c2e`: aynı metni taşıyan `str` alt sınıfını reddetme ve orijinal manifesti doğrulama regresyonu.
- Son gözlemde ilgili Actions `39871776901` paralel commit nedeniyle iptal; yeni test için entegre CI başarı kanıtı bekleniyor. Daha önceki `39871569940` başarılı. Harici yedek ve bağımsız restore kabulü açık; IBO Player Pro cihaz testi kullanıcı tarafından en son yapılacak.


## 23 Ekim 2026 — Manifest yolu kontrol karakterleri ve Unicode
- `madsc/backup.py` commit `192ccc0c4ac3f75a168dd5fe68ea198e63b86e23`: `verify_manifest`, NUL, ASCII kontrol karakterleri ve geçersiz UTF-16 surrogate kod noktalarını kaynak dosya okunmadan reddediyor.
- `tests/test_backup_manifest_hardening.py` commit `a93c60e54b369b9c5caa7326f24de617daaa338f`: gerçek Python kaçış dizileriyle NUL, newline, DEL ve iki surrogate örneği için regresyon; geçerli yerel manifest olumlu kontrolü.
- Yeni CI sonucunun doğrulanması bekleniyor. Gerçek harici yedek ve bağımsız geri yükleme kabulü açık; IBO Player Pro gerçek cihaz testi en son kullanıcı tarafından yapılacak.
