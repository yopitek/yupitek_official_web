---
title: "دليل إعداد ALFA AWUS036EACS للصين: تثبيت ويندوز وتوافق لينكس"
description: "دليل إعداد ALFA AWUS036EACS في الصين. محول نانو RTL8821CU WiFi 5 + Bluetooth 4.2. برنامج تشغيل ويندوز متاح في files.alfa.com.tw. لينكس و Kali Linux غير مدعومين — راجع البدائل الموصى بها."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 8
related_product: "/ar/products/alfa/awus036eacs/"
---

يعتبر AWUS036EACS محول نانو كومبو WiFi 5 + Bluetooth 4.2 من ALFA. تم تصميمه لمستخدمي ويندوز الذين يحتاجون إلى ترقية لاسلكية مدمجة. لا تحتوي شريحة RTL8821CU الخاصة به على برنامج تشغيل لينكس مفتوح المصدر موثوق — وضع المراقبة وحقن الحزم غير مدعومين. يغطي هذا الدليل تثبيت ويندوز من المصادر الصينية ويوضح قيود لينكس بوضوح.

## مستخدمو لينكس: يرجى القراءة أولاً

> **لا يعمل AWUS036EACS بشكل موثوق على Kali Linux أو Ubuntu أو Debian أو Raspberry Pi.** شريحة RTL8821CU ليس لها برنامج تشغيل مفتوح المصدر يتم صيانته. وضع المراقبة وحقن الحزم و VIF غير متاحة.
>
> إذا كنت بحاجة إلى محول متوافق مع لينكس لأبحاث الأمان، فاستخدم أحد هذه البدائل بدلاً من ذلك:
> - **[AWUS036ACM](/ar/blog/awus036acm-china-install-guide/)** — برنامج تشغيل MT7612U مدمج في النواة، وضع مراقبة كامل + VIF
> - **[AWUS036ACS](/ar/blog/awus036acs-china-install-guide/)** — RTL8811AU، وضع مراقبة مناسب للميزانية

---

## إعداد ويندوز 10 / 11

### الخطوة 1: تنزيل برنامج التشغيل من Alfa

يمكن الوصول إلى خادم برامج تشغيل Alfa الرسمي من الصين:

https://files.alfa.com.tw

انتقل إلى مجلد منتج **AWUS036EACS** وقم بتنزيل حزمة برنامج تشغيل ويندوز (`.zip` أو `.exe`).

بدلاً من ذلك، قم بزيارة صفحة الوثائق:
https://docs.alfa.com.tw/Product/AWUS036EACS/

### الخطوة 2: تثبيت برنامج التشغيل

1. قم بفك ضغط ملف zip الذي تم تنزيله.
2. انقر بزر الماوس الأيمن فوق ملف التثبيت `.exe` واختر **Run as administrator**.
3. اتبع التعليمات التي تظهر على الشاشة.
4. أعد التشغيل عند مطالبتك بذلك.

### الخطوة 3: التحقق من المحول

بعد إعادة التشغيل، افتح **Device Manager** (اضغط على Win+X ← Device Manager).

تحت **Network Adapters**، يجب أن ترى:

```
Realtek 8821CU Wireless LAN 802.11ac USB NIC
```

المحول جاهز الآن للاتصال بشبكات 2.4 جيجاهرتز و 5 جيجاهرتز.

### الخطوة 4: الاتصال بـ WiFi

1. انقر فوق أيقونة WiFi في شريط المهام.
2. اختر شبكتك.
3. أدخل كلمة المرور واتصل.

---

## إعداد البلوتوث (ويندوز)

يتضمن AWUS036EACS بلوتوث 4.2. بعد تثبيت برنامج التشغيل:

1. افتح **Settings → Bluetooth & devices**.
2. قم بتبديل Bluetooth إلى **On**.
3. انقر فوق **Add device** لإقران لوحات المفاتيح أو الماوس أو سماعات الرأس أو ملحقات البلوتوث الأخرى.

---

## تفاصيل توافق لينكس

### Kali Linux

لا تحتوي شريحة RTL8821CU على برنامج تشغيل DKMS يتم صيانته لنواة Kali الحديثة. توجد برامج تشغيل يحتفظ بها المجتمع ولكنها غير مستقرة — يبلغ المستخدمون عن فشل المحول وعدم استقرار النظام بعد تحديثات النواة. وضع المراقبة وحقن الحزم غير متاحين بشكل موثوق.

**التوصية:** استخدم [AWUS036ACM](/ar/blog/awus036acm-china-install-guide/) أو [AWUS036ACH](/ar/blog/awus036ach-china-install-guide/) لأعمال أمان Kali Linux.

### Ubuntu 22.04 / 24.04

يفتقر Ubuntu إلى دعم مستقر في النواة أو DKMS لـ RTL8821CU. وضع المراقبة وحقن الحزم و VIF غير مدعومة.

### Debian

نفس الوضع كما في Ubuntu. لا يوجد برنامج تشغيل مفتوح المصدر موثوق. لا ينصح به.

### Raspberry Pi

لا ينصح بشدة بـ RTL8821CU على Raspberry Pi. فشل تجميع برنامج التشغيل باستمرار على معماريات ARM. اختر [AWUS036ACM](/ar/blog/awus036acm-china-install-guide/) لمشاريع Pi بدلاً من ذلك.

---

## موارد الصين

| المورد | عنوان URL | الاستخدام |
|----------|-----|---------|
| برامج تشغيل Alfa الرسمية | [files.alfa.com.tw](https://files.alfa.com.tw) | برنامج تشغيل EACS لويندوز |
| وثائق Alfa | [docs.alfa.com.tw](https://docs.alfa.com.tw) | دليل الإعداد، الأسئلة الشائعة |
| ويكي Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات |

## المزيد من أدلة محولات Alfa للصين

- [دليل تثبيت AWUS036ACH في الصين](/ar/blog/awus036ach-china-install-guide/) — RTL8812AU، طاقة عالية
- [دليل تثبيت AWUS036ACM في الصين](/ar/blog/awus036acm-china-install-guide/) — MT7612U، دعم VIF كامل
- [دليل تثبيت AWUS036ACS في الصين](/ar/blog/awus036acs-china-install-guide/) — RTL8811AU، وضع المراقبة
- [دليل تثبيت AWUS036AX في الصين](/ar/blog/awus036ax-china-install-guide/) — RTL8832BU، WiFi 6
- [دليل تثبيت AWUS036AXER في الصين](/ar/blog/awus036axer-china-install-guide/) — RTL8832BU، نانو
- [دليل تثبيت AWUS036AXM في الصين](/ar/blog/awus036axm-china-install-guide/) — MT7921AUN، شكل L
- [دليل تثبيت AWUS036AXML في الصين](/ar/blog/awus036axml-china-install-guide/) — MT7921AUN، WiFi 6E
- AWUS036EACS ← أنت هنا

هل لديك أسئلة؟ اترك تعليقًا أدناه أو اتصل بنا على [yupitek.com](https://yupitek.com/ar/contact/).
