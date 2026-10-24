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


## 92 workflow için tekil bağımsız kabul envanteri

Bu tablo sabit kaynak envanterinden otomatik oluşturulmuştur; gerçek çalıştırma veya davranışsal kabul değildir. Kaynak commit: `ca374df3b9585c0d76a078db9536150ebbc260f7`. Her satırda yeni sistem karşılığı, izole fixture kimliği, ayrı yürütme kayıtları, çıktı ve yan etki kanıtları bağımsız olarak doğrulanana kadar durum BLOCKED kalır.

No | Eski workflow | Git blob SHA | Kabul | Açık kanıt
--- | --- | --- | --- | ---
1 | `.github/workflows/390-aday-tekrar-test.yml` | `b12f53a17434fe719a65edfdc968f675e1f16b95` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
2 | `.github/workflows/aday-bekletme.yml` | `68564680a2c32b11d1c5ed78825f01c85d0378e8` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
3 | `.github/workflows/aday-logo-epg-test.yml` | `21214309014625c4a63f00ee16c9017efac6b0a7` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
4 | `.github/workflows/aday-oncelik-kontrol.yml` | `1c2aa765b59ebad5ddbe3f0a06fcc9ead088e52b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
5 | `.github/workflows/aday-yedekleme.yml` | `6ee9e08cc161b1fc975a8108fa102867de2d9690` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
6 | `.github/workflows/akilli-aday-puanlama.yml` | `8efd3656127031ebd3d73ca32d13ae55f9e22cb8` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
7 | `.github/workflows/altinci-aday-tekrar-test.yml` | `268e05a82df328090ccf61c6335197350df8b99b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
8 | `.github/workflows/automatic-png-logos.yml` | `3d321b81f023647d1cd29c99f015d296a34df525` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
9 | `.github/workflows/besinci-zaman-asimi-test.yml` | `d36327a5b8846deab730e02043b3abc6a689ca63` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
10 | `.github/workflows/birlesik-aday-raporu.yml` | `26c0cb7bfc5af366d462eeb72461fb4ca2f9ff23` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
11 | `.github/workflows/birlesik-durum-raporu.yml` | `cfd859aa1c5d474749edd09d99506b006ab0f82b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
12 | `.github/workflows/dokuzuncu-akilli-tekrar-test.yml` | `ad54773ea6d7bb46d0c5deb51454fe8189f87c32` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
13 | `.github/workflows/epg-gunluk.yml` | `d43d5c469b54b8ef89794e8fcc2c2cee9b0d84b9` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
14 | `.github/workflows/epg-pages.yml` | `00e956c71c389d015209293b5de5b325cd4cb116` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
15 | `.github/workflows/felaket-kurtarma-tatbikati.yml` | `53081c63ade88138049d8da1fef43ecfab588b5f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
16 | `.github/workflows/genel-aday-medya-test.yml` | `8d313fa5936799f86fd026831a3a149cbb0c250b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
17 | `.github/workflows/genis-kanal-tarama.yml` | `ffea4c826bf1ea9f2b586ddbd279d169f930b9b1` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
18 | `.github/workflows/ibo-bagimsiz-test-listesi.yml` | `be63acf659a9b50c68a8b01ff5434a3151877a8f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
19 | `.github/workflows/ibo-epg-kimlik-denetimi.yml` | `67ffc18c6cd79a5ea0960de72aeeecbc98fab7d7` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
20 | `.github/workflows/ibo-yedek-kalite.yml` | `da48c5195c35094a2a519feafd6b51f20f526edc` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
21 | `.github/workflows/iptv-test.yml` | `5cd014cb94e68be22f5f68b07618920c82fee740` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
22 | `.github/workflows/k1-protected-write-tests.yml` | `52bad78597f6df07b530167a21a6256d6107bd6b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
23 | `.github/workflows/kanal-kararlilik.yml` | `c968204d3d9d54cf218d92954189c9e6945a509f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
24 | `.github/workflows/kaynak-puanlama-kontrol.yml` | `0ffc33a27ff7d6bb459fbfa608db1095218379f0` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
25 | `.github/workflows/madsc-01-guvenlik.yml` | `ae91b6c47745fe46659105f96cd28e6aca9d44d9` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
26 | `.github/workflows/madsc-02-kesif.yml` | `f9970a874258c1cbd1c59f73fa427136ff2d53d4` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
27 | `.github/workflows/madsc-03-kanal-test.yml` | `228d53500e99bc9953ab6d535b7809523a1854f0` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
28 | `.github/workflows/madsc-04-arsiv-yedek.yml` | `7b4d62f33c6438236f418f8e60f779a22d05a9d3` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
29 | `.github/workflows/madsc-05-genel-bakim.yml` | `32560f27ff29830f16f41f7a1ed0b8476f0b362f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
30 | `.github/workflows/madsc-11599-yedek-geri-yukle.yml` | `fb04cdcc5abede182df764804e8a5055956dcece` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
31 | `.github/workflows/madsc-ana-liste-saglik.yml` | `6ba3cc60b74f26d3e7dcfecdf84d0cd2ce85baf7` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
32 | `.github/workflows/madsc-arsiv-yedek-aktarim.yml` | `d2062b168db134177cb1683d86eaafa2c2937d54` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
33 | `.github/workflows/madsc-aylik-merkezi-denetim.yml` | `8cca9b93855c1e2184863b8e59b07817e546366f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
34 | `.github/workflows/madsc-birlesik-kesif.yml` | `da472ae0e45aa0d3c03a7dc8f9833bf43f733902` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
35 | `.github/workflows/madsc-cuma-ana-liste-denetimi.yml` | `b14aca32502179ae27e2399b0278502c512c2984` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
36 | `.github/workflows/madsc-documentation-check.yml` | `0678a8a201eb194503f9097265fe37e68b1e4d3d` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
37 | `.github/workflows/madsc-genis-kaynak-kontrol.yml` | `396d33dd8d5f3440dc81ae76abb91fc0d43f6a94` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
38 | `.github/workflows/madsc-hizli-on-kontrol.yml` | `92ba7ce2731d544b7361fb8877c531d4c4911840` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
39 | `.github/workflows/madsc-ibo-3-5281.yml` | `4b0745614a11625f020baa39b832983ce5fc42ca` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
40 | `.github/workflows/madsc-ibo-354-classify.yml` | `165bb7fc69775be790beab972dc68e92cf40c2c3` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
41 | `.github/workflows/madsc-ibo-364-355-364.yml` | `7dff039f081b93c0efab2ced1ab8e873f021e496` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
42 | `.github/workflows/madsc-ibo-398-16-49.yml` | `7b3dd19eb1fc1651e4f921e5b4f1c79fa0c91dc1` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
43 | `.github/workflows/madsc-ibo-530-archive.yml` | `85bb9898838d253c99bc10f7d98468d71a522a37` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
44 | `.github/workflows/madsc-ibo-6115-second.yml` | `4591be38fed55b81e6bf8d3a22319c262f11c01b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
45 | `.github/workflows/madsc-ibo-ilk-239.yml` | `7cfc6061bb1714c08cd52ff130a54c36bcee15c7` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
46 | `.github/workflows/madsc-ibo-kararlar-grup1.yml` | `d79a157a13c667d6dd60a0c4837cca2c1da4f220` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
47 | `.github/workflows/madsc-ibo-second-voice.yml` | `ad14d3daf071f8503651581ba93f6b6008fa0aee` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
48 | `.github/workflows/madsc-otomatik-devam.yml` | `4cf99f3ce1801588c24082c2122b1d781192e7dd` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
49 | `.github/workflows/madsc-rule24-test.yml` | `8092ea97979380e7af71aaa9383dc28f41c86ab8` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
50 | `.github/workflows/madsc-sistem-saglik-denetimi.yml` | `c3c18155d13c2ca5e1a76304729fbcc6739849a5` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
51 | `.github/workflows/madsc-son-kontrol-kurtarma-teshis.yml` | `471540a306c4146fa12123510a4c70dcfe1356eb` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
52 | `.github/workflows/madsc-son-kontrol.yml` | `08871f1b397184459a093606c2519e1c19e5167a` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
53 | `.github/workflows/madsc-toplu-butunluk.yml` | `d7456c7a5526350b0d52e39b6708cf288d209dbf` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
54 | `.github/workflows/madsc-tum-sistem-yedek.yml` | `f56db59dc9a8a12f21296a80ea53b602340454ef` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
55 | `.github/workflows/madsc-turk-kanal-geri-sec.yml` | `ee4538c2b9e11f5589d8babacd9f3ff39457cc9b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
56 | `.github/workflows/madsc-uc-asama.yml` | `93c3a87372b1dfbe80ba9e59dabc2180511112ae` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
57 | `.github/workflows/madsc-yedek-turk-ayir.yml` | `67b12b441fab5fa57eded1a7684ebf24e7d819c2` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
58 | `.github/workflows/madsc-yedekler-aktarim-test.yml` | `e4de46aa7edbd84b8dc3bdda0e3d75a39421118b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
59 | `.github/workflows/madsc-yedekler-sayi-duzelt.yml` | `feb92ccf12c62b3818cac164f0effe319083872f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
60 | `.github/workflows/oncelikli-kanal-dogrulama.yml` | `ae7c910e5f7d840a6bceb0ab99cad3c9d414d63f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
61 | `.github/workflows/onikinci-hata-siniflandirma-test.yml` | `41bf9c8b94b7f1e4ad045b1708cf52bb6edbe8da` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
62 | `.github/workflows/publish-iptv-png-logos.yml` | `7b8fa621b2cfaf151e26855d92a6ccbc326d6ed3` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
63 | `.github/workflows/sekizinci-tekrar-raporu-test.yml` | `64665da9b8f4602e0b9310e012c835729a73afa7` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
64 | `.github/workflows/sozcu-akit-ozel-test.yml` | `b74d2db6f7acced67f514cae037be44b9722059d` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
65 | `.github/workflows/test-13-kaynak-degisiklik.yml` | `44c95db225dca48f6a50a72f72f6e4ce2f7d5457` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
66 | `.github/workflows/test-14-istikrar.yml` | `4915ba2ac06a188a9ae4dddcfc46fda78f37515b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
67 | `.github/workflows/test-15-logo-epg.yml` | `de27646659c70b0206f998ac2b69a3aa948682d2` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
68 | `.github/workflows/test-16-workflow-safety.yml` | `902925df650f77f80e618a80da101cdeb68da23e` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
69 | `.github/workflows/test-17-candidate-summary.yml` | `70d1ae2d665ebc398d1c41d7134ea7c89a3186f1` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
70 | `.github/workflows/test-18-change-simulation.yml` | `e39f6603c188d72f7ebb87f8b1cfbb858962d553` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
71 | `.github/workflows/test-19-integration.yml` | `bd8c5c1401661fc1dff468274d9e4f6ebe963279` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
72 | `.github/workflows/test-20-full-integration.yml` | `41d5fd3ff8024f960a4c4f5e15810ea48d1fb3b8` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
73 | `.github/workflows/test-21-functional-e2e.yml` | `f13904e84f0116b53120b792a89e1a4377f6dbc3` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
74 | `.github/workflows/test-22-real-playlist.yml` | `f1fe0cc001eac113f56acffaece5850d3eba515d` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
75 | `.github/workflows/test-23-live-stream.yml` | `412b3f263bab8d8f7c96f2776e56aa939a6b73b2` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
76 | `.github/workflows/test-24-system-audit.yml` | `4cdb0dce456bd49cbb082c9506f7019f62776dc7` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
77 | `.github/workflows/test-25-full-project-readonly.yml` | `c00a6295182f7b31b7a0bc95af7056c0f20cae47` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
78 | `.github/workflows/test-26-automation-safety.yml` | `ada482112b58e47bd56b8c742ad08633e1f3b840` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
79 | `.github/workflows/test-27-pipeline-contract.yml` | `41a24282bd6785cba1025d32040ccb1c994bf38a` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
80 | `.github/workflows/test-28-approval-gate.yml` | `d9253678d662c7bb2caefe12286ce15d5e6f702f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
81 | `.github/workflows/test-29-write-path-audit.yml` | `93b083583024215f0340b2d70974732ab9478c4d` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
82 | `.github/workflows/test-30-write-risk-report.yml` | `97879b5d4f95546b521ecb5b034571fe230374dd` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
83 | `.github/workflows/test-31-protected-write-gate.yml` | `eca623c47a4cb81e88e14d59f58862c8e110e6d1` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
84 | `.github/workflows/test-32-unapproved-write-regression.yml` | `ca2bd0ed80045bc3ce0c027397172e16e28bdb5e` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
85 | `.github/workflows/test-33-all-write-paths.yml` | `76d1d09da818fe8b8fe531167e8dd30b9a8717a2` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
86 | `.github/workflows/test-34-protected-write-regression.yml` | `453f8ca6c0bcde59ef8fd4afc22fcc72baafc002` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
87 | `.github/workflows/test-35-remaining-write-gate.yml` | `8bec3b96e6b084f6f2b44f9bd5af3af7bfd103c4` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
88 | `.github/workflows/test-36-system-integration-audit.yml` | `f83899a4733d6bf979cd7ee74835ace179f6708e` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
89 | `.github/workflows/test-37-indirect-write-audit.yml` | `36b1c85749f7358efeb45962ffae0cae88525d56` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
90 | `.github/workflows/test-38-audit-selftest.yml` | `bbe368fffdf354d9f61d654f009dcd749da8183f` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
91 | `.github/workflows/test-39-protected-playlist.yml` | `2d495c94091c7c2194686c41181ac981f5a5d8aa` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
92 | `.github/workflows/test-kanal-adaylari.yml` | `324040ec251f5bc9a0dc5c652312500d6cf37d67` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
93 | `.github/workflows/toplu-sistem-kontrol.yml` | `34cf72108fb7aea4a1abde31027cfd3a859db43d` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
94 | `.github/workflows/vod-guncelle.yml` | `78c3b8aa8e27b9f25e439337e2e94be9468b6f3b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
95 | `.github/workflows/yedek-geri-yukleme-tatbikat.yml` | `08a38be283550147e0e267f72fcc1291bfc9f88c` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
96 | `.github/workflows/yedekler-yeniler-medya-kontrol.yml` | `43fd2b8bc0f6f4173bb3dde16744d10376d1027b` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
97 | `.github/workflows/yeni-aday-on-test.yml` | `a0d0625a65233e35f37dbcda25e6a3fd71915f75` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
98 | `.github/workflows/yeni-kanal-arama-2026.yml` | `89f74c54f72f48583ff5abf1d148e3cc5b57f8f6` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok
99 | `.github/workflows/yeniler-guvenli-arama.yml` | `fabb2cf59223a983ed22046d19617a210efc16f2` | BLOCKED | Ayrı eski/yeni fixture yürütme receipt'leri ve artifact/yan-etki kanıtı yok

**Toplam: 99; ACCEPTED: 0; BLOCKED: 99.** Bu tablo hiçbir workflow'u çalıştırmaz veya üretim verisini değiştirmez.
