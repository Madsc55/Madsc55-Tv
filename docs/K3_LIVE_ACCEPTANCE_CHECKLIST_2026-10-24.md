# K3 — Canlı yayın kabul kontrol planı (2026-10-24)

Durum: AÇIK / henüz üretim kabulü yok.

## Doğrulanan kanıt
- Offline CI run 40028406877, job 120670385942: completed/success; checkout commit 8884b1c6fa1a66c0996a1cd6ecc4254eec044869.
- `madsc/epg.py` yapısal M3U/XMLTV kontrolü yapar; `device_verified=False` döndürür.
- `tests/test_epg.py` regresyon testleri depoda mevcut.
- Bu kanıtlar gerçek HLS görünt/ses veya 6 saat sürekliliği doğrulamaz.

## Canlı pilot dosyaları keşfedildi (main)
- `.github/workflows/madsc-k3-live-manifest-pilot.yml` — blob `1ea9fe8f31c891bc1bb2e95451d3c243f53c02d9`; `workflow_dispatch` var, candidate limit 12/75; çalıştırıldığına dair bu turda kanıt yok.
- `madsc/k3_live_manifest_pilot.py` — blob `3ecfee30acd36c149534c7a41e6cac8c3bb22bb9`; harici herkese açık Türkçe M3U kaynağından sınırlı HTTPS adayları alıyor; DNS/IP hedef kontrolleri, TLS için sabitlenmiş IP, redirectsiz curl ve URL hash raporu kullanıyor. Kod açıkça `audio_video_verified=False` raporlar; bu sadece manifest erişim pilotudur.
- `.github/workflows/madsc-k3-turkish-tv-video.yml` — blob `18296862c040ab30bc846e2b3cf3dd73e5ea99c0`; `workflow_dispatch` var; ffprobe ile sınırlandırılmış video/ses denemesi.
- `madsc/k3_turkish_tv_video_pilot.py` — blob `489572833bcc44d8941017e8c08b36b66b62ecf9`; HLS manifesti, aynı kaynak alanındaki segmenti ve ffprobe stream türlerini denetlemeyi hedefliyor. Bu workflow da çalıştırılmış sayılmaz.
- `.github/workflows/madsc-online-pilot-gates.yml` — blob `c3365cdd0654e56e2e561244fb1506df1a583303`; offline gate başarılı olursa online K2/K3 adımlarını çalıştıracak birleşik workflow. Bu turda dispatch yapılamadı.
- İlgili kaynaklar `main` üzerinden okundu; bu bir kod incelemesidir, çalışma sonucu değildir.

## Açık kabul kapıları
1. **Canlı HLS:** Yetkili test kanallarında HTTPS manifest, master/media playlist, segment erişimi, video codec ve ses akışı; sonuçları zaman damgalı, kişisel erişim tokenlarını maskeleyerek kaydet.
2. **Süreklilik:** Aynı yayın için bağımsız en az 6 saat ölçüm; kopma, yeniden bağlanma ve kesinti sürelerini kaydet.
3. **Pages/XMLTV:** Gerçek yayın URL'leri, HTTP durumları, XMLTV şeması, EPG zaman aralığı, tvg-id eşleşmeleri.
4. **Kimlik/logo:** Kanal adları, logo URL'leri ve doğru kanal eşleşmesi; kaynakları değiştirmeden incele.
5. **IBO Player Pro:** Yalnızca yukarıdakilerden sonra, kullanıcı cihazında manuel kabul; kullanıcı sonucu bildirene kadar açık.

## Güvenlik sınırları
- Üretim M3U/XMLTV, favori, logo, yedek, arşiv ve cihaz verilerine dokunma.
- PR #71'i otomatik birleştirme.
- Workflow dosyasının tam yolu doğrulanmadan manuel çalıştırıldığını iddia etme.
- Offline CI başarısını canlı yayın kabulü sayma.
- K3-13 açık kalsın.

## Sonraki işlem
Workflow dosyaları bulundu. Sonraki adım GitHub Actions üzerinden `madsc-k3-live-manifest-pilot.yml` (limit 12) ve sonra video pilotunu yetkili şekilde dispatch edip artefakt raporlarını incelemek. Bu sohbetin mevcut GitHub araçları workflow_dispatch başlatamadığı için, run oluşmadan pilot başarılı/başarısız diye raporlama.
