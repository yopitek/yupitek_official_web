---
title: "Technical Support & Driver Downloads"
description: "Yupitek official driver download center for ALFA Network, HAK5, Flipper Zero, and Ubiquiti products."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

The following are official driver and firmware download links. Please visit each brand's official website for the latest versions.

{{< alert "circle-info" >}}
Always download drivers from official brand websites to ensure security and compatibility.
{{< /alert >}}

<div class="my-6">
  <input
    type="text"
    id="driver-search"
    placeholder="Search model, e.g.: AWUS036ACH"
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

## ALFA Network Drivers

### Wi-Fi 6E Series

| Model | Chipset | Driver Download | Documentation |
|-------|---------|------|------|
| AWUS036AXML | MT7921AUN | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AXML) | — |
| AWUS036AXM | MT7921AUN | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AXM) | — |
| AWUS036AX | RTL8832BU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AX) | — |
| AWUS036AXER | RTL8832BU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036AXER) | — |

### Wi-Fi 5 Series

| Model | Chipset | Driver Download | Documentation |
|-------|---------|------|------|
| AWUS1900 | RTL8814AU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS1900) | [Docs](https://docs.alfa.com.tw/Product/AWUS1900/) |
| AWUS036ACH | RTL8812AU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACH) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACH/) |
| AWUS036ACM | MT7612U | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACM) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACM/) |
| AWUS036ACS | RTL8811AU | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACS) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACS/) |
| AWUS036EACS | RTL8811CU | — | — |
| AWUS036ACHM | MT7610U | [Download](https://files.alfa.com.tw/?dir=%5B1%5D%20WiFi%20USB%20adapter/AWUS036ACHM) | [Docs](https://docs.alfa.com.tw/Product/AWUS036ACHM/) |

## HAK5 Resources

| Resource | Link |
|------|------|
| HAK5 Online Documentation | [docs.hak5.org](https://docs.hak5.org/hak5-docs/) |
| HAK5 Software Downloads | [downloads.hak5.org](https://downloads.hak5.org/) |
| HAK5 Community Forum | [hak5.org/community](https://hak5.org/pages/community) |

## Flipper Zero Software

Visit the [Flipper Zero official download page](https://flipper.net/pages/downloads) for the latest software.

## Ubiquiti UniFi

Visit the [Ubiquiti official download center](https://www.ui.com/download/) for the latest firmware and management software.

## Technical Support Inquiries

For driver installation assistance or technical inquiries, please [contact us](/en/contact/).
