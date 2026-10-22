## Üçüncü K3 turu — test fixture düzeltmesi (2026-10-23)
- `tests/test_epg.py` ilk üç testindeki M3U metinlerinin satır sonları çift kaçışlanmıştı (`\\n` metin olarak yazılıyordu). Gerçek satır sonu kaçışlarına çevrildi; testler artık `#EXTINF` satırlarını gerçekten içerecek.
- Test düzeltme commit'i: `ef728129a4bdebf8b1a84c14bb6cae806d2cf267`.
- Ayrı yerel davranış harness'inde güncel validator mantığı ve dokuz senaryo çalıştırıldı: 9/9 geçti. Bu, repodaki `tests/test_epg.py` dosyasının kendisini çalıştırmak veya tam depo test paketini çalıştırmak değildir; bu ikisi ve GitHub Actions hâlâ bekliyor.
- Üretim verilerine dokunulmadı; `[skip ci]` kullanıldı.

---

## İkinci K3 sertleştirme turu — M3U tvg-id (2026-10-23)
- `madsc/epg.py`, aynı `#EXTINF` satırında birden fazla `tvg-id` niteliği bulunduğunda artık `ValueError("Duplicate M3U tvg-id attribute")` ile fail-closed davranır. Böylece regex'in ilk değeri alıp çakışan metadata'yı sessizce yok sayması önlenir.
- Tek `tvg-id` değerinin çevresindeki boşluklar normalize edilerek eşleme yapılır.
- Kod commit: `6dcaaace0f8cb4faad0185584f6aafa319090159`; test commit: `73fdc790449f6c571b644729aa988d8f954d7304`; K3-13 görev defteri güncellemesi: `15e3ca6a4a3787f8b0c16e648179ec833843524a`.
- Bu turda mevcut doğrulama mantığının odaklı yerel davranış denemeleri 5/5 geçti: duplicate tvg-id reddi, eksik/boş programme channel reddi, tanımsız programme channel eşlemesinin başarısız olması ve tvg-id kenar boşluğu normalizasyonu. Bu, tam depo test paketi veya GitHub Actions başarısı değildir.
- Üç yeni birim testi değil, bu turda `tests/test_epg.py` dosyasına iki regresyon testi daha eklendi; toplam 9 test fonksiyonu var.
- Actions bilerek tetiklenmedi. Canlı yayın, IBO Player Pro, Pages zinciri ve gerçek EPG görüntülemesi hâlâ kanıtlanmadı.

---

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
