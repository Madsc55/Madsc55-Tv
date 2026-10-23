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

## 23 Ekim 2026 — GitHub kaynaklarından bağımsız kanıt taraması

- Denetlenen `main` HEAD: `e59a1ee2d4abae45a7f3efb1bbd6eb314dbbf4fa` (kontrol anı; paralel commitlerle değişebilir).
- Doğrudan incelenen `.github/workflows/madsc-04-yedek.yml`: yalnız `workflow_dispatch` tetikleyicisi vardır; gerçek ayın 1'i/15'i cron tanımı yoktur. `K4_EXTERNAL_BACKUP_ENABLED=false` ve `K4_PRODUCTION_RESTORE_ENABLED=false` değerleri doğrulanır. Oluşturulan `reports/k4-source/nested/sample.txt` dosyası test fixture'ıdır; `madsc-k4-restore-drill` ve `madsc-k4-isolated-evidence` artifact'ları harici sağlayıcı teslim makbuzu değildir. Parity manifest artifact'ı da yalnız açık opt-in fixture kanıtıdır.
- GitHub Actions `40021230720`, commit `002d1e6cfaff31b9deaeb7b678aa3ccf6968169b`: `success` (genel offline CI); bu çalışma harici depolama teslimi veya gerçek restore kabulü değildir. İnceleme anındaki `main` çalışması `40022282596` henüz `in_progress` idi.
- İncelenen yakın tarihli genel Actions çalışmaları arasında adı/yolu K4 yedek workflow'u ile eşleşen çalışma bulunamadı. Bu, tüm tarihsel çalışmaların eksiksiz tarandığı anlamına gelmez; gerçek K4 fixture artifact'ı varmış gibi beyan edilmez.
- **K4-15:** Harici sağlayıcı/bağımsız hedef, sağlayıcı makbuzu, gerçek nesne kimliği ve gerçek kaynak manifesti bulunmadı — **kanıt yok / BEKLİYOR**.
- **K4-16:** Aynı harici nesne kimliğinden temiz izole hedefe restore run ID, çıkış kodu ve üçlü bütünlük karşılaştırması bulunmadı — **kanıt yok / BEKLİYOR**.
- **K4-17:** Yetkili gerçek VOD/arşiv kapsam ve bağımsız karşılaştırma kanıtı bulunmadı — **BEKLİYOR**.
- **K4-18:** 1 ve 15 günlerine ait gerçek zamanlayıcı run/artifact kanıtı yok; mevcut workflow'da schedule tanımı da yok — **BEKLİYOR**.
- Sonuç: `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false`, `production_writes=false`. Üretim playlist/EPG/VOD/arşiv dosyalarına yazılmadı, workflow dispatch/rerun yapılmadı.
- Gerçek kabul için gerekli sonraki bağımlılık: kullanıcı tarafından yetkilendirilmiş bağımsız harici hedef/sağlayıcı, salt-okunur kaynak kapsamı ve gizli bilgileri ifşa etmeyen gerçek teslim makbuzu; ardından aynı harici yedekten ayrı izole restore kanıtı. Bu kanıtlar oluşmadan kabul bayrakları değiştirilemez.

## 23 Ekim 2026 — Actions ilk 100 kayıt üzerinde ilave tarama

- GitHub REST `actions/runs?per_page=100` yanıtında `total_count=1059` ve dönen ilk 100 çalışma içinde workflow adı veya yolu `k4`, `yedek` ya da `backup` ile eşleşen **0 çalışma** bulundu. Bu **yalnızca ilk 100 kaydın** kapsamıdır; geçmiş 1059 çalışmanın tamamı incelendiği iddia edilmez.
- İlk 100 kayıttaki en son tamamlanmış başarılı genel CI: `40022310560`, commit `cd963633ed909bf9b8acf5e64db629cd4114055b`. Bu bir K4 dış-depolama teslim makbuzu değildir.
- Tarama sırasında `40022533383` pending ve `40022512400` in_progress idi; sonuçları başarılı sayılmadı.
- Harici depolama sağlayıcısı tarafından imzalanmış teslim makbuzu veya nesne kimliği ile aynı nesneden yapılmış bağımsız restore çalışması hâlâ sunulmadı. K4-15/K4-16 **BEKLİYOR**, `external_storage_proven=false`, `production_restore_approved=false`.

## 23 Ekim 2026 — Son durum doğrulaması (aynı gün)

- `main` SHA `09cd66dc2ee2d6d04d6830e8dbd69f0ad2146634` gözlendi; GitHub Actions `40022533383`, `40022512400`, `40022310560`, `40022282596` genel CI çalışmaları `success` olarak tamamlandı. Bunlar gerçek harici yedek teslimi veya bağımsız geri yükleme makbuzu değildir.
- İlk 100 Actions çalışmasında K4/yedek/backup workflow ad/yol eşleşmesi **0**; bu sonuç toplam `1059` kaydın tümü için genellenemez.
- Bağımsız harici hedef, gerçek yedek nesne kimliği, sağlayıcı teslim makbuzu ve aynı nesneden temiz hedefe geri yükleme kanıtı bulunamadı. K4-15/16/17/18 **BEKLİYOR**; `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false`.
- Yalnızca kanıt defteri güncellendi; gerçek harici yedek, gerçek restore, workflow dispatch veya üretim yazması yapılmadı.

## 23 Ekim 2026 — Kullanıcı onaylı GitHub yedek hedefi

- Kullanıcı **ayrı ve özel** `Madsc55/Madsc55-Tv-Backup` GitHub deposunu K4 harici yedek hedefi olarak onayladı; K1–K5 sisteminin diğer uygun yedeklerinin de burada tutulmasını istedi.
- Mevcut GitHub bağlantısında **yeni repository oluşturma yeteneği sunulmadığı** için bu depo bu oturumda oluşturulamadı; **var olduğu doğrulanmadı**. Yedek yükleme, senkronizasyon, harici teslim makbuzu veya restore yapılmadı.
- Planlanan bölümler: `k1/`, `k2/`, `k3/`, `k4/`, `k5/`, `manifests/`, `restore-evidence/`. Bu yollar yalnız taslaktır; GitHub'da oluşturulmuş oldukları iddia edilmez.
- Yedek kapsamı öncesinde veri sınıflandırması, erişim denetimi, şifreleme ve boyut/kota kontrolü zorunludur. Sırlar, tokenlar, kullanıcı kimlik bilgileri, özel kaynak URL'leri, yetkisiz VOD/arşiv içeriği veya hassas üretim verileri şifresiz olarak commit edilmez. GitHub Git deposu büyük ikili arşivler için sınırsız depolama değildir.
- Kabul sırası: (1) `Madsc55-Tv-Backup` özel repo oluşturulup erişim doğrulanır; (2) izinli verilerden gerçek yedek ve SHA-256 manifesti yüklenir; (3) GitHub commit/nesne SHA'sı ve zaman damgası kaydedilir; (4) **aynı nesne** temiz ve bağımsız geçici hedefe çekilip yeniden hash'lenir; (5) kaynak/yedek/restore eşitliği ve kapsam kanıtı kaydedilir; (6) gerçek 1/15 takvim çalışmaları ayrıca kanıtlanır.
- Şu an `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false`; yalnızca hedef seçimi onaylandı.

## 23 Ekim 2026 — Özel GitHub hedefi doğrulandı

- `GET /repos/Madsc55/Madsc55-Tv-Backup`: `private=true`, `default_branch=main`, mevcut bağlantıda `push=true` doğrulandı. Önceki 404 erişim engeli kalktı.
- Boş özel depoya güvenlik/kabul yönergelerini içeren `README.md` eklendi: commit `af40e0da1d4eb55f3a5a5321132773818ef18d25`.
- **Bu commit gerçek yedek değildir.** Henüz kaynak dosya aktarımı, SHA-256 gerçek içerik manifesti, GitHub'a yedek teslim makbuzu veya temiz hedefte restore doğrulaması yapılmadı.
- K4-15/16/17/18 bekliyor; `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false`.

## 23 Ekim 2026 — İlk gerçek özel GitHub dosya yedeği (sınırlı kapsam)

- Kaynak `madsc/k4_restore_gate.py` özel `Madsc55/Madsc55-Tv-Backup` deposunda `k4/madsc/k4_restore_gate.py` yoluna gerçekten yazıldı: commit `911fbe4e3882ad341add6f9d9f7c335677aa29b0`.
- Kaynak ve hedef Git blob SHA-1: `d4f8b574dcc12c04c62d3219d2fadad103d51726`. Hedef GitHub'dan yeniden okundu; kaynakla içerik eşitliği `true` doğrulandı.
- Özel depoda kanıt notu `restore-evidence/K4_READBACK.md`: commit `746eeda6dac807d54ecbbbd0edcee66bfb02e5cc`.
- Bu **tek bir kaynak kodu dosyasının** gerçek depo-dışı kopyası ve geri okumasıdır; SHA-256 manifesti, tam K1–K5 yedeği, bağımsız temiz hedef restore'u, gerçek VOD/arşiv veya zamanlayıcı kanıtı değildir. İki depo aynı GitHub sağlayıcısında olduğu için sağlayıcıdan bağımsız felaket kurtarma sayılmaz.
- K4-15 tam kapsam **BEKLİYOR**; K4-16/17/18 **BEKLİYOR**. `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false`.

## 23 Ekim 2026 — K4 özel depoya gerçek kod/test/workflow kopyaları

- Özel hedef: `Madsc55/Madsc55-Tv-Backup` (`private=true`). Her dosya kaynak `main` üzerinden okunup özel depoya yazıldı; hedef tekrar okunarak Git blob SHA ve içerik eşitliği doğrulandı.
- `madsc/backup.py` -> `k4/madsc/backup.py`: commit `4a6a326d18ef44219848843fd048c032180f2756`, blob/content eşit.
- `tests/test_k4_restore_gate.py` -> `k4/tests/test_k4_restore_gate.py`: commit `4b22390c5e6b3f62e2fd24702332832764745506`, blob/content eşit.
- `.github/workflows/madsc-04-yedek.yml` -> `k4/.github/workflows/madsc-04-yedek.yml`: commit `5d7960ff4ace80d6d33738bcb6bb7eae77acb132`, blob/content eşit.
- Önceki `madsc/k4_restore_gate.py` kopyası dahil **dört K4 dosyası** yedeklendi. Git blob SHA-1, ayrıca talep edilen SHA-256 manifestinin yerine geçmez.
- Eksikler: atomik tam kaynak snapshot ve kapsam manifesti, SHA-256, bağımsız temiz ortam restore, gerçek VOD/arşiv kapsamı, gerçek 1/15 scheduler, K1–K5 diğer uygun dosyaları. `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false` korunur.

## 23 Ekim 2026 — K4 test ve restore kodu yedek kapsamı genişletildi

- Sabit kaynak commit `adb6cf636a5fcf88e0a2a2c090646b2d48ff9467` üzerinden üç dosya `Madsc55/Madsc55-Tv-Backup` özel deposuna aktarıldı; her biri hedef depodan yeniden okunarak içerik ve Git blob SHA eşitliği doğrulandı.
- `tests/test_backup.py` -> `k4/tests/test_backup.py`; yedek commit `a9c051890ec7c26ea53bf44435a5935e3a9f896d`; Git blob `936a34136e3b25199f9a6051e0bb9629ed50e482`.
- `tests/test_backup_manifest_hardening.py` -> `k4/tests/test_backup_manifest_hardening.py`; yedek commit `af63ca8e032f9b25c0b97b2bfdd4e36c1083ee6b`; Git blob `47a0d82487842a25199d24f37d231cf090f3ef925c`.
- `madsc/restore_drill.py` -> `k4/madsc/restore_drill.py`; yedek commit `28f23a0973dfb2151622ad103990465e322922f6`; Git blob `a9cd3f74f888a636ce624a4b6fd89f668c0f14bd`.
- Önceki dört dosyayla toplam **yedi K4 dosyası** gerçek özel depoya kopyalanıp geri okundu. Bu **tam sistem snapshot'ı değildir**; SHA-256 manifesti ve bağımsız restore henüz yoktur.
- K4-15/16/17/18 tamamlanmadı. `external_storage_proven=false`, `production_restore_approved=false`, `production_ready=false`.
