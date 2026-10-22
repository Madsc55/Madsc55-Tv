# K4 — yeni sohbet devir notu (23 Ekim 2026)

## Kesin talimat
Kullanıcı cihaz doğrulamasını **en sona** bıraktı. IBO Player Pro gerçek cihaz testini kullanıcı kendisi yapacak ve sonucu bildirecek. Cihaz kabulünü veya üretim hazır oluşunu önceden onaylama. Kalan yazılım hatalarını, güvenlik, yedekleme/geri yükleme, test ve entegrasyon eksiklerini gidermeye devam et.

## Depo ve eşzamanlı çalışma
- Kanonik GitHub: `Madsc55/Madsc55-Tv`, `main`. Eski `Madsc55/madsc-tv` salt okunur.
- Beş paralel sohbet: K1–K5. Bu sohbet K4; öncelikli sahiplik: `madsc/backup.py`, `madsc/k4_restore_gate.py`, `tests/test_backup_manifest_hardening.py`, `tests/test_k4_restore_gate.py`, K4 kanıt/devir belgeleri.
- Her yazmadan önce main'deki güncel dosyayı ve blob SHA'yı yeniden oku. Başkalarının dosyalarını/commit'lerini ezme. Küçük ve kapsamlı commit'ler yap. Workflow'ları manuel tetikleme.
- Üretim playlistleri `CALISANLAR.m3u`, EPG/XMLTV, logolar, favoriler, cihaz bilgileri, dış arşivler, üretim verileri değiştirilmeyecek. Gerçek provider çağrısı, canlı cihaz testi, üretime restore yok. PR #71 birleştirilmesin.

## Bu sohbetin tamamlanan K4 çalışmaları
- `5dfb571a`: kaynak manifesti okunurken inode/metadata/boyut değişirse güvenli ret; `9299b18d` regresyon testi.
- `653b531a`, `205ad1bf`: üç sandbox kökünde fazladan dosya/dizin/symlink reddi ve testler.
- `019a7aa4`, `95d53b1f`: iç içe klasörlerin kanonik envanteri ve testler.
- `ba8bcb26`, `877fab8d`: symlink'li üst dizinleri reddetme ve test.
- `83ed0d87`: backup testlerindeki hatalı Python çok satırlı `with` sözdizimi düzeltmesi.
- `36155ba9`, `8d72483b`: sandbox taramasına 20.000 öğe sınırı ve regresyon testi.
- `827818b8`, `41a61d61`: bildirilen envanterin sınırını dosya hash'inden önce denetleme ve test.
- `f039fa61`, `64d0db5c`, `acf31b5d`: klasör genişlemesini kademeli sınırlandırma ve gerçekçi regresyon verisi.
- `c59bd4bf`: önceden doğrulanmış klasör envanterini tekrar kullanma.
- `5702f1b1`, `02fcaa9e`, `e38ae28c`: güvensiz dosya yolları (traversal, kontrol karakteri, backslash) için erken ret ve test.

## Son doğrulanmış CI / açık sorun
- 23 Ekim 2026 itibarıyla en son incelenen main HEAD: `07af92ae93c579eaf9f7ce68c969791c9b4b4172`.
- GitHub Actions run [39872866083](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39872866083): `success`, tam olarak bu HEAD SHA üzerinde. Her yeni commit için CI yeniden kontrol edilmeli.
- Önceki run [39872216779](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39872216779) başarısızdı: K5 `test_success_creates_only_manifest_in_fresh_directory`, `OSError: Archive manifest byte integrity mismatch`. Sonraki başarılı CI bu geçmiş arızayı izleyen bir kanıttır; K5'in sahiplik dosyalarına K4 olarak dokunma. K5 regresyonunu ayrıca izlemek yararlı.
- Kabul sayaçları, bağımsız kanıtla güncellenmedikçe: 92 legacy workflow davranışsal eşdeğerliği 0/92; bağımsız runtime güvenlik 0/26; bağımsız ana görev 0/22. `production_ready=false`. Offline testler gerçek dış depo teslimi veya bağımsız geri yükleme kanıtı değildir.

## Sonraki sohbet için
1. GitHub main HEAD ve son CI sonucunu tekrar oku; başarısızlık varsa job loglarından gerçek hatayı çıkar.
2. K4 kodu ve testlerini en güncel SHA ile incele; gerçek yeni kusurları düzelt, regresyon ekle ve otomatik CI'ı izle.
3. K1–K5 ile çakışmadan kanıt/eksik listelerini güncelle; üretim kabul sayaçlarını kanıtsız yükseltme.
4. IBO Player Pro cihaz doğrulamasını en sona bırak. Son testi kullanıcı yapıp sonucunu bildirecek.

Ek tarihçe: `DEVAM_NOTU.md`, `PROJE_HAFIZASI.md`, `docs/HEPSI_YENI_SOHBET_DEVIR_2026-10-23.md`, `docs/K4_MANIFEST_CONCURRENT_MUTATION_EVIDENCE_2026-10-23.md`.
