---
title: "منارة YPB01 BLE 5.0"
description: "منارة YPB01 BLE 5.0. تقنية البلوتوث منخفض الطاقة BLE 5.0، لتحديد المواقع وحضور الموظفين وتتبع الأصول."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof"]
---

## نظرة عامة على المنتج

إنّ **YPB01** هو منارة بلوتوث منخفض الطاقة (BLE 5.0) صغيرة وقوية، مصممة لأنظمة تحديد المواقع الداخلية ومراقبة النشاط وتتبع الأصول. تعتمد على رقاقة nRF52 ذات الاستهلاك المنخفض للغاية، وتبث إطارات iBeacon و Eddystone (UID, URL, TLM) في وقت واحد.

يسمح هيكلها الدوار الميكانيكي الذكي باستبدال بطارية العملة المعدنية بسهولة مع تحقيق تصنيف مقاومة الماء والغبار IP67، مما يجعلها مثالية للبيئات الرطبة أو الصعبة.

---

## الميزات الرئيسية

* **هيكل حماية عالٍ:** تصنيف IP67 مقاوم للماء والغبار، مما يسمح بالتركيب الداخلي والخارجي الخفيف.
* **بطارية قابلة للاستبدال:** بطارية CR2477 طويلة الأمد (1000 مللي أمبير) سهلة الاستبدال عبر الهيكل الدوار.
* **بث متزامن:** يدعم البث في ما يصل إلى 6 فتحات إعلانية مختلفة في وقت واحد لبروتوكولات iBeacon و Eddystone.
* **زر طاقة مادي:** زر ضغط داخلي لتشغيل أو إيقاف المنارة لحفظ البطارية أثناء النقل والتخزين.

---

## دليل التشغيل

### كيفية تشغيل المنارة
1. افتح الهيكل الدوار باتجاه عقارب الساعة.
2. اضغط مع الاستمرار على "الزر الداخلي" لمدة **3 ثوانٍ**.
3. سيضيء مؤشر LED الأزرق لمدة **5 ثوانٍ** ثم ينطفئ. منارة YPB01 نشطة الآن وتبث.

### كيفية إيقاف تشغيل المنارة
1. اضغط مع الاستمرار على الزر الداخلي لمدة **3 ثوانٍ**.
2. سيومض مؤشر LED الأزرق لمدة **5 ثوانٍ** ثم ينطفئ. المنارة مغلقة الآن.

---

## إرشادات التهيئة

يتم تهيئة معلمات YPB01 (بما في ذلك UUID و Major و Minor وقوة الإرسال وفاصل البث) لاسلكياً عبر تطبيق **BeaconSET**:
1. قم بتنزيل **BeaconSET** من Google Play أو Apple App Store.
2. تأكد من تمكين خدمات البلوتوث والموقع على هاتفك.
3. افتح التطبيق، وامسح ضوئياً بحثاً عن عنوان MAC للمنارة، وانقر للاتصال.
4. أدخل كلمة مرور التهيئة الافتراضية الآمنة لفتح وتعديل المعلمات.

## Technical Specifications

| المعيار | المواصفات | ملاحظات |
| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
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
  <img src="/images/products/ibeacon/ypb01.png" alt="Yupitek YPB01" />
{{< /gallery >}}

---

{{< alert >}}
هل تحتاج إلى عرض أسعار مخصص أو حل تكامل؟ يرجى الاتصال بفريق المبيعات لدينا مباشرة على: **sales@yupitek.com**
{{< /alert >}}
