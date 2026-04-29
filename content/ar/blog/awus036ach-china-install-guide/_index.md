---
title: "دليل تثبيت تعريف ALFA AWUS036ACH للصين: Kali Linux وUbuntu وDebian وRaspberry Pi"
description: "دليل خطوة بخطوة لتثبيت تعريفات ALFA AWUS036ACH في الصين باستخدام المرايا المحلية. يغطي Kali Linux وUbuntu 22/24 وDebian وRaspberry Pi. لا يلزم الوصول إلى GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "تعريف", "الصين", "وضع-المراقبة"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
related_product: "/ar/products/alfa/awus036ach/"
dir: rtl
---

حصلتَ للتو على AWUS036ACH ولكن Linux لا يتعرف عليه. هذا أمر طبيعي — يحتاج هذا الشريحة إلى تعريف RTL8812AU وهو ليس جاهزاً للتشغيل فوراً. سيرشدك هذا الدليل خلال التثبيت الكامل في حوالي 30 دقيقة، باستخدام المرايا المحلية فقط. لا حاجة للوصول إلى GitHub.

## قبل البدء

تأكد من توفر ما يلي:

1. محوّل **ALFA AWUS036ACH**
2. كابل USB (الكابل المرفق في العلبة يعمل بشكل جيد)
3. محور USB بمصدر طاقة — ضروري إذا كنت تستخدم Raspberry Pi
4. اتصال إنترنت نشط للوصول إلى المرايا المحلية

وصّل المحوّل، ثم تحقق من أن النظام يراه:

```bash
lsusb
```

ابحث عن هذا في المخرجات:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

إذا رأيتَ `0bda:8812`، فقد تم اكتشاف المحوّل. انتقل إلى قسم نظام التشغيل الخاص بك أدناه.

إذا لم تره — جرّب منفذ USB مختلفاً أو استبدل الكابل، ثم شغّل `lsusb` مرة أخرى.

## اختر نظام التشغيل الخاص بك

انتقل إلى القسم المناسب لنظام التشغيل:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

هل التثبيت مكتمل بالفعل؟ انتقل مباشرةً إلى:

- [تفعيل وضع المراقبة](#enable-monitor-mode)
- [اختبار حقن الحزم](#test-packet-injection)
- [تمرير USB إلى الجهاز الافتراضي](#virtual-machine-usb-passthrough)

---

## Kali Linux

يأتي Kali بأدوات شبكات لاسلكية قوية مدمجة. يستغرق تشغيل تعريف AWUS036ACH أربع خطوات. ابدأ بالتبديل إلى مرآة صينية سريعة.

### الخطوة 1: التبديل إلى مرآة صينية

افتح ملف المصادر في الطرفية.

```bash
sudo nano /etc/apt/sources.list
```

احذف كل محتواه، ثم الصق هذا السطر:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ الملف: اضغط **Ctrl+O**، ثم Enter، ثم Ctrl+X للخروج. حدّث فهرس الحزم.

```bash
sudo apt update
```

> **مرآة احتياطية:** إذا كانت 中科大 (USTC) بطيئة، استخدم 清华 (Tsinghua) بدلاً من ذلك:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### الخطوة 2: تثبيت التعريف

يتضمن مستودع Kali حزمة DKMS جاهزة مسبقاً. ثبّتها بأمر واحد.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

يعيد DKMS تجميع التعريف تلقائياً عند تحديث النواة، لذا لن تحتاج إلى إعادة التثبيت يدوياً بعد الترقيات.

تحقق من تحميل التعريف بشكل صحيح.

```bash
modinfo 88XXau | grep -E "filename|version"
```

يجب أن ترى سطر `filename` ينتهي بـ `.ko` وسطر `version` يُظهر رقماً مثل `5.6.4.2`. إذا ظهر كلاهما، فالتعريف جاهز.

---

### الخطوة 2 (بديل): التجميع من المصدر

اتبع هذا القسم فقط إذا فشل `apt install` أعلاه. أولاً ثبّت تبعيات البناء.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

نزّل مصدر التعريف من Gitee.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **ملاحظة:** إذا لم يُحمَّل هذا الرابط، ابحث في Gitee عن `rtl8812au` واختر الفرع ذو أحدث تاريخ commit. يمكنك أيضاً تنزيل أرشيف المصدر مباشرةً من [files.alfa.com.tw](https://files.alfa.com.tw).

انتقل إلى المجلد المُنزَّل، ثم قم بالتجميع والتثبيت.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

حمّل التعريف في النواة الجارية.

```bash
sudo modprobe 88XXau
```

---

### الخطوة 3: تفعيل وضع المراقبة {#enable-monitor-mode}

قبل تحويل المحوّل إلى وضع المراقبة، تحقق من اسم الواجهة الذي خصّصه النظام.

```bash
iwconfig
```

ابحث عن إدخال `wlan0` أو `wlan1`. استخدم هذا الاسم في الأوامر أدناه.

أوقف NetworkManager وwpa_supplicant — كلاهما يتنافسان على المحوّل وسيحجبان وضع المراقبة.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

أكّد التبديل.

```bash
iwconfig
```

ابحث عن إدخال مثل `wlan0mon` مع `Mode:Monitor`. عندما تراه، يكون المحوّل جاهزاً لالتقاط الحزم.

---

### الخطوة 4: اختبار حقن الحزم {#test-packet-injection}

شغّل اختبار الحقن على واجهة المراقبة.

```bash
sudo aireplay-ng --test wlan0mon
```

نتيجة ناجحة تبدو هكذا:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

إذا فشل الاختبار، أعد تشغيل الجهاز وجرّب مرة أخرى. إذا استمر الفشل بعد إعادة التشغيل، تحقق من أن لا عملية أخرى تحتجز الواجهة — شغّل `iwconfig` وتأكد أنه يظهر فقط `wlan0mon`.

---

## Ubuntu 22.04 / 24.04

تنقسم Ubuntu إلى فرعين بتنسيقات ملفات حزم مختلفة. تتناول الخطوات أدناه الفرعين. استخدم **阿里云 (Aliyun)** كمرآة — سريعة وموثوقة ومدعومة من Alibaba.

### الخطوة 1: التبديل إلى مرآة صينية

اختر إصدار Ubuntu الخاص بك واتبع مساره فقط.

#### Ubuntu 24.04 (Noble)

افتح ملف المصادر بتنسيق DEB822 الجديد:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

احذف كل محتوى الملف والصق هذا:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

احفظ بـ `Ctrl+O`، ثم اخرج بـ `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

افتح ملف المصادر الكلاسيكي:

```bash
sudo nano /etc/apt/sources.list
```

استبدل كل الأسطر الموجودة بـ:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

احفظ واخرج بنفس الطريقة (`Ctrl+O`، ثم `Ctrl+X`).

#### تحديث فهرس الحزم

شغّل هذا لكلا الإصدارين بعد تعديل ملف المصادر:

```bash
sudo apt update
```

---

### الخطوة 2: تثبيت تبعيات البناء

يُجمَّع التعريف من المصدر، لذا تحتاج أولاً إلى ترويسات النواة وأدوات البناء:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

يكشف `$(uname -r)` عن إصدار نواتك تلقائياً — لا حاجة لكتابته يدوياً.

---

### الخطوة 3: تنزيل مصدر التعريف (مرآة صينية)

استنسخ مستودع التعريف من Gitee المتاح داخل الصين:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

انتقل إلى المجلد المُستنسَخ:

```bash
cd rtl8812au
```

> **ملاحظة:** إذا انتهت مهلة الرابط، اذهب إلى [gitee.com](https://gitee.com) وابحث عن `rtl8812au`. اختر الفرع ذو أحدث تاريخ commit.

---

### الخطوة 4: التجميع والتثبيت

ابنِ وحدة النواة من المصدر:

```bash
make
```

ثبّتها في النظام:

```bash
sudo make install
```

سجّل الوحدة مع DKMS لتبقى بعد تحديثات النواة:

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

حمّل الوحدة في النواة الجارية:

```bash
sudo modprobe 88XXau
```

تحقق من صحة التحميل:

```bash
modinfo 88XXau | grep filename
```

يجب أن ترى مساراً ينتهي بـ `88XXau.ko` أو ما يشابهه. إذا أعاد الأمر مخرجات، فالتعريف نشط.

---

### الخطوة 5: تفعيل وضع المراقبة

أولاً، أنهِ العمليات التي قد تتداخل مع الواجهة اللاسلكية:

```bash
sudo airmon-ng check kill
```

ثم حوّل المحوّل إلى وضع المراقبة:

```bash
sudo airmon-ng start wlan0
```

> **ملاحظة:** قد تكون الواجهة مسماة `wlan1` بدلاً من `wlan0`. شغّل `iwconfig` أولاً لرؤية جميع الواجهات اللاسلكية، ثم استبدل الاسم الصحيح في الأمر أعلاه.

---

### الخطوة 6: اختبار حقن الحزم

مع المحوّل في وضع المراقبة، شغّل اختبار الحقن:

```bash
sudo aireplay-ng --test wlan0mon
```

نتيجة ناجحة تُظهر أسطراً مثل `Injection is working!`. إذا رأيت أخطاء في الواجهة، تحقق مرتين من أن وضع المراقبة نشط: `iwconfig wlan0mon`.

---

## Debian

يشير مدير حزم Debian افتراضياً إلى خوادم خارجية. يرفع التبديل إلى مرآة 清华大学 (جامعة تسينغهوا) سرعة التنزيل.

### الخطوة 1: التبديل إلى مرآة صينية

افتح قائمة المصادر:

```bash
sudo nano /etc/apt/sources.list
```

احذف كل المحتوى والصق هذه الأسطر الثلاثة (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

احفظ بـ `Ctrl+O`، اخرج بـ `Ctrl+X`. حدّث فهرس الحزم:

```bash
sudo apt update
```

### الخطوة 2: تثبيت تبعيات البناء

يُجمَّع تعريف AWUS036ACH من المصدر، لذا ثبّت ترويسات النواة وأدوات البناء:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### الخطوة 3: تنزيل مصدر التعريف (مرآة صينية)

استنسخ المستودع من Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

انتقل إلى مجلد المشروع:

```bash
cd rtl8812au
```

> **لا يمكن الوصول إلى الرابط؟** ابحث في Gitee عن `rtl8812au` واختر الفرع الأحدث.

### الخطوة 4: التجميع والتثبيت

شغّل هذه الأوامر بالتسلسل داخل مجلد `rtl8812au`:

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

يسجّل `dkms` التعريف ليبقى تلقائياً بعد تحديثات النواة.

### الخطوة 5: تفعيل وضع المراقبة

**أنهِ العمليات المتداخلة** قبل تبديل الأوضاع:

```bash
sudo airmon-ng check kill
```

ابدأ وضع المراقبة على المحوّل:

```bash
sudo airmon-ng start wlan0
```

إذا كان `airmon-ng` غائباً، ثبّته أولاً:

```bash
sudo apt install -y aircrack-ng
```

أكّد ظهور الواجهة:

```bash
iwconfig
```

ابحث عن واجهة باسم `wlan0mon` في المخرجات.

### الخطوة 6: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan0mon
```

تدفق نتائج اختبار الحقن يؤكد عمل المحوّل.

---

## Raspberry Pi 4B / 5

> يستهلك AWUS036ACH حوالي 500mW. قد يتسبب التوصيل المباشر بمنفذ USB لـ Raspberry Pi في تقليص الأداء أو إعادة التشغيل تحت الحمل. **استخدم دائماً محور USB بمصدر طاقة.**

---

### الخطوة 1: تنزيل صورة Kali Linux ARM64

اذهب إلى صفحة تنزيلات Kali ARM الرسمية:
https://www.kali.org/get-kali/#kali-arm

اختر **Raspberry Pi 4 (64-bit)** أو **Raspberry Pi 5 (64-bit)** ليتوافق مع لوحتك. لا تنزّل الصورة 32-bit — بناء التعريف يتطلب نواة 64-bit.

> **مرآة صينية:** إذا كان kali.org بطيئاً، جرّب 华为云 بدلاً من ذلك:
> https://repo.huaweicloud.com/kali-images/
> تصفّح إلى مجلد الإصدار الأخير ونزّل صورة ARM64 من هناك.

---

### الخطوة 2: الكتابة على MicroSD

أدخل بطاقة microSD، ثم تحقق من مسار الجهاز قبل الكتابة.

```bash
lsblk
```

ابحث عن بطاقتك في القائمة — ستظهر كـ `sdb` أو `mmcblk0`. ثم اكتب الصورة، مستبدلاً `/dev/sdX` بمسارك الفعلي.

```bash
# استبدل /dev/sdX ببطاقة SD الفعلية (تحقق بـ lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

انتظر انتهاء `sync` قبل سحب البطاقة. شغّل Pi من البطاقة. بيانات الاعتماد الافتراضية: **kali / kali**.

---

### الخطوة 3: التبديل إلى مرآة صينية

بعد التشغيل الأول، افتح ملف مصادر الحزم.

```bash
sudo nano /etc/apt/sources.list
```

احذف كل محتوى الملف واستبدله بهذا السطر الواحد:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ: **Ctrl+O**، ثم Enter، ثم Ctrl+X. الآن طبّق المرآة وحدّث النظام.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

تلتقط إعادة التشغيل أي تحديثات للنواة قبل تثبيت التعريف.

---

### الخطوة 4: تثبيت التعريف (ARM64)

حزمة DKMS تعمل على ARM64 تماماً كما على x86 — لا خطوات خاصة مطلوبة.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

إذا أعاد الأمر خطأ يقول إن الحزمة غير موجودة، جمّع التعريف من المصدر:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### الخطوة 5: تفعيل وضع المراقبة

قبل لمس المحوّل، تحقق من اسم الواجهة الذي خصّصه Pi.

```bash
iwconfig
```

على Pi مع شريحة Wi-Fi مدمجة، يظهر AWUS036ACH كـ `wlan1` — إذ يأخذ الراديو المدمج `wlan0`. استخدم الاسم الذي أبلغ عنه `iwconfig`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

شغّل `iwconfig` مرة أخرى وابحث عن إدخال ينتهي بـ `mon` — عادةً `wlan1mon` في حالة Pi — مع `Mode:Monitor`. هذا يؤكد التبديل الناجح.

---

### الخطوة 6: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1mon
```

استبدل `wlan1mon` باسم واجهة المراقبة من الخطوة 5. يطبع المحوّل العامل `Injection is working!`. إذا فشل الاختبار، أعد التشغيل وحاول مرة أخرى. اتصال USB السيئ عبر محور غير مزوّد بطاقة هو السبب الأكثر شيوعاً على Pi.

---

## تمرير USB إلى الجهاز الافتراضي {#virtual-machine-usb-passthrough}

تشغّل Kali Linux داخل جهاز افتراضي على macOS أو Windows؟ تحتاج إلى تمرير محوّل USB إلى نظام التشغيل الضيف.

### VirtualBox

1. مع إيقاف تشغيل الجهاز الافتراضي، اذهب إلى **الإعدادات ← USB**.
2. فعّل **وحدة تحكم USB 3.0 (xHCI)**.
3. انقر أيقونة **+** لإضافة مرشّح USB.
4. اختر: **Realtek 802.11ac NIC [...]** (المعرّف: 0bda:8812).
5. شغّل الجهاز الافتراضي — سيظهر المحوّل داخل Kali.

داخل الجهاز الافتراضي، شغّل `lsusb` للتأكد من ظهور `0bda:8812`، ثم اتبع خطوات Kali Linux أعلاه.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. شغّل الجهاز الافتراضي.
2. في القائمة: **الجهاز الافتراضي ← USB والبلوتوث**.
3. ابحث عن **Realtek 802.11ac NIC** وانقر **اتصال**.
4. سينفصل المحوّل عن المضيف ويظهر داخل الجهاز الافتراضي.

شغّل `lsusb` داخل الجهاز الافتراضي للتأكد، ثم اتبع خطوات Kali Linux أعلاه.

### ملاحظة حول VIF (الواجهة الافتراضية)

شريحة RTL8812AU في AWUS036ACH لها دعم محدود لـ VIF على Linux. لا يمكن الاعتماد على تشغيل وضع الإدارة ووضع المراقبة (أو وضع AP) في نفس الوقت على نفس المحوّل.

إذا كان سير عملك يحتاج VIF — مثل تشغيل نقاط وصول وهمية مع المراقبة في نفس الوقت — فإن AWUS036ACH ليس الأداة المناسبة. اطّلع على [دليل تثبيت AWUS036ACM](/ar/blog/awus036acm-china-install-guide/). يستخدم ذلك المحوّل شريحة MT7612U مع دعم كامل لـ VIF في نواة Linux.

---

## استكشاف الأخطاء وإصلاحها

| المشكلة | السبب المحتمل | الحل |
|---------|--------------|-------|
| `lsusb` لا يُظهر 0bda:8812 | المحوّل غير مزوّد بطاقة أو كابل معيب | جرّب منفذ USB مختلفاً. استخدم محور بطاقة على Raspberry Pi. |
| `make` يفشل بأخطاء ترويسات | ترويسات النواة مفقودة أو عدم تطابق الإصدار | شغّل `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` يفشل | Secure Boot يحجب الوحدات غير الموقّعة | عطّل Secure Boot في BIOS، أو وقّع الوحدة |
| التعريف يختفي بعد تحديث النواة | التعريف غير مسجّل في DKMS | أعد تشغيل `sudo dkms install rtl8812au/$(cat VERSION)` من مجلد المصدر |
| `airmon-ng start wlan0` يفشل | NetworkManager لا يزال يعمل | شغّل `sudo airmon-ng check kill` أولاً |
| وضع المراقبة يعمل لكن لا يلتقط حركة مرور | قناة خاطئة أو اسم واجهة خاطئ | تحقق من الواجهة بـ `iwconfig`. اضبط القناة: `iwconfig wlan0mon channel 6` |
| اختبار الحقن يُظهر «No Answer» | نقطة الوصول بعيدة جداً أو واجهة خاطئة | اقترب من نقطة الوصول. استخدم `wlan0mon` لا `wlan0` |

## مرجع المرايا في الصين

جميع الموارد المستخدمة في هذا الدليل — لا يلزم GitHub:

| المورد | الرابط | الاستخدام |
|--------|--------|----------|
| التعريفات الرسمية لـ Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | حزم التعريفات، البرامج الثابتة |
| توثيق Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات |
| مرآة 清华大学 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| مرآة 阿里云 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (موصى به) |
| مرآة 中科大 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (موصى به) |
| مرآة 华为云 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | صور Kali ARM (احتياطي) |
| تعريف RTL8812AU (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | التجميع اليدوي (بديل) |

## أدلة محوّلات Alfa الأخرى للصين

هذا جزء من سلسلة **Alfa China Install Guide**. كل مقالة تغطي نموذج محوّل واحداً:

- AWUS036ACH ← أنت هنا
- [دليل AWUS036ACM للصين](/ar/blog/awus036acm-china-install-guide/) — MT7612U، أفضل دعم لـ VIF
- [دليل AWUS036ACS للصين](/ar/blog/awus036acs-china-install-guide/)
- [دليل AWUS036AX للصين](/ar/blog/awus036ax-china-install-guide/)
- [دليل AWUS036AXER للصين](/ar/blog/awus036axer-china-install-guide/)
- [دليل AWUS036AXM للصين](/ar/blog/awus036axm-china-install-guide/)
- [دليل AWUS036AXML للصين](/ar/blog/awus036axml-china-install-guide/)
- [دليل AWUS036EACS للصين](/ar/blog/awus036eacs-china-install-guide/)

هل لديك أسئلة؟ اترك تعليقاً أدناه أو تواصل معنا على [yupitek.com](https://yupitek.com/ar/contact/).
