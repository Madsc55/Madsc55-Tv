# Madsc55-Tv — toplu denetim iş paketi (19 Ekim 2026)

## Değişmez kararlar
- Eski `Madsc55/madsc-tv` yalnız okunur; yeni kod `Madsc55/Madsc55-Tv` deposunda.
- Çalışan/IBO-onaylı kanallar korunur. Otomatik silme, listeye ekleme, cron, eski workflow kapatma ve üretim yazması yok.
- Birkaç küçük commit/test yerine **ilgili dosyaların toplu denetimi → bağlantılı düzeltmeler → tek geniş regresyon/kabul** yaklaşımı.
- CI fixture başarısı, 26/26 gerçek güvenlik, 99/99 davranışsal eşdeğerlik, canlı IBO veya harici yedek kanıtı değildir.

## Bu tur doğrulanan kaynaklar
- `docs/KABUL_KAPILARI.md`: 26 kuralın çalışma zamanı kanıtı eksik; eski kaynaklar, IBO ve yedekleme için ayrı kabul kapıları.
- `docs/ESKI_45_BELGE_KARSILASTIRMA_SONUC_2026-10-19.md`: 45/45 metin belgesi konu bazında okunmuş; 777 diğer blob ve 99 workflow davranışsal denetimi açık.
- `madsc/write_path_audit.py`: yazma yolu denetimi salt-okunur; gerçek git push/write gate değildir.
- `madsc/preflight.py`: dosya adı ve EPG eşleştirmesi denetimi; cihaz/üretim onayı değildir.
- `madsc/batch_acceptance.py`: fixture kanıtlarını toplar; gerçek eski workflow eşdeğerliğini doğrulamaz.

## Bir sonraki birleşik kod paketi için inceleme ve kabul matrisi
| Sistem | Birlikte denetlenecek kod ve eski karar | Negatif test / kabul kanıtı | Açık sınır |
| --- | --- | --- | --- |
| K1 | `write_path_audit.py`, `preflight.py`, korunan yollar ve eski AGENTS kuralları | traversal, backslash, casefold, symlink ve gerçek yazma kapısı | 26/26 runtime doğrulanmadı |
| K2 | `source_import.py`, `discovery.py`, `handoff.py` | M3U/M3U8, normalize tekrar, 156/155 kaynak farkı, aday bekletme | canlı kaynak keşfi yapılmadı |
| K3 | `channel_test.py`, `ibo_policy.py`, `epg_inventory.py`, `candidate_coordination.py` | 3/3, 24 saat, 7/30 gün, IBO çalışan koruması, tvg-id/logo eşleştirmesi | gerçek IBO cihaz kanıtı yok |
| K4 | `backup.py` ve eski arşiv kararları | manifest, bağımsız kopya, izole restore, kayıp/bozuk dosya | harici restore kanıtı yok |
| K5 | `maintenance.py`, `batch_acceptance.py`, Actions ve 99 workflow envanteri | eksik/bozuk/çift kanıt, başarısız job, yanlış izin, görev çakışması | 99 davranış taşınmış sayılmaz |

## Paket bitiş koşulları
1. İlgili eski not + kod + test bir arada okunur; yalnız envanterden davranışsal eşdeğerlik iddia edilmez.
2. Aynı kök nedene bağlı düzeltmeler bir iş paketinde tamamlanır.
3. K1–K5 geniş regresyon ve Actions toplu kabul sonucunun commit SHA'sı doğrulanır.
4. Başarısız veya eksik kanıt açık iş olarak kalır; üretim izni verilmez.

## Şimdiki durum
Actions #109 ve #110 başarılı; yalnız izole fixture kapsamı. Bu belge bir **toplu çalışma sözleşmesi ve açık iş matrisi**; 99 workflow veya 26 güvenlik kuralının tamamlandığı iddiası değildir.
