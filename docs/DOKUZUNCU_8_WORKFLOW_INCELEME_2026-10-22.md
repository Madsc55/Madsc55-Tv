# K1-K5: Sekiz eski workflow kaynak incelemesi

Kaynak: `Madsc55/madsc-tv` commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Sekiz YAML dosyasının tam metni incelendi. Bu belge çalışma zamanı davranışsal kabulü değildir.

| Workflow | YAML'da gözlenen işlev |
|---|---|
| `test-29-write-path-audit.yml` | Manuel veya YAML push; PyYAML ve regex ile yazma izinleri, git push/commit, API, korunan hedefler ve onay kelimelerini tarar; JSON artifact. Onay kelimesi yetki kanıtı değildir. |
| `test-30-write-risk-report.yml` | Manuel veya YAML push; statik yazma riski kaydı ve HIGH/REVIEW öncelik raporu üretir; JSON artifact. |
| `madsc-11599-yedek-geri-yukle.yml` | Yalnızca manuel; `scripts/diagnose_11599_backups.py` ile salt okunur fark teşhisi. Geri yükleme komutu yok. |
| `madsc-ana-liste-saglik.yml` | Manuel veya ayın 1/15'i 06:40 UTC; korunan dosya SHA256, birim testi, ffmpeg, 50 kanallık/15 sn sağlık taraması, değişmezlik denetimi, rapor artifact. |
| `madsc-arsiv-yedek-aktarim.yml` | Yalnızca manuel; checkout sonrası sadece güvenli dry-run bildirimi. Gerçek aktarım yok. |
| `madsc-aylik-merkezi-denetim.yml` | Manuel, ayın 1/15'i 07:00 UTC veya seçili main push; dosya ve kural envanteri, merkezi denetimler, testler ve Actions API durum kanıtları. Ayrıntılı çağrılan betik yan etkileri ayrıca incelenmeli. |
| `madsc-birlesik-kesif.yml` | Manuel veya 06:00/18:00 UTC; yazma izinli keşif, arşivleme, medya araçları, artifact ve `madsc_kesif/` raporlarını main'e push. EPG/logo join adımı `if: false` nedeniyle çalışmaz. |
| `madsc-cuma-ana-liste-denetimi.yml` | Yalnızca manuel; ffmpeg, kanal/EPG denetimi, uyarı özeti ve artifact. Adına rağmen haftalık cron yok. |

## Kritik sonuç

`madsc-birlesik-kesif` gerçek repo yazma potansiyeli taşır; izinli K1 geçidi olmadan taşınmamalıdır. Yedek fark teşhisi geri yükleme kanıtı değildir. Echo-only aktarım işlevsel yedek aktarımı değildir. Cuma denetimi otomatik çalışmaz.

Ayrıntılı statik YAML çözümlemesi: **80/99**; kalan **19**. Davranışsal kabul **0/92**; 26 güvenlik kuralı üretim kabulü **0/26**. Üretim dosyaları değiştirilmedi, Actions başlatılmadı.
