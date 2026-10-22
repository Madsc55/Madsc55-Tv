# MADSC55-TV — K1–K5 kurulum ve kabul ayrımı (22 Ekim 2026)

Bu belge yalnızca mevcut GitHub dosyalarından doğrulanmış statik kurulum envanteridir. Canlı Actions çalışması, yayın, cihaz veya üretim kabulü değildir.

| Kademe | Ana workflow | Statik kurulum | Gerçek çalışma engeli |
| --- | --- | --- | --- |
| K1 güvenlik | .github/workflows/madsc-01-guvenlik.yml | workflow_dispatch, salt okunur izin, izole parity hook | 26 güvenlik kuralı çalışma zamanı kanıtı |
| K2 keşif | .github/workflows/madsc-02-kesif.yml | workflow_dispatch, opt-in ağ keşfi ve geçmiş | Gerçek kaynak mutabakatı, günlük üretim döngüsü |
| K3 kanal testi | .github/workflows/madsc-03-kanal-test.yml | workflow_dispatch, opt-in sınırlı canlı test | Gerçek aday akışı, medya/kimlik ve IBO cihaz testi |
| K4 yedek | .github/workflows/madsc-04-yedek.yml | workflow_dispatch, izole restore/parity hook | Gerçek dış restore kanıtı |
| K5 bakım | .github/workflows/madsc-05-bakim.yml | workflow_dispatch, toplu bakım/kabul hook | 92 eski davranışın bağımsız eşdeğerlik kanıtı |

## Kanıtlı ve kanıtsız ölçülerin ayrımı
- **5/5** ana workflow dosyası mevcut: yalnızca statik kurulum varlığı, üretim devreye alımı değil.
- **99/99** eski YAML kaynak envanteri; **92** davranış kapsamda, **7** kapsam dışı.
- **0/92** bağımsız davranışsal kabul; **0/26** çalışma zamanı güvenlik kabulü; **0/22** görev kabulü. Bunlar kod tamamlanma oranı değildir.
- Önceki **%60 tamamlandı / %40 kaldı** kullanıcıya bildirilen genel proje tahminidir; GitHub'da tekrar hesaplanmış ağırlıklı metrik bulunmadığından güncel doğrulanmış oran diye kullanılamaz.
- Beş ana workflow'un workflow_dispatch tabanlı olması **günlük otomatik üretim devrinin kurulu olduğunu kanıtlamaz**.
- K2/K3 canlı kaynaklar ve K4 dış restore, K5 legacy pair/artifact kanıtları açık.
- IBO Player Pro cihaz doğrulaması kullanıcıya aittir.

## Tek toplu bitirme kapısı
1. Mevcut 22 görev defterinin her maddesini ilgili K1–K5 workflow ve kanıt kaynağıyla bağla; statik kod ile çalışma zamanı kabulünü ayır.
2. Offline gate'i güncel HEAD üzerinde gerçekten çalıştır, test sayısı ve hata çıktısını kaydet. Önceki yeşil run'ları yeni commitlere otomatik aktarma.
3. İzinli gerçek K1–K5 çalışma kanıtlarını aynı-input eski/yeni run, artifact baytları, SHA256, yan etki ve köken karşılaştırmasına bağla.
4. K2/K3 canlı veri, K4 dış restore ve IBO cihaz bağımlılıklarını ayrı açık blokaj olarak göster.
5. Ancak bağımsız kanıt sağlandığında 92/26/22 kabul sayılarını artır. Korunan IPTV listelerine, EPG/logo/yedek/favorilere, eski depoya, PR #71'e ve izinsiz Actions'a dokunma.

Bu envanter üretim hazır onayı vermez; yeni sistemde var olan kod ve henüz doğrulanmamış çalışmayı birbirine karıştırmaz.
