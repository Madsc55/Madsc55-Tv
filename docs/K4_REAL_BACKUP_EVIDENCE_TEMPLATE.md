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

## K4 kabulünde otomasyon ve test kanıtının sınırı (23 Ekim 2026)

- Başarılı genel offline CI: [39945650886](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39945650886), commit `fcfe7ea4ae26fa13ce33088e69739460dc2fb8da`. Bu yalnızca ilgili commit'in test sonucudur; daha sonraki HEAD için ayrı doğrulama gerekir.
- Gerçek harici yedek makbuzu, bağımsız harici restore ve 1/15 gerçek scheduler run kanıtı halen yoktur. CI veya yerel fixture bunların yerine geçmez.
- Harici hedef onaylanmadan gerçek veri aktarımı ve üretim zamanlayıcısı açılmaz.


## 23 Ekim 2026 — Güncel otomatik test doğrulaması

- [Actions 39963096390](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39963096390) `b57a53d93891adedd7a98397284ce8d13095f747` commit'inde **success**; `Offline Python regression suite` job adımı da **success**. Bu yalnızca ilgili commit için geçerlidir.
- [Actions 39965157273](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39965157273) `99524af0a038ba6cd5cf5cc96c24ce507fd43fa1` commit'inde **success**. Bu da üretim kabulü değildir.
- En son sorguda [Actions 39966437586](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39966437586) `b5719ac15e4aa1683f3561d0b6718491948f6459` commit'i için **queued** durumundaydı; sonucu başarı sayılmadı.
- K4-15/16/17/18 harici sağlayıcı makbuzu, gerçek restore, VOD/arşiv envanteri ve ayın 1/15 scheduler kanıtı olmadan **BEKLİYOR** kalır. Bu kayıt kabul bayraklarını değiştirmez.
