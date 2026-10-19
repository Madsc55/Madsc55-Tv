# Madsc55-Tv — yeni sohbete eksiksiz çalışma devri (19 Ekim 2026)

> Bu belge, sohbetin kelimesi kelimesine transkripti değil; devam etmek için doğrulanmış teknik kararlar, geçmiş işler, riskler, kalan işler ve kaynak referanslarıdır. Geçmiş sohbet mesajlarının tümü buraya birebir aktarılmadı. Yeni sohbette önce bu dosyayı ve PROJE_HAFIZASI.md sonunu oku.

## Kullanıcının güncel kesin hedefi

**99 GitHub Actions YAML otomasyonunun her birinin gerçek görevini TAM çöz:** yalnız dosya adını/YAML adımlarını değil, her workflow'un bütün çağrılan Python/shell/inline kodlarını, alt çağrılarını, girdi/çıktı şemalarını, state kalıcılığını, tetik/izinleri, bağımlılıkları, ağ/ffprobe/IBO koşullarını, hata/yeniden deneme kurallarını, yerel ve remote yazma etkilerini, korunan dosya risklerini ve K1–K5'te doğru tasarım karşılığını incele. **YAPILACAK / YAPILMAYACAK / KANIT BEKLEYEN** olarak kaydet. Sonra beşli sistemi kanıtla tamamla. İncelediklerini hemen merkezi hafızaya kaydet; aynı dosyaları gereksiz tekrar inceleme. Kullanıcı kısa ilerleme raporu ve gerçek commit/test kanıtı istiyor; boş güvence istemiyor.

## Repo ayrımı / mutlak güvenlik

- **Yeni/hedef:** `Madsc55/Madsc55-Tv` (büyük/küçük harf ve tireye dikkat); tek merkezi proje hafızası `PROJE_HAFIZASI.md`. Derin görev haritası `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md`; ilk 99 YAML envanteri `docs/ESKI_WORKFLOW_99_ENVANTER.md`; kabul kapıları `docs/KABUL_KAPILARI.md`; bu devir belgesi.
- **Eski/kaynak, SALT OKUNUR:** `Madsc55/madsc-tv` dal `madsc/bes-sistem-toplu-birlestirme`, eski HEAD referansı `ca374df3b9585c0d76a078db9536150ebbc260f7`. Yeni işe başlamadan eski `AGENTS.md`, `DEVAM_NOTU.md`, `810 dosya notu.md` ve ilgili kaynak notlarını oku; önceki özet tüm notların okunduğu anlamına gelmez.
- Korunan **CALISANLAR.m3u**, ana kanal listeleri, YEDEKLER, YENİLER, FAVORİLER, yabancı kanallar, cihaz favorileri, EPG, logolar, kanal URL/ID/sıralama hiçbir şekilde otomatik değiştirilmez. **Eski depoya yazma yok**, üretim cron/push/deploy yok, main merge yok, PR #71 merge yok. Kullanıcının genel inceleme yetkisi bu riskli üretim değişikliklerine özel onay yerine geçmez.
- IBO Player Pro cihazında **kullanıcının WORKING dediği yayın**, teknik ffprobe başarısız diye silinmez; YEDEKLER kuralı korunur fakat korunan YEDEKLER'e otomatik yazılmaz. Fixture testi canlı ffprobe veya cihaz kabulü değildir.

## Sayılar — en son doğrulanan

- Eski kaynak tree: **99 workflow YAML**, **198 Python dosyası**, toplam **849 tree girdisi**. Python 198'in hepsi workflow tarafından çağrılıyor denemez.
- **99/99 YAML ilk kaynak incelemesi** tamam (tetik/izin/adım); 7 kapsam dışı (beş `madsc-01..05` kategori koordinatörü + `k1-protected-write-tests.yml` + `madsc-hizli-on-kontrol.yml`); **92 eski workflow** davranışsal parity kapsamı.
- **23/99 YAML derin görev çözümlemesi**, **32 benzersiz Python kaynak dosyası** bu çalışma turlarında incelendi. **76 YAML** aynı derinlikte bekliyor. 23'ten `madsc-01-guvenlik.yml` 92 kapsam dışı: **22/92** derin kaynak çözümlemesi.
- **0/92 davranışsal parity onayı.** Kaynak `scripts/five_category_92_workflow_audit.py` her birini `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` işaretliyor. Kaynak incelemesi/yeşil CI otomatik eşdeğerlik değildir.
- Eski 810 dosya incelemesi ayrı çalışma: 810 envanter; önceki notlara göre 437 metinsel/nonimage incelendi, 373 görsel atlandı. Eski notlarda 823/450 gibi farklı tarihli sayımlar var; kesin yeni sayım için kaynak yollarını uzlaştır.

## Şimdiye kadar derin incelenen 23 YAML — tekrar yapma, kaynak belgesine bak

1. `aday-bekletme.yml`: 8 Python, dış keşif → duplicate → video/ses → gecmis.json bekletme → akıllı takvim → RETEST_LIMIT=5 → güven puanı → öncelik. Runner'lar arasında geçmiş kalıcılığı belirsiz.
2. `390-aday-tekrar-test.yml`: 20 saniye paralel video/ses; CSV ve teknik aday M3U.
3. `akilli-aday-puanlama.yml`: ffprobe teknik puan CSV/JSON.
4. `birlesik-aday-raporu.yml`: keşif + ffprobe + puan + kararlılık + birleşik kabul raporu.
5. `kanal-kararlilik.yml`: önceki gözlem cache restore/save + ffprobe + kararlılık raporu.
6. `genel-aday-medya-test.yml`: ilk aday grubunda canlı ffprobe.
7. `aday-logo-epg-test.yml`: aday logo JSON ve IBO pilot XMLTV kanıt birleştirme.
8. `aday-yedekleme.yml`: teknik aday taslak M3U, üretim YEDEKLER'e izin değil.
9. `felaket-kurtarma-tatbikati.yml`: Git kaynaklı geçici restore/checksum; offsite değil.
10. `epg-pages.yml`: EPG doğrulama ve Pages hazırlama/deploy bağımlılığı.
11. `vod-guncelle.yml`: dış VOD takvimi → JSON; cron + contents:write + git push (yüksek risk).
12. `madsc-birlesik-kesif.yml`: çoklu keşif + ffprobe + arşiv + EPG/logo join + rapor + git push (yüksek risk).
13. `madsc-01-guvenlik.yml`: K1 korunan dosya snapshot, belge/24 kural kanıt, regresyon (92 kapsam dışı).
14. `besinci-zaman-asimi-test.yml`: inline timeout doğrulama.
15. `birlesik-durum-raporu.yml`: mevcut raporlardan birleşik haftalık durum, yeni stream testi yok.
16. `dokuzuncu-akilli-tekrar-test.yml`: inline akıllı tekrar zamanlama testi.
17. `epg-gunluk.yml`: EPG XML toplama, beş kanal IBO pilotu, cihaz bekleme raporu; cron + push (yüksek risk).
18. `genis-kanal-tarama.yml`: çoklu M3U fetch/normalize/probe ve CSV.
19. `ibo-bagimsiz-test-listesi.yml`: teknik aday raporundan bağımsız IBO deneme M3U/CSV/JSON.
20. `ibo-epg-kimlik-denetimi.yml`: CALISANLAR vs EPG tvg-id/XMLTV pilotu.
21. `ibo-yedek-kalite.yml`: inline yedek ffprobe kalite.
22. `iptv-test.yml`: `iptv_test.py` canlı test ardından **CALISANLAR.m3u'yu yeniden yazar**; `CALISMAYANLAR.txt`, `TEST_RAPORU.csv` üretir. KRİTİK, doğrudan çalıştırma yasak.
23. `kaynak-puanlama-kontrol.yml`: kaynak güven puanı syntax/fixture.

**Ek kritik kaynak incelemesi:** `automatic-png-logos.yml` YAML ve 3 betiği incelendi; `scripts/automatic_png_logos.py` `CALISANLAR.m3u` üzerine **koşulsuz `playlist.write_text(updated)`** ve `logos/auto/*.png` yazabilir. `contents:read` yerel çalışma ağacı yazmasını engellemez. Bu YAML için ayrı tam girdi/çıktı/bağımlılık kabul matrisi henüz tamamlanmadığından yukarıdaki **23/99 sayacına eklenmedi**; sıradaki incelemede bitir ve sayaç güncelle. İki riskli scripti üretim üzerinde çalıştırma.

## K1–K5 uygulama/test geçmişi

- Yeni sistemde `madsc/core.py`, `madsc/handoff.py`, `madsc/candidate_coordination.py`, `madsc/legacy_stability.py`, `madsc/legacy_unified_report.py`, fixture regresyon testleri var.
- K2→K3→K5 fingerprint/kanıt izolasyonu, orphan kanıt reddi, IBO WORKING korunması, eksik/sahte ffprobe fail-closed, 24 saatlik zaman penceresi, K4 üç bağımsız sandbox restore ve SHA256 negatif testleri eklendi.
- GitHub Actions #197–#203, her birinde K1 K2 K3 K4 K5 aggregate olmak üzere **6 işin tamamı başarılı** doğrulandı; son doğrulanan #203 run ID `39309574845`, head `b2ee7c51`, `completed/success`; hafıza commit `357898c9`. Sonraki dokümantasyon commitleri yeni Actions başarı iddiası değildir.
- **Açık:** 26 güvenlik kuralının tamamının gerçek enforcement kanıtı; canlı ffprobe/IBO cihaz kabulü; 5 dakika/7 gün/30 gün gerçek süreklilik; gerçek offsite restore; 92 işin davranış eşdeğerliği; eski cron/permissions/push/deploy riski.

## Son doğrulanmış GitHub doküman commitleri

- `4954f1ea`: 99−7=92 kapsam uzlaştırma.
- `1bd76996`: kabul kapıları matrisi.
- `964125e6`: aday-bekletme 8 betik derin çözüm.
- `4f977d38`: 12 YAML / 13 Python ek inceleme.
- `6f4b9867`: PNG logo betiğinin korunan playlist'e yazma bulgusu.
- `bf7e5142`: 10 YAML / 11 Python ek inceleme, iptv-test kritik risk.
- `27e9f254`: son çalışma durumu PROJE_HAFIZASI.md kaydı.
- Bu devir dosyasının commit'i ve sonraki merkezi hafıza commit'i yeni sohbette kontrol edilecek.

## Yeni sohbette somut yürütme planı

1. `Madsc55/Madsc55-Tv/docs/YENI_SOHBET_DEVIR_2026-10-19.md`, `PROJE_HAFIZASI.md` son bölümü, `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md`, `docs/ESKI_WORKFLOW_99_ENVANTER.md`, `docs/KABUL_KAPILARI.md` oku. Eski dalda ilgili AGENTS/DEVAM_NOTU ve kaynak notları kontrol et.
2. 99 YAML'ın **tam ad listesini envanterden** al, yukarıdaki 23 benzersiz tamamlanmış adı çıkar; `automatic-png-logos.yml` için eksik tam çözümlemeyi tamamla. Kalanları 10–15'lik gruplar halinde, **her YAML'ın gerçekten çağırdığı betikler** ile birlikte aç; Python alt çağrılarını da izle. Script olmayan YAML için inline `run` ve kullanılan `uses` action davranışını oku. Salt isim eşlemesiyle yetinme.
3. Her workflow için kalıcı kayıt: `YAML | tetik/schedule | permissions | concurrency | jobs/steps | shell/Python ve alt çağrılar | ağ kaynakları | okunan/yazılan dosyalar | artefakt/cache | retry/timeouts | protected risk | K1–K5 hedefi | parity test/kanıt | yapılacak/yapılmayacak | durum`. Yalnız kanıtlanan olguları yaz, belirsizliği açık bırak.
4. Workflow'lar arası üretici→tüketici bağımlılık grafiği kur; 198 Python dosyasının **workflow giriş noktası olanlarını** ayır; 11 eski doğrudan korunan liste yazarı dahil tüm yerel mutasyonları tarayıp riski sınıflandır. Özellikle `contents:read` ile çalışma ağacı mutasyonu arasındaki farkı kaydet.
5. 99/99 derin kaynak çözümü bitince **92/92 davranışsal parity için** fixture/negatif/gerçek izole koşu testleri geliştir; 7 hariç YAML'ı da görev olarak tam açıkla. Her birini gerçekten kanıtlamadan `VERIFIED` yapma. Üretim ve cihaz testleri için açık kullanıcı onayı ve gerçek saha kanıtı gerekir.
6. Her doğrulanmış gruptan sonra yeni depoda `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` ve `PROJE_HAFIZASI.md` güncelle; commit SHA raporla. Test kodu yazılırsa Actions run/jobs kontrol et ve yalnız gerçek sonucu kaydet.
7. Kullanıcıya kısa, kanıtlı Türkçe ilerleme raporu ver; hiçbir şeyi bitmiş gibi gösterme. Yeni sohbetten kaldığı yerden devam edilecek.

## Yeni sohbete yapıştırılabilecek istek

“**Madsc55-Tv** projemize kaldığımız yerden devam et. Yeni depoda `docs/YENI_SOHBET_DEVIR_2026-10-19.md`, `PROJE_HAFIZASI.md` ve `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` dosyalarını oku. Eski `Madsc55/madsc-tv` dalını salt-okunur incele. 99 YAML'ın ilk taraması bitti; 23/99 derin kaynak çözümü ve 32 Python incelemesi yapıldı, 76 YAML kaldı, 92 eski parity onayı 0/92. Kalan 76 YAML'ı tek tek gerçek script/yan etki/bağımlılık düzeyinde çöz, görevleri YAPILACAK/YAPILMAYACAK/KANIT BEKLEYEN olarak kaydet, her grupta hafızayı güncelle. Korunan dosyalara, eski depoya, cron/push, main merge ve PR #71'e dokunma. Önce automatic-png-logos.yml tam matrisini bitir, sonra sıradaki incelenmemiş YAML'larla devam et. Kanıtsız tamamlandı deme. Yap.”
