---
title: "اختبار AWUS036AXML عمليًا: بطاقة مركّبة Wi-Fi 6 + بلوتوث على ASUS GX10 (ARM64 / Ubuntu 24.04) — تقرير أمين: AP ثابت والحقن فاشل"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "اختبار AWUS036AXML (Wi-Fi + بلوتوث) على ASUS GX10 / Ubuntu 24.04 ARM64: AP وWPA3 وmonitor صالحة، لكن injection يفشل ويتعذّر التقاط handshake، فلا يُنصح بها لاختبار الاختراق."
faq:
  - question: "هل تستطيع AWUS036AXML حقن الحزم (packet injection)؟"
    answer: "على منصة اختبارنا (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia) لا. فـ aireplay-ng --test يردّ No Answer وFound 0 APs؛ وعند تحديد AP واختباره نقطة نقطة لا يعطي إلا No such BSSID available. وحتى عندما يرى المسح العادي تلك الـ AP (نحو -54 dBm)، فإن البطاقة في سياق أدوات الحقن لا تلتقط beacon الخاص بها، فيتعذّر deauth والتقاط handshake (0 نتيجة). والسبب الجذري ارتداد mac80211 chanctx في kernel 6.16+، لا عجز خِلقي في الرقاقة عن الحقن؛ وبطاقة AWUS036AXM تعطي النتيجة نفسها. إن احتجت الحقن فاختر AWUS036EACS أو ACH أو ACS."
  - question: "هل يعمل بلوتوث AWUS036AXML على Ubuntu؟"
    answer: "البلوتوث صالح بالاختبار على هذا الجهاز: فبـ bluetoothctl / hciconfig تأكّد أن متحكّم hci بحالة UP، ويمكنه مسح أجهزة BLE والبلوتوث الكلاسيكي، كما يعمل Wi-Fi والبلوتوث معًا (تعايش). وهي جهاز مركّب Wi-Fi + بلوتوث؛ وتنبيه: إعادة التوصيل قد تعلق أحيانًا في WiFi probe فلا تظهر واجهة wlx، ويكفي إعادة التوصيل في منفذ USB آخر لاستعادتها."
  - question: "هل تحتاج AWUS036AXML إلى تثبيت تعريف على Ubuntu 24.04؟"
    answer: "لا. فتعريف mt7921u مدمج في kernel 6.17، وبعد التوصيل يُظهر dmesg أن mt7921u أعاد تسمية الواجهة إلى wlx مع MAC (USB ID 0e8d:7961)، دون DKMS ودون تجميع. والتعريف لا يوفّر وضعي IBSS وmesh."
  - question: "هل يمكن لـ AWUS036AXML فتح AP ودعم WPA3؟"
    answer: "نعم، وهذا أثبت استخداماتها. اتصل iPhone وauthorized على كلٍّ من 2.4 GHz (802.11n، MCS 10) و5 GHz VHT80 (VHT-NSS2)؛ وبـ sae_pwe=0 اتصل iPhone 15 Pro بوضع WPA3-SAE (MFP: yes؛ اختُبر على 2.4 GHz و6 GHz، ولم يُختبر على 5 GHz)؛ وعند توازي STA + AP كان ping جانب STA نحو 4.4 ms. ورغم تصنيفها رقاقة Wi-Fi 6، فإن 6 GHz band صالح بالاختبار على هذا الجهاز (أقمنا AP على 6135 MHz، واتصل iPhone 15 Pro بـ 802.11ax وحصل على IP)."
  - question: "ما الفرق بين AWUS036AXML وAWUS036AXM، وأيّهما أختار؟"
    answer: "على هذه المنصة سلوك Wi-Fi في البطاقتين متطابق: التعريف mt7921u نفسه، والحقن فاشل في كليهما، واستقبال monitor ضعيف نسبيًا في كليهما، وAP وWPA3 وVIF صالحة في كليهما. والفرق أن AXML تزيد بالبلوتوث (صالح بالاختبار على هذا الجهاز) وأن 6 GHz band صالح فيها بالاختبار، أما بلوتوث AXM و6 GHz فلم يُختبرا منفردين في هذه الجولة. لـ AP صرف أو اتصال عام اختر أيًّا منهما؛ وللحقن أو handshake لا تختر أيًّا منهما."
draft: false
---

{{< tldr >}}AWUS036AXML على ASUS GX10 / Ubuntu 24.04 ARM64 صالحة في AP وWPA3 وVIF وmonitor السلبي، والبلوتوث و6 GHz band صالحان بالاختبار على هذا الجهاز، لكن injection فشل فعليًا (No Answer / Found 0 APs)، فيتعذّر deauth أو التقاط handshake، ولا يُنصح بها لاختبار الاختراق؛ وموضعها AP واتصال عام صرف.{{< /tldr >}}

ALFA AWUS036AXML هي الطراز المركّب الوحيد «MediaTek Wi-Fi 6 + بلوتوث» ضمن هذه الدفعة من البطاقات التسع. وهي مع AWUS036AXM الخالية من البلوتوث من جيل الرقاقة نفسه (MT7921، بتعريف `mt7921u`)، والفرق مجرد مجموعة بلوتوث إضافية. وأكثر ما يسأل عنه العملاء ما يزال تلك الأسئلة الثلاثة: هل يدخل monitor؟ هل يستطيع injection؟ هل يستطيع فتح AP؟ وهذه المقالة تفرد AWUS036AXML وحدها، وتختبرها بندًا بندًا على ASUS GX10 (ARM64) مع Ubuntu 24.04، لتبيّن ما تستطيع وما لا تستطيع مرة واحدة بوضوح، وبخاصة أهمّ قيد: **الحقن (injection) يفشل على هذه المنصة**.

ولنوضّح الموضع أولًا: أُجريت كل القياسات أدناه على أجهزة Yupitek الخاصة وشبكة مكتبها الخاصة (SSID `YUPITEK`)، تجاه هاتف اختبار مملوك (iPhone 7 Plus، واختُبر WPA3 أيضًا على iPhone 15 Pro). وهذا تحقق عتادي من الموزّع لتوافق المنتج وحدود قدراته، لا درس تشغيل على شبكات الغير. وكل اختبارات monitor وAP والحقن الذاتية أُجريت في بيئة خاصة مغلقة تجاه أجهزة مملوكة.

## أولًا. هذه البطاقة ومنصة الاختبار

- **منصة الحوسبة**: ASUS GX10 (ARM64 / aarch64)
- **نظام التشغيل**: Ubuntu 24.04 LTS
- **إصدار النواة**: kernel 6.17.0-1014-nvidia
- **البطاقة المختبَرة**: ALFA AWUS036AXML (MediaTek MT7921AUN، Wi-Fi 6 / 2x2 / +BT)
- **جهاز الاختبار**: Apple iPhone 7 Plus (وأُعيد اختبار WPA3-SAE على iPhone 15 Pro)
- **بيئة الاختبار**: شبكة مكتب خاصة، SSID `YUPITEK`، 2.4GHz ch5 / 5GHz ch36، ch157
- **مدة الاختبار**: قياس فعلي على الجهاز من 2026-11-16 إلى 2026-11-18

كل النتائج مسجَّلة بأرقام أو حالات مقيسة فعلًا، لا بتخمين من ورقة المواصفات؛ وعناوين MAC مُخفاة في المخرَجات بـ `xx`.

## ثانيًا. العتاد والتعريف: MT7921AUN، جاهز بمجرد التوصيل

| البند | المواصفة |
|---|---|
| الطراز | AWUS036AXML |
| الرقاقة | MediaTek MT7921AUN |
| USB ID | `0e8d:7961` (MediaTek Inc. Wireless_Device) |
| التعريف in-kernel | `mt7921u` |
| الجيل / التدفقات | Wi-Fi 6 / 2x2 (2T2R) |
| البلوتوث | موجود (جهاز مركّب BT + WiFi؛ بالاختبار على هذا الجهاز: متحكّم hci بحالة UP، ويمسح أجهزة BLE والبلوتوث الكلاسيكي، وتعايش WiFi+BT) |
| تعداد USB | USB 3 |
| تسمية الواجهة | `wlx<MAC>` (مثل: `wlx00c0cabd65b9`) |

التعرّف مباشر: بعد التوصيل تُظهر `lsusb` الـ USB ID الخاص بـ MediaTek، وتُظهر `dmesg` تحميل `mt7921u` وإعادة تسمية الواجهة:

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

نقطتان مهمّتان. الأولى بلا تجميع: فـ AWUS036AXML تسير على تعريف `mt7921u` المدمج في kernel 6.17، وتُعرَّف بمجرد توصيلها، دون التعامل مع أي وحدة out-of-tree DKMS على aarch64، وهذا موفِّر خاصّة على منصة ARM64. والثانية أنها تُعدَّد بـ USB 3 (بينما كان كبل OTG في بعض طرازات الجيل السابق بـ USB 2.0 فقط)، فعرض نطاق النقل ليس عنق الزجاجة.

ونضيف نقطة يكثر الخطأ فيها: فـ AWUS036AXML مصنَّفة رقاقة Wi-Fi 6 (لا 6E)، لكن **6 GHz band صالح بالاختبار على هذا الجهاز** — أقمنا AP على 6135 MHz، واتصل iPhone 15 Pro بـ 802.11ax وحصل على IP. والبلوتوث أيضًا صالح بالاختبار: فبـ `hciconfig` / `bluetoothctl` ظهر متحكّم hci بحالة UP، ويمسح أجهزة BLE والبلوتوث الكلاسيكي، ويعمل Wi-Fi والبلوتوث معًا (تعايش).

واستعلم عن أوضاع الواجهة المدعومة، فترى تفصيلًا ذا معنى للاختيار، هو غياب IBSS وmesh point:

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

أي أن managed وAP وmonitor وP2P موجودة، لكن وضعي ad-hoc (IBSS) و802.11s mesh لا يوفّرهما تعريف `mt7921u` أصلًا. فالعميل الذي يريد تجارب mesh / IBSS يستبعد هذه البطاقة مباشرة (ولينظر إلى ACM / ACHM بتعريف `mt76`).

## ثالثًا. القدرات المختبَرة: Monitor / AP / WPA3، والقيد الأمين على injection

القدرات الأساسية دفعة واحدة:

| القدرة | 2.4GHz | 5GHz | الشرح |
|---|---|---|---|
| Monitor | ✅ (ضعيف) | ✅ (ضعيف) | يمكن التسجيل الجانبي لـ beacon؛ وكثيرًا ما تفوت حزم client / data |
| **Injection** | ❌ **فاشل** | ❌ **فاشل** | حقن / deauth عبر `aireplay-ng` لا يعمل؛ السبب الجذري ارتداد mac80211 chanctx في kernel 6.16+ (لا عجز خِلقي في الرقاقة) |
| AP (نقطة وصول) | ✅ مع 802.11n | ✅ VHT80 (80MHz) | اتصل iPhone 7 Plus، `authorized: yes` |
| WPA3-SAE | ✅ | لم يُختبر | اتصل iPhone 15 Pro، `MFP: yes` (`sae_pwe=0`)؛ واختُبر أيضًا على 6 GHz (ch37، 6135 MHz) |

### Monitor: يدخل النطاقين، لكن استقباله ضعيف

تستطيع AWUS036AXML الدخول في وضع monitor على 2.4GHz (ch1 / 6 / 11) و5GHz (ch36 / 149 / 157)، والتسجيل الجانبي لـ beacon بلا مشكلة. وتدفق الإعداد هو خطوات `iw dev` الأربع القياسية:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # على 2.4GHz استخدم set channel 6
```

ولنقلها بأمانة: استقبال monitor فيها أضعف بوضوح من MT7612U (ACM) من الدفعة نفسها، أو من AXER (Wi-Fi 6). فـ beacon يُلتقط، لكن حزم client / data كثيرًا ما تفوت؛ وعند المسح القافز بـ `airodump-ng` يسهل أن تفوت بعض الـ AP. وعمليًا يُنصح بتثبيت قناة واحدة (`-c <ch>`) بدل القفز، فيكون الحصاد أثبت. كما أن `iw info` في وضع monitor يبلّغ أن txpower مجرد 3 dBm، وهذا **تبليغ وهمي** (قدرة TX العتادية الفعلية نحو 20–23 dBm، وقد تحقّق منها `txpower_sku`)، وليست القدرة قد خُفِضت إلى 3 dBm فعلًا، وسنعود إلى هذا في «الملاحظات» لاحقًا.

### AP (نقطة وصول): 2.4GHz مع HT، و5GHz يصل إلى VHT80

AP هو أثبت ما في AWUS036AXML. فعلى 2.4GHz يمكن الإبقاء مباشرة على 802.11n (HT)، دون الحاجة إلى إطفاء HT كما في ACHM ذات الهوائي الواحد؛ وعلى 5GHz يمكن الفتح إلى VHT 80MHz. وعلى النطاقين اتصل iPhone 7 Plus فعليًا وكان `authorized: yes`.

إعدادات hostapd المفتاحية لـ 5GHz VHT80:

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

بعد الاتصال فعليًا كان VHT-NSS2، 80MHz. وفي نسخة 2.4GHz يُبدَّل `hw_mode` إلى `g` و`channel=6`، مع الإبقاء على `ieee80211n=1` و`ht_capab=[HT20]`، واتصال iPhone كان MCS 10 (802.11n).

### WPA3-SAE: صالح، تذكّر sae_pwe=0

بتبديل `wpa_key_mgmt` في AP إلى `SAE`، وإضافة `ieee80211w=2` و`sae_pwe=0`، يمكن فتح WPA3-SAE. وفعليًا اتصل iPhone 15 Pro على 2.4 GHz (وعلى 6 GHz؛ 5 GHz لم يُختبر)، `authorized: yes`، `MFP: yes`. و`sae_pwe=0` من أجل التوافق مع طرازات iPhone الأقدم، وهذا الفخّ نفسه في ACHM، إذ كثيرًا ما لا تتصل الأجهزة الأقدم عند `sae_pwe=2`.

### VIF: اتصال بالإنترنت وتشغيل نقطة وصول معًا، ممكن

تدعم AWUS036AXML تعايش عدة واجهات. فبإنشاء AP VIF (بـ MAC مختلف، unmanage)، واتصال الواجهة الأساسية بـ Wi-Fi، وفتح AP على القناة نفسها، كان عند اتصال iPhone 7 Plus بـ AP VIF أن ping جانب STA تجاه `YUPITEK` 4.4 ms. فلحاجة «بطاقة واحدة تتصل بالإنترنت وتشارك نقطة وصول في آن»، فهي قائمة.

### قيد أمين: injection يفشل على هذه المنصة

هذه أحقّ نقطة بالتوضيح في AWUS036AXML (وتوأمها الخالي من البلوتوث AXM). فعلى ASUS GX10 + kernel 6.17، أجرينا اختبار injection ذاتيًّا على بيئتنا الخاصة، وكانت النتيجة الفشل:

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

وحتى بتحديد BSSID الخاص بـ AP بيتنا واختباره نقطة نقطة، لا يردّ إلا `No such BSSID available`. والمفتاح: أن المسح العادي يرى تلك الـ AP بوضوح (الإشارة -54 dBm)، لكنها بمجرد الدخول في سياق أدوات الحقن «لا تسمع» beacon الهدف، فلا يخرج deauth، وعدد التقاط 4-way handshake يكون 0.

وهذا ليس معاملًا سيئ الضبط، ولا عطل بطاقة مفردة. فالسبب الجذري الحقيقي في **طبقة البرمجيات**: فبعد kernel 6.16 ظهر ارتداد في channel context (chanctx) ضمن mac80211، جعل التعريف stock لا يلتقط beacon الهدف في سياق الحقن، فحكم `aireplay-ng` بـ `No Answer`، و**ليس عجزًا خِلقيًّا في رقاقة MT7921 عن الحقن**. والظاهرة مسجَّلة في morrownr/USB-WiFi issue #387، وتحليل السبب الجذري في morrownr/mt76 issue #18. وتشير الاختبارات المجتمعية إلى أن التعريف git / patched على الطراز نفسه يُشغّل active monitor مع الحقن، لكن firmware لرقاقة MT7921 يبقى قافلًا الحقن على معدّلي 1 Mbps / 6 Mbps الأساسيين، فلا يمكن الحقن بـ HT / VHT؛ وطرازا AXM وAXML كلاهما أصابهما الأمر نفسه على **stock kernel 6.17**، وحتى 2026-11-18 يتعذّر حلّه بالمعاملات.

لذا، فإن كل ما يمسّ injection — مثل deauth والتقاط WPA handshake واختبار الاختراق القائم على الحقن — يتعذّر على AWUS036AXML على هذه المنصة. ولمثل هذه الاستخدامات، استخدم الطرازات التي يصلح حقنها فعليًا (انظر الاختيار أدناه).

### لمحة عن الأوضاع المتقدمة الأخرى

| الوظيفة المتقدمة | الحالة | الشرح |
|---|---|---|
| VIF (STA + AP بالتوازي) | ✅ | القناة نفسها ch36؛ عند اتصال iPhone كان STA ping 4.4 ms |
| التقاط WPA handshake | ❌ | فشل الحقن ← لا يخرج deauth، وhandshake 0 |
| Active monitor | 🟡 | `set monitor active` مقبول، لكن ACK غير متحقَّق منه |
| Ad-hoc (IBSS) | N/A | تعريف `mt7921u` لا يملك هذا الوضع |
| Mesh (802.11s) | N/A | تعريف `mt7921u` لا يملك هذا الوضع |
| Wi-Fi Direct (P2P) | ⬜ | التعريف يعلن دعمه، ويحتاج جهازًا ثانيًا، فيُتخطّى |

## رابعًا. ملاحظات التركيب المزدوج للبلوتوث والاستخدامات المناسبة / غير المناسبة

### أثر جانبي عملي لبطاقة BT + WiFi المركّبة

تتضمن AWUS036AXML بلوتوثًا، وهي إحدى بطاقتين مركّبتين في هذه الدفعة (والأخرى EACS من Realtek). والبلوتوث صالح بالاختبار على هذا الجهاز (متحكّم hci بحالة UP، ويمسح أجهزة BLE والبلوتوث الكلاسيكي، ويتعايش مع Wi-Fi، كما سبق)، ونضيف هنا أثرًا جانبيًّا عمليًّا للجهاز المركّب: فإعادة التوصيل قد تعلق أحيانًا في WiFi probe فلا تظهر واجهة `wlx`، والعرَض أن `ls /sys/class/net` لا يرى البطاقة بعد إعادة التوصيل. والحل بسيط: **أعِد التوصيل في منفذ USB آخر**، فتُعدَّد عادةً بصورة طبيعية.

وحركة صغيرة أخرى جديرة بالتذكّر: في وضع AP، إن توقّف الهاتف فجأة عن رؤية الـ SSID، فافصل البطاقة وأعِد توصيلها **مرة** للتصفير، دون تغيير الإعداد. (تنبيه: القيمة 3 dBm المبلَّغة في monitor آنفًا وهمية، ليست قدرة فعلية، وليست سبب اختفاء الـ SSID.)

### قاعدة أمان المنصة

- لا تُشغّل أبدًا `airmon-ng check kill`: فهو يُغلق NetworkManager ويقطع اتصال GX10 كلّه. لا تُحرّك إلا واجهة `wlx*` الخارجية، دون المساس بخطّ الاتصال الخارجي المدمج.
- `hcxdumptool 8.x` على هذا الجهاز يُخفق بـ `failed to arm` (باستثناء AWUS036EACS على 2.4 GHz) (تعارض تعداد بطاقة GX10 المدمجة ثلاثية النطاق + غياب active-monitor في التعريف)، وهذه علّة على مستوى المنصة كلها لا علاقة لها بـ AXML؛ وعند الحاجة إلى وظيفة مشابهة، استخدم `airodump-ng` مع أدوات aircrack-ng الأخرى.
- إضافة لـ ARM64: `aircrack-ng` يلزم تجميعه من المصدر، و`wifite` يُنصح بنسخة git لتجاوز تعارض تبعيات apt.

### لمحة عن المناسب / غير المناسب

| السيناريو المناسب | السيناريو غير المناسب |
|---|---|
| AP / نقطة وصول صرفة (2.4G مع HT، 5G VHT80) | injection / deauth |
| نقطة WPA3-SAE | التقاط WPA handshake |
| اتصال managed عام | البطاقة الرئيسية لاختبار اختراق قائم على الحقن |
| monitor سلبي / جرد طيفي (بتثبيت قناة واحدة) | تجارب mesh / IBSS |
| تعايش STA + AP (VIF، اتصال ومشاركة معًا) | التسجيل الجانبي بعيد المدى المحتاج إلى استقبال قوي |

## خامسًا. توصية الاختيار (بالعودة إلى الجدول الشامل)

بإعادة AWUS036AXML إلى صورة البطاقات التسع الكاملة، يتضح موضعها: MediaTek ثابتة الاتصال، بلا تجميع، وتفتح AP بـ VHT80 على النطاقين، فهي بطاقة «اتصال صرف / AP صرف» كفؤة؛ ومتى مسّ الأمر injection، فليست ساحتها.

| الحاجة | الطراز المقترح |
|---|---|
| AP صرف / اتصال عام (بلا حقن) | **AWUS036AXML / AWUS036AXM** (هذه البطاقة مناسبة) |
| injection + handshake (اختبار اختراق) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| تجربة mesh / IBSS | AWUS036ACM / AWUS036ACHM |
| أقوى استقبال / monitor بعيد المدى | AWUS036AXER / AWUS036ACH |

إن كنت تفاضل بين البطاقات التسع، فللمصفوفة الكاملة Monitor / Injection / AP / WPA3 والاختيار بحسب الاستخدام، انظر الجدول الشامل:

- [أشمل اختبار 2026: مصفوفة كاملة لتسع بطاقات ALFA لاسلكية على ASUS GX10](/ar/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

تجنّب في جملة: **للحقن أو handshake، لا تختر AWUS036AXML / AWUS036AXM**؛ وللاتصال الصرف أو تشغيل نقطة وصول، فهي جيدة جدًّا.

## الأسئلة الشائعة (FAQ)

**س1. هل تستطيع AWUS036AXML حقن الحزم (packet injection)؟**
على منصة اختبارنا (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia) لا. فـ `aireplay-ng --test` يردّ `No Answer` وFound 0 APs؛ وعند تحديد AP واختباره نقطة نقطة لا يعطي إلا `No such BSSID available`. وحتى عندما يرى المسح العادي تلك الـ AP (نحو -54 dBm)، فإن البطاقة في سياق أدوات الحقن لا تلتقط beacon الخاص بها، فيتعذّر deauth والتقاط handshake (0 نتيجة). والسبب الجذري ارتداد mac80211 chanctx في kernel 6.16+، لا عجز خِلقي في الرقاقة عن الحقن؛ وبطاقة AWUS036AXM تعطي النتيجة نفسها. إن احتجت الحقن فاختر AWUS036EACS أو ACH أو ACS.

**س2. هل يعمل بلوتوث AWUS036AXML على Ubuntu؟**
البلوتوث صالح بالاختبار على هذا الجهاز: فبـ `bluetoothctl` / `hciconfig` تأكّد أن متحكّم hci بحالة UP، ويمكنه مسح أجهزة BLE والبلوتوث الكلاسيكي، كما يعمل Wi-Fi والبلوتوث معًا (تعايش). وهي جهاز مركّب Wi-Fi + بلوتوث؛ وتنبيه: إعادة التوصيل قد تعلق أحيانًا في WiFi probe فلا تظهر واجهة `wlx`، ويكفي إعادة التوصيل في منفذ USB آخر لاستعادتها.

**س3. هل تحتاج AWUS036AXML إلى تثبيت تعريف على Ubuntu 24.04؟**
لا. فتعريف mt7921u مدمج في kernel 6.17، وبعد التوصيل يُظهر dmesg أن mt7921u أعاد تسمية الواجهة إلى `wlx` مع MAC (USB ID `0e8d:7961`)، دون DKMS ودون تجميع. والتعريف لا يوفّر وضعي IBSS وmesh.

**س4. هل يمكن لـ AWUS036AXML فتح AP ودعم WPA3؟**
نعم، وهذا أثبت استخداماتها. اتصل iPhone وauthorized على كلٍّ من 2.4 GHz (802.11n، MCS 10) و5 GHz VHT80 (VHT-NSS2)؛ وبـ `sae_pwe=0` اتصل iPhone 15 Pro بوضع WPA3-SAE (`MFP: yes`؛ اختُبر على 2.4 GHz و6 GHz، ولم يُختبر على 5 GHz)؛ وعند توازي STA + AP كان ping جانب STA نحو 4.4 ms. ورغم تصنيفها رقاقة Wi-Fi 6، فإن 6 GHz band صالح بالاختبار على هذا الجهاز (أقمنا AP على 6135 MHz، واتصل iPhone 15 Pro بـ 802.11ax وحصل على IP).

**س5. ما الفرق بين AWUS036AXML وAWUS036AXM، وأيّهما أختار؟**
على هذه المنصة سلوك Wi-Fi في البطاقتين متطابق: التعريف mt7921u نفسه، والحقن فاشل في كليهما، واستقبال monitor ضعيف نسبيًا في كليهما، وAP وWPA3 وVIF صالحة في كليهما. والفرق أن AXML تزيد بالبلوتوث (صالح بالاختبار على هذا الجهاز) وأن 6 GHz band صالح فيها بالاختبار، أما بلوتوث AXM و6 GHz فلم يُختبرا منفردين في هذه الجولة. لـ AP صرف أو اتصال عام اختر أيًّا منهما؛ وللحقن أو handshake لا تختر أيًّا منهما.

## قراءات إضافية

(الروابط تُنشَر تباعًا، قيد الإنشاء)

- النسخة الخالية من البلوتوث بالرقاقة نفسها: [اختبار AWUS036AXM منفردًا](/ar/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- بدائل يصلح فيها الحقن: [اختبار AWUS036EACS منفردًا](/ar/blog/awus036eacs-asus-gx10-ubuntu-test-report/)، [اختبار AWUS036ACH منفردًا](/ar/blog/awus036ach-asus-gx10-ubuntu-test-report/)، [اختبار AWUS036ACS منفردًا](/ar/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- مقالة موضوعية: [بلا تثبيت تعريف: تفعيل وضعي Monitor وAP على Ubuntu (ARM64)](/ar/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- مقالة موضوعية: [اتصال WPA3-SAE وممارسة handshake (تحقق في بيئة خاصة)](/ar/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- الجدول الشامل Hub: [المصفوفة الكاملة لتسع بطاقات ALFA على ASUS GX10](/ar/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*جهة الاختبار: Yupitek (موزّع ALFA Network في تايوان) · منصة الاختبار: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia · جهاز الاختبار: Apple iPhone 7 Plus (واختُبر WPA3 على iPhone 15 Pro) · بيئة الاختبار: شبكة مكتب خاصة (SSID YUPITEK). هذه المقالة تحقق من توافق المنتج وقدراته، لا درس تشغيل على شبكات الغير.*
