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
