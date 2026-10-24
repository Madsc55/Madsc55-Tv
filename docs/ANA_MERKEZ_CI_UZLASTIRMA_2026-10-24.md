# ANA MERKEZ — K1–K5 CI UZLAŞTIRMA KAYDI (24 Ekim 2026)

- Taban main SHA: efa6399338296110058435297e0132f379442ea8.
- PR #17 ve #22 aynı workflow ve regresyon testi dosyalarında değişiklik içeriyor. #17 event/ref, #22 workflow/PR-numarası veya ref concurrency anahtarı kullanıyor. Çakışma doğrudan merge ile çözülmedi.
- Bu dalda workflow concurrency grubu PR/ref kapsamlı yapıldı, cancel-in-progress false korundu. Push ve PR path filtrelerine src/**, scripts/**, config/**, .github/workflows/** eklendi.
- Statik regresyon testi bu kapsamı ve read-only offline sözleşmesini denetleyecek şekilde genişletildi.
- Kod commitleri: 6238fbcae31d6a070a88d787f931635e5999a329, fc7341261baf9444c4fc82a3755da1496f103063.
- PR #24 draft: https://github.com/Madsc55/Madsc55-Tv/pull/24.
- Exact HEAD CI henüz bu kayıt sırasında doğrulanmadı; merge yok. K1 0/26, K5 0/92, genel 0/22 kabul değişmedi.
- Diğer K dalları, üretim playlist/EPG, favori/logo, yedek/restore ve cihaz verileri değiştirilmedi. Manuel dispatch/rerun yapılmadı.
- Sonraki iş: PR #24 exact HEAD CI ve inceleme, ardından K1–K5 ayrı regresyon ve eksik kabul kapıları. Başarılı CI tek başına üretim kabulü değildir.
