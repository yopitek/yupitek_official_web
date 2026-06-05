---
title: "ALFA AWUS036AXM — Wi-Fi 6E 三頻雙天線無線網卡"
description: "ALFA AWUS036AXM，MediaTek MT7921AUN 晶片，Wi-Fi 6E 三頻，USB-A L 型接頭，2× 5 dBi 天線，Bluetooth 5.2，適合 Kali Linux 滲透測試。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-A", "802.11ax", "三頻", "藍牙 5.2", "雙天線", "Kali Linux"]
---

{{< alert "warning" >}}
**合法使用聲明**：Monitor Mode 與 Packet Injection 功能僅供授權的資安測試、教育研究及合法滲透測試使用。請確認已取得目標網路的明確授權。
{{< /alert >}}

## 產品概述

AWUS036AXM 採用 MediaTek MT7921AUN 晶片，支援 Wi-Fi 6E 三頻（2.4 GHz / 5 GHz / 6 GHz），最高傳輸速率達 3000 Mbps，並內建 Bluetooth 5.2（含獨立 BT 天線）。L 型 USB-A 接頭可避免擋住相鄰 USB 埠。附贈 2 根 5 dBi RP-SMA 可拆卸天線。

> **注意：** 所有 ALFA 無線網卡對 macOS 支援有限。macOS 11 Big Sur 以上及 Apple Silicon（M1/M2/M3）均**不支援**。最高支援版本為 Intel Mac 上的 macOS 10.15 Catalina。

## 產品特色

- Wi-Fi 6E 三頻：2.4 / 5 / 6 GHz
- MediaTek MT7921AUN 晶片
- 最高 3000 Mbps 傳輸速率
- Bluetooth 5.2（含獨立 BT 天線及 LED 指示燈）
- USB-A L 型接頭（USB 3.2 Gen 1，5 Gbps）
- 2× RP-SMA female 可拆卸天線（5 dBi）
- WPA3/WPA2/WPA/WEP/WPS
- 支援 Kali Linux Monitor Mode + Packet Injection

## 技術規格

| 項目 | 規格 |
|------|------|
| 晶片組 | MediaTek MT7921AUN |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6E）|
| 頻段 | 2.4 GHz · 5 GHz · 6 GHz |
| 最高傳輸速率 | 3000 Mbps |
| 藍牙 | BT 5.2（含獨立天線）|
| 天線 | 2× RP-SMA female，2× 5 dBi 雙頻天線（可拆卸）|
| USB 介面 | USB 3.2 Gen 1 Type-A L 型（5 Gbps）|
| 無線安全 | WPA3 / WPA2 / WPA / WEP / WPS |

## 作業系統支援

| 作業系統 | 狀態 | 備註 |
|---------|------|------|
| Windows 10 | ✅ 支援 | 2.4+5 GHz；6 GHz 需 Windows 11 |
| Windows 11 | ✅ 支援 | 完整三頻含 6 GHz |
| macOS | ❌ 不支援 | 不支援 macOS 11+ 及 Apple Silicon |
| Ubuntu | ✅ 支援 | 核心內建 mt7921u，核心 ≥ 5.18 |
| Kali Linux | ✅ 支援 | Monitor mode + packet injection；可能需韌體檔 |
| NetHunter | ⚠️ 部分支援 | OTG；依核心版本 |

## 硬體支援

| 硬體 | 狀態 | 備註 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 支援 | 更新 Pi OS（核心 ≥ 5.18）|
| 桌機/筆電 | ✅ 支援 | L 型 USB-A 接頭不擋鄰埠 |
| Mac（Intel）| ⚠️ 有限支援 | 最高 macOS 10.15 Catalina |

## 進階功能

| 功能 | 狀態 |
|------|------|
| Monitor Mode | ✅ 支援 |
| Packet Injection | ✅ 支援 |
| Soft AP 模式 | ✅ 支援 |
| 藍牙 | ✅ BT 5.2（含獨立 BT 天線）|
| VIF | ✅ 支援 |

## 包裝內容

- 1× AWUS036AXM 無線網卡
- 2× 5 dBi 天線
- 快速設定指南

## 資源與連結

| 資源 | 連結 |
|------|------|
| 官方產品頁面 | https://www.alfa.com.tw/products/awus036axm |
| 官方文件 | https://docs.alfa.com.tw/ |
| Linux 驅動 | mt7921u — Linux 核心 ≥ 5.18 已內建 |

## 產品規格書下載

| 文件 | 下載 |
|------|------|
| 官方規格書（PDF） | [📄 下載 AWUS036AXM 規格書](/docs/alfa/AWUS036AXM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axm_image_1.png" alt="ALFA AWUS036AXM" />
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
