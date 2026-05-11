---
title: "الدليل الشامل: تثبيت جميع محوّلات Alfa USB WiFi على Linux في الصين - Kali وUbuntu وRaspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["أدلة التعريفات"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "الدليل الشامل لتثبيت جميع محوّلات Alfa USB WiFi على Linux في الصين. يغطي Kali Linux وUbuntu 22/24 وDebian وRaspberry Pi. لا حاجة إلى GitHub - استخدم المرايا المحلية فقط."
---

## مرحباً بك في الدليل الشامل لتثبيت Alfa على Linux

إذا كنت تقرأ هذا، فمن المرجح أنك اشتريت محوّل Alfa USB WiFi ووجدت نفسك عالقاً بسبب أحد هذه الأسباب:

- أنت في الصين ولا تستطيع الوصول إلى GitHub
- تبدو عملية تثبيت التعريف معقدة
- تحتاج إلى تفعيل وضع المراقبة (monitor mode) وحقن الحزم (packet injection) لاختبار الشبكات اللاسلكية
- لست متأكداً من التعريف المناسب لطراز Alfa الخاص بك

هذا الدليل يحلّ **جميع تلك المشكلات**. سنرشدك خطوة بخطوة لتثبيت **كل محوّلات Alfa USB WiFi** على **جميع توزيعات Linux الرئيسية**، باستخدام **مرايا متاحة من داخل الصين** فقط. بدون GitHub. بدون إحباط.

---

## لماذا وُجد هذا الدليل

تحظى محوّلات Alfa USB WiFi بشعبية واسعة بين مختبري الاختراق ومهندسي الشبكات وعشاق الشبكات اللاسلكية. فهي تدعم وضع المراقبة وحقن الحزم — وهي ميزات لا تتوفر في معظم محوّلات WiFi الاستهلاكية.

لكن هنا تكمن المشكلة: **تفترض معظم أدلة تثبيت التعريفات أنك تستطيع الوصول إلى GitHub**. إذا كنت في الصين، فهذا غير متاح. صُمّم هذا الدليل تحديداً للمستخدمين في الصين، باستخدام مرايا وموارد تعمل ضمن البنية التحتية لإنترنت الصين فقط.

---

## مرجع سريع للطرازات

قبل أن نبدأ، دعنا نحدد طراز محوّل Alfa الذي بحوزتك والشريحة التي يستخدمها:

### سلسلة AX (Wi-Fi 6 / 802.11ax)

| الطراز | الشريحة | التعريف | الاستخدام الأمثل |
|--------|---------|---------|-----------------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | الاستخدام العام، نطاق جيد |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | تصميم مدمج |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | فائق الإحكام |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | طاقة محسّنة |

### سلسلة AC (Wi-Fi 5 / 802.11ac)

| الطراز | الشريحة | التعريف | الاستخدام الأمثل |
|--------|---------|---------|-----------------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | طاقة عالية، نطاق ممتاز |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **أفضل دعم VIF**، تشغيل فوري |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | خيار اقتصادي |

### أيّ محوّل لديك؟

1. انظر إلى الملصق الموجود على المحوّل
2. تحقق من العلبة التي جاء فيها
3. إذا اشتريته عبر الإنترنت، راجع سجل طلباتك

بمجرد معرفة طرازك، انتقل إلى القسم المناسب أدناه أو اتبع سير العمل العام.

---

## قبل البدء: ما تحتاجه

تأكد من توفر هذه العناصر قبل البدء:

1. **محوّل Alfa USB WiFi** — الطراز المناسب لاحتياجاتك
2. **كابل USB** — الكابل المرفق في العلبة يؤدي الغرض
3. **هاب USB نشط (بمصدر طاقة خارجي)** — ضروري عند استخدام Raspberry Pi
4. **اتصال إنترنت نشط** — للوصول إلى المرايا المحلية في الصين
5. **صلاحيات Sudo** — ستحتاج إلى صلاحيات المشرف لتثبيت التعريفات

وصّل المحوّل أولاً للتحقق من أن نظامك يتعرف عليه:

```bash
lsusb
```

ابحث عن معرّف مورّد محوّلك في الناتج:

- **محوّلات Alfa** تظهر بالمعرّف `0e8d` (MediaTek) أو `0bda` (Realtek)
- مثال: `Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- مثال: `Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

إذا رأيت المعرّف، فالمحوّل مُكتشَف. انتقل إلى قسم تثبيت التعريف أدناه.

إذا لم تره، جرّب منفذ USB مختلفاً، واستبدل الكابل، ثم أعد تشغيل `lsusb`.

---

## اختر نظام التشغيل

انتقل إلى القسم المناسب لنظامك:

- [Kali Linux](#تثبيت-kali-linux)
- [Ubuntu 22.04 / 24.04](#تثبيت-ubuntu-2204--2404)
- [Debian 12 (Bookworm)](#تثبيت-debian-12-bookworm)
- [Raspberry Pi OS (64-bit)](#تثبيت-raspberry-pi-os)

هل ثبّتَ التعريف بالفعل؟ انتقل مباشرةً إلى الأقسام المتقدمة:

- [تفعيل وضع المراقبة](#تفعيل-وضع-المراقبة-على-أي-محوّل)
- [اختبار حقن الحزم](#اختبار-حقن-الحزم)
- [دعم الواجهة الافتراضية (VIF)](#دعم-الواجهة-الافتراضية-vif)
- [تمرير USB للأجهزة الافتراضية](#تمرير-usb-للأجهزة-الافتراضية)

---

## مرجع المرايا المتاحة في الصين

تستخدم جميع الموارد في هذا الدليل هذه المرايا المتاحة من الصين:

| المورد | الرابط | الاستخدام |
|--------|--------|-----------|
| **تنزيلات Alfa الرسمية** | [files.alfa.com.tw](https://files.alfa.com.tw) | حزم التعريفات والبرامج الثابتة |
| **توثيق Alfa** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات، بالإنجليزية |
| **مرآة جامعة تسينغهوا (清华大学)** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **مرآة علي بابا السحابية (阿里云)** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (موصى بها) |
| **مرآة USTC (中科大)** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (موصى بها) |
| **مرآة هواوي السحابية** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | صور Kali ARM (احتياطية) |
| **Gitee (بديل GitHub)** | [gitee.com](https://gitee.com) | شفرة مصدر التعريفات |

---

## تثبيت Kali Linux

يأتي Kali Linux مع أدوات الشبكات اللاسلكية مثبتة مسبقاً. لا يحتاج تشغيل محوّلات Alfa إلا بضع خطوات بسيطة.

### الخطوة 1: التبديل إلى مرآة صينية

افتح قائمة المصادر:

```bash
sudo nano /etc/apt/sources.list
```

استبدل كل المحتوى بما يلي:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ: **Ctrl+O**، ثم Enter، ثم **Ctrl+X**. حدّث قائمة الحزم:

```bash
sudo apt update
```

> **مرآة احتياطية:** إذا كانت مرآة 中科大 (USTC) بطيئة، استخدم 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### الخطوة 2: تثبيت التعريف حسب الشريحة

#### سلسلة AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### سلسلة AC - Realtek (RTL8812AU / RTL8811AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### سلسلة AC - MediaTek (MT7612U)

تعريف MT7612U مدمج في نواة Kali. تحقق من تحميله:

```bash
lsmod | grep mt76
```

إذا رأيت `mt76x2u`، فقد انتهيت. إذا لم تره:

```bash
sudo modprobe mt76x2u
```

### الخطوة 3: التحقق من تحميل التعريف

شغّل `lsusb` مرة أخرى. يجب أن يظهر محوّلك. ثم تحقق من الواجهات اللاسلكية:

```bash
iwconfig
```

ابحث عن `wlan0` أو `wlan1`. إذا ظهرت الواجهة، فالتعريف يعمل.

### الخطوة 4: تفعيل وضع المراقبة

أوقف العمليات المتعارضة:

```bash
sudo airmon-ng check kill
```

شغّل وضع المراقبة:

```bash
sudo airmon-ng start wlan0
```

تحقق من النتيجة:

```bash
iwconfig
```

ابحث عن `wlan0mon` مع `Mode:Monitor`. انتهيت!

---

## تثبيت Ubuntu 22.04 / 24.04

### الخطوة 1: التبديل إلى مرآة صينية

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

استبدل بما يلي:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

احفظ بـ **Ctrl+O**، واخرج بـ **Ctrl+X**.

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

استبدل بما يلي:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

احفظ واخرج.

#### تحديث فهرس الحزم

```bash
sudo apt update
```

### الخطوة 2: تثبيت متطلبات البناء

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### الخطوة 3: تثبيت التعريف

#### سلسلة AX (RTL8832BU)

استنسخ من Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### سلسلة AC - Realtek (RTL8812AU)

استنسخ من Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### سلسلة AC - MediaTek (MT7612U)

التعريف مدمج في نواة Ubuntu. قم بتحميله:

```bash
sudo modprobe mt76x2u
```

### الخطوة 4: تفعيل وضع المراقبة

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

ابحث عن `wlan0mon` مع `Mode:Monitor`.

---

## تثبيت Debian 12 (Bookworm)

### الخطوة 1: التبديل إلى مرآة صينية

```bash
sudo nano /etc/apt/sources.list
```

استبدل بما يلي:

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

احفظ واخرج. حدّث الفهرس:

```bash
sudo apt update
```

### الخطوة 2: تثبيت البرامج الثابتة غير المجانية

```bash
sudo apt install -y firmware-misc-nonfree
```

### الخطوة 3: تثبيت متطلبات البناء

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### الخطوة 4: تثبيت التعريف

#### سلسلة AX (RTL8832BU)

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### سلسلة AC - Realtek (RTL8812AU)

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### سلسلة AC - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### الخطوة 5: تثبيت Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### الخطوة 6: تفعيل وضع المراقبة

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

ابحث عن `wlan0mon` مع `Mode:Monitor`.

---

## تثبيت Raspberry Pi OS

> **تنبيه مهم:** يستهلك AWUS036ACH نحو 500mW، ويستهلك AWUS036ACM نحو 400mW. **استخدم دائماً هاباً USB بمصدر طاقة خارجي** لمنع تعثّر Pi أو انهياره تحت الحمل.

### الخطوة 1: تنزيل صورة Kali Linux ARM64

انتقل إلى: https://www.kali.org/get-kali/#kali-arm

اختر **Raspberry Pi 4 (64-bit)** أو **Raspberry Pi 5 (64-bit)**. لا تستخدم الإصدار 32-bit — يُشترط استخدام 64-bit.

> **مرآة صينية:** إذا كان kali.org بطيئاً، استخدم مرآة هواوي: https://repo.huaweicloud.com/kali-images/

### الخطوة 2: كتابة الصورة على بطاقة MicroSD

تحقق من مسار بطاقة SD:

```bash
lsblk
```

اكتب الصورة (استبدل `/dev/sdX` بمسار بطاقتك الفعلي):

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

انتظر حتى يكتمل `sync`. شغّل Pi. بيانات الدخول الافتراضية: **kali / kali**.

### الخطوة 3: التبديل إلى مرآة صينية

```bash
sudo nano /etc/apt/sources.list
```

استبدل بما يلي:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

احفظ وطبّق:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### الخطوة 4: تثبيت التعريف

#### سلسلة AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### سلسلة AC - Realtek (RTL8812AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### سلسلة AC - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### الخطوة 5: تفعيل وضع المراقبة

على Pi المزوّد بـ Wi-Fi مدمج، يظهر محوّل Alfa بالاسم `wlan1`:

```bash
iwconfig
```

ثم:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

ابحث عن `wlan1mon` مع `Mode:Monitor`.

---

## تفعيل وضع المراقبة على أي محوّل

بمجرد تثبيت التعريف، يصبح تفعيل وضع المراقبة سهلاً:

### الخطوة 1: تحقق من اسم الواجهة

```bash
iwconfig
```

لاحظ ما إذا كانت الواجهة `wlan0` أو `wlan1`.

### الخطوة 2: أوقف العمليات المتعارضة

```bash
sudo airmon-ng check kill
```

### الخطوة 3: شغّل وضع المراقبة

```bash
sudo airmon-ng start wlan0
```

استبدل `wlan0` باسم واجهتك الفعلي إذا كانت مختلفة.

### الخطوة 4: التحقق

```bash
iwconfig
```

ابحث عن واجهتك بلاحقة `mon` (مثل `wlan0mon`) مع `Mode:Monitor`.

---

## اختبار حقن الحزم

يُثبت هذا أن محوّلك قادر على إرسال حزم مخصصة — وهو أمر أساسي لاختبار الشبكات اللاسلكية.

```bash
sudo aireplay-ng --test wlan0mon
```

**نتيجة النجاح تبدو كالتالي:**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**إذا فشل الاختبار:**
- أعد تشغيل الجهاز وحاول مجدداً
- تأكد أن لا عملية أخرى تمسك الواجهة (`iwconfig`)
- اقترب من نقطة وصول WiFi لإجراء الاختبار
- تأكد من استخدام `wlan0mon` وليس `wlan0`

---

## دعم الواجهة الافتراضية (VIF)

تتيح الواجهة الافتراضية (VIF) تشغيل واجهات متعددة على محوّل واحد في آنٍ واحد. على سبيل المثال:

- **وضع Managed** (`wlan0`) + **وضع Monitor** (`mon0`) في الوقت ذاته
- التشغيل مع البقاء متصلاً بشبكة والتقاط حركة المرور في آنٍ واحد

### أي المحوّلات تدعم VIF؟

| الشريحة | دعم VIF | ملاحظات |
|---------|---------|---------|
| **MT7612U (AWUS036ACM)** | ✅ دعم أصلي كامل | الخيار الأمثل لسير عمل VIF |
| **RTL8812AU (AWUS036ACH)** | ⚠️ محدود | لا يمكن تشغيل managed + monitor في آنٍ واحد |
| **RTL8832BU (سلسلة AX)** | ⚠️ محدود | راجع وثائق الطراز المحدد |

### إنشاء واجهة افتراضية (MT7612U)

إذا كنت تملك AWUS036ACM (MT7612U):

```bash
# إنشاء واجهة مراقبة مع إبقاء wlan0 في وضع managed
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

تحقق من أن كلتا الواجهتين نشطتان:

```bash
iwconfig
```

يجب أن ترى:
- `wlan0` — وضع managed (متصل بنقطة الوصول)
- `mon0` — وضع monitor (يلتقط كل حركة المرور)

### حالات الاستخدام

**التقاط حركة المرور مع البقاء متصلاً:**

```bash
sudo airodump-ng mon0
```

تواصل `wlan0` عملها الطبيعي بينما تلتقط `mon0` كل شيء.

**نقطة وصول وهمية + مراقبة:**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## تمرير USB للأجهزة الافتراضية

هل تشغّل Linux داخل جهاز افتراضي (VM)؟ ستحتاج إلى تمرير محوّل USB إلى النظام الضيف.

### VirtualBox

1. أوقف تشغيل الجهاز الافتراضي
2. انتقل إلى **الإعدادات ← USB**
3. فعّل **USB 3.0 (xHCI) Controller**
4. انقر **+** لإضافة فلتر USB
5. اختر محوّل Alfa (المعرّف: `0bda:8812` أو `0e8d:7612`)
6. شغّل الجهاز الافتراضي

داخل الجهاز الافتراضي، شغّل `lsusb` للتأكيد، ثم اتبع خطوات Kali Linux أعلاه.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. شغّل الجهاز الافتراضي
2. من القائمة: **Virtual Machine → USB & Bluetooth**
3. ابحث عن محوّل Alfa وانقر **Connect**
4. يظهر المحوّل داخل الجهاز الافتراضي

شغّل `lsusb` للتأكيد، ثم اتبع خطوات تثبيت التعريف.

---

## استكشاف الأخطاء وإصلاحها

| المشكلة | السبب المحتمل | الحل |
|---------|--------------|------|
| `lsusb` لا يُظهر معرّف المحوّل | كابل معطوب أو لا يوجد طاقة | جرّب منفذ USB مختلفاً. استخدم هاب مزوّداً بطاقة على Pi. |
| `modprobe` يقول "Module not found" | وحدات النواة مفقودة | شغّل `sudo apt install linux-modules-extra-$(uname -r)` |
| التعريف يعمل لكن لا يمكن التبديل إلى وضع المراقبة | NetworkManager يتدخل | شغّل `sudo airmon-ng check kill` أولاً |
| وضع المراقبة يبدأ لكن لا يلتقط شيئاً | واجهة أو قناة خاطئة | شغّل `iwconfig`. اضبط القناة: `iwconfig wlan0mon channel 6` |
| فشل اختبار حقن الحزم | استخدام واجهة خاطئة | استخدم `wlan0mon` وليس `wlan0` |
| فشل إنشاء VIF | التعريف لم يُحمَّل بالكامل | افصل المحوّل وأعد توصيله، أو أعد تحميل الوحدة |

---

## الملحق: القائمة الكاملة لطرازات Alfa

| الطراز | الشريحة | التعريف | مصدر المرآة الصينية |
|--------|---------|---------|---------------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | تعريف مدمج في النواة |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## ملاحظات ختامية

يغطي هذا الدليل **جميع محوّلات Alfa USB WiFi** على **جميع توزيعات Linux الرئيسية**، باستخدام **موارد متاحة من الصين فقط**. يجب أن تكون الآن قادراً على:

✅ تثبيت تعريفات أي محوّل Alfa  
✅ تفعيل وضع المراقبة على Kali وUbuntu وDebian أو Raspberry Pi  
✅ اختبار حقن الحزم  
✅ استخدام الواجهات الافتراضية (VIF) مع الطرازات الداعمة  
✅ تمرير المحوّلات إلى الأجهزة الافتراضية  

**أسئلة أو مشكلات؟** راجع أدلة الطرازات المحددة في سلسلتنا، أو تواصل معنا على [yupitek.com](https://yupitek.com/ar/contact/).

---

## أدلة ذات صلة

هذا الدليل جزء من سلسلة **دليل تثبيت Alfa في الصين**:

- [دليل تثبيت AWUS036ACH في الصين](/ar/blog/awus036ach-china-install-guide/) — RTL8812AU، طاقة عالية
- [دليل تثبيت AWUS036ACM في الصين](/ar/blog/awus036acm-china-install-guide/) — MT7612U، أفضل دعم VIF
- [دليل تثبيت AWUS036ACS في الصين](/ar/blog/awus036acs-china-install-guide/) — RTL8811AU، خيار اقتصادي
- [دليل تثبيت AWUS036AX في الصين](/ar/blog/awus036ax-china-install-guide/) — Wi-Fi 6، RTL8832BU
- [دليل تثبيت AWUS036AXM في الصين](/ar/blog/awus036axm-china-install-guide/) — Wi-Fi 6، تصميم مدمج
- [دليل تثبيت AWUS036AXML في الصين](/ar/blog/awus036axml-china-install-guide/) — Wi-Fi 6، فائق الإحكام
- [دليل تثبيت AWUS036AXER في الصين](/ar/blog/awus036axer-china-install-guide/) — Wi-Fi 6، طاقة محسّنة
- [دليل تثبيت AWUS036EAC في الصين](/ar/blog/awus036eacs-china-install-guide/) — RTL8814AU، طاقة عالية

---

*آخر تحديث: 24 أبريل 2026*
