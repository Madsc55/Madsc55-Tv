# Beş eski workflow: on çağrılan betiğin toplu yan etki taraması

**Kaynak sabiti:** `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. GitHub üzerinden 10 betiğin gerçek kaynak içeriği salt okunur alındı. Bu rapor **kaynak-kod satırlarına dayalı ilk yazma/yürütme taramasıdır**, tam çağrı grafiği, çalışma testi veya davranışsal kabul değildir.

| Betik (kaynak blob SHA) | Kaynakta saptanan davranış ve satır | K hedefi / eksik kabul |
| --- | --- | --- |
| `tools/genis_kaynak_taramasi.py` (`d0330c0fca9ab6dfacb729868cec534c4ce73f37`) | 17: `madsc_genis_tarama/` oluşturur; 40: ağdan `urlopen`; 68–72: korunan listeleri ve keşif geçmişini okur; 106–110: `candidate_review.json`, `state.json`, `summary_*.json`, `sources_*.csv` yazar. | K2/K5 rapor zinciri; ağ girdisi ve dosya sınırı gerçek test edilmeli. |
| `scripts/build_epg.py` (`f2738ecfc3b617c6df939abb545413a58e2b70a9`) | 11: `CALISANLAR.m3u` girdisi; 13–17: harici EPG kaynakları; 32: `urlopen`; 147: eşleşme yoksa hata; 148–149 ve 156: **`epg/madsc-epg.xml`**, `epg/report.json` yazar. | K1 EPG yazmasını bloke eder; K3 fixture ile XMLTV eşlemesi ayrı sınanmalı. |
| `scripts/build_ibo_epg_test.py` (`1bebbf27ae1514a9fb02193ade6a8ddfc22b25be`) | 7–8: `epg/madsc-epg.xml` okur, **`epg/ibo-test-epg.xml`** yazar; 32: 5 kanallı kanıt eksikse hata. | K3 cihaz dışı teknik pilot; IBO cihaz kabulü değildir. |
| `scripts/epg_tv_readiness.py` (`5ca591ef7db2347b064acd91f383ae660d8eae74`) | 62–64: XML/rapor okur, **`epg/tv_kontrol_bekliyor.json`** yazar; 67: hazır değilse hata. | K3/K5 rapor kontrolü; korunan EPG alanına yazma yeni sisteme taşınmaz. |
| `final_validation.py` (`f7e7853d1e0ff9ce01ab1c8381c5fc077ac5e793`) | 40–70: `ffprobe` ve `ffmpeg` alt süreçleri; 112/116: manifest ve kanal durumunu okur; 113, 124, 135: `madsc_son_kontrol/images`, `results.json`, `summary.json` çıktıları. | K3 canlı medya ölçümü izinli değil; K5 rapor/timeout/failure eşdeğerliği eksik. |
| `scripts/archive_backups_354_classified.py` (`65f5faf61cc69d5babecacdca1db9faa84881210`) | 5: **`CALISANLAR.m3u`** açar; 28–31: `madsc_kesif/` altında iki M3U arşivi ve JSON raporu yazar; **32: `CALISANLAR.m3u` dosyasını doğrudan yeniden yazar**. | K1 **kesin korunan-yazma sınırı**; K4 izole restore dışında bu yan etkiyi taşıma. |
| `madsc_akilli_kesif.py` (`d8673dbd763c7411878bd27fa432b455c15c9b31`) | 4: `madsc_kesif/` oluşturur; 8: çok sayıda dış M3U kaynak URL'si; ağ ve paralel keşif modülleri kullanır. | K2 canlı ağ kaynakları ve dolaylı yan etkileri ayrıca çalıştırmadan doğrulanamaz. |
| `scripts/discovery_archive.py` (`22274f17f34a501f691bedb5e3667bb1fe00bf32`) | 10: `madsc_kesif/` oluşturur; 37–38: yabancı/ana listeleri okur; 69/71: **`gecmis.json`** ve registry CSV yazar. | K2→K5 kalıcı geçmiş sözleşmesi, gerçek koşu kanıtı eksik. |
| `scripts/four_stage_discovery_report.py` (`c8d0ece165ee5043a034bf276658b2be0eb79917`) | 18/33: geçmiş ve logo girdileri; 56: **`DORT_ASAMA_TEK_RAPOR.json`** üretir; EPG ertelenmiş. | K2/K5 rapor eşlemesi; EPG yapılmış sayılmaz. |
| `tools/protected_write_gate.py` (`c3c8f278db7de4cd0fd61cdb4180f9c03cb2c4c1`) | 12–20: korunan dosya/dizin adları; 45–64: `git` alt süreçleriyle staged/unstaged/untracked/ignored incelemesi; 77: hata yakalama. | K1 statik gate kodu var, ancak tüm dolaylı runtime yazmaların gerçekten engellendiği kanıtlanmadı. |

## Toplu karar

- **Kesin doğrudan korunan mutasyon:** `archive_backups_354_classified.py` satır 32. EPG üç betiği de korunan EPG dosyalarına çıktı yazar. Bu davranışların hiçbiri yeni üretim akışına taşınmamalı.
- **Yalıtılabilir rapor üretimi:** geniş kaynak taraması, discovery archive, dört aşama raporu ve son kontrol; ancak çıktı yolları, gerçek girdi, hata ve tekrar semantiği eşleştirilmeden kabul verilmez.
- **Canlı dış bağımlılıklar:** `urlopen`, `ffprobe`, `ffmpeg`, geçmiş dosyaları ve Git push, fixture testinden ayrı tutulur.
- **Önemli sınır:** Bu tarama 10 dosyanın görünen yazma/çalıştırma noktalarını çıkarır; tüm fonksiyon akışlarının ve çağrılan yardımcı betiklerin tamamının incelendiği iddia edilmez. Test koşulmadı, workflow tetiklenmedi, eski depoya veya korunan listelere yazılmadı.
- **Kabul:** 92 davranışsal eşdeğerlik 0/92, 26 güvenlik kuralı 0/26, 22 görev 0/22.

## Sonraki toplu teknik iş

K1–K5 karşılıklarıyla bu on betiğin girdi/çıktı, failure/timeout, yan etki ve geçmiş zinciri için toplu karşılaştırma matrisi oluştur; scriptlerin kalan dolaylı çağrılarını ve ürettikleri artifact adlarını kaynak üzerinden çöz. Bu raporu davranışsal kabul yerine koyma.
