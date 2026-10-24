# MADSC55-TV — ANA MERKEZ SOHBET DEVİR NOTU (24 Ekim 2026)

Bu kayıt yeni sohbetten devam etmek için hazırlanmıştır. Kaynak: ortak `main:DEVAM_NOTU.md`, K1–K5 devir bölümleri ve 24 Ekim GitHub denetimi. Ayrı sohbetlerin tamamına doğrudan erişim iddiası yoktur. Bu belge, üretim kabulü değildir.

## Son doğrulanan durum
- Depo: https://github.com/Madsc55/Madsc55-Tv
- Devir başında `main`: `76d8f0e2a0c2ad3ad498de006809ae92c144bee6` (yeni sohbette yeniden kontrol et).
- Ortak `DEVAM_NOTU.md`: K1, K2, K3, K4, K5'in beş devir bölümü okunmuştur. Bu notun hazırlanması mevcut ana dosyayı değiştirmez.
- Açık PR #22: https://github.com/Madsc55/Madsc55-Tv/pull/22; dal `ana-merkez/ci-per-ref-concurrency-20261024`; son SHA `2c6ee71f57f4c7dd8c015b758e00405ca2ecbcec`. `.github/workflows/madsc-unit-tests.yml` concurrency grubu workflow ve PR numarası/ref ile ayrıldı; `tests/test_offline_ci_trigger_contract.py` regresyon testi eklendi.
- PR #22 exact HEAD için Actions https://github.com/Madsc55/Madsc55-Tv/actions/runs/40074534071 ve https://github.com/Madsc55/Madsc55-Tv/actions/runs/40074531578 **success**. PR birleştirilmedi.
- PR #17 https://github.com/Madsc55/Madsc55-Tv/pull/17 aynı workflow concurrency satırını başka formülle değiştiriyor ve kendi regresyon testini ekliyor. **#17 ile #22 çakışmasını incele; iki değişikliği körlemesine birleştirme.**
- Son görülen açık PR'lar: #1, #2, #3, #6, #7, #10, #12, #14, #16, #17, #18, #20, #21, #22. Sayı ve HEAD'ler yeniden doğrulanmalı. Branch protection önceki denetimde kapalıydı.
- K2 PR #18 son görülen SHA `dca2a9b075d862b3c4dcd4fe67da163e25dcb4f0`; K4 PR #21 `72f1f9d109bc85d54662817ee9362bd0e1dc04b4`. Eski CI başarıları bu SHA'lar için otomatik kanıt sayılmaz.

## K1–K5 açık kabul kapıları
- K1: gerçek runtime güvenlik **0/26**; korunan yazma, TOCTOU, subprocess/callsite doğrulaması.
- K2: 1.039 EXTINF, 376 benzersiz URL, 663 tekrar URL satırı, 331 boş/eksik tvg-id, 255 HTTP URL. Bunlar salt okunur envanter sayılarıdır; canlı/hak/EPG kabulü yok.
- K3: gerçek HTTPS/HLS, 75 aday için üç snapshot, video+audio, XMLTV/tvg-id/logo, IBO Player Pro cihaz kabulü açık. Kullanıcının test playlist'inde yayın/logo çalıştığı, EPG'nin sorunlu olduğu önceki kayıtlarda bildirildi.
- K4: Google Drive'da yalnız **sentetik** round-trip SHA-256 kanıtı var; gerçek dış yedek, bağımsız sandbox restore, VOD/arşiv, 1/15 gerçek zamanlayıcı ve yetkiler açık.
- K5: eski workflow **92/92 ilk YAML/kaynak incelemesi**, ancak bağımsız gerçek davranışsal parity **0/92**.
- Genel gerçek kabul **0/22**; `production_ready=false`. Offline CI, gerçek üretim kabulü değildir.

## Yeni sohbet çalışma sırası
1. GitHub güncel `main`, `DEVAM_NOTU.md`, açık PR HEAD, CI run/job sonuçlarını yeniden oku.
2. #17/#22 concurrency çakışmasını ve gerekli regression testlerini uzlaştır; güncel exact-HEAD CI başarısı ve inceleme olmadan merge etme.
3. K1 güvenlik ve K2/K3 EPG/kimlik problemleri için salt-okunur, izole testler ve ayrı dallarda düzeltmeler yap.
4. K4 ve K5 gerçek kabul kanıtlarını, dış yetki ve kullanıcı onayı olmadan tamamlanmış sayma.
5. Her çalışmada Türkçe kısa rapor, gerçek commit/PR/CI bağlantıları ve kalan işler listesi üret; ortak devir notunda başka K bölümlerini koru.

## Değiştirilmemesi gerekenler
Üretim playlist/M3U8, EPG/XMLTV, favoriler, logolar, yedekler, arşiv/VOD, cihaz verileri ve eski repo. Yetkisiz canlı probe, workflow dispatch/rerun, gerçek restore, secret/erişim izni değişikliği ve onaysız PR merge yapılmaz.

Bu dosya yeni sohbet için bağımsız, sürümlenmiş devirdir; `main` üzerine henüz taşınmamıştır.


## 24 Ekim 2026 — Ana merkez güncel CI denetimi (10:22 Europe/Stockholm)

- Son gözlenen `main` SHA: `efa6399338296110058435297e0132f379442ea8`; branch protection kapalı. Son gözlenen main başarılı offline CI `40074564285`, ancak `345392a780a8...` SHA'sına ait; güncel main SHA'sını kanıtlamaz.
- Açık PR sayısı: **15** (#1, #2, #3, #6, #7, #10, #12, #14, #16, #17, #18, #20, #21, #22, #23).
- K5 PR #6 güncel SHA `17ecf189a90fe19995e50f19a683d82a535d6e61`; offline `40074650857` ve frozen-source `40074650847` başarıyla tamamlandı. Bu 0/92 gerçek parity kabulünü değiştirmez.
- K3 PR #10 `3501cafc40c3...` SHA'sı için offline `40074591188` başarılı; canlı yayın/cihaz kabulü yok.
- K2 PR #18 `dca2a9b075d8...` için `40074621666` ve `40074617690` **cancelled**; güncel SHA'da success yok. K4 PR #21 güncel `72f1f9d109bc...`; son SHA için CI ayrıca doğrulanmalı.
- Ana merkez PR #22'de ek somut düzeltme: `9291e5e393df0dc5ccb275cfb8ef22a6dc25c74e` commit'iyle `.github/workflows/madsc-unit-tests.yml` push ve PR path filtrelerine `src/**`, `scripts/**`, `config/**`, `.github/workflows/**` eklendi. Önceden `src/madsc_guard.py`, `scripts/birlestir_eski_sistem_notlari.py` veya yalnız workflow/config değişiklikleri offline CI tetiklemeyebilirdi. `60e1bbca587bb1cbcc7beed57be536dbc1ab13d0` commit'iyle `tests/test_offline_ci_trigger_contract.py` regresyonları genişletildi.
- PR #22 güncel SHA `60e1bbca...` için `40077803907` ve `40077806742` son kontrolde **pending**; eski `2c6ee71...` SHA'sındaki `40074531578` / `40074534071` success yeni SHA'ya aktarılmaz. PR #17 ile aynı workflow satırındaki çakışma hâlâ incelenmeli.
- Hiçbir PR birleştirilmedi, manuel workflow dispatch/rerun yapılmadı, canlı probe/restore/üretim veri yazımı olmadı. K1 0/26, K5 0/92, genel 0/22 kabul açık.
