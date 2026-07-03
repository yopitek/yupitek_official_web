---
title: "دليل تثبيت برنامج تشغيل ALFA AWUS036AXM للصين: Kali Linux، Ubuntu، Debian و Raspberry Pi"
description: "دليل خطوة بخطوة لتثبيت برامج تشغيل ALFA AWUS036AXM في الصين باستخدام المرايا المحلية. برنامج تشغيل MT7921AUN WiFi 6E المدمج في النواة، دعم كامل لوضع المراقبة و VIF. يغطي Kali Linux و Ubuntu 22/24 و Debian و Raspberry Pi. لا يتطلب GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 6
related_product: "/ar/products/alfa/awus036axm/"
featureimage: "/images/blog/awus036axm-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ما الشريحة التي يستخدمها AWUS036AXM؟ هل يدعم WiFi 6E؟"
    answer: "يستخدم شريحة MediaTek MT7921AUN ويدعم WiFi 6E ثلاثي النطاق (2.4G/5G/6G Hz)."
  - question: "هل يحتاج AWUS036AXM إلى تثبيت تعريف يدوي؟"
    answer: "لا، تعريف mt7921u مدمج في النواة منذ 5.18، يلزم فقط تثبيت حزمة البرنامج الثابت."
  - question: "هل يدعم AWUS036AXM الواجهات الافتراضية VIF؟"
    answer: "نعم، MT7921AUN يدعم بالكامل VIF الأصلي في النواة، يمكن الاتصال والمراقبة في آن واحد."
  - question: "لماذا يفشل تحميل التعريف على Ubuntu 22.04 مع AWUS036AXM؟"
    answer: "نواة Ubuntu 22.04 الافتراضية 5.15 قديمة جداً، يلزم تثبيت نواة HWE للترقية إلى 5.18 فأحدث."
  - question: "ما هو USB ID لـ AWUS036AXM؟"
    answer: "USB ID لـ MediaTek MT7921AUN هو 0e8d:7961، يمكن التأكد بـ lsusb."
---
يعتبر AWUS036AXM محول WiFi 6E ثلاثي النطاق من ALFA مع موصل USB-A موفر للمساحة على شكل حرف L. تستخدم شريحة MT7921AUN الخاصة به برنامج تشغيل `mt7921u` المدمج في نواة Linux منذ الإصدار 5.18. يحافظ الموصل على شكل حرف L على منافذ USB المجاورة خالية في أجهزة الكمبيوتر المحمولة. يغطي هذا الدليل الإعداد الكامل — البرامج الثابتة، التحقق من برنامج التشغيل، وضع المراقبة، حقن الحزم، و VIF — دون لمس GitHub.

{{< tldr >}}
يستخدم AWUS036AXM شريحة MT7921AUN ويدعم WiFi 6E، تعريفه مدمج في النواة. بعد تثبيت حزمة البرنامج الثابت يمكن استخدام وضع المراقبة وحقن الحزم و VIF.
{{< /tldr >}}

تأكد من توفر المتطلبات التالية لديك:



## قبل أن تبدأ

تأكد من توفر المتطلبات التالية لديك:

1. محول **ALFA AWUS036AXM**
2. موزع USB يعمل بالطاقة — مطلوب إذا كنت تستخدم Raspberry Pi
3. اتصال إنترنت نشط للوصول إلى المرايا المحلية

قم بتوصيل المحول، ثم تأكد من أن نظامك يتعرف عليه:

```bash
lsusb
```

ابحث عن هذا في الإخراج:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

إذا رأيت `0e8d:7961`، فهذا يعني أنه تم اكتشاف المحول. انتقل إلى قسم نظام التشغيل الخاص بك أدناه.

إذا لم تره، جرب منفذ USB-A مختلفًا، ثم قم بتشغيل `lsusb` مرة أخرى.

## اختر نظام التشغيل الخاص بك

انتقل إلى القسم الصحيح لنظام التشغيل الخاص بك:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

هل قمت بالتثبيت بالفعل؟ انتقل إلى:

- [تمكين وضع المراقبة](#enable-monitor-mode)
- [اختبار حقن الحزم](#test-packet-injection)
- [الواجهة الافتراضية (VIF)](#virtual-interface-vif)
- [تمرير USB للمحاكاة الافتراضية](#virtual-machine-usb-passthrough)

---

## Kali Linux

برنامج تشغيل MT7921AUN موجود بالفعل في نواة Kali. كل ما تحتاجه هو حزمة البرامج الثابتة MediaTek، المتوفرة من المرايا المحلية.

### الخطوة 1: التبديل إلى مرآة الصين

افتح قائمة المصادر في الجهاز (terminal).

```bash
sudo nano /etc/apt/sources.list
```

احذف كل ما هو موجود هناك، ثم الصق هذا السطر:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ: اضغط على **Ctrl+O**، ثم Enter، ثم Ctrl+X للخروج. قم بتحديث فهرس الحزم.

```bash
sudo apt update
```

> **المرآة الاحتياطية:** إذا كانت USTC بطيئة، فاستخدم Tsinghua بدلاً منها:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### الخطوة 2: تثبيت البرامج الثابتة (Firmware)

تتطلب شريحة MT7921AUN ملفات برامج ثابتة من `firmware-misc-nonfree` و `linux-firmware`. بدونها، سيتم تحميل برنامج التشغيل ولكن سيفشل المحول في البدء.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### الخطوة 3: التحقق من برنامج التشغيل

بعد إعادة التشغيل، قم بتوصيل المحول وتحقق.

```bash
lsmod | grep mt7921
```

يجب أن ترى `mt7921u` في الإخراج. ثم تأكد من ظهور واجهة لاسلكية.

```bash
iwconfig
```

ابحث عن `wlan0` أو `wlan1`. إذا ظهرت، فهذا يعني أن برنامج التشغيل يعمل.

---

### الخطوة 4: تمكين وضع المراقبة {#enable-monitor-mode}

تحقق من اسم الواجهة أولاً.

```bash
iwconfig
```

استخدم الاسم الذي تراه (مثل `wlan1`). قم بإيقاف العمليات المتداخلة، ثم قم بالتبديل إلى وضع المراقبة.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

تأكد من التبديل.

```bash
iwconfig
```

ابحث عن `Mode:Monitor` على الواجهة.

---

### الخطوة 5: اختبار حقن الحزم {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

نتيجة ناجحة:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

إذا فشل، قم بإعادة التشغيل وحاول مرة أخرى.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — نواة 6.8، توصيل وتشغيل

يأتي Ubuntu 24.04 بنواة 6.8، والتي تتضمن برنامج تشغيل MT7921AUN بشكل أصلي.

### الخطوة 1: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

احذف كل شيء والصق:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

احفظ بـ `Ctrl+O` ، ثم اخرج بـ `Ctrl+X`.

```bash
sudo apt update
```

### الخطوة 2: تثبيت البرامج الثابتة

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### الخطوة 3: التحقق وتمكين وضع المراقبة

بعد إعادة التشغيل، قم بتشغيل `lsmod | grep mt7921` للتأكد من تحميل برنامج التشغيل، ثم اتبع خطوات وضع مراقبة Kali أعلاه (الخطوة 4).

---

### Ubuntu 22.04 (Jammy) — مطلوب نواة HWE

يأتي Ubuntu 22.04 بنواة 5.15. يتطلب برنامج تشغيل MT7921AUN نواة ≥ 5.18. قم بتثبيت نواة HWE أولاً.

### الخطوة 1: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list
```

استبدل جميع الأسطر بـ:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

احفظ واخرج (`Ctrl+O` ، ثم `Ctrl+X`).

```bash
sudo apt update
```

### الخطوة 2: تثبيت نواة HWE

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

بعد إعادة التشغيل، تأكد من إصدار النواة:

```bash
uname -r
```

يجب أن ترى 5.19 أو أعلى. ثم قم بتثبيت البرامج الثابتة وتمكين وضع المراقبة كما هو موضح أعلاه.

### الخطوة 3: تثبيت البرامج الثابتة

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### الخطوة 1: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list
```

احذف كل شيء والصق (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

احفظ بـ `Ctrl+O` ، ثم اخرج بـ `Ctrl+X`.

```bash
sudo apt update
```

### الخطوة 2: تثبيت البرامج الثابتة

يأتي Debian 12 Bookworm بنواة 6.1 — متوافق مع MT7921AUN.

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### الخطوة 3: التحقق وتمكين وضع المراقبة

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### الخطوة 4: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1
```

`Injection is working!` يؤكد أن المحول يعمل بالكامل.

---

## Raspberry Pi 4B / 5

> يستهلك AWUS036AXM ما يصل إلى 2.7 واط تحت الحمل. استخدم دائمًا موزع USB يعمل بالطاقة على Raspberry Pi.

### الخطوة 1: تنزيل صورة Kali Linux ARM64

الصفحة الرسمية: https://www.kali.org/get-kali/#kali-arm

اختر **Raspberry Pi 4 (64-bit)** أو **Raspberry Pi 5 (64-bit)** — 64 بت مطلوب.

> **مرآة الصين:** https://repo.huaweicloud.com/kali-images/ — انتقل إلى أحدث مجلد إصدار وقم بتنزيل صورة ARM64.

### الخطوة 2: الحرق على MicroSD

```bash
lsblk
# استبدل /dev/sdX ببطاقة SD الفعلية الخاصة بك
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

بيانات الاعتماد الافتراضية: **kali / kali**.

### الخطوة 3: التبديل إلى مرآة الصين وتثبيت البرامج الثابتة

```bash
sudo nano /etc/apt/sources.list
```

استبدل بـ:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

ثم:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### الخطوة 4: التحقق من برنامج التشغيل

```bash
lsmod | grep mt7921
```

يجب أن يظهر `mt7921u`.

### الخطوة 5: تمكين وضع المراقبة

في Pi مع Wi-Fi مدمج، يظهر AWUS036AXM كـ `wlan1`.

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### الخطوة 6: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1
```

---

## تمرير USB للمحاكاة الافتراضية {#virtual-machine-usb-passthrough}

### VirtualBox

1. قم بإيقاف تشغيل VM. اذهب إلى **Settings → USB**.
2. تمكين **USB 3.0 (xHCI) Controller**.
3. انقر فوق **+** لإضافة فلتر USB.
4. اختر: **MediaTek Inc.** (ID: 0e8d:7961).
5. ابدأ تشغيل VM — يظهر المحول داخل Kali.

قم بتشغيل `lsusb` في VM للتأكد من وجود `0e8d:7961` ، ثم اتبع خطوات Kali أعلاه.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. ابدأ تشغيل VM.
2. القائمة: **Virtual Machine → USB & Bluetooth**.
3. ابحث عن **MediaTek MT7921AUN** وانقر فوق **Connect**.
4. قم بتشغيل `lsusb` في VM للتأكد، ثم اتبع خطوات Kali أعلاه.

---

## الواجهة الافتراضية (VIF) {#virtual-interface-vif}

يتمتع MT7921AUN بدعم VIF كامل في النواة بشكل أصلي. يمكنك تشغيل واجهة مراقبة وواجهة مدارة على نفس المحول في وقت واحد — لا حاجة لرقع (patches).

### إنشاء واجهة مراقبة بجانب الوضع المدار

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

يجب أن ترى كل من `wlan0` (مدارة) و `mon0` (مراقبة) نشطين في نفس الوقت.

### المراقبة أثناء البقاء متصلاً

```bash
sudo airodump-ng mon0
```

تبقى `wlan0` متصلة بينما تلتقط `mon0` كل شيء في النطاق.

### Fake AP + المراقبة

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> **ملاحظة حول hostapd:** يتطلب تشغيل AP الكامل تهيئة `hostapd`. الخطوات المذكورة أعلاه تؤكد أن المحول يمكنه إنشاء الواجهة — تهيئة AP الفعلية موضوع منفصل.

---

## استكشاف الأخطاء وإصلاحها

| المشكلة | السبب المرجح | الحل |
|---------|-------------|-----|
| `lsusb` لا يظهر 0e8d:7961 | المحول غير متصل أو الكبل تالف | جرب منفذ USB-A مختلفًا. استخدم موزعًا يعمل بالطاقة على Raspberry Pi. |
| `lsmod` لا يظهر mt7921u | البرامج الثابتة غير مثبتة أو النواة قديمة | قم بتشغيل `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` |
| Ubuntu 22.04 لا يقوم بتحميل برنامج التشغيل | نواة 5.15 قديمة جدًا | تثبيت HWE: `sudo apt install linux-generic-hwe-22.04` |
| تظهر الواجهة ولكن لا تتصل | فقدان ملفات البرامج الثابتة | قم بتشغيل `sudo apt install firmware-misc-nonfree` ثم أعد التشغيل |
| فشل التبديل لوضع المراقبة | الواجهة لا تزال تعمل (UP) | قم بتشغيل `sudo ip link set wlan1 down` قبل أمر `iw dev` |
| اختبار الحقن يقول "No Answer" | نقطة الوصول بعيدة جدًا أو واجهة خاطئة | اقترب أكثر. تأكد من `Mode:Monitor` باستخدام `iwconfig`. |
| فشل إنشاء واجهة VIF | لم يتم تحميل برنامج التشغيل بالكامل | افصله، ثم: `sudo rmmod mt7921u && sudo modprobe mt7921u` |

## مرجع مرايا الصين

| المورد | عنوان URL | الاستخدام |
|----------|-----|---------|
| برامج تشغيل Alfa الرسمية | [files.alfa.com.tw](https://files.alfa.com.tw) | حزم برامج التشغيل، البرامج الثابتة |
| وثائق Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات |
| جامعة تسينغ-هوا | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| مرآة علي بابا | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (موصى به) |
| جامعة العلوم والتكنولوجيا في الصين | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (موصى به) |
| مرآة هواوي | [repo.huaweicloud.com](https://repo.huaweicloud.com) | صور Kali ARM (احتياطي) |

{{< faq >}}

## المزيد من أدلة محولات Alfa للصين

هذا جزء من سلسلة **دليل تثبيت Alfa في الصين**:

- [دليل تثبيت AWUS036ACH في الصين](/ar/blog/awus036ach-china-install-guide/) — RTL8812AU، طاقة عالية
- [دليل تثبيت AWUS036ACM في الصين](/ar/blog/awus036acm-china-install-guide/) — MT7612U، دعم VIF كامل
- [دليل تثبيت AWUS036ACS في الصين](/ar/blog/awus036acs-china-install-guide/) — RTL8811AU، وضع المراقبة
- [دليل تثبيت AWUS036AX في الصين](/ar/blog/awus036ax-china-install-guide/) — RTL8832BU، WiFi 6
- [دليل تثبيت AWUS036AXER في الصين](/ar/blog/awus036axer-china-install-guide/) — RTL8832BU، نانو
- AWUS036AXM ← أنت هنا
- [دليل تثبيت AWUS036AXML في الصين](/ar/blog/awus036axml-china-install-guide/) — MT7921AUN، WiFi 6E
- [دليل تثبيت AWUS036EACS في الصين](/ar/blog/awus036eacs-china-install-guide/) — RTL8821CU، ويندوز

هل لديك أسئلة؟ اترك تعليقًا أدناه أو اتصل بنا على [yupitek.com](https://yupitek.com/ar/contact/).

## المراجع

1. [تعريف Linux Kernel mt7921](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [وثائق aircrack-ng الرسمية](https://www.aircrack-ng.org/)
3. [موقع ALFA Network الرسمي](https://www.alfa.com.tw/)
4. [وثائق Kali Linux الرسمية](https://www.kali.org/docs/)

