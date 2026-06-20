---
title: "بطاقات ALFA اللاسلكية على Apple Mac (2026): التقرير الشامل للتوافق مع M1/M2/M3/M4 و Intel"
description: "دليل توافق شامل لاستخدام محولات ALFA Network اللاسلكية USB على Apple Mac (MacBook وMacBook Pro وMacBook Air وMac Mini وMac Studio) مع معالجات Intel و Apple Silicon M1/M2/M3/M4. تعرف على بطاقات ALFA المتوافقة، ولماذا لا يدعم Apple Silicon أي بطاقة بشكل أصلي، وكيفية تفعيل وضع المراقبة عبر جهاز افتراضي Linux."
keywords: "بطاقة ALFA اللاسلكية Mac، توافق ALFA macOS، محول ALFA Apple Silicon، محول USB WiFi M1 M2 M3 M4، ALFA Network MacBook، وضع المراقبة Mac، AWUS036ACH Mac، AWUS036ACM Mac، ALFA Network Mac Mini، اختبار الاختراق Apple Silicon"
author: "فريق الدعم الفني Yupitek"
date: "2026-06-20"
category: "دليل تقني"
tags: ["Wireless Security", "ALFA Network", "Apple Mac", "Penetration Testing", "macOS Compatibility"]
---

# بطاقات ALFA اللاسلكية على Apple Mac (2026): التقرير الشامل للتوافق مع M1/M2/M3/M4 و Intel

إذا كنت تستخدم Apple Mac — سواء كان MacBook Pro بمعالج M3 Max، أو Mac Studio بمعالج M2 Ultra، أو Mac Mini المبني على Intel — وتريد استخدام محول ALFA Network اللاسلكي لتدقيق Wi-Fi، أو وضع المراقبة، أو حقن الحزم، فأنت بحاجة إلى الإجابة الحاسمة على سؤال واحد: **أي بطاقة ALFA تعمل على أي Mac؟**

إليك الإجابة المختصرة:

> **أجهزة Mac التي تعمل بـ Apple Silicon (M1/M2/M3/M4): لا تعمل أي بطاقة ALFA اللاسلكية بشكل أصلي على macOS.** هذا قيد معماري — إضافات النواة الخاصة بـ macOS من Realtek هي ملفات ثنائية x86_64 لا يمكن تحميلها على نواة ARM64. لا يوجد إصلاح، ولا يخطط أي مورد لتغيير ذلك.
>
> **أجهزة Mac التي تعمل بـ Intel: دعم محدود، اتصال عميل فقط.** تحتوي إصدارات macOS 10.11–10.15 على برامج تشغيل رسمية جزئية، لكن **وضع المراقبة وحقن الحزم غير مدعومَين على macOS** — برامج التشغيل ببساطة لا تُطبّق هذه الميزات.
>
> **الحل الفعّال:** شغّل Kali Linux ARM في جهاز افتراضي (UTM/Parallels/VMware) مع تمرير USB على جهاز Mac Apple Silicon. يعمل وضع المراقبة وحقن الحزم بشكل مثالي داخل الجهاز الافتراضي Linux.

يوفر هذا الدليل مصفوفة التوافق الكاملة، ويشرح الأسباب التقنية الستة لعدم قدرة Apple Silicon على دعم بطاقات ALFA بشكل أصلي، ويرشدك خطوة بخطوة خلال إعداد الجهاز الافتراضي الذي يعمل فعلاً.

---

## 1. مصفوفة التوافق: أي بطاقة ALFA تعمل على أي Mac؟

هذا الجدول هو المرجع الشامل. يُقيّم جميع محولات ALFA اللاسلكية الـ 9 المتاحة حالياً (غير المتوقفة عن الإنتاج) من [خط منتجات ALFA لدى Yupitek](https://yupitek.com/en/products/alfa/) وفق أربعة سيناريوهات نشر.

### 1.1 مصفوفة التوافق الكاملة

| موديل ALFA | الشريحة | Apple Silicon (macOS أصلي) | Mac Intel (macOS أصلي) | VM + تمرير USB (Kali ARM) | Raspberry Pi + Kali |
|:---|:---|:---:|:---:|:---:|:---:|
| **AWUS036ACH** | Realtek RTL8812AU | ❌ | ⚠️ عميل فقط (≤10.15) | ✅ أفضل مراقبة/حقن | ✅ |
| **AWUS036ACM** | MediaTek MT7612U | ❌ | ⚠️ عميل فقط (≤10.12) | ✅ Plug & Play | ✅ Plug & Play |
| **AWUS036AXML** | MediaTek MT7921AUN | ❌ | ❌ | ✅ Wi-Fi 6E | ✅ |
| **AWUS036AXM** | MediaTek MT7921AUN | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACHM** | MediaTek MT7610U | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACS** | Realtek RTL8811AU | ❌ | ⚠️ عميل فقط (≤10.14) | ✅ | ✅ |
| **AWUS036AX** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ محدود | ⚠️ محدود |
| **AWUS036AXER** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ محدود | ⚠️ محدود |
| **AWUS036EACS** | Realtek RTL8821CU | ❌ | ⚠️ عميل فقط | ❌ لا يوجد وضع مراقبة | ⚠️ غير موصى به |

**المفتاح:** ✅ = يعمل بشكل موثق | ⚠️ = محدود / يتطلب شروطاً | ❌ = غير مدعوم

### 1.2 الحكم السريع حسب معالج Mac

| معالج Mac | هل يمكنني استخدام بطاقات ALFA على macOS؟ | هل يمكنني استخدام وضع المراقبة؟ | الحل الموصى به |
|:---|:---|:---|:---|
| **Apple Silicon M1/M2/M3/M4** | ❌ لا — قيد معماري | ❌ ليس على macOS | ✅ Linux VM مع تمرير USB |
| **Intel (macOS 10.11–10.15)** | ⚠️ محدود — عميل فقط، بلا وضع مراقبة | ❌ غير مدعوم | ✅ Linux VM مع تمرير USB |
| **Intel (macOS 11+)** | ⚠️ kext خارجي فقط (chris1111) | ❌ غير مدعوم | ✅ Linux VM مع تمرير USB |

> [!IMPORTANT]
> **الخلاصة:** بغض النظر عن الـ Mac الذي تمتلكه، **وضع المراقبة وحقن الحزم يتطلبان Linux**. نهج VM + تمرير USB هو الحل الشامل الذي يعمل على كل Mac، من MacBook Pro Intel 2012 إلى Mac Studio M4 2025.

---

## 2. لماذا يفشل Apple Silicon: الجدار المعماري المكوّن من 6 طبقات

إذا كنت تتساءل عما إذا كان تحديث macOS مستقبلي قد يُصلح هذا — لن يفعل. عدم التوافق ليس خطأً ينتظر التصحيح. إنه النتيجة التراكمية لـ **ستة قرارات تصميم متعمدة من Apple** تجعل محولات USB Wi-Fi من الجهات الخارجية مستحيلة معماريًا على Apple Silicon.

### الطبقة 1: IO80211Controller واجهة برمجية خاصة

لم تنشر Apple قط واجهة برمجة النواة (KPI) لبرامج تشغيل Wi-Fi الأصلية. تبدو التسلسل الهرمي للفئات هكذا:

```
IOService
  └─ IONetworkController
       └─ IOEthernetController        ← KPI عامة
            └─ IO80211Controller      ← خاصة (Apple الداخلية فقط)
```

كان الموردون من الجهات الخارجية تاريخيًا يرثون مباشرة من `IOEthernetController`، ولهذا تظهر محولات USB Wi-Fi على macOS كواجهات "Ethernet" بدلاً من الاندماج مع أيقونة Wi-Fi في شريط القائمة أو AirDrop أو Sidecar أو Find My.

### الطبقة 2: NetworkingDriverKit يدعم Ethernet فقط

بديل Apple الحديث لإضافات النواة هو **DriverKit** — برامج تشغيل في مساحة المستخدم لا تخاطر باستقرار النواة. تُصرّح عائلة الشبكات `NetworkingDriverKit` صراحةً في [توثيق Apple الرسمي](https://developer.apple.com/documentation/networkingdriverkit):

> "استخدم NetworkingDriverKit لتطوير برامج تشغيل لمحولات Ethernet USB. لاحظ أن **Ethernet هو واجهة الشبكة الوحيدة التي يدعمها NetworkingDriverKit حالياً.**"

لا توجد فئة `IOUserNetworkWiFi`. لا يوجد إطار عمل Wi-Fi DriverKit. حتى لو استثمرت Realtek أو MediaTek جهدًا هندسيًا لكتابة برنامج تشغيل DriverKit، **لا يوجد إطار عمل Apple للاتصال به**.

### الطبقة 3: مزيج USB + kext الشبكات غير مدعوم منذ Big Sur

تُفيد صفحة [إضافات النواة المهجورة](https://developer.apple.com/support/kernel-extensions/) من Apple:

> "مزيج استخدام KPIs IONetworkingFamily وأي USB KPI (IOUSBHostFamily أو IOUSBFamily) **غير مدعوم في macOS Big Sur**."

هذا هو بالضبط مزيج KPI الذي تتطلبه كل إضافة نواة USB Wi-Fi. المنفذ الوحيد هو تعطيل SIP بالكامل أو استخدام ملفات تعريف MDM — لا يصلح أي منهما للمنتجات الاستهلاكية.

### الطبقة 4: kext من Realtek مخصص لـ x86_64 فقط

يُشحن برنامج تشغيل macOS من Realtek كـ `RtWlanU.kext`، مُصرَّف حصرياً لـ **x86_64**. تعمل أجهزة Mac Apple Silicon على نواة **ARM64**. تُنفَّذ إضافات النواة في فضاء النواة — **لا يستطيع Rosetta 2 ترجمة إضافات النواة**.

وثّق مستخدم في [نقاش chris1111 #128](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter/discussions/128) الفشل الدقيق على M1 MacBook Air مع Ventura 13.1 وبطاقة ALFA AWUS1900:

```
Domain=KMErrorDomain Code=71
Incompatible architecture: Binary is for x86_64, but needed arm64
Kext com.realtek.driver.RtWlanU v1830.32.b27
```

### الطبقة 5: Realtek تخلت عن تطوير برنامج تشغيل macOS

يُصرّح القائم على صيانة [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) — التوزيع المجتمعي الفعلي لبرامج تشغيل Wi-Fi لـ macOS من Realtek — صراحةً في ملف README:

> **"يبدو أنه لا يعمل على Mac M1 وM2 وM3 وM4 بشريحة Apple، ويعمل فقط مع Mac Intel."**

وردًا على سؤال مستخدم عمّا إذا كان يمكن إضافة دعم M1:

> "يجب إعادة كتابة إضافات kext القديمة لأجهزة Mac M1 (لن تعمل حتى عبر Rosetta 2)، مما يعني أن الأمر متروك للشركات الكبرى لتحديث برامج تشغيلها لدعم M1."

لم تُصدر Realtek أي kext بنظام arm64، ولا برنامج تشغيل DriverKit، ولا أي خطة عامة لدعم Apple Silicon. الحافز الاقتصادي ضئيل: كل Mac Apple Silicon يحتوي بالفعل على Wi-Fi مدمج.

### الطبقة 6: تحميل kext على Apple Silicon معادٍ بتصميم متعمد

حتى لو وجد kext بنظام arm64، فإن تحميله على Apple Silicon يتطلب:

1. إيقاف تشغيل Mac
2. **الضغط مع الاستمرار** على زر الطاقة حتى تظهر خيارات التمهيد
3. الدخول إلى وضع One True Recovery (1TR)
4. تخفيض مستوى الأمان إلى **مستوى مخفَّض**
5. تمكين "السماح بإدارة المستخدم لإضافات النواة من مطورين معرَّفين"
6. إعادة التشغيل، تثبيت kext، الموافقة عليه في إعدادات النظام
7. **إعادة التشغيل مرة أخرى** لإعادة بناء Auxiliary Kernel Collection (AuxKC)

وفقًا لدليل Apple [توسيع النواة بأمان](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web)، هذا المسار معقّد بشكل متعمد: "يجعل مزيج متطلبات 1TR وكلمة المرور من الصعب على المهاجمين البرمجيين المبتدئين من داخل macOS حقن kexts."

> [!IMPORTANT]
> **الخلاصة:** لا تعمل أي بطاقة ALFA — ولا أي محول USB Wi-Fi من أي شركة مصنعة — بشكل أصلي على Apple Silicon macOS. لن يتغير ذلك ما لم تنشر Apple إطار عمل Wi-Fi DriverKit (لم تفعل) وتكتب شركة ما برنامج تشغيل له (لم يفعل أحد).

---

## 3. Mac Intel: ما الذي لا يزال يعمل (وما لا يعمل)

إذا كان فريقك لا يزال يستخدم أجهزة Mac Intel، فالوضع أفضل — لكن فقط للاتصال الأساسي بـ Wi-Fi، ليس لتدقيق الأمن.

### 4.1 الجدول الزمني لدعم إصدارات macOS

| موديل ALFA | الشريحة | الحد الرسمي لـ macOS | برنامج التشغيل المجتمعي (chris1111) |
|------------|---------|---------------------|------------------------------|
| AWUS036ACH | RTL8812AU | 10.15 Catalina | 11 Big Sur – 26 Tahoe (Intel فقط) |
| AWUS036ACS | RTL8811AU | 10.14 Mojave | 11 Big Sur – 26 Tahoe (Intel فقط) |
| AWUS036ACM | MT7612U | **10.12 Sierra** | ❌ غير مدعوم (MediaTek) |
| AWUS036ACHM | MT7610U | ❌ لا يوجد | ❌ غير مدعوم (MediaTek) |
| AWUS036AX/AXER | RTL8832BU | ❌ لا يوجد | ❌ لا يوجد |
| AWUS036AXML/AXM | MT7921AUN | ❌ لا يوجد | ❌ لا يوجد |

### 4.2 مفارقة وضع المراقبة

ها هي المشكلة الحرجة لمحترفي الأمن: **حتى عندما يُثبَّت برنامج التشغيل بنجاح على أجهزة Mac Intel، لا يعمل وضع المراقبة وحقن الحزم.**

تُطبّق برامج تشغيل macOS من ALFA الاتصال كعميل فقط — ولا تُطبّق واجهات برمجة تطبيقات وضع المراقبة. تأكد ذلك في [نقاش على Superuser](https://superuser.com/questions/1597114/alfa-wifi-network-card-monitor-mode-on-mac-os) حيث نجح مستخدم في تثبيت برنامج تشغيل AWUS036EAC لكنه لم يتمكن من الدخول في وضع المراقبة:

> *"ما الذي يجعلك تعتقد أن ALFA أدرجت دعم وضع المراقبة في برنامج تشغيلها لـ macOS؟ واجهات برمجة وضع المراقبة مختلفة في أنظمة التشغيل المختلفة. أفترض أنهم لم يكلفوا أنفسهم عناء تطبيقها لـ macOS."*

يخلق هذا مفارقة: **تشتري بطاقة ALFA خصيصًا لوضع المراقبة وحقن الحزم، لكن برامج تشغيل macOS لا تدعم أياً منهما.** بطاقة Wi-Fi المدمجة في Mac تدعم وضع المراقبة فعلاً (عبر أداة `airport`)، لكن برامج تشغيل ALFA لا تُطبّق ذلك لأجهزتها.

> [!WARNING]
> إذا كان هدفك تدقيق أمن الشبكات اللاسلكية (وضع المراقبة، حقن الحزم، التقاط المصافحة، هجمات deauth)، **لا يستطيع macOS فعل ذلك — على أي Mac، Intel أو Apple Silicon، مع أي بطاقة ALFA.** أنت بحاجة إلى Linux.

### 4.3 برنامج تشغيل chris1111: الملاذ الأخير لأجهزة Mac Intel

بالنسبة لأجهزة Mac Intel التي تعمل بـ macOS 11 Big Sur أو أحدث، الخيار الوحيد هو مشروع [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) — التوزيع المجتمعي لـ kext من Realtek.

**المتطلبات:**
- Mac Intel فقط (ليس Apple Silicon)
- يجب تعطيل System Integrity Protection (SIP)
- الـ kext غير موقّع من Realtek/ALFA/Apple

**البطاقات المدعومة:** AWUS036ACH (RTL8812AU) وAWUS036ACS (RTL8811AU) فقط.

تُحذّر Rokland (الموزع الأمريكي لـ ALFA) [بشدة](https://store.rokland.com/blogs/news/apple-mac-os-11-big-sur-compatibility-update-for-alfa-awus036ach-other-products): *"نوصي بشدة بعدم استخدام برنامج التشغيل هذا إذا كان جهاز Mac الخاص بك هو حاسوبك الرئيسي والحيوي لعملك."*

---

## 4. الحل الفعّال: VM + تمرير USB

بما أن macOS لا يستطيع تشغيل بطاقات ALFA بشكل أصلي (وحتى لو استطاع، لن يعمل وضع المراقبة)، فإن الحل العملي لفِرق الأمن المعتمدة على Mac هو تشغيل **Linux في جهاز افتراضي** وتمرير بطاقة ALFA عبر USB.

يعمل هذا النهج على **جميع أجهزة Mac Apple Silicon** (M1/M2/M3/M4) وجميع أجهزة Mac Intel. يعمل وضع المراقبة وحقن الحزم بشكل مطابق لجهاز Linux أصلي.

### 5.1 ما ستحتاج إليه

| المكون | التوصية | التكلفة |
|-----------|---------------|---------|
| برنامج VM | [UTM](https://mac.getutm.app/) (مجاني، مفتوح المصدر) | مجاني |
| بديل | Parallels Desktop أو VMware Fusion (ARM) | 99 دولار/سنة |
| ISO Linux | [Kali Linux ARM64](https://www.kali.org/get-kali/) | مجاني |
| بطاقة ALFA | AWUS036ACH (الأفضل) أو AWUS036ACM (Plug & Play) | 40–70 دولار |
| محول USB | محول USB-C إلى USB-A (إذا كانت بطاقة ALFA ذات قابس USB-A) | 10 دولار |

### 5.2 الإعداد خطوة بخطوة

#### الخطوة 1: إنشاء VM لـ Kali Linux ARM

نزّل مثبّت Kali Linux ARM64 وأنشئ VM جديداً في UTM:
- **المعمارية:** ARM64 (aarch64)
- **ذاكرة RAM:** 2 جيجابايت كحد أدنى (4 جيجابايت موصى به)
- **المعالج:** نواتان أو أكثر
- **متحكم USB:** USB 3.0 (xHCI) — **هذا أمر بالغ الأهمية**

> [!IMPORTANT]
> يجب تهيئة متحكم USB للـ VM كـ **USB 3.0 (xHCI)**، وليس USB 2.0. تُسبب متحكمات USB 2.0 قطع اتصال متقطع مع بطاقات ALFA عالية الطاقة، خاصةً أثناء حقن الحزم.

#### الخطوة 2: تثبيت برنامج تشغيل ALFA داخل الـ VM

**لبطاقة AWUS036ACH (RTL8812AU):**

إذا كانت نواة Kali لديك **≥6.14**، فإن برنامج التشغيل الرئيسي `rtw88` مُضمَّن بالفعل — لا حاجة للتثبيت. للنوى الأقدم:

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) git
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
```

**لبطاقة AWUS036ACM (MT7612U) — تثبيت صفري:**

برنامج تشغيل MediaTek MT7612U مُضمَّن في نواة Linux منذ الإصدار 4.19. وصّله وسيعمل:

```bash
lsusb
# Bus 001 Device 005: ID 0e8d:7612 MediaTek Inc.

iw dev
# يجب أن يظهر wlan0 تلقائياً
```

**لبطاقتَي AWUS036AXML / AWUS036AXM (MT7921AUN):**

في النواة منذ Linux 5.18، لكنه يتطلب ملفات البرامج الثابتة:

```bash
sudo apt install -y firmware-misc-nonfree
# التحقق من وجود البرامج الثابتة:
ls /lib/firmware/mediatek/
# WIFI_MT7922_patch_mcu_1_1_hdr.bin
# WIFI_RAM_CODE_MT7922_1.bin
```

#### الخطوة 3: تهيئة تمرير USB

1. وصّل بطاقة ALFA بمنفذ USB-C/Thunderbolt الخاص بـ Mac (استخدم محول USB-C إلى USB-A إذا لزم الأمر)
2. في UTM: شريط قائمة VM → USB → حدد جهاز ALFA → خصّصه للـ VM
3. في Parallels: إعدادات VM → الأجهزة → USB والبلوتوث → تحقق من "USB 3.0" → خصّص جهاز ALFA للـ VM

#### الخطوة 4: التحقق من وضع المراقبة وحقن الحزم

```bash
# تحقق من التعرف على الجهاز داخل الـ VM
lsusb
# Bus 003 Device 005: ID 0bda:8812 Realtek ... RTL8812AU

# تفعيل وضع المراقبة
sudo airmon-ng start wlan0
# (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)

# التأكد من تفعيل وضع المراقبة
iw dev wlan0mon info
# Mode: monitor

# اختبار قدرة حقن الحزم
sudo aireplay-ng --test wlan0mon
# "Injection is working!" يؤكد النجاح
```

### 5.3 المشكلات المعروفة واستكشاف الأخطاء

| المشكلة | السبب | الحل |
|-------|-------|----------|
| انقطاع الاتصال أثناء الفحص المكثف | خطأ تبديل وضع USB 3.0 (morrownr/USB-WiFi #676) | استخدم محور USB 2.0 بين البطاقة والـ Mac |
| `airmon-ng` لا يرى البطاقة | متحكم USB خاطئ في إعدادات الـ VM | اضبط USB الـ VM على USB 3.0 (xHCI) بدلاً من USB 2.0 |
| برنامج التشغيل لا يُصرَّف في الـ VM | رؤوس النواة مفقودة | `sudo apt install linux-headers-$(uname -r)` |
| البطاقة معروفة لكن لا يوجد وضع مراقبة | شريحة RTL8832BU (AWUS036AX/AXER) | هذه الشريحة ذات دعم محدود لوضع المراقبة؛ استخدم AWUS036ACH بدلاً منها |

### 5.4 البديل: Raspberry Pi كعقدة اختبار اختراق مخصصة

للفرق التي تفضل حلاً مخصصاً للأجهزة، يُعدّ **Raspberry Pi 4 أو 5** الذي يعمل بـ Kali Linux عقدةً محمولة ممتازة لتدقيق الشبكات اللاسلكية. يُستخدم Mac فقط كطرفية SSH.

**المزايا:**
- يتجاوز مشكلات برامج تشغيل macOS تمامًا
- AWUS036ACM يعمل بالتوصيل والتشغيل على Pi (برنامج تشغيل مدمج في النواة، تثبيت صفري)
- التكلفة: Pi 5 + بطاقة ALFA أقل من 200 دولار
- محمول ولا يؤثر على جهاز العمل الرئيسي

```bash
# من جهاز Mac الخاص بك، اتصل بـ Pi عبر SSH:
ssh kali@192.168.1.100

# شغّل تدقيق الشبكة اللاسلكية على Pi:
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
sudo aireplay-ng --test wlan1mon
```

---

## 5. دليل أجهزة USB: أي منفذ تستخدم على أي Mac

بطاقات ALFA هي أجهزة USB 2.0 أو USB 3.0، عادةً مع موصل USB-A، تستهلك ما بين 500 مللي أمبير (2.5 واط) و900 مللي أمبير (4.5 واط). لا توفر جميع منافذ USB في Mac طاقة كافية — وللـ Mac Mini M4 (2024) ميزة خاصة حرجة تحتاج معرفتها.

### 6.1 مرجع طاقة منافذ USB في Mac

| طراز Mac | منافذ USB-A | طاقة USB-A | منافذ USB-C/TB | طاقة USB-C | توصيل ALFA مباشر؟ |
|-----------|-------------|-------------|----------------|-------------|-------------------|
| MacBook 12" (2015–2017) | ❌ لا يوجد | N/A | 1× USB-C 3.1 Gen 1 | 900 مللي أمبير | ❌ يلزم محول |
| MacBook Air Intel (2010–2017) | ✅ 2× | 900 مللي أمبير | 1× TB1/TB2 | N/A | ✅ مباشر |
| MacBook Air Intel (2018–2020) | ❌ لا يوجد | N/A | 2× TB3 | 15 واط / 7.5 واط | ❌ يلزم محول |
| MacBook Air M1/M2/M3 | ❌ لا يوجد | N/A | 2× TB/USB 4 | 15 واط / 7.5 واط | ❌ يلزم محول |
| MacBook Pro Intel (2012–2015) | ✅ 2× | 900 مللي أمبير | 2× TB2 | N/A | ✅ مباشر (أفضل حقبة) |
| MacBook Pro Intel (2016–2019) | ❌ لا يوجد | N/A | 4× TB3 | 15 واط / 7.5 واط | ❌ يلزم محول |
| MacBook Pro M1 (2020) | ❌ لا يوجد | N/A | 2× TB/USB 4 | 15 واط / 7.5 واط | ❌ يلزم محول |
| MacBook Pro M1 Pro/Max (2021+) | ❌ لا يوجد | N/A | 3× TB4 | 15 واط لكل منفذ | ❌ يلزم محول |
| MacBook Pro M2/M3/M4 Pro/Max | ❌ لا يوجد | N/A | 3× TB4 أو TB5 | 15 واط+ لكل منفذ | ❌ يلزم محول |
| Mac Mini Intel (2014) | ✅ 4× | 900 مللي أمبير | 2× TB2 | N/A | ✅ مباشر |
| Mac Mini Intel (2018) | ✅ 2× | 900 مللي أمبير | 4× TB3 | 15 واط / 7.5 واط | ✅ مباشر |
| Mac Mini M1 (2020) | ✅ 2× | 900 مللي أمبير | 2× TB/USB 4 | 15 واط / 7.5 واط | ✅ مباشر |
| Mac Mini M2/M2 Pro (2023) | ✅ 2× | 900 مللي أمبير | 2–4× TB4 | 15 واط لكل منفذ | ✅ مباشر |
| **Mac Mini M4/M4 Pro (2024)** | **❌ لا يوجد** | **N/A** | أمامي: 2× USB-C / خلفي: 3× TB4 أو TB5 | **أمامي: 500 مللي أمبير / خلفي: 900 مللي أمبير+** | **❌ المنافذ الخلفية TB فقط** |
| Mac Studio (جميع الأجيال) | ✅ 2× (خلفي) | 900 مللي أمبير | 4× TB4 أو TB5 (خلفي) | 15 واط لكل منفذ | ✅ مباشر |

### 6.2 تحذير حرج: Mac Mini M4 (2024)

Mac Mini M4/M4 Pro هو **أول Mac Mini بلا منافذ USB-A**. الأهم من ذلك، أن منفذَي USB-C الأماميين يوفران فقط **~500 مللي أمبير** — غير كافٍ لبطاقات ALFA USB 3.0 التي تتطلب 900 مللي أمبير.

> [!WARNING]
> على Mac Mini M4، **وصّل دائماً بطاقات ALFA في منافذ Thunderbolt 4/5 الخلفية** باستخدام محول USB-C إلى USB-A. ستُسبب منافذ USB-C الأمامية (500 مللي أمبير) عدم استقرار في الطاقة وانقطاع الاتصال مع بطاقات ALFA عالية الطاقة.

### 6.3 قواعد توزيع طاقة Thunderbolt

- **Thunderbolt 3 (أجهزة Mac Intel، 2016–2020):** 15 واط (3 أمبير) للمنفذين الأولين، 7.5 واط (1.5 أمبير) للمنافذ الإضافية — وفق مبدأ "الأول فالأول". وصّل بطاقة ALFA أولاً للحصول على 15 واط كاملة.
- **Thunderbolt 4 (Apple Silicon، 2021+):** 15 واط (3 أمبير) لكل منفذ — بلا حدود توزيع.
- **منافذ USB-A (جميع أجهزة Mac التي تمتلكها):** دائماً 900 مللي أمبير (مواصفة USB 3.0) — كافٍ لأي بطاقة ALFA.

---

## 6. توصيات الشراء حسب حالة الاستخدام

### 7.1 لمستخدمي Mac Apple Silicon (M1/M2/M3/M4)

| حالة الاستخدام | البطاقة الموصى بها | لماذا | طريقة الإعداد |
|----------|-----------------|-----|--------------| 
| **أفضل وضع مراقبة وحقن** | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | RTL8812AU — المعيار الذهبي لـ Kali Linux، أنضج برنامج تشغيل | VM + تمرير USB |
| **أفضل تجربة Plug & Play** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | MT7612U — في النواة منذ Linux 4.19، تثبيت صفري | VM + تمرير USB |
| **اختبار WiFi 6E / 6 جيجاهرتز** | [AWUS036AXML](https://yupitek.com/en/products/alfa/awus036axml/) | MT7921AUN — في النواة منذ Linux 5.18، ثلاثي النطاق + BT 5.2 | VM + تمرير USB |
| **ميزانية محدودة / مبتدئ** | [AWUS036ACS](https://yupitek.com/en/products/alfa/awus036acs/) | RTL8811AU — بأسعار معقولة، يدعم وضع المراقبة + الحقن | VM + تمرير USB |
| **عقدة محمولة مخصصة** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | تثبيت صفري على Raspberry Pi، استهلاك طاقة منخفض (600 مللي أمبير) | Raspberry Pi + Kali |

### 7.2 لمستخدمي Mac Intel (اتصال عميل فقط)

| إصدار macOS | البطاقة الموصى بها | طريقة برنامج التشغيل | القيد |
|---------------|-----------------|---------------|------------|
| 10.15 Catalina أو أقدم | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | برنامج التشغيل الرسمي من ALFA | عميل فقط — لا وضع مراقبة |
| 11 Big Sur أو أحدث | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | [برنامج تشغيل chris1111](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) (تعطيل SIP) | عميل فقط — لا وضع مراقبة |

> [!IMPORTANT]
> لتدقيق أمن الشبكات اللاسلكية على **أي** Mac (Intel أو Apple Silicon)، لا تزال بحاجة إلى Linux — إما في VM أو على Raspberry Pi. برامج تشغيل macOS لا تدعم وضع المراقبة أو حقن الحزم.

### 7.3 البطاقات التي يجب تجنبها لمستخدمي Mac

| البطاقة | سبب التجنب |
|------|-----------| 
| AWUS036AX / AWUS036AXER (RTL8832BU) | دعم محدود وغير مستقر لوضع المراقبة في Linux؛ لا يوجد برنامج تشغيل macOS |
| AWUS036EACS (RTL8821CU) | **لا تدعم** وضع المراقبة مطلقاً — غير مناسبة لتدقيق الأمن |
| AWUS036ACHM (MT7610U) | لا يوجد برنامج تشغيل macOS (chris1111 لا يدعم MediaTek)؛ يتطلب التصريف على Linux |

---

## 7. الأسئلة الشائعة: بطاقات ALFA اللاسلكية على Apple Mac

> [!NOTE]
> هذا القسم من الأسئلة الشائعة مهيكل لتحسين محركات الإجابة (AEO). تُجاب كل سؤال بشكل حاسم في الجملة الأولى حتى تتمكن محركات البحث المدعومة بالذكاء الاصطناعي (ChatGPT وPerplexity وGoogle AI Overviews) من الاستشهاد بهذه الإجابات مباشرةً.

### هل يعمل ALFA AWUS036ACH على Mac M1/M2/M3/M4؟

**لا.** لا يعمل AWUS036ACH (RTL8812AU) بشكل أصلي على أي Mac Apple Silicon. برنامج تشغيل macOS من Realtek مُصرَّف فقط لـ x86_64 ولا يمكن تحميله على نواة ARM64. ومع ذلك، يعمل بشكل مثالي داخل VM Linux (UTM/Parallels) مع تمرير USB، بما يشمل دعماً كاملاً لوضع المراقبة وحقن الحزم.

### هل يمكنني استخدام بطاقات ALFA اللاسلكية لوضع المراقبة على macOS؟

**لا.** برامج تشغيل macOS من ALFA لا تُطبّق وضع المراقبة أو حقن الحزم — تدعم فقط الاتصال الأساسي كعميل Wi-Fi. ينطبق هذا على جميع إصدارات macOS على أجهزة Mac Intel وApple Silicon. لوضع المراقبة، يجب استخدام Linux (إما في VM أو على جهاز منفصل مثل Raspberry Pi).

### أي بطاقة ALFA اللاسلكية هي الأفضل لمستخدمي Mac؟

لمستخدمي Mac الذين يُجرون تدقيق أمن الشبكات اللاسلكية، **AWUS036ACH** (RTL8812AU) هو الخيار الأفضل — إنه المعيار الذهبي لـ Kali Linux لوضع المراقبة وحقن الحزم. للتوصيل والتشغيل بتثبيت صفري في VM Linux، يُوصى بـ **AWUS036ACM** (MT7612U) لأن برنامج تشغيله مُدمج في نواة Linux منذ الإصدار 4.19.

### لماذا لا تعمل بطاقة ALFA على MacBook Pro M3 الخاص بي؟

تستخدم أجهزة Mac Apple Silicon (M1/M2/M3/M4) نواة ARM64 التي لا تستطيع تحميل إضافات نواة x86_64. برنامج تشغيل Wi-Fi macOS من Realtek مخصص لـ x86_64 فقط، والـ Rosetta 2 لا يستطيع ترجمة إضافات النواة. علاوة على ذلك، يدعم إطار عمل NetworkingDriverKit من Apple Ethernet فقط، وليس Wi-Fi — لذا لا يوجد مسار DriverKit حديث أيضاً. تخلت Realtek عن تطوير برنامج تشغيل macOS.

### هل يوجد محول USB Wi-Fi يعمل على Apple Silicon macOS؟

**لا.** اعتباراً من عام 2026، لا يوجد محول USB Wi-Fi من أي شركة مصنعة (ALFA أو TP-Link أو Netgear أو ASUS وغيرها) يعمل بشكل أصلي على Apple Silicon macOS. هذا قيد معماري، وليس مشكلة توفر برامج تشغيل. توصية Apple الرسمية هي استخدام راوتر سفر مع Ethernet بدلاً من ذلك.

### هل يمكنني استخدام Wi-Fi المدمج في Mac لوضع المراقبة؟

**نعم، لكن بقيود.** يدعم Wi-Fi المدمج في macOS وضع المراقبة الأساسي عبر أداة `airport` (الأمر: `sudo airport en0 sniff 11`). ومع ذلك، يلتقط على قناة واحدة فقط في كل مرة، ولا يدعم حقن الحزم، وللهوائي الداخلي نطاق محدود. لتدقيق الشبكة اللاسلكية الاحترافي، يلزم وجود محول ALFA خارجي في VM Linux.

### ما أسهل طريقة لتشغيل بطاقات ALFA على Mac؟

الطريقة الأسهل هي: تثبيت [UTM](https://mac.getutm.app/) (مجاني) → إنشاء VM لـ Kali Linux ARM → توصيل AWUS036ACM (MT7612U) → تخصيصه للـ VM عبر تمرير USB. برنامج تشغيل MT7612U مُدمج في النواة منذ Linux 4.19، لذا لا يلزم تثبيت أي برنامج تشغيل — يعمل فوراً.

### هل أحتاج إلى محور USB مزوّد بطاقة خارجية لبطاقات ALFA على Mac؟

على أجهزة Mac ذات منافذ USB-A (Mac Mini وMac Studio وأجهزة MacBook Pro/Air الأقدم)، لا — الـ 900 مللي أمبير كافٍ. على أجهزة Mac ذات منافذ USB-C/Thunderbolt فقط، الـ 15 واط (3 أمبير) أكثر من كافٍ. الاستثناء الوحيد هو منافذ USB-C الأمامية للـ Mac Mini M4 التي تُوفر 500 مللي أمبير فقط — استخدم منافذ Thunderbolt الخلفية بدلاً منها.

---

## 8. الموارد وروابط برامج التشغيل

### الموارد الرسمية

| المورد | الرابط |
|----------|-----|
| الموقع الرسمي لـ Yupitek | [https://www.yupitek.com](https://www.yupitek.com) |
| صفحة منتجات ALFA في Yupitek | [https://yupitek.com/en/products/alfa/](https://yupitek.com/en/products/alfa/) |
| الموقع الرسمي لـ ALFA Network | [https://www.alfa.com.tw](https://www.alfa.com.tw) |
| جدول مقارنة ALFA في Yupitek | [https://yupitek.com/alfa_compare.html](https://yupitek.com/alfa_compare.html) |

### مستودعات برامج تشغيل Linux (GitHub)

| الشريحة | طرازات ALFA | مستودع GitHub | نوع برنامج التشغيل |
|---------|-------------|-------------------|-------------|
| RTL8812AU | AWUS036ACH، AWUS036ACS | [morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820) | DKMS (موصى به) |
| RTL8812AU | AWUS036ACH | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) | مجتمعي (قديم) |
| RTL8812AU | AWUS036ACH | [lwfinger/rtw88](https://github.com/lwfinger/rtw88) | رئيسي (نواة ≥6.14) |
| MT7612U | AWUS036ACM | Linux في النواة (`mt76`) | في النواة (≥4.19) |
| MT7921AUN | AWUS036AXML، AWUS036AXM | Linux في النواة (`mt7921u`) | في النواة (≥5.18) |
| MT7610U | AWUS036ACHM | [imzyxwvu/mt7610u](https://github.com/imzyxwvu/mt7610u) | خارج النواة |
| RTL8832BU | AWUS036AX، AWUS036AXER | [morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi) | دعم محدود |

### برنامج تشغيل macOS (Mac Intel فقط)

| برنامج التشغيل | الرابط | macOS المدعوم | Apple Silicon |
|--------|-----|-----------------|---------------|
| chris1111 Wireless-USB-Big-Sur-Adapter | [GitHub](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) | Catalina – Tahoe 26 | ❌ Intel فقط |

### توثيق مطوري Apple

| المستند | الرابط |
|----------|-----|
| إضافات النواة المهجورة | [developer.apple.com/support/kernel-extensions/](https://developer.apple.com/support/kernel-extensions/) |
| NetworkingDriverKit (Ethernet فقط) | [developer.apple.com/documentation/networkingdriverkit](https://developer.apple.com/documentation/networkingdriverkit) |
| توسيع النواة بأمان | [support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) |

### برامج الأجهزة الافتراضية

| البرنامج | الرابط | التكلفة |
|----------|-----|---------|
| UTM | [mac.getutm.app](https://mac.getutm.app/) | مجاني |
| Parallels Desktop | [parallels.com](https://www.parallels.com/) | 99 دولار/سنة |
| VMware Fusion | [vmware.com](https://www.vmware.com/products/fusion.html) | مجاني للاستخدام الشخصي |

---

*يستند هذا المقال إلى بحوث تقنية مجمّعة من توثيق مطوري Apple، ومستودعات GitHub (chris1111، وaircrack-ng، ومorrownr)، ومواصفات منتجات ALFA Network، وتقارير مجتمع Reddit/GitHub، ووثائق الاختبارات الفعلية. جميع توصيات المنتجات مبنية على خط منتجات ALFA المتوفر حالياً في مخزون Yupitek.*

*⚠️ المعدات والتقنيات الموصوفة في هذا المقال مخصصة حصراً لعمليات تدقيق أمن المعلومات المعتمدة واختبارات الاختراق القانونية. يجب على المستخدمين التأكد من الامتثال للقوانين واللوائح المحلية.*

---
*إصدار المقال: 1.0 | 2026-06-20 | Yupitek Ltd.*
