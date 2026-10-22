# Üçüncü 12 eski workflow: yürütme zinciri ve kritik yan etkiler

Sabit kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. GitHub'dan bu 12 YAML'ın tam kaynak metni okundu. Aşağıdaki tablo yalnızca YAML'da doğrudan gözlenen davranışlara dayanır; Python dolaylı etkilerinin tamamı çözümlenmiş değildir.

| Workflow | K aşaması (aday) | Tetikleyici | YAML komut zinciri | Kanıt ve risk |
|---|---|---|---|---|
| madsc-ana-liste-saglik | K1/K3 | dispatch + ayın 1,15'i 06:40 | önce sha256 → unittest → ana_liste_saglik --batch-size 50 --timeout 15 → always sha256/git diff → artifact/summary | Ana liste 50'lik gerçek yayın probe; üç dosya hash korunumu |
| madsc-arsiv-yedek-aktarim | K4 | dispatch | sadece echo: mutasyon onay gerektirir | İşlevsel aktarım YOK; güvenli dry-run |
| madsc-aylik-merkezi-denetim | K1–K5 | dispatch + push + ayın 1,15'i 07:00 | geniş merkezi kontrol: protected gate → workflow inventory → logo/EPG → izole restore → yedek kanıt → kaynak uzlaştırma → testler → Actions API → konsolidasyon | 15 dakika sınırı; geniş YAML çok sayıda step içeriyor; çağrılan scriptler ayrıca incelenmeli |
| madsc-birlesik-kesif | K1/K2/K3/K5 | dispatch + her gün 06,18 UTC | failure gate → git reset → discovery_archive before → madsc_akilli_kesif → discovery_archive after → four_stage_discovery_report → artifact → yarış kontrollü 10 denemeli git push | EPG/logo join if:false; gerçek medya testi ve write/push var |
| madsc-cuma-ana-liste-denetimi | K3/K5 | dispatch | haftalik_ana_liste_denetimi → always cuma_denetim_uyari_ozeti → artifact | Adında cuma olsa da YAML'da cuma cron'u yok |
| madsc-documentation-check | K1/K5 | dispatch | AGENTS/OZELLIK/DEVAM varlık grep; CALISANLAR #EXTM3U başlık kontrolü | Belge smoke test; davranış kanıtı değil |
| madsc-genis-kaynak-kontrol | K1/K2/K5 | dispatch | genis_kaynak_taramasi weekly → monthly → artifact → 5 denemeli push → gh api POST madsc-uc-asama dispatch | ÖNEMLİ: ikinci workflow'u otomatik tetikliyor; onaysız etkinleştirilmemeli |
| madsc-ibo-3-5281 | K4/K1 | dispatch + branch push | sadece echo: mutasyon devre dışı | İşlevsel kanal ayırma YOK |
| madsc-ibo-354-classify | K1/K4 | push | archive_backups_354_classified → git add CALISANLAR ve arşivler → protected_write_gate → commit → push | Script CALISANLAR yazar; koruma kapısıyla çelişme olasılığı |
| madsc-ibo-364-355-364 | K1/K4 | push | archive_backups_355_364 → YABANCI diff kontrol → git add CALISANLAR → gate → push | Korunan ana liste staged; izin olmadan çalıştırılmaz |
| madsc-ibo-398-16-49 | K1/K4 | push | archive_backups_16_49 → YABANCI diff kontrol → git add CALISANLAR → gate → push | Korunan ana liste staged; izin olmadan çalıştırılmaz |
| madsc-ibo-530-archive | K1/K4 | push | archive_backups_399_onward → YABANCI diff kontrol → git add CALISANLAR → gate → push | Korunan ana liste staged; izin olmadan çalıştırılmaz |

## Güvenlik ve semantik ayrımları

- `madsc-genis-kaynak-kontrol` **başarılıysa** `gh api --method POST .../madsc-uc-asama.yml/dispatches` ile başka workflow başlatır. Bu tetikleme K1 onay kapısı olmadan taşınmamalıdır.
- `madsc-ibo-354-classify`, `madsc-ibo-364-355-364`, `madsc-ibo-398-16-49`, `madsc-ibo-530-archive` `CALISANLAR.m3u` dosyasını `git add` kapsamına alır; `contents:write` ve `git push` içerir. Protected write gate'in reddetmesi olasıdır; gerçek sonucuna dair çalıştırma kanıtı yoktur.
- `madsc-arsiv-yedek-aktarim` ve `madsc-ibo-3-5281` YAML'da yalnızca uyarı mesajı verir; adları gerçek aktarım yapıldığına delil değildir.
- `madsc-cuma-ana-liste-denetimi` adında cuma olsa da sadece manuel `workflow_dispatch` içerir.
- `madsc-aylik-merkezi-denetim` hem ayın 1/15'inde hem ilgili dosyalara push ile tetiklenir; geniş bir test/rapor zinciri vardır, ancak YAML incelenmesi gerçek çalıştırma eşdeğerliği sağlamaz.

İlk iki 12'lik çalışma zinciri belgesiyle toplam **36 farklı YAML** kaynak düzeyinde ayrıştırılmıştır. Davranışsal kabul **0/92**; güvenlik uygulama kabulü **0/26**; görev kabulü **0/22**. GitHub Actions tetiklenmedi, canlı yayın yoklanmadı, korunan veri değiştirilmedi.
