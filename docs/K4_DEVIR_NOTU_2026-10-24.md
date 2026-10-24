# K4 devir notu — 24 Ekim 2026

## Doğrulanmış kapsam
- PR #20: Google Drive preflight ve sentetik fixture kanıtları. Açık, merge edilmedi.
- PR #21: çevrimdışı 1/15 zamanlama önizlemesi, Europe/Stockholm DST gap/fold denetimi, idempotency key ve CLI dry-run testleri. Açık, merge edilmedi.
- PR #21 son commit: c0b0ba3854c8d674fcad66086a05fb9dc10d5009.
- Bu commit için GitHub Actions 40073166736 ve 40073169230 **cancelled**; başarı iddiası yok.
- Daha önce 248e38def13d03414bc138207b3e95acf47b94db commitinde 40072569431 ve 40072566216 başarılıydı; yalnızca o commit için geçerlidir.
- Google Drive fixture klasöründe sentetik Google Doc ve düz metin dosyası ile okuma/yazma ve SHA-256 karşılaştırması yapıldı. Üretim yedeği veya bağımsız restore kanıtı değildir.

## Kalan kabul kapıları
- K4-15: onaylı gerçek dış sağlayıcı yedeği, kaynak envanteri, manifest ve makbuz.
- K4-16: aynı gerçek yedeğin bağımsız izole geri yükleme ve negatif testleri.
- K4-17: izinli VOD/arşiv kapsam envanteri ve eşdeğerlik doğrulaması.
- K4-18: onaylı 1/15 üretim zamanlayıcısı, kilitleme, DST ve gerçek çalışma kanıtları.
- Başarı bayrakları kapalı kalmalı: external_storage_proven=false, production_restore_approved=false, production_writes=false, production_ready=false.

## Sonraki güvenli adımlar
1. PR #21 güncel commit CI çalışmasını yeniden kontrol et; iptalleri başarı sayma. CI yapılandırması ve tekrar tekrar iptal sebebini incele.
2. PR #20 ve #21'i birbirine karıştırmadan diff ve test kapsamını gözden geçir.
3. Yetki verilmeden üretim verisi aktarımı, GitHub secrets ekleme, cron etkinleştirme, gerçek restore veya PR merge yapma.
4. Üretim kabulünü yalnızca gerçek manifest, provider receipt, kaynak envanteri, restore kanıtı ve onay ile güncelle.

## Kalıcı kaynaklar
- https://github.com/Madsc55/Madsc55-Tv/pull/20
- https://github.com/Madsc55/Madsc55-Tv/pull/21
- https://github.com/Madsc55/Madsc55-Tv/actions/runs/40073166736
