---
title: "ALFA AWUS036AXER — محول USB Wi-Fi 6 نانو فائق النحافة"
description: "ALFA AWUS036AXER مع شريحة Realtek RTL8832BU. Wi-Fi 6 ثنائي النطاق، شكل نانو (~65×24×10mm). للاتصال اليومي — غير موصى به لـ Kali Linux أو أبحاث الأمان."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "802.11ax", "فائق النحافة", "USB 3.2", "محمول", "نانو"]
dir: rtl
---

## نظرة عامة على المنتج

يتميز AWUS036AXER بشريحة Realtek RTL8832BU مع دعم Wi-Fi 6 (802.11ax) ثنائي النطاق (2.4 GHz + 5 GHz)، حتى 1800 Mbps (2.4 GHz: 573 Mbps + 5 GHz: 1200 Mbps). تصميم نانو فائق النحافة (~65 × 24 × 10 mm، ~10g) للاستخدام اليومي المحمول.

> ⚠️ **ملاحظة:** شكل نانو — **لا يوجد موصل RP-SMA**، لا يمكن ترقية الهوائي. **غير موصى به لـ Kali Linux أو أبحاث الأمان**.

> **ملاحظة macOS:** جميع محولات ALFA لها دعم محدود أو معدوم لـ macOS. macOS 11 Big Sur وما بعده وApple Silicon (M1/M2/M3) **غير مدعومة**. الحد الأقصى للدعم هو macOS 10.15 Catalina على Mac بمعالج Intel.

## الميزات الرئيسية

- Wi-Fi 6 (802.11ax) ثنائي النطاق: 2.4 GHz + 5 GHz
- شريحة Realtek RTL8832BU
- حتى 1800 Mbps
- تصميم نانو فائق النحافة (~65×24×10mm، ~10g)
- USB 3.2 Gen 1 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ لا موصل RP-SMA، هوائي مدمج

## المواصفات التقنية

| العنصر | المواصفة |
|--------|----------|
| الشريحة | Realtek RTL8832BU |
| معايير Wi-Fi | IEEE 802.11 a/b/g/n/ac/ax (Wi-Fi 6) |
| نطاقات التردد | 2.4 GHz + 5 GHz (لا يوجد 6 GHz) |
| أقصى معدل بيانات | 1800 Mbps (2.4G: 573 Mbps + 5G: 1200 Mbps) |
| الهوائي | نانو مدمج (بدون RP-SMA) |
| واجهة USB | USB 3.2 Gen 1 Type-A |
| الأبعاد | ~65 × 24 × 10 mm، ~10g |
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
| Raspberry Pi 4/5 | ⚠️ يتطلب درايفر | تثبيت يدوي على Pi OS بنواة < 6.14 |
| PC سطح المكتب/محمول | ✅ مدعوم | USB-A قياسي |

## الإمكانات المتقدمة

| الميزة | الحالة |
|--------|--------|
| Monitor Mode | ⚠️ محدود |
| Packet Injection | ⚠️ محدود |
| Soft AP Mode | ✅ نعم |
| Bluetooth | ❌ لا |

## محتويات العبوة

- 1× محول AWUS036AXER نانو

## الموارد والروابط

| المورد | الرابط |
|--------|--------|
| التوثيق الرسمي | https://docs.alfa.com.tw/ |
| درايفر Linux (RTL8832BU) | https://github.com/morrownr/rtl8852bu-20240418 |

## تنزيل كتيب المواصفات

| المستند | التنزيل |
|------|------|
| كتيب المواصفات الرسمي (PDF) | [📄 تنزيل كتيب مواصفات AWUS036AXER](/docs/alfa/AWUS036AXER_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axer_image_1.png" alt="ALFA AWUS036AXER" />
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
هل تحتاج إلى طلب عرض سعر للمنتج؟ يرجى [الاتصال بنا](/ar/contact/).
{{< /alert >}}
