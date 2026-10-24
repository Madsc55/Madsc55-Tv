# K5 — Eski workflow 21–30 doğrudan kaynak incelemesi

Kaynak: `Madsc55/madsc-tv` sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. On YAML doğrudan okundu; hiçbir workflow tetiklenmedi. Bu, **statik sözleşme incelemesidir**, davranışsal eşdeğerlik kabulü değildir.

| # | Workflow | Kaynaktan doğrulanan temel davranış | Timeout | Kritik fark / risk | Aday |
|---:|---|---|---|---|---|
| 21 | `iptv-test.yml` | Çarşamba 06:30 UTC zamanlı ve manuel kanal testi; `iptv_test.py` ile aday M3U; sonuçlar artifact | 60 dk | `CALISANLAR.m3u` artifact kapsamına girer; üretim liste değişmezliği ayrıca kanıtlanmalı | K1/K3/K5 |
| 22 | `kanal-kararlilik.yml` | Önceki gözlem cache restore, ffprobe, günler arası karşılaştırma, cache save | 30 dk | Cache key ve tarihsel gözlem aynı fixture olmadan eşdeğerlik iddiası yapılamaz | K3/K5 |
| 23 | `kaynak-puanlama-kontrol.yml` | Python sözdizimi ve kaynak güven puanı unittest | 5 dk | Mock fixture ile offline yürütmeye aday | K2/K5 |
| 24 | `madsc-11599-yedek-geri-yukle.yml` | 11599 yedek farkını yazmadan teşhis | 10 dk | Gerçek restore yapmaz; teşhis ve geri yükleme karıştırılmamalı | K4/K5 |
| 25 | `madsc-ana-liste-saglik.yml` | Ayın 1 ve 15'i sağlık kontrolü; önce/sonra korunan dosya SHA; 50'lik kanal batch | 35 dk | Salt-okunurluk ve korunan dosya değişmezliği kritik | K1/K3/K5 |
| 26 | `madsc-arsiv-yedek-aktarim.yml` | Manuel dry-run uyarısı; otomatik korunan liste değişimi kapalı | 15 dk | Eski workflow gerçek arşiv aktarımı yapmıyor; eşleştirme buna göre olmalı | K1/K4/K5 |
| 27 | `madsc-aylik-merkezi-denetim.yml` | Beş aşamalı merkezi sistem denetimi, geniş dosya-tetikleyici kapsamı | Tam YAML devamı ayrıca incelenmeli | İlk bölümde çok sayıda test/denetim bağımlılığı; tam komut ve artifact listesi henüz çıkarılmadı | K1–K5 |
| 28 | `madsc-birlesik-kesif.yml` | Günde 06:00/18:00 UTC keşif, failure gate, reset origin/main, canlı ffmpeg, arşiv, rapor ve GitHub yazma adımı | 45 dk | `contents: write`, `actions: write`; gerçek çalışma üretim yan etkisi doğurabilir | K1/K2/K3/K5 |
| 29 | `madsc-cuma-ana-liste-denetimi.yml` | Ana liste ve EPG salt-okunur kontrolü, uyarı özeti, rapor artifact | 55 dk | Canlı yayın testleri; kontrollü ağsız fixture gerekli | K3/K5 |
| 30 | `madsc-documentation-check.yml` | AGENTS, özellik envanteri, DEVAM notu ve M3U başlığını denetler | Tanımlı değil | Basit çevrimdışı fixture eşdeğerliğine aday | K1/K5 |

## Güvenli devam

İlk 30 workflow'un YAML dosyaları doğrudan gözden geçirildi. Bu 30'un tümünde script düzeyi semantik veya bağımsız eski-yeni yürütme doğrulanmış değildir. Özellikle #27'nin tam YAML gövdesi ayrı ayrıntılı inceleme gerektirir. Önceden raporlanan 45/92 statik incelemeyle mükerrerlik ayıklanmadan toplam inceleme sayısı yükseltilmemelidir. Davranışsal kabul 0/92 ve üretim kabulü kapalı kalır.
