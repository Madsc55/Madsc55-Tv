# MADSC55-TV — K5 DEVİR NOTU / 24 EKİM 2026

## Kaynak ve çalışma sınırı

- Depo: `Madsc55/Madsc55-Tv`; çalışma dalı: `k5/fail-closed-evidence-20261023`; taslak PR: #6.
- Eski kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`.
- K5 yalnızca güvenli, izole, çevrimdışı ve kanıt temelli doğrulama yapar. `main`, korunan playlist, EPG, logo, VOD, yedek ve canlı yayın üretim verileri değiştirilmez.

## Son doğrulanan CI

- Kod/test commit'i: `0faee1c8d37a28280447a0085adad60c19c13c49`.
- Frozen Source Integrity: **SUCCESS**, https://github.com/Madsc55/Madsc55-Tv/actions/runs/40073192129
- Offline Unit Tests: **SUCCESS**, https://github.com/Madsc55/Madsc55-Tv/actions/runs/40073192074
- Bu başarı yalnızca belirtilen commit içindir. Sonraki commit'lerin CI sonucu ayrıca doğrulanmalıdır.

## Yapılanlar

1. 99 eski YAML envanteri: 7 hariç, **92/92** ilk kaynak incelemesi. Ayrıntılı script bağımlılığı ve davranışsal kabul ile karıştırma.
2. K5 karşılaştırıcısında sıkı kanıt şeması, SHA256, ayrı run ID/commit, artifact/yan etki hash, timeout, retry, path ve kontrol karakteri kontrolleri.
3. Eşleşen JSON bile **accepted=false**; bağımsız yürütme dışarıdan kanıtlanmadıkça otomatik onay yok.
4. Workflow #92 (`yeniler-guvenli-arama.yml`) tüm YAML ve iki Python giriş dosyası incelendi. 66 batch × 30 = 1.980 aday indeks sınırı; dış URL/SSRF ve ağ determinizmi riskleri kaydedildi.
5. Tutarsız `timed_out=true` + `exit_code=0` kanıtı reddedildi ve regresyon testi eklendi.
6. Tamamlanma koşulları: `docs/K5_COMPLETION_BLOCKERS_AND_ACCEPTANCE_2026-10-24.md`; workflow #92 ayrıntısı: `docs/K5_LEGACY_WORKFLOW_92_DEPENDENCY_REVIEW_2026-10-24.md`.

## Kapanmamış işler — kanıtsız kapatma yok

- **0/92** bağımsız davranışsal kabul; 92 gerçek eski/yeni izole fixture yürütme çifti, doğrulanmış runner kimliği, log ve artifact hash'leri eksik.
- Eski script bağımlılıkları ile yeni K1–K5 davranışları için tam çağrı grafiği ve eşleştirme eksik.
- Harici URL'ler için SSRF/redirect, lisans/izin, ağ sınırları ve canlı medya kontrolleri üretim kabulüne uygun şekilde doğrulanmadı.
- Korunan yazma, backup/restore ve K1/K3/K4/K5 uçtan uca kabul için bağımsız kanıtlar eksik.
- PR #6 birleştirilmedi; `main` ve üretim değiştirilmedi.

## Bir sonraki çalışmada

1. Önce **en son branch SHA** ve iki CI durumunu yeniden kontrol et.
2. Fail-closed K5 regresyonlarını iyileştir; güvenli, salt okunur fixture koşucusu ile **gerçek** bağımsız yürütme kanıtı oluştur; sahte run ID veya hash üretme.
3. Her kabul için bağımsız kanıtı doğrula; sayıları yalnızca doğrulama sonrası güncelle.
4. `main` merge veya üretim taraması/yazımı için açık onay almadan ilerleme.

**Doğrulanmış kabul: 0/92. K5 tamamlandı veya üretime hazır denemez.**

## 24 Ekim — Ek fail-closed kanıt sertleştirmesi

- `madsc/k5_behavioral_compare.py`: run ID'leri artık yalnız ASCII harf/rakamla başlayan, 1–200 karakter uzunluğunda ve devamında `[A-Za-z0-9._:-]` içeren kanonik biçimde kabul edilir. Boşluk, URL, slash, kontrol karakteri ve Unicode belirsizliği reddedilir. Bu kontrol **run ID'nin gerçekten GitHub'dan geldiğini kanıtlamaz**.
- `tests/test_k5_behavioral_compare.py`: kötü biçimli run ID regresyonları eklendi.
- Commitler: `14175a0cc0ed4602af5e86d70a6b0e61170ba8b5`, `baf48870249ce3f04b94fe80c587c1fd7cc16658`.
- Son önceki başarılı CI: `f20c9d4` için run `40073505914` ve `40073505783`. Yeni commit'lerin CI'sı henüz doğrulanmadı.
- Gerçek bağımsız davranışsal kabul **0/92**; üretim kabulü yok. Korunan veriler değiştirilmedi.
