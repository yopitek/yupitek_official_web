---
title: "SDRLab Flipper Zero 5G لوحة التوسعة — وحدة أبحاث أمان Wi-Fi ثنائية النطاق"
description: "لوحة توسعة Flipper Zero 5G، RTL8720DN Wi-Fi ثنائي النطاق (2.4+5GHz)، BLE 5.0، برنامج Deauth مُثبَّت مسبقاً، GPIO، متوافق مع Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["توسعة Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "أبحاث الأمن"]
dir: rtl
---
{{< alert "warning" >}}
**إشعار الاستخدام القانوني**: هذه اللوحة التوسعة مخصصة لأبحاث الأمن المرخصة والبحث العلمي القانوني فقط. يُرجى التحقق من الامتثال للوائح استخدام الترددات اللاسلكية المحلية.
{{< /alert >}}

## الميزات
![SDRLab Flipper Zero 5G لوحة التوسعة](/images/products/sdrlab/flipper-5g.png)
- مبنية على وحدة AI Thinker BW16 (شريحة Realtek RTL8720DN) مع دعم أصلي لـ Wi-Fi 5 GHz
- تغطية ثنائية النطاق (2.4 GHz + 5 GHz)، قادرة على استشعار بيئات الشبكات اللاسلكية الحديثة ثنائية النطاق
- برنامج إلغاء مصادقة Wi-Fi 5G (Deauth) مُحمَّل مسبقاً، جاهز للتوصيل والتشغيل
- تعمل مباشرة بالطاقة من GPIO في Flipper Zero، دون الحاجة إلى مصدر طاقة إضافي
- تدعم التعرف على هياكل شبكات Mesh ومسح البيئة اللاسلكية
- متوافقة مع أطر عمل Momentum وUnleashed
- تدعم PlatformIO للتطوير الثانوي وحرق البرامج الثابتة المخصصة
- نواة Cortex-M0 منخفضة الاستهلاك لإطالة وقت التشغيل في الميدان

## المواصفات
| المواصفة | القيمة / الوصف |
|---------|-----------|
| الشريحة الرئيسية | Realtek RTL8720DN (وحدة AI Thinker BW16) |
| وحدة المعالجة المركزية | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| معيار Wi-Fi | IEEE 802.11 a/b/g/n (2.4 GHz + 5 GHz ثنائي النطاق) |
| البلوتوث | BLE 5.0 |
| ذاكرة Flash | 4 MB |
| مصدر الطاقة | GPIO لـ Flipper Zero (5 V) |
| واجهة الاتصال | دبابيس GPIO القياسية لـ Flipper Zero |
| البرنامج الثابت المُحمَّل | 5G Wi-Fi Deauth Firmware |
| توافق البرنامج الثابت | Momentum، Unleashed |
| التطوير الثانوي | يدعم PlatformIO |
| درجة حرارة التشغيل | −40°C إلى 85°C |
| واجهة الهوائي | IPEX (U.FL) أو هوائي PCB مدمج في اللوحة (حسب الإصدار) |

## بيئات الاستخدام
- مسح نطاق Wi-Fi 5 GHz وتحليل البيئة اللاسلكية
- أبحاث أمان إلغاء مصادقة الشبكة اللاسلكية (Deauth)
- تطوير نماذج أولية لنقاط وصول خبيثة (Evil Portal)
- اختبار فيضان Beacon (Beacon Flood)
- التعرف على هياكل شبكات Mesh
- تطوير وتشخيص بروتوكولات IoT اللاسلكية
- تعليم اختبار اختراق Wi-Fi في البيئات المرخصة

---
{{< gallery >}}
  <img src="/images/products/sdrlab/flipper-5g.png" alt="SDRLab Flipper Zero 5G لوحة التوسعة" />
{{< /gallery >}}

---
{{< alert >}}
هل تريد الاستفسار عن الأسعار؟ [اتصل بنا](/ar/contact/)
{{< /alert >}}
