---
title: "ALFA AWUS036AXML — محول USB Wi-Fi 6E ثلاثي النطاق USB-C"
description: "ALFA AWUS036AXML مع شريحة MediaTek MT7921AUN، Wi-Fi 6E ثلاثي النطاق (2.4/5/6 GHz)، واجهة USB-C، Bluetooth 5.2، يدعم Monitor Mode في Kali Linux."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "ثلاثي النطاق", "Bluetooth 5.2", "6GHz", "Kali Linux"]
dir: rtl
---

{{< alert "warning" >}}
**إخلاء المسؤولية القانونية**: تُستخدم ميزتا Monitor Mode وPacket Injection فقط للاختبارات الأمنية المُرخَّصة والبحث العلمي والاختبارات القانونية. تأكد من الحصول على إذن صريح من الشبكة المستهدفة.
{{< /alert >}}

## نظرة عامة على المنتج

يتميز AWUS036AXML بشريحة MediaTek MT7921AUN مع دعم Wi-Fi 6E ثلاثي النطاق (2.4 GHz / 5 GHz / 6 GHz)، وسرعة نقل مشتركة تصل إلى 3000 Mbps، إضافةً إلى Bluetooth 5.2 المدمج. تأتي واجهة USB-C مع كابل 2-in-1 USB-C/USB-A وحامل شاشة.

> **ملاحظة macOS:** جميع محولات ALFA لها دعم محدود أو معدوم لـ macOS. macOS 11 Big Sur وما بعده وApple Silicon (M1/M2/M3) **غير مدعومة**. الحد الأقصى للدعم هو macOS 10.15 Catalina على Mac بمعالج Intel.

## الميزات الرئيسية

- Wi-Fi 6E ثلاثي النطاق: 2.4 / 5 / 6 GHz
- شريحة MediaTek MT7921AUN
- سرعة نقل مشتركة تصل إلى 3000 Mbps
- Bluetooth 5.2 (شريحة مدمجة)
- واجهة USB-C (USB 3.2 Gen 1، 5 Gbps)
- كابل 2-in-1 USB-C/USB-A مرفق
- هوائي 1× RP-SMA قابل للفصل
- حامل شاشة مرفق
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux Monitor Mode (نواة ≥ 5.18)

## المواصفات التقنية

| العنصر | المواصفة |
|--------|----------|
| الشريحة | MediaTek MT7921AUN |
| معايير Wi-Fi | IEEE 802.11 a/b/g/n/ac/ax (Wi-Fi 6E) |
| نطاقات التردد | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| أقصى معدل بيانات | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · المجموع: 3000 Mbps |
| Bluetooth | BT 5.2 (شريحة مدمجة) |
| موصل الهوائي | 1× RP-SMA female (قابل للفصل) |
| واجهة USB | USB 3.2 Gen 1 Type-C (5 Gbps) |
| الكابل | 2-in-1 USB-C/USB-A |
| الأمان اللاسلكي | WPA3 / WPA2 / WPA / WEP / WPS |
| بلد المنشأ | تايوان |

## دعم نظام التشغيل

| نظام التشغيل | الحالة | ملاحظات |
|-------------|--------|----------|
| Windows 10 | ✅ مدعوم | 2.4 GHz و 5 GHz فقط؛ 6 GHz غير متاح على Win10 |
| Windows 11 | ✅ مدعوم | ثلاثي النطاق الكامل بما في ذلك 6 GHz |
| macOS | ❌ غير مدعوم | لا دعم لـ macOS 11+ أو Apple Silicon |
| Ubuntu | ✅ مدعوم | درايفر mt7921u المدمج في النواة ≥ 5.18 (Ubuntu 22.10+) |
| Kali Linux | ✅ مدعوم | Monitor mode ≥ نواة 5.18؛ Monitor mode النشط ≥ 6.12؛ packet injection مدعوم |
| NetHunter (Android) | ⚠️ جزئي | OTG؛ يعتمد على النواة |

## الأجهزة المدعومة

| الجهاز | الحالة | ملاحظات |
|--------|--------|----------|
| Raspberry Pi 3B+/4/5 | ✅ مدعوم | تحديث Pi OS (نواة ≥ 5.18)؛ قد يحتاج نسخ ملفات الفيرموير |
| PC سطح المكتب/محمول | ✅ مدعوم | USB-C أو USB-A عبر كابل 2-in-1 المرفق |
| Mac Intel | ⚠️ محدود | الحد الأقصى macOS 10.15 Catalina |

## الإمكانات المتقدمة

| الميزة | الحالة |
|--------|--------|
| Monitor Mode | ✅ نعم (نواة ≥ 5.18؛ الوضع النشط ≥ 6.12) |
| Packet Injection | ✅ نعم |
| Soft AP Mode | ✅ نعم |
| Bluetooth | ✅ BT 5.2 |
| VIF | ✅ نعم |

## محتويات العبوة

- 1× محول AWUS036AXML
- 1× هوائي ثنائي القطب قابل للفصل
- 1× كابل 2-in-1 USB-C/USB-A
- 1× حامل شاشة

## الموارد والروابط

| المورد | الرابط |
|--------|--------|
| صفحة المنتج الرسمية | https://www.alfa.com.tw/products/awus036axml |
| التوثيق الرسمي | https://docs.alfa.com.tw/ |
| درايفر Linux (مدمج في النواة) | mt7921u — مدمج في نواة Linux ≥ 5.18 |

## تنزيل كتيب المواصفات

| المستند | التنزيل |
|------|------|
| كتيب المواصفات الرسمي (PDF) | [📄 تنزيل كتيب مواصفات AWUS036AXML](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
{{< /gallery >}}

---

{{< alert >}}
للاستفسار أو طلب عرض أسعار، [تواصل معنا](/ar/contact/).
{{< /alert >}}
