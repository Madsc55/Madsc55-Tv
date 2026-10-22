# Son altı eski workflow — kaynak notları

Kaynak depo `Madsc55/madsc-tv`, sabit revizyon `ca374df3b9585c0d76a078db9536150ebbc260f7`.

- `vod-guncelle.yml`: Günlük 07:17 UTC veya manuel. VOD JSON üretimi, koruma kontrolü, commit ve push. Gerçek depo yazma yetkisi var.
- `yedek-geri-yukleme-tatbikat.yml`: Yalnız izole restore dry-run ve JSON artifact; üretime geri yükleme değildir.
- `yedekler-yeniler-medya-kontrol.yml`: ffprobe ile iki kategori medya denetimi, CSV ve JSON raporları, 70 dakika sınır.
- `yeni-aday-on-test.yml`: Aday bağlantı/logo ön testi, CSV artifact, salt okunur.
- `yeni-kanal-arama-2026.yml`: SCAN_BATCH=1 ile aday tarama, CSV ve hata artifact, salt okunur.
- `yeniler-guvenli-arama.yml`: Önce 90 günlük kaynak keşfi, ardından 34–99 arası 66 matrix tarama işi ve ayrı artifact; gerçek çalıştırma yapılmadı.

Envanter `docs/LEGACY_SOURCE_SCOPE.json`: 99 kayıt ve 99 benzersiz yol. Önceki inceleme belgeleriyle tekil dosya bazında mutabakat henüz tamamlanmadı. Çağrılan Python betikleri ayrıca analiz edilmeli. Davranışsal kabul 0/92; güvenlik üretim kabulü 0/26.
