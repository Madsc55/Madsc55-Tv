# K4 gerçek yedekleme ve geri yükleme — kabul kayıt şablonu

Bu dosya bir **şablondur**, gerçek yedekleme yapıldığını kanıtlamaz. Gizli anahtar, erişim URL'si, parola, kişisel veri veya üretim playlist içeriği buraya konulmaz.

## K4-15 — Harici yedek teslimi (BEKLİYOR)

- Sağlayıcı / bağımsız hedef türü: **henüz belirlenmedi**
- Kaynak kapsamı ve salt-okunur envanter kimliği: **kanıt bekleniyor**
- Başlama / bitiş zamanları, UTC: **kanıt bekleniyor**
- Gerçek iş kimliği ve sağlayıcı tarafından verilen teslim makbuzu: **kanıt bekleniyor**
- Manifest: göreli yol, byte, SHA-256; tam envanter ve ekstra/eksik dosya kontrolü: **kanıt bekleniyor**
- Gizli bilgileri ayıklanmış bağımsız denetim sonucu: **kanıt bekleniyor**

## K4-16 — Harici yedekten bağımsız izole restore (BEKLİYOR)

- K4-15 ile eşleşen harici nesne / yedek kimliği: **kanıt bekleniyor**
- Kaynaktan ve harici hedeften bağımsız temiz restore kökü: **kanıt bekleniyor**
- Gerçek restore işlem kimliği, zaman damgası ve çıkış kodu: **kanıt bekleniyor**
- Kaynak, harici yedek ve restore için ayrı kök/inode kontrolü: **kanıt bekleniyor**
- Tam dosya listesi, byte ve SHA-256 eşleşmesi; fazladan dosya yokluğu: **kanıt bekleniyor**
- Bozuk kopya / eksik dosya negatif testi ve üretime sıfır yazma kanıtı: **kanıt bekleniyor**

## K4-17 — VOD ve arşiv korunması (BEKLİYOR)

- Yetkili salt-okunur VOD/arşiv kapsam envanteri: **kanıt bekleniyor**
- Yetkili izole kopyada içerik, metadata ve saklama semantiği karşılaştırması: **kanıt bekleniyor**
- Üretim VOD/arşivine yazma, silme, taşıma veya yeniden adlandırma yapılmadığına dair inceleme: **kanıt bekleniyor**

## K4-18 — Ayın 1'i ve 15'i (BEKLİYOR)

- Gerçek yedekleme hedefi ve kimlik/yetki tasarımı: **henüz belirlenmedi**
- Saat dilimi, DST, ay sonu, tekrar çalıştırma ve hata/yeniden deneme sözleşmesi: **tasarım bekleniyor**
- Ayın 1'i gerçek scheduler run ID / artifact / exit code: **kanıt bekleniyor**
- Ayın 15'i gerçek scheduler run ID / artifact / exit code: **kanıt bekleniyor**

**Kritik ayrım:** `.github/workflows/madsc-04-yedek.yml` yalnızca fixture üzerinde izole deneme yapar; gerçek harici depolama yedeği veya 1/15 scheduler değildir. Test CI başarısı gerçek harici teslim ve restore yerine geçmez.

## Kabul kapısı

Dört bölümün tamamı bağımsız ve doğrulanabilir kanıtla tamamlanana kadar:

- `external_storage_proven=false`
- `production_restore_approved=false`
- `production_ready=false`
- Büyük veri aktarımı ve üretim restore: **DURDUR**
- IBO Player Pro cihaz kabulü: kullanıcı tarafından en son yapılacak

Gerçek depolama sağlayıcısı, yetkili hedef ve erişim onaylanmadan üretim verisi aktarımı veya zamanlayıcı etkinleştirilmez.
