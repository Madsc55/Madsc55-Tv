# HEPSI — Yerel ZIP test turu (2026-10-22)

## Kaynak ve sınırlamalar
- Kullanılan arşiv: kullanıcı tarafından yüklenen `Madsc55-Tv-main.zip` (465 ZIP girdisi; kaynak ağacı yerel kopya).
- Bu ZIP, GitHub main'den eskiydi. Yerel kopyada yalnızca test yürütmek için şu iki senkronizasyon uygulandı: `madsc/workflow_consolidation.py` içindeki izinli tanılama iş akışı envanterine `madsc-online-evidence-join.yml` ve `madsc-online-pilot-gates.yml` eklenmesi; `madsc/core.py` içindeki K5 geçmiş fixture'larının zaman damgalarının sıralı yapılması. Workflow envanteri değişikliği GitHub'da önceki commit `5f222f4` ile mevcuttu. Core fixture sıralaması GitHub'a `6a5b906` ile kaydedildi.
- Testler yerel ZIP ağacında, bu iki yerel senkronizasyon sonrası çalıştırıldı; bu, tam güncel main checkout testi değildir.

## Sonuçlar
- Hedefli 13 modül: 118 test, tümü geçti. Modüller: test_workflow_consolidation (29), test_core (10), test_acceptance_output_guards (2), test_maintenance (15), test_handoff_acceptance (13), test_five_stage_evidence_audit (3), test_offline_gate (9), test_batch_acceptance (19), test_k1_k5_acceptance_requirements (5), test_progress_scorecard (5), test_five_stage_offline_gate_integration (1; bu test içeride 759 testi de çalıştırıyor), test_legacy_source_score_vectors (3), test_five_stage_installation (4).
- `assess_all()`: K1/K2/K3/K4/K5 beş izole fixture kapısı başarılı.
- `assess_report_roundtrip()`: beş rapor K5 tarafından tüketildi; rapor baytları korundu.
- `test_five_stage_installation`: 4/4 geçti; sembolik bağlantılı workflow girişi reddediliyor.
- Python başlatılırken dış artifact_tool spreadsheet warmup bir RemoteError yazdı, ancak her test süreci exit code 0 ile tamamlandı. Bu uyarı MADSC-TV testlerinin sonucu değildir.
- Tüm 150 test dosyasını bir kerede çalıştırma denemesi süre sınırını aştı; tam 150 dosyalık suite yeşil sayılmıyor.

## Kabul durumu — değişmedi
- Eski 92 workflow davranışsal eşdeğerliği: 0/92 kabul.
- 26 güvenlik kuralı: 0/26 bağımsız kabul.
- 22 ana görev: 0/22 bağımsız kabul.
- Canlı IPTV/EPG/favoriler/yedekler/arşivler/cihazlar üzerinde değişiklik yapılmadı; Actions tetiklenmedi; PR #71 birleştirilmedi.

## Sonraki adımlar
1. 150 test modülünü küçük, süre sınırlı gruplar hâlinde çalıştır; timeout ve fail sonuçlarını ayrı raporla.
2. GitHub main'in ZIP'ten farklı dosyalarını blob SHA ile eşleştir; tam main snapshot ile tekrar koş.
3. 99 workflow kaynak envanterini 92 davranış sözleşmesiyle birebir karşılaştır; sadece komut varlığı değil, girdiler/çıktılar, artifact, izin, timeout, hata davranışı ve yan etkileri doğrula.
4. K1 26 kuralı ve 22 görev için bağımsız kanıt eklemeden sayaçları artırma.

## Ek regresyon taraması — devam eden tur
- Tüm 150 `test_*.py` dosyası 10 modüllük gruplarla taranmaya başlandı; tüm paket henüz yeşil değil.
- Bulunan ve GitHub'da düzeltilen test syntax hatası: `tests/test_k3_live_manifest_source_snapshot.py`; commit `8f138e30d536e686ceac7cb15af6928dceeadfae`. ZIP çalışma kopyasında aynı düzeltme uygulandı ve hedefli test `6/6` geçti.
- Geniş taramada kalan başarısızlıklar: batch 1'de 2 failure/9 error (aday görüntü metaverisi ve fingerprint test beklentileri), batch 4'te 1 failure (üç aşamalı süreklilik alanı bekleneni karşılamıyor), batch 6'da 6 error (güvensiz aday metaverisi), batch 9'da 1 legacy retest çıktı farkı, batch 11'de 1 legacy replay zamanlama farkı. Bu gruplar henüz kök nedenlerine göre giderilmedi.
- Batch 7'nin tek SyntaxError'ı giderildi. Batch 2,3,5,10,12'nin çalıştırılabilen grupları exit 0 verdi. Tüm 150 modül için tek bir kesin toplam test sayısı çıkarılamadı; bir sonraki tarama komutunun toplam süresi aşıldı.
- Bunlar yerel ZIP ve hedefli senkronizasyonla elde edilen sonuçlardır; güncel main'in eksiksiz checkout testi değildir. Kabul sayaçları değişmez: 0/92, 0/26, 0/22.
