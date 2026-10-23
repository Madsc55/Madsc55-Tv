# K5 — On ek sabit workflow'un kaynak sözleşmesi ve üretim riski

Tarih: 2026-10-23. Eski kaynak: `Madsc55/madsc-tv` commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. On YAML dosyası GitHub'dan doğrudan okunarak blob SHA'ları doğrulandı. Aşama eşleştirmesi statik **aday** eşleştirmedir, davranışsal kabul değildir.

| Workflow ve kaynak SHA | K1–K5 aday | Eski YAML sözleşmesi | Eksik karşılaştırma kanıtı |
|---|---|---|---|
| `.github/workflows/ibo-yedek-kalite.yml` / `da48c5195c35094a2a519feafd6b51f20f526edc` | K3/K4 | 25 dk; ffprobe ile yedek akış kalitesi; CSV artifact if:always | Gerçek yedek akış örneği ve CSV eşdeğerliği |
| `.github/workflows/iptv-test.yml` / `5cd014cb94e68be22f5f68b07618920c82fee740` | K1/K3 | Çarşamba 06:30 cron; 60 dk; iptv_test.py aday M3U; CALISANLAR.m3u ve iki rapor artifact | Çalışma ağacında korunan playlist etkisi ve test eşdeğerliği |
| `.github/workflows/kanal-kararlilik.yml` / `c968204d3d9d54cf218d92954189c9e6945a509f` | K3/K5 | 30 dk; cache restore/save geçmiş; ffprobe; 3 artifact | Cache sürekliliği ve geçmişe bağlı kararlılık eşdeğerliği |
| `.github/workflows/kaynak-puanlama-kontrol.yml` / `0ffc33a27ff7d6bb459fbfa608db1095218379f0` | K2 | 5 dk; py_compile ve unittest kaynak puanlama | Eski/yeni aynı fixture skorları |
| `.github/workflows/madsc-11599-yedek-geri-yukle.yml` / `fb04cdcc5abede182df764804e8a5055956dcece` | K4 | 10 dk; yalnız manuel; 11599 yedek farkı salt-okunur teşhis | 11599 envanter/hash karşılaştırması |
| `.github/workflows/madsc-ana-liste-saglik.yml` / `6ba3cc60b74f26d3e7dcfecdf84d0cd2ce85baf7` | K1/K3 | Ayın 1 ve 15'i 06:40; 35 dk; 50 kanal batch, 15 sn timeout, üç korunan dosya SHA değişmezliği | Gerçek ana liste örneklemi ve SHA kanıtı |
| `.github/workflows/madsc-arsiv-yedek-aktarim.yml` / `d2062b168db134177cb1683d86eaafa2c2937d54` | K1/K4 | 15 dk; yalnız manuel; yalnız güvenli dry-run uyarısı; transfer komutu yok | Eski no-op davranışının yeni güvenlik kapısında korunması |
| `.github/workflows/madsc-aylik-merkezi-denetim.yml` / `8cca9b93855c1e2184863b8e59b07817e546366f` | K1/K2/K3/K4/K5 | Ayın 1 ve 15'i 07:00; 15 dk; çoklu script/test/Actions API, artifact ve hata raporları | Tüm alt komut/rapor/Actions geçmişi için aynı-girdi kanıtı |
| `.github/workflows/madsc-birlesik-kesif.yml` / `da472ae0e45aa0d3c03a7dc8f9833bf43f733902` | K1/K2/K3/K5 | 06:00 ve 18:00 cron; contents/actions write; kaynak tarama, arşiv, 10 push denemesi, korunan yazma kapısı; EPG join disabled | **Yüksek risk:** gerçek main push ve yan etkiler; yalnız izole inceleme |
| `.github/workflows/madsc-cuma-ana-liste-denetimi.yml` / `b14aca32502179ae27e2399b0278502c512c2984` | K3/K5 | 55 dk; manuel; kanal/EPG denetimi, uyarı özeti, JSON artifact if:always | Gerçek kanal/EPG raporu ve hata uyarısı eşdeğerliği |

## Yüksek riskli geçiş sınırı

`madsc-birlesik-kesif.yml` eski workflow'unda `contents: write`, `actions: write`, `git reset --hard`, korunan yazma kapısı ve **10 denemeye kadar main'e push** vardır. `iptv-test.yml` `CALISANLAR.m3u` dosyasını artifact içine dahil eder; salt-okunur izinler çalışma ağacındaki dosya değişmezliğini kanıtlamaz. Bu dosyalar **çalıştırılmadı**, yayın/üretim dosyaları değiştirilmedi. Eski kaynak YAML'ın çağırdığı Python script'lerinin tüm yan etkileri ayrıca doğrulanmalıdır.

Bu 10 kaynak, önceki ayrıntılı statik incelemelerle çakışabileceği için kayıtlı **45/92** sayısı artırılmadı. Aynı girdili bağımsız eski/yeni run, artifact SHA, timeout/retry ve yazma yan etkisi karşılaştırması olmadığı için **davranışsal kabul 0/92**. Üretime geçiş bloke.
