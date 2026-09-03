---
title: "ALFA 無線網卡是否支援 Tomato"
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "路由器韌體"
description: "目前 ALFA 全系列現役機型在 Tomato（含 FreshTomato / AdvancedTomato 等衍生版本）上均無驅動支援，完全不建議使用。Tomato 是三大第三方路由器韌體中對 USB WiFi 支援最弱的平台，其開發重心完全放在 Broadcom 晶片路由器的內建 WiFi 上。若需要在路由器上使用 USB WiFi 網卡，應改用 OpenWrt。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網卡能否在刷了 Tomato 韌體的路由器上使用？」

簡短結論：目前 ALFA 全系列現役機型在 Tomato（含 FreshTomato / AdvancedTomato 等衍生版本）上均無驅動支援，完全不建議使用。Tomato 是三大第三方路由器韌體中對 USB WiFi 支援最弱的平台，其開發重心完全放在 Broadcom 晶片路由器的內建 WiFi 上。若需要在路由器上使用 USB WiFi 網卡，應改用 OpenWrt。

判定母體：ALFA 現役 9 款 USB 網卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目標軟體規格與需求

### 2.1 Tomato 是什麼

Tomato 是一款歷史悠久的開源路由器第三方韌體，最初由 Jonathan Zarate 開發，後續衍生出多個分支：

| 衍生版本 | 維護狀態 | 支援平台 |
|---|---|---|
| 原版 Tomato | 已停止維護（2010 年代初） | Broadcom MIPS 路由器 |
| Tomato by Shibby | 已停止維護 | Broadcom MIPS / ARM |
| AdvancedTomato | 已停止維護 | Broadcom（Shibby 分支的 GUI 改版） |
| FreshTomato | 活躍維護中 | Broadcom MIPS / ARM（BCM47xx / BCM53xx） |
| Toastman Tomato | 已停止維護 | Broadcom MIPS |

### 2.2 Tomato 的 USB WiFi 支援框架

Tomato 的核心設計哲學是「為 Broadcom 路由器提供精簡、穩定的第三方韌體」，其 USB 功能主要支援：

| USB 功能類型 | 支援狀態 |
|---|---|
| USB 儲存裝置（隨身碟 / 硬碟） | ✅ 完整支援（Samba / FTP / DLNA） |
| USB 印表機 | ✅ 支援（p910nd / CUPS） |
| USB 3G/4G 數據機 | ⚠️ 部分支援 |
| USB WiFi 網卡 | ❌ 幾乎不支援 |

Tomato 的核心（kernel）預設僅編入 Broadcom 路由器內建 WiFi 的閉源驅動（wl 模組），沒有任何 USB WiFi 驅動。其套件管理系統（ipkg / Optware）也不提供 USB WiFi 驅動套件。

### 2.3 關鍵限制

- Tomato 僅支援 Broadcom 晶片的路由器，而 Broadcom 路由器的 USB 埠通常僅用於儲存 / 印表機
- FreshTomato 雖仍在維護，但開發重點是修復 Broadcom 平台的 bug，不會新增 USB WiFi 驅動
- Tomato 的檔案系統空間極小（通常 4-16MB），即使想手動編譯驅動也沒有空間安裝
- Tomato 沒有 opkg 等現代套件管理系統，無法像 OpenWrt 一樣簡單安裝 kmod 驅動

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網卡產品線如下（判定母體：9 款）：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | Tomato 驅動狀態 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ 無 |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ 無 |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ 無 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ 無 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ 無 |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ❌ 無 |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ 無 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ❌ 無 |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ❌ 無 |

## 4. 適用機型與晶片組

### 4.1 在 Tomato 上可能可用的極舊型 ALFA 機型（已停產）

| 機型 | 晶片組 | Linux 驅動模組 | 說明 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 理論上可載入，但 Tomato 未預設編入；需自行編譯 kernel module，實際可行性極低 |
| AWUS036H | Realtek RTL8187L | rtl8187 | 同上，僅 2.4GHz / 54Mbps，已停產超過十年 |

⚠️ 即使是上述舊型機型，在 Tomato 上也需要使用者自行交叉編譯對應 kernel 版本的驅動模組，且 Tomato 的檔案系統空間通常不足以安裝。這不屬於「支援」，而是「極度進階的 hack」。

### 4.2 在 Tomato 上完全不可用的現役機型

所有現役 ALFA 機型（見第 3 節表格）在 Tomato 上均不可用，原因：

- Realtek 晶片（RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU）：Tomato 無任何對應驅動，也無法透過套件管理安裝
- MediaTek 晶片（MT7612U / MT7610U / MT7921AUN）：Tomato 未編入 mt76 / mt7921 驅動，且 FreshTomato 開發團隊無計劃加入
- 即使 lsusb 能看到裝置（若 Tomato 有啟用 USB 核心），也僅是 USB 匯流排層級的辨識，無法建立網路介面

## 5. 環境需求

由於現役 ALFA 機型在 Tomato 上不可用，本節列出「若客戶堅持嘗試」所需的極端條件：

| 項目 | 需求 |
|---|---|
| 路由器硬體 | Broadcom 晶片路由器，有 USB 2.0 埠，Flash ≥ 32MB，RAM ≥ 256MB |
| Tomato 版本 | FreshTomato 最新版（舊版 USB 支援更差） |
| 交叉編譯環境 | 需搭建對應 Broadcom 架構（MIPS / ARM）的 Tomato 交叉編譯工具鏈 |
| 驅動原始碼 | 需自行取得對應晶片的 Linux 驅動原始碼，並修改為符合 Tomato kernel 版本 |
| 技術能力 | 需具備 Linux kernel module 開發、交叉編譯、除錯能力 |
| 時間成本 | 預計數小時至數天，且成功機率低 |

結論：對於 99.9% 的使用者，在 Tomato 上使用 ALFA USB WiFi 網卡是不可行的。

## 6. 相容性判定

### ALFA 現役機型 × Tomato 相容性矩陣

| 機型 | 晶片組 | USB 核心支援 | USB 偵測 | STA 上網 | AP 模式 | Monitor | 綜合評價 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ 需啟用 USB 核心 | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036EACS | RTL8811CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不支援 |

判定依據：Tomato（含 FreshTomato）官方核心與套件庫均未包含任何現代 USB WiFi 晶片驅動。Tomato 的設計目標從未包含 USB WiFi 擴充功能。

## 7. 超詳細 Step by Step 設定步驟

由於現役 ALFA 機型在 Tomato 上不可用，本節提供驗證步驟與替代方案。

### 7.1 驗證你的 Tomato 路由器是否支援 USB WiFi（除錯步驟）

**步驟 1：登入 Tomato 管理介面**

瀏覽器輸入 192.168.1.1（或你的路由器 IP）。

**步驟 2：檢查 USB 核心是否啟用**

- 進入 USB and NAS > USB Support
- 確認 Core USB Support、USB 2.0 Support、USB 3.0 Support（若有）已勾選
- 確認 USB Wireless Device Support（若有此選項）— 多數 Tomato 版本無此選項

**步驟 3：插入 ALFA 網卡到路由器 USB 埠**

**步驟 4：透過 SSH / Telnet 登入路由器檢查 USB 偵測**

```bash
# 檢查是否有 lsusb（Tomato 預設可能沒有）
which lsusb
# 若無 lsusb，檢查 /proc/bus/usb 或 dmesg
cat /proc/bus/usb/devices
# 或
dmesg | grep -i usb
```

**步驟 5：檢查網路介面**

```bash
ifconfig -a
# 若僅有 vlan0 / br0 / eth0 / eth1（路由器內建介面），無 wlan0 / wlan1，代表 USB WiFi 未被驅動
```

**步驟 6：檢查可用的 kernel module**

```bash
lsmod
# 預期僅有 wl（Broadcom 內建 WiFi 驅動）、et（乙太網路驅動）等
# 不會有 mt76 / rtl8812 / cfg80211 / mac80211 等 USB WiFi 驅動
```

**步驟 7：檢查是否可安裝額外套件**

```bash
# Tomato 使用 ipkg，但套件庫內容極少
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 預期結果為空
```

### 7.2 建議替代方案

#### 方案一：改用 OpenWrt（強烈推薦）

若你的路由器型號同時支援 OpenWrt，建議將韌體從 Tomato 改刷為 OpenWrt。OpenWrt 有完整的 USB WiFi 驅動套件庫，可支援多數 ALFA 機型。

- 確認你的路由器是否在 OpenWrt 支援裝置列表中
- 若支援，參考 [ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) 的安裝步驟

#### 方案二：使用路由器內建 WiFi

Tomato 對 Broadcom 路由器的內建 WiFi 支援完善，若你的需求是一般上網或 AP 熱點，直接使用路由器內建 WiFi 即可，不需外接 ALFA 網卡。

#### 方案三：更換硬體

若你需要 USB WiFi 的特定功能（如高功率輸出、監聽模式、封包注入），Tomato 平台無法滿足需求。建議：

- 使用支援 OpenWrt 的路由器 + ALFA 網卡
- 或使用 x86 小主機安裝 OpenWrt / pfSense + ALFA 網卡
- 或直接在 Kali Linux / Ubuntu 電腦上使用 ALFA 網卡

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| Tomato 管理介面沒有「USB Wireless Device Support」選項 | 該 Tomato 版本未編譯 USB WiFi 支援 | 這是常態，不是 bug；Tomato 多數版本無此功能 |
| 插入 ALFA 網卡後 dmesg 有 USB 偵測但無網路介面 | 缺少驅動 | 無法解決，Tomato 無對應驅動 |
| 想手動安裝 ipkg 套件但找不到 WiFi 驅動 | Tomato 套件庫無 USB WiFi 驅動 | 這是常態；建議改用 OpenWrt |
| 舊型 ALFA（RT3070）在 Tomato 上可偵測但無法連線 | 驅動不完全 / firmware 缺失 | 即使舊型晶片也不保證可用；建議在 OpenWrt 上使用 |
| 路由器刷了 Tomato 後 USB 埠僅能讀隨身碟 | Tomato 的 USB 功能設計僅限儲存 / 印表機 | 這是預期行為；Tomato 不支援 USB WiFi |

## 9. 已知限制

- 完全沒有 USB WiFi 驅動：Tomato（含 FreshTomato）官方核心不包含任何現代 USB WiFi 晶片驅動，這是最根本的限制
- Broadcom 閉源驅動綁定：Tomato 依賴 Broadcom 的閉源 wl 驅動，無法與開源 mac80211 / cfg80211 架構的 USB WiFi 驅動共存
- 無套件管理生態：Tomato 的 ipkg 套件庫內容極少，不像 OpenWrt 有數千個可安裝套件
- Flash / RAM 空間不足：多數 Tomato 路由器僅 4-16MB Flash，即使編譯出驅動也無空間安裝
- 開發方向不同：FreshTomato 開發團隊的優先事項是修復 Broadcom 平台穩定性，不會投入資源新增 USB WiFi 支援
- 監聽 / 注入完全不支援：Tomato 的 WiFi 架構（Broadcom wl 驅動）本身就不支援滲透測試功能，外接 USB WiFi 也無法改變這一點
- 無 AP 模式擴充：即使舊型晶片可載入驅動，Tomato 的網路設定介面不支援設定 USB WiFi 的 AP 模式

反駁條件：若 FreshTomato 未來版本在官方 release notes 中明確新增 USB WiFi 驅動支援，或社群出現經廣泛驗證的 FreshTomato mt76 / rtl8812au 模組移植專案，本文第 6 節「不支援」判定需重新檢視；若 FreshTomato 改用開源 mac80211 架構核心，限制說明亦需更新。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| FreshTomato 官方網站 | FreshTomato 最新版本與支援裝置列表 | https://freshtomato.org/ | ✅ 已查核 | 2026-09-03 |
| OpenWrt 官方文檔 | USB WiFi 驅動與無線設定（對比參考） | https://openwrt.org/docs/start | ✅ 已查核 | 2026-09-03 |
| OpenWrt 官方論壇 | USB WiFi 驅動討論（對比參考） | https://forum.openwrt.org/ | ✅ 已查核 | 2026-09-03 |
| ALFA Network 產品總覽（Yupitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網卡是否支援 DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責聲明：本文相容性判定以 Tomato / FreshTomato 官方核心與套件庫為準。極少數進階使用者可能透過自行交叉編譯在特定舊型晶片上實現基本功能，但這不屬於官方支援範圍，也不建議一般使用者嘗試。對於需要在路由器上使用 USB WiFi 的場景，OpenWrt 是唯一實際可行的第三方韌體選擇。
