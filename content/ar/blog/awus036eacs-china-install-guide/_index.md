---
title: "دليل إعداد ALFA AWUS036EACS للصين: تثبيت ويندوز وتوافق لينكس"
description: "دليل إعداد ALFA AWUS036EACS في الصين. محول نانو RTL8821CU WiFi 5 + Bluetooth 4.2. برنامج تشغيل ويندوز متاح في files.alfa.com.tw. على نواة لينكس 6.2 فأحدث يعمل تعريف rtw88_8821cu المدمج بمجرد التوصيل، ووضع المراقبة والحقن مُختبران ويعملان."
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
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ما الشريحة التي يستخدمها AWUS036EACS؟ هل يدعم Bluetooth؟"
    answer: "يستخدم شريحة Realtek RTL8821CU ويدعم WiFi 5 و Bluetooth 4.2."
  - question: "هل يُنصح AWUS036EACS للاستخدام على Linux؟"
    answer: "نعم. على نواة لينكس 6.2 فأحدث (مثل Ubuntu 24.04 HWE / kernel 6.17) يكون تعريف rtw88_8821cu مدمجاً في النواة، بدون أي تجميع ويعمل بمجرد التوصيل. قِسنا وضع المراقبة وحقن الحزم بنسبة 100% على النطاقين (2.4 جيجاهرتز / 5 جيجاهرتز) مع التقاط مصافحة WPA من طرف إلى طرف (.22000)، كما أن Bluetooth مُختبر ويعمل."
  - question: "كيف أثبّت تعريف AWUS036EACS على Windows؟"
    answer: "نزّل حزمة تعريف Windows من موقع Alfa files.alfa.com.tw، ثبّتها كمسؤول ثم أعد التشغيل."
  - question: "كيف أفعل Bluetooth على AWUS036EACS؟"
    answer: "بعد تثبيت التعريف يُفعّل عادةً تلقائياً، افتح مفتاح Bluetooth في إعدادات Windows للاتصال بالأجهزة."
  - question: "إذا كنت بحاجة لمحول أبحاث أمن لاسلكي على Linux، ماذا أختار؟"
    answer: "محول AWUS036EACS نفسه يعمل لوضع المراقبة وحقن الحزم على النواة 6.2 فأحدث، مع Bluetooth كميزة إضافية. وإذا أردت خيارات أكثر، فإن AWUS036ACM و AWUS036ACS يدعمان أيضاً وضع المراقبة بالكامل على Linux. استخدمه فقط على الشبكات التي تملكها أو مُصرّح لك باختبارها."
---
يعتبر AWUS036EACS محول نانو كومبو WiFi 5 + Bluetooth 4.2 من ALFA. إنه ترقية لاسلكية مدمجة لمستخدمي ويندوز، وعلى نواة لينكس 6.2 فأحدث يدعمه تعريف rtw88_8821cu المدمج بمجرد التوصيل (بدون تجميع). يغطي هذا الدليل تثبيت ويندوز من المصادر الصينية وتجربة الاستخدام على لينكس.

{{< tldr >}}
يستخدم AWUS036EACS شريحة RTL8821CU، محول WiFi 5 مدمج بـ Bluetooth 4.2. تثبيت Windows سهل؛ وعلى نواة لينكس 6.2 فأحدث يكون تعريف rtw88_8821cu مدمجاً، فيعمل وضع المراقبة وحقن الحزم بمجرد التوصيل، كما أن Bluetooth مُختبر ويعمل.
{{< /tldr >}}

> **يعمل AWUS036EACS بمجرد التوصيل على نواة لينكس 6.2 فأحدث.** النوى 6.2 فأحدث (مثل Ubuntu 24.04 HWE / kernel 6.17) تتضمن تعريف rtw88_8821cu المدمج في النواة، لذا لا حاجة لأي تجميع. قِسنا وضع المراقبة وحقن الحزم بنسبة 100% على النطاقين (2.4 جيجاهرتز / 5 جيجاهرتز)، والتقطنا مصافحة WPA من طرف إلى طرف (.22000)، كما أن Bluetooth (BT) مُختبر ويعمل (كل من BR/EDR و BLE يمسح الأجهزة ويتعايش مع WiFi). استخدمه فقط على الشبكات التي تملكها أو مُصرّح لك باختبارها.
>
> **ملاحظة تشغيلية:** هذه بطاقة مدمجة BT+WiFi. بعد تبديل الأوضاع بشكل متكرر، قد يتوقف استقبال WiFi (يُرجع `ip link set up` الرسالة `Operation already in progress`، ويُرجع `iw ... set channel` الرسالة `-16 busy`). قبل كل مرحلة اختبار، افصل المحول وأعد توصيله في منفذ USB آخر لاستعادة عمله.
>
> محولات لينكس أخرى في نفس السلسلة:
> - **[AWUS036ACM](/ar/blog/awus036acm-china-install-guide/)** — برنامج تشغيل MT7612U مدمج في النواة، وضع مراقبة كامل + VIF
> - **[AWUS036ACS](/ar/blog/awus036acs-china-install-guide/)** — RTL8811AU، وضع مراقبة مناسب للميزانية



## مستخدمو لينكس: يرجى القراءة أولاً

> **يعمل AWUS036EACS بمجرد التوصيل على نواة لينكس 6.2 فأحدث.** النوى 6.2 فأحدث (مثل Ubuntu 24.04 HWE / kernel 6.17) تتضمن تعريف rtw88_8821cu المدمج في النواة، لذا لا حاجة لأي تجميع. قِسنا وضع المراقبة وحقن الحزم بنسبة 100% على النطاقين (2.4 جيجاهرتز / 5 جيجاهرتز)، والتقطنا مصافحة WPA من طرف إلى طرف (.22000)، كما أن Bluetooth (BT) مُختبر ويعمل (كل من BR/EDR و BLE يمسح الأجهزة ويتعايش مع WiFi). استخدمه فقط على الشبكات التي تملكها أو مُصرّح لك باختبارها.
>
> **ملاحظة تشغيلية:** هذه بطاقة مدمجة BT+WiFi. بعد تبديل الأوضاع بشكل متكرر، قد يتوقف استقبال WiFi (يُرجع `ip link set up` الرسالة `Operation already in progress`، ويُرجع `iw ... set channel` الرسالة `-16 busy`). قبل كل مرحلة اختبار، افصل المحول وأعد توصيله في منفذ USB آخر لاستعادة عمله.
>
> محولات لينكس أخرى في نفس السلسلة:
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

على **النواة 6.2 فأحدث**، تُدار شريحة RTL8821CU بواسطة وحدة `rtw88_8821cu` المدمجة في النواة، لذا لا شيء يحتاج إلى تجميع — وصّلها فيتم التعرف عليها. تحقق أولاً من إصدار نواتك بالأمر `uname -r`.

### Kali Linux

مع نواة 6.2 فأحدث، يُحمّل تعريف `rtw88_8821cu` المدمج تلقائياً. اختبرنا وضع المراقبة وحقن الحزم بنسبة 100% على النطاقين (2.4 جيجاهرتز / 5 جيجاهرتز) والتقطنا مصافحة WPA من طرف إلى طرف (.22000). استخدمه فقط على الشبكات التي تملكها أو مُصرّح لك باختبارها.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu 22.04 / 24.04

يأتي Ubuntu 24.04 مزوداً بتعريف `rtw88_8821cu` المدمج في النواة (ضمن mainline منذ النواة 6.2) سواء مع نواة GA 6.8 أو نواة HWE (مثل kernel 6.17) — فيعمل وضع المراقبة وحقن الحزم واتصالات العميل بمجرد التوصيل. على نواة أقدم (أقل من 6.2، مثل نواة GA في Ubuntu 22.04)، حدّث إلى نواة HWE للحصول على التعريف المدمج.

### Debian / Raspberry Pi

نفس القصة: بمجرد أن تكون النواة 6.2 فأحدث (بما في ذلك إصدارات ARM64)، يتعامل تعريف `rtw88_8821cu` المدمج مع المحول دون أي تجميع.

### ملاحظة تشغيلية (بطاقة مدمجة BT+WiFi)

لأن EACS يحمل كلاً من Bluetooth و WiFi على شريحة واحدة، قد يؤدي تبديل الأوضاع بشكل متكرر إلى توقف استقبال WiFi — يُرجع `ip link set up` الرسالة `Operation already in progress` ويُرجع `iw ... set channel` الرسالة `-16 busy`. قبل كل مرحلة اختبار، افصل المحول وأعد توصيله في منفذ USB آخر لمسح الحالة. Bluetooth (BR/EDR + BLE) مُختبر ويعمل ويتعايش مع WiFi.

---

## موارد الصين

| المورد | عنوان URL | الاستخدام |
|----------|-----|---------|
| برامج تشغيل Alfa الرسمية | [files.alfa.com.tw](https://files.alfa.com.tw) | برنامج تشغيل EACS لويندوز |
| وثائق Alfa | [docs.alfa.com.tw](https://docs.alfa.com.tw) | دليل الإعداد، الأسئلة الشائعة |
| ويكي Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | أدلة المنتجات |

{{< faq >}}

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

## المراجع

1. [موقع ALFA Network الرسمي](https://www.alfa.com.tw/)
2. [تنزيل تعريفات Alfa الرسمية](https://files.alfa.com.tw)
3. [موقع Realtek الرسمي](https://www.realtek.com/)
