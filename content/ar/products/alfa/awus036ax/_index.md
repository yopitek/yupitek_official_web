---
title: "ALFA AWUS036AX — محول USB Wi-Fi 6 ثنائي النطاق"
description: "ALFA AWUS036AX مع شريحة Realtek RTL8832BU، Wi-Fi 6 ثنائي النطاق 2.4+5 GHz، حتى 1200 Mbps، USB 3.0. ملاحظة: Wi-Fi 6 فقط — لا نطاق 6 GHz."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "USB 3.0", "802.11ax", "ثنائي النطاق", "OFDMA", "MU-MIMO"]
dir: rtl
---

## نظرة عامة على المنتج

يتميز AWUS036AX بشريحة Realtek RTL8832BU مع دعم Wi-Fi 6 (802.11ax) ثنائي النطاق (2.4 GHz + 5 GHz)، حتى 1200 Mbps مشتركة، مع تقنية MU-MIMO 2×2 وOFDMA. الهوائي مدمج (غير قابل للفصل).

> ⚠️ **مهم:** هذا الجهاز يدعم **Wi-Fi 6** فقط، وليس Wi-Fi 6E — **لا يوجد نطاق 6 GHz**. للحصول على دعم 6 GHz، انظر AWUS036AXML أو AWUS036AXM. Monitor mode محدود على نواة < 6.12؛ **غير موصى به لأبحاث الأمان على Linux**.

> **ملاحظة macOS:** جميع محولات ALFA لها دعم محدود أو معدوم لـ macOS. macOS 11 Big Sur وما بعده وApple Silicon (M1/M2/M3) **غير مدعومة**. الحد الأقصى للدعم هو macOS 10.15 Catalina على Mac بمعالج Intel.

## الميزات الرئيسية

- Wi-Fi 6 (802.11ax) ثنائي النطاق: 2.4 GHz + 5 GHz
- شريحة Realtek RTL8832BU
- حتى 1200 Mbps مشتركة
- MU-MIMO 2×2
- تقنية OFDMA
- USB 3.0 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ لا يوجد نطاق 6 GHz

## المواصفات التقنية

| العنصر | المواصفة |
|--------|----------|
| الشريحة | Realtek RTL8832BU |
| معايير Wi-Fi | IEEE 802.11 a/b/g/n/ac/ax (Wi-Fi 6) |
| نطاقات التردد | 2.4 GHz + 5 GHz (لا يوجد 6 GHz) |
| أقصى معدل بيانات | 1200 Mbps |
| MIMO | MU-MIMO 2×2 |
| الهوائي | مدمج (غير قابل للفصل) |
| واجهة USB | USB 3.0 Type-A |
| الأمان اللاسلكي | WPA3 / WPA2 / WPA / WEP |

## دعم نظام التشغيل

| نظام التشغيل | الحالة | ملاحظات |
|-------------|--------|----------|
| Windows 10/11 | ✅ مدعوم | درايفر من موقع Alfa |
| macOS | ❌ غير مدعوم | لا دعم لـ macOS 11+ أو Apple Silicon |
| Ubuntu | ⚠️ يتطلب درايفر | مدمج في النواة ≥ 6.14 (Ubuntu 24.10+)؛ الإصدارات القديمة تحتاج DKMS يدوي |
| Kali Linux | ⚠️ محدود | Monitor mode محدود على نواة < 6.12؛ غير موصى به للاختبار |
| NetHunter | ⚠️ محدود | يعتمد على النواة |

## الأجهزة المدعومة

| الجهاز | الحالة | ملاحظات |
|--------|--------|----------|
| Raspberry Pi 4/5 | ⚠️ يتطلب درايفر | تثبيت يدوي مطلوب على Pi OS بنواة < 6.14 |
| PC سطح المكتب/محمول | ✅ مدعوم | USB-A قياسي |

## الإمكانات المتقدمة

| الميزة | الحالة |
|--------|--------|
| Monitor Mode | ⚠️ محدود (يُوصى بنواة ≥ 6.12) |
| Packet Injection | ⚠️ محدود |
| Soft AP Mode | ✅ نعم |
| Bluetooth | ❌ لا |

## محتويات العبوة

- 1× محول AWUS036AX

## الموارد والروابط

| المورد | الرابط |
|--------|--------|
| التوثيق الرسمي | https://docs.alfa.com.tw/ |
| درايفر Linux (RTL8832BU) | https://github.com/morrownr/rtl8852bu-20240418 |

## تنزيل كتيب المواصفات

| المستند | التنزيل |
|------|------|
| كتيب المواصفات الرسمي (PDF) | [📄 تنزيل كتيب مواصفات AWUS036AX](/docs/alfa/AWUS036AX_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ax_image_1.png" alt="ALFA AWUS036AX" />
{{< /gallery >}}

---

## ملحقات الهوائي المتوافقة

تستخدم جميع محولات ALFA USB موصل RP-SMA قياسي. قم بالترقية باستخدام هوائي خارجي اختياري لزيادة النطاق والكسب:

| الهوائي | التردد | الكسب | النوع |
|---------|--------|-------|-------|
| [ALFA APA-M04](/ar/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | لوحة داخلية اتجاهية |
| [ALFA APA-M25](/ar/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | لوحة داخلية ثنائية النطاق |
| [ALFA APA-M25-6E](/ar/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | لوحة داخلية ثلاثية النطاق |
| [ARS 25-57A](/ar/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | خارجي متعدد الاتجاهات |
| [ARS NT5B7](/ar/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | متعدد الاتجاهات |

{{< alert >}}
للاستفسار أو طلب عرض أسعار، [تواصل معنا](/ar/contact/).
{{< /alert >}}
