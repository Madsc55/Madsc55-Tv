# HEPSI — Birleşik doğrulama devam kaydı (2026-10-23)

## Kanonik durum
- Depo: Madsc55/Madsc55-Tv.
- GitHub main kontrol edilen HEAD: `0a286ea23065cb43071026c75bebf899d0bd230d`.
- Son 6 Actions sorgusunda en son başarı `39861826787`, SHA `a4fbd23399318bde719db095de04ea3ee7d4913a`; bu güncel HEAD değildir. Yakın geçmişte birden çok başarısız/iptal koşusu da var. Actions yeniden tetiklenmedi.
- Kullanıcı ZIP'i mevcut main'den eski; ZIP'te görülen hatalar doğrudan güncel main hatası kabul edilmemeli.

## Güncel kaynak karşılaştırmasında görülen düzeltmeler
- `tests/test_candidate_probe_link.py` artık adaylara güvenli `name` metaverisi sağlıyor ve AST incelemesinde `ast.walk(parsed)` kullanıyor.
- `tests/test_handoff.py` süreklilik örnekleri 10:00, 16:00, 22:00 UTC; her aralık 6 saat.
- `tests/test_k5_head_observation.py` ve `tests/test_probe_target_gate.py` güncel kaynakta eski ZIP'teki yalın aday fixture'larından farklı; eski hata bunlara kopyalanmamalı.
- `tests/test_legacy_retest_differential_batch.py` test saati dondurma düzeltmesi GitHub commit `b72e23bad5495658bf1f1bfb42ff63782df9743a` ile kaydedildi.
- `tests/test_k3_live_manifest_source_snapshot.py` syntax düzeltmesi commit `8f138e30d536e686ceac7cb15af6928dceeadfae` ile kaydedildi.

## Eski ZIP yerel tarama sonucu (tarihsel; güncel main sonucu değildir)
- 150 test dosyası 10 modüllük gruplarla taranırken ZIP'in eski kodu nedeniyle hata grupları bulundu: aday metaverisi fixture'ları, K3 üç aşamalı süreklilik zaman aralıkları, K3 loader AST test beklentisi, K5/legacy test farkları.
- Güncel main dosyalarıyla karşılaştırınca bu bulguların bir kısmı zaten düzeltilmiş; ZIP sonuçları kanonik test kabulü değildir.
- Legacy differential hedefli test yerel ZIP'te 1/1 geçti; bu sadece ZIP kopyasında testtir.

## Kabul sayaçları — değişmedi
- 92 eski workflow davranışsal eşdeğerlik: 0/92 kabul.
- 26 güvenlik kuralı: 0/26 bağımsız kabul.
- 22 ana görev: 0/22 bağımsız kabul.
- Hiçbir kaynak dosyası veya CI sonucu, canlı üretim davranışını tek başına kanıtlamaz.

## Güvenlik ve sonraki işler
- Üretim IPTV/EPG/favoriler/cihaz verileri/yedekler/arşivler değiştirilmedi; PR #71 birleştirilmedi; Actions tetiklenmedi.
- Sıradaki adım: güncel main'in kaynak/test snapshot'ını tutarlı biçimde dışa aktarıp hedefli grupları tekrar çalıştırmak; son başarılı CI SHA'sı ile main HEAD arasındaki farkı belirlemek; kalan CI failure loglarını ve 99 workflow/92 davranış sözleşmesini kanıtla incelemek.
