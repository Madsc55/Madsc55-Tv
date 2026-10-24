# K4 dört kabul kapısı — kanıt matrisi (24 Ekim 2026)

Bu dosya mevcut kaynaklardan çıkarılmış kontrol listesidir; üretim yedeği, gerçek restore, VOD eşdeğerliği veya zamanlayıcı çalışması gerçekleştirildiğini iddia etmez.

| Kapı | Mevcut kanıt | Kabul için eksik | Durum |
|---|---|---|---|
| K4-15 Drive yedeği | PR #20: sentetik 106 baytlık `text/plain` yükleme/indirme; kaynak ve geri indirilen SHA-256 `af227eef0e2a924f817911442cc0e5c8af865a1a29b5d10199495eb4780e5dce` | Onaylı gerçek kaynak kapsamı, dosya bazlı manifest, sağlayıcı nesne/iş makbuzu, saklama politikası, yetkili erişim | PENDING |
| K4-16 bağımsız restore | `madsc/backup.py`, `madsc/k4_restore_gate.py` izole üç ağaçlı yerel doğrulama | Aynı gerçek harici yedek kimliğinden temiz bağımsız hedefe restore; kapsam/hash/inode karşılaştırması ve bozuk kopya negatif testi | PENDING |
| K4-17 VOD/arşiv | `madsc/isolated_ibo_archive_verify.py` ve testler; korunan gerçek envanter kabulü yok | Salt-okunur onaylı kaynak envanteri; izinli kopyada içerik, metadata, erişim/saklama semantiği ve eksik/fazla kayıt karşılaştırması | PENDING |
| K4-18 1/15 zamanlayıcı | `madsc/k4_schedule_plan.py` Europe/Stockholm DST ve idempotency dry-run; CI #40083594805 success | Onaylı üretim scheduler tanımı, kimlik/yetki, kilit, retry/timeout, 1 ve 15 gerçek tetik run/artifact kayıtları | PENDING |

## Kanıt toplama protokolü
1. Her kapı için önce veri sahibi onayı, izinli kapsam, saklama süresi ve hedef izolasyonunu yazılı olarak kaydet.
2. Kimlik bilgilerini veya özel Drive nesne kimliklerini açık GitHub belgelerine koyma; yalnız maskelenmiş kanıt referansları ve SHA-256 manifesti kullan.
3. Kaynak envanteri, sağlayıcıdan bağımsız makbuz ve restore raporu farklı kökenlerden gelmeli; yalnız yerel fixture üretim kabulü sağlamaz.
4. Restore işlemi yalnız boş, izole, yetkilendirilmiş hedefte; üretim playlist/EPG, VOD ve cihaz verilerinde hiçbir yazma/silme yapılmaz.
5. VOD eşdeğerliğinde dosya/hash eşleşmesine ek olarak kayıt sayısı, göreli yol, izinli metadata, saklama ve erişim semantiğini karşılaştır.
6. Zamanlayıcıda iki gün için ayrı gerçek run kanıtı, tekrar denemede tekil işlem ve hata durumunda fail-closed davranış şarttır.
7. Kanıt tamamlanana kadar `external_storage_proven=false`, `production_restore_approved=false`, `production_writes=false`, `production_ready=false`.

## Doğrulama kaynakları
- PR #20: https://github.com/Madsc55/Madsc55-Tv/pull/20
- PR #21: https://github.com/Madsc55/Madsc55-Tv/pull/21
- Son gözlenen başarılı K4 dalı CI: https://github.com/Madsc55/Madsc55-Tv/actions/runs/40083594805 (commit `8d3207ede449e0c7f384a2573a3c4080e1fd26f4`)
- Kabul şartları: `docs/K4_EXTERNAL_BACKUP_RESTORE_ACCEPTANCE_2026-10-23.md`

Bu matrisi ekleyen commit için CI ayrıca kontrol edilmelidir.

## 24 Ekim 2026 — yeni VOD doğrulayıcı ve CI kabulü
- `madsc/k4_vod_equivalence.py`: iki salt-okunur manifestte göreli yol, byte, SHA-256, saklama ve erişim politikasını karşılaştırır. Bilinmeyen alan, yol kaçışı, Unicode taşınabilir ad çakışması ve sahte üretim kabulü fail-closed.
- `tests/test_k4_vod_equivalence.py`: eşleşme, eksik/fazla dosya, bozuk hash, erişim/saklama farkı ve geçersiz veri testleri.
- Commit `79189f99d13625a69a68b225fd18d53aba324065` için GitHub Actions `40091242333` **success**: https://github.com/Madsc55/Madsc55-Tv/actions/runs/40091242333
- Google Drive `MADSC55-TV/K4-Backups` altında yalnız `K4-Fixture-Only` klasörü gözlendi; bu klasörde 106 baytlık sentetik .txt ve Google Docs fixture var. Gerçek kaynak envanteri veya sağlayıcı yedek makbuzu gözlenmedi.
- K4-15/16/17/18 gerçek üretim kabulü hâlâ açık. Test kodu ve fixture sonuçları gerçek VOD veya bağımsız harici restore kanıtı değildir.
