---
title: "ALFA AWUS036EACS — AC600 + Bluetooth 4.2 迷你 USB 無線網路卡"
description: "ALFA AWUS036EACS，Realtek RTL8821CU，AC600 雙頻，USB 2.0 Nano 超輕薄，Bluetooth 4.2。核心 6.2 起內建 mainline rtw88_8821cu 驅動，GX10 實測 Monitor mode 與封包注入兩頻皆通過。"
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "家用", "Windows"]
---

## 產品概述

AWUS036EACS 是 Alfa Network 專為家用與辦公室設計的超小型 WiFi + Bluetooth 複合型 USB 無線網路卡。採用 Realtek RTL8821CU 晶片，整合 AC600 雙頻 WiFi 與 Bluetooth 4.2，Nano 機身設計插入 USB 埠後幾乎不佔空間。Windows 系統內建驅動支援，即插即用。支援 Soft AP 模式，可作為 WiFi 熱點分享網路。在 Linux 上，核心 6.2 起已內建 mainline rtw88_8821cu 驅動。於 GX10（Ubuntu 24.04、核心 6.17）實測，Monitor mode 與封包注入在 2.4 GHz 與 5 GHz 皆為 100%，端到端 WPA handshake 擷取成功，藍牙與 Wi-Fi 可同時使用。

> ⚠️ **注意：** AWUS036EACS 原為 Windows 家用機款，在 Linux 上亦可使用 mainline rtw88_8821cu 驅動（核心 6.2 以上）。無 RP-SMA 接頭，天線無法升級。

## 產品特色

- 802.11ac AC600 雙頻 WiFi + Bluetooth 4.2，單一 Nano USB 整合
- Windows 隨插即用，內建驅動程式自動安裝
- Soft AP 模式，可直接建立 WiFi 熱點
- 超迷你設計，插入 USB 埠幾乎無感
- 雙頻：2.4 GHz（150 Mbps）+ 5 GHz（433 Mbps）
- 整合式 2 dBi 天線，無外接 RP-SMA 接頭
- 適合桌上型電腦、嵌入式系統或家用 PC 同時需要 WiFi 與藍牙的場景
- Bluetooth 4.2 支援音訊串流、鍵盤、滑鼠等外接裝置

## 技術規格

| 項目 | 規格 |
|------|------|
| 晶片組 | Realtek RTL8821CU |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n/ac（Wi-Fi 5） |
| 藍牙 | BT 4.2（2.4 GHz） |
| 頻段 | WiFi：2.4 GHz / 5 GHz；BT：2.4 GHz |
| 最大傳輸速率 | 802.11b：11 Mbps · 802.11g：54 Mbps · 802.11n：150 Mbps · 802.11ac：433 Mbps |
| 綜合最高速率 | AC600（150 + 433 Mbps） |
| 天線 | 整合式 2 dBi（固定，無 RP-SMA） |
| USB 介面 | USB 2.0 |
| 輸出功率 | 典型值 17 dBm |
| 接收靈敏度 | 802.11b：−85 dBm · 802.11g：−69 dBm · 802.11n：−68 dBm · 802.11ac：−59 dBm |
| 無線加密 | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| 工作溫度 | −10°C 至 60°C |
| 外型規格 | Nano 超薄型 |
| 產地 | 台灣 |

## 作業系統支援

| 作業系統 | 支援狀態 | 備註 |
|---------|---------|------|
| Windows XP–10 | ✅ 支援 | 內建驅動，隨插即用。Windows 11 相容性請參閱 Alfa 驅動頁面。 |
| macOS | ⚠️ 有限支援 | 確切版本待確認，不支援 Apple Silicon。 |
| Ubuntu / Linux | ✅ 核心 6.2 以上 | 核心內建 mainline rtw88_8821cu 驅動，無需另外安裝（GX10、Ubuntu 24.04、核心 6.17 實測）。 |
| Kali Linux | ✅ 支援 | 於 GX10（Ubuntu 24.04、核心 6.17）實測 Monitor mode 與封包注入兩頻皆為 100%，端到端 WPA handshake 擷取成功。Kali 實機未實測。 |
| NetHunter（Android） | ❌ 不建議 | RTL8821CU 未確認與 NetHunter 相容。 |

## 硬體支援

| 硬體 | 支援狀態 | 備註 |
|------|---------|------|
| Raspberry Pi | ⚠️ 未實測 | 未實測；核心 6.2 以上已內建 mainline rtw88_8821cu 驅動。 |
| 桌上型／筆記型電腦 | ✅ 支援 | 僅建議 Windows 系統使用。 |
| 嵌入式 / IoT（Windows） | ⚠️ 僅限 Windows | 迷你設計適合 Windows 嵌入式系統。 |

## 進階功能

| 功能 | 支援狀態 |
|------|---------|
| Monitor Mode | ✅ 支援（GX10 實測：兩頻皆 100%） |
| 封包注入 | ✅ 支援（GX10 實測：兩頻皆 100%） |
| Soft AP 模式 | ✅ 支援 |
| Bluetooth | ✅ BT 4.2（可與 Wi-Fi 同時使用） |
| VIF | 🟡 部分支援（被動 monitor 與 managed 同頻道並存；不支援獨立雙 VIF） |

## 包裝內容

- 1× AWUS036EACS Nano 無線網路卡

## 資源與連結

| 資源 | 連結 |
|------|------|
| 原廠產品頁面 | https://www.alfa.com.tw/products/awus036eacs_1 |
| 原廠技術文件 | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## 產品規格書下載

規格書即將提供，敬請期待。

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## 可搭配的天線配件

所有 ALFA USB 無線網路卡均採用標準 RP-SMA 接頭，可搭配以下外接天線提升訊號範圍與增益：

| 天線型號 | 頻段 | 增益 | 類型 |
|---------|------|------|------|
| [ALFA APA-M04](/zh-tw/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 室內面板指向 |
| [ALFA APA-M25](/zh-tw/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | 雙頻室內面板 |
| [ALFA APA-M25-6E](/zh-tw/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | 三頻室內面板 |
| [ARS 25-57A](/zh-tw/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | 戶外全向 |
| [ARS NT5B7](/zh-tw/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | 全向 |

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}
