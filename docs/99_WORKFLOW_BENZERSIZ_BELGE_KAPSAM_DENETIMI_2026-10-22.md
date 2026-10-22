# 99 eski workflow — belge bazında benzersiz kapsam denetimi

Kaynak envanter: `docs/LEGACY_SOURCE_SCOPE.json`; 99 kayıt, 99 benzersiz YAML yolu. İncelenen belge kümesi: `UCUNCU_12`, `DORDUNCU_4`, `BESINCI_8`, `ALTINCI_8`, `YEDINCI_8`, `SEKIZINCI_8`, `DOKUZUNCU_8`, `ONUNCU_8`, `ONBIRINCI_11`, `SON_ALTI` (hepsi `docs/` altında, 2026-10-22 tarihli).

**Sonuç:** Bu 10 belgenin metninde envanterdeki 99 benzersiz dosya adından **70'i** geçiyor; **29'u geçmiyor**. Bu metin eşleştirmesi gerçek derin inceleme ve davranışsal kabul anlamına gelmez; başka eski belgeler varsa kapsama eklenebilir. Dolayısıyla önceki toplamsal 99/99 beyanı belgeler üzerinden doğrulanmış değildir.

## Bu 10 belgede adı geçmeyen 29 YAML

- `iptv-test.yml`
- `k1-protected-write-tests.yml`
- `kanal-kararlilik.yml`
- `kaynak-puanlama-kontrol.yml`
- `madsc-01-guvenlik.yml`
- `madsc-02-kesif.yml`
- `madsc-03-kanal-test.yml`
- `madsc-04-arsiv-yedek.yml`
- `madsc-05-genel-bakim.yml`
- `madsc-ibo-6115-second.yml`
- `madsc-ibo-ilk-239.yml`
- `madsc-ibo-kararlar-grup1.yml`
- `madsc-ibo-second-voice.yml`
- `madsc-otomatik-devam.yml`
- `madsc-rule24-test.yml`
- `madsc-sistem-saglik-denetimi.yml`
- `madsc-son-kontrol-kurtarma-teshis.yml`
- `madsc-son-kontrol.yml`
- `madsc-toplu-butunluk.yml`
- `madsc-tum-sistem-yedek.yml`
- `madsc-turk-kanal-geri-sec.yml`
- `madsc-yedek-turk-ayir.yml`
- `madsc-yedekler-aktarim-test.yml`
- `madsc-yedekler-sayi-duzelt.yml`
- `oncelikli-kanal-dogrulama.yml`
- `onikinci-hata-siniflandirma-test.yml`
- `publish-iptv-png-logos.yml`
- `sekizinci-tekrar-raporu-test.yml`
- `sozcu-akit-ozel-test.yml`

## Sonraki işler

1. Daha eski ilk 24/36 notunu bulup aynı benzersiz dosya eşleştirmesine dahil et.
2. Kalan her YAML için doğrudan kaynak okuması, tetikleme, çağrılan script, dosya okuma/yazma, ağ, artifact, onay ve risk kanıtı üret.
3. Statik inceleme sayısını davranışsal eşdeğerlikten ayrı tut; kabul **0/92**, güvenlik üretim kabulü **0/26**.

Bu denetimde Actions çalıştırılmadı ve korunan dosyalar değiştirilmedi.
