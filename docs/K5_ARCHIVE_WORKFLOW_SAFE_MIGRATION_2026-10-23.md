# K5 — Güvenli arşiv otomasyonu geçiş sözleşmesi (2026-10-23)

Durum: tasarım ve kabul kriterleri; **uygulandı veya parity kabul edildi anlamına gelmez**.

## İncelenen kaynaklar
- `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_15_2026-10-23.md`: `madsc-ibo-354-classify.yml`, `madsc-ibo-364-355-364.yml`, `madsc-ibo-398-16-49.yml`; frozen legacy SHA `ca374df3b9585c0d76a078db9536150ebbc260f7`.
- Üç script de runner çalışma alanında `CALISANLAR.m3u` yeniden yazar; korunan M3U yazma kapısı yayınlamayı reddetmelidir. Bu davranış üretimde uzaktan push yapıldığını kanıtlamaz.

## Replacement için zorunlu sözleşme
1. **Salt-okunur girdi:** ana playlist, favoriler, EPG, logolar, arşiv ve yedekler hiçbir aşamada değiştirilmez. Kaynak dosya için işlem öncesi ve sonrası SHA-256 ile dosya kimliği kaydedilir. Kaynak symlink, beklenmeyen dosya türü veya yarış halinde fail-closed.
2. **Ayrı, izole taslak:** üretilen M3U arşivleri ve JSON rapor yalnız önceden izin verilmiş, boş, üretim dışı bir çıktı köküne yazılır. Çıktı kökü korunan ağaç altında olamaz; nofollow/exclusive oluşturma ve K1 yazma politikası uygulanır. Otomatik `git add/commit/push` yoktur.
3. **Deterministik sınıflandırma:** tam girdi sayıları sırasıyla 354, 364, 398 değilse işlemi durdur. 354 senaryosunda 1–2 korunur, 3–334 kullanıcı bildirimi ve 335–354 yabancı sınıflandırması olarak taslağa alınır. 364 senaryosunda 355–364; 398 senaryosunda 16–49 arşiv taslağına ayrılır. Bu sınıflandırmalar teknik yayın/kimlik doğrulaması değildir.
4. **Provenance:** rapor kaynak SHA, frozen legacy workflow/script SHA, fixture SHA, girdi ve çıktı kanal sayıları, korunmuş dosyaların SHA karşılaştırmaları, çalışma kimliği, başlangıç/bitiş zamanları ve başarısızlık nedenini içerir.
5. **Hata davranışı:** sayı uyuşmazlığı, bozuk M3U, geçersiz yol, symlink, kısmi yazma, timeout veya yetkisiz hedefte sonuç başarısızdır; kısmi taslaklar güvenli rollback ile temizlenir. CI artifact tanılama yüklemesi `if: always()` ile yapılır; gizli veri, token ve üretim playlist içeriği artifact'a eklenmez.
6. **Yetki ve ağ:** replacement CI için `permissions: contents: read` ve `actions/checkout persist-credentials: false`; ağ gerekmeyen sınıflandırma için ağ çağrısı yapılmaz. Gerekli olmayan secrets sağlanmaz.
7. **Terfi:** hiçbir taslak otomatik canlı listeye alınmaz. Ayrı açık onay, K1 güvenlik doğrulaması, kanal kimliği/oynatım kanıtı ve kullanıcı cihaz kabulü gerekir.

## Offline differential kabul matrisi
Her üç senaryo için ayrı sabit, üretim dışı fixture üzerinde legacy script yalnız izole kopyada, replacement yalnız izole kopyada çalıştırılmalıdır:
- Tam sınır sayısı, bir eksik/bir fazla, boş/bozuk EXTINF, duplicate ID, CRLF/LF, Unicode ve sıra korunması.
- Başarılı koşuda aynı seçilen indeksler, aynı sayılar, aynı sınıflandırma anlamı; JSON/CSV/M3U semantiği ayrı normalize edilip karşılaştırılır. Byte-level farklar açıkça belgelenir.
- Başarısız koşuda exit code, hata sınıfı, timeout/retry ve artifact varlığı karşılaştırılır.
- Her koşuda korunan girdilerin SHA-256 değerleri aynı kalır, yazma denemeleri K1 negatif testlerinde reddedilir.
- Bağımsız iki çalışma için commit SHA, fixture SHA, komut, çalışma ortamı ve artifact hash'leri kaydedilmeden `behavioral_parity_accepted` **false** kalır.

## K5 kabul engelleri
- Bu belge kod değişikliği veya çalıştırılmış test değildir. 45/92 statik kaynak incelemesi ve 0/92 davranışsal parity son doğrulanmış görev defteri tabanıdır; güncel sayaçlar yeni kanıtla ayrıca güncellenmelidir.
- K5-19/20/21/22 açık kalır. 0/26 bağımsız runtime güvenlik ve 0/22 ana görev kabulü yükseltilmez.
- Üretim dosyaları, eski depo ve PR #71 değiştirilmez.
