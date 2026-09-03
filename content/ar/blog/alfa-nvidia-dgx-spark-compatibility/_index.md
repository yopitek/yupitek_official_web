---
title: "هل يدعم بطاقة الشبكة اللاسلكية ALFA NVIDIA DGX Spark (GB10)؟"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "دليل الأجهزة"
description: "DGX Spark支持ALFA网卡，MediaTek芯片型无需驱动，Realtek需编译驱动，USB-C转USB-A适配器必备。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. تلخيص المشكلة

يطرح العميل السؤال التالي: «هل يمكن استخدام بطاقات الشبكة اللاسلكية من سلسلة ALFA عبر منفذ USB في جهاز NVIDIA DGX Spark (GB10 Grace Blackwell) الذي يعمل بنظام AI الشخصي للمعالجة العالية؟»

الخلاصة القصيرة: نظام DGX Spark يعمل بنظام تشغيل NVIDIA DGX OS (مستند إلى Ubuntu،نواة 6.x)، ويتوافق بطاقات الشبكة اللاسلكية من سلسلة ALFA مع أنظمة Linux الحديثة للجداول الخشبية بشكل مماثل. تعمل نماذج المعالج MediaTek (AWUS036ACM / ACHM / AXML / AXM) باستخدام محرك التشغيل المدمج في النواة، وتعمل دون الحاجة إلى أي تعديلات. أما نماذج المعالج Realtek (AWUS036ACH / ACS / EACS / AX / AXER)则需要编译外部树状结构的驱动程序（ARM64 / aarch64）。تنبيه: جميع منافذ USB في DGX Spark هي من نوع USB Type-C، بينما تكون بطاقات الشبكة اللاسلكية من سلسلة ALFA من نوع USB Type-A، لذا يجب استخدام محول USB-C to USB-A أو كابل للتواصل.

الجسم الرئيسي: جميع بطاقات الشبكة اللاسلكية الـ 9 الموجودة حاليًا من سلسلة ALFA (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. تحليل هيكل المواصفات المادية الهدف

### 2.1 مواصفات المعدات المادية لـ NVIDIA DGX Spark

| العنصر | المواصفة |
|---|---|
| الاسم التجاري | NVIDIA DGX Spark |
| معالج الشريحة | NVIDIA GB10 Grace Blackwell Superchip |
| المعالج | 20 نواة Arm (10× Cortex-X925 + 10× Cortex-A725)،ARMv9.2-A |
| المعالج الرسومي | NVIDIA Blackwell Architecture،6144 نواة CUDA،الجيل الخامس Tensor Core،الجيل الرابع RT Core |
| أداء الذكاء الاصطناعي | أعلى 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| ذاكرة النظام | 128GB LPDDR5x ذاكرة مدمجة (256-bit،273 GB/s) |
| التخزين | أعلى 4TB NVMe M.2 SSD (م加密) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps)،أحدها يدعم PD الإدخال (180W EPR PD3.1) |
| مخرجات العرض | 1× HDMI 2.1a |
| الشبكة الموصلة بالسلك | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (200G QSFP) |
| الشبكة اللاسلكية | Wi-Fi 7 (مدمج) + Bluetooth 5.4 |
| نظام التشغيل | NVIDIA DGX OS (قائم على Ubuntu Linux،kernel 6.x) |
| التركيب | aarch64 (ARM64) |
| الحجم | 150 × 150 × 50.5 mm (1.13L) |
| الوزن | حوالي 1.2 كجم |
| التغذية | مزود بالطاقة بواسطة ميزة USB-C 240W |

### 2.2 بيئة البرمجيات: NVIDIA DGX OS

| العنصر | الشرح |
|---|---|
| الأساس | Ubuntu Linux (مخصص من قبل NVIDIA) |
| النواة | Linux 6.x (النسخة المحددة تتغير مع تحديث DGX OS) |
| التركيب | aarch64 (ARM64) |
| البرمجيات المدمجة | مجموعة NVIDIA AI (CUDA،cuDNN،TensorRT،PyTorch،Jupyter،الخ) |
| إدارة الحزم | apt (نظام Debian/Ubuntu) |
| إطار التشغيل | بنية driver النواة Linux القياسية (cfg80211 / mac80211) |

### 2.3 ميزات رئيسية: kernel حديث + ARM64

بيئة البرمجيات الخاصة بـ DGX Spark لها تأثيرين رئيسيين على توافق بطاقات ALFA الشبكية:

- النواة 6.x (حديثة): يمكن استخدام جميع drivers WiFi التي دخلت إلى mainline مباشرة، بما في ذلك mt76 (MT7612U / MT7610U) و mt7921u (MT7921AUN). هذا يعتبر فرقًا واضحًا مع kernel 4.9 في Jetson Nano.
- بنية ARM64 (aarch64): يتطلب drivers Realtek out-of-tree (8812au / 8821cu / rtl8852bu) الترجمة على ARM64. تم دعم الترجمة على ARM64 في upstream (morrownr)،لكن يجب التحقق من Makefile لضمان إعداد CONFIG_PLATFORM_ARM64 = y.

### 2.4 احتياجات التحويل لـ USB Type-C

تكون جميع منافذ USB في DGX Spark من نوع Type-C،بينما تكون جميع بطاقات الشبكة الخاصة بـ ALFA (معدة AXML باستثناء) من نوع USB Type-A:

| النموذج | مواصفة الواجهة | هل يحتاج إلى تحويل؟ |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ لا يحتاج إلى تحويل (يمكن إدخالها مباشرة) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ يحتاج إلى USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ يحتاج إلى تحويل |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ يحتاج إلى تحويل |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ يحتاج إلى تحويل |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ يحتاج إلى تحويل |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ يحتاج إلى تحويل |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ يحتاج إلى تحويل |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ يحتاج إلى تحويل |

النصيحة: استخدم محول USB-C to USB-A أو خط نقل يدعم USB 3.2 Gen 2×2 (20Gbps) لضمان أن يمكن للنماذج AWUS036ACH / ACM / AX إظهار أداء USB 3.x الكامل.

## 3. تحليل مواصفات بطاقات الشبكة الـ ALFA الحالية ووحدة المعالجة المركزية

حتى سبتمبر 2026، تشمل خط منتجات بطاقات الشبكة الـ ALFA Network الـ USB اللاسلكية الحالية ما يلي (الجسم الرئيسي: 9 نماذج)：

| النموذج | مستوى Wi-Fi | وحدة المعالجة المركزية | واجهة | حالة القيادة في نظام Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ في النواة (mt7921u، النواة 5.19+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ في النواة (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 (النواة 5.16+، دعم USB يتم إضافته تدريجيا) أو خارج النواة |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ كما أعلاه |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ خارج النواة (morrownr/8812au، يتطلب ترجمة ARM64) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ في النواة (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ في النواة (mt76x2u)⭐ الموصى بها |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ خارج النواة (8812au تغطيها) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ خارج النواة (morrownr/8821cu) |

## 4. أنواع الموديلات والمجموعات الداخلية

### 4.1 تصنيف التوصية

| مستوى التوصية | نموذج (المجموعة الداخلية) | شرح |
|---|---|---|
| ⭐ توصية قوية | AWUS036ACM (MT7612U) | محرك درايف في النواة، جاهز للإستخدام، AC1200 دوبل باند، يدعم AP / Monitor / Injection |
| ✅ توصية | AWUS036ACHM (MT7610U) | محرك درايف في النواة، استهلاك طاقة منخفض، AC433 دوبل باند |
| ✅ توصية (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | محرك درايف في النواة، Wi-Fi 6E، AXML يدعم USB-C مباشرة |
| ⚠️ متاح لكن يتطلب ترجمة | AWUS036ACH (RTL8812AU) | يتطلب ترجمة morrownr/8812au (ARM64)، بعد الترجمة تكون الوظائف كاملة (بما في ذلك Monitor / Injection) |
| ⚠️ متاح لكن يتطلب ترجمة | AWUS036ACS (RTL8811AU) | تغطيته من خلال محرك درايف 8812au |
| ⚠️ متاح لكن يتطلب الانتباه | AWUS036EACS (RTL8811CU) | يتطلب ترجمة morrownr/8821cu (ARM64) |
| ⚠️ متاح لكن يتطلب الانتباه | AWUS036AX / AXER (RTL8832BU) | قد يدعم kernel 6.x rtw89 USB؛ إذا لم يكن هناك حاجة إلى الترجمة خارج الشجرة |

### 4.2 نصائح حول الاستخدام

| سيناريو الاستخدام | نموذج التوصية | شرح |
|---|---|---|
| اتصال لاسلكي عادي (أبسط) | AWUS036ACM / ACHM | محرك درايف في النواة، لا يتطلب ترجمة، جاهز للإستخدام |
| اختبار التسرب اللاسلكي / الاستماع / التدخلات | AWUS036ACH أو AWUS036ACM | كلاهما يدعم Monitor + Injection؛ ACH يتطلب ترجمة، ACM جاهز للإستخدام |
| Wi-Fi 6E / تردد 6GHz | AWUS036AXML / AXM | محرك درايف في النواة، يدعم kernel 6.x بشكل كامل |
| لديك AWUS036ACH وتريد الاستمرار في استخدامه | AWUS036ACH | يمكنك ترجمة محرك درايف ARM64 للحصول على الوظائف الكاملة |
| لا تحتاج إلى WiFi خارجي (استخدام الداخلي) | — | DGX Spark يحتوي على Wi-Fi 7 + Bluetooth 5.4، لا يتطلب اتصال خارجي لـ ALFA في معظم سيناريوهات الاتصال |

ملاحظة: DGX Spark يحتوي على Wi-Fi 7 + Bluetooth 5.4، لا يتطلب اتصال خارجي لـ ALFA في معظم سيناريوهات الاتصال. الهدف الرئيسي من اتصال ALFA الخارجي هو اختبار التسرب اللاسلكي (الاستماع / التدخلات)، احتياجات مجموعة داخلية معينة، أو إذا لم يكن WiFi الداخلي كافيًا.

## 5. متطلبات البيئة

### 5.1 متطلبات الأجهزة

| العنصر | المتطلبات |
|---|---|
| محول USB | محول USB-C إلى USB-A أو كابل التحويل (استثناء AXML) |
| التغذية الكهربائية | مزود الطاقة الأصلي لـ DGX Spark 240W USB-C (كما أن وصلات USB توفر تغذية كافية) |
| التبريد | التبريد الأصلي يكفي (USB WiFi لن يؤدي إلى زيادة كبيرة في حمل النظام) |

### 5.2 متطلبات البرمجيات

| العنصر | المتطلبات |
|---|---|
| إصدار DGX OS | أي إصدار نشط (نواة 6.x) |
| أدوات الترجمة (بالنسبة لشريحة Realtek) | build-essential، git، bc، dkms |
| أدوات إدارة الواي فاي | iw، wpa_supplicant، network-manager (مثبت مسبقًا في DGX OS) |
| الشبكة | تحتاج إلى شبكة واي فاي قابلة للترجمة خلال عملية الترجمة (10GbE) أو واي فاي مدمج (Wi-Fi 7) |

## 6. تحديد التوافق

### جدول التوافق بين نماذج ALFA الحالية × NVIDIA DGX Spark (GB10)

| النموذج | المعالج | طريقة التشغيل | استشعار USB | الاتصال بالإنترنت عبر STA | نمط AP | الشاشة | صعوبة التثبيت | التقييم الشامل |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | بدون تثبيت | ⭐ أفضل |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ محدود | بدون تثبيت | ✅ جيد |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ محدود | بدون تثبيت | ✅ جيد |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ محدود | بدون تثبيت | ✅ جيد |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | متوسط (ترجمة) | ⚠️ قابلة الاستخدام |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | متوسط (ترجمة) | ⚠️ قابلة الاستخدام |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | متوسط (ترجمة) | ⚠️ قابلة الاستخدام |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | متوسط-عالي | ⚠️ قابلة الاستخدام |
| AWUS036AXER | RTL8832BU | كما هو | ✅ | ⚠️ | ⚠️ | ❌ | متوسط-عالي | ⚠️ قابلة الاستخدام |

معيار التحديد: توفر دفتر التشغيل الخاص بـ DGX OS 6.x لدعم محرك التشغيل الرئيسي + دعم محرك morrownr للـ ARM64. يتم تضمين معالجات MediaTek في محرك التشغيل الرئيسي، لذا يمكن استخدامها دون تثبيت إضافي في kernel 6.x. تحتاج معالجات Realtek إلى ترجمة محركات خارج الشجرة، ولكن تم دعم الترجمة للـ ARM64 من قبل المطورين.

## 7. تفاصيل دقيقة لخطوات الإعداد خطوة بخطوة

### 7.1 الأعمال التحضيرية

**الخطوة 1: إعادة التشغيل وال登입 إلى DGX Spark** (من خلال SSH أو الاتصال مباشرة باللوحة والشاشة)

```bash
ssh username@<dgx-spark-ip>
```

**الخطوة 2: التحقق من بنية النظام وأصدار kernel**

```bash
uname -m
# المتوقع: aarch64
uname -r
# المتوقع: 6.x.x (kernel نظام DGX)
```

**الخطوة 3: (للمعالجات Realtek) تثبيت أدوات التجميع**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 المسار A: نماذج المعالجات MediaTek (AWUS036ACM / ACHM / AXML / AXM) — جاهزة للإستخدام

**الخطوة 1: إدخال بطاقة الشبكة**

استخدم محول USB-C إلى USB-A، وضع بطاقة الشبكة ALFA في مخرج USB DGX Spark.

**الخطوة 2: التحقق من اكتشاف بطاقة الشبكة**

```bash
lsusb
# المتوقع: نتيجة م输出 مثال (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**الخطوة 3: التحقق من إنشاء واجهة الشبكة تلقائيًا**

```bash
ip link show
# المتوقع: ظهور wlan0 أو wlp... واجهة (تتم إعادة تحميل القيادة في النواة تلقائيًا)
```

**الخطوة 4: مسح شبكات WiFi**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**الخطوة 5: الاتصال بشبكة WiFi (استخدام NetworkManager)**

```bash
nmcli dev wifi list
nmcli dev wifi connect "اسم WiFi الخاص بك" password "كلمة المرور الخاصة بشبكة WiFi"
```

**الخطوة 6: (اختياري) تمكين الوضع الاستماعي**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 المسار B: نماذج المعالجات Realtek (AWUS036ACH / ACS / EACS) — يتطلب تجميع

بمثال AWUS036ACH (RTL8812AU):

**الخطوة 1: تنزيل أصل ملفات القيادة**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**الخطوة 2: التحقق من خيارات التجميع ARM64**

تعديل Makefile، التحقق من `CONFIG_PLATFORM_ARM64 = y` (يتم اكتشاف aarch64 تلقائيًا في معظم الإصدارات الجديدة).

**الخطوة 3: التجميع والتثبيت**

```bash
make
sudo make install
sudo modprobe 8812au
```

**الخطوة 4: إدخال بطاقة الشبكة (من خلال محول USB-C إلى USB-A)، التحقق من واجهة**

```bash
ip link show
# المتوقع: ظهور wlan0
```

**الخطوة 5: طريقة الاتصال مثل خطوة 7.2 الخطوة 5 (استخدام nmcli)**

**الخطوة 6: (اختياري) الاستماع والحقن**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 المسار C: نماذج Wi-Fi 6 (AWUS036AX / AXER، RTL8832BU)

**الخطوة 1: التحقق من دعم kernel للدعم المدمج لـ rtw89 USB**

```bash
# بعد إدخال البطاقة، التحقق
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# إذا ظهر wlan0 تلقائيًا، فإن دعم rtw89 في kernel 6.x يتم دعمه، يمكن استخدامها مباشرة
```

**الخطوة 2: إذا لم يتم دعم kernel تلقائيًا، قم بتجميع القيادة خارج الشجرة**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# التحقق من CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. الأخطاء الشائعة والطرق لحلها

| الأعراض | الأسباب المحتملة | طرق الحل |
|---|---|---|
| عدم رؤية بطاقة الشبكة ALFA في lsusb | عدم جودة محول USB-C أو عدم الاتصال الجيد | استبدال محول USB-C to USB-A؛ التأكد من أن المحول يدعم نقل البيانات (ليس فقط الشحن)؛ تجربة استخدام ميناء USB-C مختلف |
| عدم وجود واجهة wlan بعد إدخال معالج MediaTek | عدم تحميل module الخاص بالنواة تلقائيًا أو وجود firmware مفقود | تحميل module يدويًا: `sudo modprobe mt76x2u`؛ التحقق من `dmesg | grep mt76`؛ تثبيت firmware: `sudo apt install linux-firmware` |
| ظهور خطأ make عند تشغيل driver Realtek | خطأ في إعدادات التجميع المتقاطع | التأكد من التجميع الأصلي على DGX Spark (ليس التجميع المتقاطع)؛ عدم وجود إعداد CROSS_COMPILE في Makefile |
| ظهور رسالة "Operation not permitted" عند تشغيل modprobe 8812au | Secure Boot أو توقيع module | DGX Spark يُفترض عدم تمكين Secure Boot؛ إذا كان تم تمكينه، يجب توقيع module أو إيقاف Secure Boot |
| عدم استقرار الاتصال بالWiFi أو بطء السرعة | دعم محول USB-C فقط لـ USB 2.0 | استبدال محول يدعم USB 3.2 Gen 2×2؛ التأكد من أن المحول يحتوي على علامة "Data" وليس "Charge Only" |
| تعارض بين Wi-Fi الداخلي والبطاقة الخارجية ALFA | تعارض بين واجهتين لاسلكيتين في التوجيه | إيقاف WiFi الداخلي: `sudo nmcli radio wifi off` أو إيقافه في BIOS/UEFI؛ أو تعيين ترتيب التوجيه |
| عدم استخدام 6GHz (Wi-Fi 6E) | قيود منطقة التنظيم | تعيين منطقة التنظيم: `sudo iw reg set US` (الولايات المتحدة مفتوحة 6GHz)； التأكد من أن firmware الخاص بـ AWUS036AXML/AXM يدعم 6GHz |
| فشل بدء نمط AP | تعارض بين NetworkManager و hostapd | الاستعانة بمجلة Yupitek ALFA Soft AP؛ إيقاف NetworkManager من إدارة الواجهة بعد ذلك إعداد hostapd يدويًا |
| اختفاء بطاقة الشبكة بعد الاستيقاظ | إيقاف التشغيل التلقائي لـ USB | إيقاف التشغيل التلقائي لـ USB: `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. الحدود المعروفة

- **حاجة إلى محول USB Type-C**: باستثناء AXML، جميع بطاقات الشبكة ALFA تتطلب محول USB-C to USB-A، حيث يؤثر جودة المحول على الأداء والاستقرار.
- **ترجمة شريحة Realtek يدويًا**: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU لم تدخل في المجموعة الرئيسية، وتحتاج إلى ترجمة محرك التشغيل خارج الشجرة على ARM64.
- **إمكانية تعارض Wi-Fi 7 المدمج**: DGX Spark يحتوي على Wi-Fi 7 مدمج، ويمكن أن يحدث تعارض في الطرق أو الموارد عند استخدام Wi-Fi المدمج والخارجي في نفس الوقت.
- **إعداد نمط AP يدويًا**: DGX OS مخصص للبيئة التنموية، حيث يجب إعداد نقطة الوصول (AP) يدويًا باستخدام hostapd / dnsmasq.
- **قيود اللوائح على تردد 6GHz**: توفر طيف 6GHz لـ Wi-Fi 6E تعتمد على إعدادات منطقة القانون، ويجب التحقق من حالة فتح 6GHz في منطقة تايوان حديثًا.
- **اعتماد تحديث محركات التشغيل على المزود**: محركات التشغيل خارج الشجرة لـ Realtek يتم صيانتها من قبل المجتمع (morrownr)، وربما تحتاج إلى ترجمة جديدة بعد تحديث نواة DGX OS.
- **اختلافات في وظائف اختبار التسرب**: تحسنت وظيفة التسرب في سلسلة MediaTek mt76 على نواة 6.x، ولكن RTL8812au يظل الخيار التقليدي للمجتمع اختبار التسرب.
- **وظيفة بلوتوث**: لم يتم التحقق بشكل واسع من وظيفة بلوتوث 5.2 في AWUS036AXM على DGX OS (DGX Spark يحتوي على BT 5.4 مدمج).
- ⚠️ **يوصى بتجنب استخدام RTL8832BU (AWUS036AX/AXER)**: أعلن صاحب الصيانة morrownr رسميًا أن سلسلة rtl8852/32au «هي محركات تشغيل سيئة، يشتبه في وجود مشاكل في الشريحة نفسها»، ويُنصح المستخدمين على تجنب استخدامها في Linux (مصدر في الفصل 10). يجب فهم التصنيفات «⚠️ قابلة للتشغيل ولكن يجب الانتباه لها» في الفصول 4 و6 كتفاهمات عامة في الصناعة لا تنصح فقط بالصعوبة في التثبيت.
- **تحديد RTL8812AU «out-of-tree» ك2026**: في الواقع، تم دمج محرك التشغيل المتوافق مع معيار mac80211 للشريحة في المجموعة الرئيسية في **kernel 6.13، وأصبح جيدًا في kernel 6.14** (إعلان رسمي من morrownr)، ويمكن أن يستخدم AWUS036ACH دون ترجمة إذا كان DGX OS يستخدم نواة 6.14+. يُنصح بمطالبة العملاء بتقديم `uname -r` قبل الرد.

الشروط المضادة: إذا تغيرت إصدار نواة DGX OS أو محركات التشغيل للمعالج USB بعد التحديث، أو إذا توقفت صيانة فرع ARM64 لمحرك التشغيل morrownr، يجب مراجعة جدول التوافق في الفصل 6. إذا تم دمج دعم USB لـ rtw89 في kernel 6.x بشكل رسمي، يمكن أن يتم تحديث تصنيف AWUS036AX / AXER من «قابل للتشغيل ولكن يجب الانتباه له» إلى «قابل للتشغيل».

## 10. مصادر الاستشارة URL

| المصدر | الشرح | URL | حالة التحقق | تاريخ التحقق |
|---|---|---|---|---|
| صفحة NVIDIA DGX Spark الرسمية | معلومات حول مواصفات DGX Spark و المنصة | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ تم التحقق | 2026-09-03 |
| وثائق NVIDIA DGX | بنية نظام التشغيل DGX OS و إصدار kernel | https://docs.nvidia.com/dgx/dgx-spark | ✅ تم التحقق | 2026-09-03 |
| morrownr/8812au GitHub | محرك RTL8812AU Linux (دعم ARM64) | https://github.com/morrownr/8812au-20210820 | ✅ تم التحقق | 2026-09-03 |
| morrownr/8821cu GitHub | محرك RTL8811CU Linux | https://github.com/morrownr/8821cu-20210916 | ✅ تم التحقق | 2026-09-03 |
| morrownr/rtl8852bu GitHub | محرك RTL8832BU Linux | https://github.com/morrownr/rtl8852bu-20250826 | ✅ تم التحقق | 2026-09-03 |
| وثائق محرك mt76 Linux kernel | وثائق محرك MediaTek mt76 / mt7921 mainline (تتضمن إصدارات kernel الداعمة لكل معالج) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ تم التحقق | 2026-09-03 |
| دليل Linux Guide للSoft AP WiFi Hotspot من ALFA (Yupitek) | دليل حول كيفية إعداد نمط AP على Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ تم التحقق | 2026-09-03 |
| ملخص منتجات شبكة ALFA (Yupitek) | مواصفات المنتجات الحالية لـ ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ تم التحقق | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | بيان رسمي من مدير المحرك: يُنصح بتجنب استخدام مكونات RTL8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ تم التحقق | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | بيانات أحدث حول محرك RTL8812AU (إدراج في kernel 6.13، مستوى جودة 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ تم التحقق | 2026-09-03 |

مقالات مرتبطة: [هل يدعم بطاقة الشبكة اللاسلكية ALFA MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/) | [هل يدعم بطاقة الشبكة اللاسلكية ALFA ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/) | [هل يدعم بطاقة الشبكة اللاسلكية ALFA ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/) | [هل يدعم بطاقة الشبكة اللاسلكية ALFA GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [هل يدعم بطاقة الشبكة اللاسلكية ALFA NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

بيان الإعفاء من المسؤولية: تحديد التوافق في هذا المقال يعتمد على NVIDIA DGX OS (kernel 6.x, aarch64). محركات MediaTek للمعالجات تكون Linux mainline، مستوى الاستقرار مرتفع؛ بينما محركات Realtek للمعالجات تكون تحت صيانة المجتمع (morrownr)، ويمكن أن تتغير مستوى الاستقرار مع الإصدارات. تم دمج Wi-Fi 7 في DGX Spark، ويستخدم جهاز الشبكة اللاسلكية من ALFA بشكل رئيسي لأغراض اختبارات التداخل أو احتياجات مكونات معالج خاصة. جودة محول USB-C ستؤثر مباشرة على تجربة الاستخدام، ويُنصح باختيار محولات ماركة معروفة وتحمل علامة USB 3.2 Gen 2×2.
