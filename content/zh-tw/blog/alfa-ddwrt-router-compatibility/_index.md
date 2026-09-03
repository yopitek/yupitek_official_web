---
title: "ALFA 無線網卡是否支援 DD-WRT"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "路由器韌體"
description: "目前 ALFA 全系列現役機型（AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM，共 9 款）在 DD-WRT 上均無官方驅動支援，不建議使用。（判定母體：ALFA 現役 9 款 USB 網卡）DD-WRT 的 USB WiFi 支援僅限極少數舊型 Atheros / Ralink 晶片，且需特定編譯版本。若需要在路由..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網卡能否在刷了 DD-WRT 韌體的路由器上使用？」

簡短結論：目前 ALFA 全系列現役機型（AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM，共 9 款）在 DD-WRT 上均無官方驅動支援，不建議使用。（判定母體：ALFA 現役 9 款 USB 網卡）DD-WRT 的 USB WiFi 支援僅限極少數舊型 Atheros / Ralink 晶片，且需特定編譯版本。若需要在路由器上使用 USB WiFi 網卡，建議改用 OpenWrt（見 [ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)）。

## 2. 分析目標軟體規格與需求

### 2.1 DD-WRT 是什麼

DD-WRT 是一款開源路由器第三方韌體，主要針對內建 WiFi 晶片的路由器（Broadcom / Atheros / Ralink SoC）設計。其核心架構為 Linux kernel，但驅動程式預設僅編入目標路由器 SoC 對應的無線驅動。

### 2.2 DD-WRT 的 USB WiFi 支援框架

DD-WRT 透過 ipkg 套件管理系統安裝額外驅動，但官方套件庫中 USB WiFi 驅動極少：

| 驅動 | DD-WRT 狀態 | 對應晶片（ALFA 機型） |
|---|---|---|
| ath9k_htc | 部分版本內建 | Atheros AR9271（如 TP-Link TL-WN722N v1） |
| rt2800usb | 部分版本內建 | Ralink RT3070 / RT3370 / RT5370（舊型 ALFA AWUS036NH 等） |
| rtl8812au | 無官方套件 | Realtek RTL8812AU（AWUS036ACH） |
| mt76 / mt76x2u | 無官方套件 | MediaTek MT7612U / MT7610U（AWUS036ACM / ACHM） |
| mt7921u | 無官方套件 | MediaTek MT7921AUN（AWUS036AXML / AXM） |
| rtl8852bu / rtw89 | 無官方套件 | Realtek RTL8832BU（AWUS036AX / AXER） |

### 2.3 關鍵限制

- DD-WRT 的核心優先支援路由器內建 WiFi，USB WiFi 屬於次要功能
- 不同路由器型號的 DD-WRT 編譯版本不同，驅動可用性差異極大
- 即使社群自行編譯加入驅動，也常因 Flash / RAM 不足而無法安裝
- DD-WRT 對 USB WiFi 的監聽模式（Monitor Mode）與封包注入（Packet Injection）幾乎不支援

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網卡產品線如下：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | Linux 驅動狀態 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel（mt7921u，需 kernel 5.12+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel（mt7921u，需 kernel 5.12+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree（rtl8852bu / rtw89） |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree（rtl8852bu / rtw89） |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree（8812au，morrownr 維護） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | Linux in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel（mt76x2u） |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | Out-of-tree（8812au 涵蓋） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | Out-of-tree（8821cu，morrownr 維護） |

## 4. 適用機型與晶片組

### 4.1 在 DD-WRT 上可能可用的 ALFA 機型（已停產 / 舊款）

| 機型 | 晶片組 | 驅動 | DD-WRT 狀態 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 部分 DD-WRT 版本內建，僅 2.4GHz / 150Mbps |
| AWUS036H | Realtek RTL8187L | rtl8187 | 極舊型，部分版本支援，僅 2.4GHz / 54Mbps |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | 極舊型，雙頻，但已停產多年 |

### 4.2 在 DD-WRT 上不可用的現役機型

所有現役 ALFA 機型（見第 3 節表格）均不被 DD-WRT 官方支援，原因：

- Realtek 晶片（RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU）：DD-WRT 無對應 out-of-tree 驅動套件
- MediaTek 晶片（MT7612U / MT7610U / MT7921AUN）：DD-WRT 未編入 mt76 / mt7921 驅動
- 即使路由器有 USB 埠，硬體層面可以辨識裝置（lsusb 可看到 VID/PID），但無驅動無法建立網路介面

## 5. 環境需求

若客戶仍想嘗試在 DD-WRT 上使用 ALFA 網卡，需滿足以下條件：

| 項目 | 需求 |
|---|---|
| 路由器硬體 | 必須有 USB 2.0 / 3.0 埠，且 DD-WRT 已啟用 USB 核心支援（Services > USB） |
| DD-WRT 版本 | 需為支援該路由器的最新 BrainSlayer / Kong 版本，舊版驅動更少 |
| Flash 空間 | 至少 16MB Flash（多數入門路由器僅 4-8MB，無法安裝額外驅動） |
| RAM | 至少 128MB RAM（USB WiFi 驅動 + hostapd 會佔用記憶體） |
| 供電 | USB 埠需提供足夠電流（AWUS036ACH 高功率輸出時可達 800mA+，建議使用有電源 USB Hub） |

## 6. 相容性判定

### ALFA 現役機型 × DD-WRT 相容性矩陣

| 機型 | 晶片組 | USB 匯流排偵測 | 驅動載入 | STA 上網 | AP 模式 | Monitor | 綜合判定 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅（lsusb） | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |
| AWUS036EACS | RTL8811CU | ✅ | ❌ | ❌ | ❌ | ❌ | 不支援 |

判定依據：DD-WRT 官方套件庫與核心預設編譯均未包含上述晶片的 USB WiFi 驅動。lsusb 能看到裝置僅代表 USB 匯流排層級的辨識，不代表網路功能可用。

## 7. 超詳細 Step by Step 設定步驟

由於現役 ALFA 機型在 DD-WRT 上不可用，本節提供兩種替代路徑：

### 路徑 A：確認你的 DD-WRT 路由器是否真的不支援（除錯步驟）

**步驟 1：登入 DD-WRT 管理介面**

瀏覽器輸入 `192.168.1.1`（或你的路由器 IP）。

**步驟 2：啟用 USB 支援**

- 進入 Services > USB
- 勾選 Core USB Support、USB 2.0 Support、USB 3.0 Support（若有）
- 勾選 USB Wireless Device Support（若有此選項）
- 點擊 Save > Apply Settings

**步驟 3：插入 ALFA 網卡到路由器 USB 埠**

**步驟 4：透過 SSH 登入路由器檢查**

```bash
# 檢查 USB 裝置是否被偵測
lsusb
# 預期輸出應包含 ALFA 網卡的 VID/PID，例如：
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# 檢查網路介面是否被建立
ip link show
# 若沒有 wlan0 / wlan1 等新介面，代表驅動未載入

# 檢查核心日誌
dmesg | tail -30
# 若出現 "no driver" 或僅有 USB 列舉訊息，確認驅動缺失
```

**步驟 5：檢查可用的 WiFi 驅動模組**

```bash
# 列出已載入的無線驅動
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# 若僅有路由器內建 WiFi 的驅動（如 wl / b43 / ath9k），代表無 USB WiFi 驅動
```

**步驟 6：嘗試安裝社群驅動（若有）**

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 若搜尋結果為空，確認該 DD-WRT 版本無可用驅動
```

### 路徑 B：建議替代方案 — 改用 OpenWrt

若客戶需要在路由器上使用 ALFA USB WiFi 網卡，強烈建議將路由器韌體從 DD-WRT 改刷為 OpenWrt。OpenWrt 有活躍的 USB WiFi 驅動套件庫，支援 MT7612U / MT7610U / RTL8812AU 等晶片。詳細步驟請參考 [ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)。

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 網卡 | USB 供電不足 / 接觸不良 / DD-WRT 未啟用 USB 核心 | 檢查 Services > USB 是否已啟用；更換 USB 埠或使用有電源 USB Hub |
| lsusb 看得到但 ip link 無 wlan 介面 | 缺少對應晶片驅動 | 確認 DD-WRT 版本是否有該驅動；多數情況下無解，建議改用 OpenWrt |
| 有 wlan 介面但無法掃描 AP | 驅動不完全支援 / 監聽模式衝突 | 檢查 dmesg 是否有 firmware 載入錯誤；確認 Regulatory Domain 設定 |
| 路由器重啟後設定遺失 | DD-WRT NVRAM 空間不足 | 避免在低階路由器上安裝額外驅動；考慮升級硬體或改用 OpenWrt |
| AWUS036ACH 高功率輸出時斷線 | USB 埠供電不足 | 使用有電源的 USB 3.0 Hub；降低 TX Power 設定 |

## 9. 已知限制

- 驅動缺失：DD-WRT 官方不提供 ALFA 現役機型的 USB WiFi 驅動，這是最根本的限制
- 硬體資源：多數可刷 DD-WRT 的路由器 Flash（4-16MB）和 RAM（32-128MB）有限，即使有驅動也可能無法安裝
- 監聽 / 注入不支援：DD-WRT 的 USB WiFi 架構不支援滲透測試所需的 Monitor Mode 與 Packet Injection
- AP 模式不穩定：即使舊型 Ralink 晶片可運作，USB WiFi 的 AP 模式在 DD-WRT 上常見斷線與效能問題
- 版本碎片化：不同路由器型號的 DD-WRT 編譯版本差異大，無法保證某個版本的驅動在另一個版本也可用
- 不再活躍維護：DD-WRT 開發節奏放緩，新增 USB WiFi 驅動的可能性低
- 補充：即使拋開 DD-WRT 本身的限制，AWUS036AX / AXER（RTL8832BU）這兩款機型的驅動維護者 morrownr 本身也公開建議 Linux 使用者避開此晶片系列（詳見 [ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) 第 9 節），並非僅是 DD-WRT 平台的問題

反駁條件：若客戶使用的是 BrainSlayer / Kong 等含額外驅動的社群編譯版本，實際支援狀況可能不同；本判定以官方發布版本為準。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| DD-WRT 官方 Wiki | 安裝 / 支援 / FAQ 總入口 | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ 已查核 | 2026-09-03 |
| DD-WRT 官方 Wiki — Installation | 安裝說明（含 USB 支援） | https://wiki.dd-wrt.com/wiki/Installation | ✅ 經主頁連結確認存在 | 2026-09-03 |
| OpenWrt 官方文件 | USB WiFi 對比參考 | https://openwrt.org/docs/start | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動（DD-WRT 未整合） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA Network 產品總覽（Yupitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 無線網卡是否支援 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)

免責聲明：本文相容性判定以晶片組驅動狀態與 DD-WRT 官方套件庫為準。DD-WRT 社群存在大量自訂編譯版本，若客戶使用非官方版本，實際結果可能不同。建議客戶以 OpenWrt 作為路由器 USB WiFi 的優先選擇。
