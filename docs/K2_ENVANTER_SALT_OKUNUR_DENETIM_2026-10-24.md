# K2 — Salt okunur 1.039 kayıt envanter denetimi (24 Ekim 2026)

## Kaynak ve yöntem
- İncelenen kaynak: `main:MADSC55_TV_IBO_CALISANLAR_TEST.m3u8`.
- Depodaki dosya metni üzerinde `#EXTINF:` satırları, HTTP(S) adres satırları, tam URL eşitliği, `#EXTINF` sonrası görünen kanal adları ve metadata alanlarının varlığı sayıldı.
- Bu inceleme ağ isteği, oynatma, codec/çözünürlük ölçümü, DRM kontrolü veya yayın hakkı doğrulaması yapmaz. Yayın URL'leri rapora yazılmadı.

## Gözlenen sayımlar

| Kontrol | Sayı |
|---|---:|
| `#EXTINF` kanal kayıtları | 1.039 |
| HTTP(S) URL satırları | 1.039 |
| Benzersiz tam URL | 376 |
| Tekrarlanan URL satırı (ilk görünüm hariç) | 663 |
| Benzersiz görünen kanal adı | 382 |
| Tekrarlanan görünen kanal adı (ilk görünüm hariç) | 657 |
| Boş/eksik `tvg-id` alanı | 331 |
| Dolu `tvg-id` kaydı | 708 |
| Benzersiz dolu `tvg-id` | 106 |
| HTTPS URL satırı | 784 |
| HTTP URL satırı | 255 |
| Boş/eksik `tvg-logo` alanı | 0 |
| Boş/eksik `group-title` alanı | 0 |
| HTTP(S) olmayan yorum dışı satır | 0 |

**Önemli:** Tam URL tekrarları aynı kanalın farklı bölgesel varyantları veya amaçlı çoğaltılmış girdileri de içerebilir. Kanal adının aynı olması da tek başına birleştirme gerekçesi değildir. `tvg-logo` ve `group-title` sayıları yalnızca boş olmayan tırnaklı alanın varlığını gösterir; logo erişilebilirliğini veya grup doğruluğunu göstermez. URL'ler hassas token içerebileceği için yayımlanmaz.

## K2 kabul durumu
- Kaynak dosya ve 1.039 kayıt sayısı: **depo üzerinde doğrulandı**.
- Mükerrerlik: **tam URL ve görünen ad düzeyinde salt okunur sayım**.
- Kanal kimliği/EPG eşleştirmesi: **331 boş/eksik tvg-id kaydı nedeniyle insan incelemesi gerekli**.
- Canlı yayın erişimi, çözünürlük, codec, hak/yeniden dağıtım izni ve cihaz kabulü: **doğrulanmadı**.
- Üretim listesi değişikliği, otomatik ekleme veya URL probe: **yapılmadı**.
