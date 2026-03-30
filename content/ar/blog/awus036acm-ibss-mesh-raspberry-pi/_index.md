---
title: "ALFA AWUS036ACM: تفعيل شبكات IBSS Ad Hoc و 802.11s Mesh على Raspberry Pi مع MT7612U"
description: "ALFA AWUS036ACM (MT7612U) هو المحوّل USB WiFi الوحيد من ALFA المتوفر حالياً الذي يدعم بالكامل شبكات IBSS Ad Hoc و 802.11s Mesh على Raspberry Pi — تشغيل فوري دون الحاجة لتثبيت برامج التشغيل."
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "شبكة شبكية", "Linux", "لاسلكي"]
dir: rtl
---

# ALFA AWUS036ACM: تفعيل شبكات IBSS Ad Hoc و 802.11s Mesh على Raspberry Pi مع MT7612U

إذا حاولت يومًا بناء شبكة WiFi بين عقد Raspberry Pi **دون الحاجة إلى راوتر** — أو إنشاء شبكة شبكية لاسلكية ذاتية الإصلاح تُوجِّه حركة البيانات تلقائيًا عبر نقاط وسيطة — فستكتشف سريعًا أن معظم محوّلات USB WiFi لا تدعم ذلك. ببساطة، برنامج التشغيل الخاص بالنواة لا يكشف عن الأوضاع اللازمة.

**ALFA AWUS036ACM**، المُدار بشريحة **MediaTek MT7612U**، هو الاستثناء. يُنفِّذ برنامج التشغيل `mt76` المدمج في النواة واجهة Linux mac80211 الكاملة، مما يعني دعمًا أصليًا لوضعَي **IBSS (Ad Hoc)** و**802.11s Mesh Point** على Raspberry Pi — جاهزًا للاستخدام فور التوصيل، دون الحاجة إلى تصريف أي برنامج تشغيل.

يشرح هذا الدليل آلية عمل كلا الوضعين بدقة، ويقدّم تعليمات إعداد خطوة بخطوة، ويوضح متى تختار كل وضع منهما.

---

## جدول المحتويات

1. [ما هي IBSS و 802.11s Mesh ولماذا تهمّك؟](#1-what-are-ibss-and-80211s-mesh)
2. [المواصفات التقنية لـ ALFA AWUS036ACM](#2-alfa-awus036acm-hardware-specifications)
3. [برنامج التشغيل MT7612U على Raspberry Pi](#3-the-mt7612u-driver-on-raspberry-pi)
4. [الوضع الأول: شبكات IBSS Ad Hoc](#4-mode-1-ibss-ad-hoc-networking)
5. [الوضع الثاني: شبكات 802.11s Mesh Point](#5-mode-2-80211s-mesh-point-networking)
6. [حالات استخدام من الواقع العملي](#6-real-world-use-cases)
7. [لماذا AWUS036ACM هو الخيار الوحيد من ALFA لهذا الغرض](#7-why-the-awus036acm-is-the-only-alfa-choice-for-this)
8. [الأسئلة الشائعة واستكشاف الأخطاء](#8-faq-and-troubleshooting)
9. [أين تشتري](#9-where-to-buy)

---

## 1. ما هي IBSS و 802.11s Mesh؟

### IBSS — المجموعة الخدمية الأساسية المستقلة (وضع Ad Hoc)

عندما تتصل بجهاز الكمبيوتر المحمول براوتر WiFi المنزلي، يكون محوّلك في وضع **Managed (Station)** — إذ يتواصل مع نقطة وصول مركزية واحدة. أما IBSS فهو النقيض تمامًا: إنه مواصفة IEEE 802.11 لـ**الشبكات اللاسلكية من نظير إلى نظير دون أي بنية تحتية مركزية**.

في وضع IBSS:

- تتواصل الأجهزة **مباشرةً** مع بعضها، دون أي نقطة وصول أو راوتر
- يمكن لأي جهازين على نفس SSID والقناة تبادل البيانات
- الشبكة مكتفية بذاتها — لا حاجة لاتصال بالإنترنت
- تُعيَّن عناوين IP بشكل ثابت (أو عبر خادم DHCP بسيط تُشغّله بنفسك)
- الجهاز الأول الذي "ينضم" إلى IBSS يصبح مصدر BSSID (معرِّف الخلية)

تخيّل الأمر كإنشاء شبكة LAN لاسلكية خاصة فورية بين عدد صغير من عقد Pi — رابط ثنائي العقد، أو مجموعة استشعار ثلاثية العقد، أو مجموعة اتصالات محمولة تُنشر في الميدان.

**قيود IBSS الواجب معرفتها:**
- يجب أن تكون جميع العقد ضمن نطاق الإرسال الراديوي المباشر لبعضها — لا يوجد توجيه متعدد القفزات التلقائي
- تشفير WPA2 القياسي غير متاح في وضع IBSS (WEP ممكن تقنيًا لكنه غير مُوصى به؛ تعتمد معظم عمليات النشر على أمان طبقة التطبيقات عوضًا عن ذلك)
- يُمكن توسيع الشبكة عمليًا إلى 3–5 عقد قبل أن يتراجع الأداء

### 802.11s Mesh Point — البديل القابل للتوسع

802.11s هو إضافة IEEE منفصلة تُعرِّف **شبكات الشبكية اللاسلكية الحقيقية**. على خلاف IBSS، تعمل شبكة 802.11s على:

- اكتشاف العقد المجاورة تلقائيًا وبناء جدول توجيه
- إعادة توجيه حركة البيانات عبر قفزات وسيطة للوصول إلى عقد خارج نطاق الاتصال المباشر
- إصلاح نفسها عند اختفاء عقدة — تُستخدم المسارات البديلة تلقائيًا
- الاعتماد على **بروتوكول HWMP (Hybrid Wireless Mesh Protocol)** لاختيار المسار افتراضيًا

```
مثال: شبكة شبكية من 4 عقد

  [Pi A] ──── [Pi B] ──── [Pi C]
                │
              [Pi D]

Pi A يصل إلى Pi C عبر Pi B تلقائيًا.
Pi A يصل إلى Pi D عبر Pi B تلقائيًا.
إذا فشل Pi B، تحاول الشبكة الشبكية إيجاد مسارات بديلة.
```

802.11s هو الخيار الصحيح عندما يكون لديك أكثر من 3–4 عقد، أو عندما تكون العقد موزعةً على مساحة أكبر، أو عندما تريد شبكة مرنة دون إدارة يدوية.

### لماذا يصعب إيجاد محوّل يعمل بهذه الأوضاع

يتطلب الوضعان أعلاه أن يكون برنامج تشغيل WiFi مبنيًا على طبقة **mac80211** في Linux — مكدس IEEE 802.11 الرسمي في النواة. فقط برامج التشغيل المتوافقة مع mac80211 تكشف عن IBSS ونقطة الشبكة الشبكية كأنواع واجهات قابلة للاستخدام.

كثير من محوّلات USB WiFi الشائعة تستخدم **برامج تشغيل خارج النواة** تُنفِّذ مكدسها اللاسلكي المبسّط الخاص وتتعمّد تخطّي دعم IBSS والشبكة الشبكية. حتى بعض برامج التشغيل المدمجة في النواة لمجموعات الشرائح الأحدث لا تكشف عن هذه الأوضاع.

MT7612U هو أحد مجموعات الشرائح القليلة التي تكون إجابتها واضحة وقاطعة بـ**نعم** لكلا الوضعين.

---

## 2. المواصفات التقنية لـ ALFA AWUS036ACM

AWUS036ACM هو محوّل USB 3.0 ثنائي النطاق AC1200 من ALFA Network، مصمّم لمستخدمي Linux المتقدمين ومطوّري البرمجيات المدمجة.

![ALFA AWUS036ACM](/images/products/alfa/awus036acm.png)

### المواصفات الأساسية

| المعامل | القيمة |
|---|---|
| **مجموعة الشرائح** | MediaTek MT7612U |
| **معيار WiFi** | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| **نطاقات التردد** | 2.4 GHz (2.412–2.472 GHz) + 5 GHz (5.15–5.825 GHz) |
| **عرض القناة** | 20 / 40 / 80 MHz |
| **السرعة القصوى (5 GHz)** | 867 Mbps (802.11ac) |
| **السرعة القصوى (2.4 GHz)** | 300 Mbps (802.11n) |
| **السرعة الإجمالية** | AC1200 (867 + 300 Mbps) |
| **واجهة USB** | USB 3.0 Type-A (متوافقة مع USB 2.0) |
| **الهوائيات** | موصلان RP-SMA أنثى، هوائيان ثنائي النطاق 5 dBi (قابلان للفصل) |
| **USB VID/PID** | 0e8d:7612 |
| **مؤشرات LED** | الطاقة + نشاط WLAN |
| **الملحقات المرفقة** | كابل تمديد USB 3.0، قرص برامج التشغيل (Windows) |
| **الأبعاد** | 62 × 85.3 × 24 mm |
| **الوزن** | 60 g |
| **بلد المنشأ** | تايوان (Alfa Network Inc.) |

### قدرة الإرسال

| المعيار | قدرة TX |
|---|---|
| 802.11a | 20 dBm |
| 802.11b | 23 dBm |
| 802.11g | 23 dBm |
| 802.11n | 21 dBm |
| 802.11ac | 20 dBm |

### حساسية الاستقبال

| المعيار | الحساسية |
|---|---|
| 802.11a | −92 dBm |
| 802.11b | −97 dBm |
| 802.11g | −90 dBm |
| 802.11n | −90 dBm |
| 802.11ac | −86 dBm |

### أوضاع الواجهة المدعومة (القائمة الكاملة)

هذا هو جدول القدرات الأساسي. يدعم برنامج تشغيل MT7612U / mt76x2u جميع أوضاع واجهة mac80211 الرئيسية:

| الوضع | مدعوم | الوصف |
|---|---|---|
| **IBSS** | ✅ نعم | شبكة نظير إلى نظير Ad Hoc، لا تحتاج نقطة وصول |
| **Managed (Station)** | ✅ نعم | وضع العميل القياسي |
| **AP** | ✅ نعم | نقطة وصول برمجية (hostapd) |
| **AP/VLAN** | ✅ نعم | شبكة محلية افتراضية عبر نقطة الوصول |
| **Monitor** | ✅ نعم | التقاط سلبي + حقن حزم |
| **Mesh Point** | ✅ نعم | شبكة شبكية متعددة القفزات 802.11s |
| **P2P-client** | ✅ نعم | عميل Wi-Fi Direct |
| **P2P-GO** | ✅ نعم | مالك مجموعة Wi-Fi Direct |

### الأمان اللاسلكي
WPA2 / WPA / WEP / WPA-PSK / 802.1X / 64–128-bit WEP

### أنظمة التشغيل المدعومة

| نظام التشغيل | الحالة | ملاحظات |
|---|---|---|
| Raspberry Pi OS (2020+) | ✅ تشغيل فوري | لا حاجة لتثبيت برامج التشغيل |
| Ubuntu 20.04 LTS+ | ✅ تشغيل فوري | برنامج التشغيل mt76 المدمج في النواة |
| Kali Linux 2019.3+ | ✅ تشغيل فوري | دعم كامل للمراقبة + الحقن + VIF |
| Debian 11+ | ✅ يعمل | قد يحتاج firmware-misc-nonfree |
| Arch Linux | ✅ تشغيل فوري | مدمج في النواة منذ 4.19 |
| Windows 10/11 | ✅ مدعوم | برنامج تشغيل رسمي من موقع Alfa |
| Android NetHunter | ✅ مدعوم | USB OTG |
| macOS 11+ / Apple Silicon | ❌ غير مدعوم | macOS 10.7–10.12 فقط |

---

## 3. برنامج التشغيل MT7612U على Raspberry Pi

### برنامج التشغيل: mt76x2u (جزء من عائلة mt76)

يتولّى برنامج التشغيل `mt76x2u` إدارة MediaTek MT7612U، وهو جزء من مشروع **mt76** الأشمل الذي يصونه MediaTek ويُدمجه في النواة الرئيسية لـ Linux.

**الأرقام الحاسمة:**
- مدمج في النواة منذ: **Linux kernel 4.19** (صدر في أكتوبر 2018)
- يُشحن Raspberry Pi OS بنواة **5.15+** (Pi 4/5) و**5.10+** (Pi 3B+) — كلاهما فوق 4.19 بمراحل
- **لا توجد خطوة تثبيت على أي إصدار حديث من Raspberry Pi OS**

### كيفية التحقق من تحميل برنامج التشغيل

بعد توصيل AWUS036ACM، شغّل:

```bash
lsusb
```

ابحث عن الإدخال:
```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

ثم تحقق من تفعيل برنامج التشغيل:

```bash
dmesg | grep mt76
```

الإخراج المتوقع (مختصر):
```
mt76x2u 1-1.4:1.0: ASIC revision: 76120044
mt76x2u 1-1.4:1.0: Firmware Version: 0.1
mt76x2u 1-1.4:1.0: loaded firmware from mediatek/mt7662u_rom_patch.bin
```

سرد الواجهة الجديدة:
```bash
iw dev
```

يجب أن ترى واجهة جديدة (عادةً `wlan1` إذا كانت WiFi المدمجة في Pi هي `wlan0`):
```
phy#1
    Interface wlan1
        ifindex 4
        wdev 0x100000001
        addr xx:xx:xx:xx:xx:xx
        type managed
        channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
```

تحقق من قائمة القدرات الكاملة للمحوّل:
```bash
iw phy phy1 info | grep -A 20 "Supported interface modes"
```

ستظهر:
```
Supported interface modes:
     * IBSS
     * managed
     * AP
     * AP/VLAN
     * monitor
     * mesh point
     * P2P-client
     * P2P-GO
```

### لماذا تُهمّ بنية برنامج التشغيل

مكدس برامج التشغيل لـ AWUS036ACM يبدو هكذا:

```
Your Application (ping, iperf3, batman-adv...)
        ↓
nl80211 / cfg80211  ← kernel WiFi configuration API
        ↓
mac80211            ← IEEE 802.11 software MAC layer
        ↓
mt76x2u             ← MT7612U USB hardware driver
        ↓
MediaTek MT7612U    ← Physical chip (2×2 MIMO, USB 3.0)
```

**mac80211** هو تطبيق نواة Linux لآلة الحالة الكاملة 802.11 — يتولّى إدارة المنارات، وبناء الإطارات، وتوفير الطاقة، واكتشاف أقران IBSS، وتوجيه مسارات الشبكة الشبكية. برامج التشغيل المبنية فوق mac80211 ترث جميع هذه القدرات تلقائيًا.

أما برامج التشغيل التي تتجاوز mac80211 (كبرامج Realtek خارج النواة مثلًا) فهي تُنفِّذ فقط الأوضاع التي تختار كشفها — وكثيرًا ما يُحذف IBSS ونقطة الشبكة الشبكية منها.

---

## 4. الوضع الأول: شبكات IBSS Ad Hoc

### كيفية عمل IBSS

في وضع IBSS، يُدير كل محوّل إطارات 802.11 الخاصة به. عندما يُضبط محوّلان على نفس SSID والقناة:

1. يُولِّد الجهاز الأول **BSSID** عشوائيًا (معرِّف خلية IBSS)
2. يُذيع منارات على القناة المختارة
3. يفحص الجهاز الثاني، يجد المنارة، و**ينضم** إلى الخلية
4. يمكن لكلا الجهازين الآن تبادل إطارات البيانات مباشرةً — دون أي نقطة وصول وسيطة

من منظور نظام التشغيل، تتصرف واجهة IBSS كواجهة Ethernet عادية — تُعيّن عناوين IP وتستخدم TCP/IP بشكل طبيعي.

### مقارنة سريعة: IBSS مقابل وضع Managed

| الميزة | IBSS (Ad Hoc) | Managed (Station) |
|---|---|---|
| هل تحتاج نقطة وصول مركزية؟ | ❌ لا | ✅ نعم |
| هل يلزم اتصال بالإنترنت؟ | ❌ لا | عادةً نعم |
| تعقيد الإعداد | منخفض | منخفض جدًا |
| الحد الأقصى العملي للعقد | 3–5 | غير محدود (عبر AP) |
| دعم WPA2 | ❌ لا | ✅ نعم |
| الأنسب لـ | مجموعات Pi المعزولة، أطقم الميدان | الشبكات المنزلية/المكتبية |

### خطوة بخطوة: شبكة IBSS بين عقدتي Raspberry Pi

يُنشئ هذا المثال رابطًا مباشرًا على 5 GHz بين وحدتَي Raspberry Pi. عدّل عناوين IP وSSID لتتناسب مع بيئتك.

**على كلتا العقدتين — تحديد الواجهة الصحيحة:**

```bash
iw dev
```

سيظهر AWUS036ACM عادةً كـ`wlan1` (إذا كانت WiFi المدمجة في Pi هي `wlan0`). تحقق بمطابقة عنوان MAC مع `lsusb`. في جميع الأوامر التالية، استبدل `wlan1` باسم واجهتك الفعلية.

---

#### العقدة 1 (Pi #1 — IP: 192.168.88.1)

**الخطوة 1 — إيقاف NetworkManager / wpa_supplicant لمنع التدخل:**

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```

**الخطوة 2 — إيقاف تشغيل الواجهة:**

```bash
sudo ip link set wlan1 down
```

**الخطوة 3 — ضبط الواجهة على وضع IBSS:**

```bash
sudo iw dev wlan1 set type ibss
```

**الخطوة 4 — إعادة تشغيل الواجهة:**

```bash
sudo ip link set wlan1 up
```

**الخطوة 5 — الانضمام إلى (أو إنشاء) خلية IBSS على 5 GHz القناة 36:**

```bash
sudo iw dev wlan1 ibss join RaspberryMesh 5180
```

> **مرجع الترددات:**
> - 5180 MHz = 5 GHz القناة 36 (قناة داخلية شائعة، إنتاجية جيدة)
> - 5200 MHz = 5 GHz القناة 40
> - 2412 MHz = 2.4 GHz القناة 1 (مدى أفضل، سرعة أقل)
> - 2437 MHz = 2.4 GHz القناة 6

**الخطوة 6 — تعيين عنوان IP ثابت:**

```bash
sudo ip addr add 192.168.88.1/24 dev wlan1
```

---

#### العقدة 2 (Pi #2 — IP: 192.168.88.2)

شغّل نفس الأوامر، مع تغيير عنوان IP فقط:

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
sudo ip link set wlan1 down
sudo iw dev wlan1 set type ibss
sudo ip link set wlan1 up
sudo iw dev wlan1 ibss join RaspberryMesh 5180
sudo ip addr add 192.168.88.2/24 dev wlan1
```

---

#### التحقق من الرابط

على العقدة 1:
```bash
iw dev wlan1 link
```

الإخراج المتوقع (بعد انضمام العقدة 2):
```
Connected to xx:xx:xx:xx:xx:xx (on wlan1)
    IBSS cell ID/AP: xx:xx:xx:xx:xx:xx
    SSID: RaspberryMesh
    freq: 5180
    RX: 1204 bytes (12 packets)
    TX: 852 bytes (8 packets)
    signal: -48 dBm
    tx bitrate: 300.0 MBit/s MCS 15 40MHz
```

اختبار الاتصال:
```bash
ping -c 4 192.168.88.2
```

```
PING 192.168.88.2 (192.168.88.2) 56(84) bytes of data.
64 bytes from 192.168.88.2: icmp_seq=1 ttl=64 time=1.84 ms
64 bytes from 192.168.88.2: icmp_seq=2 ttl=64 time=1.92 ms
64 bytes from 192.168.88.2: icmp_seq=3 ttl=64 time=2.01 ms
64 bytes from 192.168.88.2: icmp_seq=4 ttl=64 time=1.88 ms
```

اختبار الإنتاجية باستخدام iperf3:
```bash
# على العقدة 2 (الخادم):
iperf3 -s

# على العقدة 1 (العميل):
iperf3 -c 192.168.88.2 -t 10
```

### جعل IBSS دائمًا عبر إعادة التشغيل

أنشئ `/etc/systemd/system/ibss-mesh.service` على كل عقدة:

```ini
[Unit]
Description=IBSS Ad Hoc Mesh Network
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  ip link set wlan1 down && \
  iw dev wlan1 set type ibss && \
  ip link set wlan1 up && \
  iw dev wlan1 ibss join RaspberryMesh 5180 && \
  ip addr add 192.168.88.1/24 dev wlan1'
ExecStop=/bin/bash -c '\
  iw dev wlan1 ibss leave && \
  ip link set wlan1 down'

[Install]
WantedBy=multi-user.target
```

فعّله:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ibss-mesh.service
sudo systemctl start ibss-mesh.service
```

> **ملاحظة:** غيّر عنوان IP في ملف الخدمة لكل عقدة (`.1`، `.2`، `.3`، إلخ)

### إضافة عقدة ثالثة

للعقدة 3، اتّبع نفس الإجراء مع IP `192.168.88.3`. يجب أن تكون جميع العقد الثلاث ضمن نطاق الإرسال الراديوي المباشر لبعضها. لتوجيه حركة البيانات بين العقدة 1 والعقدة 3 عبر العقدة 2، فعّل إعادة توجيه IP على العقدة 2:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

## 5. الوضع الثاني: شبكات 802.11s Mesh Point

### كيفية عمل 802.11s

تُضيف إضافة 802.11s **طبقة تنسيق شبكية** مباشرةً في 802.11 MAC. بدلًا من تواصل جميع العقد مع نقطة وصول مركزية، تقوم كل عقدة بـ:

1. اكتشاف عقد الشبكة الشبكية المجاورة عبر بثّ إطارات **Mesh Beacon** على القناة المختارة و`mesh_id`
2. تشغيل **HWMP (Hybrid Wireless Mesh Protocol)** لحساب أفضل مسار لكل وجهة
3. تغليف إطارات البيانات بـ**Mesh Header** يتضمن عناوين MAC المصدر والوجهة بالإضافة إلى رقم تسلسلي للشبكة الشبكية
4. إعادة توجيه الإطارات تلقائيًا عبر قفزات وسيطة عندما تكون الوجهة خارج نطاق الاتصال المباشر

تكشف نواة Linux عن هذا عبر نوع واجهة `mp` (نقطة شبكية) في `iw`، وتتولى تطبيق 80211s في النواة جميع عمليات الاقتران وإدارة المسارات.

### مقارنة 802.11s بـ IBSS

| الميزة | IBSS (Ad Hoc) | 802.11s Mesh Point |
|---|---|---|
| معيار IEEE | 802.11 IBSS | 802.11s |
| التوجيه متعدد القفزات | ❌ يدوي فقط | ✅ تلقائي (HWMP) |
| نطاق العقد | جميعها ضمن النطاق المباشر | يمتد إلى ما وراء قفزة واحدة |
| قابلية التوسع | 3–5 عقد عمليًا | 10+ عقد مع batman-adv |
| تعقيد الإعداد | منخفض | متوسط |
| الإصلاح الذاتي | ❌ لا | ✅ نعم |
| الأنسب لـ | إعدادات 2–3 عقد بسيطة | الأنظمة الموزعة الأكبر |

### خطوة بخطوة: شبكة شبكية 802.11s متعددة العقد

يبني هذا المثال شبكة شبكية ثلاثية العقد على 5 GHz القناة 36. تكتشف كل عقدة الأخريات تلقائيًا وتُنشئ مسارات اتصال.

---

#### على كل عقدة — إنشاء واجهة الشبكة الشبكية

**الخطوة 1 — تحديد اسم الجهاز الفيزيائي (phy):**

```bash
iw dev
```

ابحث عن phy المرتبط بـ AWUS036ACM (عادةً `phy1`):
```
phy#1
    Interface wlan1
        ...
```

**الخطوة 2 — إضافة واجهة نقطة شبكية جديدة باسم `mesh0`:**

```bash
sudo iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh
```

> ينشئ هذا واجهة افتراضية جديدة `mesh0` على نفس الراديو الفيزيائي لـ`wlan1`. يمكن أن تبقى `wlan1` الأصلية في وضع managed للوصول إلى الإنترنت في آنٍ واحد — هذا ما يُعرَف بـ VIF (Virtual Interface).

**الخطوة 3 — ضبط قناة التشغيل (5 GHz القناة 36):**

```bash
sudo iw dev mesh0 set channel 36
```

**الخطوة 4 — تشغيل واجهة الشبكة الشبكية:**

```bash
sudo ip link set mesh0 up
```

**الخطوة 5 — تعيين عنوان IP فريد لكل عقدة:**

```bash
# العقدة 1:
sudo ip addr add 10.88.0.1/24 dev mesh0

# العقدة 2:
sudo ip addr add 10.88.0.2/24 dev mesh0

# العقدة 3:
sudo ip addr add 10.88.0.3/24 dev mesh0
```

---

#### التحقق من تكوين الشبكة الشبكية

**تحقق من اكتشاف الأقران:**

```bash
iw dev mesh0 station dump
```

مثال على الإخراج (العقدة 1 ترى العقدة 2 والعقدة 3):
```
Station xx:xx:xx:xx:xx:02 (on mesh0)
    inactive time:  120 ms
    rx bytes:       4820
    tx bytes:       3560
    signal:         -52 dBm
    tx bitrate:     300.0 MBit/s MCS 15 40MHz
    mesh plink:     ESTAB
    mesh local PS mode: ACTIVE

Station xx:xx:xx:xx:xx:03 (on mesh0)
    mesh plink:     ESTAB
```

**فحص مسارات توجيه الشبكة الشبكية:**

```bash
iw dev mesh0 mpath dump
```

```
DEST ADDR         NEXT HOP          IFACE   SN      METRIC  QLEN    EXPTIME         DTIM    DRET    FLAGS
xx:xx:xx:xx:xx:02 xx:xx:xx:xx:xx:02 mesh0   32      1158    0       0       100     0       0x4
xx:xx:xx:xx:xx:03 xx:xx:xx:xx:xx:02 mesh0   18      2316    0       0       100     0       0x14
```

> القفزة التالية للعقدة 3 هي العقدة 2 — أي أن العقدة 1 تصل إلى العقدة 3 عبر العقدة 2 تلقائيًا.

**اختبار الاتصال عبر الشبكة الشبكية:**

```bash
# من العقدة 1:
ping -c 4 10.88.0.3
```

### متقدم: إضافة batman-adv لتوجيه الطبقة الثانية

للنشر في بيئات الإنتاج، يُوفّر استبدال HWMP المدمج في النواة بـ**batman-adv** توجيهًا أكثر تقدمًا، وأداءً أفضل في ظل حركة العقد، وتوافقًا مع أدوات الشبكات ذات المستوى الأعلى.

**تثبيت batman-adv:**

```bash
sudo apt install batctl
```

**تحميل الوحدة:**

```bash
sudo modprobe batman-adv
```

**تهيئة واجهة الشبكة الشبكية كعبد لـ batman-adv:**

```bash
# رفع mesh0 دون IP أولًا
sudo ip link set mesh0 up
sudo batctl if add mesh0

# رفع واجهة batman
sudo ip link set bat0 up

# تعيين IP لواجهة batman (وليس mesh0)
sudo ip addr add 10.88.0.1/24 dev bat0
```

**فحص جدول توجيه batman:**

```bash
sudo batctl n    # Neighbours
sudo batctl o    # Originator table (all known nodes)
sudo batctl tg   # Translation table (MAC → IP mapping)
```

### جعل شبكة 802.11s Mesh دائمة

أنشئ `/etc/systemd/system/mesh-point.service`:

```ini
[Unit]
Description=802.11s Mesh Point Network
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh && \
  iw dev mesh0 set channel 36 && \
  ip link set mesh0 up && \
  ip addr add 10.88.0.1/24 dev mesh0'
ExecStop=/bin/bash -c '\
  ip link set mesh0 down && \
  iw dev mesh0 del'

[Install]
WantedBy=multi-user.target
```

تفعيل:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mesh-point.service
sudo systemctl start mesh-point.service
```

---

## 6. حالات استخدام من الواقع العملي

### حالة الاستخدام 1 — شبكة استشعار بعيدة عن الشبكة (زراعة ذكية / رصد بيئي)

**السيناريو:** ثلاث وحدات Raspberry Pi منتشرة عبر حقل زراعي، كل منها مزوّدة بمستشعرات لرطوبة التربة ودرجة الحرارة والرطوبة. لا توجد بنية تحتية خلوية أو WiFi متاحة.

**الإعداد:** IBSS على 2.4 GHz القناة 1 (2412 MHz) لأقصى مدى. تجمع كل عقدة بيانات المستشعرات وترسلها إلى عقدة مُسجِّل مركزية (العقدة 1) كل 30 ثانية.

**لماذا AWUS036ACM:** تمنح هوائيات 5 dBi وقدرة TX البالغة 23 dBm على 2.4 GHz المحوّلَ مدىً أفضل من المتوسط — مفيد لتغطية المسافات بين صفوف المحاصيل في الحقل. مع ترقيات هوائيات RP-SMA الاختيارية (مثل هوائيات Yagi الاتجاهية)، يمكن تمديد المدى بشكل ملحوظ.

**خط أنابيب البيانات النموذجي:**
```
[Sensor Pi A] ──IBSS──> [Edge Pi B (logger)]
[Sensor Pi C] ──IBSS──> [Edge Pi B (logger)]
```

---

### حالة الاستخدام 2 — التواصل بين الطائرات المسيّرة / الروبوتات

**السيناريو:** طائرتان مسيّرتان أو ثلاث روبوتات أرضية مبنية على Raspberry Pi تحتاج إلى تبادل بيانات القياس عن بُعد وتنسيق الأفعال دون المرور بمحطة أرضية.

**الإعداد:** IBSS على 5 GHz القناة 36 (5180 MHz) لزمن استجابة منخفض وإنتاجية عالية. تبثّ كل وحدة فيديو H.264 بدقة 1080p بمعدل ~5 Mbps بالإضافة إلى بيانات قياس عن بُعد بأقل من 100 Kbps.

**لماذا 5 GHz:** بسرعات AC1200 (867 Mbps على 5 GHz)، يملك AWUS036ACM هامش عمل كافٍ لدفقات فيديو متعددة متزامنة. كما يتجنب نطاق 5 GHz التداخل المزدحم الشائع في نطاق 2.4 GHz في المناطق الحضرية.

**الطوبولوجيا:**
```
[Drone 1 / 192.168.88.1] ──5GHz IBSS──> [Drone 2 / 192.168.88.2]
```

---

### حالة الاستخدام 3 — مجموعة اتصالات الاستجابة للكوارث / الطوارئ

**السيناريو:** يصل فريق نشر سريع إلى موقع دون أي بنية تحتية. يحمل كل عضو Raspberry Pi Zero 2W + AWUS036ACM + بطارية محمولة. في غضون 60 ثانية، تكون شبكة شبكية متعددة العقد تعمل بالكامل للتواصل النصي ومشاركة الملفات والتنسيق.

**الإعداد:** 802.11s Mesh على 2.4 GHz لأقصى مدى عبر المباني والعوائق. تتولّى batman-adv التوجيه حتى لا يضطر الفريق لإدارة عناوين IP يدويًا.

**لماذا 802.11s / batman-adv:** عندما يتحرك أعضاء الفريق، تتغير طوبولوجيا الشبكة الشبكية. تُحدِّث batman-adv المسارات تلقائيًا. لا نقطة فشل واحدة.

---

### حالة الاستخدام 4 — العمود الفقري لمجموعة حوسبة Raspberry Pi

**السيناريو:** يُشغِّل مطوّر مجموعة حوسبة بأسلوب Beowulf باستخدام 4–6 وحدات Raspberry Pi 4. يريد شبكة ربط مخصصة منخفضة الكمون مستقلة عن شبكة Ethernet الرئيسية.

**الإعداد:** 802.11s Mesh على 5 GHz باستخدام mesh_id `ClusterBackbone`. تتواصل كل عقدة عبر الشبكة الشبكية للرسائل بين العمليات (MPI، Redis pub/sub، ZeroMQ).

**لماذا الشبكة الشبكية المخصصة:** يمنع فصل حركة مرور المجموعة عن الشبكة الرئيسية تشبّع مفتاح Ethernet المشترك، ويتيح شبكات المجموعة حتى عندما تكون الشبكة الرئيسية غير متاحة.

---

### حالة الاستخدام 5 — مختبر أبحاث الأمن / بيئة اختبار معزولة

**السيناريو:** يريد مختبر اختراق (Penetration Tester) أو باحث أمني محاكاة شبكة IBSS 802.11 خاصة لاختبار الثغرات الخاصة بشبكات Ad Hoc أو التحقق من صحة أدوات الكشف.

**الإعداد:** IBSS على قناة نظيفة، معزولة عن WiFi الإنتاجي، باستخدام وضع المراقبة في AWUS036ACM في آنٍ واحد عبر VIF. واجهة واحدة في وضع IBSS (مشاركة في الشبكة)، وأخرى في وضع monitor (التقاط جميع الإطارات لتحليل Wireshark).

```bash
# Create monitor interface alongside IBSS
sudo iw phy phy1 interface add mon0 type monitor
sudo ip link set mon0 up
# Capture:
sudo tcpdump -i mon0 -w capture.pcap
```

---

## 7. لماذا AWUS036ACM هو الخيار الوحيد من ALFA لهذا الغرض

### العامل الحاسم: التوافق مع mac80211

يعتمد دعم محوّل USB WiFi لوضعَي IBSS و 802.11s mesh على Linux اعتمادًا كليًا على بنية برنامج تشغيله. فقط **برامج التشغيل المدمجة في النواة والمبنية على mac80211** تكشف عن هذه الأوضاع. برامج التشغيل التي تُنفِّذ مكدس WiFi الخاص بها (معظم برامج Realtek خارج النواة) ببساطة لا تتضمن وظائف IBSS أو الشبكة الشبكية.

### موقف كل محوّل ALFA نشط

| الطراز | مجموعة الشرائح | برنامج التشغيل | IBSS | 802.11s Mesh | ملاحظات |
|---|---|---|---|---|---|
| **AWUS036ACM** | MT7612U | mt76x2u (in-kernel ≥ 4.19) | ✅ | ✅ | **الخيار الوحيد** |
| AWUS036ACH | RTL8812AU | rtw88 (in-kernel ≥ 6.14) | ✅ (kernel ≥ 6.14 فقط) | ❌ | برنامج تشغيل جديد في النواة؛ لا دعم لـ mesh point |
| AWUS036ACS | RTL8811AU | rtl8812au-dkms (OOK) | ❌ | ❌ | برنامج تشغيل خارج النواة؛ لا IBSS/mesh |
| AWUS036AX | RTL8832BU | rtw88 (in-kernel) | ❌ | ❌ | لا دعم لـ Raspberry Pi |
| AWUS036AXER | RTL8832BU | rtw88 (in-kernel) | ❌ | ❌ | لا دعم لـ Raspberry Pi |
| AWUS036AXM | MT7921AUN | mt7921u (in-kernel ≥ 5.18) | ❌ | ❌ | mt7921u لا يكشف عن IBSS |
| AWUS036AXML | MT7921AUN | mt7921u (in-kernel ≥ 5.18) | ❌ | ❌ | mt7921u لا يكشف عن IBSS |
| ~~AWUS036ACHM~~ | ~~MT7610U~~ | ~~mt76x0u~~ | ~~✅~~ | ~~✅~~ | **انتهى دعمه — متوقف** |
| ~~AWUS1900~~ | ~~RTL8814AU~~ | ~~OOK~~ | ~~Limited~~ | ~~❌~~ | **انتهى دعمه — متوقف** |

### ماذا يعني هذا بالنسبة لك

كان AWUS036ACHM (MT7610U) المحوّل السابق من ALFA الذي يدعم هذه الأوضاع — وهو الآن متوقف. لا يوجد محوّل USB من ALFA تحت التصنيع حاليًا يوفّر دعمًا نظيفًا وفوريًا لـ IBSS و 802.11s Mesh على Raspberry Pi.

**AWUS036ACM ليس فقط الخيار الأفضل — بل هو الخيار الوحيد في تشكيلة ALFA الحالية لهذا الغرض.**

علاوةً على ذلك، يُقدِّم AWUS036ACM:
- **AC1200 ثنائي النطاق** — يدعم IBSS/mesh على 2.4 GHz (مدى أوسع) أو 5 GHz (إنتاجية أعلى)
- **USB 3.0** — استخدام كامل لعرض النطاق الترددي على منافذ USB 3.0 في Pi 4/5
- **هوائيان RP-SMA قابلان للفصل** — يمكن الترقية إلى هوائيات اتجاهية عالية الكسب لتمديد مدى الشبكة الشبكية إلى ما هو أبعد بكثير من هوائيات 5 dBi المرفقة
- **دعم VIF** — تشغيل العمود الفقري للشبكة الشبكية ووضع AP في آنٍ واحد على محوّل واحد
- **يعمل على Raspberry Pi 3B+ و 4 و 5** — متّسق عبر جميع أجيال Pi

---

## 8. الأسئلة الشائعة واستكشاف الأخطاء

**س: يُظهر Pi الخاص بي `wlan0` فقط. أين `wlan1`؟**

تظهر واجهة AWUS036ACM بعد توصيل المحوّل. شغّل `iw dev` بعد التوصيل. إذا لم تظهر خلال 10 ثوانٍ، تحقق من `dmesg | grep -i mt76` بحثًا عن رسائل خطأ. على Raspberry Pi OS Lite، قد تحتاج إلى `sudo apt install iw` إذا لم تكن الحزمة موجودة.

---

**س: الأمر `iw dev wlan1 set type ibss` يُعيد رسالة "Device or resource busy"**

NetworkManager أو `wpa_supplicant` يشغل الواجهة. أوقفهما:
```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```
ثم أعد المحاولة. على Raspberry Pi OS مع واجهة سطح المكتب، قد يُمسك `dhcpcd` أيضًا بالواجهة — أضف `denyinterfaces wlan1` إلى `/etc/dhcpcd.conf` وأعد تشغيل `dhcpcd`.

---

**س: الأمر `iw phy phy1 interface add mesh0 type mp` يُعيد رسالة "Operation not supported"**

اسم phy للمحوّل قد لا يكون `phy1`. شغّل `iw dev` للتحقق من phy المرتبط بـ AWUS036ACM واستبدل الاسم الصحيح.

---

**س: تم إعداد IBSS لكن اختبار ping بين العقد فاشل**

تحقق من:
1. أن كلتا العقدتين على **نفس التردد بالضبط** (مثلًا، كلاهما على `5180`، وليس واحدة على `5180` والأخرى على `5200`)
2. أن لكل عقدة **عنوان IP مختلف** في نفس الشبكة الفرعية
3. عدم وجود جدار ناري يحجب ICMP — تحقق من `sudo iptables -L`
4. شغّل `iw dev wlan1 link` للتأكد من تطابق معرّف خلية IBSS (BSSID) على كلتا العقدتين

---

**س: واجهة mesh0 تختفي بعد إعادة التشغيل**

الواجهات الافتراضية المُنشأة بـ`iw` لا تبقى عبر إعادة التشغيل. استخدم خدمة systemd الموضحة في [القسم 5](#making-80211s-mesh-persistent) لإعادة إنشائها تلقائيًا.

---

**س: هل يمكنني استخدام تشفير WPA2 عبر IBSS؟**

WPA2-Personal (PSK) القياسي غير مدعوم في وضع IBSS بواسطة نواة Linux. للـ IBSS الآمن، يمكنك استخدام تشفير طبقة التطبيقات (WireGuard، OpenVPN، أو نفق SSH). شبكة 802.11s mesh تدعم SAE (مصادقة بأسلوب WPA3) مع `wpa_supplicant`.

---

**س: هل يمكن أن يعمل AWUS036ACM في وضعَي IBSS و managed في آنٍ واحد؟**

نعم — هذا ما صُمِّم من أجله VIF (Virtual Interface). يمكنك إبقاء `wlan1` في وضع managed متصلًا بالراوتر المنزلي للوصول إلى الإنترنت، مع إضافة واجهة افتراضية ثانية في وضع IBSS أو mesh لشبكة Pi إلى Pi:

```bash
# wlan1 stays as managed (internet)
# Add second interface for IBSS
sudo iw phy phy1 interface add adhoc0 type ibss
sudo ip link set adhoc0 up
sudo iw dev adhoc0 ibss join LocalNet 5180
sudo ip addr add 192.168.88.1/24 dev adhoc0
```

---

**س: ما هو أقصى مدى يمكن تحقيقه؟**

مع هوائيات 5 dBi المرفقة، توقّع 20–50 م في الخارج في الهواء المفتوح على 5 GHz، و50–100 م على 2.4 GHz. باستبدال الهوائيات بهوائيات RP-SMA اتجاهية عالية الكسب (متوفرة بشكل منفصل)، يمكن تمديد المدى إلى عدة مئات من الأمتار في ظروف خط الرؤية المباشر. موصلات RP-SMA على AWUS036ACM هي مقاس قياسي ومتوافقة مع مجموعة واسعة من هوائيات الجهات الأخرى.

---

**س: هل يعمل هذا على Raspberry Pi Zero 2W؟**

نعم — Raspberry Pi Zero 2W يمتلك منفذ USB-A كامل الحجم (عبر محوّل OTG) ويعمل بنظام Raspberry Pi OS بنواة تفوق 4.19 بكثير. يعمل AWUS036ACM هناك، لكن لاحظ أن منفذ USB في Zero 2W يعمل بـ USB 2.0 فقط، مما يحدّ عرض النطاق الترددي إلى حوالي 300–400 Mbps عمليًا. لحركة مرور التحكم في IBSS/mesh وبيانات المستشعرات، هذا أكثر من كافٍ.

---

## 9. أين تشتري

يتوفر ALFA AWUS036ACM من [yupitek.com](https://yupitek.com) — الموزّع الرسمي المعتمد لـ ALFA Network. الشراء عبر موزّع معتمد يضمن الحصول على أجهزة أصلية مع الضمان القياسي من Alfa Network Inc.

**صفحة المنتج:** [ALFA AWUS036ACM على Yupitek](https://yupitek.com)

محتويات الصندوق:
- 1× محوّل AWUS036ACM
- 2× هوائي ثنائي النطاق 5 dBi قابل للفصل (RP-SMA)
- 1× كابل تمديد USB 3.0
- 1× قرص برامج التشغيل (Windows)

هل أنت مهتم بهذا المنتج؟ [تواصل معنا](/ar/contact/) للحصول على عروض الأسعار.

---

## ملخص

| الميزة | AWUS036ACM |
|---|---|
| مجموعة الشرائح | MediaTek MT7612U |
| WiFi | AC1200 (867 + 300 Mbps)، ثنائي النطاق |
| IBSS Ad Hoc | ✅ جميع إصدارات Raspberry Pi OS من 2020 |
| 802.11s Mesh | ✅ تشغيل فوري |
| برنامج التشغيل المدمج في النواة | ✅ mt76x2u (منذ النواة 4.19) |
| تشغيل فوري على Pi | ✅ لا حاجة لأي تثبيت |
| هوائيات قابلة للفصل | ✅ 2× 5 dBi RP-SMA |
| الطراز الوحيد النشط من ALFA الذي يدعم IBSS + Mesh | ✅ نعم |

إذا كنت بحاجة إلى بناء شبكة لاسلكية بين عقد Raspberry Pi — سواء كانت رابطًا مباشرًا بين جهازين أو شبكة شبكية ذاتية الإصلاح متعددة القفزات — فإن ALFA AWUS036ACM هو المحوّل الذي يجعل ذلك حقيقةً.

---

*مقال بقلم الفريق التقني في Yupitek · [yupitek.com](https://yupitek.com)*

*المراجع: [التوثيق الرسمي لـ Alfa Network](https://docs.alfa.com.tw/Product/AWUS036ACM/) · [Linux Wireless Wiki — أنواع الواجهات](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif) · [برنامج تشغيل MediaTek mt76 لـ Linux](https://wireless.wiki.kernel.org/en/users/drivers/mediatek) · [قائمة morrownr للمحوّلات المدمجة في النواة](https://github.com/morrownr/USB-WiFi)*
