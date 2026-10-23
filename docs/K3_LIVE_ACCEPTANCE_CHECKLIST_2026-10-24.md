# K3 — Canlı yayın kabul kontrol planı (2026-10-24)

Durum: AÇIK / henüz üretim kabulü yok.

## Doğrulanan kanıt
- Offline CI run 40028406877, job 120670385942: completed/success; checkout commit 8884b1c6fa1a66c0996a1cd6ecc4254eec044869.
- `madsc/epg.py` yapısal M3U/XMLTV kontrolü yapar; `device_verified=False` döndürür.
- `tests/test_epg.py` regresyon testleri depoda mevcut.
- Bu kanıtlar gerçek HLS görüntü/ses veya 6 saat sürekliliği doğrulamaz.

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
Workflow dosyalarının gerçek yollarını keşfet; canlı pilotun sadece açıkça yetkilendirilmiş, güvenli test kaynaklarına eriştiğini doğrula. Sonra kontrollü pilot için ayrı kanıt topla.
