---
title: "ALFA AWUS036ACS — AC600 雙頻 USB 無線網卡（入門資安研究）"
description: "ALFA AWUS036ACS，Realtek RTL8811AU，AC600 雙頻 USB 2.0，1× 2 dBi RP-SMA 可拆卸天線，支援 Monitor Mode 與 Packet Injection，入門級資安研究首選。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "入門"]
---

{{< alert "warning" >}}
**合法使用聲明**：Monitor Mode 與 Packet Injection 功能僅供授權的資安測試、教育研究及合法滲透測試使用。請確認已取得目標網路的明確授權。
{{< /alert >}}

## 產品概述

AWUS036ACS 是 Alfa 雙頻 802.11ac 產品線中最經濟實惠的入門款，搭載 Realtek RTL8811AU 晶片，支援 Monitor Mode 與 Packet Injection。機身輕巧小型，配備 1 支可拆卸 RP-SMA 天線，可依需求升級為高增益或方向性天線。雖然效能不及 ACH 或 ACM，但對於初學者或需要預算友好型 5 GHz 外接天線網卡的使用者而言，是十分實用的選擇。

> **macOS 注意事項：** 所有 ALFA 網卡對 macOS 支援有限。macOS 10.15 Catalina 以上及 Apple Silicon（M1/M2/M3）均**不支援**。AWUS036ACS 最高支援 macOS 10.14 Mojave（Intel Mac）。

## 產品特色

- Realtek RTL8811AU 晶片 — 支援 Monitor Mode 與 Packet Injection
- WiFi 5（802.11ac）雙頻 — 2.4 GHz（150 Mbps）+ 5 GHz（433 Mbps）= AC600
- 1× RP-SMA 母頭連接器，附 1× 2 dBi 迷你可拆卸天線 — 可升級為面板天線或高增益天線
- 輕巧小型機身 — 方便攜帶
- USB 2.0（USB-A）介面 — 相容所有 USB 連接埠
- 相容 Alfa APA-M25 雙頻面板天線，可實現方向性接收
- 支援 Kali Linux on Raspberry Pi（KaliPi）— 透過 DKMS 安裝驅動程式

## 技術規格

| 參數 | 規格 |
|---|---|
| 晶片組 | Realtek RTL8811AU |
| 無線標準 | IEEE 802.11 a/b/g/n/ac（WiFi 5） |
| 頻段 | 2.4 GHz（150 Mbps）· 5 GHz（433 Mbps） |
| 最大合計速率 | AC600（150 + 433 Mbps） |
| 天線連接器 | 1× RP-SMA 母頭 |
| 隨附天線 | 1× 雙頻全向迷你偶極天線，2 dBi |
| USB 介面 | USB 2.0 Type-A |
| 接收靈敏度 | 802.11b：−85 dBm · 802.11g：−69 dBm · 802.11n：−68 dBm · 802.11ac：−59 dBm |
| 無線安全 | WPA2 / WPA / WEP / 802.1X |
| 原產地 | 台灣 |

> ⚠️ **注意：** 僅支援 USB 2.0，最高匯流排速度 480 Mbps，傳輸速率上限為 433 Mbps。如需更高速度，請選擇搭載 USB 3.0 的 AWUS036ACM 或 AWUS036ACH。

## 作業系統支援

| 作業系統 | 狀態 | 備註 |
|---|---|---|
| Windows XP–11 | ✅ 支援 | 驅動程式請至 Alfa 官網下載 |
| macOS 10.5–10.14 | ⚠️ 有限支援 | macOS 10.15+ 及 Apple Silicon 不支援 |
| Ubuntu | ✅ 支援 | 需手動安裝 DKMS 驅動（morrownr/8821au），無核心內建支援 |
| Kali Linux | ✅ 支援 | 支援 Monitor Mode + Packet Injection，使用 morrownr GitHub 社群驅動 |
| NetHunter（Android） | ✅ 支援 | OTG USB 連接；RTL8811AU 已確認相容 NetHunter |

## 硬體支援

| 硬體 | 狀態 | 備註 |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ 支援 | 可透過 morrownr DKMS 安裝 KaliPi 專用驅動 |
| 桌機／筆電 | ✅ 支援 | 標準 USB-A 連接 |
| Mac（Intel） | ⚠️ 有限支援 | 僅支援 macOS 10.5–10.14 |

## 進階功能

| 功能 | 狀態 |
|---|---|
| Monitor Mode（監聽模式） | ✅ 支援 |
| Packet Injection（封包注入） | ✅ 支援 |
| Soft AP 模式 | ✅ 支援 |
| 藍牙 | ❌ 不支援 |
| VIF（虛擬介面） | ⚠️ 有限支援 |

## 包裝內容

- 1× AWUS036ACS 無線網卡
- 1× 可拆卸 2 dBi 雙頻迷你偶極天線

## 資源與連結

| 資源 | 連結 |
|---|---|
| 官方產品頁面 | https://www.alfa.com.tw/products/awus036acs_1 |
| 官方技術文件 | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Linux 驅動（RTL8811AU） | https://github.com/morrownr/8821au-20210708 |

## 產品規格書下載

| 文件 | 連結 |
|---|---|
| 官方規格書（PDF） | [📄 下載 AWUS036ACS 規格書](/docs/alfa/AWUS036ACS_spec.pdf) |

## 產品圖片

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

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

{{< alert "info" >}}
需要詢問報價？[聯絡我們](/zh-tw/contact/)，我們提供詳細採購建議。
{{< /alert >}}
