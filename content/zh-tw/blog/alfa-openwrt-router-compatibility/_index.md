---
title: "ALFA 無線網卡是否支援 OpenWrt"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "路由器韌體"
description: "OpenWrt 是三大第三方路由器韌體（DD-WRT / OpenWrt / Tomato）中對 ALFA USB WiFi 網卡支援最好的平台。MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）透過官方 kmod-mt76 系列套件可直接支援；Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）需使用社群..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網卡能否在 OpenWrt 路由器上使用？」

簡短結論：OpenWrt 是三大第三方路由器韌體（DD-WRT / OpenWrt / Tomato）中對 ALFA USB WiFi 網卡支援最好的平台。MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）透過官方 kmod-mt76 系列套件可直接支援；Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）需使用社群維護的 out-of-tree 驅動套件，可用性因 OpenWrt 版本而異。首選 AWUS036ACM（MT7612U），驅動成熟、穩定、支援監聽與注入。

判定母體：ALFA 現役 9 款 USB 網卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目標軟體規格與需求

### 2.1 OpenWrt 是什麼

OpenWrt 是一款高度模組化的開源路由器韌體，採用 Linux kernel 與 opkg 套件管理系統。與 DD-WRT / Tomato 不同，OpenWrt 的驅動程式以可單獨安裝的 kernel module（kmod）套件形式提供，使用者可依需求安裝 USB WiFi 驅動，不需重新編譯整個韌體。

### 2.2 OpenWrt 的 USB WiFi 驅動框架

OpenWrt 官方套件庫包含以下 USB WiFi 驅動：

| 驅動套件 | 來源 | 涵蓋晶片 / 機型 | 維護狀態 |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | 官方 in-kernel | MediaTek MT7612U（AWUS036ACM） | 活躍，穩定 |
| kmod-mt76-usb + kmod-mt76x0u | 官方 in-kernel | MediaTek MT7610U（AWUS036ACHM） | 活躍 |
| kmod-mt7921u | 官方 in-kernel | MediaTek MT7921AUN（AWUS036AXML / AXM） | 23.05+ 版本可用 |
| kmod-rtl8812au-ct | 社群 out-of-tree | Realtek RTL8812AU / RTL8811AU（AWUS036ACH / ACS） | 社群維護，24.10 有 kernel crash 回報 |
| kmod-rtl8821cu | 社群 out-of-tree | Realtek RTL8811CU（AWUS036EACS） | 社群維護 |
| kmod-rtw89 / kmod-rtl8852bu | 開發中 | Realtek RTL8832BU（AWUS036AX / AXER） | rtw89 USB 支援逐步合入，需較新 kernel |

### 2.3 先決條件：USB 核心支援

在安裝 WiFi 驅動前，必須先確保 OpenWrt 已啟用 USB 核心支援：

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

多數現代 OpenWrt 版本已預設包含 kmod-usb-core，但 usbutils（提供 lsusb 指令）需手動安裝。

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網卡產品線如下（判定母體：9 款）：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | OpenWrt 驅動套件 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u（23.05+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u（23.05+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89（開發中）/ 自編 rtl8852bu |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct（社群） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u（官方） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u（官方）⭐ 首選 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct（涵蓋） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu（社群） |

## 4. 適用機型與晶片組

### 4.1 推薦等級分類

| 推薦等級 | 機型（晶片組） | 說明 |
|---|---|---|
| ⭐ 強烈推薦 | AWUS036ACM（MT7612U） | 官方驅動成熟穩定，支援 AP / STA / Monitor / Injection，OpenWrt 上的最佳選擇 |
| ✅ 推薦 | AWUS036ACHM（MT7610U） | 官方驅動，雙頻但僅 433Mbps，適合低功耗場景 |
| ✅ 推薦（新版本） | AWUS036AXML / AXM（MT7921AUN） | Wi-Fi 6E，官方驅動，需 OpenWrt 23.05+ 且 kernel 5.15+ |
| ⚠️ 可用但需注意 | AWUS036ACH（RTL8812AU） | 社群驅動，24.10 版本有 kernel crash 回報，建議用 23.05 |
| ⚠️ 可用但需注意 | AWUS036ACS（RTL8811AU） | 同上，由 8812au 驅動涵蓋 |
| ⚠️ 可用但需注意 | AWUS036EACS（RTL8811CU） | 社群驅動，穩定性中等 |
| ❌ 不建議 | AWUS036AX / AXER（RTL8832BU） | Wi-Fi 6，rtw89 USB 支援尚在開發，多數 OpenWrt 版本無法直接使用 |

### 4.2 路由器硬體需求

| 項目 | 最低需求 | 建議需求 |
|---|---|---|
| USB 埠 | USB 2.0（AWUS036ACHM / ACS / EACS） | USB 3.0（AWUS036ACH / ACM / AX 系列） |
| Flash | 16MB（安裝驅動 + 依賴套件） | 32MB+ |
| RAM | 128MB | 256MB+（AP 模式 + 多使用者） |
| OpenWrt 版本 | 21.02+ | 23.05.x（穩定版） |

## 5. 環境需求

### 5.1 軟體環境

- OpenWrt 穩定版本：23.05.x（kernel 5.15）或 24.10.x（kernel 6.6）
- 套件來源：官方 opkg 套件庫（https://downloads.openwrt.org/releases/{version}/packages/{arch}/）
- 網路連線：安裝驅動期間路由器需可聯網（透過 WAN 埠）

### 5.2 硬體環境

- 具備 USB 2.0 / 3.0 埠的 OpenWrt 相容路由器
- 高功率機型（AWUS036ACH）建議使用有電源的 USB 3.0 Hub，避免路由器 USB 埠供電不足
- AWUS036AXML 為 USB-C 介面，需確保路由器有 USB-C 埠或使用 USB-C to USB-A 轉接

## 6. 相容性判定

### ALFA 現役機型 × OpenWrt 相容性矩陣

| 機型 | 晶片組 | 驅動方式 | USB 偵測 | STA 上網 | AP 模式 | Monitor | 最低版本 | 綜合評價 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ 最佳 |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ 有限 | 21.02+ | ✅ 良好 |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 有限 | 23.05+ | ✅ 良好 |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 有限 | 23.05+ | ✅ 良好 |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ 有限 | 22.03+（24.10 有 crash） | ⚠️ 可用 |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ 可用 |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ 可用 |
| AWUS036AX | RTL8832BU | rtw89（開發中） | ⚠️ | ❌ | ❌ | ❌ | 需自訂編譯 | ❌ 不建議 |
| AWUS036AXER | RTL8832BU | rtw89（開發中） | ⚠️ | ❌ | ❌ | ❌ | 需自訂編譯 | ❌ 不建議 |

判定依據：OpenWrt 官方套件庫（23.05 / 24.10）的 kmod 套件可用性 + OpenWrt 論壇使用者回報。Realtek 晶片的驅動為社群維護，穩定性與功能完整性不及 MediaTek mt76 系列。

## 7. 超詳細 Step by Step 設定步驟

### 7.1 前置作業：啟用 USB 核心支援

**步驟 1：SSH 登入 OpenWrt 路由器**

```bash
ssh root@192.168.1.1
```

**步驟 2：更新套件庫並安裝 USB 核心支援**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**步驟 3：插入 ALFA 網卡，確認 USB 偵測**

```bash
lsusb
# 預期輸出範例（AWUS036ACM / MT7612U）：
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 路徑 A：MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）

以 AWUS036ACM（MT7612U）為例：

**步驟 1：安裝驅動套件**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — 改用
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — 改用（需 23.05+）
# opkg install kmod-mt7921u
```

**步驟 2：安裝無線管理工具**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**步驟 3：確認網路介面已建立**

```bash
iw dev
# 預期出現 wlan0 或 wlan1 介面
```

**步驟 4：掃描附近 WiFi（驗證功能）**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**步驟 5：設定為 STA 用戶端模式（連線到既有 AP）**

編輯 /etc/config/wireless：

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid '你的WiFi名稱'
       option encryption 'psk2'
       option key '你的WiFi密碼'
```

**步驟 6：重啟無線服務**

```bash
/etc/init.d/network restart
```

**步驟 7：設定為 AP 熱點模式（分享網路）**

編輯 /etc/config/wireless，將 mode 改為 ap：

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key '你的熱點密碼'
```

**步驟 8：啟用監聽模式（滲透測試用）**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# 驗證
iw dev wlan0 info
# type 應顯示 monitor
```

### 7.3 路徑 B：Realtek 晶片機型（AWUS036ACH / ACS / EACS）

以 AWUS036ACH（RTL8812AU）為例：

**步驟 1：安裝社群驅動**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — 改用
# opkg install kmod-rtl8821cu
```

**步驟 2：安裝無線管理工具**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**步驟 3：確認介面**

```bash
iw dev
# 注意：rtl8812au-ct 驅動的介面名可能是 wlan0 或 wlan1
```

設定方式同 7.2 步驟 5-7（STA / AP 模式設定）。

**步驟 4：監聽模式**

```bash
# rtl8812au-ct 驅動支援監聽模式
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# 封包注入功能有限，建議用 mt76 晶片做滲透測試
```

**步驟 5：若遇到 kernel crash（24.10 版本已知問題）**

```bash
# 降回 23.05 穩定版，或使用自訂編譯的驅動
# 檢查 crash 日誌
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 路徑 C：Wi-Fi 6 機型（AWUS036AX / AXER，RTL8832BU）

⚠️ 此路徑需自訂編譯 OpenWrt，不適合一般使用者。

**步驟 1：確認 OpenWrt 版本是否已包含 rtw89 USB 支援**

```bash
opkg list | grep rtw89
# 若無結果，代表該版本未包含
```

**步驟 2：若需使用，需自行編譯 OpenWrt 映像檔**

加入 kmod-rtw89 與對應 firmware。

**替代建議**：在 OpenWrt 路由器上使用 Wi-Fi 6 USB 網卡的需求，目前以 AWUS036AXML（MT7921AUN）替代為佳。

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 網卡 | USB 核心未安裝 / 供電不足 | 確認已安裝 kmod-usb-core kmod-usb2 kmod-usb3；使用有電源 USB Hub |
| lsusb 看得到但 iw dev 無介面 | 驅動未安裝 / 驅動不相容 | 安裝對應 kmod 套件；檢查 dmesg 是否有 firmware 缺失錯誤 |
| opkg install kmod-mt76x2u 報「kernel version mismatch」 | OpenWrt 版本與套件庫版本不一致 | 執行 opkg update 後重試；確認韌體版本與套件庫架構匹配 |
| AP 模式啟動失敗（hostapd 錯誤） | 驅動不支援 AP / 通道設定錯誤 | 確認晶片支援 AP 模式；嘗試固定通道（如 6 或 149）；檢查 Regulatory Domain |
| 監聽模式無法注入封包 | 驅動不支援注入 / 通道衝突 | MediaTek mt76 系列支援最佳；Realtek 8812au-ct 注入功能有限；確認 airmon-ng check kill |
| AWUS036ACH 高功率時斷線 | USB 供電不足 | 使用有電源 USB 3.0 Hub；在 /etc/config/wireless 中設定 option txpower '20' 降低功率 |
| 24.10 上安裝 rtl8812au-ct 後 kernel panic | 已知驅動相容性問題 | 降回 23.05.x 穩定版；或追蹤 GitHub issue 等待修復 |
| MT7921（AXML/AXM）無法使用 6GHz | Regulatory Domain 限制 / kernel 版本 | 需 kernel 5.19+ 且正確設定 Wi-Fi 6E 法規區域；OpenWrt 23.05 的 6GHz 支援仍在測試 |

## 9. 已知限制

- Realtek 晶片驅動為社群維護：kmod-rtl8812au-ct、kmod-rtl8821cu 非 OpenWrt 官方維護，穩定性與更新時程無法保證
- 24.10 版本的 rtl8812au-ct 有 kernel crash 回報：建議 Realtek 晶片使用者維持在 23.05.x
- Wi-Fi 6（RTL8832BU）支援不足：rtw89 USB 驅動尚在開發，多數 OpenWrt 版本無法直接使用 AWUS036AX / AXER
- AP 模式效能受限：USB WiFi 做 AP 時，吞吐量低於路由器內建 WiFi（USB 匯流排頻寬 + 驅動 overhead）
- 監聽 / 注入功能差異：MediaTek mt76 系列支援最完整；Realtek 晶片的注入功能有限，不適合專業滲透測試
- 路由器硬體資源：低階路由器（16MB Flash / 128MB RAM）安裝驅動後可能空間不足，影響其他功能
- USB 3.0 干擾：USB 3.0 設備會對 2.4GHz WiFi 產生干擾，建議使用 USB 2.0 埠或隔離良好的 USB Hub
- 多網卡同時使用：同時使用路由器內建 WiFi + USB WiFi 時，可能出現通道衝突或資源競爭
- ⚠️ **RTL8832BU（AWUS036AX/AXER）驅動維護者已公開建議避免使用**：本文第 4.1 節標為「❌ 不建議」，原因不只是 rtw89 USB 尚在開發，驅動維護者 morrownr 更公開表示該晶片系列「是很糟糕的驅動，懷疑晶片本身有問題」，建議 Linux 使用者現階段避開（來源見第 10 節）
- **kernel 版本門檻用詞需澄清**：第 4.1 節「MT7921AUN 需 OpenWrt 23.05+ 且 kernel 5.15+」的寫法容易誤導——mt7921u 驅動本身在桌機 Linux 上實際需要 **kernel 5.19+** 才會存在（見驅動維護者原話），但 OpenWrt 官方套件常透過 backport 機制提前收錄，因此 OpenWrt 23.05（雖標示基礎 kernel 5.15）仍有使用者回報安裝 kmod-mt7921u 成功。**判定請以客戶版本 `opkg list` 實際查詢結果為準，不要用 kernel 版號反推**

反駁條件：若 OpenWrt 後續套件更新修復 24.10 的 rtl8812au-ct kernel crash 問題，第 4.1 節與第 6 節對 AWUS036ACH 的建議可由「維持 23.05」升級；若 rtw89 USB 支援正式進入 OpenWrt 官方套件庫，AWUS036AX / AXER 的「不建議」判定需重審；若官方發布 MT7921 的 6GHz 完整支援聲明，AXML / AXM 的限制說明需更新。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| OpenWrt 官方文檔 | OpenWrt 官方文件入口（無線設定 / 套件管理） | https://openwrt.org/docs/start | ✅ 已查核 | 2026-09-03 |
| OpenWrt 官方論壇 | USB WiFi 驅動討論入口 | https://forum.openwrt.org/ | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動上游 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA Network 產品總覽（Yupitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驅動維護者官方聲明：建議避開 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko 需 kernel 5.19+ 才會出現於核心（驅動維護者原話） | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 已查核 | 2026-09-03 |
| OpenWrt 官方論壇 — Best USB WiFi dongle for Raspberry Pi 4B | 使用者回報 OpenWrt 23.05.0 成功安裝 kmod-mt7921u | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網卡是否支援 DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[ALFA 無線網卡是否支援 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責聲明：本文相容性判定以 OpenWrt 23.05.x / 24.10.x 官方套件庫為準。不同路由器架構（ath79 / ramips / mvebu / x86 等）的套件可用性可能不同。Realtek 晶片驅動為社群維護，實際穩定性可能隨版本變化。建議以 MediaTek 晶片機型（AWUS036ACM 為首選）作為 OpenWrt USB WiFi 的優先選擇。
