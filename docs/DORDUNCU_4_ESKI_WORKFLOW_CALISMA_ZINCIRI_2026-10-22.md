# Dördüncü kaynak çözümlemesi: dört eski workflow (40/99)

Kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Dört YAML doğrudan okundu. Yalnızca statik YAML kanıtıdır; çağrılan Python betiklerinin yan etkileri ve davranışsal eşdeğerlik ayrıca doğrulanmalıdır.

| Workflow | Aday sistem | Tetikleme | Çalışma zinciri | Kabulde korunacak davranış |
|---|---|---|---|---|
| `390-aday-tekrar-test.yml` | K3 | Manuel + `yedekler/tekrar_test_390.py` değişince push | ffmpeg kur; `TEST_WORKERS=10` ile 20 saniyelik paralel görüntü/ses testi; her koşulda artifact yükle | 90 dakika job timeout; `390-aday-tekrar-test` artifact; tarihli CSV ve M3U; 10 worker ve 20 saniye probelar |
| `aday-bekletme.yml` | K2/K3 | Manuel + sekiz aday/test betiğinde push | ffmpeg kur; tarama → tekrar ayırma → medya testi → bekletme → tekrar takvimi → zamanı gelen 5 aday testi → kaynak puanı → öncelik; her koşulda artifact | 90 dakika; sekiz adımın sırası; `RETEST_LIMIT=5`; 10 rapor yolu; `aday-bekletme-raporu` artifact |
| `aday-logo-epg-test.yml` | K2/K3 | Manuel + workflow veya birleştirme betiğinde push | Python sözdizimi → `CALISANLAR.m3u` SHA256 önce/sonra → aday EPG/logo birleştirme → 5 pilot EPG kanalı ve onaylanmamış aday kapısı → artifact | Korunan liste değişmezliği; `pilot_epg_channels==5`; hiçbir aday `playlist_approved` / `ready_for_playlist` olmamalı; JSON artifact |
| `aday-oncelik-kontrol.yml` | K2 | Manuel + öncelik betiğinde push | py_compile → geçici örnek klasörüne iki aday yaz → sıralama betiği → güçlü aday öncelik 1, zayıf aday 5 doğrulaması | Örnek veriyle sıralama ve üretim listesini değiştirmeme; artifact yükleme yok |

## Kritik farklar

- `aday-bekletme` sekiz aşamalı zincirdir; yalnızca tek bir aday taramasıyla eşdeğer sayılamaz. Gerçek yayın testi ve ağ bağımlılığı vardır.
- `390-aday-tekrar-test` yüksek maliyetli canlı ffmpeg testidir; opt-in olmadan çalıştırılmamalı.
- `aday-logo-epg-test` korunan dosyanın hash korunumu ve onay reddi koşullarını birlikte test eder; yalnızca JSON üretimi eşdeğerlik değildir.
- `aday-oncelik-kontrol` izole örnek veri testi içerir; gerçek aday sıralaması kabulü değildir.

Durum: ilk üç inceleme 36 YAML + bu dört YAML = **40/99 ayrıntılı statik kaynak çözümlemesi**. **59 YAML** henüz ayrıntılı çözümleme bekliyor. **92/92** davranışsal kabul bekliyor. Üretim dosyalarına dokunulmadı, Actions tetiklenmedi.
