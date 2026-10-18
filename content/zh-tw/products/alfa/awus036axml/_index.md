---
title: "ALFA AWUS036AXML — Wi-Fi 6E USB-C 三頻無線網卡"
description: "ALFA AWUS036AXML，MediaTek MT7921AUN 晶片，Wi-Fi 6E 三頻（2.4/5/6 GHz），USB-C 介面，Bluetooth 5.2，支援 Kali Linux Monitor Mode。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "三頻", "藍牙 5.2", "6GHz", "Kali Linux"]
faq:
  - question: "AWUS036AXML 是否支援 6 GHz 頻段？"
    answer: "是。這是一款三頻 Wi-Fi 6E 轉接器，涵蓋 2.4 GHz、5 GHz 和 6 GHz，採用 MediaTek MT7921AUN 晶片組。在 Windows 上，6 GHz 需要 Windows 11。"
  - question: "AWUS036AXML 在 Linux 上是否需要安裝驅動程式？"
    answer: "不需要 DKMS 編譯。mt7921u 驅動程式自 Linux 核心版本 5.18 起已內建，因此您需要 5.18 或更新版本的核心，例如 Ubuntu 22.10 或更新版本，或是 Ubuntu 22.04 上的 HWE 核心。"
  - question: "AWUS036AXML 是否包含藍牙功能？"
    answer: "是。它在同一個 USB-C 轉接器中包含藍牙 5.2，因此單一裝置即可同時提供 Wi-Fi 和藍牙功能。"
---

{{< alert "warning" >}}
**合法使用聲明**：Monitor Mode 與 Packet Injection 功能僅供授權的資安測試、教育研究及合法滲透測試使用。請確認已取得目標網路的明確授權。
{{< /alert >}}

## 產品概述

AWUS036AXML 搭載 MediaTek MT7921AUN 晶片，支援 Wi-Fi 6E 三頻（2.4 GHz / 5 GHz / 6 GHz），最高傳輸速率達 3000 Mbps，並內建 Bluetooth 5.2。採用 USB-C 介面，附贈 2-in-1 USB-C/USB-A 傳輸線，完美適配現代筆電與桌機。2× RP-SMA 可拆卸天線搭配附贈螢幕夾架。

> **注意：** 所有 ALFA 無線網卡對 macOS 支援有限。macOS 11 Big Sur 以上及 Apple Silicon（M1/M2/M3）均**不支援**。最高支援版本為 Intel Mac 上的 macOS 10.15 Catalina。

## 產品特色

- Wi-Fi 6E 三頻：2.4 / 5 / 6 GHz
- MediaTek MT7921AUN 晶片
- 最高 3000 Mbps 傳輸速率
- Bluetooth 5.2（複合晶片）
- USB-C 介面（USB 3.2 Gen 1，5 Gbps）
- 附贈 2-in-1 USB-C/USB-A 傳輸線
- 2× RP-SMA 可拆卸天線
- 附贈螢幕夾架
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux Monitor Mode（核心 ≥ 5.18）

## 技術規格

| 項目 | 規格 |
|------|------|
| 晶片組 | MediaTek MT7921AUN |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6E）|
| 頻段 | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| 最高傳輸速率 | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · 合計: 3000 Mbps |
| 藍牙 | BT 5.2（複合晶片）|
| 天線接頭 | 2× RP-SMA female（可拆卸）|
| USB 介面 | USB 3.2 Gen 1 Type-C（5 Gbps）|
| 傳輸線 | 2-in-1 USB-C/USB-A |
| 無線安全 | WPA3 / WPA2 / WPA / WEP / WPS |
| 產地 | 台灣 |

## 作業系統支援

| 作業系統 | 狀態 | 備註 |
|---------|------|------|
| Windows 10 | ✅ 支援 | 僅 2.4 GHz 與 5 GHz；Windows 10 不支援 6 GHz |
| Windows 11 | ✅ 支援 | 完整三頻，含 6 GHz |
| macOS | ❌ 不支援 | 不支援 macOS 11+ 及 Apple Silicon |
| Ubuntu | ✅ 支援 | 核心內建 mt7921u，核心 ≥ 5.18（Ubuntu 22.10+）|
| Kali Linux | ✅ 支援 | Monitor mode ≥ 核心 5.18；主動 monitor mode ≥ 6.12；支援 packet injection |
| NetHunter（Android）| ⚠️ 部分支援 | OTG；依核心版本 |

## 硬體支援

| 硬體 | 狀態 | 備註 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 支援 | 更新 Pi OS（核心 ≥ 5.18）；可能需複製韌體檔 |
| 桌機/筆電 | ✅ 支援 | USB-C 或附贈 2-in-1 傳輸線 |
| Mac（Intel）| ⚠️ 有限支援 | 最高 macOS 10.15 Catalina |

## 進階功能

| 功能 | 狀態 |
|------|------|
| Monitor Mode | ✅ 支援（核心 ≥ 5.18；主動模式 ≥ 6.12）|
| Packet Injection | ✅ 支援 |
| Soft AP 模式 | ✅ 支援 |
| 藍牙 | ✅ BT 5.2 |
| VIF | ✅ 支援 |

## 包裝內容

- 1× AWUS036AXML 無線網卡
- 2× 可拆卸雙頻天線
- 1× 2-in-1 USB-C/USB-A 傳輸線
- 1× 螢幕夾架

## 資源與連結

| 資源 | 連結 |
|------|------|
| 官方產品頁面 | https://www.alfa.com.tw/products/awus036axml |
| 官方文件 | https://docs.alfa.com.tw/ |
| Linux 驅動（核心內建）| mt7921u — Linux 核心 ≥ 5.18 已內建 |

## 產品規格書下載

| 文件 | 下載 |
|------|------|
| 官方規格書（PDF） | [📄 下載 AWUS036AXML 規格書](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
{{< /gallery >}}

---

## 可搭配的天線配件

所有 ALFA USB 無線網卡均採用標準 RP-SMA 接頭，可搭配以下外接天線提升訊號範圍與增益：

| 天線型號 | 頻段 | 增益 | 類型 |
|---------|------|------|------|
| [ALFA APA-M04](/zh-tw/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 室內面板指向 |
| [ALFA APA-M25](/zh-tw/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | 雙頻室內面板 |
| [ALFA APA-M25-6E](/zh-tw/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | 三頻室內面板 |
| [ARS 25-57A](/zh-tw/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | 戶外全向 |
| [ARS NT5B7](/zh-tw/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | 全向 |

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}

{{< faq >}}
