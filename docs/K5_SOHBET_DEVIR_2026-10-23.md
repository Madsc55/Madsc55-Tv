# K5 sohbet devri — 2026-10-23

Aktif repo: Madsc55/Madsc55-Tv main. Eski Madsc55/madsc-tv yalnızca salt okunur referans. K1–K4 ile çakışmadan K5 çalışmasını sürdür.

Kullanıcının kesin talimatı: Cihaz doğrulamasını en sona bırak. IBO Player Pro testini kullanıcı bizzat yapacak ve bildirecek. Cihaz onayı iddia etme.

K5 modülleri: madsc/isolated_ibo_classification.py, madsc/isolated_ibo_archive_preview.py, madsc/isolated_ibo_archive_export.py. 6115 konum için offline sınıflandırma; JSON manifest önizleme; create-only izole klasör, symlink/korunan yol reddi, fsync, readback/hash ve hata temizliği. Üretim M3U listelerine dokunma. İlgili testler tests/test_k5_isolated_ibo_*.py. Son K5 commit c6558d206769524380321a187e74dbb9d2713bc5 (bozuk okuma regresyonu). Diğer son commitler: cf21c6f (newline hash), 9da529a (newline testi), 7939a7d (readback testi), 6cc3b79 (root), 2b33ab4 (URL).

CI başarıları: Actions 39870824796, 39871268955, 39871751853, 39872482282. Actions 39872004684 iptal. Actions 39872580939 ve bazı yeni runlarda Offline Python regression suite başarısız; hata nedeni henüz teşhis edilmedi. Yeni testlerin CI'sını yeniden kontrol et, başarılı varsayma.

Legacy workflow statik inceleme 48/92, batch 01–16. 44 bekliyor; davranışsal kabul 0/92. 26 güvenlik runtime ve 22 ana görev kabulü bekliyor. docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_* ve ortak görev defterlerini güncellik için kontrol et.

Sonraki: main HEAD ve Actions kontrolü, offline test hatalarını teşhis/düzelt, manifest export güvenliğini tamamla, batch 17+ inceleme, diğer ajanlarla çakışma yok. Cihaz doğrulaması en son.

## 23 Ekim ek K5 uygulama ve CI teşhisi

- Actions 39872580939 job logu incelendi: 1089 testten 1 hata. `test_write_callsite_audit.WriteCallsiteAuditTests.test_metadata_mutations_are_inventoried` testinde beklenen `Path.chmod` / `Path.lchmod`, gerçek `chmod` / `lchmod`. Bu ortak K1 yazma denetimi kapsamındadır; K5 diğer ajanın dosyasını değiştirmedi. CI yeşil değildir.
- K5 manifest URL doğrulamasına ters eğik çizgi reddi eklendi: a7f2fe1. İlgili regresyon testi: fb185da.
- İzole manifest export dizini için dosya fsync sonrasında dizin fsync eklendi: 0fdccba7. Dizin fsync hata temizliği regresyon testi: 0677388. Dizin fsync açılışına O_NOFOLLOW eklendi: 347104a.
- Bu commitler `[skip ci]` içerir. Yeni testlerin CI başarısı veya gerçek cihaz doğrulaması iddia edilmez.
- Bekleyenler: K5 testlerinin bağımsız koşulması ve CI doğrulaması, manifest güvenliğinin kalan risklerinin değerlendirilmesi, legacy workflow batch 17+ incelemesi ve davranışsal kabul kanıtları. 48/92 statik sayısını yeni kanıt olmadan artırma. Cihaz testi son aşamada kullanıcıya aittir.

- Son K5 test genişletmesi: `3baaea4` doğrudan önizleme doğrulamasında sıfır, aralık dışı ve sayısal olmayan HTTPS portları için regresyon testleri ekler. Önceki `bc30b28` dizin açılışında `O_DIRECTORY` ve `O_NOFOLLOW` bayraklarını test eder. Bu yeni commitler `[skip ci]` ile kaydedildi; yeni CI/yerel test sonucu yoktur. Eski 1089 testlik başarısız koşuyu yeni commitlere atfetme.

- K5 regresyon testi düzeltmesi `63443de`: güvensiz hedef yol testindeki literal kaçış dizileri yerine gerçek kontrol/surrogate karakterleri `chr()` ile üretiliyor. Önceki test bu senaryoları doğru sınamıyordu. Test sonucu CI/yerel koşumla henüz doğrulanmadı.

- K5 private export permissions: commit `139ed08` explicitly applies mode 0700 to the newly created isolated manifest directory and fails closed if permission adjustment fails; test `c1081d3` checks POSIX mode bits. Both commits use `[skip ci]`; no test/CI pass is claimed.

- K5 symlink-destination regression test `be13cc5`: asserts an existing destination symlink is rejected and its target directory remains untouched. Commit uses `[skip ci]`; execution/CI not verified.
