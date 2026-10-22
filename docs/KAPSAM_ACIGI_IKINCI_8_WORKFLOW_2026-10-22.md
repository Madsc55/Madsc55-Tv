# Kapsam açığı: ikinci sekiz workflow kaynak incelemesi

Sabit kaynak `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Bu sekiz YAML doğrudan okundu; Actions çalıştırılmadı.

| Dosya | Doğrulanan işlev |
|---|---|
| `madsc-05-genel-bakim.yml` | K1→K2→K3→K4 reusable workflow zincirini `needs` ile kurar, ardından K5 genel denetim, kanıt aktarımı, 92 satır karar matrisi ve fail-gate kontrollerini yapar. Günlük 01:30 UTC ve manuel; kaynak dosyada ayrıca belirli dal push tetikleyicisi. `always()` koşulları nedeniyle başarısız önceki kategori sonrakini mutlaka durdurmaz; nihai kabul ayrıca kontrol edilmelidir. |
| `madsc-ibo-6115-second.yml` | Main üzerinde write yetkisi, hard reset, `apply_ibo_6115_second.py`, `CALISANLAR.m3u` ve IBO rapor/arşiv commit/push; yabancı liste değişmemeli kontrolü. |
| `madsc-ibo-ilk-239.yml` | Main push ile ilk 239 IBO kullanıcı kararını `apply_ibo_first_239_decisions.py` uygular, ana liste ve karar/rapor dosyalarını commit/push eder. |
| `madsc-ibo-kararlar-grup1.yml` | Grup 1 IBO kararlarını `apply_ibo_decisions_group1.py` uygular; korunan liste ve arşiv/karar çıktıları için write+push. |
| `madsc-ibo-second-voice.yml` | İkinci sesli inceleme kararlarını `apply_ibo_second_voice.py` ile uygular; 6115 temelinden yabancı yedek ayırma, ana liste ve arşiv commit/push. |
| `madsc-otomatik-devam.yml` | Yalnız manuel echo mesajları; yeni tarama turu başlatmaz. |
| `madsc-rule24-test.yml` | Manuel veya ilgili kod push; `test_workflow_failure_gate` unittest; gerçek arka arkaya hata durumu ayrıca sınanmalı. |
| `madsc-sistem-saglik-denetimi.yml` | Ayın 1'i ve 15'i 05:17 UTC veya manuel; Ruby YAML parse, unittest, sistem denetim betiği, GitHub Actions son 100 koşu API sorgusu, JSON artifact ve kritik hata kapısı. |

## Öncelikli riskler

- Dört IBO akışı `contents: write`, `git reset --hard`, korunan `CALISANLAR.m3u` değişikliği ve `git push` içeriyor. Betiklerin hangi kanal kayıtlarını değiştirdiği ve `tools/protected_write_gate.py` kontrolünün gerçek kapsamı incelenmeden taşınmamalı.
- K5 zincirinde `always()` başarısız bir kategori sonrasında bile aşağı akışın çalışmasına izin verebilir. Başarı kabulü yalnız yeşil job adına bağlanmamalı.
- Son 100 Actions koşusunun incelenmesi bütün tarihsel koşuların incelendiği anlamına gelmez.

Bu sekiz dosya, önceki 29 belgesiz dosya kümesinden seçildi. Önceki belgelerle ad bazında kapsam **en az 86/99**; kalan 13 ad ayrıca incelenecek. Davranışsal kabul 0/92, 26 kural üretim kabulü 0/26.
