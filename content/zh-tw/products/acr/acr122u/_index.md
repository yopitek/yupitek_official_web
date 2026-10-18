---
title: "ACS ACR122U — USB NFC 讀卡機"
description: "ACS ACR122U，USB NFC 讀卡機，支援 ISO 14443 A/B、MIFARE、FeliCa，13.56MHz，適合 NFC 研究與應用開發。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["acr"]
tags: ["NFC", "RFID", "ISO 14443", "MIFARE", "USB", "讀卡機"]
faq:
  - question: "在 Windows 上是否需要為 ACR122U 安裝 ACS 驅動程式？"
    answer: "不需要。ACS 表示 ACR122U 符合 PC/SC 標準，並使用標準的 Microsoft CCID 驅動程式，因此在 Windows 上不需要 ACS 驅動程式，因為該驅動程式已內建於作業系統中。"
  - question: "ACR122U 可以讀取和寫入哪些卡片與標籤？"
    answer: "根據 ACS 的說明，它可存取 ISO 14443-4 Type A 和 Type B 卡片、MIFARE、FeliCa 以及所有四種類型的 NFC (ISO/IEC 18092) 標籤，卡片讀取距離依標籤類型而定，最遠可達 50 mm。其內建的防衝突機制確保一次僅存取一個標籤。"
  - question: "如何在我自己的應用程式中對 ACR122U 進行程式設計？"
    answer: "ACR122U 支援 PC/SC，並透過 PC/SC 之上的 wrapper 支援 CT-API。針對 ISO 18092 標籤以及 LED 和蜂鳴器的指令，是以 pseudo-APDUs 的形式傳送。ACS 也列出了對 Android 3.1 及以上版本的支援。"
---

ACR122U

## 產品概述

ACR122U 是 ACS 基於 13.56 MHz RFID 技術的 PC 連接式非接觸智慧卡讀寫機，符合 ISO/IEC 18092 NFC 標準，支援 MIFARE®、ISO 14443 Type A/B 及全部四種 NFC 標籤類型。符合 PC/SC 及 CCID 規範的即插即用 USB 裝置，存取速度最高達 424 Kbps，USB 全速（12 Mbps）介面，操作距離最遠可達 50 mm。

## 主要規格

| 規格項目 | 內容 |
|----------|------|
| 工作頻率 | 13.56 MHz |
| 操作距離 | 最遠 50 mm（依標籤類型而異） |
| 讀寫速度 | 106 Kbps / 212 Kbps / 424 Kbps |
| USB 介面 | USB 全速（12 Mbps） |
| 供電電壓 | 5V DC 穩壓 |
| 供電電流 | 最大 200 mA |
| 天線尺寸 | 50 mm × 40 mm |
| 外觀尺寸 | 98 × 65 × 12.8 mm |
| 重量 | 70 g |
| 工作溫度 | 0°C – 60°C |
| 濕度 | 最大 90%（非冷凝） |
| MTBF | 408,500 小時 |
| LED | 1 個雙色 紅/綠（使用者可控） |
| 蜂鳴器 | 單音調（使用者可控） |
| 合規認證 | PC/SC、CCID、CE、FCC、RoHS |

## 主要功能

- USB 全速介面
- 符合 CCID 及 PC/SC 規範，即插即用
- 讀寫速度最高達 424 Kbps
- 內建天線，卡片讀取距離最遠達 50 mm
- 支援全部 4 種 NFC 標籤類型（ISO/IEC 18092）
- 支援 ISO 14443 Type A/B、MIFARE、FeliCa 及 NFC 標籤的讀寫器
- 內建防衝突機制（每次一張標籤）
- 使用者可控雙色 LED 及蜂鳴器
- 支援 PC/SC 及 CT-API

## 支援標籤型號

| 標籤 / 卡片類型 | 標準依據 |
|-----------------|----------|
| MIFARE Classic（1K、4K、MINI） | ISO 14443 Type A |
| FeliCa | ISO 18092 |
| ISO 14443 Type A 卡片 | ISO 14443 |
| ISO 14443 Type B 卡片 | ISO 14443 |

## 支援作業系統

- Windows CE 5.0、Windows Embedded Compact 6.0 / 7
- Windows XP、Vista、7、8、8.1、10
- Windows Server 2003 / 2008 / 2012 / 2016
- Linux®
- macOS®
- Solaris
- Android™ 3.1 及以上版本


## 📄 產品規格書

| 資源 | 連結 |
|----------|------|
| 📄 ACR122U 規格書 (PDF) | [下載 PDF](/docs/acr/ACR122U_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/acr/acr122u.webp" alt="ACS ACR122U NFC 讀卡機" />
{{< /gallery >}}

---

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}

{{< faq >}}

[安裝指南與技術細節 — doc.yupitek.com](https://doc.yupitek.com/acs/products/acr122u/)
