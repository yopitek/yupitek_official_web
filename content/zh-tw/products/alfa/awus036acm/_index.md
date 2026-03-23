---
title: "ALFA AWUS036ACM — AC1200 雙頻 USB 3.0 無線網卡（Linux 免驅首選）"
description: "ALFA AWUS036ACM，MediaTek MT7612U，AC1200 雙頻 USB 3.0，內建 Linux 核心驅動（Kernel 4.19+），無需手動安裝，支援 Monitor Mode、Packet Injection 與 VIF，Raspberry Pi 首選。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "雙頻", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**合法使用聲明**：Monitor Mode 與 Packet Injection 功能僅供授權的資安測試、教育研究及合法滲透測試使用。請確認已取得目標網路的明確授權。
{{< /alert >}}

## 產品概述

AWUS036ACM 是 Linux 使用者免設定上手的首選網卡。其 MediaTek MT7612U 晶片組自 Linux 核心 4.19 版本起已內建於核心中，意味著在 Ubuntu、Kali Linux、Raspberry Pi OS、Arch Linux 及幾乎所有現代發行版上，無需編譯任何程式碼即可即插即用。外觀尺寸與天線配置與 AWUS036ACH 完全相同，但採用 MediaTek 更穩定的核心內建驅動。Monitor Mode、Packet Injection 與 VIF（虛擬介面）均完整支援。

> **macOS 注意事項：** 所有 ALFA 網卡對 macOS 支援有限。macOS 11+ 及 Apple Silicon（M1/M2/M3）均**不支援**。AWUS036ACM 最高支援 macOS 10.12 Sierra（比其他型號更嚴格）。

## 產品特色

- MediaTek MT7612U 晶片組 — 自 Linux 核心 4.19 起內建（免驅、無需編譯）
- WiFi 5（802.11ac）雙頻 AC1200 — 5 GHz 最高 867 Mbps，2.4 GHz 最高 300 Mbps
- 2× RP-SMA female 接頭搭配 2× 5 dBi 可拆卸雙頻天線 — 與 AWUS036ACH 完全相同的外觀格式
- USB 3.0（USB-A）介面
- 完整支援 Monitor Mode、Packet Injection 與 AP 模式
- 支援 Kali Linux VIF（虛擬介面）
- 附贈 USB 3.0 延長線
- TAA 認證 — 適用於美國政府採購（GSA 相容）
- Raspberry Pi OS 即插即用 — 無需安裝驅動程式

## 技術規格

| 項目 | 規格 |
|------|------|
| 晶片組 | MediaTek MT7612U |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n/ac（WiFi 5）|
| 頻率範圍 | 2.4 GHz（2.412–2.472 GHz）· 5 GHz（5.15–5.825 GHz）|
| 頻道寬度 | 20 / 40 / 80 MHz |
| 最高傳輸速率 | 5 GHz：最高 867 Mbps · 2.4 GHz：最高 300 Mbps |
| 合計最高速率 | AC1200（867 + 300 Mbps）|
| 天線接頭 | 2× RP-SMA female |
| 附贈天線 | 2× 雙頻偶極天線，5 dBi |
| USB 介面 | USB 3.0 Type-A（向下相容 USB 2.0）|
| 輸出功率 | 802.11a：20 dBm · 802.11b：23 dBm · 802.11g：23 dBm · 802.11n：21 dBm · 802.11ac：20 dBm |
| 接收靈敏度 | 802.11a：−92 dBm · 802.11b：−97 dBm · 802.11g：−90 dBm · 802.11n：−90 dBm |
| 無線安全 | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| 指示燈 | 有（電源 + 無線活動）|
| 附件 | USB 3.0 延長線 |
| 原產地 | 台灣 |

## 作業系統支援

| 作業系統 | 狀態 | 備註 |
|---------|------|------|
| Windows XP–11 | ✅ 支援 | 驅動程式請至 Alfa 官網下載，建議使用 Windows 10/11 |
| macOS 10.7–10.12 | ⚠️ 有限支援 | 官方支援至 macOS 10.12 Sierra，macOS 11+ 及 Apple Silicon 不支援 |
| Ubuntu 19.04+ | ✅ 即插即用 | 核心內建 mt76 驅動（核心 ≥ 4.19），Ubuntu 20.04 LTS 以上零設定安裝 |
| Kali Linux 2019.3+ | ✅ 即插即用 | 核心內建驅動，已確認 Monitor Mode，支援 VIF，5 GHz AP 模式可能需 `disable_usb_sg` 模組參數 |
| NetHunter（Android）| ✅ 支援 | OTG USB；核心內建驅動使其相容性優於 RTL 系列 |

## 硬體支援

| 硬體 | 狀態 | 備註 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 極佳 | Raspberry Pi OS 即插即用，無需安裝驅動，ALFA 網卡中 Pi 首選 |
| 桌機/筆電 | ✅ 支援 | 標準 USB-A，附贈延長線 |
| Mac（Intel）| ⚠️ 有限支援 | 僅限 macOS 10.7–10.12 |

## 進階功能

| 功能 | 狀態 |
|------|------|
| Monitor Mode | ✅ 支援（核心內建，現代發行版無需額外步驟）|
| Packet Injection | ✅ 支援 |
| Soft AP 模式 | ✅ 支援（5 GHz AP：加入 `disable_usb_sg` 模組參數以獲最佳效能）|
| 藍牙 | ❌ 不支援 |
| VIF（虛擬介面）| ✅ 支援（Kali 完整 VIF 支援）|

## 包裝內容

- 1× AWUS036ACM 無線網卡
- 2× 可拆卸 5 dBi 雙頻偶極天線
- 1× USB 3.0 延長線
- 1× 驅動程式光碟（Windows）

## 資源與連結

| 資源 | 連結 |
|------|------|
| 官方產品頁面 | https://www.alfa.com.tw/products/awus036acm_1 |
| 官方文件 | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Linux 驅動（核心內建）| mt76 驅動 — Linux 核心 ≥ 4.19 已內建，無需安裝 |

## 產品規格書下載

| 文件 | 下載 |
|------|------|
| 官方規格書（PDF） | [📄 下載 AWUS036ACM 規格書](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
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
