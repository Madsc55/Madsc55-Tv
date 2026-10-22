# MADSC55-TV — K2/K3 sohbet devri (22 Ekim 2026)

## Kapsam ve çakışma önleme
- Depo: Madsc55/Madsc55-Tv, dal: main. Bu sohbet K2 aday/kaynak/ölçüm bağlantısı ve K3 kanal sürekliliği/kanıt doğrulaması kapsamındadır. K1, K4, K5 diğer sohbetlere bırakılmıştır.
- Korunan üretim playlistleri, EPG/XMLTV, logolar, favoriler, arşivler ve yedekler değiştirilmez. Eski madsc-tv deposu salt okunur. Canlı akış testleri ve Actions tetikleme yapılmadı.
- Eşzamanlı sohbetler main'e yazıyor: her yazımdan önce güncel dosya blob SHA'sını al; 409 çakışmada zorla yazma, yeniden oku. Commit mesajlarında [skip ci] kullan.

## Bu sohbetin doğrulanmış GitHub kayıtları
- 35090e5606a603bbf176194e55e8393f3bd09b9c: K2 aday/K3 probe bağlantısı için yinelenen aday, yinelenen ölçüm, geçersiz SHA-256 testleri.
- ad42d13e2006e4519935000f2a0d6df0ffa5f010: madsc/channel_test.py evaluate_three_stage_continuity ardışık her iki gözlem arasında en az minimum_hours (varsayılan 6 saat) arar; yalnız ilk-son toplam süre artık yeterli değildir.
- ab0c9931882d60022d71d1e6c1b5f3b1ef89bb29: yakın zamanlı örneklerin uzun toplam pencerede yanlış ön kabul almasını engelleyen regresyon testi.
- bc06b806d343f6ab8539492f00d776428a5d9253: madsc/k3_three_stage_gate.py captured_at için katı UTC RFC3339 biçimi doğrulaması.
- 745adb23c4d2b9c6940f431d914462f5936a7201: UTC tarih biçimi reddi regresyon testi.
- f07dbbbe7fd2b49fbeb1cd9f5bd45b6fdd9f99cf: UTC RFC3339 regex içindeki hatalı çift kaçış düzeltildi; geçerli timestamp reddi hatası giderildi.
- Başka sohbetlerin sonradan eklediği K2/K3 kaynak snapshot hash korelasyonu ve K3 test fixture güncellemelerini yeniden yapma. Bu devir notu hazırlanırken main başı bfb606865a...; güncel HEAD'i yeniden kontrol et.

## Kanıt durumu ve açık işler
- GitHub'a commit atılması testlerin geçtiği anlamına gelmez. Bu sohbet güncel tüm test paketini veya yeni regresyon testlerini çalıştırıp doğrulamadı; doğrulanmış yeşil test sayısı iddia edilmez.
- K2 gerçek kaynak/geçmiş kanıtının aynı snapshot'a bağlanması, K3'te 3 bağımsız örnek, ardışık >=6 saat, gerçek ffprobe/ffmpeg kanıtı ve IBO Player Pro cihaz denemesi uçtan uca doğrulanmalı. Offline sahte/fixture kanıt üretim kabulü değildir.
- Önceki proje devirlerine göre 92 eski workflow için bağımsız gerçek davranışsal kabul, 26 K1 kuralı için runtime denetim ve 22 görev için tam kabul hâlâ açık; bunları bitmiş ilan etme. Güncel durum için ana devir notları ve en yeni commitleri tekrar oku.
- Sonraki güvenli iş: güncel main'de K2/K3 testlerini topluca çalıştır; hataları kaynağında düzelt; önceki sohbetlerin aynı dosyalardaki güncellemelerini koru. Üretim kaynaklarını değiştirme.

## Ek devir — 22 Ekim, sonraki K2/K3 çalışmaları

### Bu sohbetin ek commitleri
- ea0cefc0593e4bf657341d090ec8d84435ec8f0b: aday/probe bağlantısında aday yapısı ve SHA kontrolü.
- aad6c4462a94e316ab946da90de6316b269880d9: bozuk aday regresyonu; başka sohbet daha sonra testi paket sınırında reddi doğrulayacak biçimde uyarladı.
- 3b875f7a162c53b61bbae6d908bd6520f267fb11 ve a2312a541e36ddd4246b8adfaf655c0f660f8574: aday ve alternatif listeleri için 20.000 üst sınırı ve testler.
- 07dc7b82c4710b21eb700d0411fc5ad8fd4c877c ve 0fe73d3d0f20fe7c141c1e0c73a0fb0d89925715: alternatif listesinin veri tipi kontrolü ve testler.
- fe9ee61499528a1221def7c5faf11dfa146799d8, 96abf90335716cfd6c3c7db385dc188a1009cc28, a733d2cc0996881ca47d8bc37d5d7cd25151f723: K3 süreklilik kanıtında gelecekteki/eski tarih reddi ve saat dilimi regresyonları.
- 089110df2818a163ac975b786f424986a8440a5a, c58f9f93e48cec122ae1594244cabd5dacb773a9: JSON'a çevrilemeyen veya 16 MiB üstü K2/K3 keşif kanıtı reddi ve testleri.
- ae3b70751a56e3c8621a6d66890c5b05fd2a31e4, 84c958add37b86f97c07706fedcd38d2700c4a6d: canonical küçük harf SHA-256 digest ve hmac.compare_digest ile doğrulama, bozuk digest regresyonları.
- be7b53571f20c81431582cf277ed5fd1e50ade32, 012bf2dfea267273b5d17d2a7800de34a0de9636: K2/K3 run_id en fazla 20 ASCII rakam ve sınır testleri.

### Paralel sohbet koordinasyonu
- Başka sohbetler K1, K5 ve K3 testlerini aynı main dalına kaydediyor; son görülen HEAD d686a73e8e (K3 probe-cap testi). Bu sohbetin 012bf2d commit'i öncesinde K1'in 876868 commit'i yüzünden GitHub 409 oluştu; dosya tekrar okunarak değişiklik güvenle yeniden yazıldı. Doğrudan sohbetler arası mesajlaşma yok; ortak commit geçmişi üzerinden koordinasyon var.
- Diğer K3 sohbetinin URL deduplikasyonu, unseekable stream ve kimlik normalizasyonu düzeltmelerini tekrarlama. Aynı dosyada eşzamanlı çalışma riskini gözet.

### Dürüst doğrulama durumu ve sıradaki işler
- Bu ek commitler GitHub'a kaydedildi; bu sohbet henüz Python testlerini çalıştırmadı. Önce yeni testlerin mevcut fixture yapısına uygunluğunu ve toplu unittest/pytest çalışmasını doğrula. K2/K3 gerçek üretim kanıtı ve cihaz kabulü açık.
- Özellikle tests/test_artifact_handoff.py içindeki yeni testlerin self.discovery ve self.envelope fixture'larının mevcut olup olmadığını kontrol et; yanlış fixture varsa düzelt. K3'te 3 ayrı >=6 saat ölçüm ve gerçek kaynak/ffprobe kanıtı olmadan üretim onayı verme.
- Korunan dosyalara dokunma; canlı yayın veya GitHub Actions tetikleme için ayrıca izin gerekir.

## Son K2/K3 ilerleme — 22 Ekim

- 967e238 ve 56c6bdf: alternatif kaynakların canonical birincil kimliğe bağlanması ve ters/zincir eşleştirme regresyonları.
- f46156a, f859671 ve ef15f5e: handoff tvg-id güvenli karakter doğrulaması ve test.
- d69631d ve 35a4438: kanal adı, logo ve grup metadata doğrulaması ve test.
- 8c60ccc ve 494b47a: doğrudan handoff için 20.000 aday/alternatif sınırları ve test.
- 21bf6d1 ve 17e6299: probe, continuity ve IBO kanıt haritalarında 20.000 sınırı ve test.
- 5b7f7e1 ve c63cb1b: kanıt haritası anahtarlarında canonical SHA-256 kontrolü ve test.
- 7b1bac6 ve 888137f: alternatif ilişki SHA-256 kontrolü ve test.
- 6477dc3: alternatifin ana kaynak diye kullanılmasını engelleyen ek koruma; henüz test çalıştırılmadı.
- Diğer sohbetler aynı anda ortak kaynak snapshot, K3 evidence loader ve K1/K5 düzeltmelerini yaptı. Son görülen HEAD 65027d921d; her işlemden önce güncel HEAD ve blob SHA kontrol edilmeli.
- Testler bu sohbet tarafından çalıştırılıp doğrulanmadı. Devir notunu gerçek yeşil test raporu yerine kullanma; yeni testler ve tüm K2/K3 paketi toplu doğrulanmalı. Üretim playlist/EPG/logo/favori/arşiv/yedek korunur; canlı probelar/Actions izinsiz başlatılmaz.

## Sohbet birleştirme için son devir — 22 Ekim 2026

**Bu sohbetin sahipliği:** K2 keşif / K2→K3 salt-okunur kanıt aktarımı ve bu sınırdaki regresyon testleri. Diğer sohbetler K1/K5, K2/K4, K3 ve ortak snapshot/entegrasyon işlerini paralel yaptı. Tek sohbette birleşirken yeni görev sahipliği dağıt; aynı düzeltmeleri yeniden yapma. Her düzenlemeden önce güncel main commit'i ve hedef dosyanın SHA'sını yeniden oku, eşzamanlı commit varsa yeniden dene, zorla üzerine yazma.

**Bu sohbetin son kod/test commit'leri:**
- 17a4fa7, d69ab20: keşif ham aday satırı ve bilinen URL sayısı 20.000 sınırı, regresyon.
- 5f453f6, ba8f87e: sınır kontrollerini pahalı URL normalleştirmesinin önüne taşıma.
- a178a3c, f568780: K2 keşifte geçersiz Unicode'u reddetme ve bozuk satırdan sonra sağlam satırı işleme testi.
- 102269e, f629bde: normalize URL'nin UTF-8'e kodlanabilirliğini kontrol ve regresyon.
- abc239c, 73b61d9: URL sunucu adı yazdırılamayan karakter doğrulaması ve test.
- b97b8bc, a5bd63c: K2→K3 aktarılan metadata'nın canonical kırpılmış biçimi ve test.
- 9d54308, 475733b: aktarım metadata'sında Unicode surrogate reddi ve test.
- 6477dc3: alternatifin kendisi alternatifse ana kaynak olarak kullanmayı reddetme.
- 7b1bac6, 888137f: alternatif ilişki SHA-256 kimliklerinin canonical biçimi ve test.
- 5b7f7e1, c63cb1b: probe/süreklilik/IBO kanıt anahtarlarının canonical SHA-256 biçimi ve test.
- 21bf6d1, 17e6299: probe/süreklilik/IBO kanıt haritalarında 20.000 sınırı ve test.
- 8c60ccc, 494b47a: doğrudan aktarımda aday/alternatif sayısı 20.000 sınırı ve test.

**Son görülen kendi test commit'i:** 73b61d90304b21c500f4fa8c1104a8d4ab2b8113. Paralel sohbetler main'e daha yeni commit'ler göndermiş olabilir; bunu HEAD sanma.

**Gerçek durum / eksikler:** Kod ve test dosyaları GitHub'a kaydedildi, ancak son commit'ler için başarılı test koşusu doğrulanmadı. 22 Ekim GitHub Actions geçmişinde eski commit'lere ait başarılı offline unit test koşuları var; bunlar güncel main'in yeşil olduğu anlamına gelmez. Birleştirme sonrası ilk iş: tüm yeni testleri gerçekten çalıştır, hataları düzelt, K1–K5 entegrasyon kapılarını ve K2–K3 gerçek uçtan uca kabulünü doğrula. 92 eski workflow davranışsal eşdeğerliğinin ve 99 workflow envanterinin tamamlandığını varsayma; bağımsız kanıt gerekir. Üretim playlist/EPG/XMLTV/logolar/favoriler/arşiv/yedekler korunacak; canlı stream probe ve workflow tetiklemesi açık onay olmadan yapılmayacak. [skip ci] ile işlenen commit'ler CI kanıtı sayılmaz.
