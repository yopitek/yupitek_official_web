---
title: "ALFA AWUS036AX — Wi-Fi 6 雙頻 USB 無線網卡"
description: "ALFA AWUS036AX，Realtek RTL8832BU 晶片，Wi-Fi 6（802.11ax）雙頻 2.4+5 GHz，最高 1200 Mbps，USB 3.0。注意：此為 Wi-Fi 6，非 Wi-Fi 6E，不含 6 GHz 頻段。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "USB 3.0", "802.11ax", "雙頻", "OFDMA", "MU-MIMO"]
---

## 產品概述

AWUS036AX 採用 Realtek RTL8832BU 晶片，支援 Wi-Fi 6（802.11ax）雙頻（2.4 GHz + 5 GHz），最高傳輸速率 1200 Mbps，支援 MU-MIMO 2×2 與 OFDMA 技術。天線為一體化設計（不可拆卸）。

> ⚠️ **重要提示：** 此型號為 **Wi-Fi 6**，並非 Wi-Fi 6E，**不含 6 GHz 頻段**。若需 6 GHz 頻段，請選擇 AWUS036AXML 或 AWUS036AXM。此型號在核心 < 6.12 時 Monitor mode 受限，**不建議用於 Linux 資安研究**。

> **注意：** 所有 ALFA 無線網卡對 macOS 支援有限。macOS 11 Big Sur 以上及 Apple Silicon（M1/M2/M3）均**不支援**。最高支援版本為 Intel Mac 上的 macOS 10.15 Catalina。

## 產品特色

- Wi-Fi 6（802.11ax）雙頻：2.4 GHz + 5 GHz
- Realtek RTL8832BU 晶片
- 最高 1200 Mbps 傳輸速率
- MU-MIMO 2×2
- OFDMA 技術
- USB 3.0 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ 不含 6 GHz 頻段

## 技術規格

| 項目 | 規格 |
|------|------|
| 晶片組 | Realtek RTL8832BU |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6）|
| 頻段 | 2.4 GHz + 5 GHz（無 6 GHz）|
| 最高傳輸速率 | 1200 Mbps |
| MIMO | MU-MIMO 2×2 |
| 天線 | 一體化（不可拆卸）|
| USB 介面 | USB 3.0 Type-A |
| 無線安全 | WPA3 / WPA2 / WPA / WEP |

## 作業系統支援

| 作業系統 | 狀態 | 備註 |
|---------|------|------|
| Windows 10/11 | ✅ 支援 | 從 Alfa 官網下載驅動 |
| macOS | ❌ 不支援 | 不支援 macOS 11+ 及 Apple Silicon |
| Ubuntu | ⚠️ 需安裝驅動 | 核心 ≥ 6.14（Ubuntu 24.10+）已內建；舊版需手動 DKMS |
| Kali Linux | ⚠️ 有限 | 核心 < 6.12 時 Monitor mode 受限；不建議用於滲透測試 |
| NetHunter | ⚠️ 有限 | 依核心版本 |

## 硬體支援

| 硬體 | 狀態 | 備註 |
|------|------|------|
| Raspberry Pi 4/5 | ⚠️ 需安裝驅動 | Pi OS 核心 < 6.14 需手動安裝 |
| 桌機/筆電 | ✅ 支援 | 標準 USB-A |

## 進階功能

| 功能 | 狀態 |
|------|------|
| Monitor Mode | ⚠️ 有限（建議核心 ≥ 6.12）|
| Packet Injection | ⚠️ 有限 |
| Soft AP 模式 | ✅ 支援 |
| 藍牙 | ❌ 無 |

## 包裝內容

- 1× AWUS036AX 無線網卡

## 資源與連結

| 資源 | 連結 |
|------|------|
| 官方文件 | https://docs.alfa.com.tw/ |
| Linux 驅動（RTL8832BU）| https://github.com/morrownr/rtl8852bu-20240418 |

## 產品規格書下載

| 文件 | 下載 |
|------|------|
| 官方規格書（PDF） | [📄 下載 AWUS036AX 規格書](/docs/alfa/AWUS036AX_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ax_image_1.png" alt="ALFA AWUS036AX" />
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
需要詢問報價？[聯絡我們](/zh-tw/contact/)，我們提供詳細採購建議。
{{< /alert >}}
