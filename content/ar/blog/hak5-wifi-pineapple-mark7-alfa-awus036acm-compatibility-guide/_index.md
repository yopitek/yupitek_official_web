---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: دليل الإعداد الكامل 5GHz (2026)"
description: "دليل التوافق الكامل لـ HAK5 WiFi Pineapple MK7 مع ALFA AWUS036ACM (MT7612U) — وضع المراقبة 5GHz، حقن الحزم، وتوسيع PineAP. إعداد خطوة بخطوة مع أوامر موثقة. لا حاجة لتجميع التعريفات."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "هل تحتاج WiFi Pineapple Mark VII إلى محول خارجي؟"
    answer: "نعم. اللاسلكي المدمج في MK7 يدعم 2.4 GHz فقط، ومعظم الشبكات انتقلت إلى 5 GHz في 2026. محول AWUS036ACM الخارجي يضيف قدرة مراقبة وحقن 5 GHz."
  - question: "لماذا يعمل AWUS036ACM فور التوصيل على MK7؟"
    answer: "برنامج MK7 Firmware 2.x يأتي محملاً مسبقاً بتعريف kmod-mt76x2u، وشريحة MT7612U مدمجة في النواة منذ 4.19، دون تجميع أو تثبيت."
  - question: "هل يحد USB 2.0 من أداء AWUS036ACM على MK7؟"
    answer: "USB 2.0 يحد الإنتاجية إلى 150-250 Mbps، لكن أحمال اختبار الاختراق مثل التقاط الحزم وجمع المصافحات لا تتأثر. فقط الجسر عالي الإنتاجية محدود."
  - question: "كيف أفعّل وضع المراقبة على MK7؟"
    answer: "عبر SSH نفّذ airmon-ng start wlan3، ستُعاد تسمية الواجهة إلى wlan3mon، تحقق بالوضع عبر iwconfig."
  - question: "ما محولات ALFA غير المتوافقة مع MK7؟"
    answer: "AWUS036AX و AWUS036AXER يستخدمان RTL8832BU، و AWUS036EACS يستخدم RTL8811CU. تعريفاتها لا تدعم وضع المراقبة أو الحقن، جميعها غير متوافقة."
---
جهاز HAK5 WiFi Pineapple Mark VII هو المعيار الذهبي لتدقيق الأمن اللاسلكي المحمول. لكنه يأتي بقيود: الراديو المدمج يعمل فقط على **2.4 GHz**. في عام 2026، انتقلت معظم الشبكات إلى 5 GHz.

{{< tldr >}}
يستخدم AWUS036ACM شريحة MT7612U، MK7 Firmware 2.x يأتي بتعريف محمّل مسبقاً، بعد التوصيل يظهر كواجهة wlan3، يدعم مراقبة 5 GHz وحقن الحزم وامتداد PineAP، جاهز خلال 10 دقائق.
{{< /tldr >}}


هنا يأتي دور **ALFA AWUS036ACM**. إنه أحد المحولات القليلة [المؤكدة رسمياً من Hak5](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) للتوافق، ويعمل **بدون تجميع للتعريفات** بفضل تعريف `mt76x2u` المدمج في نواة MK7 Firmware 2.x.

---

## 1. المواصفات

| المكون | المواصفة |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **USB Host** | 1× USB 2.0 Type-A |

> ✅ `kmod-mt76x2u` محمل مسبقاً في Firmware 2.x — **توصيل وتشغيل**.

---

## 2. ALFA AWUS036ACM

| المواصفة | التفاصيل |
|---|---|
| **الشريحة** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **النطاقات** | 2.4 GHz + 5 GHz |
| **وضع المراقبة** | ✅ مدعوم |
| **حقن الحزم** | ✅ مدعوم |

---

## 3. الإعداد

```bash
ssh root@172.16.42.1
lsusb                          # التحقق من USB
lsmod | grep mt76              # التحقق من التعريف
iw dev                         # التحقق من الواجهة
airmon-ng check kill           # تفعيل وضع المراقبة
airmon-ng start wlan3
iw wlan3mon set channel 36     # مسح 5 GHz
airodump-ng --band a wlan3mon
aireplay-ng --test wlan3mon    # اختبار الحقن
```

---

## 4. النتائج — جميع الاختبارات ناجحة ✅

---

{{< faq >}}

## 5. التوصية

**ALFA AWUS036ACM هو أفضل محول متاح لتوسيع WiFi Pineapple Mark VII إلى 5 GHz.**

👉 [صفحة منتج AWUS036ACM](/ar/products/alfa/awus036acm/)

*هل تحتاج مساعدة؟ اتصل بدعم Yupitek: [yupitek.com/support](/ar/support/)*

## المراجع

1. [وثائق Hak5 الرسمية — قائمة محولات 802.11ac المتوافقة](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [مستودع تعريف OpenWrt mt76 — GitHub](https://github.com/openwrt/mt76)
3. [aircrack-ng — موقع مجموعة أدوات الأمن اللاسلكي الرسمي](https://www.aircrack-ng.org/)
4. [موقع ALFA Network الرسمي — مواصفات منتج AWUS036ACM](https://www.alfa.com.tw/)
5. [Linux Wireless — وثائق تعريف MT76x2U](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
