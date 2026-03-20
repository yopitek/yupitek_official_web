---
title: "ALFA AWUS036ACH — AC1200 雙頻高功率 USB-C 無線網卡"
description: "ALFA AWUS036ACH，Realtek RTL8812AU，AC1200 雙頻，USB-C，雙 5 dBi 外接天線，Kali Linux 資安研究黃金標準，支援 Monitor Mode 與 Packet Injection。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "雙天線", "Monitor Mode", "Kali Linux", "資安研究"]
---

{{< alert "warning" >}}
**合法使用聲明**：Monitor Mode 與 Packet Injection 功能僅供授權的資安測試、教育研究及合法滲透測試使用。請確認已取得目標網路的明確授權。
{{< /alert >}}

## 產品概述

AWUS036ACH 是 ALFA Network 資安研究社群公認的黃金標準無線網卡，自 2017 年起即為 Kali Linux 滲透測試的首選機款。採用 Realtek RTL8812AU 晶片，具備穩定的 Monitor Mode 與 Packet Injection 支援，內建功率放大器提升遠距感測能力，配備兩根可拆卸 5 dBi 天線。本機為全球首款搭載 USB Type-C 介面的 Wi-Fi 5 USB 網卡。

> **macOS 注意事項：** 所有 ALFA 網卡對 macOS 支援有限。macOS 11 Big Sur 以上版本及 Apple Silicon（M1/M2/M3）均**不支援**，最高支援為 Intel Mac 上的 macOS 10.15 Catalina。

## 產品特色

- Realtek RTL8812AU 晶片 — 資安研究社群記錄最完整的晶片組
- Wi-Fi 5（802.11ac）AC1200 雙頻：5 GHz 867 Mbps + 2.4 GHz 300 Mbps
- 內建功率放大器 — 接收距離最高達一般筆電內建網卡的 3 倍
- 2× RP-SMA female 天線接頭搭配 2× 5 dBi 可拆卸雙頻天線（可升級高增益天線）
- 全球首款 Wi-Fi 5 USB Type-C 介面無線網卡
- 附贈螢幕夾架
- Kali Linux Packet Injection 支援自 Kali 2017.1 起
- 相容 802.11a/b/g/n

## 技術規格

| 項目 | 規格 |
|------|------|
| 晶片組 | Realtek RTL8812AU |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n/ac（Wi-Fi 5） |
| 頻段 | 雙頻 2.4 GHz / 5 GHz |
| 最高傳輸速率 | 802.11b: 11 Mbps · 802.11a/g: 54 Mbps · 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| 合計最高速率 | AC1200（867 + 300 Mbps） |
| 天線接頭 | 2× RP-SMA female |
| 內附天線 | 2× 雙頻全向偶極天線，5 dBi |
| USB 介面 | Type-C SuperSpeed USB（5 Gbps）；相容 USB 2.0 |
| 功率放大器 | 有 — 延伸接收距離 |
| 無線安全 | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| 產地 | 台灣 |

## 作業系統支援

| 作業系統 | 狀態 | 備註 |
|---------|------|------|
| Windows 10/11 | ✅ 支援 | 請至 ALFA 官網下載驅動；WPA3 支援（2019 年 10 月驅動後） |
| macOS 10.15 Catalina | ⚠️ 有限支援 | 需手動安裝；不支援 macOS 11+ 及 Apple Silicon |
| Ubuntu | ✅ 支援 | 需透過 DKMS 手動安裝 RTL8812AU 驅動；Ubuntu 24.10+（核心 ≥ 6.14）起內建 |
| Kali Linux | ✅ 優異 | 自 Kali 2017.1 起支援；完整 Monitor Mode + Packet Injection；建議使用 aircrack-ng 驅動 |
| NetHunter（Android） | ✅ 支援 | OTG USB 連接；廣泛確認可用 |

## 硬體支援

| 硬體 | 狀態 | 備註 |
|------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 支援 | 透過 morrownr DKMS 腳本手動安裝驅動 |
| 桌機/筆電 | ✅ 支援 | USB-C 或附贈傳輸線 |
| Mac（Intel） | ⚠️ 有限支援 | 最高 macOS 10.15 Catalina |

## 進階功能

| 功能 | 狀態 |
|------|------|
| Monitor Mode | ✅ 優異（黃金標準 — 社群驗證自 2017 年起） |
| Packet Injection | ✅ 優異 |
| Soft AP 模式 | ✅ 支援 |
| 藍牙 | ❌ 無 |
| VIF | ⚠️ 有限（如需完整 VIF 支援，請選 AWUS036ACM） |

## 包裝內容

- 1× AWUS036ACH 無線網卡
- 2× 可拆卸 5 dBi 雙頻偶極天線
- 1× USB-C to USB-A 傳輸線
- 1× 螢幕夾架

## 資源與連結

| 資源 | 連結 |
|------|------|
| 官方產品頁面 | https://www.alfa.com.tw/products/awus036ach_1 |
| 官方文件 | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| 驅動（aircrack-ng，Kali 推薦）| https://github.com/aircrack-ng/rtl8812au |
| 驅動（morrownr，一般 Linux） | https://github.com/morrownr/8812au-20210708 |

## 產品規格書下載

| 文件 | 下載 |
|------|------|
| 官方規格書（PDF） | [📄 下載 AWUS036ACH 規格書](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
{{< /gallery >}}

---

{{< alert >}}
需要詢問報價？[聯絡我們](/zh-tw/contact/)，我們提供詳細採購建議。
{{< /alert >}}
