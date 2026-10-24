# K5 — Davranışsal kabul için eksik kanıt ve tamamlanma kapıları

Tarih: 2026-10-24. Dal: `k5/fail-closed-evidence-20261023`. Eski kaynak sabit SHA: `ca374df3b9585c0d76a078db9536150ebbc260f7`.

## Gerçekleşen

- 92/92 eski workflow YAML için ilk kaynak incelemesi belgelendi. Kaynak SHA envanteri ve kaynak bütünlüğü CI testi bulunuyor.
- K5 karşılaştırıcısı fixture SHA256, ayrı eski/yeni commit ve run ID, stdout/stderr, artifact, yan etki, exit code, timeout ve retry alanlarını denetliyor.
- JSON içindeki `independent_runs: true` iddiası tek başına yürütme kanıtı değildir. Karşılaştırıcı, eşleşme olsa bile `accepted=false` döndürür.
- Son doğrulanan CI (commit `a41cab06fd86e9d97b0b82abb9bd1f6fce687304`): K5 kaynak bütünlüğü ve offline unit testleri başarılı.

## Kapanmamış kabul engelleri

1. **92/92 bağımsız eski/yeni fixture yürütme çifti eksik.** Ayrı izole runner, sabit fixture, iki gerçek run ID, stdout/stderr hash'leri, artifact ve yan etki manifesti, hata/timeout/retry karşılaştırması gerekiyor.
2. **Detaylı YAML/script çağrı grafiği ve gerçek davranışsal eşleştirme eksik.** İlk inceleme tam davranış sözleşmesi veya entegrasyon kanıtı değildir.
3. **Canlı ağ ve medya koşulları doğrulanmadı.** HTTP HEAD/Range erişimi, gerçek ffprobe/oynatma, coğrafi erişim ve lisans/izin kontrolleri farklıdır. Yetkisiz kaynaklar kabul edilmemeli.
4. **Korunan yazma güvenliği üretim ortamında onaylanmadı.** Playlist, EPG, logo, VOD ve yedek için izinli yazma yolları, approval gate, değişmez hash ve restore dry-run ayrı kanıt ister.
5. **K1/K3/K4/K5 çapraz kabul raporları tamamlanmadı.** Son bilinen K1 runtime 0/26 ve genel 0/22; güncel bağımsız kanıtlarla yeniden ölçülmeli.
6. **PR #6 henüz birleştirilmedi.** CI yeşil olması merge/production onayı anlamına gelmez.

## Tamamlanma ölçütü

Her workflow için kaynak sözleşmesi + script bağımlılıkları + eşleşen yeni sistem davranışı + bağımsız fixture yürütmeleri + iki yürütmenin doğrulanabilir log ve artifact hash'leri + yan etki ve korunan dosya hash kontrolü + negatif senaryolar + gözden geçirenin onayı gerekir. Eksik veya çelişkili kanıt `BLOCKED` olarak kalır. Hiçbir kabul sayısı kanıtsız artırılmamalı.

## Öncelik sırası

1. Offline, read-only iş akışlarında ilk bağımsız fixture yürütme çifti oluşturulması ve kayıtlarının doğrulanması.
2. #49 ve uzun workflow'lar dahil ayrıntılı bağımlılık/yan etki envanterinin tamamlanması.
3. Ağlı kanal keşiflerinin izole ve izinli kaynaklarla sınanması.
4. Yazma ve geri yükleme yollarının açık onayla, korunan üretim verilerine dokunmadan sınanması.
5. K1–K5 kabul kapılarının ayrı raporlarla kapatılması.

**Şu an kabul: 0/92.** Bu belge tamamlanma iddiası değil, doğrulanabilir açık iş listesidir.
