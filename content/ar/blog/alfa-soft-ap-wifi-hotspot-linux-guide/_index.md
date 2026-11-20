---
title: "الدليل الكامل لـ Soft AP من ALFA Network 2026: إنشاء نقاط اتصال WiFi على Kali Linux و Ubuntu و Debian و Raspberry Pi 4/5"
description: "تحقيق معمق في دعم Soft AP (hostapd/WiFi Hotspot) لمحولات USB WiFi من ALFA Network على Kali Linux و Ubuntu و Debian و Raspberry Pi 4/5. أدلة إعداد كاملة لـ AWUS036ACM و AWUS036ACH و AWUS036AXML."
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "هل يمكن استخدام محول ALFA USB كنقطة اتصال WiFi على Linux؟"
    answer: "يعتمد على مجموعة الشرائح. AWUS036ACM (MT7612U) يدعم Soft AP بالكامل ويعمل فور التوصيل، AWUS036ACH (RTL8812AU) يدعمه بشكل مشروط، و AWUS036AXML يدعمه جزئياً ويتطلب ضبطاً."
  - question: "ما أفضل محول ALFA لإنشاء Soft AP على Raspberry Pi؟"
    answer: "AWUS036ACM هو الخيار الأفضل. تعريفه المدمج في النواة يعمل فور التوصيل، واستهلاكه للطاقة 400mA فقط مناسب لـ Pi، ويدعم WPA3 والواجهات الافتراضية VIF، وهو مستقر عبر جميع المنصات."
  - question: "كيف أتحقق من دعم المحول لوضع AP؟"
    answer: "نفّذ iw list | grep -A 10 'Supported interface modes'، إذا تضمن المخرج * AP فالتعريف يدعم Soft AP وستعمل hostapd بشكل صحيح."
  - question: "ما قيود Soft AP على تعريف RTL8812AU؟"
    answer: "لا يدعم WPA3 ويمكن استخدام WPA2-PSK فقط، لا يدعم الواجهات الافتراضية VIF فتحتاج بطاقتين للتقسيم، ويستهلك حوالي 800mA مما يتطلب موزع USB مزوداً بمصدر طاقة على Pi."
  - question: "ماذا أفعل إذا انقطع WiFi أثناء تشغيل AWUS036AXML كـ Soft AP؟"
    answer: "MT7921AUN المدمج به Bluetooth 5.2 يتداخل مع WiFi. نفّذ echo 'install btusb /bin/false' في /etc/modprobe.d/ لتعطيل تعريف Bluetooth نهائياً ثم أعد التشغيل."
---
> "هل يمكنني استخدام محولات ALFA USB WiFi كنقطة اتصال WiFi ‏(Soft AP) على Kali Linux / Ubuntu / Raspberry Pi؟"

## مقدمة

هذا من أكثر الأسئلة شيوعاً التي تصلنا في Yopitek. يبدو السؤال بسيطاً، لكن الإجابة تختلف اختلافاً كبيراً بحسب الطراز والشريحة — **ليس كل محول USB WiFi يمكنه العمل في وضع Soft AP.**

يجمع هذا المقال أكثر من 500 نقاش مجتمعي من GitHub ‏(morrownr/USB-WiFi) ومنتديات Reddit التقنية ووثائق Raspberry Pi الرسمية وتجارب المستخدمين الفعلية، ليقدم لك تقريراً صادقاً وشاملاً عن محولات ALFA التي تعمل وتلك التي لا تعمل، مع خطوات الإعداد الكاملة خطوة بخطوة.

{{< tldr >}}
يعتمد توافق محولات ALFA مع Soft AP على تعريف الشريحة. AWUS036ACM هو الخيار الأمثل المستقر عبر جميع المنصات، AWUS036ACH قابل للاستخدام لكن بدون WPA3، و AWUS036AXML يحتاج تعطيل Bluetooth وتحديث البرنامج الثابت. يعمل RTL8832BU (AX / AXER) ببرنامج التشغيل المدمج على النواة 6.17 فما فوق.
{{< /tldr >}}


محوّل ALFA AWUS036ACM (MT7612U) هو الخيار الأمثل لـ Soft AP على Linux: تعريف مدمج في النواة يعمل فور التوصيل، يدعم WPA3 والواجهات الافتراضية VIF. أما RTL8812AU فدعمه مشروط، و MT7921AUN يتطلب ضبطاً يدوياً.

---

## ١. ما هو Soft AP؟ كيف يعمل على Linux {#what-is-softap}

**Soft AP (Software Access Point)** هو القدرة على تحويل محول USB WiFi عادي إلى محطة قاعدة لاسلكية (Access Point) عبر البرمجيات — وبشكل أساسي **hostapd**. يتيح ذلك للأجهزة الأخرى (الهواتف، الحواسيب المحمولة، أجهزة IoT) الاتصال بالشبكة دون شراء موجّه أو جهاز AP مخصص.

هذه القدرة بالغة القيمة في عدة سيناريوهات:

- **موجّه السفر / المنزل**: أثناء السفر أو التخييم، وصّل محول ALFA بحاسوبك المحمول أو Raspberry Pi وأنشئ فوراً نقطة اتصال WiFi محمولة
- **مختبر اختبار الاختراق**: أنشئ Rogue AP معزولة لأغراض البحث الأمني
- **مُرحِّل IoT**: أنشئ مكرراً في المناطق الميتة للإشارة لتتمكن مستشعرات IoT من إرسال بياناتها
- **نشر الذكاء الاصطناعي على الحافة (Edge AI)**: في البيئات الصناعية التي تفتقر إلى شبكة سلكية — حوّل الجهاز إلى نقطة اتصال تتصل بها المعدات الأخرى
- **اتصالات الطوارئ**: أقم شبكة مؤقتة بسرعة عند انقطاع الاتصال

### المكونات الأساسية الأربعة لـ Soft AP في Linux

| المكوّن | الوظيفة |
|-----------|----------|
| **hostapd** | الخدمة (daemon) الأساسية التي تنشئ نقطة الوصول — تدير SSID والمصادقة والتشفير |
| **nl80211** | الواجهة القياسية للنظام الفرعي اللاسلكي في Linux — يجب أن يدعم برنامج التشغيل هذا الإطار ليعمل مع hostapd |
| **dnsmasq** | خادم DHCP يوزّع عناوين IP تلقائياً على العملاء المتصلين |
| **iptables / nftables** | ترجمة عناوين الشبكة (NAT) — تتيح للعملاء المتصلين مشاركة الشبكة الصاعدة |

### المفهوم الأساسي: وضع Master

**وضع Master** (ويُسمى أيضاً وضع AP أو وضع Infrastructure) هو قدرة على مستوى برنامج التشغيل. إذا لم يدعم برنامج التشغيل وضع Master، فلن يتمكن hostapd من البدء إطلاقاً — مهما كانت إعداداتك مثالية.

تحقق من دعم وضع AP باستخدام:

```bash
iw list | grep -A 10 "Supported interface modes"
```

إذا تضمّن المخرج `* AP`، فإن برنامج تشغيل المحول يدعم Soft AP. وإن لم يتضمنه، فلا يصلح هذا المحول لهذا الغرض.

### 💡 برامج التشغيل In-kernel مقابل Out-of-kernel

هذا هو المفهوم **الأهم على الإطلاق** عند اختيار محول لـ Soft AP:

| النوع | الوصف | التأثير على Soft AP |
|------|-------------|-------------------|
| **برنامج تشغيل In-kernel** | مدمج في شجرة مصدر Linux الرسمية؛ يُحمَّل تلقائياً عند الإقلاع — لا حاجة لتثبيت يدوي | ✅ مستقر على المدى الطويل؛ يصمد بعد ترقيات النواة |
| **برنامج تشغيل Out-of-kernel** | يجب تنزيله من GitHub وتجميعه يدوياً؛ وقد يحتاج إلى إعادة تجميع بعد كل تحديث للنواة | ⚠️ قد يتعطل بعد أي ترقية للنواة |

**لاستقرار Soft AP على المدى الطويل، تتفوق برامج التشغيل in-kernel بفارق كبير على برامج التشغيل out-of-kernel.**

---

## ٢. خط منتجات ALFA ونظرة عامة على الشرائح {#product-lineup}

فيما يلي خط منتجات ALFA الحالي الذي تبيعه Yopitek، مع الشرائح والتقييم المبدئي لوضع Soft AP:

| الطراز | الشريحة | نوع برنامج التشغيل | معيار WiFi | تقييم Soft AP |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel (نواة 4.19+) | WiFi 5 AC1200 ثنائي النطاق | ✅ دعم كامل |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel (in-kernel من 6.13+) | WiFi 5 AC1200 ثنائي النطاق | ⚠️ مشروط |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel (5.18+, وضع AP 5.19+) | WiFi 6E AX3000 ثلاثي النطاق | ⚠️ جزئي |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel (كما سبق) | WiFi 6E AX3000 ثلاثي النطاق | ⚠️ جزئي |
| AWUS036AX | Realtek RTL8832BU | مدمج rtw89_8852bu (نواة 6.17+)؛ النوى الأقدم: برنامج DKMS المجتمعي | WiFi 6 AX1800 ثنائي النطاق | ✅ يعمل (نواة 6.17+) |
| AWUS036AXER | Realtek RTL8832BU | مدمج rtw89_8852bu (نواة 6.17+؛ كما في AX) | WiFi 6 AX1800 ثنائي النطاق | ✅ يعمل (نواة 6.17+) |

> **ملاحظة**: توقف إنتاج AWUS036ACHM (MT7610U) ولم يعد مدرجاً في صفحة منتجات Yopitek. يغطي هذا المقال المنتجات المتوفرة حالياً فقط.

---

## ٣. AWUS036ACM (MT7612U) — ⭐ أفضل توصية {#acm}

### حالة Soft AP: ✅ دعم كامل

تُعد MT7612U أكثر شرائح Soft AP استقراراً في خط منتجات ALFA الحالي. برنامج تشغيلها `mt76x2u` جزء من نواة Linux الرسمية منذ 2018 (النواة 4.19)، أي أنها تعمل مباشرة على أي نظام حديث نسبياً — **لا `git clone`، ولا `dkms`، ولا إعادة تجميع بعد ترقيات النواة.**

### المزايا الرئيسية

- **دعم مزدوج WPA2 + WPA3**: يدعم برنامج تشغيل MediaTek المدمج في النواة WPA3 SAE أصلياً — ميزة لا تضاهيها برامج تشغيل Realtek
- **دعم الواجهات الافتراضية VIF**: شغّل أوضاع AP + Managed + Monitor في آن واحد على محول واحد — دون الحاجة لشراء بطاقة ثانية. شارك شبكتك وراقب الطيف اللاسلكي في الوقت نفسه
- **استهلاك طاقة منخفض للغاية**: حد أقصى ~400mA، مثالي لـ Raspberry Pi (يوفر النظام الفرعي USB في Pi 4 ما مجموعه 1200mA فقط)
- **متعدد المنصات**: تم التحقق منه على نطاق واسع على Kali Linux 2022.x–2025.x و Ubuntu 22.04/24.04 و Debian 11/12 و Raspberry Pi OS ‏(Pi 3B+ و 4 و 5)

### إعدادات hostapd الصحيحة (MT7612U)

تم التحقق من رايات القدرات التالية عبر سنوات من اختبارات المجتمع (morrownr/USB-WiFi). **يجب أن تطابق تماماً قدرات العتاد الفعلية لـ MT7612U:**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; use g for 2.4GHz
channel=36                    # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U correct HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # Center frequency index for channel 36

# Security: WPA2 + WPA3 mixed mode
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 dual support
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ الخطأ الأكثر شيوعاً

إذا تضمّن `ht_capab` رايات قدرات لا تدعمها MT7612U فعلياً (خاصة عند فرض بعض إعدادات HT40 عبر USB 2.0)، فسيتعطل hostapd بصمت مع رسائل خطأ غير مفيدة إطلاقاً. **استخدم فقط تركيبة الرايات المُتحقق منها أعلاه — ولا تنسخ إعدادات شرائح أخرى مثل RTL8812AU.** (المصدر: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### آراء المجتمع

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> *(ترجمة: «يعمل Alfa AWUS036ACM جيداً جداً مع عتاد Raspberry Pi. لقد اختبرت Alfa AWUS036ACM مع العديد من أنظمة الحاسوب وتوزيعات Linux المختلفة. في رأيي، إنه محول USB WiFi متميز.»)*
> — **morrownr**، مشرف أكثر قواعد المعرفة المجتمعية موثوقية حول Linux USB WiFi على GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> *(ترجمة: «يستطيع هذا المحول تنفيذ وضع Monitor وحقن الحزم بشكل مثالي. مستقر جداً على Linux باستخدام النوى الأصلية، دون الحاجة لتجميع برامج تشغيل خارجية.»)*
> — مراجعة مستخدم على eBay

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> *(ترجمة: «ACM أكثر تنوعاً قليلاً وأسهل في الإعداد لوضع AP.»)*
> — سلسلة نقاش GitHub issue #2

---

## ٤. AWUS036ACH (RTL8812AU) — يعمل ولكن مع تنازلات {#ach}

### حالة Soft AP: ⚠️ دعم مشروط

تُعد RTL8812AU أشهر شريحة لاختبار الاختراق لدى ALFA والمفضلة منذ زمن طويل لدى مجتمع Kali Linux. وظيفة Soft AP فيها تعمل فعلاً — فإنشاء نقطة اتصال أساسية لا مشكلة فيه — لكن بنية برنامج تشغيل Realtek الخارج عن النواة (out-of-kernel) تفرض عدة قيود مستمرة:

### القيود المعروفة

1. **لا دعم لـ WPA3**: رغم أن برنامج تشغيل RTL8812AU يدّعي دعم WPA3، أكد عدة مستخدمين أنه لا يعمل فعلياً. **WPA2-PSK فقط.**
2. **لا دعم لـ VIF**: لا يمكن تشغيل وضعي AP + Monitor على البطاقة نفسها في آن واحد. إذا احتجت إلى AP مع المراقبة، فعليك استخدام محولين منفصلين.
3. **مشكلات برنامج التشغيل على Kali Linux 2025.x**: يعاني أحدث برنامج تشغيل aircrack-ng/rtl8812au على أحدث إصدار من Kali من مشكلات توافق — وعليك الرجوع إلى commit قديم محدد (`63cf0b4`). قد يتحسن الوضع مع برنامج التشغيل rtw88 المدمج في النواة 6.13+.
4. **استهلاك طاقة مرتفع**: حد أقصى ~800mA — على Raspberry Pi مع توصيل عدة أجهزة USB، قد يسبب ذلك عدم استقرار النظام. استخدم موزع USB مزوداً بمصدر طاقة.

### إعدادات hostapd ‏(RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# NOTE: Completely different capabilities from MT7612U!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# Security: WPA2 only, do NOT add WPA3
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### تثبيت برنامج التشغيل (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x requires the older commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### آراء المجتمع

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> *(ترجمة: «يمكنني وضع RTL8812AU ‏(AWUS036AC) بدلاً منه واستخدام 'sudo service hostapd restart && sudo service dnsmasq restart'، وقد عمل بشكل جيد تماماً.»)*
> — مستخدم في GitHub issue #2

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> *(ترجمة: «المحولات المبنية على RTL8812AU — وضع AP يعمل، لكنك تفقد دعم WPA3 و VIF مقارنة بـ MediaTek.»)*
> — ملاحظات morrownr التقنية

### الحكم على ACH

إذا كنت تمتلك AWUS036ACH بالفعل، فيمكنه العمل كـ Soft AP (وظيفة نقطة الاتصال الأساسية تعمل). لكن إن لم تشترِ بعد وكان هدفك الأساسي هو Soft AP، **فاختر ACM بدلاً منه.**

---

## ٥. AWUS036AXML / AWUS036AXM (MT7921AUN) — تابع بحذر {#axml}

### حالة Soft AP: ⚠️ دعم جزئي — مشكلات معروفة في البرنامج الثابت/برنامج التشغيل

يُعد AWUS036AXML و AWUS036AXM الطرازين الرائدين ثلاثيي النطاق من ALFA بمعيار WiFi 6E، ويغطيان وفق المواصفات 2.4 GHz و 5 GHz ونطاق 6 GHz الجديد (تم التحقق من 6 GHz محلياً على AXML؛ ولم يُختبر 6 GHz على AXM). برنامج التشغيل المدمج `mt7921u` موجود في النواة منذ الإصدار 5.18، وأُضيف دعم وضع AP رسمياً في 5.19. لكن شريحة MT7921AUN تدمج أيضاً Bluetooth 5.2 — وهو ما أصبح المشكلة الأولى لدى المجتمع في 2024–2025.

### محطات إصدارات النواة لوضع AP

| الوضع | الحد الأدنى للنواة |
|------|---------------|
| Managed (WiFi العادي) | 5.18+ |
| **وضع AP ‏(Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO ‏(Wi-Fi Direct AP) | 6.4+ |

### المشكلات المعروفة والحلول

#### المشكلة ١: تداخل Bluetooth يسبب أعطال WiFi

على النوى 6.6+، تتسبب تغييرات في النظام الفرعي BT في أعطال WiFi متقطعة مع mt7921u. وتختلف قابلية تكرار المشكلة بحسب بيئة النظام. **الحل البديل الأكثر فعالية هو تعطيل برنامج التشغيل btusb:**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### المشكلة ٢: برنامج ثابت قديم

إذا كان البرنامج الثابت لـ MediaTek في النظام قديماً جداً، فقد لا يُتعرَّف على المحول بشكل صحيح. ثبّت برنامجاً ثابتاً بتاريخ نوفمبر 2024 أو أحدث:

```bash
# Check current firmware version
dmesg | grep "WM Firmware"
# Should show: Build Time: 20241106151045 or newer

# If outdated, download from kernel.org
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### المشكلة ٣: متطلبات إصدار hostapd

يفيد بعض المستخدمين بحاجتهم إلى تجميع hostapd من git للحصول على دعم كامل لوضع AP في WiFi 6. قد تكون الإصدارات المتوفرة في مدير حزم النظام غير مكتملة.

#### المشكلة ٤: خلل في عرض قدرة الإرسال (Tx Power) في وضع AP

يعرض `iw` قيمة 3 dBm فقط دون إمكانية التعديل، لكن الشريحة تحتوي فعلياً على مضخم داخلي — هذه مشكلة عرض في برنامج تشغيل النواة، وليست قيداً في العتاد.

#### المشكلة ٥: مشكلات وضع Monitor في بعض إصدارات النواة

حتى ديسمبر 2025، تعاني النواة 6.18 وبعض الإصدارات الأقدم من برنامج التشغيل mt7921u من مشكلات في وضع Monitor.

### رأي المجتمع

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> *(ترجمة: «لديّ Alfa AXML يعمل كـ AP على مضيف RPi3B بنظام ArchLinux ARM aarch64. إنه أكثر mt7921 استقراراً في مجموعتي. لكنني أشغّل hostapd مُجمَّعاً من git.»)*
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### الحكم على AXML/AXM

اختر هذين الطرازين إذا كنت بحاجة إلى نطاق 6 GHz في WiFi 6E ومستعداً لتعديل الإعدادات أحياناً. **أما لبيئات الإنتاج التي تتطلب استقراراً مطلقاً لـ Soft AP، فاختر ACM بدلاً منهما.**

---

## ٦. AWUS036AX / AWUS036AXER (RTL8832BU) — يعمل مع Soft AP على النواة 6.17 فما فوق {#ax}

### حالة Soft AP: ✅ يعمل على النواة 6.17 فما فوق (النوى الأقدم تحتاج برنامج DKMS المجتمعي)

في اختباراتنا على ASUS GX10 (Ubuntu 24.04 ARM64، النواة 6.17) مع برنامج التشغيل المدمج `rtw89_8852bu`، يتصرف AWUS036AX وAWUS036AXER (الشريحة نفسها وبرنامج التشغيل نفسه) بالطريقة نفسها، ويعمل Soft AP على نطاقي 2.4 و5 GHz.

**نتائج الاختبار (النواة 6.17):**

1. **وضع AP**: يعمل على 2.4 GHz (802.11n) و5 GHz (VHT 80 MHz)
2. **VIF (STA + AP)**: يعمل — اتصال عميل وواجهة AP بالتوازي على القناة نفسها
3. **WPA3-SAE AP**: يعمل على 2.4 GHz (اتصل iPhone 15 Pro، وMFP مفعّل؛ لم يُختبر 5 GHz)
4. **Monitor / الحقن**: استقبال monitor قوي على 2.4 و5 GHz؛ حقن 2.4 GHz بنسبة AX 96% / AXER 73%، و5 GHz قابل للاستخدام؛ ونجح التقاط WPA handshake من البداية إلى النهاية
5. **غير مدعوم**: IBSS وMesh وactive monitor

**تنبيهات:**

- **إصدار النواة شرط أساسي**: `rtw89_8852bu` مدمج في النواة ابتداءً من 6.17. أما النوى الأقدم فتحتاج برنامج DKMS المجتمعي (rtl8852bu)، وقد يكون وضع monitor محدوداً معه ولا يدعم VIF.
- **وضع USB**: قد تُعرَّف بعض الوحدات في وضع CD-ROM (`0bda:1a2b`) وتحتاج `usb_modeswitch -v 0bda -p 1a2b -K`؛ أما وحدة الاختبار لدينا فقد عُرّفت مباشرة كمحول WLAN.
- **الحالات المجتمعية**: تقارير Soft AP لهذه الشريحة ما زالت أقل من MT7612U وRTL8812AU.

> نتيجة اختبار Yopitek (ASUS GX10، النواة 6.17): مع برنامج التشغيل المدمج يتمتع AWUS036AX / AWUS036AXER باستقبال monitor قوي وحقن حزم يعمل، فيصلحان أيضاً لاختبار الاختراق. ينطبق دعم monitor المحدود فقط على النوى الأقدم التي تستخدم برنامج DKMS المجتمعي.
>
> تحديث: على نواة stock 6.16 وما بعدها (تم الاختبار على 6.17) يعمل AWUS036AXML في أوضاع monitor وAP وWPA3 وVIF، لكن اختبار حقن الحزم فشل (aireplay-ng --test: Found 0 APs / No Answer). السبب هو تراجع في mac80211 chanctx وليس الشريحة نفسها. إذا احتجت إلى الحقن فاستخدم AWUS036ACH أو EACS أو ACS أو AX.

---

## ٧. مصفوفة توافق المنصات {#compat-matrix}

### AWUS036ACM (MT7612U)

| المنصة | Soft AP | ملاحظات |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel، يعمل فور التوصيل، النواة 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel، بلا إعداد، استخدم إصدار LTS |
| Debian 11 / 12 | ✅ | In-kernel، مستقر |
| Raspberry Pi 4 (RPi OS) | ✅ | أقل استهلاك للطاقة (400mA)، تحقق طويل الأمد من morrownr. يُفضَّل منفذ USB 3.0 في Pi 4 |
| Raspberry Pi 5 (RPi OS) | ✅ | برنامج التشغيل نفسه كما في Pi 4، مستقر |

### AWUS036ACH (RTL8812AU)

| المنصة | Soft AP | ملاحظات |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | يحتاج برنامج تشغيل خارجياً؛ يتطلب 2025.x الـ commit ‏`63cf0b4`. قد يتحسن الوضع مع rtw88 في النواة 6.13+ |
| Ubuntu 22.04 / 24.04 | ⚠️ | قد يلزم تثبيت برنامج التشغيل rtw88 أو aircrack-ng يدوياً |
| Debian 11 / 12 | ⚠️ | كما سبق |
| Raspberry Pi 4 | ⚠️ | يعمل لكن استهلاك الطاقة مرتفع (800mA)؛ استخدم موزع USB مزوداً بمصدر طاقة |
| Raspberry Pi 5 | ⚠️ | كما سبق؛ قد تؤثر اختلافات وحدة تحكم USB في Pi 5 على السلوك |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| المنصة | Soft AP | ملاحظات |
|----------|---------|-------|
| Kali Linux 2022.x (kernel 5.18+) | ✅ | عطّل btusb، وحدّث البرنامج الثابت |
| Kali Linux 2024.x / 2025.x | ⚠️ | تعارض BT/WiFi في النواة 6.11+، غير مستقر |
| Ubuntu 24.04 (kernel 6.8+) | ⚠️ | أُبلغ عن مشكلات في أواخر 2024 |
| Ubuntu 25.04 / CachyOS (kernel 6.14+) | ✅ | يعمل فور التوصيل، تحسن ملحوظ مع النواة الجديدة |
| Debian 12 | ⚠️ | يعتمد على إصدار النواة |
| Raspberry Pi 4 / 5 | ⚠️ | توجد حالات نجاح، لكن تحقق من البرنامج الثابت وعطّل BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| المنصة | Soft AP | ملاحظات |
|----------|---------|-------|
| Kali Linux | ✅ | rtw89_8852bu مدمج ابتداءً من النواة 6.17؛ النوى الأقدم تحتاج برنامج DKMS المجتمعي |
| Ubuntu / Debian | ✅ | يتطلب Ubuntu 24.04 نواة HWE 6.17+ (نواتا GA 6.8 وHWE 6.14 تحتاجان برنامج DKMS المجتمعي)؛ ويتطلب Debian نواة 6.17+ |
| Raspberry Pi 4 / 5 | ⚠️ | لم يُختبر على Pi؛ النوى الأقدم من 6.17 تحتاج برنامج DKMS المجتمعي |

---

## ٨. دليل إعداد Soft AP الكامل (AWUS036ACM) {#setup-guide}

فيما يلي دليل كامل خطوة بخطوة لإعداد Soft AP على نطاق 5GHz باستخدام AWUS036ACM على Raspberry Pi 4.

### الخطوة ١: التحقق من اكتشاف المحول وبرنامج التشغيل

```bash
# Confirm the adapter is detected
lsusb | grep MediaTek
# Expected: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Check driver loaded
dmesg | grep mt76
# Expected: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# Confirm AP mode support
iw list | grep -A 10 "Supported interface modes"
# Check that output includes "* AP"
```

### الخطوة ٢: تثبيت الحزم المطلوبة

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### الخطوة ٣: إعداد hostapd

أنشئ الملف `/etc/hostapd/hostapd.conf`:

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT settings (MT7612U specific)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 mixed mode
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### الخطوة ٤: إعداد dnsmasq ‏(DHCP)

أنشئ الملف `/etc/dnsmasq.conf`:

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### الخطوة ٥: تعيين IP ثابت و NAT

```bash
# Assign static IP to wlan0
sudo ip addr add 192.168.10.1/24 dev wlan0

# Enable IP forwarding
sudo sysctl net.ipv4.ip_forward=1

# Configure NAT (assuming eth0 is the upstream interface)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Persist iptables rules
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### الخطوة ٦: تشغيل الخدمات

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Check service status
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# Enable auto-start on boot
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

بعد الانتهاء، ابحث عن شبكات WiFi على هاتفك أو حاسوبك المحمول — يُفترض أن ترى SSID ‏`Yupitek_AP`.

---

## ٩. استكشاف الأخطاء الشائعة {#troubleshooting}

### س١: hostapd يتعطل فور بدء التشغيل

**العَرَض**: يعرض `sudo systemctl status hostapd` الحالة `exited` أو `failed`

**السبب المرجّح**: يحتوي `hostapd.conf` على رايات قدرات لا تدعمها الشريحة

**الحل**: احذف الرايات الزائدة. بالنسبة لـ MT7612U ‏(ACM)، فإن الطريقة الأكثر أماناً هي استخدام الإعدادات المُتحقق منها في القسم ٣. **لا تنسخ ht_capab من شرائح أخرى.**

---

### س٢: العملاء يتصلون لكن لا يصلون إلى الإنترنت

**العَرَض**: WiFi متصل وتم الحصول على IP، لكن `ping 8.8.8.8` لا يتلقى رداً

**قائمة التحقق**:

```bash
# 1. Check IP forwarding enabled
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1

# 2. Check NAT rules exist
sudo iptables -t nat -L POSTROUTING -v
# Should see MASQUERADE rule

# 3. Confirm upstream interface is working
ping -I eth0 8.8.8.8
```

---

### س٣: نقطة AP على 5GHz غير ظاهرة أو غير مستقرة

**الأسباب المحتملة**:

1. **استخدام قنوات DFS ‏(100–144)**: لا تدعم MT7612U / MT7610U تقنية DFS — استخدم قنوات UNII-1 ‏(36–48)
2. **قدرة إرسال غير كافية**: تأكد من إحكام ربط الهوائيات على موصلات RP-SMA
3. **طاقة USB غير كافية** (Raspberry Pi): استخدم مزود الطاقة الرسمي 5A أو موزع USB مزوداً بمصدر طاقة

---

### س٤: hostapd يعيد التشغيل باستمرار على Raspberry Pi

**العَرَض**: يعرض `dmesg` رسائل إعادة تعيين USB متكررة

**السبب المرجّح**: طاقة منفذ USB غير كافية (خاصة مع شريحة AWUS036ACH عالية الاستهلاك، بحد أقصى 800mA)

**الحل**:
- استخدم مزود الطاقة الرسمي 5A لـ Pi
- استخدم موزع USB مزوداً بمصدر طاقة
- وصّل المحول بمنفذ USB 3.0 ‏(Pi 4 فقط)

---

### س٥: WiFi على AWUS036AXML/AXM ينقطع فجأة أو لا يبدأ

**السبب المرجّح**: تداخل النظام الفرعي Bluetooth مع WiFi ‏(تحتوي MT7921AUN على BT 5.2 مدمج)

**الحل**: عطّل برنامج تشغيل Bluetooth نهائياً

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## ١٠. تحليل تقني متعمق: VIF و WPA3 وقنوات DFS {#technical}

### VIF ‏(الواجهة الافتراضية): بطاقة واحدة، أدوار متعددة

تتيح VIF ‏(Virtual Interface) لمحول فعلي واحد العمل بعدة واجهات منطقية في آن واحد. على سبيل المثال: واجهة تتصل بالموجّه الصاعد (وضع managed) بينما تعمل أخرى كـ AP ‏(وضع master) للأجهزة الأخرى.

ثلاثة سيناريوهات شائعة:

| السيناريو | هل تحتاج VIF؟ | المحول الأفضل |
|----------|--------------|--------------|
| توجيه NAT أساسي (eth0 صاعد + wlan AP) | ❌ لا | أي محول يدعم AP |
| جسر لاسلكي (استقبال WiFi + WiFi AP في آن واحد) | ✅ نعم | ACM (MT7612U) |
| Monitor + AP في آن واحد (بحث أمني / Rogue AP) | ✅ نعم | ACM (MT7612U) |

**مثال عملي على VIF ‏(MT7612U):**

```bash
# Create an additional AP virtual interface alongside existing wlan1
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Now wlan1 can connect upstream while ap0 runs hostapd
```

برامج تشغيل MediaTek المدمجة في النواة (mt76x2u و mt7921u) فقط هي التي تدعم VIF بالكامل. أما برامج تشغيل Realtek الخارجة عن النواة فتفتقر أساساً لهذه القدرة — إذا احتجت إلى AP + Monitor في آن واحد، فعليك استخدام محولين منفصلين.

---

### مقارنة دعم WPA3

| الشريحة | الطراز المقابل | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ دعم SAE أصلي |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ دعم SAE أصلي |
| RTL8812AU | AWUS036ACH | ✅ | ❌ يدّعي الدعم لكنه لا يعمل |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ تم اختباره على النواة 6.17 (`sae_pwe=0`، وMFP مفعّل) |

---

### اختيار قناة Soft AP على 5GHz: تجنّب DFS

تتطلب قنوات DFS ‏(Dynamic Frequency Selection) ‏(ch100–ch140) كشف الرادار على مستوى النواة. لا تدعم MT7612U والشرائح المماثلة تقنية DFS. لوضع AP على 5GHz، اختر:

| النطاق | القنوات الموصى بها | السبب |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | مدعومة من جميع الشرائح؛ الخيار الأكثر أماناً |
| UNII-2 (DFS) | 52–144 | غير مدعومة في الغالب؛ غير موصى بها |
| UNII-3 | 149–165 | دعم جزئي (حسب المنطقة) |

---

## ١١. حالات واقعية من المجتمع {#real-cases}

### الحالة ١: RPi4B + AWUS036ACM = نقطة AP منزلية على 5GHz مستقرة على المدى الطويل

**المصدر**: قاعدة معرفة morrownr/7612u على GitHub
**السيناريو**: يستخدم morrownr منذ فترة طويلة RPi4B + AWUS036ACM كنقطة AP منزلية على 5GHz، مع شبكة 2.4GHz المدمجة في Pi لتقديم خدمة ثنائية النطاق
**النتيجة**: تشغيل مستقر على المدى الطويل دون الحاجة لإعادة التشغيل، بتقييم "متميز"
**الإعدادات**: hostapd + dnsmasq + iptables NAT

### الحالة ٢: RPi3B+ + ACM — تعطل أولي، تم إصلاحه

**المصدر**: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**المشكلة**: تعطل hostapd عند تشغيله عبر USB 2.0 على RPi3B+
**السبب الجذري**: احتوى `ht_capab` على رايات HT40 غير مدعومة ضمن حدود عرض نطاق USB 2.0
**الحل**: حُذفت الرايات الزائدة؛ وتم التشغيل بنجاح على Kali Linux

### الحالة ٣: Pi PwnBox + AWUS036ACH = Rogue AP للفريق الأحمر

**المصدر**: GitHub koutto/pi-pwnbox-rogueap
**السيناريو**: منصة Rogue AP على RPi3B+: محول RTL8812AU ‏(AWUS036ACH) للـ AP، وآخر RT3070 ‏(AWUS036NEH) لهجمات حقن الحزم
**النتيجة الرئيسية**: لأن RTL8812AU يفتقر إلى VIF، لزم استخدام محولين منفصلين (بخلاف ACM الذي يتولى المهمتين على بطاقة واحدة)

### الحالة ٤: AP مستقرة على AWUS036AXML على RPi3B بنظام ArchLinux ARM

**المصدر**: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**السيناريو**: شغّل مستخدم AWUS036AXML بنجاح في وضع AP على RPi3B بنظام ArchLinux aarch64
**اقتباس**: «إنه أكثر mt7921 استقراراً في مجموعتي.»
**المتطلبات الرئيسية**: hostapd مُجمَّع من git + تعطيل btusb

### الحالة ٥: AP بالسرعة الكاملة على AWUS036ACHM ‏(MT7610U، متوقف الإنتاج) على Pi4

**المصدر**: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**المشكلة**: حققت الإعدادات الأولية سرعة ربط 65 Mbps فقط، أقل بكثير من السرعة الكاملة لـ AC على 5GHz
**الحل**: أُضيف `vht_oper_chwidth=1` و `vht_oper_centr_freq_seg0_idx` الصحيحان؛ وتحقق معدل ربط 433 Mbps
**الصلة بـ ACM**: إعداد معاملات VHT نفسه بالغ الأهمية لـ MT7612U ‏(ACM) أيضاً

---

## ١٢. توصيات الشراء والحكم النهائي {#recommendations}

### مصفوفة القرار السريع

| التقييم | الطراز | الأنسب لـ | باختصار |
|--------|-------|----------|-----------|
| 🥇 **الخيار الأفضل** | **AWUS036ACM** | الجميع، خاصة من يبني Soft AP لأول مرة | مستقر على جميع المنصات، بلا متاعب |
| 🥈 قابل للاستخدام | AWUS036ACH | المستخدمون الذين يمتلكون هذا الطراز بالفعل | يحتاج برنامج تشغيل، لا WPA3 |
| 🥉 متقدم | AWUS036AXML | من يحتاج WiFi 6E ومستعد للتجريب | ميزة 6GHz، يحتاج إصلاحات يدوية |
| ✅ يعمل على النواة 6.17+ | AWUS036AX / AXER | AP بتقنية Wi-Fi 6؛ ويعمل monitor والحقن أيضاً | برنامج تشغيل مدمج؛ تم اختبار AP على 2.4 / 5 GHz وVIF، واختُبر WPA3 على 2.4 GHz |

### 🎯 دليل القرار

- **تحتاج Soft AP مستقرة على Kali / Ubuntu / Debian / Raspberry Pi 4 أو 5؟**
  → اختر **AWUS036ACM** بلا منازع.

- **تمتلك AWUS036ACH بالفعل وتريد تجربة Soft AP؟**
  → يعمل، لكن مع WPA2 فقط، وستحتاج إلى تثبيت برنامج التشغيل. إذا قبلت هذه القيود، فلا مانع.

- **تحتاج WiFi 6E ‏(نطاق 6 GHz) ومستعد لضبط الإعدادات؟**
  → AWUS036AXML — تذكّر تعطيل برنامج تشغيل BT والتحقق من أن النواة ≥ 6.6 LTS.

- **الغرض الأساسي هو Soft AP وليس اختبار الاختراق؟**
  → AWUS036ACM هو الخيار الوحيد الذي يحظى بتحقق مجتمعي واسع على جميع المنصات.

---

{{< faq >}}

### الخلاصة

العامل الجوهري في بناء Soft AP ليس سرعة WiFi ولا عدد الهوائيات — **إنه دعم وضع AP لبرنامج تشغيل الشريحة.**

من بين جميع منتجات ALFA التي بحثناها، **AWUS036ACM (MT7612U)** هو المحول الوحيد الذي يلبي في آن واحد: برنامج تشغيل in-kernel، WPA3 أصلي، واجهات VIF افتراضية، استهلاك طاقة منخفض، واستقرار عبر المنصات. إنه المعيار الذهبي لـ Soft AP.

يعمل AWUS036ACH ‏(RTL8812AU) إذا قبلت قيوده. يتمتع AWUS036AXML/AXM ‏(MT7921AUN) بإمكانات كبيرة، لكن نضج برنامج التشغيل لا يزال قيد التطوير. أما AWUS036AX/AXER ‏(RTL8832BU) فيعمل جيداً على النواة 6.17 فما فوق ببرنامج التشغيل المدمج (تم اختبار AP وVIF وWPA3)؛ والنوى الأقدم تحتاج برنامج DKMS المجتمعي.

**إذا كانت هذه هي المرة الأولى لك في إعداد Soft AP على Raspberry Pi أو Kali Linux — اختر ACM. لن تندم.**

---

### روابط الشراء

- [AWUS036ACM — الخيار الأفضل لـ Soft AP](/ar/products/alfa/awus036acm/)
- [AWUS036ACH — محول اختبار الاختراق الكلاسيكي](/ar/products/alfa/awus036ach/)
- [AWUS036AXML — الطراز الرائد ثلاثي النطاق WiFi 6E](/ar/products/alfa/awus036axml/)
- [خط منتجات ALFA Network الكامل](/ar/products/alfa/)

### قراءات إضافية

- [AWUS036ACH مقابل AWUS036ACM: مقارنة شاملة لبرامج تشغيل الشرائح](/ar/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM: وضعا IBSS و Mesh على Raspberry Pi](/ar/blog/)
- [morrownr/USB-WiFi — قاعدة المعرفة المرجعية حول Linux USB WiFi](https://github.com/morrownr/USB-WiFi) (أكثر من 4,100 نجمة)
- [morrownr/7612u — مرجع MT7612U (يشمل دليل Bridged AP على RPi4B)](https://github.com/morrownr/7612u)
- [DeepWiki — قاعدة معرفة morrownr/USB-WiFi المُنظَّمة تلقائياً](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 مصادر البيانات

يجمع هذا المقال معلومات من:
- **morrownr/USB-WiFi** قاعدة معرفة على GitHub (أكثر من 4,100 نجمة) مع سجلات iw_list كاملة
- **morrownr/7612u** — دليل Bridged AP بـ MT7612U على RPi4B
- **متتبع مشكلات GitHub** — issue #2 (إعدادات AP لـ ACM)، و #476 (اختبار AP على AXML)، و Discussion #31 (AP بالسرعة الكاملة على ACHM)
- **koutto/pi-pwnbox-rogueap** — حالة تطبيق RogueAP بمحول Alfa
- صفحات دعم Linux لدى الموزع المعتمد **Rokland**
- مراجعات **Lab401** التقنية وتقارير أفضل الخيارات لاختبار الاختراق لعام 2025
- **منتدى Raspberry Pi الرسمي** — نقاشات توافق USB WiFi مع Pi 4/5
- **مدونة Yopitek الحالية** — دليل تثبيت ACM في الصين، مراجعة AXML WiFi 6E، أفضل محولات Kali Linux 2026

## المراجع

1. [مستودع GitHub لمعرفة morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi)
2. [وثائق hostapd الرسمية](https://w1.fi/cgit/hostap/)
3. [تعريف Linux Wireless mt76](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
4. [وثائق Raspberry Pi الرسمية](https://www.raspberrypi.com/documentation/)
5. [وثائق Kali Linux الرسمية](https://www.kali.org/docs/)

---

> **الوسوم**: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yopitek
>
> **المؤلف**: Yopitek Ltd — الموزع المعتمد لـ ALFA Network في تايوان
>
> **إخلاء مسؤولية**: بيانات البحث حديثة حتى مايو ٢٠٢٦. تستمر نوى Linux والتوزيعات في التطور، وقد يتغير دعم برامج التشغيل مع الإصدارات الجديدة. تحقق من إصدار النواة وتوافق برنامج التشغيل على المنصة المستهدفة قبل النشر.
>
> **الدعم الفني**: لمشكلات إعداد Soft AP، تواصل مع الدعم الفني لـ Yopitek تايوان. للاستفسار عن المنتجات: [yupitek.com](https://yupitek.com/ar/).
