# Beş eski yüksek-yazma-riskli workflow — kaynak YAML incelemesi (22 Ekim 2026)

Kaynak: `Madsc55/madsc-tv` commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. İnceleme yalnız GitHub üzerinden **salt okunur** yapıldı. Aşağıdaki satır numaraları kaynak YAML dosyalarına aittir; doğrudan veya dolaylı script yan etkilerinin tamamının doğrulandığı anlamına gelmez.

| Eski YAML | Sabit kaynak blob SHA | Doğrudan gözlenen yetki ve yan etki | K1–K5 tasarım kararı |
| --- | --- | --- | --- |
| `madsc-birlesik-kesif.yml` | `da472ae0e45aa0d3c03a7dc8f9833bf43f733902` | Satır 7–8: `contents:write`, `actions:write`; satır 42–51: discovery before/after ve EPG join adımı **`if: false` ile atlanıyor**; satır 90–97: `git add madsc_kesif/`, protected gate, `git push origin HEAD:main`. | K2 aday/rapor davranışı K5'e salt okunur kanıt olarak aktarılabilir; git push ve canlı keşif onaysız etkinleştirilmez. EPG join'in yürütüldüğü iddia edilemez. |
| `epg-gunluk.yml` | `d43d5c469b54b8ef89794e8fcc2c2cee9b0d84b9` | Satır 7: `contents:write`; satır 25–28: EPG üretim ve hazır olma betikleri; satır 33–34: EPG XML/JSON çıktıları `git add`, gate ve `git push`. | K1 korunan EPG yazmasını bloke eder; K3/K5 yalnız fixture/rapor denetimini taşıyabilir. Otomatik EPG yayını ve cihaz kabulü yok. |
| `madsc-son-kontrol.yml` | `08871f1b397184459a093606c2519e1c19e5167a` | Satır 11–12: `contents:write`, `actions:write`; satır 42: `final_validation.py`; satır 54: korunan liste ve dizinler için diff kontrolü; satır 69–73: sonuç JSON'ları `git add`, gate, `git push`. | K1 + K3 + K5: rapor kanıtı ayrılmalı, push/retry yan etkisi taşınmamalı. |
| `madsc-genis-kaynak-kontrol.yml` | `396d33dd8d5f3440dc81ae76abb91fc0d43f6a94` | Satır 5–6: `contents:write`, `actions:write`; satır 27–31: geniş kaynak taraması; satır 56–61: `madsc_genis_tarama/` stage, gate, push. | K2 keşif çıktısı K5 raporuna bağlanabilir; yazma yetkisi ve canlı tarama otomatik açılmaz. |
| `madsc-ibo-354-classify.yml` | `165bb7fc69775be790beab972dc68e92cf40c2c3` | Satır 7: `contents:write`; satır 15: sınıflandırma betiği; satır 21–24: **`CALISANLAR.m3u`** ve IBO arşivlerini stage, gate ve `git push`. | K1 mutasyon yasağı nedeniyle doğrudan taşınamaz. K4 yalnız izole kopya/restore kanıtı; gerçek liste değişikliği yok. |

## Davranış eşdeğerliği için gerekli ayrım

1. **Okuma/hesaplama:** Komutun kaynak sürümü, girdi ve çıktı formatı, hata/timeout, tekrarlama, artifact isimleri ve korunmuş dosyalara dokunmama koşulu ayrı ayrı kanıtlanmalı.
2. **Yan etki:** Eski workflow'un `contents:write`, `actions:write`, `git push`, cron veya `CALISANLAR.m3u` yazması yeni K1–K5'e otomatik aktarılmaz. Eski davranışın ne yaptığı kaydedilir, fakat yeni üretim mutasyonuna onay verilmez.
3. **Kabul:** Beş YAML'ın kaynak komut/izin incelemesi yapıldı; bunlar 92 kapsam workflow'unun davranışsal eşdeğerlik onayı değildir. Kabul sayaçları **0/92, 0/26, 0/22** olarak kalır.

**Sonraki kaynak adımı:** Bu beş YAML'ın çağırdığı Python betiklerini sabit kaynak commit'inde tek tek inceleyip dolaylı yazma yollarını ve hata semantiğini çıkarmak; ardından K1/K2/K3/K4/K5 karşılıklarının gerçek yürütme kanıtlarını ayrı bağlamak.
