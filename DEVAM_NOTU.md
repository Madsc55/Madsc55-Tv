# K3 YEREL HEDEFLİ TEST KANITI — 2026-10-23
- GitHub `madsc/epg.py` blob `29fac7a619b198c6207767ba113e6a9d7c6629cf` esas alınarak ayrıştırıcı mantığı geçici yerel ortamda yeniden kuruldu. `python -m py_compile` geçti; 6 odaklı senaryo geçti: geçerli eşleşme, tırnaklı virgül, eksik stream URI, çift tvg-id, eksik tvg-id, sahte tvg-id.
- Bunlar GitHub test dosyasının tamamının koşulduğu veya birebir kaynak dosyanın çalıştırıldığı anlamına gelmez. Tam unittest suite / CI hâlâ doğrulanmadı. GitHub clone denemesi DNS kısıtıyla başarısız oldu.
- Canlı HLS video/ses, 6+ saat, Pages/XMLTV, logo kimliği ve en son kullanıcının IBO Player Pro cihaz kabulü açık. Üretim verilerine dokunulmadı.

---

# K3 M3U YAYIN ADRESİ KONTROLÜ — 2026-10-23
- Kod commit `21939da0e88779891d23cc8ca2b501c7ba94385d`: `#EXTINF` kaydının ardından yayın URI'si yoksa veya yeni `#EXTINF` gelirse fail-closed `ValueError` verir. Yayın adresi içeriğini indirmez/değiştirmez.
- Test commit `2497512559a354f0a2785b417563ae245fd1c002`: eksik URI ve ikinci `#EXTINF` regresyonları.
- Güncel değişiklikler için tam unittest/CI çalıştırma kanıtı yoktur; başarı iddiası yok. K3 canlı HLS/video/ses, 6+ saat, Pages/XMLTV/logo ve en son kullanıcı IBO Player Pro kabulü açıktır.
- Üretim playlist/XMLTV, favori, logo, arşiv ve cihaz verilerine dokunulmadı; PR #71 merge edilmedi.

---

# K3 SÖZDİZİMİ DÜZELTMESİ — 2026-10-23
- Önceki `madsc/epg.py` commitinde `matches` ifadesine yanlışlıkla literal `\\n` dizisi yazılmıştı; Python sözdizimini bozuyordu. Commit `74f4710099cc3ffd3a493a502cdb1cd00b6eac61` ile gerçek satır sonları kullanılarak onarıldı.
- `tvg-id` nitelik başlangıcının başka tırnaklı niteliğin içinde kalmadığı da kontrol ediliyor.
- Bu turda GitHub'a erişen ortamdan tam repo clone veya test çalıştırması yapılamadı (ağ DNS kısıtı); CI başarılı diye işaretlenmedi. Canlı kabul ve cihaz kabulü açık.

---

# K3 EK DÜZELTME — 2026-10-23
- `madsc/epg.py` commit `de5dd1a8ab09ff1d2ee41f2d2670397e5588bf8b`: tvg-id yalnız gerçek M3U nitelik anahtarından okunur; diğer tırnaklı niteliklerin metnindeki sahte tvg-id yok sayılır.
- `tests/test_epg.py` commit `269416752f6ac678f9e0fa43abfef778716a266a`: bu durum için regresyon eklendi.
- Yerel küçük ayrıştırıcı örnekleri (tırnak içi virgül, sahte tvg-id, tekrar eden tvg-id) denendi; **tam unittest/CI suite çalıştırılmadı**. Canlı HLS/6+ saat/Pages/XMLTV/logo ve en sonda kullanıcı cihaz kabulü açık.
- Üretim verileri korunmuştur; PR #71 birleştirilmedi. [skip ci] commitleri CI sonucu olarak değerlendirme.

---

# K3 SON GÜNCELLEME — 2026-10-23
- Kod commitleri: dea1d9c15f03b1f5f1833f7e3bf789d7a2a86cb8 (EXTINF ayıracı yoksa reddet), 57dad5f4c70505e59d8888c504e98d0643ccf9c8 (tırnak içindeki virgülü ayıraç sayma).
- Test commitleri: a0da67add7764bf9c2f51ecadb45820898ac7af7 (eksik virgül regresyonu), 1d9ff2d5091e4bcf30c367a4ff046758ec7f9390 (tırnak içi virgül ve bozuk tırnak testleri). İlk test ekleme commitindeki satır sonu kaçışları sonraki committe düzeltildi.
- Bu turda tam offline suite veya Actions çalıştırılmadı; yeni commitler için CI başarı kanıtı yok. [skip ci] kullanıldı.
- K3 canlı HTTPS/HLS video-ses, 6+ saat süreklilik, Pages/XMLTV canlı zinciri, logo/kanal kimliği ve en sonda kullanıcının IBO Player Pro cihaz kabulü halen açık. K3-13 kapanmadı.
- Üretim playlist/XMLTV/favori/logo/yedek/arşiv/cihaz verileri değiştirilmedi; PR #71 birleştirilmedi. K1/K2/K4/K5 işlerine dokunulmadı.
- Sonraki adım: yeni regresyonları ve offline gate'i yetkili ortamda çalıştır, sonra ayrı izin gerektiren canlı kanıtları topla; test edilmemiş kodu başarılı sayma.

---

# EN YENİ K3 GÜNCELLEMESİ — cihaz testi en sona (2026-10-23)
- Kullanıcı talimatı: IBO Player Pro cihaz kabulünü **en sona bırak**; kullanıcı cihazda kendisi deneyip sonucu bildirecek. Cihaz testi yapılmış gibi gösterme, kullanıcıdan şu aşamada isteme.
- `madsc/epg.py`: playlist içinde tekrar eden aynı `tvg-id` değerlerini `duplicate_playlist_ids` alanında raporlar ve `matching_verified=false` yapar. Kod commit `c2419d1f700b04752c0fb0c7d0e51b142707990a`.
- `tests/test_epg.py`: bu davranışı doğrulayan regresyonla toplam 16 EPG testi; commit `2dddb7493762b35519073cd619b1ce324c22818a`.
- GitHub Actions offline run `39870201168`, tested commit `21410cc6101ca5fad8b4500a74e9c955f23e9ecd`: **success**, `tests_discovered=1039`, `test_exit_code=0`, `tests_passed=true`, `all_offline_gates_passed=true`. Test edilen commit 16 EPG testini ve duplicate tvg-id kodunu içeriyor.
- Sonraki işler: K3 gerçek HTTPS manifest/video/ses pilotlarının kontrollü kanıtları, 6+ saat bağımsız süreklilik, Pages/XMLTV canlı zinciri, logo/kanal kimliği; **en son** kullanıcı tarafından IBO Player Pro cihaz kabulü.
- Üretim playlist, XMLTV, favori, logo, yedek, arşiv, cihaz verilerine dokunma; PR #71 merge etme. K3-13 canlı kabul bitene kadar açık.

---

# EN YENİ K3 GÜNCELLEMESİ — 15 EPG testi içeren offline suite başarılı (2026-10-23)
- M3U başlığı ve tvg-id ayrıştırması sıkılaştırıldı. `tvg-id` yalnız `#EXTINF` virgülünden önceki nitelik alanında aranıyor; görünen kanal adındaki sahte metin kabul edilmiyor.
- GitHub Actions run `39868761301`, tested commit `bbb975e650456ae29d89d5c66dbc4ce51e7c2f6a`: **success**. Log: 1020 test keşfedildi, `test_exit_code=0`, `tests_passed=true`, `all_offline_gates_passed=true`, K3 fixture success.
- Tested commit'te `tests/test_epg.py` 15 test içeriyor; EPG kod/test blob'ları `03755ace638bf3f788b8d3cfdf95d7d77ef077ed` / `aea48db70cee57802dda5e993d365c1e53ab6480`. Rapor: `docs/K3_HARDENING_2026-10-23.md`.
- Daha yeni `main` HEAD K1/K2/K4 commit'lerini de içeriyor; son başarılı suite ile K3 dosyalarının blob'ları aynı. Güncel HEAD üzerinde tekrar koşu yine tercih edilir.
- Canlı HLS video/ses, 6+ saat süreklilik, Pages/XMLTV canlı zinciri, IBO Player Pro EPG ve logo doğrulaması açık. Canlı pilot workflow'ları `workflow_dispatch` ile tanımlı, ancak bu oturumdaki GitHub aracı manuel workflow dispatch yapamıyor; çalıştırılmış gibi raporlama.
- Üretim verilerine dokunulmadı; PR #71 merge edilmedi; genel sayaçlar 0/92, 0/26, 0/22. K3-13 açık kalsın.

---

# EN YENİ K3 GÜNCELLEMESİ — 1017 test başarılı (2026-10-23)
- `madsc/epg.py` artık `tvg-id` değerini yalnız `#EXTINF` satırının virgülden önceki nitelik alanından okur; görünen kanal adındaki sahte `tvg-id` kabul edilmez.
- EPG test sayısı 15. GitHub Actions Offline Unit Tests run `39868610849`, commit `8e78f26d855f8c4bb89b22f1b8f026d4a6234902`: **success**, 1017 test keşfedildi, `test_exit_code=0`, `tests_passed=true`, `all_offline_gates_passed=true`, K3 fixture success.
- Rapor: `docs/K3_HARDENING_2026-10-23.md`. Test edilen commit'te EPG kod/test blob'ları `03755ace638bf3f788b8d3cfdf95d7d77ef077ed` / `aea48db70cee57802dda5e993d365c1e53ab6480`.
- Canlı HLS video/ses, 6+ saat süreklilik, Pages/XMLTV canlı zinciri, IBO cihaz EPG'si ve logo doğrulaması açık. Üretim verilerine dokunulmadı; PR #71 merge edilmedi; genel sayaçlar 0/92, 0/26, 0/22.
- K3-13 tamamlanmış sayılmasın; offline CI üretim kabulü değildir.

---

# EN YENİ K3 GÜNCELLEMESİ — EXTINF başlığı sahte tvg-id düzeltmesi (2026-10-23)
- Yeni hata düzeltildi: virgülden sonraki kanal görünen adındaki `tvg-id="..."` metni artık gerçek M3U niteliği olarak kabul edilmiyor. `madsc/epg.py` yalnız `#EXTINF` satırının virgülden önceki nitelik bölümünü tarıyor.
- Kod commit: `2e1ee36d2f54b9d8a6b72eb43751ab4e60224c9f`; regresyon testi commit: `7ced6524a166c76c1994a7f0d79574c519c7dc17`; EPG test sayısı 15.
- Ortak offline suite run #99 / `39868459061` daha önce 1016 testi geçti (o commit'te 14 EPG testi vardı). En yeni kod/test commit'lerinin Actions koşuları iptal edildi; 15. test için henüz başarılı CI kanıtı yok. K1–K5 eşzamanlı commit'leri tek pending concurrency yuvasını sürekli değiştiriyor.
- K3 canlı video/ses, 6+ saat süreklilik, Pages/XMLTV zinciri, IBO cihaz EPG kabulü ve logo doğrulaması açık. Üretim verilerine dokunulmadı; PR #71 merge edilmedi; genel sayaçlar 0/92, 0/26, 0/22.
- Yeni commit'ler durulduğunda tam offline suite'i güncel HEAD üzerinde doğrula; CI geçmeden 15 testin tamamı geçti deme.

---

# EN YENİ K3 GÜNCELLEMESİ — EPG sertleştirmesi tam offline suite'te geçti (2026-10-23)
- M3U header token doğrulaması sıkılaştırıldı; `#EXTM3U-invalid` reddediliyor. `tvg-id` yalnız gerçek whitespace-delimited nitelik olarak algılanıyor; `not-tvg-id` eşleşmesi reddediliyor.
- `tests/test_epg.py`: 14 EPG testi. Bu testler main commit `a0469c34ec9a8642acffdddfbda55dadf9d39aba` içinde mevcut.
- GitHub Actions Offline Unit Tests run #99 / ID `39868459061`: success; 1016 test keşfedildi, `tests_passed=true`, `all_offline_gates_passed=true`, K3 izole fixture success. Kanıt raporu: `docs/K3_HARDENING_2026-10-23.md`.
- Bu, offline doğrulamadır; gerçek HLS video/ses, 6+ saat süreklilik, Pages/XMLTV canlı zinciri, IBO Player Pro cihaz EPG'si ve logo doğrulaması hâlâ açık. K3-13 tamamlandı olarak işaretlenmesin.
- Üretim playlist/EPG/cihaz verileri değiştirilmedi; PR #71 merge edilmedi; genel sayaçlar 0/92, 0/26, 0/22.
- Sonraki adım: yetkili canlı manifest/video pilotunu kontrollü olarak çalıştırıp raporu gözden geçir; CI başarısını canlı kabul yerine kullanma.

---

# EN YENİ K3 GÜNCELLEMESİ — EPG regresyon CI başarılı (2026-10-23)
- EPG test fixture'larının ilk üçündeki çift kaçışlı satır sonları düzeltildi; test sayısı 9'dan 12'ye çıkarıldı. Eklenenler: geçersiz M3U başlığı, yanlış XMLTV kökü ve bozuk XML.
- GitHub Actions Offline Unit Tests run #89, ID `39867960099`, tested commit `474dc5392538fa1bca9d920d9285aa4dc9af1696`: **completed / success**. Log açıkça `tests_passed=true`, `all_offline_gates_passed=true`, K1-K5 isolated fixture kategorilerinin tamamı success gösteriyor. Bu production certification değildir.
- Kanıt raporu: `docs/K3_CI_PASS_2026-10-23.md`; görev defteri güncellemesi commit `09caa5c4375f7ab1b1768f889bab867bdbcd0b35`.
- K3 gerçek yayın/ffprobe, 6+ saat bağımsız süreklilik, IBO cihaz EPG kabulü, Pages canlı EPG zinciri ve logo doğrulaması hâlâ açık. Üretim playlist/EPG/cihaz verilerine dokunulmadı; PR #71 merge edilmedi; sayaçlar 0/92, 0/26, 0/22.
- Sonraki adım: CI başarısını yalnız offline kanıt olarak tut; K3-13 canlı zincir ve cihaz kabulünü doğrulanana kadar in_progress bırak.

---

# EN YENİ K3 GÜNCELLEMESİ — EPG test fixture hatası düzeltildi (2026-10-23)
- `tests/test_epg.py` içindeki ilk üç M3U fixture'ında çift kaçışlı satır sonları düzeltildi; artık gerçek `\n` kaçışları kullanılıyor.
- Test düzeltme commit'i: `ef728129a4bdebf8b1a84c14bb6cae806d2cf267`; rapor güncellemesi: `1d92ad7902bb589e8eb4776cb1caa86c9895e505`; görev defteri güncellemesi: `8222a57863020218e9e4017f5993a41d9d059539`.
- Ayrı yerel davranış harness'i: 9/9 senaryo geçti. Repo test dosyası ve tam depo test paketi bu turda çalıştırılmadı; Actions çalıştırılmadı.
- K3 gerçek yayın/ffprobe, 6+ saat bağımsız süreklilik, IBO cihaz kabulü, Pages EPG zinciri ve logo doğrulaması açık. Üretim playlist/EPG/cihaz verilerine dokunulmadı; PR #71 merge edilmedi; sayaçlar 0/92, 0/26, 0/22.
- Sonraki adım: test fixture düzeltmesini mevcut ana test koşumunda çalıştırıp gerçek CI kanıtı elde et; sonra dış ağ/cihaz kabulüne ilerle.

---

# EN YENİ K3 GÜNCELLEMESİ — M3U tvg-id sertleştirmesi (2026-10-23)
- Aynı M3U `#EXTINF` satırında duplicate `tvg-id` artık reddediliyor; tek değer çevresindeki boşluklar normalize ediliyor.
- Kod: `6dcaaace0f8cb4faad0185584f6aafa319090159`; test: `73fdc790449f6c571b644729aa988d8f954d7304`; K3-13 görev defteri: `15e3ca6a4a3787f8b0c16e648179ec833843524a`; rapor: `7badc4f3a7d4ebc9a9ca298ffbd956bc1458184e`.
- Odaklı yerel davranış denemeleri: 5/5 geçti. Tam depo test paketi ve GitHub Actions çalıştırılmadı; CI sonucu iddia etme.
- K3 canlı yayın/ffprobe, bağımsız 6+ saat süreklilik, IBO cihaz kabulü, Pages EPG zinciri ve logo eşlemesi hâlâ açık. Korunan üretim dosyalarına dokunulmadı, PR #71 merge edilmedi; sayaçlar 0/92, 0/26, 0/22.
- Sonraki adım: değişen dosyaları ve HEAD'i tekrar kontrol et; güvenli offline regresyon paketini çalıştırma imkânı varsa kullan; dış kanıt olmadan K3 kabulünü kapatma.

---

# EN YENİ K3 GÜNCELLEMESİ — 23 Ekim 2026
- Bu turdaki K3 EPG/XMLTV değişiklikleri: `madsc/epg.py` artık eksik/boş XMLTV `programme channel` alanını reddeder; XMLTV'de tanımlanmayan programme channel eşleşmeyi başarısız yapar. Üç regresyon testi eklendi.
- Kod commit: `62211f43813ef87ec8a75329cf89506dcebac261`; test commit: `4a3eee527902eea22a99afc9f82901ae3e837ed4`; görev defteri commit: `b700d68370b261567a1c6518db5ebc70e98f2753`; K3 raporu: `docs/K3_EPG_FAIL_CLOSED_PROGRESS_2026-10-23.md` commit `0b544c35b1bd469eec9bc75190848324ef789ee8`.
- Bu commit'ler `[skip ci]` ile kaydedildi; CI veya yerel test sonucu iddia edilmiyor. Actions dispatch/rerun yapılmadı.
- K3 gerçek yayın/ffprobe, 6+ saat bağımsız süreklilik, IBO Player Pro cihaz kabulü, Pages EPG zinciri ve logo kimliği hâlâ açık. K3 kabulü tamamlanmış sayılmadı.
- Korunan üretim dosyalarına dokunulmadı; PR #71 merge edilmedi. Genel sayaçlar 0/92, 0/26, 0/22.
- Güncel main HEAD'i bu nottan sonra yeniden kontrol et; eşzamanlı değişiklik varsa onu esas al.

---

# Madsc55-Tv — DEVAM NOTU

> Son doğrulama: 22 Ekim 2026, kod/test SHA `61bbf78214a63400083cf7d615c64a1b13547896`; 800/800 offline test + beş kapı, kurulum, rapor round-trip ve statik sözleşme kapısı başarılı. Ayrıntı en sondaki kayıt ve `K1_K4_K5_PENDING_VALIDATION_2026-10-22.json`. Gerçek kabul 0/92, 0/26, 0/22.

**Son paket:** 776 test ve bütün offline kapılar geçti. Mevcut toplu CLI'ye açık opt-in API+ZIP bayt doğrulaması bağlandı; gerçek GitHub sorgusunda güncel aynı-input çift bulunmadı. 0/92, 0/26, 0/22 korunur. Ayrıntı son kayıtta.


**Son paket:** 769 test ve bütün offline kapılar geçti; 11 statik sözleşme farkı 0'a indirildi. Ana K2 geçmiş kaynak paketi/tüketim bağlantısı yerelde doğrulandı. Gerçek 92/26/22 kabulü açık; ayrıntı son kayıtta.


**Son birleşik doğrulama:** 764 test + beş izole kapı + kurulum + beş rapor/K5 başarılı. İki süre farkı giderildi; dokuz artifact adı farkı incelemeye açık. Ayrıntı en sondaki operasyon sözleşmesi kaydında.


**En güncel doğrulanmış paket (22 Ekim 2026):** Kod/test/kanıt SHA `e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991`; güncel main üzerinde **760/760 yerel test**, beş izole K kapısı, kurulum envanteri ve beş rapor/K5 round-trip başarılı. Ayrıntı en alttaki kayıtta. Tam kabuller değişmedi: 0/92, 0/26, 0/22.

**En yeni kayıt:** Yeni sohbet devri tamamlandı: SOHBET_DEVIR_2026-10-22_SON.md. Son doğrulanmış paket 757 test+5 kapı+5 rapor/K5; sonraki 3c228e7 modülü henüz test edilmedi. Önce son devir kaydını oku.

## YENİ SOHBETE GEÇİŞ — önce bu özeti oku (22 Ekim 2026)

- Kullanıcı bu sohbetten yeni sohbete geçiyor. Geliştirmeyi baştan kurma; bu dosyanın güncel main sürümü, BIRLESIK_KALICI_CALISMA_KURALLARI.md ve PROJE_HAFIZASI.md son kayıtları başlangıç kaynağıdır. Yeni sohbette önce GitHub main HEAD'ini doğrula; otomatik görev arada ilerlemişse yeni kayıt üstün gelir. Önceki tüm sohbetlerin otomatik eksiksiz görüldüğünü varsayma.
- Tek yazılabilir hedef **Madsc55/Madsc55-Tv/main**. Bu geliştirme öncesi main: **c1fe77e309eaa6332c54add4d858058c7ee993de**. Son geliştirme kodu: **e10fcdc4c878305ca44e110b29ad88128cf16cb2**. Bu devir bir not kaydıdır, yeni kod/test değildir; kendi commit SHA'sı dosya geçmişindedir.
- Son test kanıtı: **632 yerel test + beş izole K1–K5 kapısı success**; kaynak 92+7, 10 yardımcı komut ve 22 görev envanteri geçti. docs/PARITY_CONTROLLED_TIMEOUT_KANIT_2026-10-22.json güncel kanıttır. GitHub Actions başlatılmadı.
- Tamamlanmış işleri tekrarlama: 92/99 kapsam mutabakatı; K1 rapor/summary/aktarım yazıcı korumaları; izole deneme playlist+JSON paketi; FIFO ve okuma sırasında değişen dosya reddi; gerçek dosyadan snapshot/manifest üreticileri; K1/K4/K5 default-false opt-in kancaları; kaynak Git blob/SHA256 + output role preflight'ının provenance CLI/API/artifact karşılaştırıcılarına bağlanması. Ön kontrol yalnız açık replacement_workflow_root argümanıyla devrededir; argüman yoksa checked=false. Bunlar gerçek legacy runtime kabulü değildir.
- **İlk sıradaki somut kod işi:** failure diagnostic artifact üyelerinin hash ve outcome JSON doğrulamasını mevcut provenance artifact/API zincirine bağla. K1/K4/K5 ölçülen timeout adaptörü ve workflow bağlantısını tekrar kurma; ayrıntılı sonraki adım son kayıtta.
- Açık dış kanıtlar: K2/K3 karşılaştırılabilir ortak input canlı ağ/harici geçmiş/aday kaynaklarına bağlı; eski 92 tarafta v1 manifest artifact eksik; opt-in gerçek run/artifact kökeni yok. 75 adayın zamanlı üç örnek/6+ saat ölçümleri, gerçek ffprobe/ffmpeg, kullanıcı IBO Player Pro cihaz sonucu, EPG/Pages/logo kimliği, bağımsız harici backup/restore ve VOD/arşiv/periyodik tetik kanıtları açık. **Tam kabuller 0/92, 0/26, 0/22**; fixture yeşilini bunlara ekleme ve genel bitiş yüzdesi uydurma.
- **Kesin korumalar:** canlı ana kanal listeleri/playlist, EPG/XMLTV, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logolar ve korunan arşivlere yazma. Eski Madsc55/madsc-tv salt okunur; eski depoya commit/Actions yapma, eski depoyu veya PR #71'i birleştirme; merge yapma. Kanıt olmadan eski otomasyon kapatma.
- **Test/kota:** güvenli yerel offline test ve kod/not kayıtları yetkili. GitHub Actions dispatch/rerun, canlı stream probing ve üretim yazma için ayrı açık izin yok; çalıştırma. Commitler [skip ci]. Her önemli gelişmeden sonra son kod SHA, yapılan iş, failure'lar, kanıtlar, kalanlar ve sonraki adımı bu dosya ve PROJE_HAFIZASI.md'ye kaydet. Eşzamanlı main değişirse yeniden oku, yeni commitleri ezme; yalnız erişilebilir commit/run kanıtını başarı say.
- **Otomatik devam doğrulandı:** saatlik Madsc55-Tv Otomatik Devam görevi 6ad2b2e925bc8191a91b01728e57d707 aktif; prompt en son kod/test ve sıradaki işe güncellendi. Güncel notu her tur okur. Sabah raporu görevi 6ad950197fbc8191b905c13fb344b920 aktif; Europe/Stockholm günlük 08:00 civarı, raporlama salt okunur. Yeni sohbet için aynı görevleri tekrar oluşturma. Saatlik tur, kesintisiz çalışma/bitiş garantisi değildir; görev sonuçları ilgili görev sohbetinde görünebilir, bu yeni sohbeti otomatik devraldığı iddia edilmez.
- Yeni sohbet başlangıç talimatı: “Madsc55/Madsc55-Tv main dalındaki DEVAM_NOTU.md dosyasının en üstündeki yeni sohbet özetini ve en son kayıtlarını oku. Güncel HEAD'i doğrula; yapılmış işleri tekrarlamadan ilk açık somut işten devam et. Tüm korumaları uygula, değişiklik ve kanıtları GitHub'a kaydet.”

Güncelleme: 22 Ekim 2026 (Europe/Stockholm).
Son geliştirme commit SHA: bd641a057d9ff47a2daeeddbef7eab742779db93
Bu notu kaydeden commit, yukarıdaki kod commit'inin doğrudan çocuğudur; kendi SHA'sı GitHub dosya geçmişindedir.

## Her yeni sohbette ilk adım
Bu dosyayı, BIRLESIK_KALICI_CALISMA_KURALLARI.md ve PROJE_HAFIZASI.md son bölümünü oku. GitHub main HEAD'ini doğrula. Tamamlanan inceleme ve testleri yeni sebep olmadan tekrarlama.

## Kullanıcının kalıcı görev ve sınırları
- Tek yazılabilir hedef: Madsc55/Madsc55-Tv, main. Main'in güncel durumundan K1–K5 eksiklerini topluca incele, kodları düzelt, yerel testleri çalıştır, ilerlemeyi GitHub'a kaydet. Engellenmedikçe çalışmayı sürdür, sonunda kanıtlı rapor ver.
- Eski 92 otomasyonun gerçek davranışsal entegrasyonunu doğrula; kaynak incelemesi veya fixture yeşil diye tamamlandı deme.
- Canlı kanal listelerini, EPG'yi, YEDEKLER, YENİLER, FAVORİLER ve cihaz favorilerini değiştirme. Logo/arşiv korumaları da geçerli.
- Eski Madsc55/madsc-tv salt okunur. Eski depoyu veya PR #71'i birleştirme; merge yapma.
- Her önemli geliştirmeden sonra bu dosyaya son kod commit SHA, tamamlananlar, başarısız testler, kalan görevler ve bir sonraki adımı yaz.
- Mevcut kota kararı: GitHub Actions için ayrıca açık izin gerekir; “devam/testleri çalıştır” tek başına bu izin değildir. Commitlerde [skip ci]; canlı probing ve üretim yazma yok.

## Bu pakette tamamlananlar
1. legacy_parity_cli ve legacy_99_bulk_audit çıktıları K1 enforce_local_output_path ile korunuyor: korunan dosya, symlink üst dizin ve mevcut hedef reddi. Audit ağ çağrısından önce hedefi kontrol ediyor; hedef üst klasör mevcut olmalı.
2. 92/99 sayım farkı kaynakla doğrulandı. Eski denetim beş merkezi workflow ile k1-protected-write-tests.yml ve madsc-hizli-on-kontrol.yml dosyalarını 92 kapsamından çıkarıyor.
3. Kaynak tree a88dfa874b6964dcaa4de7a8f9075af2f146acd8, commit ca374df3b9585c0d76a078db9536150ebbc260f7; eski denetim script blob SHA 9a35ecd797e5c1c595d6796cfffba6cd8a289853. Script içeriği ve tree kaydı eşleşti; 99 workflow yol/blob SHA docs/LEGACY_SOURCE_SCOPE.json içinde. Bu tur 99 YAML içeriği yeniden indirilmedi.
4. reconcile_legacy_scope kapsam değişimini reddediyor; offline_gate 92+7 ayrımını artık zorunlu denetliyor. Bu, davranışsal kabul değildir.
5. Yerel python -m madsc.offline_gate: 552 test başarılı; beş izole K kapısı success; 10 yardımcı komut ve 22 görev envanteri geçti. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22.json (test edilen kaynak SHA256'ları dahil).

## Başarısız testler ve denemeler
- Bu pakette başarısız test yok. İlk düzeltmede 549, nihai kapsam paketiyle 552 test başarılı.
- GitHub tree sorgusunda slash içeren branch URL'si connector tarafından INVALID_ARGUMENT ile reddedildi; aynı sorgu tekrarlanmadı, belgelenmiş sabit tree SHA ile başarılı okundu.
- Son gözlenen Actions #39686179902 success, SHA d5d61317806dc7a00b762567695286e3779ceaf1; yeni kodun CI kanıtı değil. Bu tur Actions başlatılmadı.

## Açık işler / dürüst kabul durumu
- 92 davranış için tam kabul 0/92, runtime güvenlik 0/26, tam görev 0/22. Statik 99 kaynak envanteri ve 92 kapsam mutabakatı bu sayıları artırmaz.
- Eski/yeni aynı girdide gerçek execution çiftleri, artifact kökeni ve SHA, tetik/izin farkları, hata/timeout/retry ve yan etkiler karşılaştırılmalı. Mevcut snapshot karşılaştırıcısı provenance doğrulamıyor ve kabul vermiyor.
- K2 gerçek kaynak/lisans ve bağımsız geçmiş artifact kanıtı; K3 75 adayın zamanlı gerçek ölçümleri, üç örnek/6+ saat, ffprobe/ffmpeg, IBO kullanıcı cihaz sonucu, EPG/Pages ve görsel kimlik açık.
- K4 bağımsız harici yedek makbuzu ve hariciden izole restore, VOD/arşiv ve periyodik tetik kanıtı açık.
- K1 tüm yazıcıların çağrı noktaları ve 26 runtime kuralı; K5 gerçek uçtan uca kanıt zinciri açık.

## Sonraki somut adım
92 kapsamını yeniden araştırma: reconcile_legacy_scope ve pinned JSON kullan. K5 karşılaştırmalı kanıt çiftlerini bu 92 gerçek kaynak yoluna bağla; aynı girdi hashleri ve bağımsız köken doğrulamasının eksikliğini gider. Yeni rapor yazıcı ekleme; ortak K1 kapısını kullan. Gerçek cihaz/harici depolama kanıtını uydurma ve korunan üretim verilerine yazma. Mevcut kodun güvenle tamamlanabilen kısmını sürdür.

## İkinci önemli geliştirme — son kayıt
- Kod commit SHA: 268f16d304d4ce68fb9cbc201d51d34d793707c6. Önceki paket: 53ca22f2781d106139d52a20493e223b391418fd.
- history_origin_cli, batch_acceptance, handoff_acceptance ve legacy_notes_integrity ortak K1 çıkış kapısı + exclusive create kullanıyor. İlk üç komut korunan/mevcut/symlink hedefi kanıt işleme veya GitHub doğrulama başlamadan reddediyor. Çıktı üst klasörü mevcut olmalı.
- Son test: 554 test ve beş izole K1–K5 kapısı success; başarısız test yok. git diff --check temiz. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET2.json. Önceki 552 sonucu önceki pakete aittir.
- Son CI artifact listesi yalnız metadata düzeyinde incelendi, 92 gerçek karşılaştırma kanıtı kabul edilmedi. Yeni Actions yok. Kabul sayıları 0/92, 0/26, 0/22.
- Sıradaki bağımsız yerel iş: tüm kalan yazma noktalarını çağrı zinciriyle denetle (özellikle ci_diagnostics --summary append ve canlı pilot rapor yazıcıları); onaysız canlı probing yapmadan gerçek yazma reddini fixture ile sına. Sonra 92 gerçek execution/artifact çiftlerinin köken ve girdi hash bağını tamamla. Bu tur tüm yazıcılar kapandı iddiası yok.
- Korunan yayın/EPG/yedek/favoriler ve eski depo değişmedi; PR #71 merge edilmedi. Bu kalıcı sınırlar sonraki sohbetlerde de geçerli.

## 22 Ekim 2026 — Otomatik devam ve sabah raporu
- Kullanıcı kalan işlerin otomatik sürdürülmesini ve sabah raporunu istedi. Mevcut saatlik ChatGPT görevi 6ad2b2e925bc8191a91b01728e57d707 güncellendi: Madsc55-Tv Otomatik Devam. Eski depoya yönelik talimat kaldırıldı; tek yazılabilir hedef Madsc55/Madsc55-Tv/main. Saatlik çalışma turu, kesintisiz çalışma garantisi değildir.
- Mevcut sabah görevi 6ad950197fbc8191b905c13fb344b920 güncellendi: Europe/Stockholm yaklaşık 08:00, flexible_schedule (saatin bir saat çevresinde). Sonuçları salt okunur doğrulayıp raporlar; geliştirme yapmaz. Mevcut günlük tekrarı korundu.
- Her geliştirme turu önce güncel main ve bu notu okur; tamamlanan işleri tekrarlamaz, kod/test ilerlemesini GitHub'a ve devir notuna kaydeder. Gece ara bildirim yerine kalıcı kayıt kullanır.
- Tüm korumalar geçerli: canlı kanal/EPG/yedek/yeni/favoriler değişmez, eski depoya yazılmaz, PR #71 merge edilmez; Actions/live probe ayrı izin olmadan çalıştırılmaz. Bitmiş veya kanıtlanmış olmayan kabul uydurulmaz.
- Son geliştirme SHA ve 554 test sonucu yukarıdaki kayıtta korunuyor; otomasyon kurmak yeni test veya geliştirme kanıtı değildir. Sonraki kod işi değişmedi: kalan yazıcıların K1 çağrı noktası denetimi.

## Üçüncü önemli geliştirme — güncel devam noktası
- Son kod commit SHA: e5222e2aff553c65c27e1678365a95fa6e40f39e. Başlangıç main: d70479db18814251247b7da6cae72520982a56b3. Bu notu kaydeden commit kodun doğrudan çocuğudur.
- Tamamlanan: CI JSON raporunda exclusive create, açık summary append için K1 protected/symlink/regular/hardlink kapısı ve O_NOFOLLOW/fstat; dört pilot JSON raporu mevcut ortak write_fixture_report üzerinden yazılıyor. K3 reason_counts tek yazıdan önce tamamlanıyor.
- progress_scorecard ve k5_channel_gate hedefi giriş işlemeden önce doğruluyor. artifact_transport/history_transport guard öncesi mkdir yapmıyor. History artifact indirme/extraction ve legacy rapor export hedefleri ortak K1 kapısında; üst klasör önceden mevcut olmalı.
- Başarısız test kaydı: LegacyReportExportTests.test_exports_separate_legacy_artifacts bir ara turda ERROR verdi; mevcut klasör reddinde eski ValueError sözleşmesi değişmişti. ValueError kontrolü korunarak düzeltildi, finalde geçti.
- Nihai test: python -m madsc.offline_gate, 562 test, K1/K2/K3/K4/K5 izole kapıları success; kaynak 92+7, 10 yardımcı komut ve 22 görev envanteri geçti. git diff --check temiz. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET3.json, test edilen dosya SHA256 ve çözülen hata dahil. Ağ/Actions/cihaz testi yapılmadı.
- Gerçek dosya sınırları test edildi: mevcut summary ekleme; protected/symlink/hardlink/FIFO reddi; pilot rapor üzerine yazmama; guard reddinde klasör oluşturmama ve indirme çağırmama. Bu testler 26/26 tam runtime kabulü değildir; tüm yazıcılar tamamlandı denmez.
- Kalan ilk yerel iş: turkish_tv_batch_validation.py yalnız reports/ altındaki deneme M3U8 + JSON paketinin yazma yolunu güvenli ve tekil hale getir. Mevcut genel M3U yasağını gevşetme; korunan listelere yazma. Bu pakette bu dosya değiştirilmedi. Diğer kalan çağrı noktalarını da incele.
- Sonraki davranışsal iş: pinned 92 kaynak yoluna aynı girdi hashleri ve bağımsız execution/artifact kökeni bağlı eski/yeni karşılaştırma. 92/99 farkını tekrar araştırma; çözülmüş kapsam JSON'unu kullan.
- 0/92 tam legacy kabul, 0/26 tam runtime kabul, 0/22 görev kabulü korunuyor. IBO kullanıcı cihazı, 75 adayın zamanlı ölçümleri, EPG/Pages ve bağımsız harici restore kanıtları açık.
- Korunan yayın/EPG/yedek/yeni/favori verileri, eski repo ve PR #71 değişmedi. Saatlik otomasyon bu güncel kaydı başlangıç almalı; eski 554 sonucu güncel sonuç diye tekrarlamamalı.

## Dördüncü önemli geliştirme — toplu K3 kanıt yazıcısı
- Son kaydedilmiş kod commit SHA: fe40f60aa989c121144cdbdca0bdd38f7d67f607; başlangıç main 861932763c247b5402015e3bd33ab403854fddac.
- turkish_tv_batch_validation deneme M3U8 + JSON kanıt paketi ortak K1 yerel sınırlarına bağlandı. Genel M3U/M3U8 yasağı değiştirilmedi; yalnız sabit reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8 yolu için dar, üretim izni vermeyen kapı var.
- İki dosya exclusive create ile yazılıyor; mevcut kanıt, symlink reports klasörü ve politika dışı M3U8 reddediliyor. JSON yazımı başarısız olursa bu çağrının oluşturduğu playlist geri alınıyor. Mevcut çıktı tarama/probe başlamadan reddediliyor.
- Yerel python -m madsc.offline_gate: 568 test ve K1–K5 izole kapıları başarılı. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET4.json. Ağ, Actions ve cihaz testi yapılmadı.
- Bu fixture sonucu 0/92, 0/26 ve 0/22 kabullerini değiştirmez. Korunan üretim playlist/EPG/yedek/favori dosyalarına dokunulmadı.
- Şu an üzerinde çalışılan sonraki iş: pinned 92 kapsamı için aynı input SHA256 ve ayrı execution/artifact kökenini zorunlu kılan karşılaştırma şeması. Gerçek GitHub origin doğrulaması olmadan acceptance verme.

## Beşinci önemli geliştirme — 92 workflow köken-bağlı karşılaştırma kontratı
- Son kod commit SHA: f222a81ce96901a8adc0dbc92a5213cf149500c9; taban fe40f60aa989c121144cdbdca0bdd38f7d67f607.
- compare_provenance_bound_batch yalnız reconcile_legacy_scope tarafından sabitlenen 92 yolu kabul ediyor. Yedi merkezi/kapsam dışı workflow kanıt çifti olarak verilemez.
- Her çift aynı input SHA256'yı kullanmalı. Legacy tarafı eski repo/dal/yol ve pinned git_blob_sha'ya; replacement tarafı yeni repo main ve beş merkezi workflow'dan birine bağlanıyor.
- Run id/attempt/head SHA ile artifact repository/run/head/id/SHA256 bağları ve iki tarafın ayrı execution/artifact kökenleri yapısal olarak zorunlu. Snapshot çıktı/yan etki/timeout/exit karşılaştırması bundan sonra bu bağın içinde yapılıyor.
- Offline metadata bağı gerçek GitHub API doğrulaması değildir: independent_origin_api_verified false, kabul 0/92 kalır. CLI yeni madsc-legacy-provenance-pairs-v1 şemasını tanır; eski snapshot modu geriye uyumlu fakat kabul vermez.
- Nihai yerel test: 570 test ve beş K kapısı success; docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET5.json. Başarısız test yok, git diff --check temiz; Actions/ağ/cihaz yok.
- Sıradaki somut iş: GitHub salt-okunur run ve artifact metadata doğrulamasını bu v1 kontratına bağlayan bağımsız verifier/client ekle. Gerçek legacy ve replacement run çifti bulunmadan 92 sayaçlarını artırma.
- Korunan listeler/EPG/yedek/yeni/favoriler, eski depo ve PR #71 değişmedi; merge ve Actions dispatch yapılmadı.

## Altıncı önemli geliştirme — bağımsız GitHub origin doğrulayıcısı
- Son kod commit SHA: 7b4855293564c1baafdca8246f932ca1a1e5986e; taban main 80bcb8dc4328351660d586730f9f4676307d4e6f.
- github_legacy_pair_client her execution için üç ayrı salt-okunur GitHub kaydı ister: run, run artifact listesi ve run head SHA'sındaki workflow blob'u. İki taraf için toplam altı API okuması yapar; dispatch/rerun/yazma yoktur.
- Repository, branch, workflow path, run id/attempt/head/event/conclusion, workflow blob SHA ve artifact id/name/run/head/SHA256 digest bağları fail-closed doğrulanır. Eksik digest, eksik pagination, yanlış blob veya repository reddedilir.
- İki origin API düzeyinde doğrulansa ve snapshot eşleşse bile behavioral_parity_accepted ve production_ready false kalır; reviewer/gerçek davranış kabulü ayrıca gerekir.
- Yerel toplu sonuç: 573 test ve K1–K5 izole kapıları başarılı. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET6.json. Başarısız unit test yok. Kapsamsız git diff --check bir kez signal 11 verdi; iki değişen dosyada scoped diff --check ve tam offline_gate geçti.
- Salt-okunur gerçek kontrol: yeni run 39686179902 artifactleri ve eski run 39590927353 artifactleri SHA256 digest taşıyor. Ancak eski run k1-protected-write-tests.yml, pinned 92 davranış kapsamının dışındaki yedi dosyadan biridir; bu iki run aynı-girdi 92 çifti değildir ve kabul verilmedi.
- Sıradaki somut iş: artifact içindeki manifestten input SHA256 ve snapshot bağını güvenli biçimde çıkarıp GitHub artifact digest/run origin doğrulamasına bağla. Sadece metadata içindeki beyanı aynı-girdi kanıtı sayma.
- Kabul sayaçları 0/92, 0/26 ve 0/22. Korunan veriler, eski depo ve PR #71 değişmedi; Actions başlatılmadı.

## Yedinci önemli geliştirme — artifact baytına bağlı aynı-girdi manifesti
- Son kod commit SHA: b1be6c247b769bc911773ed35d30b5991875b913; taban ca2b33fb45d188cbe2ce6a9ea164d677dc084e0e.
- legacy_pair_artifact, SHA256'sı API origin kaydına bağlı artifact ZIP'i sınırlı ve fail-closed okur. Yalnız tek madsc-parity-evidence.json kabul edilir; ekstra entry, symlink, büyük ZIP/manifest, aşırı sıkıştırma, bozuk/duplicate-key JSON reddedilir.
- Manifest repository/run/head/workflow_path, input_sha256 ve snapshot alanlarını execution origin beyanına bağlar. İki artifact manifesti aynı input SHA256 taşımadan pair karşılaştırması geçmez.
- Yerel sonuç: 576 test ve beş izole K kapısı success. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET7.json. Ağ/Actions/canlı probing yok.
- Bu, gelecek artifactlerin üretim kontratıdır; geçmiş run artifactleri bu manifest şemasıyla üretilmediği için geriye dönük 92 kabulü yaratmaz. behavioral_parity_accepted=false ve production_ready=false.
- Sıradaki somut iş: beşli workflow'ların opt-in parity artifact üretim yolunu bu manifest şemasına bağla; eski taraf için salt-okunur gerçek 92 run artifacti yoksa açık blocker olarak bırak. Actions izni olmadan çalıştırma.
- Kabul 0/92, 0/26, 0/22; korunan dosyalar/eski depo/PR #71 değişmedi.

## Sekizinci önemli geliştirme — K1 korumalı replacement manifest üreticisi
- Son kod commit SHA: c5a7060684e57f1e35d2b367e1757d5901dfcafb; taban f4198b56cd9e3e40c45797cb9ae74b934a1fa043.
- parity_manifest_writer gerçek input baytlarının SHA256'sından deterministik madsc-parity-artifact-v1 JSON üretir; snapshot şekli/digestleri mevcut fail-closed karşılaştırıcıyla doğrulanır. Çıktı yalnız reports/madsc-parity-evidence.json ve ortak K1 izole yazıcısı üzerinden exclusive-create/symlink/ancestor/root kontrolleriyle yazılır.
- Üretici yalnız Madsc55/Madsc55-Tv, main ve depoda gerçekten kurulu beş workflow yolunu kabul eder. Önceki replacement kontratındaki var olmayan K4/K5 adları madsc-04-arsiv-yedek.yml ve madsc-05-genel-bakim.yml düzeltilerek madsc-04-yedek.yml ve madsc-05-bakim.yml oldu. Eski adlar pinned legacy 92+7 kapsam dışlamasında aynen ve doğru biçimde kalır.
- Yerel python -m madsc.offline_gate: 580 test, beş izole K kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; path-scoped git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET8.json.
- Actions, canlı probe, cihaz veya üretim yazması yapılmadı. Manifest üretimi artifact upload/origin doğrulaması veya parity kabulü değildir; sayaçlar 0/92, 0/26, 0/22.
- Açık engel: eski salt-okunur 92 workflow artifactlerinde v1 manifest üretimi yok. Gerçek aynı-girdi çifti için iki tarafta gerçek davranış girdisi ve snapshot üretimi gerekir; eski tarafa yazmadan bu tur tamamlanamaz.
- Sıradaki güvenli adım: replacement üreticisini gerçek davranış girdisi ve snapshotı olan açık opt-in job çağrılarına bağlayacak CLI/iş akışı kontratını ekle. Yalnız beyan edilen hash kabul etme; input baytını yerinde hashle. Actions izni olmadan çalıştırma ve legacy kabulü verme.

## Dokuzuncu önemli geliştirme — gerçek dosyadan opt-in manifest CLI
- Son kod commit SHA: 6b07cb1a7fa27e643e89cad6f1a7ffdb5a5d2c1a; taban e80291daf5225b60a1fa327610d5c88a0b9d138b.
- parity_manifest_cli beyan edilmiş bir input hash kabul etmez. Gerçek input ve snapshot dosyalarını read-only açar; O_NOFOLLOW (platformda varsa), fstat regular-file ve boyut sınırlarını uygular; input baytlarını kendisi SHA256 ile bağlar. Snapshot JSON duplicate key reddiyle okunur ve sıkı snapshot şemasından geçer.
- CLI repository/branch/run/head kimliğini GitHub runtime environment değişkenlerinden alabilir, workflow yolu açık argümandır ve gerçek beşli allowlist'ine tabidir. Çıktı yine sabit K1-korumalı reports/madsc-parity-evidence.json; artifact yüklemez, Actions başlatmaz, kabul vermez.
- İlk odak testinde test_real_file_bytes_are_hashed_and_written başarısız oldu: sabit test girdisinin beklenen SHA256 literal'i yanlıştı. Doğru hashlib sonucu yazıldı; odak testleri ve tam offline_gate geçti.
- Nihai yerel sonuç: 583 test ve beş K kapısı success; 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri geçti. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET9.json. Kabul 0/92, 0/26, 0/22.
- Açık: beş workflow'da gerçek davranış input/snapshot dosyalarını üreten ortak job sözleşmesi yok; mevcut fixture raporlarını davranış eşdeğerliği diye paketlemek yasak. Sıradaki adım, yalnız gerçek input/snapshot üretebilen workflow noktalarını statik eşleştirip güvenli opt-in entegrasyon planı/kontrat testi eklemek; Actions çalıştırmamak.

## Onuncu önemli geliştirme — ölçülmüş çıktı/yan-etki snapshot üreticisi
- Son kod commit SHA: 27c8b62165e511d09d42b319766a39d77994deb9; taban bedca31aef1998c51b23f468bf4bdd2950b9ea7c.
- parity_snapshot_writer ve CLI gerçek execution çıktı/yan-etki dosyalarını read-only açar, O_NOFOLLOW/fstat/2 MiB sınırı uygular ve SHA256'larını katı exit_code/timed_out/outputs/side_effects snapshot şemasına yazar. En az bir gerçek çıktı zorunlu; duplicate/control-character label, symlink, nonregular/büyük dosya ve mevcut snapshot reddedilir.
- Snapshot yalnız sabit reports/madsc-parity-snapshot.json yoluna ortak K1 izole writer ile exclusive create edilir; production_ready ve behavioral_parity_accepted false kalır.
- Uçtan uca offline test gerçek input baytı + gerçek çıktı baytı -> snapshot -> v1 manifest -> artifact ZIP digest/origin manifest doğrulamasını bağladı. Bu fixture origin/API veya 92 kabulü değildir.
- Nihai python -m madsc.offline_gate: 587 test, beş izole K kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; değişen dosyalarda git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET10.json.
- Actions/live probe/production write/eski repo yazısı yok. Kabul sayaçları 0/92, 0/26, 0/22.
- Açık blocker: mevcut beş workflow ortak gerçek davranış input ve side-effect dosyası üretmiyor; fixture raporunu parity kanıtı diye yeniden adlandırmak yasak. Sonraki güvenli iş workflow job'larını read-only statik denetleyip hangi gerçek çıktının hangi input/side-effect kaydıyla bağlanabileceğini makine-okunur readiness raporunda fail-closed göstermek; eksik olanı acceptance saymamak.

## On birinci önemli geliştirme — beş workflow parity readiness denetimi
- Son kod commit SHA: 79ddf0e7bbec7cdb47fb1a79e285f35d5c5e9b02; taban f4f14fd668e37ca382f50c2991c4c1616ed7fbd9.
- parity_workflow_readiness tam olarak depoda kurulu beş merkezi workflow'u okur ve açık opt-in, opt-in koşulu, snapshot CLI, manifest CLI, manifest artifact upload ve üretici sırası işaretlerini fail-closed denetler. Workflow kaynak SHA256'larını rapora bağlar.
- Whole-line comment örnekleri readiness sayılmaz; symlink, nonregular, boş/büyük ve UTF-8 olmayan workflow kaynağı reddedilir. Rapor yalnız reports/parity-workflow-readiness.json yolunda ortak K1 exclusive writer ile yazılabilir.
- Gerçek mevcut sonuç: 0/5 workflow marker kontratı tamam. Bu dürüst blocker kaydıdır. Tam marker'lı sentetik test bile runtime_origin_verified, real_behavior_ready ve behavioral_parity_accepted alanlarını false/0 tutar.
- Nihai python -m madsc.offline_gate: 590 test ve beş izole K kapısı success; 92+7 kapsam, 10 yardımcı komut, 22 görev envanteri geçti. Başarısız test yok; path-scoped git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET11.json.
- Actions/live probe/production write/eski repo yazısı yok. Kabul 0/92, 0/26, 0/22.
- Açık blocker: gerçek beşli job'larda ortak input/snapshot/side-effect sözleşmesi ve legacy 92 v1 artifactleri yok. Sıradaki güvenli adım, yalnız izole/gerçek dosya çıktısı olan K1-K5 yollarında açık opt-in marker zincirini eklemek için ortak workflow sözleşmesini tasarlamak; ağ/canlı/korunan veri yollarını bu entegrasyona dahil etmemek ve Actions çalıştırmamak.

## On ikinci önemli geliştirme — K4 ve K5 gerçek dosya dilimlerinde opt-in zincir
- Son kod commit SHA: 03fbcdb42cad69ae69641f2d4033b8537ee0f7b6; taban 3409a2c7a50ec20ae215f207c0af053a0740be05.
- madsc-04-yedek.yml restore drill'i ve madsc-05-bakim.yml içindeki K2 handoff dilimi default false allow_parity_evidence girdisi aldı. Her iki zincir de yalnız açık opt-in ile snapshot -> manifest -> tek JSON artifact üretir; depo permissions read-only kalır.
- K4 manifest input'u restore_drill'in gerçekten tükettiği reports/k4-source/nested/sample.txt, ölçülen output reports/k4-restore-drill.json. K5/K2 diliminde input artifact_transport'un tükettiği reports/k2-input.m3u, output reports/k2-candidates.json. Testler üretici komut < snapshot < manifest < upload sırasını zorunlu kılar.
- K1, standalone K2 ve K3'e sahte ortak input marker'ı eklenmedi. Readiness sonucu marker kontratı 2/5, fakat runtime_origin_verified=0, real_behavior_ready=0 ve acceptance=0; workflow'lar bu tur çalıştırılmadı.
- Nihai python -m madsc.offline_gate: 593 test, beş izole K kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; değişen dosyalarda git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET12.json.
- Actions/live probe/production write/eski repo yazısı yok. Kabul 0/92, 0/26, 0/22.
- Açık blocker: iki opt-in zincirin gerçek run/artifact kökeni henüz yok; Actions için ayrı izin gerekir. Eski read-only 92 artifactlerinde v1 manifest yok. Sıradaki güvenli yerel iş, K1/standalone K2/K3 için gerçek ve karşılaştırılabilir input bağının bulunup bulunmadığını statik komut/veri akışıyla sınıflandırmak; yoksa blocker bırakmak.

## On üçüncü önemli geliştirme — K1 guard gerçek input/output bağı
- Son kod commit SHA: 32db584bdeff7d2bc42bb54c68d7bf3c2aa3af17; taban e984ab5ddb8d043b974da93a74f7a625f0263af2.
- madsc-01-guvenlik.yml içindeki gerçek K1 guard'ın tükettiği config/shadow_manifest.json parity input oldu. Guard stdout'u bash pipefail + tee ile reports/k1-guard.txt dosyasına alınır; böylece hata kodu gizlenmeden gerçek çıktı snapshot içinde hashlenir.
- Default false allow_parity_evidence yalnız açık opt-in ile snapshot -> manifest -> reports/madsc-parity-evidence.json artifact zincirini çalıştırır. Permissions read-only, protected/production write yok. Readiness marker kontratı 3/5 oldu; runtime ve acceptance hâlâ 0.
- Standalone K2 ve K3 dosya tabanlı ortak karşılaştırılabilir girdi sunmuyor; mevcut yollar canlı/harici/örtük girdili olduğundan sahte marker eklenmedi.
- Odak test komutunda olmayan tests.test_madsc_guard modülü çağrıldığı için bir ImportError kaydedildi; gerçek tests.test_guard ile odak 18/18 ve ardından tam offline_gate geçti.
- Nihai python -m madsc.offline_gate: 593 test ve beş izole K kapısı success; 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET13.json. Actions çalıştırılmadı; kabul 0/92, 0/26, 0/22.
- Sıradaki güvenli yerel adım: K2/K3 blocker sınıflamasını makine-okunur dataflow raporuna bağlamak ve readiness denetçisinin marker eksikliğini gerçek input sınıfıyla açıklamasını sağlamak. Canlı/harici input için Actions veya probing yapma.

## On dördüncü önemli geliştirme — parity input veri-akışı sınıflaması
- Son kod commit SHA: 51267b0bee39522d2017381594827f4bf7d3265c; taban 2d584f703aabb3f7ab5c2af17c2683e5c3dd1f13.
- parity_workflow_readiness artık K1, K4 ve K5 için gerçek tüketici komutu, tüketilen input ve üretilen output tokenlarını parity snapshot/manifest sırasından bağımsız olarak doğrular. Üç yol `isolated_file_bound`; marker mevcut olsa bile tüketici input'u kayarsa bağ fail-closed bozulur.
- Standalone K2 `live_stream_sources_required`, standalone K3 `external_delivery_or_notification_state_required` olarak makine-okunur `external_or_live_input_blocked` sınıfındadır. Fixture input veya sahte runtime kanıtı üretilmedi.
- Odak 7/7 ve nihai `python -m madsc.offline_gate` 594/594 test başarılı; beş izole K fixture kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri geçti. Başarısız test yok; `git diff --check` temiz. Kanıt `docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET14.json`.
- Actions/live probe/production write/eski repo yazısı yok. Statik file binding 3/5; runtime origin ve gerçek behavior ready 0, kabul 0/92, 0/26, 0/22.
- Açık blocker: üç opt-in zincirin bağımsız gerçek run/artifact kökeni için ayrıca Actions izni gerekir; eski read-only 92 artifactlerinde v1 manifest yok. K2/K3 canlı veya harici girdiyi yetkisiz kullanmadan karşılaştırılabilir ortak gerçek dosyaya bağlanamıyor.
- Sıradaki güvenli yerel adım: readiness JSON şemasını ve üç statik bağın kaynak SHA/input/output alanlarını parity manifest karşılaştırıcısının preflight doğrulamasına bağlamak; bu işlem runtime/acceptance üretmemeli ve Actions çalıştırmamalı.

## Parity dosya okuma güvenliği — güncel kayıt
- Son kod commit SHA: 7635cbe28071df818ecdefb77cc43e40ea5ffb09; taban 53ca334a0eb7b209251f41b06909e5ebb0cfdf85. Eşzamanlı otomatik turdaki 51267b0 K2/K3 readiness geliştirmesi ve 53ca334 devir kaydı korunarak üzerine normal commit hazırlandı; eski HEAD'e zorla yazılmadı, merge yapılmadı.
- parity_manifest_cli ve parity_snapshot_writer FIFO açılışında fstat'a ulaşmadan bekliyordu. Gerçek FIFO alt süreç testi iki entrypoint'te de 2 saniye timeout verdi. O_NONBLOCK ile regular olmayan girdi artık beklemeden reddedilir.
- Gerçek dosya okuma sırasında değiştirildiğinde önceki iki negatif test hata atmadan kanıt üretildiğini gösterdi. Descriptor ve pathname dev/inode/size/mtime_ns/ctime_ns/nlink değerleri okuma sonunda denetleniyor; değişim, kaybolma veya aynı boyutta inode değiştirme tespit edilirse kanıt yazılmıyor. Bu metadata tutarlılık kontrolüdür; tam atomiklik veya execution boyunca input dondurma iddiası değildir.
- Başarısız test kaydı: FIFO manifest/snapshot alt vakalarında 2 ERROR (TimeoutExpired); input/output değişiminde 2 FAIL (ValueError gelmedi). Düzeltme sonrası hepsi geçti. Aynı boyutta dosya değiştirme de her iki entrypoint'te sınandı; ret durumlarında reports oluşmadı.
- Nihai birleşik yerel sonuç: python -m madsc.offline_gate, 598 test ve beş izole K kapısı success; 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri geçti. Kanıt docs/PARITY_FILE_READ_KANIT_2026-10-22.json. Paket14 dosyası otomatik turun ayrı kanıtı olarak aynen korundu.
- Kaydetme sırasında main değiştiği için ilk ref güncellemesi doğrulanamadı. Main yeniden okundu, yeni turun kod/testleri alınarak regresyon tekrarlandı ve güncel HEAD üzerine kaydedildi. Yalnız main'den erişilebilir son commitler ilerleme kanıtıdır.
- Önceki devirde K3 için yazılan external_delivery_or_notification_state_required ifadesi kaynak kod sınıfı değildir. Gerçek readiness kodundaki K3 engeli canlı stream probe/harici aday kaynağı; sınıf external_or_live_input_blocked'dır. K2 de canlı ağ/harici history girdisine bağlıdır. Bu ifadeleri delivery sistemi kurulmuş gibi yorumlama.
- Actions/live probe/cihaz/production write/eski depo yazısı yok. Korunan yayın listeleri, EPG, YEDEKLER/YENİLER/FAVORİLER ve PR #71 değişmedi; kabul 0/92, 0/26, 0/22.
- Sıradaki güvenli yerel iş: mevcut readiness'deki üç statik file binding kaydını parity manifest preflight doğrulamasına bağla; marker ya da yerel dosya hashini bağımsız runtime veya 92 kabulü sayma. Gerçek opt-in run/artifact kökeni ve legacy 92 v1 manifest eksikliği açık.

## Manifest karşılaştırıcısında kaynak workflow ön kontrolü — güncel kayıt
- Son kod commit SHA: 7beab850d06fb40d491d233d8bc3108ea984782b; taban 436266996ba86e28dcef9951954a1e460d21a801. Otomatik readiness geliştirmesi ve önceki FIFO/mutasyon düzeltmeleri korundu.
- Readiness kayıtlarına gerçek workflow_blob_sha (Git blob), workflow_sha256 ve declared_file_binding {consumer_command,input_path,output_label,output_path} eklendi. preflight_replacement_execution, sunulmuş bir readiness JSON'una güvenmeden kaynak workflow'ları yeniden okur.
- Kaynak markerları + statik input/output kontratı, origin.workflow_blob_sha ve snapshot'ın beklenen output label'ı birlikte doğrulanır. Yanlış/eski kaynak blob, kaynak drift'i, eksik çıktı rolü ve ortak izole input sözleşmesi olmayan K2/K3 fail-closed reddedilir. K1/K4/K5 kapsamı statik kontrattır; gerçek yürütme kabulü değildir.
- compare_provenance_bound_pair/batch, API origin doğrulayıcısı ve artifact manifest doğrulayıcısı replacement_workflow_root açık argümanıyla aynı kapıyı kullanır. CLI: --replacement-workflow-root PATH yalnız madsc-legacy-provenance-pairs-v1 girdisinde geçerlidir. Kaynak kökü, iddia edilen koşunun workflow blob'u ile aynı baytları içermelidir; yeni main'den farklı tarihsel kaynakta ön kontrol reddedilir.
- Argüman yoksa replacement_workflow_contract_checked=false ve replacement_static_preflight=null olur. Batch açıkça kaç çiftin statik kontratının kontrol edildiğini raporlar. v1 manifest formatı korunur. Statik ön kontrol input baytını veya bağımsız runtime kökenini doğrulamaz; ilgili alanlar false kalır.
- Uçtan uca test gerçek src.madsc_guard komutunu geçici gerçek config baytlarıyla çalıştırdı; stdout -> dosya snapshot'ı -> manifest -> ZIP -> kaynak preflight zinciri geçti. Bu testte legacy taraf fixture, API testi fake fetcher kullandı; gerçek 92 legacy execution veya canlı API kabulü yok.
- Nihai yerel python -m madsc.offline_gate: 605 test, beş izole K kapısı, 92+7 kaynak kapsamı, 10 yardımcı komut ve 22 görev envanteri success. Bu pakette başarısız test yok; git diff --check temiz. Kanıt docs/PARITY_WORKFLOW_PREFLIGHT_KANIT_2026-10-22.json kaynak hashleri ve statik binding kayıtları dahil.
- Korunan listeler/EPG/yedek/yeni/favori, eski repo ve PR #71 değişmedi. Actions veya gerçek ağ/cihaz testi çalıştırılmadı. Kabul 0/92, 0/26, 0/22; statik preflight bunu artırmaz.
- Sıradaki güvenli yerel iş: yalnız opt-in K1/K4/K5 tüketicileri için işlem öncesi/sonrası input hash bağını kur; tüketici çalışırken değişen dosyadan manifest üretilmesin. Gerçek runtime/artifact kökeni için ayrı Actions izni, eski 92 v1 manifestleri için mevcut salt-okunur kanıt gerekir; K2/K3 harici/canlı girdi engelleri açık.

## 22 Ekim 2026 — Opt-in parity girdi hash kontrolü (yeni sohbet)
- Kod commitleri: ffa4262c1ffa27e3c5c463810d840055aaf4640f (K1), b26d613e18afc93522b88676eac41893962927f0 (K4), 79ba7859632a4b88b698c5d8c80091f079dc1ad4 (K5/K2). Başlangıç main d2d2ea8acb661ea23653c5b8365d3904e7302491.
- Yalnız allow_parity_evidence=true iken gerçek tüketici komutundan hemen önce sha256sum kaydı alınıyor; manifest öncesinde ve manifest sonrasında sha256sum --check --status ile değişen input reddediliyor. Varsayılan opt-in false korunuyor; ayrı workflow/Actions başlatılmadı.
- ÖNEMLİ: Bu turda offline test çalıştırılmadı; 605 test önceki commitin kanıtıdır, yeni kodun test başarısı değildir. YAML/kontrat ve toplu offline_gate testleri henüz doğrulanmalı. Kodun hash kontrolü input dosyasının atomik dondurulması veya gerçek legacy runtime parity kanıtı değildir.
- Sonraki adım: kaynak YAML'larını ve statik readiness testlerini doğrula, gerekli kontrat testlerini güncelle, tek toplu offline regresyon çalıştır, başarısızlık varsa düzelt. GitHub Actions için ayrı izin gerekir. Kabul 0/92, 0/26, 0/22.
- Korunan playlist/EPG/YEDEKLER/YENİLER/FAVORİLER/logo/arşiv, eski repo ve PR #71 değişmedi; merge yapılmadı.

## 22 Ekim 2026 — Hash sırası kontrat testi
- Kod/test commit: 0abc1e5ab3243eb0a4bfd7d5df268153e597067b. tests/test_parity_workflow_integration.py içinde K1/K4/K5 için girdi hash kaydı < gerçek tüketici < ilk hash doğrulaması < manifest CLI < ikinci hash doğrulaması < artifact upload sırasını statik olarak denetleyen test eklendi.
- Test çalıştırılmadı: yerel container GitHub DNS çözümlemesi başarısız (Could not resolve host: github.com); GitHub Actions kota izni olmadığı için dispatch/rerun yapılmadı. 605 eski kanıt yeni commit için geçerli sayılmaz.
- Sonraki adım: erişilebilir checkout ile tek offline_gate, statik test ve YAML doğrulaması; hataları düzeltip kanıt SHA'larıyla kaydet. Tam kabul 0/92, 0/26, 0/22. Korunan üretim verileri, eski repo ve PR #71 değişmedi.

## 22 Ekim 2026 — 3/3 statik hash sırası kontrolü
- Kaynak HEAD ddebbac51b15a16e6d86e67633a504f9c6ca8a0c üzerinde K1/K4/K5 YAML dosyaları GitHub'dan yeniden okunarak tam sıralama koşulları 3/3 sağlandı. Kanıt: docs/PARITY_HASH_ORDER_STATIC_KANIT_2026-10-22.json (commit de0baa35997eb7eadcab996291c339651ae9970e).
- Bu sonuç yalnızca statik string/konum kontrolüdür; Python unittest, YAML parser, offline_gate, GitHub Actions ve gerçek davranışsal parity testleri ÇALIŞTIRILMADI. Yerel git clone DNS engelli; Actions izinsiz tetiklenmedi. Sonraki iş erişilebilir yerel checkout ile gerçek toplu test, hata düzeltmesi ve güvenli kanıt.

## Manifest girdisi işlem öncesi digest kaydına bağlandı — güncel devam
- Son kod commit SHA: 788a4b76ed96677d0ec05cb90e2f4fe835b611f1; taban e1b4997b796d4f17a0f08e4b59cf9a9c8d548aa8. Diğer sohbetin ffa4262/b26d613/79ba785 hash kontrolleri ile 0abc1e5 statik sıra testi korunarak kullanıldı. Başlangıç 8883d5c üzerinde 605 test gerçekten çalıştırılıp geçti; ardından yeni main'deki test de alınarak final regresyon yapıldı. Önceki DNS/“test edilmedi” kayıtları o turların durumudur, güncel sonuç aşağıdadır.
- parity_manifest_cli --input-digest-receipt kaydını bounded/nonblocking/non-symlink okuyucuyla okur. Tam tek satır sha256sum biçimi, lowercase digest ve birebir input yolu zorunludur. Manifestte kullanılan input baytlarının SHA256'sı işlem öncesi kayıtla eşleşmezse henüz snapshot/manifest yazmadan reddedilir. Yanlış digest/yol, çok satır veya bozuk kayıt çıktı oluşturmaz. Argüman yoksa sonuç input_digest_receipt_matched=false; v1 manifest şeması korunur.
- K1/K4/K5 manifest komutları bu kaydı açıkça kullanıyor. İlgili değiştirilen adım adları Türkçeleştirildi. Default-false opt-in, read-only permission ve üç kaynak sözleşmesi korunur; readiness/preflight artık capture < consumer < snapshot < ilk check < manifest+receipt < ikinci check < upload sırasını da ister. Eksik receipt bağı statik ön kontrolden geçmez.
- Gerçek workflow consumer/run blokları temporary dizinde bash -e -o pipefail ile çalıştırıldı (GitHub Actions değil). Üç gerçek tüketici: K1 guard, K4 restore drill, K5/K2 artifact producer. Her biri stable, tüketici sonrası değişim, precheck sonrası/manifest öncesi değişim, manifest sonrası değişim ve opt-out senaryolarında sınandı.
- Stable girdide manifest SHA doğru. İlk iki değişim senaryosunda manifest yok; manifest sonrası değişimde yerel manifest kalır fakat başarısız son kontrol publish simülasyonuna geçirmez. Opt-out girdide digest kaydı/parity manifest yok. Yayınlama bu testte yalnız yerel simülasyon işaretidir; gerçek artifact upload veya legacy runtime değildir.
- Nihai python -m madsc.offline_gate: **610 test ve beş izole K1–K5 kapısı success**, 92+7 kaynak, 10 yardımcı komut ve 22 görev envanteri geçti. Yeni geliştirmede başarısız test yok; git diff --check temiz. Kanıt docs/PARITY_INPUT_RECEIPT_KANIT_2026-10-22.json; taban SHA, test edilen kaynak hashleri, readiness ve senaryolar dahil.
- Bu endpoint hash bağları tam atomik input dondurma veya geçici değiştirip geri alma saldırısının tam ispatı değildir. Bağımsız run/artifact ve execution boyunca değişmez girdi kökeni hâlâ ayrı kanıt ister. Korunan kanal/EPG/yedek/yeni/favori/logolar/arşiv, eski repo ve PR #71 değişmedi; merge/Actions/live probe yok. Kabul 0/92, 0/26, 0/22.
- Sonraki güvenli yerel iş: üç opt-in üreticinin başarısız tüketici ve timeout durumlarında gerçek exit-code/snapshot/hata artifact akışını koru; şu an başarı yolundaki sabit --exit-code 0 failure parity kanıtı değildir. Kaynak preflight ve input digest bağını tekrar kurma. Hata raporlamak başarı kapısını veya işin gerçek hata kodunu gizlememeli.

## 22 Ekim 2026 — Failure/timeout snapshot regresyon testleri
- 823ab04e80a2e2842d49fbd2951eb92bd7c1bce8 commit'inde tests/test_parity_snapshot_writer.py içine iki yeni test eklendi: exit_code=23/timed_out=false ve exit_code=124/timed_out=true gerçek çıktı SHA256 korunumu; eksik failure log dosyası snapshot yazmadan fail-closed.
- Bu turda testler ÇALIŞTIRILMADI (container GitHub DNS engeli). Önceki 610 yerel test, bu yeni test commit'ini kapsamaz. Workflow tüketicilerindeki sabit --exit-code 0 henüz düzeltilmedi; failure/timeout opt-in akışını gerçek exit code ve log ile bağlamak ilk açık iştir. Actions izinsiz tetiklenmedi. Tam kabuller 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Opt-in tüketici failure snapshot akışı
- Kod: K1 118bed0e6e8869291fc305cabe4b7119a58bc8b5; K4 86164e1cac9984f35ab17923e78fee9d78990a57; K5 903ea0d750acf70e161de9d37879c0a07ded39fc. Tüketici nonzero dönerse gerçek exit code yakalanır, opt-in ve çıktı mevcutsa nonzero snapshot denenir, ardından orijinal exit code ile workflow step başarısız olur. K1 pipefail tüketici status'u PIPESTATUS[0] ile alınır. Başarılı yolun eski snapshot/manifesti korunur.
- Test kodu: 13008e629292a675bd6f03aada7829060f6e8f56 ve b3fab67ce9b5ce3761570d6ff489fb5160a16cec. Statik nonzero snapshot sözleşmesi eklendi; opt-in adım sayımı consumer içindeki failure snapshot'tan ayrıldı.
- SINIR: Çıktı üretmeden hata veren K4/K5 için snapshot oluşturulmaz (fail-closed); timeout-minutes ile runner kesilirse snapshot garantisi yok, timed_out=true yolu henüz bağlanmadı. Yeni kod/testler henüz yerelde ÇALIŞTIRILMADI, son 610 test önceki commit kanıtıdır. Actions tetiklenmedi. Sonraki adım yerel toplu regresyon + failure/timeout uçtan uca test; hata olursa düzelt. Kabul 0/92, 0/26, 0/22; üretim ve eski depo korumaları değişmedi.

## 22 Ekim 2026 — Hata snapshot'ı başarısızken orijinal exit code korunumu
- K1 209c368b3c70827e60939aa77b96ff6465ccd171, K4 07341e60fbc22d271103b5f6f5ecb5aa3a7171a9, K5 3621d20ab53999697c1079437a15e6d0ba5f57f1: opt-in failure snapshot CLI kendisi başarısız olsa bile uyarı verip tüketicinin orijinal nonzero exit code'una ulaşılır. Test kontratı c89f62480844f9eb167c9e0cca44aae34e5235b5.
- Test henüz çalıştırılmadı: yerel git ls-remote de GitHub DNS hatası verdi. 610 eski test kanıtı bu commitleri kapsamaz. Workflow job timeout-minutes nedeniyle sert kesilme halinde timed_out=true snapshot garantisi yok; ayrı kontrollü yerel timeout tatbikatı ve test gerekiyor. Actions tetiklenmedi. Tam kabuller 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Gerçek süreç gözlemi ve K1 pipe hata düzeltmesi
- Son kod commit SHA: 09e3b31ddc86c0a01ba9ea1bff153416705319c5. Başlangıç main c6e74cc53f21aae486cda7f191e3a11836ef87f8. Eşzamanlı failure snapshot kodu korundu ve ilk kez bu pakette toplu yerel regresyondan geçirildi.
- madsc.parity_process.observe_process gerçek returncode/stdout/stderr ölçüyor; monotonic timeout, shell kullanmayan argv, iki pipe eşzamanlı okuma, akış başına 1 MiB sınırı ve process-group temizliği var. Normal exit 124 timeout sayılmıyor. Gerçek timeout stderr çıktısı mevcut snapshot yazıcısına bağlanarak test edildi. Çıktı taşmasında eksik kanıt üretilmez. Bu API komut yetkilendirmesi veya üretim koruma sandbox'ı değildir; çağıran güvenli komutu seçmeli.
- K1 consumer PIPESTATUS artık hem tüketici hem tee sonucunu koruyor: tüketici başarılı olsa bile tee failure yeşile dönmez; tüketici failure önceliği korunur.
- İlk offline_gate 621 testte 7 failure verdi: altı girdi-mutasyon alt senaryosu yeni consumer içindeki failure snapshot komutunu yanlışlıkla başarı adımı seçiyordu; standalone başarı snapshot seçimi düzeltildi. Bir descendant kapanış testi OS sinyal yarışı nedeniyle erken okuyordu; 1 saniyelik sınırlı kapanış kontrolü eklendi. Başarısızlıklar gizlenmedi.
- Nihai python -m madsc.offline_gate: 621 test ve beş izole K1–K5 kapısı success; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/PARITY_PROCESS_KANIT_2026-10-22.json; test edilen kaynak hashleri kayıtlı. Actions/ağ/cihaz testi yapılmadı.
- ÖNEMLİ AÇIK: süreç gözlem API'si henüz workflow tüketicilerine bağlanmadı. K1/K4/K5 mevcut failure snapshot akışı yalnız mevcut normal çıktı için çalışıyor; gerçek timeout workflow snapshot ve her koşulda failure artifact yükleme garantisi yok. Sonraki somut iş: dar consumer CLI adaptörü + stdout/stderr tanı rollerini snapshot/preflight'a bağla; opt-in workflow adımlarında ölçülen sonuçla manifest/artifact üret, artifact sonrasında orijinal nonzero sonucu geri ver. Sabit exit-code 0'dan timeout kabulü türetme.
- K2/K3 ortak harici input, legacy v1 artifact/provenance, 75 aday ölçümü, cihaz ve bağımsız restore kanıtları açık. Tam kabuller 0/92, 0/26, 0/22. Korunan kanal/EPG/YEDEKLER/YENİLER/FAVORİLER, eski repo ve PR #71 değişmedi; merge/Actions yok.

## 22 Ekim 2026 — Bash failure exit yerel 3/3 senaryo
- Yeni unittest: tests/test_parity_workflow_integration.py, commit e6d6322a49d50dec6edca9133dfaf7bcce27ac89 (önceki taslak 917ab692 sözdizimi hatası aynı dosyada düzeltilmiştir).
- Yerel Python subprocess ile Bash shell-fixture 3/3 geçti: consumer=23 snapshot=0 -> exit 23; consumer=23 snapshot=31 -> exit 23; consumer=124 snapshot=31 -> exit 124. Bu test yalnız shell exit propagation semantiğidir; gerçek workflow/CLI timeout testi değildir. Tam repo 610+ unittest bu commit için çalıştırılmadı; yerel GitHub DNS engeli sürüyor.
- Sonraki iş: gerçek timeout flag'i ve consumer failure çıktı kanıtını test et; full offline suite erişilebilir checkout üzerinde çalıştır. GitHub Actions tetiklenmedi. Tam kabuller 0/92, 0/26, 0/22.

## 22 Ekim 2026 — GNU timeout kontrollü yerel doğrulama
- tests/test_parity_workflow_integration.py içinde GNU timeout gerçek kesme regresyonu eklendi: cc875429213ab2f1dcf255f5fbe0c7361a56a4d0. Yerelde `timeout 0.1s bash -c 'sleep 2'` gerçekten çalıştırıldı, snapshot komutu exit 31 verdiğinde son exit 124 olarak korundu. Önceki 23/0, 23/31, 124/31 yerel shell kontrolleri de 3/3 tekrar çalıştırıldı.
- SINIR: Bu sadece Bash/GNU timeout kontrolü; GitHub Actions job timeout-minutes tarafından kesilme halinde snapshot üretimi doğrulanmadı. Repo genel 610+ regresyonu bu committe çalıştırılmadı; git ls-remote GitHub DNS çözemedi. Eski 92 davranış kabulü 0/92, güvenlik 0/26, görev 0/22. Actions tetiklenmedi. Sıradaki iş: gerçek workflow timeout davranışı ve güvenli offline suite.

## 22 Ekim 2026 — Başarısız tüketici snapshot artifact kalıcılığı
- K1 b9f713453b14e35d27197b06f2de66494fb48534; K4 b3e899b41d4ff9e6094f5dd88557a5d93329c151; K5/K2 879fea336ca8e2b307a7e3fb734b40ea07282376. failure() && !cancelled() && allow_parity_evidence=true koşullu ayrı upload-artifact@v4 adımları eklendi; hata sırasında oluşan reports/madsc-parity-snapshot.json saklanabilir. if-no-files-found: ignore; çıktı/snapshot yoksa kabul veya sahte kanıt üretilmez.
- Test kontratı 5d4301c801b7a85ab0aae561ba75bd7b8f52fc9a: her üç workflow için ayrı failure artifact adı, opt-in ve failure koşulu, path, upload, fail-closed olmayan opsiyonel yükleme sırası. Yeni testler ve Actions bu turda ÇALIŞTIRILMADI. Önceki 610 test bunları kapsamaz. Gerçek GitHub job timeout kesilmesinde snapshot garantisi yok. Tam kabuller 0/92, 0/26, 0/22. Korunan içeriklere dokunulmadı.

## 22 Ekim 2026 — K1/K4/K5 kontrollü timeout ve failure kanıt zinciri
- Son kod commit SHA: e10fcdc4c878305ca44e110b29ad88128cf16cb2. Başlangıç main c1fe77e309eaa6332c54add4d858058c7ee993de; eşzamanlı failure artifact adımı ve GNU timeout regresyon testi korundu/geliştirildi. Bu not commit'inin kendi SHA'sı GitHub geçmişindedir.
- Yeni madsc.parity_consumer_cli yalnız üç sabit izole tüketiciyi shell kullanmadan çalıştırır. Varsayılan workflow opt-in false; açıkken ölçülen çıkış kodu, gerçek timeout flag'i, stdout/stderr ve outcome JSON kaydedilir. Normal çocuk exit124 timeout sayılmaz. Kontrollü üst sınır 120 saniye, job sınırı 10 dakika. Normal çıktı oluşmadan hata veren K5 için de tanı snapshot'ı var; eksik normal rapor uydurulmaz.
- Tüketici nonzero adımı başarısız kalır; continue-on-error yok. Mevcut failed-consumer-snapshot artifact adı korundu, ham stdout/stderr ve outcome eklenerek consumer failure koşuluna daraltıldı. always/!cancelled kanıt zinciri ön hash kontrolü -> manifest -> son hash kontrolü -> upload sırasını önceki adımın success sonucuna bağlar. Hash değişiminde manifest yayınlanmaz; ayrı tanı artifact'i saklanabilir. Normal başarı yolu mevcut dosya snapshot'ını kullanır.
- Failure static preflight yalnız üç tanı rolünün tamamı ve ölçülen tüketici kaynak kontratı varsa ilerler; başarı rolüyle hata kanıtı ikame edilemez. Bu hâlâ statik kontrol: tanı artifact baytlarının GitHub kökeni/indirme/hash doğrulaması bu pakette tamamlanmadı; tam davranışsal kabul yok.
- Process observer timeout sonrası pipe EOF bekleyişi readiness + sınırlı cleanup deadline ile düzeltildi; alt süreç sinyalinin asenkron teslimi eksik kanıt veya sınırsız beklemeye dönüşmemeli. Çıktı taşması, spawn/preflight/writer hatası tamamlanmış ölçüm diye sunulmaz.
- Gerçek yerel testler: üç workflow shell gövdesinde timeout -> exit124/timed_out=true -> manifest -> statik preflight; K1 gerçek stderr ardından timeout; normal exit124/timed_out=false; K1/K5 gerçek nonzero ve K5 normal çıktı yokluğu; failure manifest öncesi/sonrası input mutasyonu; mevcut hedefte süreç başlatmama; writer hatasında consumer exit korunumu; eksik tanı rolü reddi. Mevcut başarı/opt-out/üç input mutasyon regresyonları da geçti.
- Nihai python -m madsc.offline_gate: 632 test ve beş izole K1–K5 kapısı success; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. Üç YAML parse ve job içi step id tekilliği geçti; git diff --check temiz. Bu pakette başarısız test yok; önce 629, sonra mutation testiyle 630, eşzamanlı iki test korununca 632. Önceki 621/7-failure kaydı tarihsel olarak korunur. Kanıt docs/PARITY_CONTROLLED_TIMEOUT_KANIT_2026-10-22.json, test edilen kaynak SHA256'ları içerir.
- Sınırlar: Actions dispatch/rerun, canlı probing, cihaz testi veya eski repo çalıştırması yapılmadı. GitHub koşullarının gerçek runtime sonucu yok. Sert job timeout, iptal veya runner kaybında upload garantisi verilemez. Girdi endpoint hashleri atomik freeze kanıtı değildir. Tam kabul 0/92, 0/26, 0/22.
- Sonraki somut yerel iş: failure snapshot'ındaki process_stdout/process_stderr/process_outcome hashlerini gerçek diagnostic artifact üyeleriyle doğrulayan bounded ZIP/receipt kontrolünü mevcut provenance artifact/API zincirine bağla. Outcome JSON exit_code/timed_out ile manifesti eşleştir; missing/mutated/duplicate/symlink/oversize üyeyi reddet; yalnız manifest JSON'u eşleşti diye tanı baytları doğrulandı deme. Ardından eski/yeni aynı input ve ayrı GitHub execution/artifact çiftleri hâlâ dış kanıt bekler.
- Korunan kanal listeleri, EPG, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logo/arşivler değişmedi. Eski repo salt okunur, merge ve PR #71 merge yok. Sonraki tur güncel main ve bu kayıttan devam etmeli; tamamlanan timeout adaptörünü yeniden kurmamalı.


## 22 Ekim 2026 — Failure diagnostic artifact regresyon testi (yeni sohbet)
- Test commit: 21b82e923c9e644c7d6299175dde937731c14414; tests/test_failure_diagnostic_artifact_regression.py eklendi. Mevcut madsc/legacy_pair_artifact.py ve github_legacy_pair_client.py içinde tanı ZIP baytı + API köken doğrulayıcıları main üzerinde bulundu; tekrar yazılmadı.
- Yeni test vakaları: failure exit23, measured timeout exit124, missing/duplicate/mutated ZIP üyesi, outcome exit uyuşmazlığı, ayrı artifact ID zorunluluğu, symlink ve oversized entry reddi. Bu testlerin başarıyla çalıştığı iddia edilmez.
- Bu tur yerel git ls-remote https://github.com/Madsc55/Madsc55-Tv.git HEAD komutu DNS nedeniyle başarısız: Could not resolve host: github.com. Bu yüzden tam repo checkout, yeni unittest ve python -m madsc.offline_gate ÇALIŞTIRILAMADI. Önceki 632 test sonucu yeni commit'i kapsamaz. GitHub Actions tetiklenmedi.
- Sonraki ilk iş: erişilebilir checkout üzerinde python -m unittest tests.test_failure_diagnostic_artifact_regression -v ve python -m madsc.offline_gate; varsa hataları düzelt, sonra bağımsız diagnostic artifact API origin/digest entegrasyonunu uçtan uca test et. ZIP ve outcome gerçek artifact kökeni olmadan kabul verme.
- Tam kabul 0/92, 0/26, 0/22; korunan yayın/EPG/YEDEKLER/YENİLER/FAVORİLER/logolar/arşivlere yazma, eski repo ve PR #71 merge yasağı geçerli. Eşzamanlı sohbetlerde yeni main HEAD kontrolü zorunlu.

## 22 Ekim 2026 — Paralel sohbet çakışma denetimi ve tanı API regresyonu
- main HEAD okunarak çalışıldı; önceki diagnostic ZIP/API doğrulayıcıları ve testleri tekrar yazılmadı. Ayrı tests/test_failure_diagnostic_api_fail_closed.py eklendi: commit 2aa79162627663cb8b11c7efbaba2765a47dfc34. Dört negatif senaryo: API run_attempt, artifact workflow_run.id, artifact workflow_run.head_sha ve artifact digest uyuşmazlığı ValueError ile reddedilmeli.
- Bu yeni test henüz ÇALIŞTIRILMADI; mevcut 632 test kanıtına eklenemez. GitHub Actions izinsiz tetiklenmedi. Başka sohbet main üzerinde eşzamanlı çalışıyor: her sonraki işlem öncesi HEAD ve dosya SHA yeniden okunmalı, var olan çalışma ezilmemeli. Kabul 0/92, 0/26, 0/22.


## 22 Ekim 2026 — Diagnostic outcome strictness regresyonu
- Yeni test commit 71ba4aeb3e79456855ac8392b09ee9fe3740f0d3; tests/test_diagnostic_outcome_strictness.py içinde duplicate JSON key, timeout conclusion/measurement mismatch ve yanlış consumer identity için üç fail-closed senaryo eklendi. Mevcut diagnostic ZIP/API testleri tekrar yazılmadı.
- Yerel GitHub git ls-remote hâlâ DNS 'Could not resolve host: github.com' verdi. Yeni testler ve tam offline_gate ÇALIŞTIRILMADI; 632 önceki test bu commit'i kapsamaz. GitHub Actions/üretim tetiklenmedi.
- Sonraki iş: erişilebilir checkout üzerinde python -m unittest tests.test_diagnostic_outcome_strictness -v ve python -m madsc.offline_gate; başarısızlıkları düzelt, gerçek diagnostic artifact API/byte doğrulamasını bağımsız execution kanıtıyla sınamaya devam et. Kabul 0/92, 0/26, 0/22; tüm korumalar geçerli. Paralel sohbet için her yazmadan önce main/dosya SHA yeniden okunmalı.

## 22 Ekim 2026 — Paralel çalışma: diagnostic API run-state regresyonu
- Kendi tests/test_failure_diagnostic_api_fail_closed.py dosyasına dört yeni fail-closed API negatif senaryo eklendi: e34b9481c888173f7b943c4ff05f959040bfdef5. total_count uyuşmazlığı, run.status in_progress, run.conclusion success ve run.repository.full_name uyuşmazlığı. Önceki sekizle toplam 12 negatif alt senaryo tanımlı.
- Testler henüz çalıştırılmadı; `git ls-remote` GitHub DNS çözümleme hatası verdi. 632 test önceki kaynak sürümüne aittir. Başka sohbetin güncel kodu yeniden yazılmadı; sonraki turda HEAD ve dosya SHA yeniden doğrulanmalı. GitHub Actions tetiklenmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Birikmiş diagnostic ve 92-kapsam kodunun gerçek toplu doğrulaması
- Son kod/test commit SHA: bd641a057d9ff47a2daeeddbef7eab742779db93; taban da6700fc31b8378a19363cba7477b6a49f2a248f. Önceki turlarda checkout/DNS engeli nedeniyle çalıştırılmamış diagnostic ZIP, API origin ve pinned 92-scope sertleştirmeleri güncel `main` checkout'unda birlikte sınandı.
- İlk odak çalıştırmada 48 testten event alt senaryosu başarısız oldu: fixture `workflow_dispatch` değerini zaten aynı olan beyan edilmiş event üzerine yazıyordu. Gerçek uyuşmazlık üretmesi için `schedule` kullanıldı; doğrulayıcı değiştirilmedi. Aynı odak kümesi finalde 48/48 geçti.
- Nihai `python -m madsc.offline_gate`: 658/658 test ve beş izole K1–K5 kapısı success; 92+7 kaynak, 10 yardımcı komut ve 22 görev envanteri geçti. `git diff --check` temiz. Kanıt `docs/OFFLINE_REGRESSION_KANIT_658_2026-10-22.json`.
- Bu testler gerçek Actions koşusu değildir. Yeni/current-code diagnostic artifact yok; legacy 92 tarafında aynı-input v1 artifact ve bağımsız replacement execution çifti yok. Kabul 0/92, 0/26, 0/22 kaldı. Actions/live probe/production write/eski repo yazısı yapılmadı.
- Statik incelemede yedi eski workflow'un `CALISANLAR.m3u` yazıp tüm M3U/M3U8'i reddeden protected-write gate'i çağırdığı çelişki doğrulandı. K1 gevşetilmedi; korunan listeye yazılmadı. Bu yollar üretim eşdeğeri sayılamaz ve kullanıcı onayı + ayrı yayın tasarımı olmadan düzeltilemez.
- Sıradaki güvenli yerel iş: gerçek dış kanıt gerektirmeyen 92 kaynak davranış eşleme kayıtlarını, pinned source commit/blob kimliklerinden başlayarak aynı-input pair hazırlık raporunda fail-closed eksik kanıt durumlarına bağla. Gerçek run/artifact oluşmadan kabul üretme; korunan playlist yayın tasarımını yetkisiz uygulama.

## 22 Ekim 2026 — Yanlış depodaki düzeltmelerin Madsc55-Tv karşılıklarına aktarımı
- Kullanıcının düzeltmesi üzerine tek hedef Madsc55/Madsc55-Tv/main olarak yeniden doğrulandı. Önceki sohbette eski depoya yapılan commit/testler yeni sistemin ilerlemesi değildi; bu kayıt o hatayı gizlemez. Bu aktarım turunda eski depoya yazılmadı, eski workflowlar kopyalanmadı, hiçbir Actions tetiklenmedi.
- Başlangıç bd641a057d9ff47a2daeeddbef7eab742779db93 üzerinde mevcut 658 test ve beş izole kapı geçti. Diğer sohbetin yalnız notları değiştiren 644ec08a4d3ef28414b3014813b0652164b68c8d commit'i korundu; aktarım bu güncel tabana uygulandı.
- K1: FAVORILER/favorites/HEPSI metadata kök adları ortak audit/enforcement kapısına eklendi; src manifest kapısı aynı politikayı kullanır. allowed_root korunan üst dizin adını gizleyemez. Yeni dosya yazılmadan ret ve eski bayt korunumu sınandı. Nested EPG/logo/arşiv koruması zaten mevcuttu, tekrar kurulmadı; yeni regresyonlarla doğrulandı. K1 izole kapısı metadata/logo reddini de gerçekten çağırır.
- K5: mevcut retry_decision politikasına assess_failure_history bağlandı. En çok 10 sağlanan sayfa, gerçek integer kimlik/total, tekil kayıt, mevcut koşu/dal/tarih ve eski koşu sırası kontrol edilir. Yetersiz geçmiş sıfır hata sayılmaz; ikinci sayfadaki hatalar durdurur, sonraki koşular eski rerun'a yüklenmez. Yeni sistemin varsayılan üç hata eşiği korunur. Otomatik API fetch/scheduler kurulmadı; bu offline değerlendirici kimlik doğrulanmış production geçmişi kanıtı değildir. K5 izole kapısı 100 aktif koşu arkasındaki üç başarısızlığı iki sayfadan gerçekten değerlendirir.
- Mevcut legacy_99_bulk_audit, SHA'sı doğrulanmış her kaynak satırına job/step/line/if/reusable/gate-order bağlamı ekler. madsc/legacy_workflow_safety saf/offline işlevdir. Başka job'daki/sonraki/continue-on-error gate önceki yazmaya yetki sayılmaz; echo/test/GET metni ayrılır. K5 kapısına çapraz-job yanlış kabul regresyonu bağlandı. Gerçek 99 kaynak ağdan yeniden çalıştırılmadı; eski 24/18/6 sayıları yeni pinned kaynak sonucu diye kullanılmadı.
- Git diff/push yazıcısı yeni runtime'da olmadığı için eski Git referansı çözüm kodu ve eski Actions testleri bağımsız kopya olarak eklenmedi; uygulanabilir davranış mevcut yeni kapılara uyarlandı. Eski başarı artifact'leri yeni kanıt gibi gösterilmedi. Ayrıntılı kaynak-commit/yeni-dosya eşlemesi ve SHA256: docs/TRANSFER_K1_K5_KANIT_2026-10-22.json.
- Nihai toplu offline doğrulama: 670 test + beş izole K1–K5 kapısı başarılı; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. Git diff --check temiz. Başarısız test yok. Bu kod, test ve kanıt bu kaydın bulunduğu tek [skip ci] commitinde saklanır; commit SHA dosya geçmişinden ve son kullanıcı raporundan doğrulanabilir.
- Tam kabul 0/92, 0/26, 0/22 değişmedi. Workflow/cron/izinler, canlı kanal/EPG/yedek/yeni/favori/logo/arşiv dosyaları değiştirilmedi. Sonraki iş diğer sohbetin pinned aynı-input pair hazırlık işini ezmeden sürdürülmeli; history API kökeni ve gerçek eski/yeni bağımsız run/artifact kanıtı hâlâ eksik. Bu paket tüm eski düzeltmelerin aynen kopyalandığı veya üretime kurulduğu iddiası değildir.

## 22 Ekim 2026 — Sohbet devri: diagnostic outcome tür koruması
- Kanonik hedef yalnız `Madsc55/Madsc55-Tv` main; `Madsc55/madsc-tv` eski kaynak ve salt okunur. Paralel sohbetin K1–K5 ilerlemesini veya korunan üretim içeriklerini ezme. Her yeni işlemde HEAD ve blob SHA kontrol et.
- `madsc/legacy_pair_artifact.py` outcome `exit_code` için `type(...) is int`, `timed_out` için `type(...) is bool` kesin kontrolü eklendi: commit `ed345b90af6db0d7175286db1227608463d363d5`. JSON bool/int eşitlik karışıklığını reddeder.
- `tests/test_diagnostic_outcome_type_confusion.py` iki regresyon testi eklendi: commit `28b1f0852a8e0c3f8e2e1c92580b0d5b3a598b4e`. Bunlar henüz gerçek depo modülleriyle çalıştırılmadı.
- Bu sohbet içinde aynı kontrol mantığının izole kopyası üzerinde 4 unittest (geçerli failure, bool exit_code, integer timed_out, float exit_code) çalıştırıldı: 4/4 geçti. Bu sonuç depo testi veya full offline_gate kanıtı değildir.
- Bu devirden hemen önce HEAD `0bd40de657410a309949626f4f4dfcd61bfd3222` görüldü; diğer sohbet yeni K1–K5 transfer paketi ve 670 test + 5 offline kapı sonucunu not etmiş. Bu sonuç yalnız notta belirtilen kendi kaynak sürümüne aittir, bizim iki yeni commitin tamamını kapsadığı ayrıca kontrol edilmeli.
- Sonraki iş: güncel HEAD'de `python -m unittest tests.test_diagnostic_outcome_type_confusion tests.test_diagnostic_outcome_strictness tests.test_failure_diagnostic_api_fail_closed -v` ve `python -m madsc.offline_gate` çalıştır; gerçek sonuçları kaydet. Bağımsız legacy/replacement run-artifact aynı input kabul kanıtlarını üretmeden kabul artırma. Tam kabul 0/92, 0/26, 0/22.
- Actions dispatch/rerun, canlı probing, cihaz testi, merge ve PR #71 merge izinsiz yapılmaz. Korunan yayın/EPG/YEDEKLER/YENİLER/FAVORİLER/logo/arşivlere dokunma. Commitlerde [skip ci] kullan.

## 22 Ekim 2026 — 92 davranış için kaynak kimlikli pair hazırlığı
- Tek hedef Madsc55/Madsc55-Tv/main. a37086e tabanında başlayan paket, diğer sohbetin 28b1f08 ve 27ea4c81dcb8fee19ae28489c6dcf3e4100a3562 commitlerindeki diagnostic düzeltme/test/notları korunarak güncel main üzerine uygulandı. Önceki yayın denemesi main ilerlediğinde dalı değiştirmedi; yeni HEAD üzerine kaydedildi.
- Mevcut compare_provenance_bound_batch ve legacy_parity_cli genişletildi; yeni workflow/yazıcı/CLI yok. 92 satırda pinned eski repo/dal/commit/tree/workflow/blob/boyut, gözden geçirilecek beş merkezi replacement seçeneği, varsa aynı-input SHA256 ve altı bağımsız eksik kanıt alanı var. Yedi kapsam dışı workflow eklenmez; eksik çiftin input hash'i null kalır. Gerçek run/artifact uydurulmaz.
- 99 kaynak yol/blob/boyut digest'i sıralamadan bağımsız sabitlendi; pinned tree ve scope-script SHA da kontrol edilir. Biçimi geçerli fakat değiştirilmiş blob/boyut/yol/tree/script kimliği karşılaştırmadan önce reddedilir. Bu offline kaynak katalog bağıdır; API kökeni veya canlı yürütme doğrulaması değildir.
- Mevcut CLI ile docs/PARITY_PAIR_PREPARATION_2026-10-22.json üretildi: 92 kaynak kimliği bağlı hazırlık satırı, 92 eksik gerçek pair, sıfır kabul. Eşleşen fixture metadata'sında dahi API kökeni/artifact baytları/yan etki/gözden geçirme açık kalır. K5 izole kapısı bu 92-satır sözleşmesini gerçekten çağırır.
- İlk toplu denemede yeni test dosyasındaki kullanılmayan yanlış sınıf import'u 1 keşif hatası verdi (671 keşif kaydı); import kaldırıldı. Sonraki 675 ve 677 yerel testler geçti. Main yeniden ilerlediği için son dört eşzamanlı test de korunup nihai toplu python -m madsc.offline_gate çalıştırıldı: **679 test + beş izole K1–K5 kapısı success**; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/PARITY_PAIR_PREPARATION_KANIT_2026-10-22.json; kaynak ve üretilen rapor SHA256'ları kayıtlı.
- Kod/test/rapor/notlar aynı [skip ci] commitinde; kendi SHA'sı dosya geçmişindedir. Actions/rerun/live probing, üretim dosyası, workflow/cron/izin, eski repo yazısı veya merge yok. Kabul **0/92, 0/26, 0/22** korunur.
- Sonraki iş 92 satırın replacement davranış eşlemelerini mevcut uygulanmış komut ve input/output role sözleşmelerine bağlamak; beş seçenekten otomatik onaylı eşleme türetmemek. Gerçek bağımsız eski/yeni aynı-input run/artifact ve yan etki kanıtları dış bağımlılık olarak açık.

## 22 Ekim 2026 — 92 hazırlık kaydı yeni workflow sözleşmelerine bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban **52117ac42f268ade64e48490edac8c6a0e624657**. compare_provenance_bound_batch mevcut replacement_workflow_root argümanı verilince güncel beş YAML'ı mevcut audit_parity_workflow_readiness ile okuyup karşılaştırma raporuna replacement_contract_catalog ekler. Kaynak dizin verilmezse checked=false ve catalog=null; eski çağrı uyumluluğu korunur.
- 92 satırdaki kaynak-kimlikli pair hazırlığı bu kataloğa açık checked referansıyla bağlanır. Üç izole tüketici/girdi/çıktı rolü (K1 guard, K4 restore, K5 içindeki K2 artifact üreticisi) ve iki harici/canlı input engeli (K2/K3) gerçek mevcut source hashleriyle raporlanır. Bu, 92 davranışın seçilmiş/onaylanmış yeni eşlemesi değildir: replacement_mapping_review_required her satırda true kalır. K1/K4/K5 sözleşmesini sırf ad eşleşmesiyle tüm eski işlere uygulama.
- K5 izole kapısı aynı rapor zincirini beş kaynak üzerinden çağırır. Kaynak dosya değişirse fresh blob/hash ve eksik rol durumu yenilenir; cached readiness dosyası onay olarak kullanılmaz. Eksik kaynak mevcut CLI output yazmadan reddedilir. Yeni workflow veya yazıcı eklenmedi; üretim kapıları gevşetilmedi.
- Dört yeni offline regresyon: argümansız kontrol yapıldı iddiasının reddi; beş gerçek source/3 izole+2 harici contract; değişen source blob ve kaybolan binding; eksik source halinde çıktı olmaması. Toplu python -m madsc.offline_gate **683 test ve beş izole K1–K5 success**; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. Başarısız test yok; git diff --check temiz.
- Mevcut legacy_parity_cli.run ile ağsız/boş gerçek-pair girdisi üzerinde rapor üretildi. docs/PAIR_REPLACEMENT_CONTRACT_KANIT_2026-10-22.json beş güncel sözleşmeyi, 92 checked referansı, CLI rapor SHA256'sını ve test edilen source hashlerini içerir. Gerçek execution/artifact uydurulmadı; 92 pair hâlâ eksik.
- Kod/test/kanıt/notlar aynı [skip ci] commitinde; kendi SHA'sı Git geçmişindedir. Actions/rerun/live probe, korunan kanal/EPG/yedek/favori/logo/arşiv, workflow/cron/izin, eski repo veya merge işlemi yok. Kabul 0/92, 0/26, 0/22 korunur.
- Sonraki somut iş: bağımsız pair verisi geldiğinde seçilen replacement tüketici ve input/output role sözleşmesinin eski davranışa gerçekten karşılık geldiğini kaynak-bağlı mapping kaydıyla doğrulamak; metadata match'i davranışsal kabul saymamak. K2/K3 ortak harici input, legacy v1 manifest/artifact ve bağımsız origin/bayt/yan etki kanıtları dış bağımlılık olarak açık.

## 22 Ekim 2026 — Seçilen davranış eşlemesi mevcut karşılaştırıcıya bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main. Diğer sohbetin kaynak eşleme inceleyicisi ve sekiz testi korunarak 65109d7 tabanına uygulandı. Mevcut batch/CLI isteğe bağlı behavior_mappings alır; pinned legacy blob, güncel replacement blob, tüketici komutu ve input/output rolü birebir doğrulanır. Eksik kaynak, harici-input sözleşmesi, yanlış hedef ve ek approved alanı reddedilir; hatalı CLI girdisinde rapor yazılmaz.
- Bildirim gerçek eşleme incelemesi değildir. replacement_mapping_review_required=true kalır; gerçek incelenmiş eşleme ve doğrulanmış legacy pair sayısı sıfırdır. Fixture seçimi gerçek 92 davranışa otomatik atanmadı. Bağımsız yürütme/API/artifact baytları/yan etki kanıtı hâlâ gerekir.
- Yedi yeni regresyonla birleşik python -m madsc.offline_gate: **698 test + beş izole K1–K5 kapısı başarılı**; 92+7 kaynak, 10 yardımcı komut ve 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/BEHAVIOR_MAPPING_BINDING_KANIT_2026-10-22.json. Kod/test/kanıt/notlar aynı [skip ci] commitinde; SHA dosya geçmişindedir.
- Actions, canlı test, üretim dosyası, eski repo, workflow/cron/izin veya PR değişikliği yok. Kabul 0/92, 0/26, 0/22 korunur. Sonraki iş bağımsız kaynak gerekçeli eşleme incelemesini mevcut pair zincirine taşımak; aynı-input gerçek yürütme kanıtı eksikliğini kabul saymamak.

## 22 Ekim 2026 — Kullanıcının eski depodaki test ekranlarının yeni sistem karşılığı
- Kullanıcının paylaştığı ekranlardaki ebf7e25, d0ec63a, 28fe155, 1b4474d, ebb3550, 4bc7328 ve 17e9167 değişiklikleri mevcut aktarım kaydı ve yeni kod/testlerle karşılaştırıldı. Tek hedef Madsc55/Madsc55-Tv/main; eski depo değiştirilmedi. Eski kırmızı/yeşil run sonuçları yeni sisteme kanıt sayılmadı.
- Favori metadata/iç içe korunan yol K1 kapıları, K5 sayfalı eksik geçmiş reddi/current-run/rerun ayrımı ve job/step kaynak kapsamı mevcut yeni uygulamada doğrulandı. Bağımsız kategori kanıtının explicit true gereksinimi mevcut maintenance testiyle doğrulandı. Eski escaped-newline testi farklı workflow metnine körlemesine kopyalanmadı. Yeni runtime'da Git diff/push yayıncısı olmadığı için baseline seçenek enjeksiyonu düzeltmesi uygulanabilir bir üretim yolu olarak gösterilmedi.
- 0962bc188f712948a03971d012a7d7ad3b381742 üzerinde güncel yerel doğrulama: **698 test + beş izole K1–K5 kapısı başarılı**. Ayrıntı, kaynak SHA256, K etki matrisi ve açık bağımlılıklar docs/SCREENSHOT_TEST_TRANSFER_AUDIT_2026-10-22.json içinde. Bu paket mevcut aktarımı ekrana göre doğrular; yeni işlev/test sayısı artışı değildir.
- Actions başlatılmadı; üretim/korunan veri/eski repo/workflow değişmedi. Authenticated hata geçmişinin üretimde zorunlu kılındığı veya ekranlardaki eski kırmızı Actions'ın düzeldiği iddia edilmez. Kabul 0/92, 0/26, 0/22. Sonraki iş yeni sistemde bağımsız gerçek yürütme ve kaynak gerekçeli davranış eşlemesi kanıtını tamamlamaktır.

## 22 Ekim 2026 — Gerekçeli eşleme incelemesi pair zincirine bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban bf56ac1826d9e0d43a9e9c218e3865865b580b8d. Diğer sohbetin mevcut review_replacement_mappings işlevi lazy import ile mevcut provenance batch/CLI zincirinde kullanılır. İsteğe bağlı mapping_review_rows kaynak blob, seçilen replacement ve input/output rolü açısından behavior_mappings ile birebir bağlanır; kopuk veya kaynaksız inceleme rapor yazılmadan reddedilir. Yeni CLI/workflow/yazıcı yok.
- İnceleme gerekçesi ilgili pair_preparation satırına taşınır; supplied aday sayısı ayrı raporlanır. Bunlar bağımsız onay değildir: review_required=true, independently_reviewed=0, behavioral acceptance=0 kalır. Fixture eşlemesi gerçek legacy davranış incelemesi gibi kaydedilmedi.
- Dört yeni bütünleşik regresyon: gerekçenin aynı satıra taşınması, yanlış kaynak/rol/ek approved/duplicate/kaynaksız bildirim reddi, boş ve hiç verilmemiş inceleme ayrımı, mevcut CLI'nin hatalı incelemede çıktı yazmaması. python -m madsc.offline_gate: **702 test + beş izole K1–K5 kapısı başarılı**; 92+7 kaynak/10 yardımcı komut/22 görev envanteri geçti. git diff --check temiz. Kanıt docs/MAPPING_REVIEW_CHAIN_KANIT_2026-10-22.json.
- K1 çıktı koruması değişmedi; K2/K3 canlı input ve K4 yedek/restore yolu değişmedi; K5 karşılaştırma raporu genişledi. Actions, production, eski repo, workflow/cron/izin, PR değişmedi. Kod/test/kanıt/notlar aynı [skip ci] commitinde, SHA geçmiştedir. Kabul 0/92, 0/26, 0/22. Gerçek kaynak gerekçeli davranış incelemesi ve bağımsız aynı-input yürütme/API/artifact/yan etki kanıtları hâlâ açık; yeni sahte metadata ekleyerek kabul üretme.

## 22 Ekim 2026 — K5 sayfalı hata geçmişi sıra doğrulaması
- Tek hedef Madsc55/Madsc55-Tv/main, taban 37e52ab3647e9198e4ed2d207f47aaf81b87f59d. Eksik ve sırası bozuk supplied history eski success sınırını kullanarak RETRY_LATER verebiliyordu. Mevcut assess_failure_history artık filtrelemeden önce bütün aktif/tamamlanmış satırların timestamp/id sırasını sayfa içinde ve sayfalar arasında azalan olarak doğrular; bozuk aktif timestamp de reddedilir. Varsayılan üç hata eşiği ve sıralı prefix success sınırı politikası değişmedi.
- Beş regresyonun dördü düzeltme öncesi beklenen ValueError oluşmadığı için başarısızdı. Düzeltme sonrası toplu python -m madsc.offline_gate: **707 test + beş izole K1–K5 kapısı başarılı**; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/FAILURE_HISTORY_ORDER_KANIT_2026-10-22.json.
- K5 retry kararı sıkılaştırıldı; K1 çıktı kapısı, K2/K3 keşif/kanal ve K4 yedek yolları değişmedi, beş izole kapı birlikte geçti. Actions/production/eski repo/workflow/cron/izin/PR değişikliği yok. Kod/test/kanıt/notlar aynı [skip ci] commitinde; SHA geçmiştedir. Sıra doğrulaması tek başına API kökenini veya atlanmış satır bulunmadığını kanıtlamaz; authenticated history ve gerçek bağımsız yürütme kanıtı hâlâ eksiktir. Kabul 0/92, 0/26, 0/22 korunur.

## 22 Ekim 2026 — replacement katalog bütünlüğü (MADSC55-TV)
- Yalnızca `Madsc55/Madsc55-Tv/main` değiştirildi; eski `madsc-tv` salt okunur kaynak olarak kaldı.
- `madsc/legacy_replacement_mapping_review.py` eksik veya tekrarlı K1–K5 kaynak kataloğunu fail-closed reddediyor; eşleme ancak beş merkezi workflow kaydı eksiksiz ve tekilse inceleniyor.
- `tests/test_legacy_replacement_mapping_review.py` fixture'ı beş merkezi workflow'u içeriyor; eksik/tekrarlı kayıt için iki regresyon testi eklendi.
- Commitler `cd2e667a63589a5f02e3d9d996fd6571b8a6772c`, `4943508c668a6e151070243e0596f1c00cd1584e`; ikisi de `[skip ci]`.
- Bu turda testler çalıştırılmadı; Actions `#482/#483` gerçek run ID/logları henüz bulunamadı. GitHub run numarası API run ID değildir. Üretim/EPG/playlist/yedek/favori/workflow/cron değiştirilmedi; gerçek kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — mapping dosya bağları fail-closed
- `madsc/legacy_replacement_mapping_review.py` replacement `declared_file_binding` içindeki `input_path`, `output_label`, `output_path` değerlerini dolu string olarak doğrular; liste/boş değer kontrollü ValueError ile reddedilir.
- `tests/test_legacy_replacement_mapping_review.py` iki negatif regresyon senaryosu eklendi.
- Yeni `Madsc55/Madsc55-Tv/main` commitleri: `91e625b1fe1e0dd5c8a8c9e5aa14f326deb9ccc8`, `483c75c9374e258402f3ae28485d3ad01c5465e8` (`[skip ci]`). Testler bu turda çalıştırılmadı; Actions #482/#483 logları henüz doğrulanmadı. Üretim dosyaları, workflow'lar, eski repo değişmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — kontrollü süreç sözleşmesi mapping kapısı
- `madsc/legacy_replacement_mapping_review.py` statik adaylık için `controlled_process_contract_complete` alanını zorunlu kıldı; eksik alan fail-closed, false alan `mapping_contract_blocked`. Kaynak: `madsc/parity_workflow_readiness.py` güncel sözleşme satırları.
- `tests/test_legacy_replacement_mapping_review.py` beşli fixture'lara bu alanı ekledi, iki negatif regresyon testi oluşturuldu.
- Commitler `11e1f12a50ce91c412a2fb8d13db417f7753608c` ve `768150c2ed7d3af99f419001caa1d7d575d0c9c3` (`[skip ci]`). Bu turda CI ve offline test çalıştırılmadı. Üretim, Actions, eski depo değiştirilmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — K2/K3 harici kaynak mapping blokajı
- `madsc/legacy_replacement_mapping_review.py` K2 ve K3 için statik kaynak sözleşmesi alanları true olsa bile eşleme adayını `mapping_contract_blocked` tutar. Bu aşamaların harici/canlı girdileri bağımsız karşılaştırma olmadan kabul edilemez.
- `tests/test_legacy_replacement_mapping_review.py` K2 ve K3 için yanlışlıkla tüm flaglerin true olduğu negatif senaryoları ekledi.
- Yeni sistem commitleri `6e01ae808056e7ebac50d9ab95666bbe1d603fb3`, `2c6d680bbc39ee3e9d0467228670f8ddcf3c0f75` (`[skip ci]`). Bu turda testler yürütülmedi; Actions #482/#483 logları elde edilmedi. Üretim/EPG/yedek/favori/workflow/cron/legacy repo değiştirilmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Beşli sistem toplu rapor üretimi ve K5 uçtan uca yerel kapısı
- Yalnız Madsc55/Madsc55-Tv/main; taban 2ea58e800156e3c99eb63f882f838045fc0714eb. Güncel diğer sohbet kodu korundu. Önceki yerel ortam kaybolduğu için yeni checkout alındı; geçmiş 707 testi güncel kodun kanıtı sayılmadı. Birleşik kaynakta ilk toplu test: 754 test, 1 failure/4 error. Eksik EXT M3U başlıklı üç test girdisi ve literal backslash-n içeren iki fixture düzeltildi. Preview testi mevcut büyük harfli ad sözleşmesiyle, virgüllü id/grup korunumu da doğrulanarak güncellendi. Üretim parser'ları gevşetilmedi.
- Mevcut offline_five_gate içine assess_report_roundtrip eklendi: gerçek core.run beş kategorinin raporlarını ayrı geçici artifact dizinlerine yazar; gerçek batch_acceptance.collect bunları K5 olarak okur; bütün dosya SHA256'ları tüketim öncesi/sonrası aynı olmalıdır. Mevcut offline_gate bu aşamayı artık zorunlu kılar; eksik/bozuk çıktı veya exception exit_code=5 ile yeşil unit test sonucunu engeller. Yeni workflow/zamanlayıcı/üretim yazıcısı yok.
- K1 korumalı rapor yazısı, K2 keşif ve geçmiş fixture'ı, K3 teknik/IBO/EPG fixture'ı, K4 izole restore ve K5 toplu tüketim aynı pakette yürütüldü. Üç yeni regresyon: gerçek beş rapor tüketimi ve byte korunumu; eksik üretici çıktısının reddi; başarılı unit testin bozuk roundtrip'i örtememesi. Geliştirme sırasında eksik dosya testinde yanlış exception beklentisi bir hata verdi; FileNotFoundError beklentisiyle düzeltildi.
- Nihai python -m madsc.offline_gate **757 test, beş izole K1–K5 kapısı, beş gerçek yerel rapor/K5 roundtrip ve 92+7/10 komut/22 görev envanteri başarılı**. git diff --check temiz. Kaynak hashleri, rapor hashleri, bütün görevlerin açık kanıt listesi ve yardımcı sözleşme farkları docs/FIVE_SYSTEM_BULK_VALIDATION_2026-10-22.json içinde.
- Tam bitmiş değildir: kurulumda 16 YAML vardır (beş ana + ekler); on yardımcı komut ana sisteme bağlıdır fakat 11 statik sözleşme farkı açık. 125 statik yazıcı çağrı adayı tümü runtime denetlendi sayılmaz. Defter 0 completed/7 in_progress/15 pending; kabul 0/92, 0/26, 0/22. Eski bağımsız aynı-input execution/artifact, canlı/zaman aralıklı K3, kullanıcının IBO cihaz testi, harici yedek/restore ve gerçek uçtan uca güvenlik kanıtları eksik. Gerçek kabul olmadan eski otomasyonları kapatma veya defteri completed yapma.
- Actions/merge/PR71/canlı probing/korunan IPTV-EPG-yedek-favori-logo-arşiv ve eski repo yazısı yapılmadı. Bu [skip ci] paketinin SHA'sı Git geçmişindedir. Sonraki iş rapordaki bağımsız dış kanıt engellerini ve 11 kaynak sözleşme farkını ana beşli sistem içinde çözmek; küçük fixture testlerini gerçek 92 davranış tamamlandı gibi sunmamak.

- Yayın sırasında diğer sohbetin yalnız docs/K1_K5_KURULUM_DURUMU_2026-10-22.md ekleyen a39cdfa commit'i geldi; içerik okundu ve korundu. Test edilen Python/test/workflow kaynakları değişmedi; dal eski HEAD üzerine zorlanmadı.


## 22 Ekim 2026 — Bu sohbetin son devri
Kullanıcı tüm ilerlemenin kaydedilip yeni sohbete geçilmesini istedi. Ayrıntılı toplu devir: SOHBET_DEVIR_2026-10-22_SON.md. Yanlış eski repo çalışması ve yeni sisteme aktarım, bütün ilgili commit/kanıt dosyaları, başarısız testler ve düzeltmeleri, 757 test+5 kapı+5 dosya/K5 doğrulaması, açık 11 sözleşme farkı ve 92/26/22 bağımsız kabul eksikleri kaydedildi. Bu devir hazırlanırken HEAD 3c228e7340b090ae4edf49d3d7b49382a4ef6d69; bu HEAD'in eklediği five_stage_installation modülü ve iki testi okundu ama çalıştırılmadı. İlk iş güncel HEAD'de bunları ve tam offline_gate'i doğrulamak. 757 testi sonraki kaynak sürümüne otomatik mal etme. Korunan veriler/eski repo/PR71/izinsiz Actions ve canlı test sınırları değişmedi; IBO testi kullanıcıda. Bu commit yalnız dokümandır, yeni test sonucu değildir.


## Eşzamanlı diğer devirle mutabakat
Devir yazılırken aeee8354c1e55f398c1f194650475d15769688bf yalnız YENI_SOHBET_DEVIR_2026-10-22.md ekledi; metin okundu ve korundu. O belgedeki 707 test bilgisi tarihsel kaldı: 1b30eee paketi 757 test+5 kapı+5 rapor/K5 ile doğrulandı, daha sonraki 3c228e7 dosyaları henüz sınanmadı. Diğer belgenin kullanıcı ekranından aktardığı K4 EPG/logo ve K5 arşiv/bakım hedefleri ile repo teknik K4 yedek/K5 bakım adlandırması arasındaki fark yeni sohbette açık görev eşlemesiyle uzlaştırılmalı; repo isimleri varsayımla değiştirilmemeli. Bu devir kaydı bütün önceki notları tamamlar.

## 22 Ekim 2026 — kurulum kapısı ve zamanlama regresyonu doğrulaması
- Son kod/test/kanıt commit SHA: `e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991`; taban `554ec5f07a10dcf81041c1cc18a2081a04dc9e4c`. Eşzamanlı gelen `4fa9cf7` ve `554ec5f` kurulum-envanteri fail-closed testini ekledi/düzeltti; eski HEAD üzerine yazılmadı.
- Güncel kaynakta kurulum envanteri genel offline kapının zorunlu parçası olarak doğrulandı. Odaklı kurulum/offline/round-trip seti 14/14 geçti. Nihai `python -m madsc.offline_gate` sonucu 760/760 test, beş izole K1–K5 kapısı, kurulum envanteri, beş gerçek yerel rapor/K5 byte-koruyan round-trip ve 92+7/10 komut/22 görev envanteri başarılıdır.
- İlk tam koşu host yükü altında FIFO snapshot 2 saniye ve K1 workflow simülasyonu 10 saniye sınırında iki timeout verdi; ikisi izole tekrarında geçti. İkinci tam koşu, öldürülen alt süreç için PID numarasının yeniden kullanılmasını ayırt etmeyen `/proc` kontrolünde 1 saniyelik sınırı yaklaşık 10 ms aştı. Sadece bekleme süresini artıran ilk deneme yeterli olmadı.
- Nihai test düzeltmesi süreç kimliğini Linux `/proc/<pid>/stat` starttime alanına bağladı; yeniden kullanılan PID artık eski alt süreç sanılmıyor. Gerçek aynı süreç canlıysa test hâlâ kırmızı kalır. FIFO ve workflow simülasyonu test-harness zamanlama üst sınırları 5 ve 30 saniyeye çıkarıldı; üretim timeout/kill/fail-closed davranışı değiştirilmedi. Üç süreç-kapatma tekrarı ve iki ilgili sınır testi 5/5 geçti.
- Kanıt: `docs/FIVE_STAGE_INSTALLATION_GATE_KANIT_2026-10-22.json`. `git diff --check` temiz. GitHub Actions, canlı stream probing, cihaz testi, üretim yazma, eski depo yazısı, merge veya PR #71 işlemi yapılmadı; korunan veri değişmedi.
- Açık işler/engeller: gerçek 92 aynı-input çifti için bağımsız legacy ve replacement execution/artifact kökeni hâlâ yok; K2/K3 canlı/harici kaynaklar, IBO kullanıcı cihaz sonucu ve K4 bağımsız harici restore kanıtı eksik. Tam kabuller 0/92, 0/26, 0/22; fixture sonuçları bu sayaçları artırmaz.
- Sıradaki somut adım: `five_stage_installation` raporundaki 11 statik sözleşme farkını kaynak gerekçeleriyle gözden geçir; güvenle yerel çözülebilenleri beş ana workflow sözleşmesine taşı. Gerçek aynı-input/bağımsız run-artifact bulunmadan 92 davranış kabulü verme ve mevcut kanıt zincirini sahte metadata ile doldurma.


## 22 Ekim 2026 — Güncel kurulum ve operasyon sözleşmeleri topluca doğrulandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban 554ec5f07a10dcf81041c1cc18a2081a04dc9e4c. Sonraki kurulum modülü/kapı değişiklikleri ilk kez bu turda gerçek yerel toplu testle kapsandı.
- İlk 760 test: 1 failure/1 error. K1 preflight alt süreç başlatması 5 saniyeyi aştı; ilgili 15 test kod gevşetilmeden 0.868 saniyede geçti. Süreç sonlandırma testi toplu koşuda tekrar başarısızdı (763 test/1 failure). Kapsayıcı getpid kimliklerinin host /proc dizininde ilgisiz sync_share.sh/sites-preview süreçlerine karşılık geldiği gerçek tanı çıktısıyla bulundu. Test artık çocukların /proc/self/stat PID ve başlangıç zamanını kullanır, iki ayrı sürecin gerçekten başladığını zorunlu doğrular; üretim süreç öldürme kodu gevşetilmedi.
- K5 25 dakika eski kaynak audit + 15 dakika not birleştirme opt-in adımlarının 10 dakika job limiti altında kalması düzeltildi: job 45, adımlar 25/15 dakika. Bu üst sınır süre tüketimi değildir; dispatch yapılmadı. Opt-in rapor upload artık failure durumunda da always() && !cancelled() ile denenir; kaynaklar/izinler/cron/korunan veri değişmedi.
- Sözleşme denetimi süreyi yalnız ilgili komutun bulunduğu job ile karşılaştırır; ilgisiz uzun job komutu maskeleyemez. Komut, süre, rapor yolu, actions izni veya failure-upload kaybı contract_gate ve mevcut offline_gate başarısını engeller. Artifact ad farkı ayrı inceleme olarak görünür; otomatik eşdeğerlik verilmez. Yeni kapı entegrasyon regresyonu dahil dört test eklendi. Önceki süre fixture'ı gerçek komutu içermediğinden düzeltildi; eksik komut süre uyumluluğu sayılmıyor.
- Nihai python -m madsc.offline_gate: 764 test, beş izole K1–K5 kapısı, kurulum envanteri, 92+7 kaynak/10 yardımcı komut/22 görev ve beş gerçek yerel raporun K5 tüketimi başarılı. git diff --check temiz. Kanıt, test edilen kaynak SHA256 ve rapor hashleri: docs/FIVE_STAGE_CONTRACT_VALIDATION_2026-10-22.json.
- 11 statik farktan iki süre farkı giderildi; dokuz artifact isim değişikliği inceleme olarak açık. Bunlar çalışma zamanı byte zinciri kabulü değildir. Davranış 0/92, runtime güvenlik 0/26, görev tam kabulü 0/22 korunur. Korunan listeler/EPG/favoriler/yedek/logo/arşiv, eski depo, PR71 ve merge işlemi yok. Actions başlatılmadı; kullanıcının ilettiği izin kotayı harcamak için gereksiz tekrar gerekçesi sayılmadı. IBO cihaz testi kullanıcıda.
- Sıradaki bağlantılı iş: dokuz yeniden adlandırılan artifact için gerçek üretici/tüketici dosya ve byte zinciri ile bağımsız aynı-input eski/yeni run/artifact kanıtını bağlamak; eksik dış kaynağı fixture ile tamamlanmış göstermemek. K2/K3 canlı ölçüm ve bağımsız geçmiş, K4 dış backup/restore, K1 26 runtime kuralı ve K5 gerçek uçtan uca kabul açık. Kod/kanıt/notlar aynı [skip ci] commitindedir; kendi SHA'sı Git geçmişindedir.

- Yayın öncesi main e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991 commitine ilerledi: FIFO/receipt test süreleri ve bağımsız 760-test kanıtı okundu/korundu. Aynı process testinin starttime ve beş saniye bekleme düzeltmesi procfs PID kimliği ve iki süreç zorunluluğu ile uzlaştırıldı. Son toplu test bu birleşik kaynaklar üzerinde yeniden çalıştırıldı.


## 22 Ekim 2026 — Dokuz artifact sözleşmesi ve ana K2 geçmiş zinciri
- Tek hedef Madsc55/Madsc55-Tv/main, taban 60031b9bc46728b7773ad8037fe398b3c1d50814. Önceki test/kanıt/notlar korundu. Paket SHA Git geçmişindedir; kod/test/kanıt/devir tek [skip ci] commitinde.
- Dokuz artifact adı farkı yalnız rapordan gizlenmedi: eski yardımcıların upload-artifact adları, dosya yolları ve ZIP common-root yerleşimi ana K2/K3/K5 işlerine opt-in upload adımları olarak eklendi. Mevcut birleşik paketler korundu; yeni workflow/job/cron açılmadı, yardımcılar kapatılmadı. Paket isimleri artık contract_gate tarafından zorunlu; silinirse toplu offline kapı başarısız olur. Statik sözleşme farkı 9→0; bu çalışma zamanı eşdeğerlik kabulü değildir.
- Somut K2 kopukluğu: tüketici madsc-k2-history-source beklerken ana K2 yalnız madsc-k2-isolated-evidence üretiyordu. Ana K2 artık kaynak çiftini eski tüketicinin beklediği ad ve iki kök ZIP üyesiyle saklar. Kaynak üretimi allow_history_source_publish, bağımsız eski kaynağı doğrulama allow_verified_history ile ayrı default-false izinlerdir; kaynak üretmek için zorunlu olarak eski manifest doğrulatılmaz. Hassas komutların açık izin regresyonu bu yeni iki ayrı flag'i zorunlu denetler.
- history_verified_pipeline/CLI açık source_workflow_path/--source-workflow seçeneği alır; yalnız eski gerçek-kaynak yardımcı workflow'u veya ana K2 kabul edilir. Varsayılan eski kaynak uyumluluğunu korur. Seçim API run.path ile birebir doğrulanır; K5 fixture CI ve keyfi workflow, doğrulamadan önce reddedilir. Manifest şeması, token zorunluluğu, repo/dal/başarı/ancestor/artifact kökeni ve bayt hash denetimleri gevşetilmedi.
- Gerçek yerel zincir testi publish_source → iki dosyalı ZIP → gerçek provenance client (API fixture) → gerçek downloader/extractor → gerçek verified pipeline → mevcut-run handoff çalıştırır; kaynak/paket baytları aynı kalır. Generic paket adı, yanlış workflow ve bozuk ZIP baytı çıktı üretmeden reddedilir; izinsiz workflow ağdan önce durur. Dokuz kaynak upload sözleşmesi birebir karşılaştırılır; source artifact adı kaldırıldığında contract gate kırmızı olur. Beş yeni test eklendi.
- Odaklı ilk set 38/38 geçti. İlk toplu 769 testte 1 failure: eski opt-in testi yayın komutunu eski doğrulama flag'inde bekliyordu. Test, yeni default-false yayın flag'ini ayrıca zorunlu kılacak biçimde güncellendi. Nihai python -m madsc.offline_gate: 769 test + beş izole K1–K5 kapısı + kurulum + beş gerçek yerel rapor/K5 + 92+7 kaynak/10 komut/22 görev envanteri başarılı; contract gaps=0; git diff --check temiz. Kanıt: docs/MAIN_ARTIFACT_CHAIN_KANIT_2026-10-22.json.
- Sınırlar: API cevapları ve geçmiş girdileri fixture'dır; gerçek Actions upload/download kökeni bu tur ölçülmedi. Statik 0 fark, eski 92 otomasyonun aynı-input bağımsız runtime kabulü değildir. Tam kabul 0/92, 0/26, 0/22 kalır. Korunan kanal/EPG/favori/logo/arşiv/yedek ve eski depo değiştirilmedi; Actions, canlı probe, merge/PR71 veya IBO cihaz işlemi yok. IBO kullanıcıdadır.
- Sıradaki gerçek engeller: bağımsız eski/yeni aynı-input yürütme ve artifact çiftleri; 26 kuralın gerçek writer yollarında runtime kanıtı; K2/K3 harici geçmiş ve zaman aralıklı medya ölçümleri; kullanıcı IBO testi; K4 bağımsız harici backup/restore. Bunlar fixture veya yeni test sayısı artırılarak tamamlanmış gösterilmeyecek. İzinli gerçek koşu için kaynak girdileri/manifest ve harici kanıt sağlanmadan genel sistem bitti denmeyecek.


## 22 Ekim 2026 — Gerçek pair toplama için API ve ZIP bayt zinciri mevcut toplu CLI'ye bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban cffae104160b69866b2da69d8b9130d99dd5649f. Önceki dokuz artifact entegrasyonu ve statik 0 fark korundu. Bu paketin SHA'sı Git geçmişindedir; tek [skip ci] kod/test/kanıt/devir kaydıdır.
- Kalan somut kopukluk giderildi: verify_provenance_pair_api ve verify_provenance_pair_artifacts daha önce ayrı çağrılardı. Mevcut github_legacy_pair_client artık verify_provenance_pair_evidence ile altı bağımsız API kaydı, iki sınırlı ZIP indirmesi, archive SHA256, strict manifest, same-input ve snapshot bağlarını tek zincirde doğrular. Yeni standalone script/workflow/zamanlayıcı yok.
- Mevcut legacy_parity_cli --verify-github-artifacts açık opt-in seçeneğiyle sağlanan pinned kapsam pair'lerini topluca doğrular; token yalnız GITHUB_TOKEN ortamından gelir. Varsayılan mod tamamen ağsız ve eski çıktı uyumludur. Boş pair veya provenance dışı snapshot bu modda reddedilir; eksik 91/92 satır başarılı kabul edilmez. Bütün supplied pair'ler doğrulanmadan çıktı yazılmaz; raporda supplied_pairs_verified ve her pair'in API/bayt kanıtı ayrı alanlardır. Davranışsal kabul 0 kalır.
- K1 rapor hedefini artık kaynak okumadan ve ağdan önce denetler; yazmadan hemen önce tekrar denetler ve exclusive open kullanır. ZIP indirmesi repo/id/token kontrolü, 30sn timeout ve 2MiB+1 bounded read ile sınırlıdır; diske ZIP/extract yazmaz. Signed storage redirect'inde GitHub Authorization başlığı silinir, HTTPS dışı redirect reddedilir.
- Yedi yeni testte gerçek mevcut CLI/karşılaştırıcı, gerçek downloader'ın yerel HTTP fixture'ı ve gerçek ZIP parser birlikte çalışır. Altı API okuması ve iki indirme doğrulanır; yanlış workflow blob'u indirmeden, bozuk ZIP çıktıdan önce, eksik token/korunan yol ağdan önce durur. HTTP redirect/token sızıntısı, büyük paket, bool id, varsayılan ağsız mod ve boş pair negatifleri denetlenir. Odaklı 16/16; nihai python -m madsc.offline_gate 776 test ve bütün offline alt kapılar başarılı. git diff --check temiz. Kanıt docs/PAIR_API_BYTE_CHAIN_KANIT_2026-10-22.json.
- Gerçek salt-okunur GitHub sorgusu da yapıldı: yeni depoda event=workflow_dispatch toplam 9, tamamı döndü; hepsi K5, 21 Ekim sürümleridir. Son 10 genel run yalnız offline unit CI'dır; bunlar güncel runtime pair kanıtı değildir. Son K5 run39686179902 ve eski discovery run39768459333 artifact metadata örnekleri okundu; yenide Ekim22 kaynak çifti yok, eski örnek main dalında olduğundan pinned legacy karşılaştırma dalına bağlanamaz. Bu örnekler aynı-input v1 manifest çifti sağlamaz. Eski deponun bütün artifact geçmişi tarandı denmez.
- Araç sınırları kaydedildi: repo-geneli artifact ve workflow-spesifik run URL'leri connector allowlist tarafından reddedildi; desteklenen run collection + artifact-by-run araçları kullanıldı. Artifact wrapper yalnız ilk sayfayı/total_count olmadan verir; tam artifact envanteri iddiası yok. Gerçek ZIP baytları bu üretim sorgusunda indirilmedi; metadata başarıları bayt doğrulaması sayılmadı. Sorgular test/Actions çalıştırmadı.
- Kullanım hazır olduğunda: python -m madsc.legacy_parity_cli --inventory docs/LEGACY_SOURCE_SCOPE.json --snapshots actual-pairs.json --output reports/parity-api-byte-proof.json --replacement-workflow-root . --verify-github-artifacts ; reports gerçek/mevcut güvenli dizin ve actual-pairs.json bağımsız gerçek origin/manifest kaydı olmalıdır. Bu komut gerçek pair bulunmadığı için bu tur üretim ağına karşı çalıştırılmadı; fixture testi gerçek kabul sayılmaz.
- Tam kabul 0/92, 0/26, 0/22. Korunan kanal/EPG/favori/yedek/logo/arşiv, eski repo, PR71, merge, Actions dispatch, canlı probing ve cihaz testi değişmedi/yapılmadı. IBO testi kullanıcıdadır. Gerçek aynı-input pair, semantik bağımsız inceleme/yan etki, K1 gerçek writer/runtime26, K2/K3 canlı/zamanlı ölçümler ve K4 harici restore açık. Sıradaki iş gerçek v1 pair kanıtını bu mevcut birleşik CLI'ye vermek; eski raporu yeni manifest gibi yeniden etiketlememek.


## 22 Ekim 2026 — GitHub istemcilerinde ortak token/yönlendirme koruması
- Kaynak tabanı 21a9146cd09feccb19084f78965652142ea82f31; bu bölümün bulunduğu commit kod/test/kanıt paketidir.
- K1 güvenlik çapraz etkisi: K2 geçmiş artifact indirmesi, GitHub köken JSON istemcisi, K5 eski kaynak denetimi ve legacy pair ZIP indirmesi aynı HTTPS yönlendirme politikasına bağlandı. API JSON başka origin'e yönlendirilirse ikinci bağlantıdan önce reddedilir. İmzalı artifact depolama adresine geçişte Authorization kaldırılır; geri yönlendirmede geri eklenmez. HTTP ve URL kullanıcı bilgisi reddedilir. Eski 99 kaynak denetimindeki sınırsız JSON okuma da 2 MiB sınırına bağlandı. K3/K4 tüketici ve veri biçimleri değişmedi, beşli entegrasyon geçti.
- Doğrulama: 19/19 odaklı test; gerçek urllib redirect dispatch sahte HTTPS yanıtlarıyla, ağsız sınandı. Nihai python -m madsc.offline_gate: 783/783 test, beş izole kapı, kurulum envanteri, beş rapor/K5 round-trip başarılı; statik sözleşme farkı 0. Kanıt: docs/GITHUB_TRANSPORT_KANIT_2026-10-22.json; değiştirilmiş kaynak SHA256 ve tam kapı sonucu içerir. Bu pakette başarısız test yok.
- Otomatik devam görevi 6ad2b2e925bc8191a91b01728e57d707 mevcut saatlik takviminde etkin doğrulandı. Eski 605 test/eski görev öncelikleri kaldırıldı; her çalışmada güncel main/devir esas alınacak, küçük paket sonrası güvenli bağlantılı işe devam edilecek. next_run_time araçta null döndü; kesin sonraki saat veya kesintisiz çalışma iddiası yok. Yinelenen görev oluşturulmadı.
- Gerçek kabul 0/92, 0/26, 0/22 olarak kaldı. Korunan üretim verisi, eski depo, PR71, merge ve cihaz testi değişmedi. Actions veya canlı probing çalıştırılmadı.
- Sıradaki somut işler: K1-03 gerçek yazıcı çağrı yollarının kalanlarını görev defteriyle eşleştir; K4 harici geri-yükleme kanıtının mevcut tüketicilere bağlanmasındaki gerçek eksikleri incele. Gerçek v1 bağımsız aynı-input pair bulunduğunda mevcut --verify-github-artifacts CLI'yi kullan; eski metadata taramasını sebep olmadan tekrarlama. Harici/cihaz kanıtı yoksa kabul artırma.


## 22 Ekim 2026 — K4 rapor hedefi işlem öncesi kontrolü
- Başlangıç main SHA: 54b76d5dd03fe41a017fd5c7b23834ef7d0a1d18. Kod commit: 7dd644cf307eed79394cd70be4a65d2fab1fe83d [skip ci].
- madsc/restore_drill.py: isolated-report-root için beklenen yol ve K1 yerel çıktı kapısı, run_drill çağrısından önce denetlenir. Normal --output hedefi de tatbikat başlamadan kontrol edilir; yazma öncesi mevcut kontrol korunur.
- Bu oturumda offline regresyon çalıştırılmadı; değişiklik henüz testle doğrulanmış değildir. Actions dispatch yok. 783 önceki SHA'nın sonucudur, yeni commit sonucu değildir.
- Açık işler: yeni SHA'da offline_gate, K4 hatalı yolun tatbikatı başlatmadığını gösteren negatif test, K4 kanıt dosyası TOCTOU incelemesi, K1-03 gerçek writer haritası ve bağımsız harici restore kanıtı. Kabul 0/92, 0/26, 0/22.
- Korunan IPTV/EPG/playlist/favoriler/logo/yedek/arşiv, eski depo, PR #71 ve cihaz testi değiştirilmedi. Sıradaki somut adım: K4 negatif testleri ve tam offline regresyon; engel varsa açıkça kaydet.


## 22 Ekim 2026 — K4 erken red negatif testleri
- Kod 7dd644cf307eed79394cd70be4a65d2fab1fe83d üzerine tests/test_restore_drill.py negatif testleri eklendi: commit 56ca20984f043263579179ee810b04b53f0304ef [skip ci]. Yanlış izole rapor adı ve mevcut normal çıktı hedefi, run_drill çağrılmadan reddedilmelidir. Önceki tekrar-yazma beklentisi K1 ProtectedWriteRejected ile eşleştirildi.
- Bu çalışma ortamında GitHub deposu yerel kopyalanamadı (github.com DNS erişimi yok). Testler çalıştırılmadı; yeşil sonuç veya 783 yeni test iddiası yok. Actions dispatch yapılmadı. Öncelik: erişilebilir ortamda python -m unittest tests.test_restore_drill ve python -m madsc.offline_gate doğrulaması, sonra K4 tüketici yarış koşulu incelemesi.
- Korunan veri, eski depo ve cihaz testi değişmedi; gerçek kabul 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K4 kanıt okuyucu sertleştirme
- madsc/k4_evidence.py commit 37f74521295d84705a702da4d4b13d696f50fcb8 [skip ci]: çıktı yolu okumadan önce denetlenir; kanıt os.open/O_NOFOLLOW (varsa), fstat ile regular/single-link, 1 MiB bounded read kullanır. Symlink parent kontrolü korunur. Test commit 80972e5badcc47173df7f4d613891b268daeade5: mevcut çıktı, symlink ve büyük kanıt negatif senaryoları.
- Kod/test GitHub'a kaydedildi; bu turda yerel test ve offline_gate çalıştırılmadı, Actions tetiklenmedi. O_NOFOLLOW olmayan platformlarda yarış koruması sınırlıdır; parent değişimi yarışına karşı tam fd-tabanlı dizin zinciri henüz yoktur.
- Öncelik: test_restore_drill ve test_k4_evidence + tüm offline_gate çalıştırıp gerçek sonuçları kaydet; K1-03 gerçek writer denetimine devam et. Gerçek kabul 0/92, 0/26, 0/22; korunan veriye dokunulmadı.


## 22 Ekim 2026 — K4 doğrulayıcı çıktısında ikinci kapı
- madsc/k4_evidence.py commit d8e5e1925c7ea9994f3e0649b4640cf5569b038a: parse/doğrulama sonrası çıktı yolunu tekrar denetle; os.open(O_EXCL|O_CREAT|O_NOFOLLOW varsa) ile tek seferlik çıktı oluştur. tests/test_k4_evidence.py commit bc21ebd0954250b65b0ae4665d40775242ecee91: geçerli kanıttan çıktı, production_ready=false, external_storage_proven=false ve ikinci yazmayı reddetme senaryosu.
- Yerel depo indirme github.com DNS hatası nedeniyle mümkün olmadı; bu yeni SHA için testler/offline_gate çalıştırılmış değildir, GitHub Actions tetiklenmedi. Elde doğrulanmış yeni test sonucu yoktur. Tam parent-ancestor TOCTOU koruması halen açık; K1 runtime kabul iddiası yok.
- Sonraki öncelik: erişilebilir çalıştırma ortamında test_restore_drill, test_k4_evidence ve python -m madsc.offline_gate; gerçek sonuçlar gelmeden 783 sayısını güncel sayma. Gerçek kabul 0/92, 0/26, 0/22. Korunan dosyalar, eski depo ve IBO cihaz testi değişmedi.


## 22 Ekim 2026 — K4 JSON/üst-dizin negatif testleri
- tests/test_k4_evidence.py commit b853106868f1cc13bc2172051c22bd71641ec7a8 [skip ci]: yinelenen files_checked JSON anahtarı ve sembolik bağlantılı kanıt üst dizini reddi; başarısız doğrulamada çıktı yokluğu. Kod davranışı değişmedi.
- Yerel ortam github.com DNS çözümleyemiyor; testler/offline_gate bu yeni SHA'da çalıştırılmadı, Actions dispatch yok. Gerçek kabul 0/92, 0/26, 0/22. Öncelik erişilebilir test koşucusunda odaklı testler ve tam offline_gate; test sonucu olmadan yeşil iddia edilmez.


## 22 Ekim 2026 — K4 hardlink negatif testi
- tests/test_k4_evidence.py commit 9facdef81be2553e145465e9c65cbff889b11b2f [skip ci]: kanıt dosyasının stat.st_nlink != 1 durumunda reddi ve çıktı yokluğu kontrolü; üretim verisine dokunulmadı.
- Bu oturumda git ls-remote github.com DNS çözümleme hatası verdi. Yerel testler/offline_gate çalıştırılmadı, GitHub Actions tetiklenmedi. Test sonucu doğrulanana kadar gerçek kabul 0/92, 0/26, 0/22 olarak kalır.


## 22 Ekim 2026 — K4 O_NOFOLLOW kapısı
- madsc/k4_evidence.py b0f1d0a49966608c8e63ad291f46a9fb043c2cd4 [skip ci]: os.O_NOFOLLOW yoksa kanıt okuma fail-closed. tests/test_k4_evidence.py eadb7e40a412679c30108a0260c6ada76fa12a71 [skip ci]: bu durumu ve çıktı üretilmediğini kontrol eden test.
- Yerel git ls-remote: github.com DNS çözümlenemiyor; testler ve offline_gate yeni HEAD üzerinde çalıştırılmadı. Actions tetiklenmedi. Üst dizin TOCTOU sertleştirmesi ve gerçek kabul kanıtı açık; 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K4 sahte üretim iddiası reddi
- K4 verify(): production_ready=True/1 ve category='k3' gibi sahte alanları reddetme, opsiyonel category yoksa eski run_drill raporuyla uyum; kod c189cde33a47690373eddc6c502b4e14cfb82fd6, test afe19df9646868a0153a19c4c9895c4bf90c29d1 [skip ci].
- Yerel git ls-remote denemesi github.com DNS çözümleme hatasıyla başarısız. Bu SHA için test ve offline_gate doğrulaması yapılmadı, Actions tetiklenmedi. Gerçek kabul 0/92, 0/26, 0/22; korunan veriye dokunulmadı.


## 22 Ekim 2026 — K5 davranış karşılaştırma çıktısı, test bekliyor
- madsc/legacy_parity_cli.py commit 108de8e7c049bf8abab52fa69ae587133ba420f4: K5 karşılaştırma raporu exclusive os.open(O_CREAT|O_EXCL, varsa O_NOFOLLOW) ile açılıyor; ikinci yol kontrolü korunuyor. tests/test_legacy_parity_cli.py commit 1f4d31a03f3ca7b61bd06b28c4693bd3e3142867: ikinci kontrol sonrasında sembolik bağlantı değişiminde hedefin korunmasını denetleyen regresyon eklendi.
- Bu SHA için test sonucu yok; GitHub Actions tetiklenmedi. K5 gerçek davranış eşdeğerliği 0/92, 26 runtime güvenlik 0/26, görev kabulü 0/22. Öncelik test_legacy_parity_cli, tam offline_gate, sonra eksik gerçek eski/yeni çalışma çiftlerini toplu kanıtlama. Korunan veriye dokunulmadı.


## 22 Ekim 2026 — Playlist K2/K3→K5 güvenli taslak hattı
- madsc/playlist_previews.py: katalogdaki yinelenen source_index ve URL SHA256 reddi (db091a3f88e7ce515858310d70c6d754925eec5d); üretim yazısı/hazırlığı iddiası taşıyan kataloglar reddediliyor (88ceeb937285d5adc5433f659de67f2d62a2945a). Regresyon testleri tests/test_playlist_previews.py (c9a88cc750bf8c98272ef4ef23cca13f84583fd1 ve c8f5592d1399fc21b8a7b1c312451fbf49b18f59).
- Kod ve testler commit edildi, bu SHA için test yürütülmedi. Mevcut playlist/YEDEKLER/YENILER/FAVORILER/EPG değiştirilmedi; Actions tetiklenmedi. İzole taslak üretimi canlı otomatik playlist güncellemesinin kanıtı değildir. 92 davranışsal kabul, 26 runtime güvenlik kabulü ve 22 görev kabulü değişmedi.

## 22 Ekim 2026 — bekleyen K1/K4/K5 paketinin toplu doğrulaması
- Başlangıç main `adbaf72d6eb21b88d81c557ad0076a70ca617164`; eşzamanlı playlist kaçış düzeltmesi `5af20718f14be617e0c20b5fee797572d7924a6e` okundu ve korundu. Kod/test/kanıt commit'i `61bbf78214a63400083cf7d615c64a1b13547896` (`[skip ci]`).
- İlk odaklı 44 testte iki failure ve bir error bulundu: hardlink testi geçerli kaynağı hâlâ iki linkli bırakıyordu; literal backslash kaçışlı playlist adı reddedilmiyordu; K1 AST envanteri yerel `flags` değişkenindeki `O_CREAT` bitlerini ve `os.fdopen` modunun ikinci argümanını çözemiyordu. Üçü düzeltildi; eşzamanlı `5af2071` playlist düzeltmesi tekrar yazılmadı.
- K1 envanteri artık aynı lexical scope içindeki en yakın flag atamasını çözerek `os.open(..., flags)` yazıcılarını bulur; `os.fdopen(fd, mode)` gerçek ikinci argümana göre okuma/yazma ayrılır. Aday sayısı 130, dinamik inceleme 20; subprocess ve gerçekten dinamik çağrılar açık kalır. `all_writer_callsites_manually_verified=false`; bu 26/26 runtime kabulü değildir.
- K4 erken hedef reddi, O_NOFOLLOW, regular/single-link/bounded read, duplicate JSON, sahte production/category ve exclusive çıktı testleri; K5 parity/playlist ve source-import sınırları birlikte geçti. Odaklı sonuç 44/44. Nihai `python -m madsc.offline_gate`: **800/800**, beş izole K kapısı, kurulum envanteri, beş rapor/K5 round-trip, 92+7/10 komut/22 görev ve `static_gaps_total=0` başarılı. `git diff --check` temiz.
- Kanıt: `docs/K1_K4_K5_PENDING_VALIDATION_2026-10-22.json`. Actions dispatch/rerun, canlı stream probing, cihaz testi, üretim/korunan veri yazısı, eski depo, merge veya PR #71 işlemi yapılmadı.
- Açık kabul/engeller: 0/92, 0/26, 0/22. Gerçek aynı-input bağımsız legacy/replacement execution+artifact çifti, K2/K3 canlı/harici ölçümler, IBO cihaz sonucu, K4 bağımsız harici restore ve 20 dinamik writer/subprocess adayının gerçek runtime değerlendirmesi açık.
- Sıradaki somut yerel iş: 20 dinamik aday içinden K1 writer etkisi olabilen subprocess çağrılarını komut/argüman düzeyinde sınıflandır; yalnız salt-okunur probe/test çağrılarını ayrı işaretle, belirsiz veya üretim yazabilen çağrıları fail-closed inceleme olarak bırak. Harici kanıt olmadan kabul sayaçlarını artırma.


## 22 Ekim 2026 — Bu sohbetin kapsamı K2 ve K4; ortak çalışma kaydı
- Kullanıcının son talimatı: bu sohbet yalnız K2 ve K4'e odaklanacak, diğer sohbetle çakışmayacak ve biten işleri tekrarlamayacak. Kullanıcı sohbet başlığını K2 ve K4 istedi; başlık değiştirme aracı yok, fiilen değiştirildi denmedi.
- Güncel main'de diğer sohbetin restore_drill erken hedef kontrolü zaten bulundu; yeniden uygulanmadı ve dosya değiştirilmedi. K1/K5, online pilot, parser ve playlist değişiklikleri korundu. 56f64fa test tabanından e6b9e396776f04f06dd7ab55e7528e3c93c764a8 yayın tabanına gelen üç commit incelendi; bu paketin dosyalarıyla çakışmıyor.
- K4 backup_to_new_sandbox / restore_to_new_sandbox: yeni kök hedef ve tüm üst dizinler kaynak içerik okunmadan ve mkdir öncesi merkezi K1 kapısından geçiyor. Korunan EPG/FAVORILER/YEDEKLER/logo/playlist hedefleri engelleniyor. Ortak fixture_report_writer yalnız K4'ün gerekli bağımlılığı olarak düzeltildi: korunan kök altında reports dizini bile oluşturulmadan ret; mevcut son yazma kontrolü korunuyor. Aynı korumayı kullanan K3/K5 raporları da test edildi, ilgili iş akışları değiştirilmedi.
- K2 atomic_write_pair: yalnız dosya adı yerine tam hedef/üst dizin ve mevcut regular/single-link dosya kontrolü, staging öncesi ve os.replace öncesi uygulanıyor. Geçerli atomik güncelleme semantiği korunuyor. History ZIP çıkarıcısı her iki belgenin history/channels şemasını dizin veya dosya oluşturmadan doğruluyor. Geçersiz şema artık yarım çıktı bırakmıyor.
- Son K2/K4 odaklı doğrulama 87/87 başarılı. Tam kapı 56f64fa tabanında 816 test çalıştırdı: 5 failure + 3 error nedeniyle BAŞARISIZ. Beş izole K kapısı ve beş rapor/K5 round-trip geçti. 816 başarılı test olarak sunulmayacak. Kanıt ve kaynak hashleri docs/K2_K4_WRITE_PREFLIGHT_2026-10-22.json içinde.
- Diğer sohbet için mevcut toplu engeller: workflow_consolidation.consolidation_plan yeni madsc-online-pilot-gates.yml dosyasını envanter dışı görüyor; bu kök hata beş offline kapı testini de düşürüyor. tests/test_playlist_previews.py içindeki test_import_to_five_playlists_end_to_end_offline ve test_offline_cli_emits_five_drafts_without_writing_files kaynakları gerçek satır sonu yerine literal \\n kullanıyor, Invalid playlist header alıyor. Bu aktif diğer-sohbet dosyaları bu pakette değiştirilmedi. Düzeltmeleri sonrasında tam kapı yeniden gerekli.
- Önceki /tmp çalışma ortamı kayboldu; yayımlanmamış geçici K4 değişiklikleri güncel main ile karşılaştırılarak yalnız eksik kısmı yeniden oluşturuldu. İlk geçici odaklı testte eski kapı çağrı beklentisi başarısızdı; reports mkdir öncesi ret beklentisiyle güncellendi ve 87 test geçti.
- Üretim verisi, eski depo, PR71, merge, Actions dispatch ve canlı probing yapılmadı. Gerçek kabul 0/92, 0/26, 0/22; harici restore/IBO/bağımsız runtime kanıtı açık. Sıradaki K2/K4 işi: mevcut geçmiş alım ve yedek kopyalama akışlarında değişen kaynak/yarım yazma temizliği sınırlarını incele; dış depolama kanıtı olmadan harici restore kabulü verme.

## 23 Ekim 2026 — K4 manifest root alias koruması
- Güncel main incelendi; K4 snapshot_manifest() yalnızca son dizin bileşeninin symlink olup olmadığını denetliyordu. Gerçek bir dizine symlink üst dizin üzerinden ulaşılması doğrudan manifest snapshot çağrısında kabul edilebilirdi.
- Kod düzeltmesi: d23c4e54e6882b01bba1440ac38e61d8abb180b4 — snapshot_manifest() artık kök dizinin ve tüm üst dizinlerin symlink olmadığını, ayrıca kökün kanonik mutlak yolla eşleştiğini kontrol ediyor.
- Negatif regresyon testi: c53875f29dc0d605d24295e642dcc75f9ab358ee — gerçek köke symlink üst dizinden erişildiğinde manifest snapshot reddedilmeli.
- Test çalıştırılmadı; Actions yeniden tetiklenmedi ([skip ci]). Dolayısıyla kod/test sonucu doğrulanmayı bekliyor.
- Canlı playlist, EPG, favoriler, cihaz verileri, üretim yedekleri ve arşivler değiştirilmedi. Harici backup/restore ve K3 IBO cihaz kabulü açık. Kabul sayaçları değişmedi: 0/92, 0/26, 0/22.

## 23 Ekim 2026 — K4 sandbox rollback yarış koşulu
- İncelemede backup_to_new_sandbox() ve restore_to_new_sandbox() hata sırasında yalnızca destination yoluna bakarak shutil.rmtree(destination) çağırıyordu. Hata anında aynı yol başka bir işlem tarafından başka bir dizinle değiştirilirse, cleanup bu işleme ait olmayan dizini silebilirdi.
- Kod commit d3ce6cb5eeb962473dfd0cc95ec05d84e679d0b6: her iki işlem de oluşturduğu dizinin (st_dev, st_ino) kimliğini kaydediyor; rollback yalnızca hedef hâlâ aynı gerçek dizin inode'uysa kaldırıyor.
- Negatif test commit 34028a822c9d38738a7edcf35a84913e3c0b17c4: hem backup hem restore sırasında hedef dizin eşzamanlı değiştirilirse, yeni dizindeki sentinel dosyasının korunması doğrulanacak.
- Testler çalıştırılmadı; bu commit'lerde [skip ci] kullanıldığı için otomatik CI sonucu beklenmiyor. Bu yüzden doğrulanmış başarı iddiası yok.
- Önceki root-symlink koruması ve testi: d23c4e54e6882b01bba1440ac38e61d8abb180b4 / c53875f29dc0d605d24295e642dcc75f9ab358ee.
- Canlı IPTV/EPG/favoriler/cihazlar/üretim yedekleri/arşivler değiştirilmedi. Harici yedek ve üretim geri yükleme kabulü açık. Sayaçlar değişmedi: 0/92 workflow, 0/26 güvenlik kuralı, 0/22 ana görev.

## 23 Ekim 2026 — K4 manifest symlink TOCTOU sertleştirmesi
- snapshot_manifest() önceden symlink kontrolleri sonrası Path.open() ile açıyordu; kontrol ile açılış arasında bir bileşen symlink ile değiştirilirse TOCTOU riski kalıyordu.
- Kod commit: cca807332bf900d9d70206c4a8261acfb1c21cdf. Yeni _open_relative_file_nofollow() root ve her alt dizini O_DIRECTORY|O_NOFOLLOW ile dir_fd üzerinden açıyor, son dosyayı da O_NOFOLLOW ile açıyor; fstat ile normal dosya ve nlink==1 kontrolü korunuyor. Manifest yolu çözülmüş hedeften değil, doğrulanmış istenen göreli yoldan yazılıyor.
- Test commit: 0ad1566d25799edb610745a60a76ce24e27a466c. Final symlink reddi, ara dizin symlink reddi ve nested göreli yol korunması için üç test eklendi.
- Testler çalıştırılmadı; commit mesajlarında [skip ci] olduğu için CI otomatik tetiklenmedi. Kod ve test sonucu doğrulanmayı bekliyor.
- Önceki sandbox rollback inode-koruması d3ce6cb5eeb962473dfd0cc95ec05d84e679d0b6; testler 34028a822c9d38738a7edcf35a84913e3c0b17c4.
- Üretim playlist/EPG/favoriler/cihaz verileri ve yedekler değiştirilmedi. Gerçek harici backup/restore ve K3 cihaz kabulü açık. Kabul sayaçları: 0/92 workflow, 0/26 runtime güvenlik kuralı, 0/22 ana görev.

## 23 Ekim 2026 — K1/K4 son CI hata kök nedenleri
- İncelenen Actions çalışması 39863302393, commit 38c2a46702: 970 testten 4 hata. K4 backup rollback hata yolunda created_identity eksik olduğuna dair NameError raporlanmıştı; güncel main dosyası yeniden okundu ve destination.mkdir() hemen sonrasında lstat ile created_identity alınmasının mevcut olduğu doğrulandı (main blob 780c64811d0cf1267548bcf94a2da009e408d847). Eski CI commit'i bu düzeltmeyi içermiyordu.
- K1 test_fixture_report_writer.py içindeki yarış testi unlink()+write() yapıyordu; dosya sistemi inode numarasını hemen yeniden kullanırsa yeni dosya yanlışlıkla aynı inode gibi görünebilirdi. Test artık eski inode'u ayrı bir yolda tutmak için rename ediyor, ardından concurrent replacement oluşturuyor. Commit e3ee2405d9dd3bc23ca567e43c26288fcab16d28.
- Bu test değişikliği [skip ci] ile kaydedildi; yeni CI sonucu henüz yok. Canlı playlist/EPG ve üretim yedekleri değişmedi. Beşli offline fixture gate önceki kayıtta başarılıydı; tüm güncel regresyon kapısı bu yeni commit için doğrulanmayı bekliyor. 92 workflow/26 güvenlik kuralı/22 ana görev davranışsal kabulü hâlâ kanıtlanmış değil.

## 23 Ekim 2026 — Beşli sistem offline kabul doğrulaması
- GitHub Actions run 39863567977, commit de82210cdea1281b8ad2d1f622925fa1d8d8c397 başarılı tamamlandı: 970 test keşfedildi, tests_passed=true, five_stage_fixture_gate_passed=true, all_offline_gates_passed=true.
- Bu sonuç güncel K1/K4 rollback yarış testi düzeltmesini içeriyor. K1 testindeki önceki inode-reuse flakiness düzeltmesi de bu yeşil çalışmada doğrulandı.
- Bu yalnızca offline regression + isolated five-stage fixture kabulüdür; workflow raporunda production_acceptance=false. Beş raporun fixture round-trip doğrulaması offline ortam içindir, üretim entegrasyon kanıtı değildir.
- Açık kabul: 92 eski workflow davranışsal eşdeğerliği 0/92; 26 runtime güvenlik kuralının üretim uygulama kanıtı 0/26; 22 ana görev 0/22; harici yedek/izole gerçek geri yükleme ve IBO Player Pro EPG cihaz kabulü bekliyor.
- Canlı yayın listesi, EPG, favoriler, cihaz verileri ve üretim yedekleri değiştirilmedi. Sonraki adım: K1–K5 entegrasyon manifesti ve 92 workflow için her biri adına kaynak hash + davranış eşlemesi + negatif/pozitif test + artifact kanıtı üretmek; sayacı yalnız doğrulanmış maddelerde artırmak.

## 23 Ekim 2026 — K3/K4 sohbeti: beşli sistem, K4 güvenli kopyalama, devredilen işler
- Başlangıç gözlemi: GitHub Actions `39863567977`, SHA `de82210cdea1281b8ad2d1f622925fa1d8d8c397` üzerinde 970 offline test ve K1–K5 izole fixture kapısı başarılı. Bu eski SHA için doğrulanmış offline testtir; yeni kodun test sonucu değildir. Yeni K1 AST envanter koşusu `39863897767` gözlem sırasında in_progress durumundaydı; bu sohbet Actions dispatch/rerun yapmadı.
- K4 kaynak incelemesi iki açık bulgu gösterdi: `_open_relative_file_nofollow()` O_NOFOLLOW/O_DIRECTORY bulunmasa sessizce `0` ile devam ediyordu; `backup_to_new_sandbox()` ve `restore_to_new_sandbox()` manifesti güvenli okusa da asıl kopyalamada tekrar `Path.open()` ile kaynak açıyordu. Bu, manifest ile kopyalama arasındaki symlink-swap penceresini açık bırakıyordu.
- Kod commit `46d04cfe0f59c6a11951862190d4aba3ec0dc26a`: O_NOFOLLOW/O_DIRECTORY ve os.open dir_fd desteği yoksa işlem fail-closed, dosya O_NONBLOCK ile açılır.
- Kod commit `e293a0d62211a8cc96a6cccc82cbb350fd19371e`: sandbox yedekleme ve geri yükleme kaynakları aynı descriptor-relative nofollow yordamından okunur; açılan dosyada os.fstat ile regular file ve nlink==1 tekrar denetlenir.
- Test commit `02e70ee607855111ba10bdcbed61a1d4c37afa0d`: eksik nofollow desteği, backup kaynak symlink-swap ve restore kaynak symlink-swap için üç negatif regresyon eklendi; dış sentinel dosyası korunur ve yarım sandbox output geri alınır.
- Değişiklikler yalnız `madsc/backup.py`, `tests/test_backup.py` ve bu DEVAM_NOTU dosyasındadır; K1/K2/K5 koduna dokunulmadı. Yeni testler çalıştırılmadı ve bu SHA için CI kabulü yok; [skip ci] kullanıldı.
- K1–K5 offline zinciri tanımlı, fakat gerçek üretim kabulü açık: eski 92 workflow 0/92 bağımsız davranışsal kabul, 26 runtime güvenlik kuralı 0/26, 22 ana görev 0/22. K3'te gerçek ffprobe/IBO Player Pro cihaz/EPG kanıtı, K4'te harici backup ve izole restore makbuzu eksik.
- Korunan canlı IPTV listeleri, EPG/XMLTV, FAVORILER, YENILER, YEDEKLER, HEPSI, logolar ve üretim arşivleri değişmedi. Eski depoya ve PR #71'e dokunulmadı.
- Sıradaki işlem: GitHub'daki mevcut yeni CI sonucunu salt okunur kontrol etmek; K4 3 yeni testi ve tam offline regresyonu koşup başarısızlıkları düzeltmek (Actions tetiklemek için ayrıca açık onay gerek). Sonra K3 cihaz ve K4 harici kaynak kabul kanıtlarını gerçek dış kaynaklardan toplamak.

## 23 Ekim 2026 — K3/K4 sertleştirmesi CI ile doğrulandı
- GitHub Actions run 39864090233, SHA bcd8245a143abb5a24fc05b244127f28876c2ce2, offline-tests job conclusion success. Log: 979 test keşfi; tests_passed=true; five_stage_fixture_gate_passed=true; all_offline_gates_passed=true; production_acceptance=false.
- Bu SHA K4 kaynak dosyalarını nofollow/dirfd ile açan kod commitlerini 46d04cfe0f59c6a11951862190d4aba3ec0dc26a ve e293a0d62211a8cc96a6cccc82cbb350fd19371e, ayrıca üç negatif test commitini 02e70ee607855111ba10bdcbed61a1d4c37afa0d içerir. Bir önceki notta bekleyen bu K4 offline regresyon kanıtı artık başarılı koşuyla doğrulanmıştır.
- Bu CI otomatik olarak diğer K1 çalışmasının commit'iyle oluştu; bu sohbet yeni Actions dispatch/rerun çağrısı yapmadı. Korunan IPTV/EPG/favoriler/yedekler/arşivler değiştirilmedi.
- Sonraki kabul ayrı kalır: 92 davranışsal workflow 0/92, 26 runtime güvenlik kuralı 0/26, 22 ana görev 0/22. K3 IBO cihaz/EPG gerçek doğrulaması, K4 harici yedek ve restore makbuzu açık.


## 23 Ekim 2026 — K3 EPG kimlik doğrulaması ve K4 descriptor-relative sandbox kopyalama
- K3 bulgusu: XMLTV duplicate channel IDs sözlük/set oluşturulurken sessizce çöküyor ve geçerli tvg-id eşleşmesi gibi görünebiliyordu. `madsc/trial_epg_matching.py` artık `<tv>` root'u, boş id'leri ve duplicate id'leri reddeder; `madsc/epg.py::check_epg_mapping` de boş/duplicate kanal kimliğinde fail-closed. Kod commitleri `939267f738745476953545c0cccd162e7aa68ff2`, `9a1ebdcb02f06e9b2fc476449799df0f3a2897e6`; regresyon testleri `f48f04fab3b455ca7b9c8fceb7c5ac87b1363004`, `420d15d1e318e81d1bb55b024a3cf01003bfcd5b`.
- K3 offline CI: run `39865646219` ve `39865719002` başarıyla tamamlandı; run `39865719002` SHA `420d15d1`, 982 test, five-stage fixture gate ve all offline gates true. Bu XMLTV parsing doğrulamasıdır; IBO Player Pro cihaz testi değildir.
- K4 bulgusu: sandbox backup/restore kopyası kaynak dosyaları descriptor-relative nofollow ile açıyordu, fakat hedefteki iç klasör ve dosyalar hâlâ path-based `mkdir/open` ile oluşturuluyordu. `madsc/backup.py` artık hedef dosyaları da root descriptor + O_NOFOLLOW/O_DIRECTORY + dir_fd + O_EXCL ile oluşturur; destination root inode'u başlangıçta oluşturulan inode ile karşılaştırılır; symlink'li iç klasör, kök inode değişimi ve backslash separator testleri eklendi. Kod `e32d522d93bb1e2307ab0bee9eb88d1e61625043`, testler `a5590c3e451d64f35d8e9d11c4fa32336817948d`, `949c2398bc02d005f69715b9e4872b4e989d0ca0`, `a4c70f7277be8aad73cdd95d027115b7bcab469d`.
- K4 offline CI run `39865918685`, SHA `949c2398`: 989 test; tests_passed, five_stage_fixture_gate ve all_offline_gates başarılı. Son test run `39865933101`, SHA `a4c70f7`: 990 test; tests_passed, five_stage_fixture_gate ve all_offline_gates başarılı. K1 AST envanteri 97 Python dosyasında 75 mutasyon adayı raporladı (kopyalama kodu artık farklı API kullanıyor). Üretim kabulü false.
- İstenen eski run `39863892845` GitHub API'de 404 döndürüyor; ID sonucu doğrulanamadı. En güncel erişilebilir run `39865933101` başarıyla doğrulandı.
- K3 gerçek HLS/ffprobe ve IBO Player Pro cihaz pilotları workflow_dispatch gerektiriyor. Mevcut GitHub bağlantısında workflow dispatch/POST aracı bulunmadığından bu pilotlar bu oturumda başlatılamadı; canlı playlist/EPG'ye yazılmadı. K4 harici storage kanıtı ve bağımsız dış ortam restore'u da yapılmadı; üretim yedeği kullanılmadı.
- Açık sayaçlar değişmedi: legacy 0/92 davranışsal kabul, runtime security 0/26, ana görevler 0/22. PR #71 merge edilmedi; eski depo ve üretim verileri değiştirilmedi.


## 23 Ekim 2026 — HEPSI yeni sohbet devri: 990 test ve gerçek kabul eksikleri
- Kanonik kapsamlı devir: `docs/HEPSI_YENI_SOHBET_DEVIR_2026-10-23.md` (oluşturma commit `b463c13fd75fefa470cc889cc229f04633044033`). Yeni sohbette önce bu dosyanın tamamını oku.
- Son CI `39865933101`, SHA `a4c70f7277be8aad73cdd95d027115b7bcab469d`: 990 test başarılı; K1–K5 fixture ve offline gate yeşil; production_ready=false. Test SHA'sından sonra yalnız devir/dokümanlar değişti.
- 22 ana görev: 7 in_progress, 15 pending, 0 completed. Eski 92 workflow: altı batch'te 18 statik kaynak incelemesi (%19,6), 74 statik kaynak incelemesi bekliyor; davranışsal eşdeğerlik 0/92. 26 runtime güvenlik kuralı kabulü 0/26; 22 görev bağımsız kabulü 0/22. İnformal toplam proje yüzdesi gerçek kabul oranıymış gibi söylenmemeli.
- K3: duplicate/eksik XMLTV ID fail-closed kod ve testleri güncel CI'ya dahil; gerçek HLS/IBO Player Pro/EPG cihaz kanıtı eksik. K4: descriptor-relative kaynak/hedef sandbox kopyalama testleri CI'da başarılı; harici backup ve bağımsız restore kanıtı eksik.
- K1: 97 Python dosyasında 75 AST mutasyon adayı manuel tasnif bekliyor. K5 92 workflow için birebir runtime parity, yan etki, artifact, retry/timeout ve reviewer kanıtı eksik.
- Eski depoya yazma, PR #71 merge, canlı IPTV/EPG/favori/cihaz/yedek/arşiv değişikliği ve izinsiz workflow_dispatch yapılmadı. Yeni sohbette HEAD ve Actions'ı tekrar doğrula; diğer paralel sohbetleri ezme.


## 23 Ekim 2026 — K5 legacy workflow batch 07 (salt-okunur kaynak incelemesi)
- Yeni kaynak inceleme belgesi: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_07_2026-10-23.md`; commit `bf2db8d7e19898a91f1d3ac70baa3cc765c6e4d9`.
- Frozen `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7` üzerinde üç yeni workflow incelendi: `automatic-png-logos.yml`, `birlesik-durum-raporu.yml`, `genis-kanal-tarama.yml`. Workflow SHA'ları kaynak envanteriyle eşleşti; eski depoya yazılmadı.
- K1/K5 için kritik bulgu: `scripts/automatic_png_logos.py` korunan `CALISANLAR.m3u` dosyasını doğrudan `playlist.write_text(updated,...)` ile yazıyor. Workflow sonrasında diff görürse `git restore -- CALISANLAR.m3u` çalıştırıyor; write-then-restore, protected path'e hiç yazmama garantisi değildir. Replacement parity, izole fixture kopyası ve sıfır protected-path write ile kanıtlanmalı. Bu eski workflow çalıştırılmadı; playlist değişmedi.
- Birleşik durum workflow'u snapshot JSON'ları üretir ve sadece generated health report yazar; tarihsel snapshot'ı canlı durum gibi sunmamalı. Geniş kanal taraması 9 public M3U kaynağı ve ffprobe kullandığı için gerçek ağ/probe işidir; fixture/parity amaçlı tetiklenmedi.
- Statik inceleme toplamı 21/92; statik inceleme bekleyen 71. Bu kabul değildir: davranışsal parity 0/92, runtime güvenlik 0/26, ana görev kabulü 0/22, production_ready=false.


## 23 Ekim 2026 — K1 yazma-adayı tarayıcısındaki iki gerçek kapsam boşluğu
- K1 kod commit'leri: `c6affc2824a1c8e5288da16eff853f7bb690e1ca` (dinamik open modu envanteri), `d6f1ce5c98c85658336198b542d0a7ccb65a6394` (shell/subprocess çağrıları envanteri).
- Regresyon test commit'leri: `2a0796ebe98b03db88905534c6546153dd92020a` (positional/keyword dinamik open modu), `cb0a046252e1a75d119ae12e0af6c76028b3379c` (subprocess.run ve os.system).
- Bulgu 1: `open(path, requested_mode)` ve `path.open(requested_mode)` sabit metin olmayan modlarda yazma modu taşıyabilmesine rağmen AST envanterinden düşüyordu. Tarayıcı artık bu çağrıları `[dynamic mode]` etiketiyle incelemeye alıyor.
- Bulgu 2: shell/subprocess komutları Python dosya API mutasyonları gibi envantere alınmıyordu. `subprocess.run/call/Popen/check_call/check_output`, `os.system` ve `os.popen` artık `[process command requires review]` adayı olarak listeleniyor; bu sınıflandırma her komutun yazma yaptığı anlamına gelmez, manuel komut incelemesi gerektirir.
- İki yeni test dosyaya kaydedildi. Bu kayıtta GitHub birleşik status API'si commit için status/check döndürmedi; bu nedenle yeni testlerin CI sonucu **henüz doğrulanmış değil**. Son doğrulanmış genel baseline run `39865933101`, SHA `a4c70f7277be8aad73cdd95d027115b7bcab469d`, 990 testtir ve yeni kodu kapsamaz.
- Sonraki K1 adımı: güncel Actions sonucu erişilebilir hale gelince test edilen SHA'yı doğrula; ardından 75 adayın her birini gerçek mutasyon/yan etki, guard sırası ve çağıran zincirine göre sınıflandırıp kritik korumasız yazıcılara hedefli negatif test ekle.
- Kabul sayaçları değişmez: K1 runtime 0/26, legacy davranış 0/92, ana görev 0/22; production acceptance false. Korunan üretim verilerine dokunulmadı.


## 23 Ekim 2026 — K4 harici yedek/izole restore kabul kapısı
- Güncel çalışma dalı `main`; K4 kodunun mevcut blob SHA'ları: `madsc/backup.py` = `f3b4171805b4206dc79d12366ba84df5ea2ba68c`, `tests/test_backup.py` = `bfcc3b734431ead1cf1d66967503d7b084a45c92`, `tests/test_backup_manifest_hardening.py` = `e73a7c724532b4c1e2760b9f3aed6effee35b0fe`. K4'ün no-follow/dirfd, SHA-256 manifest, bağımsız sandbox kopyası ve üç ağaçlı restore karşılaştırma testleri mevcut; bunlar dış servis/üretim kanıtı değildir.
- Yeni belge: `docs/K4_EXTERNAL_BACKUP_RESTORE_ACCEPTANCE_2026-10-23.md`. K4-15 dış depolama makbuzu/nesne kimliği; K4-16 harici kaynaktan gerçek izole restore ve bağımsız SHA kanıtı; K4-17 arşiv/VOD envanter ve güvenli kopya eşdeğerliği; K4-18 ayın 1'i/15'i timezone, DST, retry/idempotency ve gerçek scheduler run kanıtını tek tek tanımlar.
- `docs/K1_K5_KANITLI_GOREV_DEFTERI.json` K4-15/16 kanıt gereksinimleriyle güncellendi. Belge/ledger güncellemeleri için commitler: `41773318afc7c1849724d1397e4990959051f5b7`, `3478b770b3d5ad28b181cca8641c5425a1ecaf38`.
- Kabul durumu değişmedi: K4-15 pending, K4-16 in_progress (sandbox fixture only), K4-17 pending, K4-18 pending. Genel kabul: 0/92 eski workflow davranışsal parity, 0/26 bağımsız runtime güvenlik, 0/22 ana görev. Harici depolama veya kullanıcı cihazı erişimi yapılmadı; Actions dispatch/rerun, merge ve üretim yazması yapılmadı.
- Son genel CI baseline hâlâ Actions `39865933101`, test edilen SHA `a4c70f7277be8aad73cdd95d027115b7bcab469d`, 990 test. Bu K4 belge/ledger değişiklikleri için yeni CI sonucu iddia edilmiyor; kod/test değiştirilmedi.
- Sonraki gerçek adım: yetkili harici yedek sağlayıcısından makbuz ve bağımsız restore run kanıtı geldiğinde dosya/byte/SHA listelerini doğrula; aksi durumda K4 kabulünü açma. Korunan playlist/EPG/favori/yedek/arşiv/cihaz dosyalarına dokunma.


## 23 Ekim 2026 — K5 legacy review batch 08
- Yeni statik inceleme: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_08_2026-10-23.md`; commit `95c1aa9201c8f83b9ce8741cba2cfd2ce143c519`.
- Üç workflow ve doğrudan çağırdığı scriptler sabitlenmiş Git blob SHA'larıyla incelendi: `kanal-kararlilik.yml`, `kaynak-puanlama-kontrol.yml`, `ibo-bagimsiz-test-listesi.yml`.
- Önemli bulgu: IBO listesi akışı keşfi `SCAN_BATCH=-1` ile geniş yapıyor ancak medya testi `ADAY_TEST_GRUBU=0` ile yalnız ilk 30 sıralanmış adayı inceliyor. “Tüm keşfedilen adaylar test edildi” denemez.
- Kararlılık akışında cache restore/save kaynak kodu var ama iki bağımsız run kanıtı olmadan geçmişin kalıcı olduğu kabul edilemez. Kaynak puanlama scripti `KAYNAK_GUVEN_PUANLARI.csv` yazar; izole hedef sınırı ve edge-case davranışı differential test gerektirir.
- Kümülatif statik inceleme 24/92; 68 workflow için kaynak incelemesi bekliyor. Gerçek davranışsal kabul 0/92, runtime güvenlik kabulü 0/26, ana görev kabulü 0/22 olarak korunur.
- Görev defteri K5-19 yeni kanıtla güncellendi: commit `826411b90f37cbe8863f966d874cb4d5925cf6ab`. Bu belge/defter değişiklikleri `[skip ci]`; yeni CI başarısı iddia edilmiyor. En son gözlenen başarılı offline run `39867301153`, test SHA `cb0a046252e1a75d119ae12e0af6c76028b3379c`; bu, daha sonraki HEAD'i veya üretim kabulünü doğrulamaz.
- Sonraki iş: bu üç workflow için güvenli fixture tabanlı differential testleri eklemek; önce deterministik kaynak puanlama ve IBO artifact seçimini test et. Gerçek keşif/ffprobe/IBO/üretim işlemi için yetki ve bağımsız kanıt olmadan çalıştırma.
- Korunan playlist, EPG, favori, cihaz, logo, yedek/arşiv dosyalarına dokunulmadı; eski `Madsc55/madsc-tv` deposu salt okunur kaldı; Actions dispatch/rerun ve merge yapılmadı.


## 23 Ekim 2026 — K2 metadata çakışması düzeltmesi ve devir
- `madsc/discovery_batch.py` yinelenen EXTINF metadata adlarını case-insensitive kontrol ederek `duplicate_metadata_attribute` ile reddeder; metadata anahtarları normalize edilir.
- Kod: `a83211a36e9ad1dd1c6047b74888970ddc33b381`, `b0ab88f2ab2043ecbd24620bd76066a0cd924b45`. Regresyonlar: `b4b13f9de4913af05f5ddcc21e714fff8227c667`, `75d1fa756a232d4ee594bb5ae28faa01abba931b`.
- Birleşik doğrulama raporu güncellendi: `5fab36193e467b302c5bfe6d90b5558fe42b2547`. Merkezi proje hafızası güncellendi: `89d5a1d03aee84207fecfcc7bd2ed4c684d6bdec`.
- CI durumu doğrulanmadı; workflow `workflow_dispatch` gerektiriyor ve manuel dispatch yapılmadı. 990 testlik eski baseline yeni kodu kapsamıyor. Testleri başarılı olarak raporlama.
- Sonraki: güncel HEAD'i tekrar oku; erişilebilir CI sonucu elde edildiğinde regresyonları doğrula. K2-05/06/07/08 durumlarını kanıtsız kapatma. Gerçek kaynak/lisans, günlük eşdeğerlik ve bağımsız artifact SHA kanıtı açık. Üretim listeleri ve eski depo değişmedi.


## 23 Ekim 2026 — K4 workflow kaynak bulgusu
K4 kaynağı `.github/workflows/madsc-04-yedek.yml` blob `28910baa5840da87c97834a9fe4d2708db99a949` incelendi. Yalnız `workflow_dispatch` var; schedule/cron yok. `contents: read`, 10 dakikalık timeout ve 14 günlük Actions artifact'ları mevcut. Akış gerçek harici hedefe yedek yazmıyor; yalnız yerel `reports/k4-source/nested/sample.txt` fixture'ı ile sandbox restore drill yapıyor. Bu nedenle K4-18 için tetikleme eksikliği kaynak seviyesinde doğrulandı; bu workflow'a körlemesine cron eklenmedi çünkü bu gerçek yedekleme sağlamaz ve yanıltıcı kabul yaratır.
- Bulgu `docs/K4_EXTERNAL_BACKUP_RESTORE_ACCEPTANCE_2026-10-23.md` içine eklendi; görev defterinde K4-18 not/evidence güncellendi. Commitler: `7713d91e4a35a86973d8120701c2a6d112a7ae56`, `bfed9d956a8ce4c2cf4f437b5d5eafaf6f5ddabe`.
- Bu iki değişiklik dokümantasyon/kayıt niteliğinde; test başarısı iddia edilmiyor. Önceki genel CI run `39867650745` (SHA `a83211a36e9ad1dd1c6047b74888970ddc33b381`) bu sırada kontrol edildi ve o an `in_progress` idi; nihai sonucu doğrulanmadan başarılı sayılmamalı. Güncel main HEAD'i her devam adımında yeniden oku; paralel K1/K2/K3/K5 çalışmaları nedeniyle aynı dosyaları eski SHA ile güncelleme.
- K4-15/16/17/18 kabulü hâlâ tamamlanmadı. Harici sağlayıcı makbuzu/gerçek restore kanıtı yok; üretim dosyaları ve cihazlar değişmedi, Actions dispatch/rerun yapılmadı.


## 23 Ekim 2026 — K1 izole kanıt yazıcısında descriptor-relative güvenlik düzeltmesi
- Bulgu: `_exclusive_bytes` önce hedefin tam yolunu `os.open(destination, ...)` ile açıyordu. Önceki symlink kontrollerine rağmen doğrulama ile açma arasında üst dizin değiştirilirse TOCTOU penceresi kalıyordu. Hata durumunda cleanup kimliği de yazma öncesi fstat'tan alındığından kısmi yazım sonrası dosya boyutu/zamanları değişince kendi kısmi dosyasını temizleyemeyebilirdi.
- Düzeltme commit'i: `967977def72e1f184c7e2920d323401f4afb035b`. Yazıcı artık her üst dizini `O_DIRECTORY|O_NOFOLLOW` ve `dir_fd` ile adım adım açıyor, son dosyayı açık parent descriptor'ına göre `O_EXCL|O_NOFOLLOW` ile oluşturuyor; hata cleanup'ı aynı açık dizin descriptor'ında inode/metadata eşleşmesiyle sınırlı.
- Regresyon commit'leri: `6d9624592a93a885fddd5aaccab2cfcc5f8f1d95` kısmi yazım/fsync başarısızlığında temizlik; `32fd75b48d334068efe5687b085daeb86603a0b4` symlink parent üzerinden kaçışın engellenmesi.
- Doğrulama: dosyalar main üzerinde SHA ile tekrar okundu; fakat bu commitler için doğrulanmış Actions/check sonucu henüz yok. Önceki 990 test baseline'ı bu değişiklikleri kapsamaz.
- Kapsam: bu koruma paylaşılan izole kanıt yazıcısını güçlendirir; tüm Python/shell yazma noktalarının merkezi K1 kapısından geçtiğini kanıtlamaz. K1 0/26, K1-03 in_progress, production_ready=false. Üretim dosyalarına dokunulmadı.
- Sonraki adım: yeni test SHA için otomatik CI sonucunu doğrula; sonra 75 mutasyon adayının kalanlarını çağıran zinciri ve gerçek yan etkileriyle sınıflandır.


## K2 devamı — birebir aynı M3U feed oy şişirmesi
- `corroborate_sources` artık feed gövdesi SHA-256 fingerprint'ine göre birebir aynı metni tek bağımsız oy sayar; kaynak etiketleri listelenir ama `source_count` şişmez.
- Kod `3ea2415ba29b08994c892dca2cdcfd23b42bd9e5`, regresyon testi `70433a0079dff063187ce5c094cd5c70d4f828be`; rapor `53abbed82744c7e966d8feaa453ad33627fc8bf5`, hafıza `c852c120ed74e28393495c38f840f74b879a0a39`.
- CI doğrulanmadı; testleri yeşil sayma. Birebir olmayan yeniden biçimlendirilmiş kopyalar hâlâ gerçek kaynak URL/köken kanıtı gerektirir. K2-05/06/07/08 açık; üretim verisine dokunulmadı.


## 23 Ekim 2026 — K5 legacy review batch 09
- Yeni kaynak inceleme belgesi: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_09_2026-10-23.md`, belge commit `4e8cb0bc5fcfb36987fc4f1563a6b922817a279f`.
- Üç workflow ve doğrudan çağırdığı betikler sabit blob SHA'larıyla incelendi: `ibo-yedek-kalite.yml`, `iptv-test.yml`, `k1-protected-write-tests.yml`.
- Kritik bulgu: `iptv_test.py` “salt okunur” workflow altında `CALISANLAR.m3u`, `CALISMAYANLAR.txt` ve `TEST_RAPORU.csv` dosyalarını yazar; workflow bunların hepsini artifact olarak yayımlar. `yedekler/ibo_yedek_kalite_tespit.py` de `CALISANLAR.m3u` içindeki yedek kanal görünen adlarını değiştirerek aynı korunan dosyayı runner çalışma alanında yeniden yazar. Bu workflow'larda git push tanımı görülmedi; fakat kaynak/çıktı ayrımı yok ve “read-only” iddiası davranışla örtüşmüyor.
- `scripts/acceptance_26_92.py` regresyon paketleri geçerse normal çıkış kodu 0 olabilir, `acceptance_complete=false` iken bile; tam kabulü zorunlu kılmak için `--require-full-acceptance` gerekir. Unit test geçişi üretim/cihaz/legacy eşdeğerliği değildir.
- Kümülatif statik kaynak incelemesi 27/92; 65 kalmış. Davranışsal kabul 0/92, runtime güvenlik kabulü 0/26, ana görev kabulü 0/22. K5-19 görev defteri güncellendi; commit `3d810e27c8ceb3d1e2141475377ae0e91035836b`.
- Sonraki iş: yeni depodaki karşılık gelen script ve workflow'ları kontrol et; korunan playlist'in byte/hash değişmezliğini ve çıktıların ayrı dizine yazılmasını doğrulayan izole test ekle. Eski `Madsc55/madsc-tv` deposunu değiştirme veya canlı workflow çalıştırma. Kullanıcı/cihaz onayı olmadan ana playlist'i yayımlama.
- Bu belgeler `[skip ci]` niteliğindedir; bu değişiklikler için yeni test başarısı iddia edilmez. Güncel Actions sonucunu HEAD SHA ile ayrıca eşleştir.


## 23 Ekim 2026 — K1 AST tarayıcısında open() argüman indeksleme hatası
- Yeni kök neden bulgusu: generic `*.open` sınıflandırması `open(path, "w")` çağrısını Path.open gibi yorumlayıp ilk argümanı mode sayabiliyordu; ayrıca `os.open` generic open dalına girerek flags incelemesini atlayabiliyordu. `builtins.open` ve `io.open` da Attribute çağrısı oldukları için yanlış positional mode indeksine düşebiliyordu.
- Düzeltmeler: `ccf5bfea56c9ebbd741d28afa9ed97482c57f513` os.open flags dalını generic open öncesine aldı; `5138e550e9ac2cba2cd7f8eec016a7c018aad999` plain built-in `open()` ile `Path.open()` ayrımını düzeltti. Keyword `flags=` ve dinamik/bitwise flag ifadeleri de review adayı oluyor.
- Testler: `4eacdf0f70d7fb1bf0391a015216bde64e8516c3` builtins/io/os.open regresyonları ekledi. Mevcut plain `open(path, "w")` ve read-only testleri de bu indeksleme ayrımını kontrol ediyor.
- CI/check sonucu henüz doğrulanmadı; yeni testleri geçmiş gibi sayma. K1 0/26, production_ready=false; 75 adayın tamamı kapanmış değil.


## 23 Ekim 2026 — K2 kaynak fingerprint biçim normalizasyonu
- `corroborate_sources` artık feed fingerprint'ini üretmeden önce UTF-8 BOM'u, CRLF/LF farkını, boş satırları ve satırların dış boşluklarını normalize eder. Aynı içeriğin yalnız aktarım biçimi değişti diye bağımsız kaynak oyu sayısı artmaz.
- Kod commitleri: `c1d29af73cbc0a08c82d93d31d8d83b8508986c9` (ilk normalizasyon), `3696f2c0221c1c571ec145b2fa2e97fdf07d9399` (kaçış düzeltmesi). Test commit: `e8eb0b34e60b612dc0d09b096dafa1e0123eaead`.
- Güncel dosya blobları yeniden okundu; canonical fingerprint kodu ve LF/CRLF+BOM regresyon testi depoda mevcut. Bu, yerel test çalıştırması veya CI başarısı değildir. CI combined status yeni test SHA'sı için boş; manuel workflow dispatch yapılmadı.
- Sınır: semantik olarak yeniden yazılmış feed kopyaları veya farklı URL'lerle yayımlanan aynı kaynak hâlâ gerçek kaynak URL/kökeni ile çözülmelidir. K2 gerçek kaynak/lisans, günlük keşif parity ve bağımsız artifact SHA kabulü açık kalır. Üretim dosyaları ve eski depo değişmedi.


## 23 Ekim 2026 — K5 devamı: izole dışa aktarım hata temizliği ve legacy batch 10
- K5 düzeltmesi: `madsc/isolated_playlist_bundle.py` manifest dosyasını yazmaya başlamadan önce rollback listesine kaydediyor. Önceki akışta JSON serialization sırasında kısmi `manifest.json` oluşursa cleanup bu dosyayı silmediğinden `destination.rmdir()` asıl hatayı maskeleyebilirdi. Ek regresyon testi `tests/test_k5_legacy_protected_input_contract.py` içine eklendi: manifest serialize hatasında kısmi paket temizlenmeli, korunan kaynak baytları aynı kalmalı.
- İlk test denemesi fixture'ın kaynak ağacına çok yakın konumlandırılması ve sonra yanlış literal satır sonları nedeniyle başarısız oldu. Test hedefi kaynak dizin ağacının dışına alındı; playlist fixture'ındaki newline'lar düzeltildi. Güncel doğrulama için en son Actions run/HEAD yeniden kontrol edilmeli; bu düzeltmenin geçtiği henüz doğrulanmadı.
- Yeni kaynak inceleme belgesi: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_10_2026-10-23.md`. Eski depodaki üç workflow ve tam blob kimlikleri incelendi; eski depoya hiçbir yazma yapılmadı:
  1. `vod-guncelle.yml` (`78c3b8a...`) + `scripts/vod_guncelle.py` (`94f83bb...`): 15 günlük TVMaze penceresinde tekil gün hataları yakalanıyor ama kısmi veri yine yazılıp commit/push edilebiliyor.
  2. `yedek-geri-yukleme-tatbikat.yml` (`08a38be...`) + `scripts/restore_dry_run.py` (`5985b9f...`): geçici dizine yerel kopya/sha doğrulaması yapıyor; harici restore değil. Erken hata korunan dosya son kontrolünü ve rapor yazımını atlayabilir; `always()` artifact upload ise raporu zorunlu tutuyor.
  3. `publish-iptv-png-logos.yml` (`7b8fa62...`): `logos/` altına PNG üretip yayınlamaya çalışıyor; fakat `tools/protected_write_gate.py` (`11b257e...`) tüm `logos/` yollarını engelliyor. Değişen PNG varsa publisher/gate kapsamı statik olarak çelişiyor.
- K5-19 defterinde statik inceleme 30/92, kalan 62 olarak güncellendi; gerçek davranışsal kabul hâlâ 0/92, K1 runtime güvenlik kabulü 0/26 ve 22 ana görev 0/22. Kaynak incelemesi kabul sayacını artırmaz.
- Korunan IPTV/EPG/favoriler/cihaz/backup/VOD verileri değiştirilmedi; legacy workflow dispatch veya canlı probe yapılmadı. Son test sonuçları, paralel K1-K5 commitleri nedeniyle iptal/yeniden kuyruğa alınabildiğinden, sadece son HEAD üzerindeki tamamlanmış Actions çalıştırması kanıt sayılmalı.


## 23 Ekim 2026 — K2 semantik feed fingerprint'i
- `corroborate_sources` artık ham metin biçimi yerine parse edilmiş kanal envanterinin sıralı imzasını (normalize URL SHA-256, kanal adı, tvg-id, logo ve grup) hash'liyor. Satır sırası, yorum satırları, BOM ve CRLF/LF farkları tek başına bağımsız kaynak oyu üretemez.
- Kod commit: `28a8d963798a85db7639890cb04bec544a3314b5`; test commit: `5c6e087387b731948d98ad699bca33d8521e3cdd`. Yeni test iki kanallı, yorum/sıra/BOM/CRLF farkı olan eşdeğer feed'lerin her aday için tek kaynak sayıldığını kontrol eder.
- Doğrulama sınırı: commit `e8eb0b34e60b612dc0d09b096dafa1e0123eaead` için offline Actions başarılı oldu. Daha yeni çalıştırmalar K5'te `test_manifest_serialization_failure_cleans_partial_bundle_and_preserves_source` hatasıyla başarısız oldu (`Invalid playlist header`) ve eşzamanlı push'lar bazı test çalıştırmalarını iptal etti. En son K2 test commit'i için başarılı CI sonucu henüz yok; testler yerelde çalıştırılmış sayılmaz.
- Bu semantik fingerprint yine de kısmi kopyaları, yeniden yazılmış metadata'yı veya aynı kaynağın farklı alt kümelerini kesin olarak tanımaz. Gerçek kaynak URL/köken/lisans, günlük keşif parity ve bağımsız artifact SHA kanıtı açık. K2 kabul sayaçları değişmedi; üretim playlist/EPG/favoriler/yedekler ve eski depo değişmedi.

## 23 Ekim 2026 — K5 legacy review batch 11 ve K5 export rollback düzeltmesi
- Yeni kaynak inceleme belgesi: docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_11_2026-10-23.md (commit 82178289e12221e84b6c6ca46f2e9bb36a52199a). Eski Madsc55/madsc-tv deposu yalnız okundu.
- Üç ek workflow sabit kaynak SHA'larıyla incelendi: madsc-01-guvenlik.yml (ae91b6c47745fe46659105f96cd28e6aca9d44d9), madsc-02-kesif.yml (f9970a874258c1cbd1c59f73fa427136ff2d53d4), madsc-03-kanal-test.yml (228d53500e99bc9953ab6d535b7809523a1854f0). Rapor: strict 26/26 runtime kanıt kapısı; keşif geçmişi/artifact kökeni ve canlı ağ testlerinin sınırlamaları; IBO aday çıktılarının üretim listesinden ayrı tutulması.
- Statik kaynak inceleme sayacı K5-19 defterinde 33/92 olarak güncellendi, 59 kaldı. Davranışsal kabul 0/92, runtime güvenlik 0/26, ana görevler 0/22; statik inceleme bu sayaçları artırmaz.
- K5 madsc/isolated_playlist_bundle.py manifest yazımı sırasında hata oluşursa kısmi manifest.json dosyasını cleanup listesine ekleyerek özgün hatanın rmdir hatasıyla maskelenmesini önleyecek biçimde düzeltildi (mevcut blob SHA 5fbee3ede24f999443cd12cd39ab713ec31acea7). K5 regresyon testi artık geçerli gerçek satır sonlarıyla kaynak CALISANLAR.m3u baytlarını/hash'ini korumayı ve manifest serileştirme hatasında kısmi bundle'ın temizlenmesini denetliyor.
- İlgili önceki Actions koşuları, daha yeni paralel commitler nedeniyle iptal edildi veya eski SHA'da başarısız oldu; son HEAD üzerinde bu testlerin yeşil olduğuna dair henüz kanıt yok. Güncel Actions'ı son kod/test SHA'sıyla eşleştirerek doğrula; manuel dispatch/rerun yapılmadı.
- Üretim playlist/EPG/favoriler/logo/yedek/cihaz değişikliği yapılmadı; eski depoya yazılmadı; PR #71 merge edilmedi.

## 23 Ekim 2026 — K5 devamı: Batch 12 ve offline CI doğrulaması
- Batch 12 raporu: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_12_2026-10-23.md`. Eski `Madsc55/madsc-tv` deposunda `madsc-04-arsiv-yedek.yml`, `madsc-05-genel-bakim.yml`, `madsc-ana-liste-saglik.yml` ve doğrudan betikleri sabit blob SHA'larıyla okundu; eski depoya yazılmadı.
- Bulgular: arşiv/restore kontrolü Git HEAD'den geçici geri yükleme yapıyor ama harici/tarihsel yedek kanıtı değil; K5 merkezi toplayıcı aynı run/head SHA ve başarılı K1-K4 iş/artifact kökenini doğruluyor ancak son 100 Actions koşusu ve en fazla 20 başarısız koşunun ayrıntısıyla sınırlı; ana liste sağlık regresyonundaki çok satırlı fixture Python kaynak kodunda çift kaçışlı `\\n` kullanıyor ve geçerli satır sonlarını temsil etmiyor. Bu fixture yalnız yeni depoda gerçek satır sonları ve parsed-row count assert'iyle düzeltilmeli.
- Kümülatif statik inceleme: 36/92, 56 kaldı. Davranışsal parity 0/92; runtime güvenlik 0/26; ana görevler 0/22. K5-19 görev defteri güncellendi; batch 12 kaynak incelemesi kabul sayacı artırmaz.
- K5 izole playlist export/manifest regression için Actions run `39868459061`, test edilen HEAD `a0469c34ec9a8642acffdddfbda55dadf9d39aba`, sonuç `success`. Bu yalnız offline regresyon kapısının yeşil olduğudur; gerçek kaynak, IBO cihazı, harici yedek veya 92 workflow davranışsal eşdeğerliği değildir.
- Korunan üretim listeleri/EPG/favoriler/logolar/yedekler ve gerçek cihaz değiştirilmedi; eski depo salt okunur kaldı; PR #71 merge edilmedi. Devir notu güncel; Actions sonuçları yalnız tam SHA eşleşmesiyle kabul edilmeli.


## 23 Ekim 2026 — K2 kaynak bağımsızlığı açıkça doğrulanmamış olarak işaretlendi
- `corroborate_sources` çıktısına `source_independence_verified: false` ve `source_count_semantics: distinct_semantic_feed_inventories_not_verified_origins` eklendi. Farklı semantik envanter sayıları, gerçek ayrı işletmeci/kaynak kökeni kanıtı olarak yorumlanamaz.
- Kod commit `e8e686bfa0f2bf31376bcf58230bc8b5aa212a6d`; regresyon testi commit `9c1c8a594849d730f75d9c050265df74b382b8ec`. K2-08 görev defterine CI ve sınırlar işlendi (`42841d5e`).
- Son bilinen tam offline CI başarısı `39868459061` (commit `a0469c34`); 1016 testlik paket sonraki K3 devir notunda raporlandı. Yeni açık `source_independence_verified` regresyonu için workflow `39868653542`, SHA `9c1c8a594849d730f75d9c050265df74b382b8ec` üzerinde `success` ile tamamlandı.
- K2-05 gerçek kaynak URL/işletmeci/lisans mutabakatı, K2-06 günlük keşif/tetik eşdeğerliği ve K2-07 bağımsız gerçek artifact SHA kanıtı açık. Gerçek kaynak verisi olmadan kabul kapatılmadı; üretim verisi değiştirilmedi.


## 23 Ekim 2026 — K3 kaynak M3U içe aktarımında yinelenen metadata öznitelikleri
- `madsc/source_import.py` artık EXTINF metadata öznitelik adlarını büyük/küçük harf duyarsız karşılaştırıyor ve yinelenen özniteliklerde (ör. iki `tvg-id` veya `tvg-id`/`TVG-ID`) belirsiz EPG/logo eşleşmesi üretmek yerine `ValueError` ile reddediyor. Regex kaçışları ayrıca kontrol edilip düzeltildi.
- Regresyon testi `tests/test_source_import.py` içinde tam ve büyük/küçük harf farkı olan duplicate `tvg-id` ile duplicate `group-title` durumlarını kapsıyor. Test fixture satır sonları doğrulandı.
- Entegre offline regression workflow `39868653542` SHA `9c1c8a594849d730f75d9c050265df74b382b8ec` için `success` ile tamamlandı. Bu çalışma yeni duplicate metadata testini içerir; ayrı K3 regex commit çalışması `39868610849` de `success` oldu.
- Bu değişiklik aday içe aktarım doğrulamasını sıkılaştırır; kaynak M3U değiştirilmedi, gerçek yayın URL'leri denenmedi ve kanal canlı doğrulandı olarak işaretlenmedi.


## K2 CI sonuç güncellemesi — 23 Ekim 2026
- Güncelleme: `source_independence_verified` korumasını içeren kod/test commit'i `9c1c8a594849d730f75d9c050265df74b382b8ec` için GitHub Actions run `39868653542` başarıyla tamamlandı: https://github.com/Madsc55/Madsc55-Tv/actions/runs/39868653542
- Böylece bu regresyon için önceki “CI bekleniyor” notu geçersizdir. Görev defterine başarılı koşum kanıtı eklendi. Bu başarı gerçek kaynak/lisans kanıtı veya günlük tetik eşdeğerliği anlamına gelmez; K2-05/06/07 ve gerçek kaynak davranış kabulü açık kalır.


## 23 Ekim 2026 — K1 lambda guard kapsamı: iç içe ziyaretçi hatası düzeltildi
- Ek incelemede bulundu: `_Scanner.visit_Lambda` lambda gövdesini ayrı kapsamda işlese de `_ScopeCalls` üst fonksiyonun guard envanterini toplarken varsayılan NodeVisitor davranışı lambda gövdesine giriyordu. Böylece ertelenmiş lambda içindeki guard, dış fonksiyonun yazma çağrısına yanlışlıkla iliştirilebiliyordu; yeni regresyon testi bu vakayı yakalamak üzere eklenmişti.
- Düzeltme: `_ScopeCalls.visit_Lambda` artık lambda gövdesini dış kapsam için ziyaret etmiyor. Yinelenen visitor tanımı da kaldırıldı.
- Kod commitleri: `9bf7f9926ddab13c3bebc4ca108e8d2908ef8a6b`, temizlik `bbb975e650456ae29d89d5c66dbc4ce51e7c2f6a`. İlgili test `3c3610e35eef121b6e876eccd62c50754fd7ee6e`.
- Dosyalar GitHub'da tekrar okundu; bu son düzeltme için Actions/check sonucu doğrulanmadı ve test çalıştırılmış sayılmıyor. K1 kabulü 0/26, üretim hazır değil. Üretim dosyaları değişmedi.

## 23 Ekim 2026 — K5 devamı: Batch 13–15
- Raporlar: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_13_2026-10-23.md`, `...BATCH_14...`, `...BATCH_15...`.
- Batch 13: birleşik keşif workflow'u `contents: write` + `actions: write` ile raporları main'e gönderiyor ve ardından eski üç aşamalı workflow'u dispatch edebiliyor; cuma ana liste/EPG raporu sorunlarda uyarı verir ama sağlık kabul kapısı değildir; dokümantasyon kontrolü yalnız sabit string smoke testidir.
- Batch 14: geniş kaynak taraması yine geniş yazma izinleriyle rapor commit/push ve sonrasında workflow dispatch yapabiliyor; hızlı ön kontrol static-only ve cutover'ı reddediyor; `madsc-ibo-3-5281.yml` gerçek kanal ayırma yapmayan placeholder.
- Batch 15: üç IBO yedek sınıflandırma script'i `CALISANLAR.m3u` dosyasını runner çalışma alanında yeniden yazıyor. Protected-write gate tüm `.m3u` değişikliklerini reddettiği için bu staged main-list değişiklikleri kaynakta fail-closed bloklanmalı. Sınıflandırma kullanıcı bildirimi; doğrulanmış playback/kimlik değil. Üretim değişikliği veya workflow dispatch yapılmadı.
- Kümülatif K5 statik kaynak incelemesi 45/92, 47 kaldı; behavioral parity 0/92, runtime security 0/26, ana görev 0/22. Statik incelemeler kabul sayacı artırmaz. K5 export regression Actions run `39868459061`, SHA `a0469c34ec9a8642acffdddfbda55dadf9d39aba`, `success` (yalnız offline suite).
- Korunan playlist/EPG/favoriler/logolar/yedekler/cihazlar değiştirilmedi; eski `Madsc55/madsc-tv` deposu salt okunur; PR #71 merge edilmedi. Sonraki adım: Batch 16'dan üç sabit kaynak workflow incelemesi daha ve yeni depoda isolated archive regression fixture'ları; her yeni CI sonucunu tam SHA ile doğrula.


## 23 Ekim 2026 — K1 AST disk-etkisi envanteri genişletildi
- `os.open` icin callable/conditional/unary ve taninmayan flags ifadeleri artik elle inceleme adayi; kod `ab8d2d28`, regresyon `f510ba4c`.
- `os.fdopen` yazma modlari ve `tempfile.NamedTemporaryFile/TemporaryFile/mkstemp/mkdtemp/TemporaryDirectory` dosya/dizin olusturmalari artik envanterde; kod `946ab465`, regresyon `3e3cc524`.
- Bu statik aday tespiti otomatik runtime enforcement degildir. Onceki 75 aday sayisi eski tarayici kapsamindan geldigi icin yeni sayim yapilmadan guncel toplam sayilmaz. Tum adaylar manuel disposition bekler.
- Yeni commitler GitHub main dosyalarinda dogrulandi; bu SHA'lar icin offline CI basarisi henuz dogrulanmadi. 26 runtime kural 0/26, 22 gorev 0/22, uretim kabul false. Korunan playlist, EPG, yedekler degistirilmedi.


## 23 Ekim 2026 — K2 metadata ve kaynak liste sınırı sertleştirmesi
- `madsc/discovery_batch.py::corroborate_sources` `known_urls` girdisini en fazla 20.000 öğeyle sınırlar (`8d116818`). Çok büyük giriş hatayla reddedilir.
- `parse_m3u` kimlik alanları (`tvg-id`, `tvg-logo`, `group-title`) yanlış veya tırnaksız yazıldığında sessizce metadata düşürmez: `invalid_metadata_attribute` üretir ve ilişkili URL'yi aday kataloğuna almaz. Kod `a5d0d3b4`, kaçış düzeltmesi `f82e0cb9`.
- İki regresyon testi `38d8209adce32f8d2afa964a6a32ed77c35959b8` commit'inde. Bu commitin doğrudan Actions koşusu iptal edildi; ancak onun iki commit ilerideki soyundan gelen `205ad1bf6f094a36600a0ad5872f228fc74fe850` commit'i için Actions `39869009399` başarıyla tamamlandı. GitHub compare sonucu `ahead`, ahead_by=2, behind_by=0 olarak doğrulandı.
- K2-08 görev defteri yeni kanıtla güncellendi; tamamlandı statüsüne geçirilmedi. K2-05 gerçek kaynak/lisans, K2-06 günlük tetik davranışsal eşdeğerlik, K2-07 bağımsız gerçek artifact köken/SHA kanıtı hâlâ açık. Korunan üretim dosyalarına, eski depoya ve IBO cihazına dokunulmadı.


## 23 Ekim 2026 — K2 hatalı EXTINF satırı sonrası toparlanma
- `madsc/discovery_batch.py` içindeki `parse_m3u`, kanal adı bulunmayan, boş başlıklı veya metadata tırnakları dengesiz olan EXTINF satırından sonra ilişkili URL'yi tüketerek gereksiz `orphan_url` tanısını önlüyor; sonraki geçerli kanal korunuyor. Kod `aa6cba2913d5a1c5ad368a4a7c6c76d10197149a`.
- Regresyon testi `1d222cde478962ccef73ec361834660dfc1af87f`. Tam bu commit'in Actions çalıştırması `39869955026` eşzamanlı push nedeniyle `cancelled`; başarılı test sonucu olarak sayma. Daha yeni soy commitlerin CI sonucu ayrıca kontrol edilmeli.
- K2-08 görev defterinde `in_progress` kaldı. Gerçek kaynak/lisans, günlük keşif eşdeğerliği ve bağımsız artifact SHA kabulü açık; üretim playlist/EPG/favoriler/yedekler ve eski depo değiştirilmedi.


## 23 Ekim 2026 — K2 UTF-8 giriş doğrulaması; IBO cihaz testi en son
- Kullanıcı kararı: IBO Player Pro cihaz doğrulaması **en sona bırakılacak**. Gerçek cihaz denemesini kullanıcı yapıp sonucu bildirecek; o zamana kadar `ibo_device_verified=false` ve cihaz kabulü açık kalır.
- Önceki K2 `orphan_url` regresyon düzeltmesi, daha sonraki commit `21410cc6101ca5fad8b4500a74e9c955f23e9ecd` için başarılı Actions `39870201168` ile doğrulandı.
- K2 `parse_m3u`, metin veya kaynak etiketindeki Unicode surrogate karakterleri UTF-8 olarak kodlanamayacağı için girişte `ValueError` ile reddediyor (`6ac6eef780e14559854740539d96cdd8dfd39912`). `parse_m3u`, `corroborate_sources` ve `build_m3u8_preview` yolları için regresyon testi eklendi (`a794aeca142581eb5a70db90ec4ae51d5a1b63de`). Bu yeni testin CI sonucu ilk kontrolde bekliyordu (`39870351806`), başarı iddia edilmez.
- Gerçek kaynak/lisans, günlük keşif eşdeğerliği, gerçek artifact köken/SHA ve K2-08 gerçek kaynak davranış kabulü açık. Korunan üretim verisi değiştirilmedi.


## 23 Ekim 2026 — K4 düşük seviyeli güvenli dosya açma ve cihaz doğrulama sırası
- Kullanıcı talimatı: **IBO Player Pro üzerindeki gerçek cihaz doğrulaması en son yapılacak; cihazı kullanıcı bizzat deneyip sonucu bildirecek.** K1–K5 kod, test, kaynak ve yedekleme eksikleri önce tamamlanmalı; cihaz testinin sonucu varsayılmamalı ve hiçbir otomatik cihaz doğrulaması tetiklenmemeli.
- `madsc/backup.py` içinde `_open_relative_file_nofollow` kaynak dosya yol bileşenlerini artık descriptor açmadan önce denetliyor. Boş, `.`, `..`, slash ve tek backslash içeren bileşenler reddediliyor. Nihai düzeltme commit `7df85585bd152e07fef2703a2c6497414ae7e594`.
- `tests/test_backup_manifest_hardening.py` içine doğrudan düşük seviyeli fonksiyonun traversal ve backslash girdilerini reddetmesini doğrulayan test eklendi. Nihai test commit `0524a7d0bca2a79da83d5abd47bb136169c9a7df`.
- Son gözlem: ilgili Actions `39870389256` henüz pending; yeni test için başarılı CI kanıtı bekleniyor. Gerçek harici yedek, bağımsız harici restore ve ayın 1/15 zamanlayıcı kabulü hâlâ açık. Korunan IPTV, EPG, favori, cihaz ve üretim yedek dosyaları değiştirilmedi.


## 23 Ekim 2026 — K2 kaynak etiketleri denetimi; cihaz doğrulaması ertelendi
- Önceki Unicode surrogate regresyonu (`a794aeca`) daha sonraki `0524a7d0bca2a79da83d5abd47bb136169c9a7df` commit'inde başarılı GitHub Actions `39870389256` ile kapsandı; GitHub compare `ahead=5`, `behind=0`.
- `parse_m3u` kaynak köken etiketlerindeki ASCII kontrol karakterlerini (satır sonu, tab, NUL, DEL) reddediyor (`a9e193bd2ea8de8d8f0ce0be937042dbcce894b4`). Bu, rapor ve köken kayıtlarının kontrol karakterleriyle kirletilmesini engeller. Parser, kaynak mutabakatı ve önizleme için regresyon `e03b92d13a41a3e1d48e06c73981c1e7299473e1`; yeni CI sonucu henüz doğrulanmadı.
- K2-08 görev defterine kanıt işlendi, kabul kapatılmadı. Gerçek kaynak/lisans, günlük keşif eşdeğerliği ve gerçek artifact SHA kökeni hâlâ açık. IBO Player Pro cihaz testini en sonda kullanıcı yapacak; cihaz doğrulandı iddiası yok. Korunan üretim verisine dokunulmadı.


## 23 Ekim 2026 — K2 kaynak etiketinin URL mutabakatından önce doğrulanması
- Kaynak etiketindeki kontrol karakterleri ve UTF-8 surrogate kod noktaları `corroborate_sources` girişinde bilinen URL normalizasyonundan önce reddedilir. Gereksiz çift M3U ayrıştırması kaldırıldı. Son kod `eb4b3fc841852d09ede8599de2984985f710167d`; regresyon `bd0aab8bfb24596d20f9716cb7cbefcd1ce85387`.
- Önceki kaynak etiketi regresyonunun birebir SHA `e03b92d1` Actions `39870604494` sonucu `success`. Yeni `bd0aab8b` koşusu `39870812620` eşzamanlı push nedeniyle `cancelled`; yeni regresyon için başarılı CI henüz teyit edilmedi.
- K2-08 in_progress; K2-05/06/07 gerçek kaynak/lisans, günlük keşif eşdeğerliği ve gerçek artifact köken kanıtı açık. Cihaz doğrulaması en sona bırakıldı; IBO Player Pro denemesini kullanıcı yapacak. Üretim verisine dokunulmadı.


## 23 Ekim 2026 — K2 kaynak etiketi uzunluk sınırı
- `parse_m3u`, `corroborate_sources`, `build_m3u8_preview` kaynak köken etiketlerini 256 karakterle sınırlar; 257 ve üzeri reddedilir. Kod `b79ff7a8e6855911104ee5b38388a592c64b9e7f`, sınır regresyonu `91f32d6ebd7540c1bce2fb07628db6648299261b`.
- Önceki etiket doğrulama sırası regresyonu `bd0aab8b` daha sonraki `0e2d5e6844f93f4e04970f9992018d00ad593eaf` commit'i için başarılı Actions `39870824796` ile doğrulandı (compare ahead=3, behind=0). Yeni 256 karakter sınır testinin CI sonucu ilk kontrolde bekliyordu (`39870982558`); doğrulanmadan başarılı sayma.
- K2-08 in_progress; K2-05/06/07 gerçek kaynak/lisans, günlük keşif eşdeğerliği ve artifact köken kanıtı açık. Kullanıcı IBO Player Pro cihaz testini en son kendisi yapacak. Korunan üretim dosyaları değişmedi.


## 23 Ekim 2026 — K2 aynalanmış feed kaynak oyları
- `corroborate_sources` semantik feed fingerprint'i `tvg-id` bulunan kanallarda URL SHA-256 + tvg-id kimliğini kullanır; kanal adı, logo veya grup değişimi kopya feed'e ikinci oy vermez. `tvg-id` bulunmayan kanallarda isim+grup kimliği korunur. Kod `53f5850e1678ec6e2dcf639d15a22365478f9145`; iki regresyon `3cebc66d1d48b53ce7b2f9cd86b6f8ebb6bfe5d9`.
- Önceki 256 karakter kaynak etiketi regresyonu `91f32d6e`, sonraki `41a61d61b92f0e6c043abd969caeb01100df4b1b` commit'i için başarılı Actions `39871021673` ile kapsandı (compare ahead=7, behind=0). Yeni fingerprint regresyonu Actions `39871248968` ilk kontrolde bekliyordu; sonuç doğrulanmadan kabul kapatılmayacak.
- `source_independence_verified=false`; kaynak sayısı gerçek bağımsız yayıncı/lisans kanıtı değildir. K2-05/06/07/08 açık. IBO Player Pro cihaz testini en son kullanıcı yapacak; üretim dosyalarına dokunulmadı.


## 23 Ekim 2026 — K1–K5 kanıt denetimi TOCTOU/hardlink sertleştirmesi ve güncel tam regresyon
- Kod commitleri: `2047d2c51a489e7bace618d6ea5d9910f93e2a00` (bounded descriptor tabanlı okuma) ve `ef076219cb9eecc9a084d94f19c115c78c5fd53a` (hardlink ve okuma sırasında inode değiştirme regresyonları). `five_stage_evidence_audit` artık `O_NOFOLLOW|O_NONBLOCK`, regular-file, tek-link ve 2 MiB sınırını uygular; okuma öncesi/sonrası descriptor metadata'sını ve güncel pathname inode'unu eşleştirmeden JSON'u geçerli saymaz.
- Güncel temiz checkout kaynak SHA'sı `2c0a3ebc2d7d36572e98e68792e2bdff2f82db7d`. İlk tam kapı denemesi yoğun eşzamanlı yükte kendi 180 saniyelik sınırına ulaştı; bu başarı sayılmadı. Aynı checkout'ta doğrudan unittest keşfi **1058/1058** ve hemen ardından `python -m madsc.offline_gate` **1058/1058 + beş izole K kapısı + kurulum/contract/rapor round-trip** ile başarılı oldu. Hedefli son paket 65/65 başarılıydı; `git diff --check` temizdi.
- Güncel K1 salt-okunur callsite envanteri 99 Python dosyasında 141 aday gösteriyor. Bu yalnız statik inceleme kuyruğudur; tüm satırlar `review_required=true`, runtime güvenlik kabulü değildir.
- Kabul değişmedi: davranışsal parity **0/92**, runtime güvenlik **0/26**, ana görev **0/22**. Canlı probing, cihaz testi, üretim yazması, korunan playlist/EPG/favori/logo/yedek/arşiv değişikliği, eski depo yazısı, merge veya PR #71 işlemi yapılmadı; Actions elle başlatılmadı.
- Sıradaki somut yerel iş: 141 adayın gerçek dosya etkisi olmayan string `.replace` ve salt-okunur descriptor false-positive'larını kaynak-bağlı disposition ile ayır; gerçek writer ve subprocess satırlarını K1 guard/call-chain kanıtıyla fail-closed bırak. Gerçek aynı-input bağımsız legacy/replacement run+artifact çiftleri gelmeden 92 kabulünü artırma.


## 23 Ekim 2026 — K2 bilinen URL girdisi sınırı
- `corroborate_sources` bilinen URL kümesindeki 8192 karakterden uzun veya UTF-8 surrogate içeren adresleri normalizasyondan önce reddeder. Kod `ea305e1650a19fd592064f71d4b3cbdfd94aa670`, regresyon `a11999c7bc6888e6ba46c86803cb3154f4182300`. Normal bilinen URL dışlama davranışı da test edilir.
- Önceki aynalanmış feed fingerprint testi `3cebc66d`, sonraki `a22684d4a259ccc986c2b4baa8fcb92ecbf02b10` commit'inde başarılı Actions `39871279885` ile kapsandı (compare ahead=2, behind=0). Yeni URL sınırı testinin CI sonucu ilk kontrolde bekliyordu (`39871566283`), doğrulanmadan başarılı denemez.
- K2-05/06/07/08 açık. IBO Player Pro cihaz doğrulaması en sonda kullanıcı tarafından yapılacak; üretim playlist/EPG/favori/yedekler değiştirilmedi.


## 23 Ekim 2026 — K2 bilinen URL kontrol karakterleri
- `corroborate_sources` bilinen URL kümesinde satır sonu, tab, NUL ve DEL gibi ASCII kontrol karakterlerini normalizasyondan önce reddeder. Kod `d64a03a07fb03e6af091f2929b7655dae4f9dfed`, regresyon `096eb6038d8cd6fa3fa3f0a75260c2bfab8c631a`.
- Önceki bilinen URL uzunluk/Unicode regresyonu `a11999c7`, sonraki `c59bd4bf6f86ed0acdf3dc39aeebfbbfebc1de7f` commit'inde başarılı Actions `39871569940` ile kapsandı (compare ahead=1, behind=0). Yeni kontrol karakteri testinin Actions `39871799412` sonucu ilk kontrolde bekliyordu; doğrulanmadan kabul kapatılmaz.
- K2-05/06/07/08 açık; gerçek kaynak/lisans, günlük keşif ve artifact köken kanıtı bekliyor. IBO Player Pro cihaz testini en son kullanıcı yapacak; üretim playlist, EPG, favori, yedekler değiştirilmedi.


## 23 Ekim 2026 — K2 bilinen kanalların kaynak oyu üretmesini önleme
- `corroborate_sources` feed fingerprint'i artık yalnızca `known_urls` dışındaki yeni kanal envanterinden hesaplar. Aynı yeni kanal, farklı eski/bilinen kanalları barındıran aynalanmış feed'lerde iki bağımsız oy almaz. Kod `f4ef8312ff713d32f729075260d7635d81823f4d`, regresyon `1100410d83c5f47e5947a08fce480705463a1bee`.
- Önceki kontrol karakteri regresyonu `096eb603` tam SHA için Actions `39871799412` sonucu `success`. Yeni bilinen-kanal kaynak oyu regresyonu Actions `39872022686` ilk kontrolde `pending`, başarılı CI henüz doğrulanmadı.
- Kaynak envanteri oyları gerçek yayıncı bağımsızlığını/lisansı kanıtlamaz (`source_independence_verified=false`). K2-05/06/07/08 açık. IBO Player Pro cihaz testini en son kullanıcı yapacak; üretim playlist/EPG/favori/yedekleri değiştirilmedi.


## 23 Ekim 2026 — K2 sohbet devri / yeni sohbet için son kayıt
- Doğru depo `Madsc55/Madsc55-Tv`, dal `main`; bu sohbet K2 sorumluluğundadır. K1–K5 paralel commit atıyor; CI push iptalleri ve 409 SHA çatışmaları görülebilir. Üretim playlist, EPG, favoriler, yedekler, arşivler, eski repo/PR değiştirilmemeli.
- K2: bilinen URL uzunluk/surrogate sınırı `ea305e16`, testi `a11999c7`, başarılı descendant CI `39871569940`; bilinen URL kontrol karakteri engeli `d64a03a0`, testi `096eb603`, başarılı exact CI `39871799412`.
- K2: bilinen kanalların kaynak fingerprint oylarını şişirmesini engelleyen kod `f4ef8312ff713d32f729075260d7635d81823f4d`, regresyon `1100410d83c5f47e5947a08fce480705463a1bee`. İlk Actions `39872022686` iptal edildi; en yeni başarılı descendant CI `39872866083`, SHA `07af92ae93c579eaf9f7ce68c969791c9b4b4172` (K1 düzeltmesi `b8d59ef8` sonrasındaki 2 commit, compare ahead=2/behind=0). Başarı yalnızca bu CI kapsamı için geçerli.
- K5: 1086 testli CI'da manifest byte integrity mismatch yakalandı; `madsc/isolated_ibo_archive_export.py` tek-sefer JSON byte serialization `74779167a5cafb8a5727ce51f5e37b5241b1dabc`, test `ee9873307fe2a57a4fe70cd865b8e7b143d2cbd5`. Ardından 1089 testte K1 write callsite audit `Path.chmod` adlandırma hatası bulundu, `madsc/write_callsite_audit.py` kod `b8d59ef8742646e870c3073d3944a00b9cea23fa` ile düzeltildi. Son CI `39872866083` başarılı descendant.
- Açık K2 görevleri: K2-05 gerçek kaynak ve lisans kanıtları; K2-06 günlük keşif / eski workflow davranışsal eşdeğerliği; K2-07 geçmiş artifact SHA-256 köken kanıtları; K2-08 gerçek kaynaklarla alternatif/duplicate kabulü. Gerçek yayıncı bağımsızlığı doğrulanmadı (`source_independence_verified=false`). Hiçbirini kanıtsız kapatma.
- **IBO Player Pro cihaz doğrulaması kesinlikle en sona bırakıldı**. Kullanıcı cihazda test edip sonucu bildirecek; cihazın doğrulandığı iddia edilmeyecek.
- Yeni sohbette önce `main` son commit ve Actions sonuçlarını kontrol et, başarısızlık varsa logları inceleyip düzelt, K2 açık işleri tekrarsız sürdür; paralel ajanların commit'lerini ezme.


## 23 Ekim 2026 — Yeni sohbete devir: K4 güvenlik çalışmaları ve CI
- Kullanıcı kararı: **IBO Player Pro cihaz doğrulaması EN SON**; kullanıcı gerçek cihazda deneyecek ve sonucu bildirecek.
- Doğru yazılabilir depo `Madsc55/Madsc55-Tv`, dal `main`. K1–K5 paralel commit gönderiyor; her yazma öncesi güncel SHA al, 409'da yeniden oku.
- Bu sohbette K4 kod/test çiftleri: manifest girdi sayısı `49122e9` / `1394bcf`; doğrulama yol uzunluğu `1b40b3d` / `0e80fb7`; snapshot kaynak sınırları `1fdd720` / `3979d18`; sahte mode `98080a0` / `2669060`; tam str mode türü `57d5080` / `791d87c`; kontrol karakteri/surrogate manifest yolu `192ccc0` / `a93c60e`; surrogate kaynak yolu `74ac750` / `2f2d021`; kanonik entry/path türü `a1df955` / `5407bda`. Ayrıntılı kabul dosyası `docs/K4_EXTERNAL_BACKUP_RESTORE_ACCEPTANCE_2026-10-23.md`.
- Son kontrol: Actions `39872866083` **success**; eski `39872580939` **failure** (K1 Path.chmod/Path.lchmod adlandırması), `39872833113` **failure** (K5 archive manifest bozuk bayt testi). Bazı bireysel Actions paralel push yüzünden **cancelled**. Yeni sohbette en güncel Actions ve job loglarını yeniden doğrula.
- Açık kabul: gerçek harici yedekleme ve bağımsız restore kanıtı yok; üretim kabulü ve cihaz testi tamamlanmadı. Korunan IPTV/playlist, XMLTV/EPG, favori, logo, cihaz, yedek ve arşiv dosyalarına dokunma; canlı probe veya üretim yazısı yapma.
- Devam sırası: güncel HEAD/CI kontrolü, başarısız logların incelenmesi, diğer sohbetlerin işini tekrarlamadan K4 somut hata+regresyon düzeltmesi, CI kanıtı; cihaz doğrulaması en son.


## 23 Ekim 2026 — K1 kaynak-bağlı yazma çağrısı disposition v2
- K1 salt-okunur AST envanteri v2'ye geçirildi. Her aday ve kapatılan false-positive artık kaynak dosya SHA-256'sı ile tam çağrı ifadesi SHA-256'sını taşır; kaynak değişirse önceki disposition sessizce devralınamaz.
- Açıkça çözümlenebilen `os.open` bayrakları için yalnız `O_RDONLY/O_PATH` ve salt-okunur modifier birleşimleri `proven_read_only_descriptor` sayılır. Dinamik/değişken/tanınmayan bayraklar ve yazma bayrakları fail-closed olarak aday kalır. String `.replace` yalnız literal-string köklü çağrı zincirinde kapatılır; bilinmeyen nesnelerin `strip/lower/replace` yöntemleri yazma adayı olarak kalır.
- İlgili commitler: kod `9bb82d897959412c550307ffdaf9c95646db2431`, şema kapısı `b353f3919ef374f3a33997b5b42bc701ee7c5a1a`, ilk regresyon `57cc1d0ed05302bc5acdb7595bb88523bfb2ffa6`; fail-closed receiver sertleştirmesi `60f984d` / `9078e18`, son test uyarlaması `0d32b48b7f15c53050f2c5c85412eebffc34c533`.
- Temiz güncel kaynakta hedefli K1 paketi 32/32; tam `python -m madsc.offline_gate` 1120/1120 test, beş izole K kapısı, kurulum/contract/rapor round-trip ve pinned 92 kapsamıyla başarılı. Güncel tarama 100 Python dosyasında 142 inceleme adayı; ayrıca 5 kanıtlı salt-okunur descriptor ve 2 literal-string dönüşümü kaynak-hash-bağlı non-write disposition'dır.
- İlk tam denemede geçersiz HLS test satır sonları nedeniyle 3 K3 testi ve v1/v2 şema uyuşmazlığı nedeniyle 2 offline-gate testi başarısız oldu; HLS fixture düzeltmesi `17fef31`, şema düzeltmesi ve sonraki test uyarlamalarıyla son temiz koşu yeşil. Başarısız ilk koşu kabul kanıtı sayılmadı.
- Kabul sayaçları değişmedi: davranışsal parity 0/92, runtime güvenlik 0/26, ana görev 0/22. Fixture/statik sınıflandırma üretim kabulü değildir. Canlı probe, cihaz testi, üretim yazısı, korunan playlist/EPG/favori/logo/yedek/arşiv değişikliği, eski depo yazısı, merge veya PR #71 işlemi yapılmadı; Actions elle başlatılmadı.
- Sıradaki somut iş: değişken bayraklı salt-okunur `os.open` çağrılarını aynı lexical scope içindeki sabit atamalara kaynak-bağlı ve fail-closed çözümle; ardından kalan gerçek writer/subprocess satırlarında K1 guard dominasyonu ve call-chain kanıtını tek tek kapat. Gerçek aynı-input bağımsız execution/artifact çiftleri olmadan 92 kabulünü artırma.


### Aynı paket için son HEAD doğrulama güncellemesi
- Yukarıdaki 1120-test koşusundan sonra eşzamanlı K2/K4/K5 commitleri main'e girdi. En son temiz checkout SHA `5b8d0fb515df8865047a92cdfc12cd856f7c6595` üzerinde tam offline kapı yeniden çalıştırıldı: **1123/1123 test**, beş izole K kapısı, write-callsite v2, kurulum/contract/rapor round-trip ve pinned 92 kapsamı başarılı. Tarama 100 dosya / 142 açık aday / 7 non-write disposition olarak aynı kaldı. Bu da üretim veya 92/26/22 kabulü değildir.


## 23 Ekim 2026 — K1 yerel `os.open` bayrak çözümleme ve yapısal guard baskınlığı
- Başlangıç main SHA'sı `dd1b8fd862762f1e04c17d067814e84448639249`; son kod/test SHA'sı `08aa6447dae79cfacca058f534bcb0cbd912a1c4`. Yerel tek-atamalı ve çağrıdan önce tanımlı salt-okunur `os.open` bayrakları kaynak-bağlı çözümleniyor (`8bda1064e806948158f3fa890ba39498948513d1`); parametre, yeniden/koşullu atama, import/pattern capture, `global`/`nonlocal`, closure mutasyonu ve `exec` bulunan kapsamlar fail-closed aday kalıyor (`c2ada47861fcd2c06abd8c58c34dac9f252e1e3d`).
- Doğrudan ifade deyimi olan koşulsuz K1 guard'ları, aynı lexical gövdedeki daha sonraki çağrılar için yapısal baskınlık olarak kaydediliyor (`97ecba41f2bc89462f40dd4e88533e06b3c00ce3`); `try`/koşul/döngü içindeki guard'lar bu kanıtı üretmiyor. Regresyonlar `08aa6447dae79cfacca058f534bcb0cbd912a1c4`. Bu alan çağrı zinciri veya callee sözleşmesi kanıtı değildir ve tüm satırlar `review_required=true` kalır.
- Uzak main'in temiz checkout'unda `python -m madsc.offline_gate`: **1151/1151 test**, beş izole K kapısı ve tüm offline kapılar başarılı; başarısız test yok. Tarama 100 dosya / 142 aday / 9 kaynak-bağlı non-write disposition; 75 adayda doğrudan guard baskınlığı doğrulandı.
- Kabul değişmedi: davranışsal parity **0/92**, runtime güvenlik **0/26**, ana görev **0/22**. Fixture/statik baskınlık kabul kanıtı değildir. Korunan üretim verisi, eski depo, PR #71, cihaz, canlı probe ve üretim yazısı değiştirilmedi; Actions elle başlatılmadı.
- Açık işler/engel: kalan gerçek writer ve subprocess adaylarının çağıran zinciri ile callee guard sözleşmesini kaynak-hash-bağlı kapat; gerçek aynı-input ve bağımsız execution/artifact çiftleri olmadan 92 parity kabulünü artırma. Gerçek dış kanıt, harici restore ve en sona bırakılan kullanıcı cihaz testi bekleniyor.


## 23 Ekim 2026 — K1 artifact yazıcısı ve subprocess etki envanteri
- `artifact_transport` içindeki produce/consume JSON yazmaları tek `_write_json_exclusive` yardımcısında toplandı. Yardımcı her gerçek `open("x")`/`write` öncesinde koşulsuz `enforce_write_paths` ve `enforce_local_output_path` çalıştırıyor; mevcut hedefi değiştirmiyor ve korunan ata dizinde fail-closed duruyor. Kod `1d347f79173870b2313b6ec9ce9ed466569418ae`; yapısal baskınlık testi `6aee0d5a70a72ac19fa0087fb08821700d7435da`, davranış testi `6cf0c3932bf521dbafff18787cec4ba034a2465b`.
- İlk davranış testi tekrar yazmada `FileExistsError` bekledi; K1 preflight daha erken `PermissionError` verdiği için bu deneme başarısızdı ve başarı sayılmadı. Test fail-closed sözleşmeye göre düzeltildi.
- Altı subprocess adayı için `shell` durumu, literal argv ve executable sözdizimi kaynak/callsite SHA bağıyla kaydediliyor (`039826136d99fa9bf4a7d44b6b7661d1566209da`, test `ff946c3b35f2efde1972dac64f09663e2d98e14e`). Altısında shell-disabled sözdizimi var; komut etkisi kanıtı **0/6**, dolayısıyla hiçbir aday kapatılmadı ve tümü `review_required=true`.
- Temiz uzak main `ff946c3b35f2efde1972dac64f09663e2d98e14e` üzerinde tam offline kapı: **1154/1154 test**, beş izole K kapısı ve bütün offline kapılar başarılı. Envanter 100 dosya / 140 aday / 9 non-write disposition; doğrudan guard baskınlığı 77 aday. Kabul 0/92, 0/26, 0/22 olarak kaldı.
- Sıradaki somut iş: subprocess komutlarını ve gerçek writer helper'larını tek tek kaynak-bağlı etki/caller sözleşmesiyle incelemek; shell-disabled bilgisini read-only kanıtı saymamak. Gerçek bağımsız run/artifact, harici restore ve kullanıcı cihaz kanıtı bekleniyor. Korunan üretim verisi, eski depo, PR #71 ve Actions tetiklenmedi.


## 23 Ekim 2026 — K1 subprocess argv kökeni ve yerel writer çağıranları
- Tek ve baskın yerel argv atamaları fail-closed binding kurallarıyla subprocess çağrısına bağlandı (`5b79da4e60e89c098bf5416e2162ab53f5648467`, test `d1707ae589d56a36a600bf4a47ef84bcce28cc93`). Altı adayın beşinde executable sözdizimi kaynak-bağlı çözüldü: iki `curl`, bir `ffprobe`, iki `sys.executable`; caller-controlled `parity_process.argv` çözümsüz kaldı. İlk hedefli test karışık argv'nin ilk literal executable'ını çıkaramayan hatayı yakaladı; düzeltilmeden başarı sayılmadı.
- Top-level, yeniden bağlanmamış yerel writer helper'ları için gözlenen doğrudan çağıranlar, çağrı SHA'sı ve çağrı noktasındaki guard baskınlığı envantere eklendi (`1bc73b2abd6b0f9dc20d3d4636e0f7e6cd23dfdd`, test `c16f25d230b411ac100411a113a125b0b8f6b3fa`). Rebind, dinamik `exec` ve belirsiz adlar çağıran kanıtı üretmiyor.
- Temiz uzak main `c16f25d230b411ac100411a113a125b0b8f6b3fa` doğrulaması: **1157/1157 test**, beş izole K kapısı ve bütün offline kapılar başarılı; 140 adayın 104'ünde doğrudan yerel çağıran, 16'sında en az bir guarded çağıran gözlendi. Dış/import/callback çağrıları kapanmadığı için `caller_closure_verified=0`; subprocess read-only etki kanıtı da 0/6.
- Kabul değişmedi: 0/92 davranış parity, 0/26 runtime güvenlik, 0/22 ana görev. Sıradaki iş 16 kısmi guarded çağıran kaydında tüm gerçek giriş yollarını ve altı subprocess komutunun etkisini tek tek kaynak-bağlı kapatmak; statik çağıran gözlemini runtime kabulü saymamak.
- Korunan üretim verisi, eski depo, PR #71, canlı probe, cihaz ve Actions tetiklenmedi. Gerçek bağımsız execution/artifact, harici restore ve en son kullanıcı cihaz kanıtı hâlâ dış engel.
## 23 Ekim 2026 — K1 artifact yazıcısı ebeveyn-değiştirme yarışı kapatıldı
- Başlangıç `main` SHA'sı `fb4b00a88af5a1257eeb92bc531f2f94348e786c`; bu SHA'daki bağımsız M3U8 önizleme çalışmasına dokunulmadı. Güvenli descriptor-relative evidence yazıcısı public yardımcı olarak açıldı: `ce830b31d3fde66ebd63c853de54c4268a304ebd`. `artifact_transport._write_json_exclusive`, iki doğrudan K1 preflight sonrasında `O_NOFOLLOW|O_EXCL` ve dizin-descriptor traversal kullanan bu yazıcıya bağlandı: `083ef2dd1e98d3ff8ccfbc708391d73365ac09d1`.
- Ebeveyn `reports` dizininin preflight dönüşünde dış dizine symlink olarak değiştirilmesi regresyonu eklendi; dışarıda dosya oluşmadığı doğrulandı. Test commitleri `40c58fbbb6ea4c7a14ed76b0e4f154b726f538bf` ve `f8c32a3a2bdf278ac627571e4118dd5bc07821e7`.
- Temiz uzak `f8c32a3a2bdf278ac627571e4118dd5bc07821e7` checkout'unda hedefli 83/83 ve tam offline 1190/1190 test; beş izole K kapısı, write-callsite audit ve rapor round-trip başarılı. Başarısız test yok. Actions dispatch/rerun yapılmadı.
- Bu yerel fixture/statik doğrulama davranışsal veya üretim kabulü değildir: parity 0/92, runtime güvenlik 0/26, ana görev 0/22 ve `production_acceptance=false` kaldı. Gerçek aynı-input bağımsız execution/artifact çiftleri, harici restore ve en son kullanıcı cihaz kanıtı hâlâ engelli/açık.
- Sıradaki somut yerel iş: 140 açık write-callsite adayında kısmi guarded caller yollarını kaynak hashine bağlı kapatmak ve altı subprocess çağrısının gerçek dosya etkisini fail-closed sınıflandırmak. Korunan playlist/EPG/favori/logo/yedek/arşiv, eski depo, PR #71 ve üretim verisi değiştirilmedi.


## 23 Ekim 2026 — Ana denetim, IBO M3U8 ve EPG açık işleri
- Kullanıcı, yeni bağımsız `MADSC55_TV_IBO_CALISANLAR_TEST.m3u8` listesini IBO Player Pro'ya ekledi; kanalların çalıştığını ve logoların göründüğünü bildirdi. **EPG hâlâ çalışmıyor**; cihazda tamamen boş mu yoksa kısmen dolu mu olduğu henüz bilinmiyor.
- Yeni test listesi eski `Madsc55/madsc-tv` deposundaki `CALISANLAR.m3u` dosyasının 1039 EXTINF kaydını ve kaynak blob SHA `b40aaf6615b120eac7bd936ccf022dc4a14025ae` kimliğini aynen korur. Favori kategorisi, sıralama, logo ve XMLTV başlığı değişmedi. Eski sistem, üretim playlist'i ve PR #71 korunacak.
- Eski `epg/report.json` raporu (2026-10-14): 1039 playlist kaydı, 730 eşleşen, 309 eşleşmeyen, 583 kullanılabilir kayıt; güncel EPG/IBO kabul kanıtı değildir. EPG URL erişimi, XMLTV güncelliği, `tvg-id` ↔ XMLTV channel id eşleşmesi, IBO'nun harici EPG yükleme biçimi ve cihazda yenileme sırayla doğrulanmalı. Yeni test ortamı dışında EPG değiştirilmemeli.
- Ana denetimde Actions `39924276525` ve `39924305569` kırmızı: `test_unpaired_surrogate_history_data_rejected_cleanly` testinde `"\\\\ud800"` düz metni gerçek eşleşmemiş Unicode surrogate yerine kullanılıyordu. Test `chr(0xD800)` ile düzeltildi (`7f0e0187093033b5b7e7416422693581ae9b91c0`); yeni Actions `39924407034` inceleme anında çalışıyordu, başarı henüz doğrulanmadı.
- Açık işler: son HEAD CI kapıları; eski yabancı/çalışmayan/yeni aday kanalların izole M3U8 taslakları ve geçmiş test eşlemesi; K1–K5 kalan güvenlik/parity kabulü; canlı EPG ve kanal süreklilik testi; son kullanıcı IBO kabulü. Eski listeyi veya mevcut cihaz kurulumunu otomatik değiştirme.


## 23 Ekim 2026 — Yeni sohbet için son devir güncellemesi
- Son kontrol: GitHub Actions CI `39924407034` (`7f0e01870930`) **başarılı**. Önceki history-pair Unicode surrogate regresyonu düzeltildi. Sonrasında `DEVAM_NOTU.md` belge commit'i `bd7f17ddf703` oluşturuldu; bu belge commit'inin CI sonucu ayrı doğrulanmış değil. Yeni sohbet başında HEAD ve Actions yeniden kontrol edilmeli.
- Kullanıcı IBO Player Pro üzerinde bağımsız `MADSC55_TV_IBO_CALISANLAR_TEST.m3u8` listesini ekledi; yayınlar ve logolar çalışıyor, **EPG hâlâ sorunlu**. Eski aktif playlist ve eski depo korunacak. 1039 EXTINF kaydı, kaynak SHA `b40aaf6615b120eac7bd936ccf022dc4a14025ae`, orijinal favori/kategori/kanal sırası ve EPG başlığı yeni listede aynen var.
- Yeni sohbet öncelikleri: (1) CI/HEAD doğrula; (2) IBO'da EPG'nin tümden boş mu kısmen dolu mu olduğunu öğren; (3) yeni test listesi ve XMLTV'de tvg-id/channel-id eşleşmesi, URL ulaşılabilirliği, rehber güncelliği ve IBO harici EPG kurulumunu izole olarak incele; (4) yabancı, çalışmayan ve bekleyen adayların salt-okunur kaynaklarından izole M3U8 test listeleri ve geçmiş raporlarını tamamla; (5) K1–K5 güvenlik/parity/CI açıklarını ele al. İlerleme gerçek test kanıtıyla raporlanacak, canlı/üretim kabulü varsayılmayacak.


## 23 Ekim 2026 — K1 subprocess stdio sözleşmesi
- Başlangıç `main` SHA'sı `9ff814ca77504eca2cf0485cf872c3d3e54b10a5`; eşzamanlı K3/K4/K5 düzeltmeleri tekrar edilmedi. Altı subprocess çağrısının tamamında stdin `subprocess.DEVNULL`, stdout/stderr ise pipe/capture olarak kaynakta bağlandı. Audit artık stdin/stdout/stderr durumunu ve `process_stdio_bounded_verified` sonucunu kaynak SHA'larıyla raporluyor.
- Kod zinciri: audit `869a5405056dc6c86c6fcf4b1055e7efab8987ef`; DNS resolver `509ae57ed135106a6988f12d68422c9215c74102`; K3 curl `7c639daed7a0210c760e42c03172bd60c097295f`; K3 curl+ffprobe `3dea21b0b6a44decca1f4020c248c053bd1a8c86`; offline gate `818d67a8b12a989667fd6271aa0d79397aca32ae`; regresyon `fbb4b6a23ff044803723999eb98b6e396b21abe0`.
- Temiz uzak `fbb4b6a23ff044803723999eb98b6e396b21abe0` checkout'unda hedefli 95/95 ve tam offline 1220/1220 test, beş izole K kapısı ve write-callsite audit başarılı. Altı subprocess adayının 6/6 stdio sözleşmesi bağlı; dış komutların gerçek dosya/ağ etkisi `0/6` doğrulandığı için tümü `review_required=true` ve `process_effect_verified_read_only=false` kaldı. Başarısız test yok.
- Kabul değişmedi: parity 0/92, runtime güvenlik 0/26, ana görev 0/22, production acceptance false. Actions dispatch/rerun, canlı probing, cihaz testi ve üretim yazması yapılmadı; korunan veri ve eski depo değiştirilmedi.
- Sıradaki somut iş: altı komutun argv/çalışma dizini/environment ve olası dosya çıktı argümanlarını kaynak-bağlı sınıflandır; yalnız kanıtlanabilir etkileri ayır, arbitrary parity komutunu fail-closed bırak. EPG canlı erişimi ve cihaz yenilemesi dış izin/kullanıcı kanıtı bekler.


## 23 Ekim 2026 — K1 subprocess etki sözdizimi sınıflandırması
- Başlangıçta doğrulanan güncel `main` SHA'sı `ae3778f0746def5635f9ad5fa55c7f8c00a37057`; bu tabandaki eşzamanlı K2/K3/K5 değişiklikleri korunarak çalışıldı. Audit kodu `691a95b1a73da526325fe0d906491e6c117eac8d`, fail-closed regresyonları `adf72bd893c97b7185ad6a4f1a5b2f259079587c`.
- Altı subprocess adayı için argv argüman/dinamik argüman sayısı, literal seçenekler, `curl` dosya çıktı seçenekleri, cwd/env kökeni ve komut etki sınıfı kaynak/callsite SHA bağıyla kaydediliyor. Mevcut dağılım: 2 ağ istemcisi (`curl`), 1 medya inceleyici (`ffprobe`), 1 satır içi Python, 1 Python modülü ve 1 çağıran-kontrollü komut.
- Dinamik argümanlar, cwd/env ifadeleri ve olası çıktı seçenekleri yalnız inceleme verisidir. Altı adayın tamamı `process_effect_verified_read_only=false`, `review_required=true`; komut etkisi kabulü **0/6** kaldı. `ffprobe -of` dosya çıktısı olarak yanlış sınıflandırılmıyor; `curl -o/--output` gibi gerçek literal yazma seçenekleri ayrı kaydediliyor.
- Sonradan gelen K3 commitleri korunarak güncel uzak `dc354863e8a70a555a744dbd42e19f09fd6e31a0` içeriğinde hedefli **109/109** ve tam `python -m madsc.offline_gate` **1275/1275** test başarılı; beş izole K kapısı, write-callsite audit, kurulum/contract/rapor round-trip ve pinned 92 kapsam kapısı geçti. Başarısız test yok. İlk GitHub yazma denemesi yanlış blob SHA nedeniyle 409 ile güvenle durdu; doğru güncel blob yeniden okunarak başka commit ezilmeden yazıldı.
- Kabul değişmedi: gerçek davranış parity **0/92**, runtime güvenlik **0/26**, ana görev **0/22**, production acceptance false. Fixture/statik sınıflandırma kabul değildir. Actions tetiklenmedi; canlı probing, cihaz testi, üretim yazısı, korunan playlist/EPG/favori/logo/yedek/arşiv ve eski depo değiştirilmedi.
- Açık iş/engel: gerçek aynı-input bağımsız execution/artifact çiftleri, harici restore ve en son kullanıcı cihaz kanıtı dış kanıt bekliyor. Sıradaki somut yerel iş, `_open_relative_file_nofollow` gibi hem guarded hem unguarded çağıranı bulunan yardımcıların okuma/yazma etkilerini ayırıp gerçek giriş yollarını kaynak-hash-bağlı incelemek; çağrı grafiği kapanmadan kabul vermemek.


## 23 Ekim 2026 — K1/K4 yedek okuma-yazma etkisi ayrımı
- Çalışma güncel `main` commitleri korunarak `f11a7f31a5d714ca595e1836402d74c06b0db93c` tabanına taşındı. Kod `adb358e3dbef94c21121ece7a7e34083cba91356`; davranış regresyonu `20616331cff3f6621f6ac685533f5ac20306464e`; audit regresyonu `9680bfc660d026b5b2a66993fc73e9fea1fa4413`.
- `_open_relative_file_nofollow` içindeki üç `os.open`, yalnız `O_RDONLY/O_DIRECTORY/O_NOFOLLOW/O_NONBLOCK` adlarıyla kaynak-bağlı hale getirildi ve `proven_read_only_descriptor` olarak ayrıldı. `_create_relative_file_nofollow` içindeki üç `os.open` ile bir `os.mkdir` gerçek yazma adayı kaldı; yardımcının kendisi sandbox kökünü koşulsuz `enforce_write_paths` ile yeniden denetliyor. Korunan `FAVORILER`, `EPG` ve `logos` kökleri descriptor açılmadan reddediliyor.
- İzole K4 yedeğinin içeride `channels.m3u` saklaması korunuyor: K1 denetimi canlı/sandbox köküne uygulanıyor, sandbox içeriği yanlışlıkla üretim playlist'i sayılmıyor. Descriptor-relative `O_NOFOLLOW|O_EXCL`, root inode bağı ve üst seviye `enforce_local_output_path` kontrolleri değişmedi.
- Eşzamanlı K4 commitlerinde bulunan kontrol-sırası hataları da kapatıldı: `compare_copy` ve `verify_independent_restore`, symlink kökü genel dizin hatasına düşürmeden önce açıkça “symlinked ancestors” olarak reddediyor.
- İlk tam koşu, fazla geniş hedef-dosya guard'ının izole `channels.m3u` restore fixture'ını reddetmesiyle 1 error verdi; başarı sayılmadı ve guard köke daraltıldı. Daha yeni K4 testleri ardından aynı erken genel hata nedeniyle önce 2, sonra 1 hedefli failure yakaladı; her ikisi kontrol sırası düzeltilip yeniden çalıştırıldı.
- Güncel uzak içerikte hedefli **163/163**, tam `python -m madsc.offline_gate` **1299/1299** başarılı. Envanter 107 Python dosyası / 142 açık aday / 13 non-write disposition; hedef oluşturma yardımcısı 4/4 doğrudan guard baskınlığı taşıyor. Beş izole K kapısı, write-callsite audit, workflow/task ve pinned 92 kapsam kapıları başarılı.
- Kabul değişmedi: parity **0/92**, runtime güvenlik **0/26**, ana görev **0/22**. Bu statik/fixture kanıt production kabulü değildir. Actions, canlı probe, cihaz, üretim/korunan veri, eski depo, PR #71 ve merge işlemi yapılmadı.
- Sıradaki somut yerel iş: kalan unguarded gerçek writer adaylarını helper bazında ayırıp doğrudan K1 guard eklenebilenleri kapatmak; dış/import/callback çağrı grafiği kapanmadan `caller_closure_verified` verme. Gerçek bağımsız execution/artifact, harici restore ve son kullanıcı cihaz kanıtı dış engel olarak açık.


## 23 Ekim 2026 — K1/K4 rollback silme kapısı ve güncel birleşik regresyon
- Başlangıçta doğrulanan uzak `main` SHA `bb3ff0df907ff761d52d93f762a73c1709779439`; eşzamanlı K1–K5 commitleri ezilmeden güncel dala taşındı. K4 `_remove_created_tree_if_same` rollback yardımcısı artık korunan hedefi `lstat` ve `shutil.rmtree` öncesinde doğrudan `enforce_write_paths` ile fail-closed denetliyor. Kod/test/audit commitleri: `703ebe30423486889b8dc71289ba06ca07bb986b`, `9c0ffe87e81a0a994f6fcbdb52f024943d80ff44`, `73acd25842408baabecebb8a71874d834bce4c2c`.
- Korunan `FAVORILER` kökünde doğrudan helper çağrısının dosya sistemi incelemesi veya silmeye ulaşmadığı davranış testiyle; `shutil.rmtree` adayının doğrudan K1 guard baskınlığı da kaynak-bağlı audit testiyle doğrulandı. Güncel envanter 107 Python dosyası / 143 açık aday / 13 non-write disposition; 84 adayda yapısal guard baskınlığı var. Bunlar 26 runtime kabulü değildir.
- Birleşik tam kapı sırasında eşzamanlı K2 değişikliklerinde iki gerçek regresyon yakalandı: surrogate kaynak etiketi yanlış hata sınıfına düşüyordu ve gömülü `xtvg-id` kabul ediliyordu. `66c682f89fb853cd3c632480f0bdf96618606430` bunları kapattı; eşzamanlı preview-label preflight'ı güncel kaynakta korundu. Başarısız 1/1332 koşu ve ara 3 hedefli failure başarı sayılmadı.
- Temiz güncel kaynak `72b20cf80b833049e1b7c555afcfb10848bed3dc` üzerinde hedefli backup/K1 paketi 193/193, son tam `python -m madsc.offline_gate` 1340/1340, beş izole K kapısı ve tüm offline kapılar başarılı. Başarısız test yok. Bu fixture/statik kanıt üretim kabulü değildir: parity 0/92, runtime güvenlik 0/26, ana görev 0/22 ve production acceptance false kaldı.
- Actions dispatch/rerun, canlı stream/EPG probe, cihaz testi, üretim yazması, korunan playlist/EPG/favori/logo/yedek/arşiv, eski depo, PR #71 veya merge işlemi yapılmadı.
- Sıradaki somut yerel iş: kalan gerçek unguarded writer helper'larını doğrudan K1 guard ile kapatmak; özellikle fixture evidence düşük-seviye descriptor yazıcısı ve rollback unlink yollarında sabit playlist istisnasını genişletmeden caller/callee sözleşmesini kaynak-hash-bağlı tamamlamak. Gerçek aynı-input bağımsız execution/artifact, harici restore ve en son kullanıcı cihaz kanıtı dış engel olarak açık.


### Aynı paket için exact-HEAD kanıt düzeltmesi
- Önceki kayıttaki `72b20cf… / 1340` eşlemesi exact checkout kanıtı olarak kullanılmamalı: komut yeni worktree oluşturduktan sonra eski, yerel preview düzeltmesi taşıyan çalışma dizininde çalışmıştı. Bu etiketleme hatası burada açıkça geri çekildi; başarı sayacı olarak kullanılmayacak.
- Gerçek güncel `37b9d1f12082ea6c480ee3c94bb9d38ae7e474f0` checkout'u 1341 testte K2 provenance hata metni nedeniyle 4 failure ve K1 mutasyon testindeki recursive patch nedeniyle 1 error verdi; bu koşu başarısızdır. K2 düzeltmesi `d60aadb5c01cab20965e6527bc87fc28104f0e81`, K1 test düzeltmesi `f6bc48f478ecabb5a254b4d0eb6dfd47e83ea950`.
- Yetkili son temiz kanıt: uzak `main` exact SHA `f6bc48f478ecabb5a254b4d0eb6dfd47e83ea950` üzerinde `python -m madsc.offline_gate` **1342/1342**, beş izole K kapısı ve tüm offline kapılar başarılı; stderr boş. Envanter 107 dosya / 143 aday. Kabul yine 0/92, 0/26, 0/22 ve production acceptance false.


## 23 Ekim 2026 — K1 düşük-seviye evidence yazıcısı ve rollback kapısı
- Başlangıçta doğrulanan uzak `main` SHA'sı `538851d6776268355389af5dbf68673fff1b6a9b`; son kod/test commit'i `67d1c183540ff28ed5c532887d71ac21b854f687` (`[skip ci]`). Eşzamanlı daha yeni HEAD yoktu; lease-korumalı ref güncellemesiyle başka commit ezilmedi.
- Ortak `write_exclusive_bytes` artık her descriptor mutasyonundan önce `enforce_local_evidence_path` çalıştırıyor. Genel JSON/diagnostic çağıranları açık `allowed_root` taşıyor; sabit Türkçe TV test playlist istisnası yalnız exact ad ve izole root için korunuyor. Korunan `FAVORILER` hedefinin ilk `os.open` çağrısından önce reddedildiği regresyonla doğrulandı.
- Bundle rollback, `Path.unlink` yerine parent dizinleri `O_NOFOLLOW|O_DIRECTORY` ile açan descriptor-relative `_unlink_evidence_if_same` yardımcısına taşındı. Silme yalnız aynı dev/inode/size/mtime/ctime kimliği için yapılır; eşzamanlı replacement korunur. Audit bu düşük-seviye yazma/rollback kapsamındaki **9/9** mutasyon için doğrudan K1 guard baskınlığı raporladı.
- İlk hedefli koşuda yanlış yazılmış `tests.test_artifact_transport` modülü bir komut hatası verdi; gerçek audit de eski bundle `Path.unlink` satırını doğrudan guarded saymadı. Bu koşu başarı sayılmadı. Descriptor-relative rollback düzeltmesinden sonra temiz exact-SHA checkout'unda hedefli paket **161/161**, `python -m madsc.offline_gate` **1372/1372** geçti; beş izole K kapısı ve tüm offline kapılar başarılı. Envanter **107 dosya / 145 aday**; başarısız son test yok.
- Kabul değişmedi: gerçek davranış parity **0/92**, runtime güvenlik **0/26**, ana görev **0/22**, production acceptance false. Fixture/statik başarılar bunların yerine sayılmadı. Actions dispatch/rerun, canlı stream/EPG probe, cihaz testi, üretim yazması, korunan playlist/EPG/favori/logo/yedek/arşiv, eski depo, PR #71 veya merge işlemi yapılmadı.
- Açık işler/engel: gerçek aynı-input ve bağımsız execution/artifact kökenli 92 çift, 26 runtime kuralı, 22 gerçek görev, harici restore ve en son kullanıcı cihaz kanıtı dış doğrulama bekliyor. Sıradaki güvenli yerel iş 145 açık aday içindeki diğer gerçek writer/rollback helper'larını kaynak-hash-bağlı inceleyip doğrudan K1 guard veya kanıtlı non-write disposition ile kapatmak; caller closure olmadan kabul vermemek.


## 23 Ekim 2026 — K1 parity okuyucu descriptor disposition paketi
- Önceki belge commit'i `7516a67606ccb7539be8aa91061bb3178e6ad73c`; kod/test `cd9e164efe14ff2510c5bf98fdfa758d62e680f3` (`[skip ci]`). `parity_manifest_cli._read_regular_file` ve `parity_snapshot_writer._sha256_regular_file` içindeki salt-okunur bayraklar tek kaynak-bağlı `O_RDONLY | getattr(O_NONBLOCK, 0) | getattr(O_NOFOLLOW, 0)` ifadesine taşındı; çalışma davranışı değişmedi.
- Audit regresyonu iki `os.open` satırının `proven_read_only_descriptor`, `review_required=false` ve kaynak SHA bağlı disposition olduğunu doğruluyor. Böylece gerçek yazma adayı sayısı **145'ten 143'e**, disposition sayısı **13'ten 15'e** indi; bu sonuç runtime güvenlik kabulü değildir.
- Temiz exact uzak `cd9e164efe14ff2510c5bf98fdfa758d62e680f3` checkout'unda hedefli parity/audit paketi **90/90**, tam offline kapı **1373/1373** geçti; beş izole K kapısı ve bütün offline kapılar başarılı, başarısız test yok. Kabul 0/92, 0/26, 0/22 ve production false kaldı.
- Sıradaki somut yerel iş 143 aday içindeki gerçek writer/rollback helper'larını doğrudan guard/caller sözleşmesiyle kapatmak; özellikle `core.py` fixture yazıları ile legacy not birleştiricisinin atomic replace/delete yollarını izin sınırlarını genişletmeden ayırmak. Dış bağımsız run/artifact, restore ve en son kullanıcı cihaz kanıtı bekliyor; Actions/canlı probe/üretim/korunan veri/eski repo/PR71/merge işlemi yapılmadı.


## 23 Ekim 2026 — K1 legacy not birleştirici atomic replace ve arşiv koruması
- Başlangıçta doğrulanan güncel `main` `736f119bc23ca1ceecce39b834abc89e36ba0ce2`; kod/test commit'i `8f8251a43d005b2bcb040739a3fc1c5725f333d3` (`[skip ci]`). Aradaki K2/K3/K4/K5 commitleri korunarak lease-korumalı güncelleme yapıldı.
- `scripts/birlestir_eski_sistem_notlari.py` artık merged çıktıyı doğrudan `write_text/Path.replace` ile yazmıyor: yeni hedef ve mevcut regular-file replacement için ayrı K1 guard, exclusive/no-follow geçici dosya, aynı inode/size/zaman kimliği ve descriptor-relative `os.replace` kullanıyor. Geçici çıktı symlink'i dış dosyaya yazamıyor; mevcut güvenli merged belge atomik olarak yenilenebiliyor.
- `docs/eski_depo_not_arsivi/` her repository derinliğinde açıkça korunan yol oldu. Geriye uyumlu `--remove-archived-notes` seçeneği artık kaynak/çıktı mutasyonundan önce fail-closed reddediliyor; hiçbir arşiv kopyası silinmedi. Audit'te birleştiricide kalan tek gerçek mutasyon `os.replace` ve doğrudan K1 guard baskınlığı doğrulandı.
- İlk hedefli koşudaki 2 failure test bloğu yerleşimi ve yeni audit beklentisi sorunuydu; başarı sayılmadan düzeltildi. Temiz exact uzak `8f8251a43d005b2bcb040739a3fc1c5725f333d3` checkout'unda hedefli **128/128**, tam offline **1385/1385** geçti; beş izole K kapısı ve bütün offline kapılar başarılı. Envanter **107 dosya / 142 aday / 17 disposition**; son başarısız test yok.
- Kabul değişmedi: parity 0/92, runtime güvenlik 0/26, ana görev 0/22, production false. Sıradaki somut yerel iş `core.py` içindeki izole fixture yazılarını canlı M3U/XMLTV istisnasını genişletmeden güvenli test-writer/callsite sözleşmesine bağlamak. Gerçek bağımsız execution/artifact, harici restore ve en son kullanıcı cihaz kanıtı dış engel; Actions/canlı probe/üretim/korunan veri/eski repo/PR71/merge işlemi yapılmadı.


## 23 Ekim 2026 — K1 `core.py` izole fixture yazıcı kapısı
- Başlangıç `main` SHA `2bb2cc0f408b8af5f878bc03723c8758439c1d70` idi; eşzamanlı K3/K5 commitleri geldikten sonra paket `0030d8b1b284a3714cf9ed22db45c006dfee5939` üzerine yeniden tabanlandı. Son kod/test SHA `70d1150fe4866f96c87b7bc3dece6b3ba2741080` (`[skip ci]`).
- `core.execute` içindeki doğrudan fixture `write_text`/`write_bytes`/`mkdir` çağrıları sabit allowlist, yalnız doğrudan sistem temp kökü, no-follow dizin descriptor'ları, regular-file/tek-link ve overwrite inode eşliği uygulayan `write_core_fixture` yardımcısına taşındı. Korumalı/traversal path, nested root, symlink parent/target ve hardlink overwrite regresyonları eklendi. `execute` kapsamında doğrudan mutasyon adayı kalmadı; yeni yardımcının 7 gerçek mutasyon adayı doğrudan K1 guard baskınlığı taşıyor.
- İlk hedefli koşu, guard çağrısını ayrı deyime çevirirken dönüş path'inin yeniden kurulmadığını gösteren 14 error + 3 bağlı failure üretti; bu koşu başarı sayılmadı. Düzeltmeden ve rebase'den sonra exact uzak SHA'da hedefli **110/110**, tam `python -m madsc.offline_gate` **1435/1435**, beş izole K kapısı ve tüm offline kapılar başarılı. Envanter 109 dosya / 140 aday; başarısız son test yok.
- Kabul değişmedi: parity **0/92**, runtime güvenlik **0/26**, ana görev **0/22**, production false. Fixture/statik sonuçlar gerçek bağımsız execution/artifact, harici restore veya cihaz kanıtı değildir. Actions elle başlatılmadı; canlı probe, üretim yazısı, korunan veri, eski repo, PR #71 ve merge işlemi yapılmadı.
- Sıradaki somut yerel iş: güncel envanterde guard baskınlığı olmayan gerçek writer/rollback helper'larını string dönüşümü ve subprocess adaylarından ayır; merkezi K1 guard eklenebilen ilk bağımsız grubu kaynak-bağlı testlerle kapat. Dış aynı-input bağımsız run/artifact kanıtı gelmeden 92 kabulünü artırma.


## 23 Ekim 2026 — K1 K3 pilot segment yazısı koruması
- Core fixture paketinden sonra güncel `main` yeniden okunup K5'in `ffa444e`/`e9d3825` commitleri korunarak kod/test SHA `08ae448288ca488ce54caeea1993f787eca75e87` yayımlandı (`[skip ci]`).
- `k3_turkish_tv_video_pilot.verify_av` indirilen segment baytlarını artık doğrudan `Path.write_bytes` ile yazmıyor; ortak `write_exclusive_bytes` üzerinden açık temporary `allowed_root`, K1 path preflight, no-follow dizin traversal ve exclusive create kullanıyor. Test, payload/destination/root sözleşmesini doğruluyor; audit'te `segment.write_bytes` adayı kaldırıldı. Canlı pilot veya stream probing çalıştırılmadı.
- İlk audit testi mevcut ffprobe subprocess adayını hesaba katmadığı için 1/139 failure verdi; başarı sayılmadan yalnız dosya yazma adayına daraltıldı. Exact uzak SHA'da hedefli **139/139**, tam offline **1438/1438**, beş izole K kapısı ve bütün offline kapılar başarılı. Envanter 109 dosya / **139 aday**; son başarısız test yok.
- Kabul değişmedi: parity 0/92, runtime 0/26, görev 0/22, production false. Sıradaki yerel iş `offline_five_gate.assess_report_roundtrip` geçici paket dizini oluşturmasını güvenli temp-root/callsite sözleşmesine bağlamak; `legacy_retest_390` CSV `StringIO` çağrılarını filesystem yazısı saymadan kaynak-bağlı ayırmak. Gerçek bağımsız artifact/run, restore ve en son kullanıcı cihaz kanıtı bekleniyor.


## 24 Ekim 2026 — Devir belgeleri kesilme onarımı
- Büyük devir dosyaları connector'a tek parça komut çıktısından aktarılırken çıktı sınırı metni iki belgeye gömülmüş ve orta bölümler kesilmişti. `0fadad010e3cbc5846a97466944d7b613b2b851c` (`[skip ci]`) yalnız `DEVAM_NOTU.md` ile `PROJE_HAFIZASI.md`yi onardı: DEVAM son sağlam `ff74d555…`, PROJE son sağlam `1c57c6ca…` gövdesi üzerine sonraki tarihli bölümler eksiksiz yeniden eklendi.
- Uzak commit yeniden okunarak hiçbir `Warning: truncated output`/`tokens truncated` izi kalmadığı, DEVAM'ın 1144 ve PROJE_HAFIZASI'nın 2790 satır olduğu doğrulandı. Eşzamanlı `518cbbf…` K1–K5 kod/test geçmişi korundu; bu belge onarımı test veya kabul sayacı değildir.
- Son doğrulanmış kod paketi `08ae448288ca488ce54caeea1993f787eca75e87`; 139 hedefli ve 1438 tam offline test başarılıydı. Kabul 0/92, 0/26, 0/22 ve production false kalır. Sıradaki turda güncel main yeniden okunup belgede kayıtlı ilk bağımsız yerel işe ilerlenmelidir.
