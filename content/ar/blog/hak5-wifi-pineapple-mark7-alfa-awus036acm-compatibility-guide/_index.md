---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: دليل الإعداد الكامل 5GHz (2026)"
description: "دليل التوافق الكامل لـ HAK5 WiFi Pineapple MK7 مع ALFA AWUS036ACM (MT7612U) — وضع المراقبة 5GHz، حقن الحزم، وتوسيع PineAP. إعداد خطوة بخطوة مع أوامر موثقة. لا حاجة لتجميع التعريفات."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

جهاز HAK5 WiFi Pineapple Mark VII هو المعيار الذهبي لتدقيق الأمن اللاسلكي المحمول. لكنه يأتي بقيود: الراديو المدمج يعمل فقط على **2.4 GHz**. في عام 2026، انتقلت معظم الشبكات إلى 5 GHz.

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

## 5. التوصية

**ALFA AWUS036ACM هو أفضل محول متاح لتوسيع WiFi Pineapple Mark VII إلى 5 GHz.**

👉 [صفحة منتج AWUS036ACM](/ar/products/alfa/awus036acm/)

*هل تحتاج مساعدة؟ اتصل بدعم Yupitek: [yupitek.com/support](/ar/support/)*
