---
title: "ALFA AWUS036ACHM — محول USB لاسلكي ثنائي النطاق AC433 خفيف الوزن"
description: "ALFA AWUS036ACHM، مجموعة شرائح MediaTek MT7610U، ثنائي النطاق AC433، USB 2.0، تصميم هوائي أحادي خفيف الوزن، يدعم وضع المراقبة (Monitor Mode)، مثالي للاستخدام المتنقل."
date: 2026-03-12
showBreadcrumbs: true
showTableOfContents: true
dir: rtl
languageDirection: rtl
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC433", "USB 2.0", "ثنائي النطاق", "خفيف الوزن"]
faq:
  - question: "هل أحتاج إلى تثبيت برنامج تشغيل لجهاز AWUS036ACHM على نظام Linux؟"
    answer: "عادةً لا. تشير صفحة دعم ALFA لنظام Linux إلى أن الجهاز يعمل بتوصيل وتشغيل (plug and play) على أنظمة Kali و Ubuntu و Raspberry Pi OS، وتذكر الدعم في نواة Linux الرئيسية بدءًا من الإصدار 4.19. على نظام Debian، تحتاج بالإضافة إلى ذلك إلى إضافة مصدر APT غير الحر وتثبيت حزمة البرنامج الثابت (firmware)."
  - question: "هل يعمل جهاز AWUS036ACHM على نظامي Windows و macOS؟"
    answer: "توفر ALFA تنزيلات برامج التشغيل لأنظمة Windows و macOS على صفحة وثائق AWUS036ACHM، جنبًا إلى جنب مع دليل التثبيت السريع. قم بتثبيت برنامج التشغيل قبل الاستخدام الأول على هذه الأنظمة."
  - question: "هل يدعم جهاز AWUS036ACHM وضع المراقبة (monitor mode) وحقن الحزم (packet injection)؟"
    answer: "لا تذكر وثائق ALFA صراحةً دعم وضع المراقبة. ومع ذلك، تعرض صفحة دعم Linux الخاصة بها نتائج اختبار حقن aireplay-ng، حيث تم الإبلاغ عن جميعها على أنها OK. قم باختبار ذلك على إعدادك الخاص، واستخدم هذه الميزات فقط لاختبارات الأمن المصرح بها."
---

{{< alert "warning" >}}
**إقرار الاستخدام القانوني**: وضع المراقبة (Monitor Mode) مخصص فقط لاختبار الاختراق المصرّح به، والبحث التعليمي، والاختبار الأمني القانوني.
{{< /alert >}}

## نظرة عامة على المنتج
AWUS036ACHM يعتمد على مجموعة شرائح (Chipset) MediaTek MT7610U، ويدعم معيار IEEE 802.11ac ثنائي النطاق، بأقصى سرعة 433 Mbps (5GHz). تصميم بهوائي أحادي خفيف الوزن، مثالي للاستخدام المتنقل خارج المنزل.

## جدول المواصفات
| البند | المواصفة |
|-------|----------|
| الطراز | AWUS036ACHM |
| مجموعة الشرائح (Chipset) | MediaTek MT7610U |
| معيار Wi-Fi | IEEE 802.11 a/b/g/n/ac |
| النطاق | ثنائي النطاق 2.4GHz / 5GHz |
| أقصى سرعة نقل | 802.11n: 150 Mbps / 802.11ac: 433 Mbps |
| الهوائي | 1 × هوائي ثنائي النطاق خارجي قابل للفصل، 5 dBi |
| موصل الهوائي | RP-SMA أنثى |
| الواجهة | USB 2.0 |

## دعم أنظمة التشغيل
| النظام | حالة الدعم |
|--------|-----------|
| Windows | ✅ يتطلب تثبيت برنامج التشغيل |
| Linux | ✅ مدعوم |
| Kali Linux | ✅ دعم كامل |

## محتويات العبوة
- AWUS036ACHM محول USB لاسلكي × 1
- هوائي ثنائي النطاق × 1
- كابل USB (1 م) × 1

## تنزيل برنامج التشغيل
| المنصة | الرابط |
|--------|--------|
| تنزيل برنامج التشغيل (Driver) | [مستودع ALFA الرسمي](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACHM) |
| الوثائق الرسمية | [وثائق منتجات ALFA](https://docs.alfa.com.tw/Product/AWUS036ACHM/) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036achm_image_1.png" alt="ALFA AWUS036ACHM" />
{{< /gallery >}}

---

## ملحقات الهوائي المتوافقة

تستخدم جميع محولات ALFA USB موصل RP-SMA قياسي. قم بالترقية باستخدام هوائي خارجي اختياري لزيادة النطاق والكسب:

| الهوائي | التردد | الكسب | النوع |
|---------|--------|-------|-------|
| [ALFA APA-M04](/ar/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | لوحة داخلية اتجاهية |
| [ALFA APA-M25](/ar/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | لوحة داخلية ثنائية النطاق |
| [ALFA APA-M25-6E](/ar/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | لوحة داخلية ثلاثية النطاق |
| [ARS 25-57A](/ar/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | خارجي متعدد الاتجاهات |
| [ARS NT5B7](/ar/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | متعدد الاتجاهات |

{{< alert >}}
هل تحتاج إلى طلب عرض سعر للمنتج؟ يرجى [الاتصال بنا](/ar/contact/).
{{< /alert >}}

{{< faq >}}

[أدلة الإعداد والتفاصيل التقنية — doc.yupitek.com](https://doc.yupitek.com/alfa-network/products/awus036achm/)
