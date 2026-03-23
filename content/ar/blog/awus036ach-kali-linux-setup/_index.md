---
title: "دليل إعداد ALFA AWUS036ACH على Kali Linux: وضع المراقبة وحقن الحزم (2026)"
description: "دليل خطوة بخطوة لتثبيت ALFA AWUS036ACH على Kali Linux 2024/2025، تفعيل وضع المراقبة باستخدام airmon-ng، والتحقق من حقن الحزم."
date: 2026-03-23
draft: false
dir: rtl
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "Kali-Linux", "وضع-المراقبة", "حقن-الحزم", "RTL8812AU"]
---

أثبت ALFA AWUS036ACH مكانته بجدارة بوصفه محول USB WiFi الأكثر توصيةً في مجتمع Kali Linux — ولأسباب وجيهة. مدفوعاً بشريحة Realtek RTL8812AU، يوفر دعماً موثوقاً لوضع المراقبة وحقن الحزم اعتمد عليه محترفو الأمن منذ عام 2017. يأخذك هذا الدليل خطوةً بخطوة من لحظة فتح الصندوق حتى التحقق الكامل من عمل حقن الحزم على Kali Linux 2024 و2025.

---

## لماذا يُعدّ AWUS036ACH الخيار الأول؟

قبل الغوص في الأوامر، يستحق الأمر أن نفهم تحديداً ما يجعل هذا المحول مميزاً.

**شريحة RTL8812AU**

RTL8812AU من Realtek هي شريحة 802.11ac ثنائية النطاق (2.4 + 5 GHz) تمتلك دعماً قوياً لعمليات التحكم على مستوى الإطار التي تتطلبها أدوات الأمن. برنامج التشغيل المفتوح المصدر المُصان في `aircrack-ng/rtl8812au` على GitHub هو نتاج سنوات من التعاون بين فريق Aircrack-ng والمجتمع الأمني الأشمل على Linux. يتلقى صيانة منتظمة، ويُختبر بانتظام في مواجهة إصدارات النواة الجديدة، ويدعم وضع المراقبة وحقن الحزم دعماً صريحاً — لا بصفة ثانوية.

**دعم مجتمعي منذ 2017**

حين تواجه مشكلة مع AWUS036ACH، ستجد الإجابة. يظهر المحول في آلاف المنشورات في المنتديات وعلى YouTube وفي تقارير Hack The Box ومواد دورة Offensive Security ومشكلات GitHub. لا يضاهيه أي محول آخر من حيث قاعدة معرفة استكشاف الأخطاء وإصلاحها.

**أداء AC1200 ثنائي النطاق**

يوفر المحول ما يصل إلى 300 Mbps على 2.4 GHz و867 Mbps على 5 GHz، مع هوائيين RP-SMA قابلين للفصل يدعمان MIMO 2×2. تحصل على أداء نقل بيانات حقيقي عالٍ حين تحتاجه، إلى جانب قدرات اختبار الاختراق الكاملة.

**USB 3.0**

تمنع واجهة USB 3.0 المحولَ من أن يصبح عنق زجاجة أثناء الالتقاط عالي النطاق الترددي أو تشغيل أدوات متعددة في وقت واحد.

يمكنك إيجاده في متجرنا: [ALFA AWUS036ACH](/ar/products/alfa/awus036ach/).

---

## المتطلبات الأساسية

قبل البدء، تأكد مما يلي:

- **Kali Linux 2024.x أو أحدث** (هذا الدليل مُختبر على Kali 2024.1 حتى 2025.1)
- **منفذ USB 3.0** — يعمل المحول على USB 2.0 لكن معدل النقل يكون محدوداً. استخدم USB 3.0 للحصول على أفضل النتائج.
- **اتصال بالإنترنت** لتنزيل برنامج التشغيل
- **صلاحيات root أو sudo**
- **أدوات البناء مثبتة** — تشملها الخطوة الثانية

إن كنت تشغّل Kali في جهاز افتراضي (VMware أو VirtualBox أو UTM)، يجب تمرير جهاز USB إلى الجهاز الافتراضي. في VMware: VM ← Removable Devices ← وصّل محولك. في VirtualBox: الإعدادات ← USB ← أضف مرشح USB لجهاز Realtek.

---

## الخطوة 1: توصيل المحول والتحقق من اكتشافه

أدخل AWUS036ACH في منفذ USB وشغّل:

```bash
lsusb
```

يجب أن ترى إدخالاً مشابهاً لـ:

```
Bus 001 Device 004: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

المعرّفات المهمة:
- **معرف المورد:** `0bda` (Realtek)
- **معرف المنتج:** `8812` (RTL8812AU)

إذا لم يظهر الجهاز على الإطلاق، جرّب منفذ USB أو كابلاً آخر. إذا ظهر بمعرف منتج مختلف، فربما لديك إصدار مختلف من الجهاز.

تحقق أيضاً من سجل رسائل النواة فور التوصيل:

```bash
dmesg | tail -20
```

إذا كان برنامج التشغيل محملاً بالفعل (غير مرجح على تثبيت Kali جديد)، ستظهر أسطر كـ:

```
usb 1-1: new high-speed USB device number 4 using xhci_hcd
usbcore: registered new interface driver rtl88XXau
```

بدون تثبيت برنامج التشغيل، ستجد جهاز USB مكتشفاً لكن دون واجهة شبكة مُنشأة.

---

## الخطوة 2: تثبيت برنامج التشغيل RTL8812AU

هناك طريقتان للتثبيت. **الطريقة A (برنامج تشغيل aircrack-ng)** موصى بها لنظام Kali Linux. **الطريقة B (DKMS)** موصى بها إن أردت أن يستمر برنامج التشغيل تلقائياً عبر تحديثات النواة.

### تثبيت متطلبات البناء

كلتا الطريقتين تتطلبان المتطلبات ذاتها:

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

يثبّت هذا ترويسات النواة المطابقة لنواتك الجارية حالياً، وهي ضرورية لعملية بناء برنامج التشغيل.

### الطريقة A: التثبيت المباشر (برنامج تشغيل aircrack-ng — موصى به لـ Kali)

```bash
# استنساخ برنامج التشغيل الذي يُصونه aircrack-ng
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# بناء برنامج التشغيل
make

# تثبيت برنامج التشغيل
sudo make install

# تحميل وحدة برنامج التشغيل
sudo modprobe 88XXau
```

تحقق من تحميل الوحدة:

```bash
lsmod | grep 88XXau
```

الناتج المتوقع:

```
88XXau               3461120  0
cfg80211             1081344  1 88XXau
```

يجب الآن ظهور واجهة شبكة لاسلكية:

```bash
ip link show
# أو
iwconfig
```

ستلاحظ واجهة جديدة — عادةً `wlan0` أو `wlan1` إذا كانت لديك واجهات لاسلكية أخرى.

### الطريقة B: التثبيت عبر DKMS (يدوم عبر تحديثات النواة)

مع `make install` العادي، تُصرَّف وحدة برنامج التشغيل للنواة الحالية فقط. إذا حدّث Kali النواة (كما يحدث بانتظام عبر `apt upgrade`)، توقف عمل برنامج التشغيل حتى تُعيد تصريفه.

يحل DKMS (نظام دعم الوحدات الديناميكية) هذه المشكلة بإعادة تصريف برنامج التشغيل تلقائياً كلما ثُبّتت نواة جديدة.

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# استخدام سكريبت تثبيت DKMS
sudo make dkms_install
```

أو التسجيل اليدوي في DKMS:

```bash
# احصل على إصدار برنامج التشغيل
grep MODULE_VERSION Makefile | head -1
# مثال على الناتج: v5.6.4.2

# انسخ المصدر إلى مجلد DKMS
sudo cp -r ../rtl8812au /usr/src/rtl8812au-5.6.4.2

# سجّل مع DKMS
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```

تحقق من تسجيل DKMS:

```bash
dkms status
# المتوقع: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## الخطوة 3: تفعيل وضع المراقبة

مع تحميل برنامج التشغيل وظهور الواجهة، أنت جاهز لتفعيل وضع المراقبة.

### الطريقة A: airmon-ng (موصى بها)

أوقف أولاً أي عمليات قد تتعارض مع وضع المراقبة:

```bash
sudo airmon-ng check kill
```

يوقف هذا NetworkManager وwpa_supplicant والشياطين الأخرى التي تحتفظ بالواجهة. الناتج المتوقع:

```
Killing these processes:
  PID Name
  1234 NetworkManager
  1235 wpa_supplicant
```

شغّل الآن وضع المراقبة:

```bash
sudo airmon-ng start wlan0
```

استبدل `wlan0` باسم واجهتك الفعلي إذا كان مختلفاً. الناتج المتوقع:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       88XXau      Realtek Semiconductor Corp. RTL8812AU

                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)
```

واجهة وضع المراقبة تُسمى `wlan0mon`.

### الطريقة B: iw (يدوي)

إذا كنت تفضل عدم إيقاف NetworkManager، أو لم يكن airmon-ng متاحاً:

```bash
# أوقف الواجهة
sudo ip link set wlan0 down

# بدّل إلى وضع المراقبة
sudo iw dev wlan0 set type monitor

# أعد تشغيل الواجهة
sudo ip link set wlan0 up
```

لتحديد قناة بعينها عند تفعيل وضع المراقبة:

```bash
sudo iw dev wlan0 set channel 6
```

---

## الخطوة 4: التحقق من وضع المراقبة

تأكد من أن الواجهة في وضع المراقبة:

```bash
iwconfig
```

ابحث عن إدخال `wlan0mon` (أو `wlan0`). يجب أن يُظهر:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

المؤشر الأساسي هو `Mode:Monitor`. إذا ظهر `Mode:Managed`، فوضع المراقبة غير مفعّل.

يمكنك أيضاً استخدام:

```bash
iw dev wlan0mon info
```

يتضمن الناتج المتوقع:

```
type monitor
```

### التحقق باستخدام Airodump-ng

شغّل فحصاً سريعاً للتأكد من أن المحول يلتقط حركة البيانات:

```bash
sudo airodump-ng wlan0mon
```

يجب أن تظهر شبكات WiFi على الفور في الناتج. اضغط `Ctrl+C` للإيقاف.

---

## الخطوة 5: اختبار حقن الحزم

حقن الحزم هو القدرة على إرسال إطارات 802.11 عشوائية. استخدم اختبار الحقن في aireplay-ng:

```bash
sudo aireplay-ng --test wlan0mon
```

يبث هذا إطارات اختبار ويستمع للردود من نقاط الوصول القريبة. نتيجة ناجحة تبدو كالتالي:

```
15:42:11  Trying broadcast probe requests...
15:42:11  Injection is working!
15:42:12  Found 3 APs

15:42:12  Trying directed probe requests...
15:42:12  aa:bb:cc:dd:ee:ff - channel: 6 - 'HomeNetwork' - 30/30: 100%
15:42:13  11:22:33:44:55:66 - channel: 11 - 'OfficeWiFi' - 28/30: 93%
```

تشير النسبة المئوية إلى معدل نجاح الحقن. أي قيمة فوق 80% لنقاط الوصول القريبة مقبولة. 100% هي النتيجة المعتادة حين تكون في النطاق.

إذا رأيت `Injection is working!` في الناتج، يكون إعدادك مكتملاً وجاهزاً للاستخدام مع مجموعة Aircrack-ng الكاملة.

### اختبار الحقن على النطاق الثنائي (5 GHz)

لاختبار الحقن على 5 GHz، حدد القناة:

```bash
# التبديل إلى قناة 5 GHz (مثلاً القناة 36)
sudo iwconfig wlan0mon channel 36
# أو
sudo iw dev wlan0mon set channel 36

# شغّل اختبار الحقن
sudo aireplay-ng --test wlan0mon
```

---

## استكشاف الأخطاء وإصلاحها

### "Interface not found" / لا توجد واجهة wlan بعد تثبيت برنامج التشغيل

**السبب:** لم يُحمَّل وحدة برنامج التشغيل بنجاح.

**الحل:**

```bash
# تحقق من أخطاء تحميل الوحدة
dmesg | grep -i 88XX
dmesg | grep -i rtl

# حاول تحميل الوحدة يدوياً
sudo modprobe 88XXau

# إذا فشل modprobe، تحقق من التبعيات المفقودة
modinfo 88XXau

# أعد بناء برنامج التشغيل
cd rtl8812au
make clean && make && sudo make install
```

تأكد أيضاً من أن ترويسات النواة تطابق نواتك الجارية:

```bash
uname -r
ls /lib/modules/$(uname -r)/build
```

إذا لم يوجد مجلد `build`، أعد تثبيت الترويسات:

```bash
sudo apt install linux-headers-$(uname -r)
```

---

### "Operation not permitted" عند تفعيل وضع المراقبة

**السبب:** لا تعمل بصلاحيات root، أو هناك إذن مفقود.

**الحل:**

استخدم دائماً `sudo` مع airmon-ng وaireplay-ng:

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

إذا كنت تعمل بصلاحيات root بالفعل، تحقق من أن مستخدم Kali هو root فعلاً:

```bash
whoami
# يجب أن يُظهر: root
```

---

### "No module named rtl8812au" / فشل DKMS بعد تحديث النواة

**السبب:** لم يُعد DKMS تصريف برنامج التشغيل للنواة الجديدة.

**الحل:**

```bash
# تحقق من حالة DKMS
dkms status

# إذا أظهر rtl8812au حالة "built" وليس "installed" للنواة الجديدة:
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)

# إذا فشل ذلك، أزل وأعد التثبيت:
sudo dkms remove rtl8812au/5.6.4.2 --all
cd /path/to/rtl8812au
sudo make dkms_install
```

---

### وضع المراقبة يعمل لكن لا يُلتقط أي حركة بيانات

**السبب:** قناة خاطئة، تشويش، أو مشكلة في النطاق التنظيمي.

**الحل:**

```bash
# تحقق من القناة الحالية
iwconfig wlan0mon

# حدد القناة يدوياً
sudo iwconfig wlan0mon channel 1

# تحقق من النطاق التنظيمي
iw reg get

# عيّن نطاقاً تنظيمياً متساهلاً (استخدم بمسؤولية)
sudo iw reg set BO
```

---

### معدل نجاح حقن منخفض (أقل من 50%)

**السبب:** المسافة من نقطة الوصول، أو تشويش، أو مشكلة في إدارة الطاقة.

**الحل:**

```bash
# تعطيل إدارة الطاقة على الواجهة
sudo iwconfig wlan0mon power off

# رفع قدرة الإرسال (تحقق من اللوائح المحلية قبل الاستخدام)
sudo iw dev wlan0mon set txpower fixed 3000  # 30 dBm
```

---

## استعادة الوضع الاعتيادي (Managed Mode)

حين تنتهي من الاختبار وتريد الاتصال بالشبكات بصورة طبيعية:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

أو باستخدام iw:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

---

## ملخص

| الخطوة | الأمر |
|---|---|
| التحقق من الاكتشاف | `lsusb \| grep Realtek` |
| تثبيت التبعيات | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| استنساخ برنامج التشغيل | `git clone https://github.com/aircrack-ng/rtl8812au` |
| البناء والتثبيت | `make && sudo make install` |
| تحميل الوحدة | `sudo modprobe 88XXau` |
| إيقاف العمليات المتعارضة | `sudo airmon-ng check kill` |
| تفعيل وضع المراقبة | `sudo airmon-ng start wlan0` |
| التحقق من وضع المراقبة | `iwconfig wlan0mon` |
| اختبار الحقن | `sudo aireplay-ng --test wlan0mon` |

يظل [ALFA AWUS036ACH](/ar/products/alfa/awus036ach/) مقروناً بـ Kali Linux 2024+ وبرنامج تشغيل RTL8812AU من aircrack-ng الإعداد الأكثر موثوقية والأوفر توثيقاً في مجتمع اختبار الاختراق. بعد التحقق من عمل الحقن، ستكون جاهزاً لاستخدام مجموعة Aircrack-ng الكاملة وWireshark وKismet وBettercap وأي أداة أخرى تتطلب وضع المراقبة أو حقن الحزم.
