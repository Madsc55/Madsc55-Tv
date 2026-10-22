# K1 / K5 — 22 Ekim 2026 devir notu

## Kapsam ve eşzamanlı çalışma
Bu sohbet yalnız K1 güvenlik ve K5 bakım/kabul sınırlarını işler. K2/K3/K4 sohbetlerinin aktif dosyalarını değiştirme; aynı işleri tekrar etme. Ana depo `Madsc55/Madsc55-Tv`, dal `main`. Üretim playlistleri, EPG, logolar, yedekler, cihaz verisi ve PR #71 korunur. Bu not yalnız kayıt amaçlıdır; çalışma zamanı kabul kanıtı değildir.

## Bu sohbetin kaydedilmiş kod ve test commitleri
- `9805fa7`, `d068403`: K5 beş ayrı kategori raporu ve negatif testleri.
- `b8a0243`, `56f64fa`: K1 .git/.github/.gitmodules/.gitattributes yazma reddi ve test.
- `b2a355c`, `3858954`, `e6b9e39`: K1 boş yazma talebi reddi, K5 boş fixture anahtarı reddi ve test.
- `74c1b28`, `35d0e10`: K1 Unicode format/bidi yol gizleme reddi ve test.
- `c187398`, `4f0f7db`: K5 toplam aday sayısı sınırı (10000) ve test.
- `4f1f847`, `865ea57`: K5 aday başına alan sayısı sınırı (32) ve test.
- `7692b0e`, `3c391fa`: K5 cancelled/skipped/neutral/action_required/stale sonucunu başarı saymama ve test.
- `b05806b`, `3620938`: K5 önceki aktif çalışmayı atlamama ve test.
- `3610c9f`, `bfb6068`: K1 .gitignore/.mailmap yazma reddi ve test.

## Bağımsız doğrulama ve kabul ayrımı
Bu sohbetin yeni commitleri için GitHub Actions sonucuyla eşleşen güncel başarılı tam test koşusu **doğrulanmadı**. 22 Ekim'de başka sohbetin `DEVAM_NOTU.md` kaydında, farklı bir SHA üzerinde 800/800 offline test ve beş izole kapının geçtiği, fakat daha sonraki başka SHA üzerinde 816 testte 5 failure ve 3 error bulunduğu yazıyor; bunlar mevcut HEAD'in yeşil olduğu anlamına gelmez. Son görülen Actions offline test başarıları da eski SHA'lara aitti. `[skip ci]` commitleri otomatik test çalıştırmaz.

**Gerçek kabul sayaçları değişmedi: 0/92 eski davranış eşdeğerliği, 0/26 runtime güvenlik kuralı, 0/22 görev.** K1 koruma fonksiyonları çağıranları denetler; bağımsız git push veya workflow yazmalarını otomatik olarak durdurmaz.

## Sıradaki işler
1. Diğer sohbetlerin HEAD güncellemelerini ve devir notunu tekrar okuyup çatışmayı önle.
2. Güncel HEAD üzerinde K1/K5 odaklı regresyonları ve tam offline gate'i **gerçekten çalıştır**; SHA, test sayısı ve başarısızlıkları kaydet. Çalıştırılamıyorsa geçti deme.
3. K1 yazıcı AST envanterindeki 20 dinamik/subprocess adayını güvenli salt-okunur / belirsiz / yazabilir olarak komut düzeyinde sınıflandır; çalışma zamanı kanıtı yoksa fail-closed.
4. K5 için gerçek eski/yeni aynı girdili karşılaştırma çiftleri, kökeni doğrulanmış Actions geçmişi ve harici kanıtları ayrı kabul et; fixture kanıtından üretim hazır sonucu çıkarma.
5. Başka sohbetlerin K2/K3/K4 kodunu, üretim dosyalarını veya ortak `DEVAM_NOTU.md` dosyasını bu sohbetten değiştirme.

Bu dosya yalnız K1/K5'e ait ayrı devir kaydıdır.


## 22 Ekim — eşzamanlı sohbet koordinasyonu ve yeni K5 düzeltmeleri
- GitHub main üzerindeki son commitler yeniden kontrol edildi: K2/K3 sohbetleri `madsc` kanıt doğrulaması, keşif zarfı ve regresyon testlerinde aktif. Bu sohbet onların dosyalarını değiştirmedi.
- K5 `madsc/maintenance.py` ve bağımsız `tests/test_k5_*.py` dosyaları: `0d9ad9a` durum/sonuç tutarlılığı, `e8b9726` test; `174492f` hatalı zaman damgası hatası, `3e680a3` test; `76a17c2` sonuç tipi, `48ce649` test; `ab4c39a` aynı dalda daha yeni çalışmanın eski hedefi geçersiz kılması, `add5501` test; `47e8cbc` 1000 kayıt üst sınırı, `846bb16` sayfalama sınırı testleri.
- Bunlar `[skip ci]` commitleridir; yeni HEAD üzerinde odaklı veya tam test başarısı doğrulanmadı. Sonradan gelen K2/K3 commitleri de test gerektirir.
- Sohbetler arasında otomatik kilit/gerçek zamanlı senkronizasyon yok; her yazma öncesinde son HEAD ve dosya SHA kontrol edilmeli. Ortak dosya değişikliklerinden kaçınmak temel kuraldır. Kabul sayaçları 0/92, 0/26, 0/22.


## 22 Ekim — K1 aygıt adı koruması ve son durum
- K1 `madsc/write_path_audit.py` commit `8768682792535285640c0e62c688a162bfee844b`: Windows özel aygıt kökleri `CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`, dosya uzantısı ve NFKC eşdeğeri olsa bile her dizin seviyesinde reddedilir. `tests/test_k1_reserved_device_paths.py` commit `9109b49f026541e81ea93eb45173cb09269b94b6`: 8 reddedilen ve 4 geçerli yol vakası.
- Bu iki commit GitHub'a yazıldı ancak güncel HEAD üzerinde çalıştırılmış test kanıtı **yok**. Kod incelemesi test çalıştırmasının yerine geçmez.
- Son main kontrolünde K3 sohbeti ardışık commitler yayımlıyor; K1/K5 bu dosyalara dokunmuyor. Sohbetler arasında gerçek zamanlı kilit yok; yalnız son HEAD/dosya SHA kontrolü ve ayrı dosya sahipliğiyle çakışma riski azaltılıyor.
- Öncelikler: güncel HEAD üzerinde odaklı K1/K5 testleri ve tam offline gate; K1 20 dinamik yazıcı/subprocess adayı; K5 gerçek eski/yeni davranış çiftleri. 0/92, 0/26, 0/22 gerçek kabul sayaçları değişmedi.


## 22 Ekim — sonraki K1/K5 doğrulama devri
- K1 Unicode NFKC sonrasında alternatif veri akışı `:` ayracını engelleme: `23c1381`; `tests/test_k1_unicode_stream_separators.py`: `ed5dd4e`.
- K5 tarih damgası doğrulaması: ilk `5a83ec4` ve `8729f06` test; tam RFC3339 biçim kontrolü `5bdd2f6` ve `tests/test_k5_strict_rfc3339.py` `13a830c`. İlgili kod ve testler ana dala yazıldı.
- **Test engeli teyidi:** çalışma konteynerinde `git ls-remote https://github.com/Madsc55/Madsc55-Tv.git HEAD` komutu DNS çözümleme hatasıyla sonuçlandı (`Could not resolve host: github.com`). GitHub bağlayıcısı kaynak okuma/yazma ve eski Actions sonuçlarını görmeyi sağlıyor; mevcut araçlarla yeni HEAD için tam test koşusu başlatılamadı. Eski yeşil Actions koşusu güncel HEAD'i doğrulamaz.
- Son incelemede K2/K3/K4 paralel commitleri sürüyor. K1/K5 ayrı dosyaları dışında değişiklik yapılmadı; testler gerçek çalışmadan kabul sayıları artırılmamalı.


## 22 Ekim — K1/K5 son uygulama ve düzeltme notları
- K1 geçersiz Unicode surrogate koruması `50b1288`, test `6e0ce96`. Testin ilk sürümü gerçek surrogate karakterleri yerine kaçış metinlerini deniyordu; `a4f9e28` ile `chr(0xD800)` vb. gerçek karakterler kullanılarak düzeltildi.
- K1 yerel çıktı denetiminde eklenen erken politika kontrolü `224a950`, mevcut geç aşama kontrolünü yinelediği ve hata türünü değiştirdiği için `3ae9989` ile geri alındı. **Son geçerli K1 kaynak durumunda tekrar yoktur.**
- Paralel sohbetler K2/K3 dosyalarını değiştirmeye devam ediyor; bu sohbet yalnız K1/K5 ve ayrı devir dosyasına yazdı.
- Son durum: Kod ve test dosyaları commit edildi, fakat güncel HEAD üzerinde CI/offline test koşusu kanıtlanmadı. Gerçek kabul 0/92, 0/26, 0/22 olarak tutulur. Bir sonraki iş test altyapısını doğrulamak ve 20 K1 dinamik yazıcı adayının salt-okunur sınıflandırmasını tamamlamaktır.


## 22 Ekim — K1 kaynak envanteriyle kritik tutarlılık kontrolü
- GitHub main recursive tree incelendi. `tools/protected_write_gate.py` **main ağacında bulunamadı**; doğrudan fetch 404 verdi. Buna karşılık `docs/K1_KORUNAN_YAZMA_KAPISI_CELISKI_2026-10-22.md` bu kapıyı **başka bir kaynak revizyonunda** (`Madsc55/madsc-tv@ca374df3...`) anlatıyor. Bu raporu mevcut `Madsc55/Madsc55-Tv` main üzerinde fiilen çalışan kapı kanıtı sayma.
- Main üzerinde `madsc/write_path_audit.py` mevcuttur, ancak `enforce_write_paths` çağrısı yapan yazıcıların tam listesi ve 26 güvenlik kuralının çalışma zamanı icrası henüz doğrulanmadı. `runtime_gate_enforced` dönüş değeri yalnız fonksiyonun çağrıldığını gösterir; bağımsız yazıcıları kapsadığını göstermez.
- `madsc/k1_k5_acceptance_requirements.py` 22 görev için eksik kanıt anahtarlarını hesaplar, fakat modülün kendi açıklamasına göre doğrulama/gerçek üretim kabulü değildir. `verified` girdisini bağımsız kanıt yerine kullanıp görev kapatma.
- **Kritik sonraki adım:** doğru depo/dal ve eski kapının kaynak revizyonu arasında iz sür; main üzerindeki gerçek yazıcı çağrılarını envanterle, dinamik/subprocess adaylarını ayrı sınıflandır. Korunan üretim M3U kapısını kullanıcı onayı olmadan gevşetme.


## 22 Ekim — K1 yazıcı envanterinde doğrudan kaynak incelemesi
GitHub main üzerinde dört modülün kaynakları doğrudan okundu:
1. `madsc/fixture_report_writer.py`: `_exclusive_bytes` os.open(O_EXCL|O_CREAT), mümkünse O_NOFOLLOW ve fstat ile yalnız izole fixture çıktısı üretir. `write_fixture_report` ve K3 test paketi için kapsamı sınırlıdır; depo genelinde otomatik yazma engeli değildir.
2. `madsc/parity_manifest_writer.py`: `write_replacement_parity_manifest` çıktı üretimini `write_fixture_report` üzerinden yapar. Davranış eşdeğerliğini kabul etmez.
3. `madsc/parity_snapshot_writer.py`: `write_execution_snapshot` yine fixture yazıcısını kullanır; `_sha256_regular_file` salt-okunur dosya gözlemidir, fstat/lstat sürüm kontrolü yapar. Harici üretim kanıtı değildir.
4. `madsc/backup.py`: `snapshot_manifest` salt-okunur hash envanteri, `verify_manifest` salt-okunur karşılaştırma, `compare_copy` salt-okunur izole kopya karşılaştırması. Dış depolama/gerçek restore kanıtı değildir.
**Sınır:** Bu 4 modül, daha önce sözü edilen 20 dinamik/subprocess adayının tam listesi değildir. 20/20 incelendi iddiası yok. Önceki rapordaki `tools/protected_write_gate.py` güncel main üzerinde yok; kaynak/dal karışıklığı çözülmeden o kapının kapsamı varsayılmamalı.
