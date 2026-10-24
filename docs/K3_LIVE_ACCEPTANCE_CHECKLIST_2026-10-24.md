# K3 — Canlı yayın kabul kontrol planı (2026-10-24)

Durum: AÇIK / henüz üretim kabulü yok.

## Doğrulanan kanıt
- `main` HEAD: `743fdccd73e60330949b867b4c9e4f876a7933be` (branch API).
- HEAD combined commit status sorgusu boş döndü; bu, başarılı CI kanıtı değildir.
- Önceki offline CI run 40028406877 / job 120670385942 başarılıydı, ancak test edilen commit `8884b1c6fa1a66c0996a1cd6ecc4254eec044869` idi.
- `madsc/epg.py` yapısal M3U/XMLTV kontrolü yapar; `device_verified=False` döndürür.
- Bu kanıtlar gerçek HLS görünt/ses veya 6 saat sürekliliği doğrulamaz.

## Canlı pilot dosyaları keşfedildi (main)
- `.github/workflows/madsc-k3-live-manifest-pilot.yml` — blob `1ea9fe8f31c891bc1bb2e95451d3c243f53c02d9`; `workflow_dispatch`, limit 12/75. Ana dalda mevcut, fakat bu turda çalıştırıldığına dair kanıt yok.
- `madsc/k3_live_manifest_pilot.py` — blob `3ecfee30acd36c149534c7a41e6cac8c3bb22bb9`; dış M3U kaynağından sınırlı HTTPS adayları alır, DNS/IP doğrulaması ve sabitlenmiş IP ile redirectsiz curl kullanır. Açıkça `audio_video_verified=False` yazar: bu sadece manifest erişim pilotudur.
- `.github/workflows/madsc-k3-turkish-tv-video.yml` — blob `18296862c040ab30bc846e2b3cf3dd73e5ea99c0`; `workflow_dispatch`, ffprobe tabanlı sınırlı video/ses denemesi.
- `madsc/k3_turkish_tv_video_pilot.py` — blob `489572833bcc44d8941017e8c08b36b66b62ecf9`; manifest, segment ve ffprobe stream türlerini inceler; workflow henüz bu oturumda çalıştırılmadı.
- `.github/workflows/madsc-online-pilot-gates.yml` — blob `c3365cdd0654e56e2e561244fb1506df1a583303`; offline gate sonrası online K2/K3 pilotlarını çalıştıran alternatif workflow.

## Bu audit dalındaki güvenli düzeltmeler
- `.github/workflows/madsc-k3-live-manifest-pilot.yml` (audit branch blob `f9aa053633f513778d86804c533c673118ef73b1`): çevrimiçi adaylara erişmeden önce `python -m madsc.offline_gate` koşulu eklendi; `needs: offline-regression` ile ağ işi gate başarısına bağlandı; eşzamanlı çalıştırma grubu eklendi.
- `.github/workflows/madsc-k3-turkish-tv-video.yml` (audit branch blob `a4b2193c03343c006bba0149131b241cf2422e00`): aynı offline gate ve bağımlılık eklendi; aynı pilotun eşzamanlı çalışması engellendi.
- Bu değişiklikler yalnız audit dalındadır; henüz `main`'e alınmadı ve CI ile doğrulanmadı. YAML/CI başarısı iddia edilmez.
- GitHub Actions araç seti bu oturumda workflow dispatch sunmuyor. Bu yüzden çevrimiçi pilotlar başlatılmış gibi raporlanmayacak.

## Açık kabul kapıları
1. **Canlı HLS:** İzinli test kaynaklarında HTTPS manifest, master/media playlist, segment, video ve audio stream doğrulaması; URL/token gizliliğini koruyan zaman damgalı rapor.
2. **Süreklilik:** Aynı yayında bağımsız en az 6 saat; kopma, yeniden bağlanma ve kesinti süreleri.
3. **Pages/XMLTV:** HTTP erişimi, XMLTV şeması, EPG zaman aralığı ve tvg-id eşleşmeleri.
4. **Kimlik/logo:** Kanal adı, logo URL'si ve doğru kanal eşleşmesi.
5. **IBO Player Pro:** Yalnızca diğer kapılardan sonra kullanıcı cihazında manuel kabul.

## Güvenlik sınırları
- Üretim M3U/XMLTV, favori, logo, yedek, arşiv ve cihaz verilerine dokunma.
- K3 taslak PR #10'u otomatik birleştirme.
- Offline CI'yi canlı yayın kabulü olarak sunma.
- K3-13 açık kalsın.

## Sonraki işlem
Audit dalı değişiklikleri PR olarak incelemeye sunulsun; Actions CI doğrulaması ve çevrimiçi pilotlar gerçek çalıştırma raporları oluşunca değerlendirilsin.


## 2026-10-24 CI hata düzeltmeleri
- Run `40032824172` / commit `f03709dfc18b24b88e806bf272d510cfc6130c99` başarısız oldu: 1.484 testte 2 hata.
- `test_contradictory_success_is_rejected` testi hatalı saat koşulu kullanıyordu: fixture saatleri (0, 3, 6) iken bozuk veri koşulu (12) idi. Koşul gerçek orta ölçüme (3) taşındı; üretim kodunun çelişkili başarılı kanıtı reddetmesi doğrulanacak.
- K3 video artifact sözleşmesi hedef workflow'unda `if-no-files-found: warn` eksikti; `.github/workflows/madsc-03-kanal-test.yml` içine eklendi.
- Yeni CI: run `40033130573` (commit `0fb444b246450615b390f572f30daafd1236f90f`) ve run `40033132772` (commit `d309bf7d24859d773a77f7cb742e5bc670818b84`) kontrol sırasında henüz sonuçlanmamıştı.
- CI sonuçları başarılı olmadan bu düzeltmeler doğrulanmış sayılmaz. Canlı HLS, video/ses, Pages/XMLTV, 6 saat süreklilik ve cihaz kabul kapıları hâlâ açık.


## Güncel doğrulama sonucu
- Run `40033130573` — commit `0fb444b246450615b390f572f30daafd1236f90f`: SUCCESS, offline-tests işi başarılı.
- Run `40033132772` — commit `d309bf7d24859d773a77f7cb742e5bc670818b84`: SUCCESS, offline-tests işi başarılı.
- Run `40033178689` — commit `1816b0e5f2448b6c6d28d9e5865be27124cbdc23`: SUCCESS, offline-tests işi başarılı. Bu, kayıtlı test dalındaki en yeni doğrulama; run bağlantısı: https://github.com/Madsc55/Madsc55-Tv/actions/runs/40033178689
- Önceki 1.484 testlik çalışmadaki iki hata düzeltildikten sonra offline gate geçti. Bu başarı yalnızca o commit'in offline test kapsamını kanıtlar.
- Online manifest/video workflow'ları bu oturumda başlatılmadı; gerçek HLS video/ses, Pages/XMLTV, 6 saat süreklilik ve IBO Player Pro doğrulanmış değildir.
- K3-13 açık kalır; audit dalı PR ile incelemede, main'e birleştirilmedi.


## Güncel K3 CI ve kabul durumu (24 Ekim)
- K3 değişiklikleri taslak PR #10 üzerindedir: https://github.com/Madsc55/Madsc55-Tv/pull/10
- Offline run 40071744359 (d6d0341e): SUCCESS; sadece offline test kanıtıdır.
- Offline run 40071899872 (4babb5c7): FAILURE; blocked probe test fixture'ı manifest gözlemi çelişkisi üretti.
- Fixture, gerçek blocked probe çıktısına uygun olarak manifest gözlem alanı kaldırılarak düzeltildi (b4079a95). Run 40072187564 kontrol sırasında devam ediyordu; başarı iddiası yok.
- K3-13 AÇIK: gerçek ağda 75 aday, altı saat aralıklı üç bağımsız kanıt, ffprobe video/ses, Pages/XMLTV, logolar ve son IBO Player Pro cihaz kabulü gerekir.
- Manifest-only raporu decoded video/audio veya tam üretim kabulü kanıtı değildir.
