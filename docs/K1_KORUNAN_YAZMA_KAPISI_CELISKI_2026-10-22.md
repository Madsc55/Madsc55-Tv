# K1 kritik çelişki: korunan yazma kapısı ve beş çağrılan betik

Kaynak `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`; kod doğrudan okundu. Çalıştırma yapılmadı.

## Korunan kapı: `tools/protected_write_gate.py`

`blocked_paths()` **`CALISANLAR.m3u` dahil tüm `.m3u` ve `.m3u8` dosyalarını** reddeder. `git_changed_paths()` commit farkı, staged/unstaged, untracked ve ignored dosyaları da denetler. `--base` karşılaştırma hatasında fail-closed davranır. Bu kontrol bir onay sistemi değil, yasaklı yol kontrolüdür.

**Kritik çelişki:** `madsc-ibo-6115-second`, `madsc-ibo-ilk-239`, `madsc-ibo-kararlar-grup1`, `madsc-ibo-second-voice`, `madsc-turk-kanal-geri-sec`, `madsc-yedek-turk-ayir`, `madsc-yedekler-sayi-duzelt` workflow'ları `CALISANLAR.m3u` dosyasını stage edip kapıyı çağırır. Gerçek bir M3U değişikliği varsa kapı `DENY` verir; bu kod yolları mevcut haliyle başarılı bir korunan liste push işlemini gerçekleştiremez. Bu, statik kod mantığı sonucudur; koşu kanıtı değildir. Kapı atlatılmamalı; ihtiyaç varsa kullanıcı onayı ve ayrı güvenli yayın tasarımı gerekir.

## Betikler

- `scripts/keep_turkish_backups.py`: `CALISANLAR.m3u`, keşif arşiv CSV ve `YABANCI_KANALLAR.m3u` okur. İlk iki yedeği korur, kaynak/isim işaretleriyle Türk adayları tutar, yabancı ve belirsizleri tarihli M3U snapshot'a ayırır; ana listeyi ve JSON raporunu yazar. Belirsizleri kesin yabancı diye etiketlemez. Kapı ana liste değişikliğini engeller.
- `scripts/recover_turkish_backups.py`: sabit tarihli snapshot, kaynak arşivi ve yabancı liste okur; iptv-org TR ülke M3U'sunu ağdan alır (35 sn); URL, tvg-id veya kaynak işaretine göre adayları yedeklere geri ekler; ana liste/CSV/JSON yazar. Ülke eşleşmesi oynatma kanıtı değildir. Kapı ana liste değişikliğini engeller.
- `scripts/sync_yedekler_category_count.py`: ana listedeki YEDEKLER grup etiketindeki sayıyı gerçek EXTINF adedine eşitler ve ana listeyi yazar. Kapı bu değişikliği de reddeder.
- `scripts/full_system_backup.py`: `git ls-files` ile izlenen dosyaları ve varsa ayar envanterini en çok 400 MiB tar.gz dosyasına alır; manifest SHA256 ile geçici dizine geri açıp byte eşitliğini denetler; JSON raporu üretir. Offsite veya kalıcı yedek değildir.

## Karar

1. Bu yazma yollarını eşdeğer ve çalışır kabul etme.
2. Kullanıcı onayı olmadan korunan M3U için kapı gevşetme veya canlı workflow çalıştırma.
3. Kontrollü fixture testinde beklenen `DENY` ve hiçbir üretim değişikliği olmadığını kanıtla.
4. Geçişte rapor üretimi, onay ve yayın işlemlerini ayrı güvenlik sınırlarında tasarla.

Davranışsal eşdeğerlik 0/92, güvenlik üretim kabulü 0/26.
