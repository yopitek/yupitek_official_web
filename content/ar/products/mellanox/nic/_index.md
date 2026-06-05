---
title: "بطاقات واجهة الشبكة NVIDIA Mellanox ConnectX (NIC)"
description: "قارن بين محولات شبكة NVIDIA Mellanox ConnectX-4 Lx وConnectX-5 وConnectX-6 Dx/Lx وConnectX-7. خيارات سرعة 10G و25G و50G و100G و200G و400G لواجهات PCIe Gen3/4/5."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# بطاقات شبكة Mellanox / NVIDIA ConnectX — من 10 جيجابت إلى 400 جيجابت في الثانية

توفر محولات NVIDIA Mellanox ConnectX نطاقاً ترددياً رائداً وزمن استجابة فائقاً لخوادم المؤسسات ومجموعات الذكاء الاصطناعي. ستجد أدناه الكتالوج الكامل للموديلات التي توزعها يوبيتك (Yupitek)، مصنفة حسب فئات السرعة.

---

## بطاقات شبكة 10GbE / 25GbE

مثالية لخوادم المؤسسات العامة، والبيئات الافتراضية (VMware ESXi)، وأنظمة التخزين الشبكي (NAS) عالية الأداء.

### موديل 10G

| رقم الجزء | الجيل / شريحة المعالجة | المنافذ | السرعة | منفذ PCIe | الموصل | البروتوكول | الحامل |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | مزدوج | 10GbE | PCIe 3.0 x8 | SFP28 | إيثرنت | طويل |

### موديلات 25G

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*محول NVIDIA ConnectX-4 Lx 25GbE ثنائي المنافذ*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*محول NVIDIA ConnectX-5 25GbE ثنائي المنافذ*

| رقم الجزء | الجيل / شريحة المعالجة | المنافذ | السرعة | منفذ PCIe | الموصل | البروتوكول | الحامل / عامل الشكل | الميزات الخاصة |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | مزدوج | 25GbE | PCIe 3.0 x8 | SFP28 | إيثرنت | حامل طويل | بطاقة PCIe قياسية |
| **MCX4121A-ACUT** | ConnectX-4 Lx | مزدوج | 25GbE | PCIe 3.0 x8 | SFP28 | إيثرنت | حامل طويل | مُمكّن واجهة UEFI |
| **MCX512A-ACAT** | ConnectX-5 EN | مزدوج | 25GbE | PCIe 3.0 x8 | SFP28 | إيثرنت | حامل طويل | تقنية RoCEv2 محسنة |
| **MCX512A-ACUT** | ConnectX-5 EN | مزدوج | 25GbE | PCIe 3.0 x8 | SFP28 | إيثرنت | حامل طويل | واجهة UEFI (x86/ARM) |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | مزدوج | 25GbE | PCIe 4.0 x8 | SFP28 | إيثرنت | حامل طويل | إقلاع آمن، بدون تشفير |
| **MCX623432AS-ADAB**| ConnectX-6 Lx | مزدوج | 25GbE | PCIe 4.0 x8 | SFP28 | إيثرنت | OCP 3.0 ببرغي إبهامي | إقلاع آمن، عامل شكل OCP 3.0 |

---

## بطاقات شبكة 50GbE / 100GbE

مناسبة لأنظمة تخزين NVMe عبر الشبكات (NVMe-oF) عالية السرعة، والبنية التحتية شديدة التقارب (HCI)، وخوادم قواعد البيانات.

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*محول NVIDIA ConnectX-5 100GbE*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*محول NVIDIA ConnectX-6 Dx 100GbE ثنائي المنافذ*

### موديل 50G

| رقم الجزء | الجيل / شريحة المعالجة | المنافذ | السرعة | منفذ PCIe | الموصل | البروتوكول | الحامل |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | أحادي | 50GbE | PCIe 3.0 x16 | QSFP28 | إيثرنت | طويل |

### موديلات 100G

| رقم الجزء | الجيل / شريحة المعالجة | المنافذ | السرعة | منفذ PCIe | الموصل | البروتوكول | عامل الشكل | الميزات الخاصة |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | أحادي | 100GbE | PCIe 3.0 x16 | QSFP28 | إيثرنت | PCIe طويل | بطاقة 100G قياسية |
| **MCX555A-ECAT** | ConnectX-5 VPI | أحادي | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe طويل | منفذ EDR IB و100GbE |
| **MCX516A-CCAT** | ConnectX-5 EN | مزدوج | 100GbE | PCIe 3.0 x16 | QSFP28 | إيثرنت | PCIe طويل | منفذ 100G مزدوج |
| **MCX516A-CDAT** | ConnectX-5 Ex | مزدوج | 100GbE | PCIe 4.0 x16 | QSFP28 | إيثرنت | PCIe طويل | واجهة PCIe 4.0 |
| **MCX556A-ECAT** | ConnectX-5 VPI | مزدوج | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe طويل | منفذ EDR IB مزدوج |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| مزدوج | 100G | PCIe 4.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe طويل | منفذ EDR مزدوج بواجهة PCIe 4.0 |
| **MCX653105A-ECAT**| ConnectX-6 VPI | أحادي | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe طويل | منفذ HDR100 IB و100GbE |
| **MCX653106A-ECAT**| ConnectX-6 VPI | مزدوج | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe طويل | منفذ HDR100 IB و100GbE |
| **MCX623106AN-CDAT**| ConnectX-6 Dx | مزدوج | 100GbE | PCIe 4.0 x16 | QSFP56 | إيثرنت | PCIe طويل | منفذ SFP56/QSFP56 مزدوج بسرعة 100G |
| **MCX623436AN-CDAB**| ConnectX-6 Dx | مزدوج | 100GbE | PCIe 4.0 x16 | QSFP56 | إيثرنت | OCP 3.0 ببرغي إبهامي | عامل شكل OCP |

---

## بطاقات شبكة 200GbE / 400GbE

محولات شبكة فائقة مصممة لعقد خوادم وحدات معالجة الرسومات المخصصة للذكاء الاصطناعي (مثل بنيات NVIDIA HGX/DGX)، والتداول عالي التردد (HFT)، والعمود الفقري لشبكات الحوسبة عالية الأداء (HPC).

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*محول NVIDIA ConnectX-7 400G OSFP*

### موديلات 200G

| رقم الجزء | الجيل / شريحة المعالجة | المنافذ | السرعة | منفذ PCIe | الموصل | البروتوكول | عامل الشكل | الميزات الخاصة |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | أحادي | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | PCIe طويل | منفذ HDR IB و200GbE |
| **MCX653106A-HDAT**| ConnectX-6 VPI | مزدوج | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | PCIe طويل | منفذ HDR/200G مزدوج |
| **MCX623105A-VDAT**| ConnectX-6 Dx | أحادي | 200GbE | PCIe 4.0 x16 | QSFP56 | إيثرنت | PCIe طويل | منفذ 200G أحادي |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | أحادي | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | PCIe طويل | منفذ NDR200، تقنية Socket Direct |
| **MCX755106AS-HEAT**| ConnectX-7 VPI | مزدوج | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | PCIe طويل | منفذ 1 إينفينيباند، المنفذ الثاني VPI |
| **MCX753436MS-HEAB**| ConnectX-7 VPI | مزدوج | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | OCP 3.0 ببرغي إبهامي | عامل شكل OCP متعدد المضيفين / Socket Direct |

### موديلات 400G

| رقم الجزء | الجيل / شريحة المعالجة | المنافذ | السرعة | منفذ PCIe | الموصل | البروتوكول | عامل الشكل | الميزات الخاصة |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | أحادي | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | PCIe طويل | بروتوكول NDR InfiniBand |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | أحادي | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | PCIe طويل | منفذ NDR OSFP، جاهز لتقنية Socket Direct |

---

## دليل الاختيار الفني

عند اختيار محول ConnectX المناسب، انتبه جيداً للنقاط التالية:

### 1. وضع البروتوكول (VPI مقابل EN)
- **محولات EN**: تدعم شبكات إيثرنت فقط.
- **محولات VPI (الاتصال البيني الافتراضي للبروتوكولات)**: يمكن تهيئتها عبر البرامج الثابتة (Firmware) للعمل كبطاقة InfiniBand أو إيثرنت، مما يوفر مرونة قصوى في التشغيل والتهيئة.

### 2. متطلبات النطاق الترددي لمنفذ PCIe
تأكد من أن إصدار منفذ PCIe وعرض المجرى (Slot Width) في الخادم المضيف يمكنهما دعم البطاقة بالسرعة الكاملة:
- تتطلب بطاقة شبكة 100G ثنائية المنافذ منفذ PCIe 4.0 x16 لتشغيل كلا المنفذين معاً بكامل طاقتهما.
- تركيب بطاقة تدعم PCIe 4.0 في منفذ PCIe 3.0 يوفر توافقاً تنازلياً، ولكن سيتم تقييد معدل نقل البيانات بحدود إصدار PCIe 3.0 (حوالي 64 جيجابت في الثانية لسرعة x8، و128 جيجابت في الثانية لسرعة x16).

### 3. عامل الشكل OCP 3.0 مقابل PCIe القياسي
الموديلات التي تنتهي بلواحق مثل `-ADAB` و `-CDAB` و `-HEAB` تستخدم عامل الشكل **OCP NIC 3.0**. تنزلق هذه البطاقات داخل فتحات مخصصة في الخوادم (الشائعة في الأجيال الحديثة من خوادم Supermicro و Dell و HPE و Lenovo) ولا يمكن تركيبها في فتحة PCIe قياسية.

---

{{< alert >}}
هل تحتاج إلى طلب عرض سعر للمنتج؟ يرجى [الاتصال بنا](/ar/contact/).
{{< /alert >}}
