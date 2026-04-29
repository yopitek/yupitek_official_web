---
title: "دليل تثبيت تعريف ALFA AWUS036ACM للصين: Kali Linux وUbuntu وDebian وRaspberry Pi"
description: "دليل خطوة بخطوة لتثبيت تعريفات ALFA AWUS036ACM في الصين باستخدام المرايا المحلية. تعريف MT7612U مدمج في النواة، دعم كامل لـ VIF. يغطي Kali Linux وUbuntu 22/24 وDebian وRaspberry Pi. لا حاجة لـ GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
dir: rtl
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "تعريف", "الصين", "وضع-المراقبة", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
related_product: "/ar/products/alfa/awus036acm/"
---

يُعدّ AWUS036ACM من أيسر محوّلات Alfa إعدادًا على Linux. تستخدم شريحته MT7612U تعريف `mt76x2u`، المدمج في نواة Linux منذ الإصدار 4.19. على معظم الأنظمة الحديثة، يعمل المحوّل بأمرين أو ثلاثة فحسب. يتناول هذا الدليل الإعداد الكامل — التحقق من التعريف، وتفعيل وضع المراقبة، وحقن الحزم، والواجهة الافتراضية (VIF) — باستخدام المرايا المحلية حصرًا. لا حاجة لـ GitHub.

## قبل البدء

تأكد من توافر ما يلي:

1. محوّل **ALFA AWUS036ACM**
2. كابل USB (الكابل المرفق في الصندوق مناسب تمامًا)
3. موزّع USB بمصدر طاقة مستقل — ضروري عند الاستخدام مع Raspberry Pi
4. اتصال إنترنت نشط للوصول إلى المرايا المحلية

وصّل المحوّل، ثم تأكد من أن النظام يتعرف عليه:

```bash
lsusb
```

ابحث عن هذا السطر في المخرجات:

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

إذا رأيت `0e8d:7612`، فالمحوّل مُكتشَف. انتقل إلى قسم نظام التشغيل الخاص بك أدناه.

إذا لم يظهر، جرّب منفذ USB آخر أو استبدل الكابل، ثم أعد تشغيل `lsusb`.

## اختر نظام التشغيل

انتقل إلى القسم المناسب لنظامك:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

إذا أتممت التثبيت مسبقًا، انتقل مباشرةً إلى:

- [تفعيل وضع المراقبة](#enable-monitor-mode)
- [اختبار حقن الحزم](#test-packet-injection)
- [الواجهة الافتراضية (VIF)](#virtual-interface-vif)
- [تمرير USB إلى الآلة الافتراضية](#virtual-machine-usb-passthrough)

---

## Kali Linux

تعريف MT7612U مدرج بالفعل في نواة Kali. في معظم الحالات يعمل المحوّل فور توصيله. تتحقق الخطوات التالية من تحميل التعريف وتوجّهك عبر وضع المراقبة.

### الخطوة 1: التحويل إلى مرايا الصين

افتح قائمة المصادر في الطرفية.

```bash
sudo nano /etc/apt/sources.list
```

احذف كل ما فيه، ثم ألصق هذا السطر:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ بالضغط على **Ctrl+O**، ثم Enter، ثم Ctrl+X للخروج. حدّث فهرس الحزم.

```bash
sudo apt update
```

> **مرآة احتياطية:** إذا كانت 中科大 (USTC) بطيئة، استخدم 清华 (Tsinghua) بدلًا منها:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### الخطوة 2: التحقق من التعريف

تحقق مما إذا كانت الوحدة قد تحملت تلقائيًا عند توصيل المحوّل.

```bash
lsmod | grep mt76
```

يجب أن ترى في المخرجات `mt76x2u`. إذا لم يظهر شيء، حمّله يدويًا.

```bash
sudo modprobe mt76x2u
```

أعد تشغيل `lsmod | grep mt76` للتأكيد. ثم تحقق من أن المحوّل يعمل.

```bash
iwconfig
```

ابحث عن واجهة لاسلكية — في العادة `wlan0` أو `wlan1`. إذا ظهرت الواجهة مع ESSID أو `unassociated`، فالتعريف يعمل.

---

### الخطوة 2 (بديلة): تثبيت وحدات النواة الإضافية

إذا أعطى `modprobe mt76x2u` خطأ "Module not found"، فقد تكون وحدات MT76 مفقودة من بنية النواة. ثبّتها من مرايا الصين.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

بعد اكتمال التثبيت، حمّل الوحدة مجددًا.

```bash
sudo modprobe mt76x2u
```

إذا لم تكن الحزمة متاحة لإصدار نواتك تحديدًا، فاصرف التعريف من المصدر عوضًا عن ذلك.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **ملاحظة:** إذا لم يُحمَّل رابط Gitee، ابحث في Gitee عن `mt76` واختر أحدث نسخة مُحدَّثة. يمكنك أيضًا تنزيل حزم التعريف مباشرةً من [files.alfa.com.tw](https://files.alfa.com.tw).

---

### الخطوة 3: تفعيل وضع المراقبة {#enable-monitor-mode}

قبل التبديل إلى وضع المراقبة، تحقق من اسم الواجهة الذي خصّصه النظام للمحوّل.

```bash
iwconfig
```

ابحث عن `wlan0` أو `wlan1`. استخدم ذلك الاسم في الأوامر أدناه.

أوقف NetworkManager و wpa_supplicant حتى لا يتداخلا مع العملية.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

أكّد التبديل.

```bash
iwconfig
```

ابحث عن إدخال مثل `wlan0mon` مع `Mode:Monitor`. حين ترى ذلك، يكون المحوّل جاهزًا لالتقاط الحزم.

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

إذا فشل الاختبار، أعد تشغيل الجهاز وكرّره. إذا استمر الفشل، تأكد أن لا عملية أخرى تستخدم الواجهة بتشغيل `iwconfig`.

---

## Ubuntu 22.04 / 24.04

تعريف MT7612U موجود في نواة Ubuntu أيضًا، لكنه قد يكون في حزمة `linux-modules-extra` بدلًا من صورة النواة الأساسية. تتعامل الخطوات التالية مع كلتا الحالتين.

### الخطوة 1: التحويل إلى مرايا الصين

#### Ubuntu 24.04 (Noble)

افتح ملف المصادر بصيغة DEB822:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

احذف كل شيء وألصق:

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

استبدل كل الأسطر بما يلي:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

احفظ واخرج (`Ctrl+O`، ثم `Ctrl+X`).

#### تحديث فهرس الحزم

```bash
sudo apt update
```

---

### الخطوة 2: تحميل التعريف

حاول تحميل الوحدة مباشرةً أولًا.

```bash
sudo modprobe mt76x2u
```

إذا أعطى خطأ "Module not found"، ثبّت حزمة الوحدات الإضافية.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

تحقق من ظهور المحوّل.

```bash
iwconfig
```

ظهور واجهة مثل `wlan0` أو `wlan1` في المخرجات يؤكد أن التعريف نشط.

---

### الخطوة 3: تثبيت أدوات الشبكة اللاسلكية

ثبّت aircrack-ng لوضع المراقبة واختبار الحقن.

```bash
sudo apt install -y aircrack-ng
```

---

### الخطوة 4: تفعيل وضع المراقبة

أنهِ العمليات المتداخلة، ثم شغّل وضع المراقبة.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **ملاحظة:** قد تكون واجهتك `wlan1` إذا كان ثمة بطاقة لاسلكية أخرى. شغّل `iwconfig` أولًا للتحقق.

---

### الخطوة 5: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan0mon
```

نتيجة ناجحة تُظهر `Injection is working!`. إذا ظهرت أخطاء في الواجهة، تحقق من تفعيل وضع المراقبة بـ `iwconfig wlan0mon`.

---

## Debian

تعريف MT7612U موجود في نواة Debian، لكنه قد يحتاج إلى حزمة `firmware-misc-nonfree` للتهيئة الكاملة.

### الخطوة 1: التحويل إلى مرايا الصين

افتح قائمة المصادر:

```bash
sudo nano /etc/apt/sources.list
```

احذف كل شيء وألصق هذه الأسطر الثلاثة (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

احفظ بـ `Ctrl+O`، ثم اخرج بـ `Ctrl+X`. حدّث:

```bash
sudo apt update
```

### الخطوة 2: تثبيت البرامج الثابتة غير الحرة

يحتاج MT7612U إلى ملفات البرامج الثابتة من حزمة `firmware-misc-nonfree`. بدونها، يُهيَّأ المحوّل لكنه قد لا يرتبط بالشبكة أو لا يتبدّل إلى وضع المراقبة.

```bash
sudo apt install -y firmware-misc-nonfree
```

### الخطوة 3: تحميل التعريف

```bash
sudo modprobe mt76x2u
```

إذا كانت الوحدة مفقودة، ثبّت وحدات النواة الإضافية أولًا.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

أكّد ظهور الواجهة.

```bash
iwconfig
```

### الخطوة 4: تفعيل وضع المراقبة

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

أكّد وضع المراقبة بـ `iwconfig` — ابحث عن `wlan0mon` مع `Mode:Monitor`.

### الخطوة 5: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` يؤكد أن المحوّل يعمل بصورة كاملة.

---

## Raspberry Pi 4B / 5

> يستهلك AWUS036ACM نحو 400mW تحت الحمل. استخدم موزّع USB بمصدر طاقة مستقل لمنع Pi من تقليص الأداء.

---

### الخطوة 1: تنزيل صورة Kali Linux ARM64

انتقل إلى صفحة تنزيلات Kali ARM الرسمية:
https://www.kali.org/get-kali/#kali-arm

اختر **Raspberry Pi 4 (64-bit)** أو **Raspberry Pi 5 (64-bit)**. لا تستخدم الصورة 32-bit — يُشترط 64-bit.

> **مرايا الصين:** إذا كان kali.org بطيئًا، استخدم 华为云:
> https://repo.huaweicloud.com/kali-images/
> تصفّح إلى مجلد الإصدار الأحدث ونزّل صورة ARM64 من هناك.

---

### الخطوة 2: نسخ الصورة على MicroSD

تحقق أولًا من مسار الجهاز الخاص ببطاقتك.

```bash
lsblk
```

ثم انسخ الصورة، مستبدلًا `/dev/sdX` بمسار البطاقة الفعلي.

```bash
# Replace /dev/sdX with your actual SD card (check with lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

انتظر حتى تنتهي `sync`، ثم أقلع. بيانات الاعتماد الافتراضية: **kali / kali**.

---

### الخطوة 3: التحويل إلى مرايا الصين

```bash
sudo nano /etc/apt/sources.list
```

استبدل المحتوى بما يلي:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ وطبّق.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### الخطوة 4: التحقق من التعريف

بعد إعادة التشغيل، وصّل المحوّل وتحقق.

```bash
lsmod | grep mt76
```

إذا ظهر `mt76x2u`، انتهيت. وإن لم يظهر:

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### الخطوة 5: تفعيل وضع المراقبة

على Pi مزوّد بـ Wi-Fi مدمج، يظهر AWUS036ACM باسم `wlan1` — إذ يشغل الراديو المدمج `wlan0`.

```bash
iwconfig
```

دوّن اسم الواجهة، ثم شغّل وضع المراقبة عليها.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

أكّد بـ `iwconfig` — ابحث عن `wlan1mon` مع `Mode:Monitor`.

---

### الخطوة 6: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` يؤكد التشغيل الكامل. إذا فشل الاختبار، تأكد من استخدام موزّع USB بمصدر طاقة مستقل.

---

## تمرير USB إلى الآلة الافتراضية {#virtual-machine-usb-passthrough}

### VirtualBox

1. أوقف تشغيل الآلة الافتراضية. انتقل إلى **Settings → USB**.
2. فعّل **USB 3.0 (xHCI) Controller**.
3. انقر **+** لإضافة مرشّح USB.
4. اختر: **MediaTek Inc. MT7612U** (ID: 0e8d:7612).
5. شغّل الآلة الافتراضية — يظهر المحوّل داخل Kali.

شغّل `lsusb` في الآلة الافتراضية للتأكد من `0e8d:7612`، ثم اتبع خطوات Kali أعلاه.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. شغّل الآلة الافتراضية.
2. من القائمة: **Virtual Machine → USB & Bluetooth**.
3. ابحث عن **MediaTek MT7612U** وانقر **Connect**.
4. شغّل `lsusb` في الآلة الافتراضية للتأكيد، ثم اتبع خطوات Kali أعلاه.

---

## الواجهة الافتراضية (VIF) {#virtual-interface-vif}

هنا يتفوق AWUS036ACM على ACH. تتمتع شريحة MT7612U بدعم كامل للواجهة الافتراضية (VIF) على مستوى النواة. يمكنك تشغيل واجهة مراقبة وواجهة مُدارة أو نقطة وصول على المحوّل ذاته في آنٍ واحد — دون تصحيحات أو حيل.

### إنشاء واجهة افتراضية ثانية

مع المحوّل في وضع إدارة باسم `wlan0`، أضف واجهة مراقبة بجانبه.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

الآن تحقق من أن كلتا الواجهتين نشطتان.

```bash
iwconfig
```

يجب أن ترى `wlan0` (مرتبطة، وضع إدارة) و`mon0` (وضع مراقبة). يؤدي المحوّل كلتا المهمتين في وقت واحد.

### حالة استخدام: المراقبة مع الاتصال

يتيح لك هذا التقاط حركة البيانات على `mon0` بينما تظل `wlan0` متصلة بشبكة — مفيد للتحليل المترابط.

```bash
sudo airodump-ng mon0
```

تستمر `wlan0` في ارتباطها الطبيعي بينما تلتقط `mon0` كل شيء في النطاق.

### حالة استخدام: نقطة وصول مزيّفة + مراقبة

أنشئ واجهة نقطة وصول وواجهة مراقبة معًا.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

شغّل `iwconfig` للتأكد من أن الثلاث واجهات (`wlan0` و`ap0` و`mon0`) نشطة.

> **ملاحظة بشأن hostapd:** يتطلب تشغيل نقطة الوصول الكاملة تهيئة `hostapd`، وهو خارج نطاق هذا الدليل. الخطوات أعلاه تؤكد قدرة المحوّل على إنشاء الواجهة — أما تهيئة نقطة الوصول الفعلية فموضوع منفصل.

---

## استكشاف الأخطاء وإصلاحها

| المشكلة | السبب المحتمل | الحل |
|---------|--------------|-------|
| `lsusb` لا يُظهر 0e8d:7612 | المحوّل غير مُزوَّد بالطاقة أو الكابل معطوب | جرّب منفذ USB آخر. استخدم موزّع USB بمصدر طاقة مع Raspberry Pi. |
| `modprobe mt76x2u` يقول "Module not found" | وحدات النواة الإضافية مفقودة | شغّل `sudo apt install linux-modules-extra-$(uname -r)` |
| الواجهة تظهر لكنها لا ترتبط | ملف البرامج الثابتة مفقود | شغّل `sudo apt install firmware-misc-nonfree` (Debian) |
| `airmon-ng start wlan0` يفشل | NetworkManager لا يزال يعمل | شغّل `sudo airmon-ng check kill` أولًا |
| وضع المراقبة يبدأ لكن لا تُلتقط أي حزم | القناة خاطئة أو اسم الواجهة خاطئ | اضبط القناة: `iwconfig wlan0mon channel 6` |
| اختبار الحقن يقول "No Answer" | نقطة الوصول بعيدة جدًا أو الواجهة خاطئة | اقترب من نقطة الوصول. استخدم `wlan0mon` لا `wlan0`. |
| إنشاء واجهة VIF يفشل | التعريف لم يُحمَّل بالكامل | افصل المحوّل وأعد تحميل الوحدة: `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## مرجع مرايا الصين

جميع الموارد المستخدمة في هذا الدليل — لا حاجة لـ GitHub:

| المورد | الرابط | الاستخدام |
|--------|--------|-----------|
| تعريفات Alfa الرسمية | [files.alfa.com.tw](https://files.alfa.com.tw) | حزم التعريف والبرامج الثابتة |
| توثيق Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (موصى به) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (موصى به) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | صور Kali ARM (احتياطي) |
| تعريف MT76 (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | التصريف اليدوي الاحتياطي |

## المزيد من أدلة محوّلات Alfa للصين

هذا المقال جزء من سلسلة **Alfa China Install Guide**. يتناول كل مقال طرازًا واحدًا:

- [دليل تثبيت AWUS036ACH للصين](/ar/blog/awus036ach-china-install-guide/) — RTL8812AU، طاقة عالية
- AWUS036ACM ← أنت هنا
- [دليل تثبيت AWUS036ACS للصين](/ar/blog/awus036acs-china-install-guide/)
- [دليل تثبيت AWUS036AX للصين](/ar/blog/awus036ax-china-install-guide/)
- [دليل تثبيت AWUS036AXER للصين](/ar/blog/awus036axer-china-install-guide/)
- [دليل تثبيت AWUS036AXM للصين](/ar/blog/awus036axm-china-install-guide/)
- [دليل تثبيت AWUS036AXML للصين](/ar/blog/awus036axml-china-install-guide/)
- [دليل تثبيت AWUS036EAC للصين](/ar/blog/awus036eacs-china-install-guide/)

هل لديك استفسار؟ اترك تعليقًا أدناه أو تواصل معنا عبر [yupitek.com](https://yupitek.com/ar/contact/).
