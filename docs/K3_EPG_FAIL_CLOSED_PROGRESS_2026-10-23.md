# K3 — EPG/XMLTV eşleme sertleştirmesi ve açık kabul boşlukları
Tarih: 2026-10-23 (Europe/Stockholm)
Depo: Madsc55/Madsc55-Tv, main

## Bu turda yapılan değişiklik
- `madsc/epg.py` artık her XMLTV `programme` öğesinde boş/eksik `channel` değerini fail-closed reddediyor.
- Program `channel` referansları XMLTV `channel id` kümesine karşı doğrulanıyor; eşleşmeyen program referansı `matching_verified=false` yapıyor.
- M3U `tvg-id` alanları eşlemeden önce kenar boşluklarından arındırılıyor.
- Validator'ın yalnız yapısal eşleme kontrolü yaptığı, IBO cihazında EPG görüntüsünü kanıtlamadığı açıkça belgelendi.
- `tests/test_epg.py` içine üç regresyon eklendi: eksik programme channel, boş programme channel, XMLTV channel listesinde bulunmayan programme channel.
- `docs/K1_K5_KANITLI_GOREV_DEFTERI.json` içindeki K3-13 kanıt notu güncellendi.

## Git kayıtları
- `62211f43813ef87ec8a75329cf89506dcebac261` — `madsc/epg.py` fail-closed doğrulaması.
- `4a3eee527902eea22a99afc9f82901ae3e837ed4` — üç EPG regresyon testi.
- `b700d68370b261567a1c6518db5ebc70e98f2753` — K3-13 görev defteri kaydı.
- Bu commit'lerde `[skip ci]` kullanıldı. Bu turda testler yerel ortamda çalıştırılmış gibi gösterilmedi; yeni GitHub Actions sonucu yok ve CI bilerek tetiklenmedi.

## K3 kabul durumu — tamamlandı olarak işaretlenmedi
- K3-09: 75 adayın gerçek, zamana yayılmış tekrar testleri bekliyor.
- K3-10: üç aşama / en az altı saat süreklilik değerlendirme mantığı var; bağımsız kökenli gerçek ağ ölçümleri yok.
- K3-11: gerçek yayın için ffprobe/ffmpeg kanıtı bekliyor.
- K3-12: IBO Player Pro cihaz kabulü kullanıcı cihazında yapılmalı; bu oturum cihazı kontrol etmiyor.
- K3-13: yerel XMLTV/tvg-id yapısal denetimi güçlendi; IBO/Pages canlı zinciri doğrulanmadı.
- K3-14: gerçek logo ve kanal kimliği görsel doğrulaması bekliyor.

## Kısıtlar ve sonraki adımlar
- `.github/workflows/madsc-k3-live-manifest-pilot.yml` ve `.github/workflows/madsc-k3-turkish-tv-video.yml` yalnız `workflow_dispatch` ile tetikleniyor. Bu turda dispatch/rerun yapılmadı.
- Üretim playlist'i, XMLTV/EPG, favoriler, YEDEKLER/YENİLER, logolar, cihaz veya arşiv verileri değiştirilmedi.
- Sonraki güvenli adım: EPG birim testlerini offline çalıştırıp sonucu doğrulamak; ardından yetkili, bağımsız kaynaklı dış ağ ölçümleri ve kullanıcı tarafından IBO cihazında gözlenen EPG sonucu olmadan K3 üretim kabulü vermemek.
- Genel kabul sayaçları değişmedi: 92 workflow 0/92, 26 runtime güvenlik kuralı 0/26, 22 ana görev 0/22.
