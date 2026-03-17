---
title: "الدعم التقني وتنزيل برامج التشغيل"
description: "مركز تنزيل برامج التشغيل الرسمي لمنتجات ALFA Network وHAK5 وFlipper Zero وUbiquiti."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
dir: rtl
---

فيما يلي روابط تنزيل برامج التشغيل والبرامج الثابتة الرسمية. يرجى زيارة الموقع الرسمي لكل علامة تجارية للحصول على أحدث الإصدارات.

{{< alert "circle-info" >}}
تنزيل برامج التشغيل دائماً من المواقع الرسمية للعلامات التجارية لضمان الأمان والتوافق.
{{< /alert >}}

<div class="my-6">
  <input
    type="text"
    id="driver-search"
    placeholder="ابحث عن الموديل، مثال: AWUS036ACH"
    oninput="filterDriverTable(this.value)"
    class="w-full px-4 py-3 rounded-lg border border-neutral-600 bg-neutral-800 text-neutral-200 placeholder-neutral-500 focus:outline-none focus:border-primary-400 text-sm"
    style="max-width:480px"
  />
</div>

<script>
function filterDriverTable(query) {
  var q = query.toLowerCase();
  var rows = document.querySelectorAll('table tbody tr');
  rows.forEach(function(row) {
    var cell = row.querySelector('td');
    if (!cell) return;
    row.style.display = cell.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
  });
}
</script>

## برامج تشغيل ALFA Network

### سلسلة Wi-Fi 6E

| Model | Chipset | تنزيل برنامج التشغيل | الوثائق الرسمية |
|-------|---------|------|------|
| AWUS036AXML | MT7921AUN | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AXML) | — |
| AWUS036AXM | MT7921AUN | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AXM) | — |
| AWUS036AX | RTL8832BU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AX) | — |
| AWUS036AXER | RTL8832BU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AXER) | — |

### سلسلة Wi-Fi 5

| Model | Chipset | تنزيل برنامج التشغيل | الوثائق الرسمية |
|-------|---------|------|------|
| AWUS1900 | RTL8814AU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS1900) | [Docs](https://docs.alfa.com.tw/Product/AWUS1900/) |
| AWUS036ACH | RTL8812AU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACH) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACH/) |
| AWUS036ACM | MT7612U | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACM) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACM/) |
| AWUS036ACS | RTL8811AU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACS) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACS/) |
| AWUS036EACS | RTL8811CU | — | — |
| AWUS036ACHM | MT7610U | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACHM) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACHM/) |

## موارد HAK5

| المورد | الرابط |
|------|------|
| وثائق HAK5 عبر الإنترنت | [docs.hak5.org](https://docs.hak5.org/hak5-docs/) |
| تنزيلات برامج HAK5 | [downloads.hak5.org](https://downloads.hak5.org/) |
| منتدى مجتمع HAK5 | [hak5.org/community](https://hak5.org/pages/community) |

## برنامج Flipper Zero

تفضل بزيارة [صفحة التنزيل الرسمية لـ Flipper Zero](https://flipper.net/pages/downloads) للحصول على أحدث البرامج.

## Ubiquiti UniFi

تفضل بزيارة [مركز التنزيل الرسمي لـ Ubiquiti](https://www.ui.com/download/) للحصول على أحدث البرامج الثابتة.

## استفسارات الدعم التقني

للحصول على مساعدة في تثبيت برامج التشغيل أو الاستفسارات التقنية، يرجى [التواصل معنا](/ar/contact/).
