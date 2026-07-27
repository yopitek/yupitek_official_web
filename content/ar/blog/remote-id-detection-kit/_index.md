---
title: "ALFA AWUS036ACH × Raspberry Pi: مجموعة كشف Remote ID كاملة للطائرات بدون طيار (2026)"
description: "باستخدام ALFA AWUS036ACH و Raspberry Pi، ابنِ مجموعة كشف Remote ID سلبية قانونية للطائرات بدون طيار. تشمل تحليل معيار ASTM F3411، قائمة المكونات، الإعداد خطوة بخطوة، وتوضيح تقني حول DJI OcuSync."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "كشف-طائرات-بدون-طيار", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "لماذا تعتبر AWUS036ACH الخيار المفضل بدلاً من بطاقات WiFi 6/6E الأحدث؟"
    answer: "التقاط Remote ID يتطلب وضع مراقبة (monitor mode) مستقراً وحقن حزم خام (raw packet injection). حالياً، أكثر برامج التشغيل (drivers) نضجاً في المجتمع هو فرع Realtek rtl88xxau (RTL8812AU / RTL8814AU). بطاقات WiFi 6/6E (MediaTek MT7921AUN، Realtek RTL8832BU) لا تملك بعد برامج تشغيل للحقن في أدوات المراقبة الرئيسية، لذلك يتم تجاهلها. AWUS036ACH هي خيار تم التحقق منه مزدوجاً من المجتمع وهذه المجموعة."
  - question: "هل nRF52840 ضروري؟"
    answer: "إذا كنت تحتاج فقط Remote ID عبر WiFi (NAN / Beacon)، لا؛ AWUS036ACH كافية. إذا كنت ترغب أيضاً في التقاط بثوث Bluetooth 5 Long Range، فستحتاج إلى nRF52840 (مع برنامج ثابت sniffer). يُوصى بتضمين هذه الوحدة لتغطية كاملة."
  - question: "هل يمكن لهذه المجموعة فك تشفير طائرات DJI؟"
    answer: "يمكنها معالجة بثوث WiFi/BT Remote ID القياسية من DJI. لكن DroneID الخاص بـ DJI OcuSync ليس ضمن البروتوكول القياسي؛ بطاقة ALFA لا يمكنها فك تشفيره. ستحتاج إلى SDR (ANTSDR / HackRF) مع إضافة Kismet. يمكن نشر كلا النظامين بالتوازي."
  - question: "أي جيل من Raspberry Pi يُوصى به؟"
    answer: "Raspberry Pi 4 (2 GB+) هو الأكثر توازناً. Pi 3B تم التحقق منه من قبل مؤلف unix_rid_capture في اختباراته. Pi 5 يعمل أيضاً (انتبه للتبريد والطاقة). WiFi المدمج في Pi لا يمكنه الدخول بشكل مستقر إلى وضع المراقبة، لذا من الضروري استخدام AWUS036ACH الخارجية."
  - question: "هل الاستقبال السلبي قانوني؟"
    answer: "استقبال بثوث Remote ID العامة من الطائرات بدون طيار هو قانوني، ويعادل قراءة معلومات عامة. لكن التداخل النشط (jamming) منظم بشدة ولا يندرج ضمن هذه المجموعة."
---
> الفريق التقني لشركة Yupitek | الموزع المعتمد لـ ALFA Network في تايوان

{{< tldr >}}
مجموعة كشف Remote ID تستخدم وضع المراقبة (monitor mode) لبطاقة **ALFA AWUS036ACH** لاستقبال معلومات الهوية والموضع التي يجب على الطائرات بدون طيار بثها قانونياً (ما يعادل «لوحة أرقام جوية») بشكل سلبي، مما يوفر لمديري الأمن أداة قانونية ومنخفضة التكلفة للوعي الظرفي.
{{< /tldr >}}

---

## 1. لماذا تحتاج مجموعة كشف Remote ID

تنظيم الطائرات بدون طيار عالمياً دخل عصر «التعريف عبر البث». وفقاً للمعايير، يجب على الطائرات بدون طيار بث معلوماتها باستمرار في الجو:

| الحقل المُبَث | الوصف |
|---|---|
| معرف UAS / المشغل | رقم تسلسلي أو رمز تسجيل |
| الموقع الفوري (خط العرض، خط الطول، الارتفاع) | WGS-84 / ارتفاع بارومتري |
| السرعة، الاتجاه | سرعة أفقية / رأسية |
| موقع المشغل | نقطة الإقلاع أو الموقع الفوري |

البث يتم عبر نوعين من الناقلات اللاسلكية:

- **Bluetooth**: BT4 Legacy Advertising، BT5 Long Range (Extended Advertising)
- **WiFi**: NAN (Wi-Fi Aware، 2.4 / 5 GHz)، Beacon (2.4 / 5 GHz)

لمديري المطارات والمناطق الصناعية والسجون والفعاليات الكبيرة، **استقبال هذه البثوث العامة بشكل سلبي** (ما يعادل رؤية «رقم ذيل» الطائرة) هو وسيلة قانونية ومنخفضة التكلفة للوعي الظرفي، دون حاجة لتداخل نشط.

{{< alert "triangle-exclamation" >}}
**ملاحظة قانونية**: جميع الطرق في هذا المقال هي **استقبال سلبي للبثوث العامة**. التداخل النشط (jamming) منظم بشدة ولا يندرج ضمن هذه المجموعة، ولا يُوصى باستخدامه.
{{< /alert >}}

---

## 2. تحديد موقع المنتج: المسار مفتوح المصدر الأقل خطراً تقنياً

بعد تقييم مسارات تقنية متعددة، اخترنا المجموعة القائمة على **ALFA AWUS036ACH**:

- ALFA AWUS036ACH تستخدم شريحة **Realtek RTL8812AU**، مزدوجة النطاق 2.4 + 5 GHz (802.11ac)، 2×2 MIMO، هوائيين قابلين للفصل بكسب 5 dBi (RP-SMA)، مع عرض نطاق USB 3.0 كافٍ.
- برنامج التشغيل (driver) `rtl88xxau` الذي يحافظ عليه المجتمع يسمح لها بالدخول بشكل مستقر إلى **وضع المراقبة (monitor mode)** ودعم **حقن الحزم الخام (raw packet injection)** — وهو الشرط المسبق لالتقاط إطارات Wi-Fi RID Beacon / NAN.
- الأهم: ملف README لـ `sxjack/unix_rid_capture` يذكر صراحةً **«تم الاختبار باستخدام دونغل WiFi يعتمد على rtl8812au، ودونغل nRF52840، وRaspberry Pi 3B»** ، مما يعني أن المجتمع قد تحقق بالفعل من العتاد. نسخ بنيته لصنع منتج يمثل أقل خطر تقني.

---

## 3. قائمة المكونات (Hardware List)

| المكون | الطراز / المواصفات | الوظيفة | الضرورة |
|---|---|---|---|
| **البطاقة الرئيسية** | ALFA **AWUS036ACH** (RTL8812AU، مزدوجة النطاق 2.4/5 GHz، USB 3.0، هوائي مزدوج 5 dBi RP-SMA) | التقاط WiFi Remote ID (وضع المراقبة) | **إلزامي** |
| كمبيوتر لوحي بسيط | Raspberry Pi 4 (2 GB+ موصى به؛ 3B / 5 صالح أيضاً) | الكمبيوتر الرئيسي | **إلزامي** |
| تخزين | microSD 16 GB+ (Samsung / SanDisk Endurance موصى به) | قرص النظام | **إلزامي** |
| التقاط Bluetooth 5 | **nRF52840** USB Dongle (مع برنامج ثابت sniffer، مثل Nordic Sniffer) | التقاط BT5 Long Range Remote ID | موصى به (اختياري) |
| مصدر طاقة | 5 V / 3 A USB-C (مصدر Pi الرسمي) | التغذية الكهربائية | **إلزامي** |
| شبكة | كابل Ethernet أو بيانات اعتماد WiFi | التحميل / الإدارة | **إلزامي** |
| هوائي محسّن | ALFA **APA-M25** هوائي لوحي اتجاهي | زيادة مدى الاستقبال، تقليل الضوضاء | اختياري |

> ملاحظة: القائمة الأصلية لمشروع المجتمع `DroneAware` تحدد **AWUS036N (Ralink RT3070، 2.4 GHz أحادي النطاق)** . تم ترقية هذه المجموعة إلى **AWUS036ACH (مزدوج النطاق)** ، القادرة على تغطية كل من **NAN و Beacon** في 2.4 / 5 GHz، مما يوفر تغطية أكثر اكتمالاً وقابلية توسع أفضل في المستقبل.

---

## 4. قائمة البرامج (Software List)

| البرنامج / الحزمة | الاستخدام | المصدر |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | نظام التشغيل (بدون واجهة) | raspberrypi.com |
| **برنامج تشغيل rtl88xxau** | برنامج تشغيل للمراقبة/الحقن لـ RTL8812AU | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`، `libbluetooth-dev`، `libncurses-dev` | تبعيات ترجمة `unix_rid_capture` | APT |
| **opendroneid-core-c** | مكتبة C لترميز/فك ترميز رسائل Open Drone ID (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | برنامج التقاط RID WiFi/BT للينكس (مخرجات JSON) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (اختياري) | الاتصال بخريطة المجتمع الفورية | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + إضافة ANTSDR (مسار DJI) | فك ترميز DJI OcuSync DroneID (يتطلب عتاد SDR) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. روابط المشاريع على GitHub

```text
# مكتبة فك الترميز الأساسية (ترميز/فك ترميز ASTM F3411 / EN 4709-002)
https://github.com/opendroneid/opendroneid-core-c

# برنامج التقاط للينكس (البرنامج الرئيسي لهذه المجموعة، تم التحقق منه rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# شبكة خرائط مجتمعية فورية (تثبيت بنقرة واحدة، رفع تلقائي إلى droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# إطار كشف لاسلكي (مسار DJI OcuSync يتطلب إضافة SDR)
https://github.com/kismetwireless/kismet

# برنامج تشغيل مراقبة/حقن RTL8812AU (إلزامي لـ AWUS036ACH)
https://github.com/morrownr/8812au-20210629
```

---

## 6. الإعداد خطوة بخطوة

### الخطوة 1 — حرق النظام

استخدم **Raspberry Pi Imager** لكتابة **Raspberry Pi OS Lite (64-bit)** . في الترس (الإعدادات المتقدمة):

- اسم المضيف: `droneid-kit`
- فعّل SSH واضبط اسم المستخدم وكلمة المرور
- أدخل بيانات اعتماد WiFi (لتجنب توصيل Ethernet لاحقاً)

### الخطوة 2 — التوصيل والتحقق من العتاد

صل AWUS036ACH مباشرة بمنفذ **USB 3.0** في Pi (باللون الأزرق / علامة `SS`)، وتأكد من ربط كلا الهوائيين بإحكام. بعد التشغيل، ادخل عبر SSH:

```bash
ssh <المستخدم>@droneid-kit.local
sudo -i
lsusb
```

يجب رؤية:

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### الخطوة 3 — تثبيت برنامج تشغيل المراقبة rtl88xxau

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### الخطوة 4 — التحقق من وضع المراقبة

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

يجب أن يُظهر الإخراج **`Mode:Monitor`** .

### الخطوة 5 — تثبيت تبعيات الترجمة

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### الخطوة 6 — ترجمة opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# ينتج libopendroneid/libopendroneid.so و test/odidtest
```

### الخطوة 7 — ترجمة unix_rid_capture

`unix_rid_capture` يحتاج `opendroneid.c` / `opendroneid.h`؛ انسخهما من الخطوة السابقة:

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### الخطوة 8 — تشغيل الالتقاط

مطلوب صلاحيات الجذر أو `cap_net_raw`:

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # التقاط وحفظ JSON
```

مخرجات UDP فورية (افتح طرفية أخرى):

```bash
nc -lu 32001
```

### الخطوة 9 — عرض المسارات (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # إنشاء .gpx
```

افتح باستخدام Google Earth لرؤية مسار طيران الطائرة بدون طيار. مثال JSON نموذجي:

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### الخطوة 10 — (اختياري) الاتصال بخريطة مجتمع DroneAware

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**نصيحة أمنية**: لأي سكريبت طرف ثالث مع `curl ... | sudo bash`، يُوصى بتنزيله ومراجعته قبل التشغيل: `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. سيكتشف المثبّت بطاقة USB تلقائياً، ويطلب اسم عقدة، ويوجه التسجيل في droneaware.io. تظهر نتائج الكشف فورياً على الخريطة الحية.
{{< /alert >}}

---

## 7. توضيح تقني مهم: RID القياسي مقابل DJI OcuSync

هذه هي القيمة المهنية للمقال؛ من المهم شرحها بوضوح للعميل:

| المسار | المسؤول | العتاد | هل يمكن استخدام ALFA AWUS036ACH؟ |
|---|---|---|---|
| **Remote ID القياسي** | بث ASTM F3411 WiFi/BT | AWUS036ACH + nRF52840 | ✅ نعم (الموضوع الرئيسي لهذا المقال) |
| **DJI OcuSync DroneID** | بروتوكول DJI الخاص (WiFi غير قياسي) | SDR كامل (ANTSDR / HackRF / USRP) + إضافة Kismet `kismet_cap_antsdr_droneid` | ❌ لا |

- ALFA AWUS036ACH هي **مستقبل في نطاقات WiFi (2.4 / 5 / 6 GHz)** ، قادرة على معالجة RID القياسي بالكامل.
- DroneID الخاص بـ **OcuSync** من DJI **لا يستخدم بروتوكول WiFi القياسي**، لذلك **بطاقة ALFA لا يمكنها فك تشفيره**؛ تحتاج SDR يغطي 2.4 / 5.8 GHz (مثل ANTSDR E200) مع إضافة `alphafox02/antsdr_dji_droneid` + Kismet.
- ⚠️ ملاحظة: **عرض نطاق RTL-SDR محدود بحوالي 1.7 GHz**، لذلك لا يمكنه رؤية OcuSync في 2.4 / 5.8 GHz؛ يجب اختيار SDR يدعم الترددات العالية.
- كلا المسارين **متكاملان**: بطاقة ALFA لكشف بثوث RID القياسية، SDR لفك بروتوكول DJI الخاص، مما يشكل واجهة أمامية كاملة لـ Counter-UAV / RF.

---

{{< faq >}}

---

## ملحق: قاموس المصطلحات للمبتدئين (مصطلحات رئيسية بلغة مبسطة)

إذا كانت هذه أول مرة تواجه فيها تقنية تنظيم / مكافحة الطائرات بدون طيار (Counter-UAV)، إليك شرح سريع للمصطلحات الأكثر استخداماً في هذا المقال:

| المصطلح | شرح مبسط |
|---|---|
| **Remote ID (التعريف عن بعد)** | «لوحة أرقام الطائرة الجوية». التشريعات تتطلب من الطائرات بدون طيار بث هويتها وموقعها باستمرار بعد الإقلاع، ليعرف من على الأرض (خاصة الجهات التنظيمية) «لمن هذه الطائرة وأين تتجه». |
| **ASTM F3411 / EN 4709-002** | معايير بث Remote ID الأمريكية والأوروبية على التوالي، تحدد محتوى وشكل البث لضمان قابلية التشغيل البيني بين طائرات وأجهزة كشف من شركات مختلفة. |
| **الكشف السلبي (Passive Detection)** | مجرد «الاستماع» للمعلومات العامة المُبَثة، دون إرسال إشارات نشطة للتشويش أو مهاجمة الطائرة. شرعيته مختلفة تماماً عن التشويش النشط (jamming). |
| **monitor mode (وضع المراقبة)** | يسمح لبطاقة WiFi بعدم الاتصال بأي موجه (router)، بل «الاستماع فقط» لحزم الراديو في الهواء؛ هو الشرط المسبق لالتقاط بثوث Remote ID. |
| **NAN (Wi-Fi Aware) / Beacon** | صيغتا إطار WiFi تستخدمهما الطائرات بدون طيار لبث Remote ID. هذه المجموعة تحاول تحليل كليهما في وقت واحد. |
| **Bluetooth 5 Long Range** | بالإضافة إلى WiFi، بعض الطائرات بدون طيار تبث Remote ID أيضاً عبر Bluetooth، وهذا يتطلب nRF52840 إضافياً لالتقاطه. |
| **DJI OcuSync / DroneID** | بروتوكول نقل فيديو/قياس عن بعد خاص بشركة DJI، **ليس WiFi قياسي** ولا Remote ID الذي يحله هذا المقال؛ يتطلب عتاد SDR مختلفاً تماماً وإضافات لفك تشفيره، موضح في القسم 7. |
| **SDR (Software Defined Radio)** | عتاد راديو معرف بالبرمجيات يسمح بضبط نطاق تردد الاستقبال وطريقة إزالة التشكيل عبر البرمجيات، مثل ANTSDR أو HackRF، قادر على تغطية نطاقات لا تستطيع بطاقة ALFA استقبالها (مثل DJI OcuSync). |
| **RTL8812AU** | طراز شريحة Realtek التي تستخدمها بطاقة ALFA AWUS036ACH، ويحدد دعمها لوضع المراقبة (monitor mode). |
| **ملف GPX** | تنسيق قياسي لتسجيل مسارات إحداثيات GPS، يمكن فتحه مباشرة باستخدام Google Earth لرسم مسار طيران الطائرة بدون طيار. |

> في جملة واحدة: هذا المقال يعلمك تحويل بطاقة ALFA إلى «ماسح هوية طائرات بدون طيار» — استقبال سلبي للمعلومات العامة التي يجب على الطائرات بدون طيار بثها قانونياً، وهي وسيلة قانونية لإدارة أمن المحيط.

---

## المراجع

1. [opendroneid/opendroneid-core-c — مكتبة C الأساسية لـ Open Drone ID](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — التقاط WiFi/BT RID (تم التحقق rtl8812au + nRF52840 + RPi)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — شبكة كشف Remote ID مجتمعية](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — إطار كشف لاسلكي](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — فك ترميز SDR لـ DJI OcuSync DroneID](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — برنامج تشغيل لينكس RTL8812AU للمراقبة/الحقن](https://github.com/morrownr/8812au-20210629)
7. [صفحة منتج ALFA AWUS036ACH (Yupitek)](https://yupitek.com/ar/products/alfa/awus036ach/)
8. [اتصال وطلبات Yupitek](https://www.yupitek.com/ar/contact/)

---

*تم إعداد هذا المقال من قبل الفريق التقني لشركة Yupitek. AWUS036ACH والعتاد المرتبط بها متوفرة عبر Yupitek كموزع معتمد، مع دعم فني.*
