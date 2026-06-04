---
title: "منارة YPB02 BLE بمستشعر حركة"
description: "منارة YPB02 BLE بمستشعر حركة. تقنية البلوتوث منخفض الطاقة BLE 5.0، لتحديد المواقع وحضور الموظفين وتتبع الأصول."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## نظرة عامة على المنتج

إنّ **YPB02** هو منارة بلوتوث منخفض الطاقة (BLE 5.0) مستشعرة للحركة ومجهزة بمستشعر تسارع ثلاثي المحاور **LIS3DH**. تشارك نفس الحجم الصغير، والبطارية القابلة للاستبدال CR2477 (1000 مللي أمبير)، والهيكل المقاوم للماء والغبار IP67 للمنارة YPB01، ولكن يضيف YPB02 كشف الحركة الذكي والقياس عن بعد.

تدعم المنارة البث المعتمد على المحفزات، مما يسمح لها ببث بيانات التسارع في الوقت الفعلي أو تعديل فاصل البث فقط عند الحركة أو الاهتزاز أو في حالة السقوط.

---

## الميزات الرئيسية

* **مستشعر تسارع ثلاثي المحاور:** مستشعر LIS3DH لرسم خرائط الحركة والميل على محاور X و Y و Z.
* **البث المعتمد على المحفزات:** يدعم التهيئة لبث الحركة فقط، وتنبيهات السقوط، أو تغيير الفاصل إلى 100 مللي ثانية عند الحركة.
* **هيكل حماية عالٍ:** تصنيف IP67 مقاوم للماء والغبار.
* **بطارية قابلة للاستبدال:** استخدام بطارية CR2477 طويلة الأمد سهلة الاستبدال.

---

## استشعار الحركة والقياس عن بعد

باستخدام مستشعر LIS3DH، يدعم YPB02:
1. **البث القائم على النشاط:** يبث إطارات قياسية باستمرار، ولكنه يحفز إطارات بيانات المستشعر فقط عند الحركة.
2. **الوضع المزدوج:** يظل صامتاً في وضع السكون عند الثبات، ويبث بفاصل 100 مللي ثانية عند الحركة.
3. **معايرة العتبة:** يمكن تخصيص عتبات التسارع ومدة المحفز داخل التطبيق.

---

## إرشادات التهيئة

يتم تهيئة المعلمات لاسلكياً عبر تطبيق **BeaconSET+**:
1. قم بتنزيل **BeaconSET+**.
2. تأكد من تمكين خدمات البلوتوث والموقع.
3. امسح واتصل بالمنارة عبر عنوان MAC.
4. أدخل كلمة المرور لتعديل وحفظ المعلمات.

## Technical Specifications

| المعيار | المواصفات | ملاحظات |
| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Sensor** | LIS3DH 3-axis accelerometer | X, Y, Z axes telemetry |
| **Transmission Range** | Up to 100 meters | Open space |
| **Antenna Impedance** | 50 ohm | On-board / PCB Antenna |
| **Power Source** | 1 × CR2477 coin battery | Replaceable (3.0V, 1000mAh) |
| **Operating Voltage** | 1.8V - 3.9V | DC |
| **Peak Current** | 5.3 mA | Tested at 0dBm transmission power |
| **Dimensions** | Φ39 × 15.5 mm | Compact circular shape |
| **Default Settings** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## معرض صور المنتج

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02" />
{{< /gallery >}}

---

{{< alert >}}
هل تحتاج إلى عرض أسعار مخصص أو حل تكامل؟ يرجى الاتصال بفريق المبيعات لدينا مباشرة على: **sales@yupitek.com**
{{< /alert >}}
