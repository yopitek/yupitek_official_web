---
title: "دليل تثبيت برنامج تشغيل ALFA AWUS036AX للصين: Kali Linux، Ubuntu، Debian و Raspberry Pi"
description: "دليل خطوة بخطوة لتثبيت برامج تشغيل ALFA AWUS036AX في الصين باستخدام المرايا المحلية. برنامج تشغيل RTL8832BU، WiFi 6 AX1800. يغطي Kali Linux و Ubuntu 22/24 (DKMS) و Debian و Raspberry Pi. لا يتطلب GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 4
related_product: "/ar/products/alfa/awus036ax/"
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ما الشريحة التي يستخدمها AWUS036AX؟ هل يدعم WiFi 6؟"
    answer: "يستخدم شريحة Realtek RTL8832BU ويدعم WiFi 6 (802.11ax) عالي السرعة."
  - question: "هل يحتاج AWUS036AX إلى تثبيت تعريف على Ubuntu 24.04؟"
    answer: "نعم. شريحة RTL8832BU غير موجودة في نواة Ubuntu 24.04. قم ببناء برنامج التشغيل المجتمعي rtl8852bu (morrownr/rtl8852bu-20250826) مرة واحدة عبر DKMS؛ ثم تُعاد بناؤه تلقائياً عند تحديث النواة."
  - question: "هل AWUS036AX مناسب لأبحاث الأمن اللاسلكي؟"
    answer: "لا. برنامج التشغيل المجتمعي rtl8852bu لا يدعم وضع المراقبة ولا حقن الحزم. استخدم بدلاً منه محولاً ببرنامج تشغيل MediaTek مدمج في النواة مثل AWUS036ACM."
  - question: "هل أحتاج إلى VPN لتثبيت AWUS036AX في الصين؟"
    answer: "لا، نزّل كود rtl8852bu من Gitee واستخدم المرايا المحلية لتثبيت أدوات التجميع."
  - question: "ما هو USB ID لـ AWUS036AX؟"
    answer: "USB ID لـ Realtek RTL8832BU هو 0bda:8832، يمكن التأكد بـ lsusb."
---
يعتبر AWUS036AX محول WiFi 6 AX1800 ثنائي النطاق من ALFA. شريحة RTL8832BU في AWUS036AX ليس لها برنامج تشغيل مدمج في نواة Linux، لذا يجب في كل توزيعة (بما فيها Ubuntu 24.04) بناء برنامج التشغيل المجتمعي rtl8852bu مرة واحدة عبر DKMS. يستخدم هذا الدليل مرايا Gitee فلا حاجة إلى الوصول إلى GitHub. وضع المراقبة غير مدعوم في برنامج التشغيل هذا.

{{< tldr >}}
يستخدم AWUS036AX شريحة RTL8832BU ويدعم WiFi 6. برنامج التشغيل غير موجود في النواة: كل توزيعة (بما فيها Ubuntu 24.04) تحتاج إلى بناء rtl8852bu عبر DKMS. وضع المراقبة غير مدعوم.
{{< /tldr >}}


> **ملاحظة حول أبحاث الأمان:** برنامج التشغيل المجتمعي rtl8852bu لا يدعم وضع المراقبة ولا حقن الحزم. لأبحاث الأمان استخدم محولاً ببرنامج تشغيل MediaTek مدمج في النواة مثل [AWUS036ACM](/ar/blog/awus036acm-china-install-guide/).

## قبل أن تبدأ

1. محول **ALFA AWUS036AX**
2. كبل USB-A
3. اتصال إنترنت نشط

```bash
lsusb
```

ابحث عن:

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## اختر نظام التشغيل الخاص بك

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### الخطوة 1: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### الخطوة 2: تثبيت تبعيات البناء

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### الخطوة 3: استنساخ برنامج التشغيل من Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **ملاحظة:** إذا لم يتم تحميل عنوان URL الخاص بـ Gitee، فابحث في Gitee عن `rtl8852bu` واختر أحدث نسخة. يمكنك أيضًا تنزيل الأرشيفات من [files.alfa.com.tw](https://files.alfa.com.tw).

### الخطوة 4: التجميع والتثبيت

```bash
sudo ./install-driver.sh
sudo reboot
```

تأكد من تحميل برنامج التشغيل:

```bash
lsmod | grep 8852bu
iwconfig
```

### الخطوة 5: تمكين وضع المراقبة {#enable-monitor-mode}

> **غير مدعوم:** برنامج التشغيل المجتمعي rtl8852bu لشريحة RTL8832BU لا يدعم وضع المراقبة، لذلك لا توجد أوامر لتنفيذها هنا. إذا كنت تحتاج إلى وضع المراقبة فاستخدم محولاً ببرنامج تشغيل MediaTek مدمج في النواة مثل [AWUS036ACM](/ar/blog/awus036acm-china-install-guide/).

### الخطوة 6: اختبار حقن الحزم {#test-packet-injection}

> **غير مدعوم:** يعتمد حقن الحزم على وضع المراقبة الذي لا يوفره برنامج التشغيل هذا. استخدم [AWUS036ACM](/ar/blog/awus036acm-china-install-guide/) لاختبارات الحقن.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — يتطلب DKMS

لا يتضمن Ubuntu 24.04 (النواة 6.8) برنامج تشغيل لشريحة RTL8832BU. انتقل إلى مرآة محلية ثم ابنِ برنامج التشغيل كما في Ubuntu 22.04 أدناه.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

بعد إعادة التشغيل نفّذ `sudo modprobe 8852bu` و `iwconfig`. إذا تم تحميل الوحدة وظهرت واجهة فقد انتهيت (وضع الإدارة فقط؛ وضع المراقبة غير مدعوم).

---

### Ubuntu 22.04 (Jammy) — مطلوب DKMS

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

وضع المراقبة غير مدعوم في برنامج التشغيل هذا (راجع الخطوة 5 في Kali).

---

## Raspberry Pi 4B / 5

قم بالتبديل إلى مرآة الصين أولاً:

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## تمرير USB للمحاكاة الافتراضية {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Settings → USB** → قم بتمكين **USB 3.0 (xHCI) Controller**.
2. أضف فلتر: **Realtek** (ID: 0bda:885a).
3. ابدأ VM → `lsusb` للتأكد → اتبع خطوات Kali.

### VMware

1. **Virtual Machine → USB & Bluetooth** → ابحث عن **Realtek RTL8832BU** → **Connect**.
2. `lsusb` للتأكد → اتبع خطوات Kali.

---

## استكشاف الأخطاء وإصلاحها

| المشكلة | السبب المرجح | الحل |
|---------|-------------|-----|
| `lsusb` لا يظهر 0bda:885a | لم يتم اكتشاف المحول | جرب منفذ USB مختلفًا |
| فشل `install-driver.sh` | فقدان الرؤوس | `sudo apt install linux-headers-$(uname -r)` |
| فشل استنساخ Gitee | مشكلة في الشبكة | ابحث في gitee.com عن `rtl8852bu` |
| فشل `modprobe 8852bu` | لم يُبنَ برنامج التشغيل أو لم يُحمَّل | أعد تشغيل `sudo ./install-driver.sh` وتحقق من `sudo dkms status` ثم أعد التشغيل |
| وضع المراقبة / الحقن لا يعمل | غير مدعوم في برنامج التشغيل rtl8852bu | استخدم AWUS036ACM لأعمال الاختبار الأمني |

> **ملاحظة حول VIF:** برنامج تشغيل RTL8832BU خارج النواة لا يدعم الواجهات الافتراضية (VIF).

## مرجع مرايا الصين

| المورد | عنوان URL | الاستخدام |
|----------|-----|---------|
| برامج تشغيل Alfa الرسمية | [files.alfa.com.tw](https://files.alfa.com.tw) | حزم برامج التشغيل |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | برنامج تشغيل RTL8832BU |
| جامعة تسينغ-هوا | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| مرآة علي بابا | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| جامعة العلوم والتكنولوجيا في الصين | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| مرآة هواوي | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

{{< faq >}}

## المزيد من أدلة محولات Alfa للصين

- [دليل تثبيت AWUS036ACH في الصين](/ar/blog/awus036ach-china-install-guide/) — RTL8812AU، طاقة عالية
- [دليل تثبيت AWUS036ACM في الصين](/ar/blog/awus036acm-china-install-guide/) — MT7612U، دعم VIF كامل
- [دليل تثبيت AWUS036ACS في الصين](/ar/blog/awus036acs-china-install-guide/) — RTL8811AU، وضع المراقبة
- AWUS036AX ← أنت هنا
- [دليل تثبيت AWUS036AXER في الصين](/ar/blog/awus036axer-china-install-guide/) — RTL8832BU، نانو
- [دليل تثبيت AWUS036AXM في الصين](/ar/blog/awus036axm-china-install-guide/) — MT7921AUN، شكل L
- [دليل تثبيت AWUS036AXML في الصين](/ar/blog/awus036axml-china-install-guide/) — MT7921AUN، WiFi 6E
- [دليل تثبيت AWUS036EACS في الصين](/ar/blog/awus036eacs-china-install-guide/) — RTL8821CU، ويندوز

هل لديك أسئلة؟ اترك تعليقًا أدناه أو اتصل بنا على [yupitek.com](https://yupitek.com/ar/contact/).

## المراجع

1. [موقع Realtek الرسمي](https://www.realtek.com/)
2. [موقع ALFA Network الرسمي](https://www.alfa.com.tw/)
3. [وثائق Kali Linux الرسمية](https://www.kali.org/docs/)
4. [مرآة Gitee لـ rtl8852bu](https://gitee.com/mirrors/rtl8852bu)

