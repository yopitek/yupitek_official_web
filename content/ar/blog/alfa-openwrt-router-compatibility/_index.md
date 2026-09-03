---
title: "مستوى دعم بطاقة الشبكة اللاسلكية ALFA لـ OpenWrt"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "دليل الأجهزة"
description: "OpenWrt最佳支持ALFA USB WiFi卡，MT76芯片型直接支持，Realtek需社区驱动，首选AWUS036ACM。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. ملخص المشكلة

السؤال الذي طُلبه العميل: «هل يمكن استخدام بطاقات الشبكة اللاسلكية USB من سلسلة ALFA في روتر OpenWrt؟»

الخلاصة القصيرة: OpenWrt يُعتبر أفضل منصة من بين الثلاثة أنظمة التشغيل الثالثة للروترور (DD-WRT / OpenWrt / Tomato) في دعم بطاقات الشبكة اللاسلكية USB من سلسلة ALFA. حيث يمكن دعم موديلات المعالجات MediaTek (AWUS036ACM / ACHM / AXML / AXM) عبر套اجات kmod-mt76 الرسمية؛ بينما تحتاج موديلات المعالجات Realtek (AWUS036ACH / ACS / EACS / AX / AXER) إلى استخدام套اجات القيادة خارج الشجرة (out-of-tree) التي تُعتني بها المجتمع، ويمكن أن تختلف قابلية الاستخدام بناءً على إصدار OpenWrt. يُفضل استخدام AWUS036ACM (MT7612U) حيث أن القيادة متقدمة ومستقرة وتدعم الاستماع والإدراج.

الجسم المحدد: جميع بطاقات الشبكة اللاسلكية USB من سلسلة ALFA الحالية (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. تحليل مواصفات وتحديد احتياجات البرمجيات المستهدفة

### 2.1 ما هو OpenWrt

OpenWrt هو نظام تشغيل روتير مفتوح المصدر متعدد الاستخدامات، يعتمد على kernel Linux و نظام إدارة الحزم opkg. على عكس DD-WRT / Tomato، يقدم OpenWrt برامج التشغيل كحزم kernel module (kmod) قابلة للتنزيل بشكل مستقل، مما يتيح للمستخدمين تثبيت برامج تشغيل WiFi USB دون الحاجة إلى إعادة ترميز النظام بأكمله.

### 2.2 إطار برامج تشغيل WiFi USB في OpenWrt

تتضمن مكتبة الحزم الرسمية لـ OpenWrt برامج تشغيل WiFi USB التالية:

| حزمة برمجية | مصدر | تغطي جهاز / نموذج | حالة الصيانة |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | رسمي في kernel | MediaTek MT7612U (AWUS036ACM) | نشط، مستقر |
| kmod-mt76-usb + kmod-mt76x0u | رسمي في kernel | MediaTek MT7610U (AWUS036ACHM) | نشط |
| kmod-mt7921u | رسمي في kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | متاح في إصدار 23.05+ |
| kmod-rtl8812au-ct | مجتمع out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | صيانة مجتمعية، هناك تقارير عن تحطم kernel في 24.10 |
| kmod-rtl8821cu | مجتمع out-of-tree | Realtek RTL8811CU (AWUS036EACS) | صيانة مجتمعية |
| kmod-rtw89 / kmod-rtl8852bu | قيد التطوير | Realtek RTL8832BU (AWUS036AX / AXER) | دعم USB rtw89 يتم تدريجياً إدراجه، يتطلب kernel حديث |

### 2.3 الشروط الأساسية: دعم نواة USB

قبل تثبيت برامج تشغيل WiFi USB، يجب التأكد من أن OpenWrt قد تم تفعيل دعم نواة USB:

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

معظم إصدارات OpenWrt الحديثة تأتي مسبقًا بـ kmod-usb-core، ولكن usbutils (الذي يقدم أمر lsusb) يجب تثبيته يدويًا.

## 3. تحليل مواصفات بطاقات الشبكة الخاصة بـ ALFA ووحدة المعالجة المركزية

حتى سبتمبر 2026، تشمل خط منتجات بطاقات الشبكة اللاسلكية الخاصة بـ ALFA Network الحالية ما يلي (الجسم الرئيسي: 9 نماذج)：

| النموذج | مستوى Wi-Fi | وحدة المعالجة المركزية | واجهة | حزمة أجهزة التوجيه OpenWrt |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (في التطوير) / rtl8852bu مكتوبة |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | كما هو الحال أعلاه |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (المجتمع) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (رسمي) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (رسمي)⭐ المفضل |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (مغطى) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu (المجتمع) |

## 4. أنواع الموديلات والمجموعات الداخلية

### 4.1 تصنيف التوصية

| مستوى التوصية | نموذج (المجموعة الداخلية) | شرح |
|---|---|---|
| ⭐ توصية قوية | AWUS036ACM (MT7612U) | محرك التشغيل الرسمي ناضج ومستقر، يدعم AP / STA / Monitor / Injection، أفضل اختيار على OpenWrt |
| ✅ توصية | AWUS036ACHM (MT7610U) | محرك التشغيل الرسمي، دوبل باند لكن بسرعة 433Mbps فقط، مناسب لسيناريوهات استهلاك الطاقة المنخفضة |
| ✅ توصية (إصدار جديد) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E، محرك التشغيل الرسمي، يتطلب OpenWrt 23.05+ وkernel 5.15+ |
| ⚠️ متاح لكن يجب الانتباه | AWUS036ACH (RTL8812AU) | محرك التشغيل المجتمعي، هناك تقارير عن Kernel Crash في إصدار 24.10، يُنصح باستخدام 23.05 |
| ⚠️ متاح لكن يجب الانتباه | AWUS036ACS (RTL8811AU) | كما في السابق، تغطي محركات 8812au |
| ⚠️ متاح لكن يجب الانتباه | AWUS036EACS (RTL8811CU) | محرك التشغيل المجتمعي، مستقرية متوسطة |
| ❌ غير مستحسن | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6، دعم rtw89 USB في طور التطوير، لا يمكن استخدام معظم إصدارات OpenWrt مباشرة |

### 4.2 متطلبات الأجهزة للراوتر

| عنصر | متطلبات الحد الأدنى | متطلبات التوصية |
|---|---|---|
| مخرج USB | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX Series) |
| Flash | 16MB (تثبيت محرك التشغيل + مكتبات إضافية) | 32MB+ |
| RAM | 128MB | 256MB+ (وضع AP + مستخدمين متعددين) |
| إصدار OpenWrt | 21.02+ | 23.05.x (الإصدار المستقر) |

## 5. متطلبات البيئة

### 5.1 بيئة البرمجيات

- إصدار مستقر من OpenWrt: 23.05.x (نواة 5.15) أو 24.10.x (نواة 6.6)
- مصادر الحزم: مكتبة حزم opkg الرسمية (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- الاتصال بالشبكة: يجب أن يكون جهاز التوجيه قادرًا على الاتصال بالشبكة خلال عملية تثبيت القيادة (من خلال واجهة WAN)

### 5.2 بيئة الهاردوير

- جهاز توجيه متوافق مع OpenWrt يحتوي على واجهة USB 2.0 / 3.0
- للنماذج عالية الطاقة (AWUS036ACH)، يُنصح باستخدام هاب USB 3.0 بتغذية طاقة، لتجنب قلة تغذية واجهة USB في جهاز التوجيه
- نموذج AWUS036AXML يحتوي على واجهة USB-C، ويجب التأكد من أن جهاز التوجيه يحتوي على واجهة USB-C أو استخدام محوّل USB-C to USB-A

## 6. تحديد التوافق

### جدول التوافق بين نماذج ALFA الحالية و OpenWrt

| النموذج | المعالج | طريقة التشغيل | استشعار USB | الاتصال عبر STA | نموذج AP | المراقبة | الإصدار الأدنى | التقييم الشامل |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ أفضل |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ محدود | 21.02+ | ✅ جيد |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ محدود | 23.05+ | ✅ جيد |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ محدود | 23.05+ | ✅ جيد |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ محدود | 22.03+（24.10 مع خطأ） | ⚠️ قابلة الاستخدام |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ قابلة الاستخدام |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ قابلة الاستخدام |
| AWUS036AX | RTL8832BU | rtw89 (في التطوير) | ⚠️ | ❌ | ❌ | ❌ | يتطلب ترجمة مخصصة | ❌ غير موصى به |
| AWUS036AXER | RTL8832BU | rtw89 (في التطوير) | ⚠️ | ❌ | ❌ | ❌ | يتطلب ترجمة مخصصة | ❌ غير موصى به |

معيار التحديد: توفر مكتبة套اجات OpenWrt الرسمية (23.05 / 24.10) للـ kmod + تقارير المستخدمين في منتدى OpenWrt. يتم صيانة محركات Realtek بشكل مجتمعي، وقد لا تكون الاستقرار والكاملية مثل MediaTek mt76 سلسلة.

## 7. تفاصيل دقيقة خطوة بخطوة للاعدادات

### 7.1 الأعمال التحضيرية: تمكين دعم نواة USB

**الخطوة 1: تسجيل الدخول إلى جهاز التوجيه OpenWrt عبر SSH**

```bash
ssh root@192.168.1.1
```

**الخطوة 2: تحديث مكتبات الحزم وتثبيت دعم نواة USB**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**الخطوة 3: إدخال بطاقة الشبكة ALFA، وتأكيد اكتشاف USB**

```bash
lsusb
# مخرجات التوقعات مثال (AWUS036ACM / MT7612U)：
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 المسار A: أجهزة MediaTek (AWUS036ACM / ACHM / AXML / AXM)

بمثال AWUS036ACM (MT7612U):

**الخطوة 1: تثبيت حزمة التشغيل**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — استبدل
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — استبدل (يحتاج إلى 23.05+)
# opkg install kmod-mt7921u
```

**الخطوة 2: تثبيت أدوات إدارة الشبكة اللاسلكية**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**الخطوة 3: تأكيد إنشاء واجهة الشبكة**

```bash
iw dev
# مخرجات التوقعات: wlan0 أو wlan1
```

**الخطوة 4: مسح قائمة WiFi القريبة (لتحقق من الوظائف)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**الخطوة 5: إعداد كائن المستخدم STA (الانضمام إلى AP موجود)**

تعديل ملف /etc/config/wireless:

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'اسم WiFi الخاص بك'
       option encryption 'psk2'
       option key 'كلمة المرور الخاصة بك'
```

**الخطوة 6: إعادة تشغيل خدمة الشبكة**

```bash
/etc/init.d/network restart
```

**الخطوة 7: إعداد كائن المستخدم AP (تشارك الشبكة)**

تعديل ملف /etc/config/wireless، قم بتغيير mode إلى ap:

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'كلمة المرور الخاصة بك'
```

**الخطوة 8: تمكين الوضع الاستماعي (للاختبار بالتسرب)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# التحقق
iw dev wlan0 info
# type يجب أن يظهر monitor
```

### 7.3 المسار B: أجهزة Realtek (AWUS036ACH / ACS / EACS)

بمثال AWUS036ACH (RTL8812AU):

**الخطوة 1: تثبيت حزمة التشغيل المجتمعية**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — استبدل
# opkg install kmod-rtl8821cu
```

**الخطوة 2: تثبيت أدوات إدارة الشبكة اللاسلكية**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**الخطوة 3: تأكيد واجهة الشبكة**

```bash
iw dev
# ملاحظة: واجهة الشبكة المسمى بـ rtl8812au-ct قد تكون wlan0 أو wlan1
```

الإعداد مشابه لـ 7.2 الخطوات 5-7 (وضع STA / AP).

**الخطوة 4: الوضع الاستماعي**

```bash
# يدعم تشغيل rtl8812au-ct الوضع الاستماعي
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# قد تكون هناك قيود في وظيفة إدخال البيانات، يُنصح باستخدام معالج mt76 للتجارب بالتسرب
```

**الخطوة 5: إذا واجهت kernel crash (مشكلة معروفة في الإصدار 24.10)**

```bash
# عودة إلى الإصدار الثابت 23.05، أو استخدام تشغيل مخصص للوحدة
# تفحص سجلات التهكيل
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 المسار C: نماذج Wi-Fi 6 (AWUS036AX / AXER،RTL8832BU)

⚠️ هذا المسار يتطلب ترجمة مخصصة لـ OpenWrt، وغير مناسب للمستخدمين العاديين.

**الخطوة 1: تأكيد أن الإصدار الحالي من OpenWrt يحتوي على دعم USB لـ rtw89**

```bash
opkg list | grep rtw89
# إذا لم يكن هناك نتيجة، فإن الإصدار لا يحتوي على الدعم
```

**الخطوة 2: إذا كنت بحاجة إلى استخدامه، يجب عليك ترجمة صورة OpenWrt الخاصة بك**

أضف kmod-rtw89 وfirmware المطلوب.

**البديل المقترح**: للاستخدامات التي تتطلب بطاقات USB Wi-Fi 6 في جهاز التوجيه OpenWrt، يُفضل استخدام AWUS036AXML (MT7921AUN) كالبديل.

## 8. الأخطاء الشائعة والطرق لحلها

| الأعراض | الأسباب المحتملة | طرق الحل |
|---|---|---|
| عدم رؤية بطاقة الشبكة ALFA في lsusb | عدم تثبيت نواة USB / نقص التغذية | التأكد من تثبيت kmod-usb-core kmod-usb2 kmod-usb3؛ استخدام ميزة USB Hub التي تحتوي على تغذية الكهرباء |
| رؤية بطاقة الشبكة في lsusb ولكن عدم وجود واجهة في iw dev | عدم تثبيت التطبيق أو عدم توافق التطبيق | تثبيت套ب kmod المناسب؛ التحقق من dmesg لمعرفة ما إذا كان هناك خطأ في التطبيق الثابت |
| ظهور رسالة "kernel version mismatch" عند تثبيت opkg kmod-mt76x2u | عدم تطابق إصدار OpenWrt مع إصدار مكتبة التطبيق | تنفيذ opkg update ثم المحاولة مرة أخرى؛ التحقق من تطابق إصدار الجهاز الثابت مع بنية مكتبة التطبيق |
| فشل بدء نمط AP (خطأ في hostapd) | عدم دعم التطبيق لنمط AP / إعدادات القناة غير صحيحة | التأكد من دعم المعالج لنمط AP؛ محاولة تعيين القناة الثابتة (مثل 6 أو 149)；التحقق من منطقة التنظيم |
| عدم القدرة على إدخال الحزم في نمط الاستماع | عدم دعم التطبيق للإدخال / تصادم القناة | دعم MediaTek mt76 أفضل؛ محدودية وظيفة الإدخال في Realtek 8812au-ct؛ التحقق من airmon-ng check kill |
| انقطاع الاتصال عند تشغيل AWUS036ACH في وضع الطاقة العالية | نقص التغذية في USB | استخدام ميزة USB 3.0 التي تحتوي على تغذية الكهرباء؛ تعديل إعدادات الطاقة في /etc/config/wireless لتقليل الطاقة (مثل option txpower '20') |
| Kernel panic بعد تثبيت rtl8812au-ct في إصدار 24.10 | مشكلة توافق في التطبيق | العودة إلى إصدار 23.05.x المستقر أو متابعة issue على GitHub للحصول على إصلاح |
| عدم استخدام MT7921 (AXML/AXM) في النطاق 6GHz | قيود منطقة التنظيم / إصدار النواة | الحاجة إلى نواة 5.19+ مع إعدادات منطقة Wi-Fi 6E الصحيحة؛ دعم النطاق 6GHz في OpenWrt 23.05 لا يزال قيد الاختبار |

## 9. الحدود المعروفة

- **تحذير**: قيادة Realtek للشريحة غير معروفة للصيانة في المجتمع: `kmod-rtl8812au-ct` و `kmod-rtl8821cu` ليست معروفة للصيانة من قبل OpenWrt، ولا يمكن ضمان استقرارها ومواعيد التحديث.
- **الإصدار 24.10 من rtl8812au-ct**: هناك تقارير عن تحطم النواة: يُنصح مستخدمي شريحة Realtek بالبقاء عند الإصدار 23.05.x.
- **دعم Wi-Fi 6 (RTL8832BU) غير كافٍ**: قيادة `rtw89 USB` في طور التطوير، لا يمكن استخدام AWUS036AX / AXER في معظم إصدارات OpenWrt بشكل مباشر.
- **أداء نموذج AP محدود**: عند استخدام WiFi USB كـ AP، يكون معدل التدفق أقل من WiFi المدمج في الراوتر (نطاق التردد + عوامل التداخل من القيادة).
- **اختلافات في وظائف الاستماع / التداخل**: دعم MediaTek mt76 سلسلة كامل الأداء؛ وظائف التداخل لشريحة Realtek محدودة، غير مناسبة للاختبارات الاحترافية للإختراق.
- **موارد الراوتر**: قد لا يكون هناك مساحة كافية بعد تثبيت القيادة في راوتر من الفئة المنخفضة (16MB Flash / 128MB RAM)، مما يؤثر على الوظائف الأخرى.
- **تداخل USB 3.0**: أجهزة USB 3.0 قد تؤثر على WiFi 2.4GHz، يُنصح باستخدام مخرج USB 2.0 أو مخرج USB Hub منفصل.
- **استخدام كروت الشبكة المتعددة في نفس الوقت**: عند استخدام WiFi المدمج في الراوتر + WiFi USB في نفس الوقت، قد يحدث تعارض في القنوات أو منافسة في الموارد.
- ⚠️ **RTL8832BU (AWUS036AX/AXER)**: قدمت قيادة القيادة نصيحة عامة بعدم استخدامها: في المقطع 4.1، تم وضع علامة "❌ غير مستحسن"، ليس فقط لأن قيادة `rtw89 USB` في طور التطوير، بل لأن قيادة القيادة `morrownr` قدمت تعليقًا عامًا بأن هذه السلسلة "مزعجة للقيادة، يشك في أن هناك مشكلة في الشريحة نفسها"، يُنصح باستخدام Linux حاليًا (مصدره في المقطع 10).
- **تحديد كلمات الحد الأدنى للإصدار النواة**: في المقطع 4.1، يُعتبر الكتابة "MT7921AUN يتطلب OpenWrt 23.05+ وkernel 5.15+" سهلة التشويه - في الواقع، تحتاج قيادة `mt7921u` في نظام التشغيل Linux على الحاسوب إلى **kernel 5.19+** لتكون موجودة (انظر تعليق قيادة القيادة)، ولكن عادة ما يتم إدخالها في套اجات OpenWrt الرسمية من خلال ميكانيكية backport، لذا لا يزال OpenWrt 23.05 (بالرغم من أن النواة الأساسية معروفة كـ 5.15) يحتوي على تقارير من المستخدمين حول نجاح تثبيت `kmod-mt7921u`. **يرجى التحقق من النتائج الفعلية باستخدام `opkg list` حسب إصدار العملاء، وليس من خلال الترجيع إلى إصدار النواة**.

شروط الرد: إذا تم إصلاح مشكلة تحطم النواة في إصدار 24.10 من `rtl8812au-ct` في تحديثات OpenWrt اللاحقة، يمكن رفع النصيحة في المقطع 4.1 والجزء 6 حول AWUS036ACH من "البقاء عند 23.05" إلى تحديث؛ إذا تم دمج دعم `rtw89 USB` بشكل رسمي في مكتبة OpenWrt الرسمية، يجب مراجعة الحكم "غير مستحسن" لـ AWUS036AX / AXER؛ إذا تم إصدار بيان صادر عن OpenWrt الرسمية يدعم MT7921 في 6GHz، يجب تحديث شرح القيود لـ AXML / AXM.

## 10. مصادر الاستشارة URL

| المصدر | الشرح | URL | حالة التحقق | تاريخ التحقق |
|---|---|---|---|---|
| وثائق OpenWrt الرسمية | مدخل وثائق OpenWrt الرسمية (إعدادات اللاسلكي / إدارة الحزم) | https://openwrt.org/docs/start | ✅ تم التحقق | 2026-09-03 |
| منتدى OpenWrt الرسمي | مدخل مناقشة محركات الـ USB WiFi | https://forum.openwrt.org/ | ✅ تم التحقق | 2026-09-03 |
| morrownr/8812au GitHub | المورد الأصلي لمحركات الـ RTL8812AU لـ Linux | https://github.com/morrownr/8812au-20210820 | ✅ تم التحقق | 2026-09-03 |
| ملخص منتجات ALFA Network (Yupitek) | مواصفات المنتجات الحالية لـ ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ تم التحقق | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | بيان رسمي من قدماء المحركات: يُنصح بتجنب الرقائق rtl8852/32au (RTL8832BU) | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ تم التحقق | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko يتطلب kernel 5.19+ ليظهر في النواة (كلام قدماء المحركات) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ تم التحقق | 2026-09-03 |
| منتدى OpenWrt الرسمي — أفضل وحدة توصيل WiFi USB للـ Raspberry Pi 4B | تقارير المستخدمين حول نجاح تثبيت kmod-mt7921u في OpenWrt 23.05.0 | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ تم التحقق | 2026-09-03 |

مقالات مرتبطة: [هل يدعم بطاقات الشبكة اللاسلكية الخاصة بـ ALFA DD-WRT؟](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[هل يدعم بطاقات الشبكة اللاسلكية الخاصة بـ ALFA Tomato؟](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[هل يدعم بطاقات الشبكة اللاسلكية الخاصة بـ ALFA NVIDIA DGX Spark؟](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[هل يدعم بطاقات الشبكة اللاسلكية الخاصة بـ ALFA NVIDIA Jetson Nano؟](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

بيان الإعفاء من المسؤولية: يتم تحديد التوافق في هذا المقال بناءً على مكتبة الحزم الرسمية لـ OpenWrt 23.05.x / 24.10.x. قد تختلف توفر الحزم بين بنيات الشبكات المختلفة (ath79 / ramips / mvebu / x86، إلخ). محركات شريحة Realtek هي محركات مجتمعية، وقد تتغير الاستقرار حسب الإصدار. يُنصح باختيار نماذج شريحة MediaTek (AWUS036ACM كأول اختيار) كخيار مفضل لـ OpenWrt USB WiFi.
