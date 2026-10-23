# K4 — Yeni sohbet devir notu (23 Ekim 2026)

## Amaç
Madsc55/Madsc55-Tv deposunda main dalı üzerinde K1–K5 beşli sisteminin K4 (yedek, arşiv, izole geri yükleme) tarafını güvenli biçimde tamamlamak; ortak CI hatalarını izlemek. Üretim verilerine yazma, gerçek restore, workflow dispatch, PR #71 merge veya gerçek playlist/EPG/VOD değişikliği yapılmaz.

## Son doğrulanan durum
- Bu not yazılmadan önce main HEAD: `9360c46bbd250a35931b782d0d00ca976d20db6e`. Bu SHA not commit'i ve eşzamanlı diğer commit'ler nedeniyle değişebilir.
- En son görülen başarılı GitHub Actions: 40002212175, commit `9b950286d905ca2393a7ffa30ca01c0852f94ef0`; https://github.com/Madsc55/Madsc55-Tv/actions/runs/40002212175
- Daha yeni HEAD için CI başarısı varsayılmamalı; önce main ve son Actions sorgulanmalı.
- K4 restore gate `madsc/k4_restore_gate.py`: kaynak, yedek ve restored manifestlerini başlangıç kaynak manifestine karşılaştırıyor; dosya/klasör Unicode NFKC/casefold çakışmalarını reddediyor; symlink, alias, envanter ve bağımsız sandbox kontrolleri var.
- Önceki K4 commitleri: `db8a007e` (üç manifest başlangıç kaydına sabitlenir), `b388acfa` (portable dosya/klasör çakışması). İkisinin de CI çalışması başarılıydı (39985616433 ve 39987221687).
- `madsc/restore_drill.py` yalnız yerel sandbox fixture çalıştırır; gerçek harici yedek kanıtı değildir.
- İlgili testler: `tests/test_k4_restore_gate.py`, `tests/test_backup_manifest_hardening.py`, `tests/test_k4_copy_audit_ancestor_symlinks.py`.

## Gerçek kabul engelleri
- K4-15: bağımsız harici yedek hedefi, gerçek teslim makbuzu, tam manifest ve yetkili kanıt yok.
- K4-16: aynı harici yedekten bağımsız temiz hedefe gerçek restore ve bağımsız inceleme kanıtı yok.
- K4-17: gerçek VOD/arşiv kapsam envanteri ve yetkili salt-okunur eşdeğerlik kanıtı yok.
- K4-18: ayın 1'i ve 15'i gerçek scheduler run/artifact/exit-code kanıtı yok.
- `production_ready=false`, `external_storage_proven=false`, `production_restore_approved=false` korunmalı; CI fixture'ı bu değerleri true yapamaz.
- Kanıt şablonu: `docs/K4_REAL_BACKUP_EVIDENCE_TEMPLATE.md`; kabul koşulları: `docs/K4_EXTERNAL_BACKUP_RESTORE_ACCEPTANCE_2026-10-23.md`.

## Yeni sohbette yapılacaklar
1. Canlı main HEAD, son Actions run'ları ve offline-tests adımını kontrol et. Başarısızsa logları incele, gerçek hataları testle düzelt.
2. K4 backup/restore/gate kodunda doğrulanabilir eksik veya regresyon bulursan hedefli düzeltme + test ekle, SHA kontrollü commit yap. Eşzamanlı K1–K5 değişikliklerini ezme.
3. K4-15–18 için harici sağlayıcı ve yetkili hedef belirlenmediyse gerçek aktarım/restore/cron etkinleştirme; yalnız kod/test/dokümantasyon hazırlığı yap.
4. Üretim kabulünü kanıtsız ilan etme. Her turda yapılan gerçek commit, CI SHA ve kalan engelleri açık yaz.
