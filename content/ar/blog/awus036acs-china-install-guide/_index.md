---
title: "دليل تثبيت برنامج تشغيل ALFA AWUS036ACS للصين: Kali Linux، Ubuntu، Debian و Raspberry Pi"
description: "دليل خطوة بخطوة لتثبيت برامج تشغيل ALFA AWUS036ACS في الصين باستخدام المرايا المحلية. برنامج تشغيل RTL8811AU DKMS، وضع المراقبة الكامل وحقن الحزم. يغطي Kali Linux و Ubuntu 22/24 و Debian و Raspberry Pi. لا يتطلب GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 3
related_product: "/ar/products/alfa/awus036acs/"
featureimage: "/images/blog/awus036acs-china-install-guide.webp"
---

يعتبر AWUS036ACS محول أبحاث أمان مدمج ثنائي النطاق من ALFA. تدعم شريحة RTL8811AU الخاصة به وضع المراقبة الكامل وحقن الحزم على Kali Linux — ولكن نظرًا لأن برنامج التشغيل خارج النواة، فأنت بحاجة إلى تجميعه من المصدر. في الصين، يتم حظر GitHub، لذا يستخدم هذا الدليل مرايا Gitee حصريًا. لا داعي للقلق، GitHub ليس مطلوبًا على الإطلاق.

## قبل أن تبدأ

تأكد من توفر المتطلبات التالية لديك:

1. محول **ALFA AWUS036ACS**
2. كبل USB (USB-A 2.0، الكبل الموجود في العلبة يعمل بشكل جيد)
3. اتصال إنترنت نشط للوصول إلى المرايا المحلية

قم بتوصيل المحول، ثم تأكد من أن نظامك يتعرف عليه:

```bash
lsusb
```

ابحث عن هذا في الإخراج:

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

إذا رأيت `0bda:0811`، فهذا يعني أنه تم اكتشاف المحول. انتقل إلى قسم نظام التشغيل الخاص بك أدناه.

## اختر نظام التشغيل الخاص بك

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

هل قمت بالتثبيت بالفعل؟ انتقل إلى:

- [تمكين وضع المراقبة](#enable-monitor-mode)
- [اختبار حقن الحزم](#test-packet-injection)
- [تمرير USB للمحاكاة الافتراضية](#virtual-machine-usb-passthrough)

---

## Kali Linux

### الخطوة 1: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list
```

احذف كل ما هو موجود هناك، ثم الصق:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ بالضغط على **Ctrl+O**، ثم Enter، ثم Ctrl+X. قم بتحديث المستودعات:

```bash
sudo apt update
```

> **المرآة الاحتياطية:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### الخطوة 2: تثبيت تبعيات البناء

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### الخطوة 3: استنساخ برنامج التشغيل من Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **ملاحظة:** إذا لم يتم تحميل عنوان URL الخاص بـ Gitee، فابحث في Gitee عن `8821au` واختر أحدث نسخة (fork). يمكنك أيضًا تنزيل أرشيفات برامج التشغيل من [files.alfa.com.tw](https://files.alfa.com.tw).

---

### الخطوة 4: التجميع والتثبيت

```bash
sudo ./install-driver.sh
sudo reboot
```

بعد إعادة التشغيل، تأكد من تحميل برنامج التشغيل.

```bash
lsmod | grep 88XXau
```

يجب أن ترى وحدة `88XXau` مدرجة. ثم تأكد من ظهور الواجهة.

```bash
iwconfig
```

ابحث عن `wlan0` أو `wlan1`.

---

### الخطوة 5: تمكين وضع المراقبة {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

تأكد باستخدام `iwconfig` — ابحث عن `wlan1mon` مع `Mode:Monitor`.

---

### الخطوة 6: اختبار حقن الحزم {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### الخطوة 1: التبديل إلى مرآة الصين

#### Ubuntu 24.04 (Noble)

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

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

استبدل جميع الأسطر بـ:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### الخطوة 2: تثبيت تبعيات البناء

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### الخطوة 3: استنساخ وتثبيت برنامج التشغيل من Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### الخطوة 4: تمكين وضع المراقبة

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### الخطوة 5: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### الخطوة 1: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list
```

الصق (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### الخطوة 2: تثبيت تبعيات البناء

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### الخطوة 3: الاستنساخ والتثبيت

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### الخطوة 4: تمكين وضع المراقبة

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

تأكد: `iwconfig` → ابحث عن `wlan1mon` مع `Mode:Monitor`.

### الخطوة 5: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### الخطوة 1: تنزيل وحرق Kali ARM64

الموقع الرسمي: https://www.kali.org/get-kali/#kali-arm — اختر Raspberry Pi 4/5 64-bit.

مرآة الصين: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

بيانات الاعتماد الافتراضية: **kali / kali**.

### الخطوة 2: التبديل إلى مرآة الصين

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### الخطوة 3: تثبيت تبعيات البناء

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### الخطوة 4: استنساخ وتثبيت برنامج التشغيل

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### الخطوة 5: تمكين وضع المراقبة

في Pi مع Wi-Fi مدمج، يظهر AWUS036ACS كـ `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### الخطوة 6: اختبار حقن الحزم

```bash
sudo aireplay-ng --test wlan1mon
```

---

## تمرير USB للمحاكاة الافتراضية {#virtual-machine-usb-passthrough}

### VirtualBox

1. قم بإيقاف تشغيل VM → **Settings → USB** → قم بتمكين **USB 2.0 Controller**.
2. انقر فوق **+** ← اختر: **Realtek** (ID: 0bda:0811).
3. ابدأ تشغيل VM. قم بتشغيل `lsusb` للتأكد من وجود `0bda:0811` ، ثم اتبع خطوات Kali أعلاه.

### VMware Fusion / Workstation

1. **Virtual Machine → USB & Bluetooth** → ابحث عن **Realtek 8811AU** → **Connect**.
2. قم بتشغيل `lsusb` للتأكد، ثم اتبع خطوات Kali أعلاه.

---

## استكشاف الأخطاء وإصلاحها

| المشكلة | السبب المرجح | الحل |
|---------|-------------|-----|
| `lsusb` لا يظهر 0bda:0811 | المحول غير متصل أو الكبل تالف | جرب منفذ USB مختلفًا |
| فشل `install-driver.sh` | فقدان الرؤوس (headers) | قم بتشغيل `sudo apt install linux-headers-$(uname -r)` |
| فشل استنساخ Gitee | مشكلة في الشبكة | ابحث في gitee.com عن `8821au` وجرب نسخة مختلفة |
| فشل `airmon-ng start` | NetworkManager قيد التشغيل | قم بتشغيل `sudo airmon-ng check kill` أولاً |
| لا توجد حركة مرور في وضع المراقبة | قناة خاطئة | اضبط القناة: `iwconfig wlan1mon channel 6` |
| اختبار الحقن "No Answer" | نقطة الوصول بعيدة جدًا | اقترب أكثر. استخدم `wlan1mon` وليس `wlan1`. |

> **ملاحظة حول VIF:** برنامج تشغيل RTL8811AU لا يدعم الواجهات الافتراضية (VIF). وضع المراقبة والوضع المدار (managed) في نفس الوقت غير متاحين لهذا المحول.

## مرجع مرايا الصين

| المورد | عنوان URL | الاستخدام |
|----------|-----|---------|
| برامج تشغيل Alfa الرسمية | [files.alfa.com.tw](https://files.alfa.com.tw) | حزم برامج التشغيل |
| وثائق Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات |
| برنامج تشغيل 8821au (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | برنامج تشغيل RTL8811AU |
| جامعة تسينغ-هوا | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| مرآة علي بابا | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (موصى به) |
| جامعة العلوم والتكنولوجيا في الصين | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (موصى به) |
| مرآة هواوي | [repo.huaweicloud.com](https://repo.huaweicloud.com) | صور Kali ARM |

## المزيد من أدلة محولات Alfa للصين

- [دليل تثبيت AWUS036ACH في الصين](/ar/blog/awus036ach-china-install-guide/) — RTL8812AU، طاقة عالية
- [دليل تثبيت AWUS036ACM في الصين](/ar/blog/awus036acm-china-install-guide/) — MT7612U، دعم VIF كامل
- AWUS036ACS ← أنت هنا
- [دليل تثبيت AWUS036AX في الصين](/ar/blog/awus036ax-china-install-guide/) — RTL8832BU، WiFi 6
- [دليل تثبيت AWUS036AXER في الصين](/ar/blog/awus036axer-china-install-guide/) — RTL8832BU، نانو
- [دليل تثبيت AWUS036AXM في الصين](/ar/blog/awus036axm-china-install-guide/) — MT7921AUN، شكل L
- [دليل تثبيت AWUS036AXML في الصين](/ar/blog/awus036axml-china-install-guide/) — MT7921AUN، WiFi 6E
- [دليل تثبيت AWUS036EACS في الصين](/ar/blog/awus036eacs-china-install-guide/) — RTL8821CU، ويندوز

هل لديك أسئلة؟ اترك تعليقًا أدناه أو اتصل بنا على [yupitek.com](https://yupitek.com/ar/contact/).
