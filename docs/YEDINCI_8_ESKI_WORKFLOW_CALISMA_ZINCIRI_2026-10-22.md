# Yedinci kaynak çözümlemesi: sekiz eski workflow (64/99)

Kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Aşağıdaki sekiz YAML'ın tam kaynak metni okundu. İnceleme statiktir; gerçek çalışma zamanı eşdeğerliği kanıtlanmamıştır.

| Workflow | K aşaması | Tetikleme | Yürütme zinciri ve kritik test sözleşmesi |
|---|---|---|---|
| `test-13-kaynak-degisiklik.yml` | K1/K2 | Manuel + betik/YAML push | Python 3.11; geçici iki M3U ile added/changed/removed üç fark; JSON rollback notu otomatik geri almanın yapılmadığını belirtmeli; asıl örnekler değişmemeli |
| `test-14-istikrar.yml` | K3 | Manuel + betik/YAML push | Python 3.11; sabit tarihli 7 ve 30 gün penceresi; 7 gün 2 test/1 başarı=%50; 30 gün 3 test/2 başarı=%66,67; son başarı zamanı; veri yoksa null |
| `test-15-logo-epg.yml` | K1/K3 | Manuel + betik/YAML push | Python 3.11; yinelenen tvg-id, eksik logo, eksik tvg-id, şüpheli logo URL uyarıları; ayrıca mevcut korunan M3U'yu salt okunur audit |
| `test-16-workflow-safety.yml` | K1/K5 | Manuel + betik/YAML push | Python 3.11; token, API key, Basic URL kullanıcı/parola ve bearer maskelenmesi; sınırlı 3 deneme başarılı, 2 deneme başarısız TimeoutError; 5 dk job/2 dk step |
| `test-17-candidate-summary.yml` | K2 | Manuel + betik/YAML push | Python 3.11; 7 adayın new(2), verified(1), quarantine(1), broken(1), identity_pending(1), unknown(1) sınıflandırılması; CSV/JSON yükleme ve boş girdi |
| `test-18-change-simulation.yml` | K1/K4 | Manuel + betik/YAML push | Python 3.11; dry-run M3U eklemesi, 1→2 kanal, applied=false, rollback SHA256, eşit içerikte changed=false; korunan iki M3U'da git diff sıfır |
| `test-19-integration.yml` | K1/K2/K3/K5 | Manuel + workflow/tools push | Python; beş modülün (logo, aday durumu, maskeleme/tekrar, kararlılık, dry-run) örnek veride birlikte testi; CALISANLAR/YENILER önce/sonra SHA256 eşitliği |
| `test-20-full-integration.yml` | K1–K5 | Manuel + YAML push | Python 3.11; kök/tools Python AST parse; korunan iki M3U mevcut; hem tests/ hem kökte unittest discover; 11 eski test workflow dosyası mevcut mu kontrolü; 10 dk |

## Davranış farkları

- `test-20-full-integration` kendisi açıkça 1–18 arasının **uçtan uca davranış kanıtı olmadığını** belirtir; yalnızca sözdizimi, dosya envanteri ve regresyonları çalıştırır.
- `test-19-integration` fixture entegrasyonudur; canlı yayın, üretim EPG veya gerçek harici yedek kabulü değildir.
- `test-14-istikrar` sabit geçmişli birim testidir; 7/30 gün gerçek gözlem toplandığı anlamına gelmez.
- `test-16-workflow-safety` hassas URL maskeleme ve bounded retry semantiği K1/K5 regresyonunda korunmalıdır.

**Ayrıntılı statik kaynak çözümlemesi: 64/99 (%64,6), kalan 35.** 92 davranışsal kabul hâlâ **0/92**. Üretim dosyalarına dokunulmadı; Actions çalıştırılmadı.
