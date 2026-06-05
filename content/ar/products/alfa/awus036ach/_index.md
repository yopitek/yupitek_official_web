---
title: "ALFA AWUS036ACH — محول USB-C لاسلكي ثنائي النطاق AC1200 عالي الطاقة"
description: "ALFA AWUS036ACH، Realtek RTL8812AU، AC1200 ثنائي النطاق، USB-C، هوائيان خارجيان 5 dBi، المعيار الذهبي لأبحاث أمن Kali Linux، يدعم Monitor Mode وPacket Injection."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
dir: rtl
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "هوائيان", "Monitor Mode", "Kali Linux", "أبحاث أمنية"]
---

{{< alert "warning" >}}
**إخلاء المسؤولية القانونية**: تُستخدم ميزتا Monitor Mode وPacket Injection فقط للاختبارات الأمنية المُرخَّصة والبحث العلمي والاختبارات القانونية. تأكد من الحصول على إذن صريح من الشبكة المستهدفة.
{{< /alert >}}

## نظرة عامة على المنتج

AWUS036ACH هو المحول الأكثر شهرةً من ALFA Network، والمعيار الذهبي لاختبار الاختراق على Kali Linux منذ عام 2017. يعمل بشريحة Realtek RTL8812AU الموثوقة، ويوفر دعمًا راسخًا لـ Monitor Mode وPacket Injection، ومضخم طاقة مدمج للاستقبال بعيد المدى، وهوائيان قابلان للفصل بقوة 5 dBi. كان أول محول Wi-Fi 5 في العالم يتميز بموصل USB Type-C.

> **ملاحظة macOS:** جميع محولات ALFA لها دعم محدود أو معدوم لـ macOS. macOS 11 Big Sur وما بعده وApple Silicon (M1/M2/M3) **غير مدعومة**. الحد الأقصى للدعم هو macOS 10.15 Catalina على Mac بمعالج Intel.

## الميزات الرئيسية

- Realtek RTL8812AU — الشريحة الأكثر اختبارًا في أبحاث أمن Wi-Fi
- Wi-Fi 5 (802.11ac) ثنائي النطاق AC1200 — 867 Mbps على 5 GHz، و300 Mbps على 2.4 GHz
- مضخم طاقة مدمج — مدى يصل إلى 3 أضعاف بطاقات اللابتوب العادية
- 2× RP-SMA female مع 2× هوائي ثنائي النطاق 5 dBi قابل للفصل (قابل للترقية)
- أول محول Wi-Fi 5 USB-C في العالم
- حامل شاشة مرفق
- دعم Packet Injection على Kali Linux منذ Kali 2017.1
- متوافق مع 802.11a/b/g/n

## المواصفات التقنية

| العنصر | المواصفة |
|--------|----------|
| الشريحة | Realtek RTL8812AU |
| معايير Wi-Fi | IEEE 802.11 a/b/g/n/ac (Wi-Fi 5) |
| نطاقات التردد | 2.4 GHz · 5 GHz (ثنائي النطاق) |
| أقصى معدل بيانات | 802.11b: 11 Mbps · 802.11a/g: 54 Mbps · 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| السرعة القصوى المجمعة | AC1200 (867 + 300 Mbps) |
| موصلات الهوائي | 2× RP-SMA female |
| الهوائيات المرفقة | 2× هوائي ثنائي القطب متعدد الاتجاهات ثنائي النطاق، 5 dBi |
| واجهة USB | Type-C SuperSpeed USB (5 Gbps)؛ متوافق مع USB 2.0 |
| مضخم الطاقة | نعم — مدى موسّع |
| الأمان اللاسلكي | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| الملحقات | حامل شاشة · كابل USB |
| بلد المنشأ | تايوان |

## دعم نظام التشغيل

| نظام التشغيل | الحالة | ملاحظات |
|-------------|--------|----------|
| Windows 10 / 11 | ✅ مدعوم | تنزيل الدرايفر من موقع ALFA؛ دعم WPA3 (درايفر أكتوبر 2019+) |
| macOS 10.15 Catalina | ⚠️ محدود | تثبيت يدوي؛ macOS 11+ وApple Silicon غير مدعومان |
| Ubuntu | ✅ مدعوم | تثبيت RTL8812AU DKMS يدويًا؛ مدمج في Ubuntu 24.10+ (نواة ≥ 6.14) |
| Kali Linux | ✅ ممتاز | منذ Kali 2017.1؛ Monitor Mode + Packet Injection كاملان؛ استخدم درايفر aircrack-ng |
| NetHunter (Android) | ✅ مدعوم | OTG USB؛ مؤكد على نطاق واسع |

## الأجهزة المدعومة

| الجهاز | الحالة | ملاحظات |
|--------|--------|----------|
| Raspberry Pi 3B+/4/5 | ✅ مدعوم | تثبيت يدوي عبر سكريبت morrownr DKMS |
| PC سطح المكتب / محمول | ✅ مدعوم | USB-C أو USB-A (عبر الكابل المرفق) |
| Mac (Intel) | ⚠️ محدود | الحد الأقصى macOS 10.15 Catalina |

## الإمكانات المتقدمة

| الميزة | الحالة |
|--------|--------|
| Monitor Mode | ✅ ممتاز (المعيار الذهبي — مُثبَت من المجتمع منذ 2017) |
| Packet Injection | ✅ ممتاز |
| Soft AP Mode | ✅ نعم |
| Bluetooth | ❌ لا |
| VIF | ⚠️ محدود (استخدم AWUS036ACM لدعم VIF الكامل) |

## محتويات العبوة

- 1× محول AWUS036ACH
- 2× هوائي ثنائي القطب ثنائي النطاق 5 dBi قابل للفصل
- 1× كابل USB-C إلى USB-A
- 1× حامل شاشة

## الموارد والروابط

| المورد | الرابط |
|--------|--------|
| صفحة المنتج الرسمية | https://www.alfa.com.tw/products/awus036ach_1 |
| التوثيق الرسمي | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| الدرايفر (aircrack-ng، الأفضل لـ Kali) | https://github.com/aircrack-ng/rtl8812au |
| الدرايفر (morrownr، Linux العام) | https://github.com/morrownr/8812au-20210708 |

## تنزيل كتيب المواصفات

| المستند | التنزيل |
|---------|---------|
| كتيب المواصفات الرسمي (PDF) | [📄 تنزيل كتيب مواصفات AWUS036ACH](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
