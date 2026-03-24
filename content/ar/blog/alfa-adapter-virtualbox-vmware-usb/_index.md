---
title: "ALFA USB Passthrough: دليل إعداد VirtualBox و VMware"
description: "دليل خطوة بخطوة لإعداد USB Passthrough لمحول ALFA WiFi في VirtualBox و VMware Workstation لنظام Kali Linux. يشمل AWUS036ACH وAWUS036AXML وفلتر USB 3.0 وExtension Pack واستكشاف الأخطاء."
date: 2026-03-24
draft: false
dir: rtl
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
---

تشغيل محول ALFA WiFi داخل جهاز افتراضي ليس بالأمر البسيط الذي يكفي فيه توصيل المحول وانتظار أن يتعرف عليه نظام التشغيل الضيف تلقائياً. على عكس المجلدات المشتركة والشبكات المجسّرة، يتطلب وضع المراقبة (monitor mode) وحقن الحزم الخام (packet injection) **تحكماً كاملاً في USB** — أي يجب أن تمتلك الآلة الافتراضية الجهاز حصرياً بدلاً من مشاركته عبر مكدّس شبكة المضيف. يُسمّى هذا بـ USB Passthrough، وإعداده بشكل صحيح هو السبب الأكثر شيوعاً لفشل الإعداد لدى مختبري الاختراق ولاعبي CTF العاملين في البيئات الافتراضية.

يغطي هذا الدليل الإعداد الكامل لـ **VirtualBox 7.x** و**VMware Workstation 17+ / VMware Fusion 13+**، مستهدفاً Kali Linux كنظام تشغيل ضيف. يتناول الدليل كلاً من AWUS036ACH (شريحة RTL8812AU) والأحدث AWUS036AXML (شريحة MT7921AUN)، مع ملاحظات خاصة بكل محول عند اختلاف السلوك.

بعد الانتهاء، سيظهر محول ALFA الخاص بك داخل Kali عبر `lsusb`، وسيتم تحميل برنامج التشغيل الصحيح، وسيؤكد `airmon-ng` عمل وضع المراقبة.

---

## المتطلبات المسبقة

قبل البدء، تأكد من أن بيئتك تستوفي المتطلبات التالية. غياب أي عنصر منها — خاصة Extension Pack في VirtualBox — هو السبب الجذري لمعظم حالات فشل الـ passthrough.

| المتطلب | التفاصيل |
|---|---|
| **برنامج المحاكاة الافتراضية** | VirtualBox 7.x + Extension Pack **أو** VMware Workstation 17+ / Fusion 13+ |
| **نظام التشغيل الضيف** | Kali Linux 2024.x أو أحدث (تم الاختبار على 2024.1 حتى 2025.1) |
| **محول ALFA** | AWUS036ACH أو AWUS036AXML أو AWUS036ACM أو أي جهاز RTL8812AU / MT7921AUN |
| **منفذ USB بالمضيف** | يُوصى بـ USB 3.0 (خاصة لـ AWUS036AXML) |
| **نظام تشغيل المضيف** | Windows 10/11 أو Linux أو macOS (Fusion) |
| **صلاحيات Sudo** | مطلوبة داخل VM الخاص بـ Kali |

{{< alert "circle-info" >}}
إذا لم تقم بعد بتثبيت برنامج التشغيل داخل Kali، فأكمل خطوات USB Passthrough في هذا الدليل أولاً. بمجرد ظهور المحول داخل VM، اتبع [دليل تثبيت برنامج تشغيل ALFA](/ar/blog/install-alfa-driver-kali-ubuntu/) لتجميع وتحميل برنامج التشغيل الصحيح.
{{< /alert >}}

---

## USB Passthrough في VirtualBox — خطوة بخطوة

يتطلب VirtualBox مكوناً إضافياً — **Extension Pack** — لدعم USB 2.0 و3.0 passthrough. بدونه، لا يتوفر سوى USB 1.1 (OHCI)، وهو غير كافٍ لمحولات ALFA الحديثة.

### تثبيت VirtualBox Extension Pack

1. افتح [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. ضمن **VirtualBox Extension Pack**، انقر على **All supported platforms** لتنزيل ملف `.vbox-extpack`. يجب أن يتطابق الإصدار تماماً مع إصدار VirtualBox المثبت.
3. افتح VirtualBox، ثم انتقل إلى **ملف → التفضيلات → الامتدادات** (على macOS: **VirtualBox → الإعدادات → الامتدادات**).
4. انقر على أيقونة **+**، وتصفح إلى ملف `.vbox-extpack` الذي تم تنزيله، ثم قم بتثبيته. اقبل الترخيص عند المطالبة.

للتحقق من تفعيل Extension Pack عبر سطر الأوامر:

```bash
VBoxManage list extpacks
```

المخرج المتوقع:

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
إذا أظهر حقل **Usable** القيمة `false`، فإن إصدار Extension Pack لا يتطابق مع إصدار VirtualBox. قم بإلغاء تثبيته وإعادة تثبيت الإصدار الصحيح.
{{< /alert >}}

### إضافة المستخدم إلى مجموعة vboxusers (لمضيفي Linux فقط)

على مضيفي Linux، يجب أن يكون حسابك عضواً في مجموعة `vboxusers` للوصول إلى أجهزة USB.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

بعد تنفيذ هذا الأمر، **سجّل الخروج وأعد تسجيل الدخول** (أو أعد التشغيل) لتفعيل تغيير المجموعة. يمكنك التحقق بـ:

```bash
groups $USER
```

يجب أن يتضمن المخرج `vboxusers`.

### تفعيل وحدة تحكم USB في إعدادات VM

1. أوقف تشغيل VM الخاص بـ Kali إذا كان يعمل.
2. حدد VM، ثم انقر على **الإعدادات → USB**.
3. ضع علامة على **تفعيل وحدة تحكم USB**.
4. حدد **وحدة تحكم USB 3.0 (xHCI)** من أزرار الاختيار.

{{< alert "circle-info" >}}
يتطلب AWUS036AXML USB 3.0 (xHCI). بالنسبة لـ AWUS036ACH، يكفي USB 2.0 (EHCI) تقنياً نظراً لأن المحول نفسه يعمل بـ USB 2.0، لكن استخدام xHCI لا يسبب مشاكل ويحافظ على اتساق الإعداد.
{{< /alert >}}

### إضافة فلتر جهاز USB

يخبر فلتر جهاز USB الخاص بـ VirtualBox أن يلتقط محول ALFA تلقائياً في كل مرة يتم توصيله، دون الحاجة إلى تدخل يدوي في كل جلسة.

1. في نفس لوحة **الإعدادات → USB**، انقر على أيقونة **+** (إضافة فلتر USB من الجهاز).
2. وصّل محول ALFA الآن إذا لم يكن متصلاً بالفعل. سيعرضه VirtualBox في القائمة المنسدلة.
3. حدد الجهاز. يظهر عادةً بـ **"Realtek 802.11ac NIC"** (AWUS036ACH) أو **"MediaTek Corp. 802.11 b/g/n"** (AWUS036AXML).
4. انقر على **موافق** للحفظ.

### تشغيل VM والتحقق عبر lsusb

شغّل VM الخاص بـ Kali. بعد تحميل سطح المكتب، افتح طرفية ونفّذ:

```bash
lsusb
```

يجب أن ترى سطراً مشابهاً لـ:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

أو لـ AWUS036AXML:

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

### تحميل برنامج التشغيل

**AWUS036ACH (RTL8812AU):**

```bash
sudo modprobe 88XXau
```

إذا فشل (الوحدة غير موجودة)، ثبّت حزمة DKMS أولاً:

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML (MT7921AUN):**

```bash
sudo modprobe mt7921u
```

### التحقق من وضع المراقبة

```bash
sudo airmon-ng start wlan1
sudo iwconfig wlan1mon
```

يجب أن يُظهر حقل **Mode** القيمة `Monitor`.

### أخطاء VirtualBox الشائعة

| الخطأ | السبب | الحل |
|---|---|---|
| "لا توجد أجهزة USB متاحة" في إعدادات USB | Extension Pack غير مثبت أو إصداره غير متطابق | ثبّت الإصدار المطابق من Extension Pack |
| المحول غير مُلتقَط / غير مرئي في lsusb | المستخدم غير موجود في مجموعة `vboxusers` (مضيف Linux) | `sudo usermod -aG vboxusers $USER`، ثم اخرج وأعد تسجيل الدخول |
| "جهاز USB مشغول بطلب سابق" | عملية أخرى على المضيف تستخدم الجهاز | افصل المحول وأعد توصيله قبل تشغيل VM |
| الجهاز يستمر في الانقطاع داخل VM | وحدة تحكم USB 3.0 غير مفعّلة؛ يستخدم VM الـ OHCI | التبديل إلى USB 3.0 (xHCI) في إعدادات VM → USB |
| تم إضافة الفلتر لكن الجهاز لا يُلتقَط تلقائياً | تم إنشاء الفلتر قبل تثبيت Extension Pack | احذف الفلتر وثبّت Extension Pack وأعد إضافته |

---

## USB Passthrough في VMware Workstation / VMware Fusion

تتعامل VMware مع USB passthrough بشكل مختلف عن VirtualBox. لا توجد حاجة لتثبيت امتداد منفصل — دعم USB 2.0 و3.0 مدمج في VMware Workstation 17+ وFusion 13+. الآلية الرئيسية هي **خدمة USB Arbitrator**، التي تراقب أحداث USB في المضيف وتوجّه الأجهزة إلى VMs.

### توصيل المحول عبر قائمة الأجهزة

عند توصيل محول ALFA أثناء تشغيل VM، تُظهر VMware عادةً نافذة منبثقة تسأل عن الـ VM الذي يجب أن يمتلك الجهاز. إذا فاتتك النافذة:

1. مع تشغيل Kali VM، انتقل إلى **VM → الأجهزة القابلة للإزالة** في شريط القوائم.
2. وسّع القائمة وحدد محول ALFA (مثلاً **Realtek 802.11ac NIC**).
3. انقر على **توصيل (قطع الاتصال من المضيف)**.

### VMware Fusion (macOS)

1. انتقل إلى **الجهاز الافتراضي → USB والبلوتوث**.
2. حدد محول ALFA في القائمة.
3. بدّل الاتصال إلى **الاتصال بـ Linux** (أو اسم VM الخاص بـ Kali).

### التحقق وتحميل برنامج التشغيل

بعد التوصيل، تحقق داخل Kali:

```bash
lsusb
```

ثم قم بتحميل برنامج التشغيل المناسب كما هو موضح في قسم VirtualBox أعلاه.

### التحقق من خدمة USB Arbitrator في VMware

إذا لم يظهر محول ALFA في قائمة **الأجهزة القابلة للإزالة**، فقد لا تكون خدمة USB arbitrator تعمل. على مضيفي Linux:

```bash
sudo systemctl status vmware-usbarbitrator
```

إذا كانت متوقفة:

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

### تفعيل USB 3.0 في VMware

افتح ملف `.vmx` الخاص بـ Kali VM وتأكد من وجود أو أضف:

```
usb_xhci.present = "TRUE"
```

{{< alert "triangle-exclamation" >}}
مطلوب إصدار VMware للأجهزة 14 أو أحدث لدعم USB 3.0 (xHCI). إذا كان VM تم إنشاؤه بإصدار أجهزة أقدم، قم بالترقية عبر **VM → إدارة → تغيير توافق الأجهزة**.
{{< /alert >}}

### أخطاء VMware الشائعة

| الخطأ | السبب | الحل |
|---|---|---|
| المحول غير موجود في قائمة الأجهزة القابلة للإزالة | USB arbitrator لا يعمل | تشغيل خدمة `vmware-usbarbitrator` |
| الجهاز يتصل ثم ينقطع فوراً | برنامج تشغيل نظام المضيف يستعيد الجهاز | تعطيل برنامج تشغيل WiFi للمحول على المضيف، أو إعادة التوصيل بسرعة أكبر |
| "الجهاز قيد الاستخدام من قبل المضيف" | نظام تشغيل المضيف استحوذ على الجهاز | أزل الجهاز من المضيف قبل التوصيل في VM |
| لا تتوفر سرعة USB 3.0 داخل VM | إصدار أجهزة VM أقل من 14 أو xHCI غير مفعّل | ترقية إصدار الأجهزة، إضافة `usb_xhci.present = "TRUE"` إلى .vmx |
| وضع المراقبة يفشل حتى بعد الـ passthrough | برنامج تشغيل خاطئ أو مفقود داخل Kali | اتبع [دليل تثبيت برنامج التشغيل](/ar/blog/install-alfa-driver-kali-ubuntu/) |

---

## ملاحظات خاصة بكل محول

### AWUS036ACH (RTL8812AU)

AWUS036ACH جهاز **USB 2.0** وهو من أكثر المحولات المختبرة في بيئات VM. كلٌّ من VirtualBox وVMware يتعامل معه بشكل موثوق. حزمة برنامج التشغيل: `realtek-rtl88xxau-dkms`. اسم الوحدة: `88XXau`.

### AWUS036AXML (MT7921AUN)

AWUS036AXML جهاز **USB 3.0** يدعم WiFi 6E وله بعض الحالات الخاصة في بيئات VM. **يجب** استخدام وحدة تحكم USB 3.0 (xHCI). حزمة البرنامج الثابت: `firmware-misc-nonfree`. قد تعاني بعض الوحدات المبكرة من تجمّد دوري تحت VMware/VirtualBox USB 3.0 arbitration. يتعامل VMware Workstation مع AWUS036AXML بشكل أكثر استقراراً من VirtualBox في passthrough USB 3.0.

المراجعة الكاملة: [مراجعة AWUS036AXML WiFi 6E](/ar/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM (RTL8812AU، هوائي واحد)

يتصرف بشكل مطابق لـ AWUS036ACH من منظور برامج التشغيل والـ passthrough. استخدم نفس وحدة `88XXau` ونفس إعدادات VirtualBox/VMware.

---

## نصائح تحسين الأداء

**تعطيل الإيقاف التلقائي لـ USB على المضيف:**

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

**تخصيص موارد كافية للـ VM:**
- **نواتين على الأقل للمعالج** (4 نوى موصى به)
- **2 GB RAM** (4 GB إذا كنت تشغل سطح مكتب Kali كاملاً)

**التقاط لقطة للـ VM قبل مهام اختبار الاختراق.**

{{< alert "circle-info" >}}
لجلسات التقاط الحزم التي تتجاوز 30 دقيقة، فكّر في استخدام موزع USB منفصل بين المحول والمضيف. يوفر طاقة مستقرة ويمنع انقطاع المحول بسبب انخفاض الجهد أثناء الالتقاط الحرج.
{{< /alert >}}

---

## المقارنة الصادقة: الأجهزة المادية مقابل VM

| الميزة | Kali على الأجهزة المادية | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **دعم برامج التشغيل** | كامل ومباشر | جيد (مع Extension Pack) | جيد (USB مدمج) |
| **استقرار وضع المراقبة** | ممتاز | جيد | جيد–ممتاز |
| **موثوقية حقن الحزم** | ممتاز | جيد (أحياناً فقدان إطارات) | جيد–ممتاز |
| **وقت الإعداد** | مرتفع (أجهزة مخصصة) | منخفض–متوسط | منخفض–متوسط |
| **قابلية النقل** | منخفضة | عالية (لقطات، محمول) | عالية |
| **CTF / استخدام المختبر** | مبالغة | مثالي | مثالي |
| **اختبار الاختراق الاحترافي** | موصى به | مقبول | مقبول |

---

## مرجع سريع لاستكشاف الأخطاء

| العَرَض | السبب الأرجح | الحل |
|---|---|---|
| `lsusb` لا يُظهر شيئاً داخل Kali | USB passthrough غير مُعدّ | إضافة فلتر USB (VBox) أو التوصيل عبر الأجهزة القابلة للإزالة (VMware) |
| "لا توجد أجهزة USB" في إعدادات VirtualBox | Extension Pack مفقود أو إصداره غير متطابق | تثبيت Extension Pack المطابق |
| المحول مرئي في `lsusb` لكن لا يوجد واجهة `wlan` | برنامج التشغيل لم يُحمَّل | `sudo modprobe 88XXau` أو `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | حزمة DKMS غير مثبتة | `sudo apt install realtek-rtl88xxau-dkms` |
| الواجهة تظهر ثم تختفي | الإيقاف التلقائي لـ USB أو VBox xHCI arbitration | تعطيل الإيقاف التلقائي؛ جرّب وحدة تحكم USB 2.0 للـ ACH |
| `airmon-ng` يبدأ لكن وضع المراقبة يفشل صامتاً | برنامج تشغيل خاطئ أو تعارض مع مدير الشبكة | `sudo airmon-ng check kill` ثم أعد المحاولة |
| فلتر USB في VirtualBox لا يلتقط عند الإقلاع | تمت إضافة الفلتر قبل تثبيت Extension Pack | احذف الفلتر وثبّت Extension Pack وأعد إضافته |
| VMware يفقد الجهاز خلال الجلسات الطويلة | توقف خدمة USB arbitrator في VMware | إعادة التفعيل وتعيينها للبدء التلقائي |

---

## الخطوات التالية

- **تثبيت أو تحديث برنامج التشغيل:** [دليل تثبيت برنامج تشغيل ALFA لـ Kali وUbuntu](/ar/blog/install-alfa-driver-kali-ubuntu/)
- **الإعداد الكامل لـ AWUS036ACH:** [دليل إعداد AWUS036ACH على Kali Linux](/ar/blog/awus036ach-kali-linux-setup/)
- **مراجعة أجهزة AWUS036AXML:** [مراجعة AWUS036AXML WiFi 6E](/ar/blog/awus036axml-wifi-6e-review/)
