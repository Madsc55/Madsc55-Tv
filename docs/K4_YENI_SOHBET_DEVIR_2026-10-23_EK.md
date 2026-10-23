# K4 yeni sohbet devir notu — 23 Ekim 2026 (ek)

## Depo ve sınırlar
- Repo: Madsc55/Madsc55-Tv; dal: main. K1–K5 paralel sohbetleri aynı dala yazıyor. Her değişiklikten önce güncel HEAD ve dosya SHA al; 409 olursa yeniden oku.
- K4: madsc/backup.py, madsc/k4_restore_gate.py, madsc/restore_drill.py, K4 testleri ve K4 dokümanları.
- Üretim playlist/EPG/XMLTV/logo/VOD/arşiv/favori/cihaz verisine dokunma. Gerçek provider erişimi, üretim restore ve cihaz testini başlatma. PR #71'i birleştirme. CI'ı manuel tetikleme.
- Gerçek harici yedek hedefi hâlâ seçilmedi. K4-15 harici teslim, K4-16 bağımsız harici restore, K4-17 VOD/arşiv kabulü, K4-18 ayın 1'i/15'i gerçek scheduler kayıtları **bekliyor**. production_ready=false.

## Bu sohbetin K4 commitleri
- 0d4b1ff: backup.py taşınabilir ara klasör alias denetimi.
- dc649ca: taşınabilir klasör alias regresyon testleri.
- f0b6ac8: eski kesin dosya/dizin çakışması hata sözleşmesini koru.
- 9440168: iç içe klasör alias testleri. CI 39958701547 başarılı.
- 5c9951c: geçerli iç içe klasörlerin snapshot/verify pozitif testi. CI 39959033394 başarılı.
- cc674d9: compare_copy için symlinkli üst dizin reddi. CI 39959424124 başarılı.
- 13d4139: compare_copy / verify_sandbox_restore symlink alias testi.
- e330de5: verify_independent_restore üç kök için symlinkli üst dizin reddi.
- fa7b9d3: üç köklü restore symlink alias regresyon testi.
- b10b3c0 ve c29b852: harici kabul kanıt şablonu ve CI kaydı.

## ACİL: CI KIRMIZI, ÖNCE BUNU DÜZELT
Son kontrol: GitHub Actions
- 39959626099 (fa7b9d3): **failure**
- 39959609860 (e330de5): **failure**
- 39959442528 (13d4139): **failure**
- 39959574944 (cad3c38): success (farklı commit)
Bu başarısızlıkların kök nedenleri **henüz incelenmedi**. Yeni sohbetin ilk işi üç failed run'ın job loglarını açmak, K4 kaynaklı hataları tespit edip minimal düzeltme ve regresyon testleri yapmak; ardından yeni main CI'ını doğrulamak. Başarı iddia etme.

## Devam sırası
1. Güncel main HEAD + Actions CI ve job logları; paralel K1–K5 değişikliklerini ayır.
2. K4 test hatalarını düzelt; başarılı otomatik CI sonucunu doğrula.
3. K4 manifest, no-follow, üç bağımsız kök, sandbox rollback ve güvenli output path testlerini gözden geçir.
4. Gerçek harici hedef/kimlik/yetki olmadan harici teslim veya üretim restore yapma; sahte kabul kanıtı üretme.
5. Kullanıcı IBO Player Pro cihaz kabulünü en son yapacak.

Ayrıntılı kabul şablonu: docs/K4_REAL_BACKUP_EVIDENCE_TEMPLATE.md
