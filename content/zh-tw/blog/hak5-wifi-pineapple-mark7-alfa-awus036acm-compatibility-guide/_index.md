---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM：5GHz 完整設定指南（2026）"
description: "HAK5 WiFi Pineapple MK7 搭配 ALFA AWUS036ACM (MT7612U) 完整相容性指南 — 隨插即用 5GHz Monitor Mode、Packet Injection 與 PineAP 擴充。逐步設定教學，附驗證指令。無需編譯驅動程式。"
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz", "滲透測試"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

HAK5 WiFi Pineapple Mark VII 是可攜式無線安全稽核的業界標竿。但開箱即用的它有一個重要限制：內建無線電僅支援 **2.4 GHz**。到了 2026 年，大多數企業與家用網路已遷移至 5 GHz 以獲得更好的效能與更少的干擾——這意味著一台原廠 MK7 會錯過一半的無線頻譜。

此時 **ALFA AWUS036ACM** 登場。它是少數被 Hak5 [官方確認相容](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) 的 802.11ac 網卡之一，且因為 MK7 Firmware 2.x 已預載 `mt76x2u` 核心驅動程式，達到**完全無需編譯驅動**的即插即用體驗。

本指南涵蓋所有內容：硬體規格、驅動相容性分析、經過驗證的 7 步驟設定流程，以及完整的滲透測試拓撲圖，讓你在 10 分鐘內為 Pineapple 加入 5 GHz Monitor Mode 與 Packet Injection 能力。

---

## 1. 為什麼你的 WiFi Pineapple 需要 5 GHz

MK7 內建的 MT7628AN SoC 提供了一個可靠的 2.4 GHz b/g/n 無線電——足以應付基本的 PineAP 操作，例如 Beacon Flood、Deauth 攻擊與 Client Probing。但無線環境已經進化：

| 場景 | 2.4 GHz（內建） | 5 GHz（AWUS036ACM） |
|---|---|---|
| 企業 WPA2-Enterprise 網路 | 偶爾仍有 2.4 GHz | **現代部署的主要頻段** |
| 家用 Mesh 系統（Eero、Google WiFi） | 僅作為舊裝置備援 | **客戶端連線的預設頻段** |
| 802.11ac 客戶端裝置 | 幾乎不使用 2.4 GHz | **永遠優先選擇 5 GHz** |
| 頻道壅塞（公寓／辦公室） | 極度擁擠（頻道 1–11） | 乾淨頻譜（頻道 36–165） |
| WPA3-SAE Handshake 捕獲 | 有限 | 完整 5 GHz 捕獲能力 |

**結論**：如果你正在稽核現代網路，你需要 5 GHz。AWUS036ACM 是為 WiFi Pineapple MK7 加入 5 GHz 最可靠的方式。

---

## 2. 目標平台：HAK5 WiFi Pineapple Mark VII

### 2.1 硬體規格

MK7 採用 MediaTek MT7628AN 系統單晶片，這是一款針對封包級操作優化的單核心 MIPS 24KEc 網路處理器：

| 元件 | 規格 |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **儲存空間** | 2 GB eMMC |
| **供電** | USB-C，5V @ 2A |
| **USB Host** | 1× USB 2.0 Type-A（最高 480 Mbps） |
| **USB 供電能力** | 500 mA @ 5V（總共 2.5W） |

USB 2.0 埠值得特別注意。雖然 AWUS036ACM 是 USB 3.0 裝置，在 5 GHz 下最高可達 867 Mbps，但 MK7 的 USB 2.0 匯流排將吞吐量限制在約 150–250 Mbps。對滲透測試工作負載——Monitor Mode 封包捕獲、Handshake 收集、Beacon 分析——這個頻寬完全足夠。只有在嘗試將 MK7 用作高吞吐量無線橋接器時才會遇到限制，而這並非其設計用途。

### 2.2 軟體環境

MK7 運行由 Hak5 維護的高度客製化 OpenWrt 發行版：

| 層級 | 詳細資訊 |
|---|---|
| **作業系統** | OpenWrt（Hak5 客製版） |
| **核心版本** | 5.4.x（Firmware 2.x 系列） |
| **預載驅動** | `kmod-mt76x2u`（MT7612U）、`kmod-mt7601u`（MT7601U） |
| **套件管理** | `opkg` |
| **無線工具** | `iw`、`iwconfig`、`airmon-ng`、`hostapd`（2.9）、`uci` |
| **管理介面** | PineAP Web UI + SSH（port 22） |

> ✅ **關鍵事實**：`kmod-mt76x2u` 已預載於 MK7 Firmware 2.x。AWUS036ACM 達到**隨插即用**——無需 `opkg install`、無需交叉編譯、無 DKMS 頭痛問題。

---

## 3. ALFA AWUS036ACM — 硬體深入分析

### 3.1 規格

AWUS036ACM 採用 **MediaTek MT7612U** 晶片組，該晶片於 Linux 核心 4.19 版（2018 年 10 月）合併至主線。正是這個上游整合使其在 MK7 上實現無縫相容。

| 規格 | 詳細資訊 |
|---|---|
| **晶片組** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **USB 介面** | USB 3.0 Type-A（向下相容 USB 2.0） |
| **支援頻段** | 2.4 GHz (b/g/n) + 5 GHz (a/n/ac) |
| **最大傳輸速率** | 2.4 GHz：300 Mbps · 5 GHz：867 Mbps |
| **通道寬度** | 20 / 40 / 80 MHz |
| **Monitor Mode** | ✅ 支援 |
| **Packet Injection** | ✅ 支援（透過 mac80211 framework） |
| **AP Mode（Master）** | ✅ 支援 |
| **天線** | 2× 5 dBi 雙頻 RP-SMA（可拆換） |
| **TX 功率** | 2.4G：23 dBm · 5G：20 dBm（±2 dBm） |
| **峰值電流消耗** | ~380 mA @ 5V |
| **安全協定** | WEP / WPA / WPA2 / WPA3 / 802.1X |

RP-SMA 天線接頭是一大優勢：你可以根據測試環境，將原廠 5 dBi 全向天線更換為高增益定向天線、平板天線或戶外等級天線。

### 3.2 Hak5 官方確認相容

Hak5 維護一份官方的[相容 802.11ac 網卡清單](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)。AWUS036ACM (MT7612U) 被明確列為相容——與 Hak5 自家的 MK7AC Adapter 使用**相同 MT7612U 晶片組**。

| 網卡 | 晶片組 | 狀態 |
|---|---|---|
| Hak5 MK7AC Adapter | MT7612U | ✅ 官方配件 |
| **ALFA AWUS036ACM** | **MT7612U** | ✅ **官方確認** |
| EP-AC1605 V1 | MT7612U | ✅（V2 不相容） |

驅動原始碼位於 GitHub 上的 [OpenWrt mt76 倉庫](https://github.com/openwrt/mt76)，安裝說明由社群維護於 [morrownr/7612u](https://github.com/morrownr/7612u)。

---

## 4. 相容性矩陣

| 評估項目 | 結果 | 備註 |
|---|---|---|
| 晶片組相容性 | ✅ **完全** | MT7612U 是 MK7 確認相容的晶片 |
| 驅動可用性 | ✅ **已預載** | `kmod-mt76x2u` 內建於 Firmware 2.x |
| USB 識別 | ✅ **自動** | VID `0E8D` / PID `7612` 由 `mt76x2u` 自動匹配 |
| Monitor Mode | ✅ **支援** | 可透過 `airmon-ng` 或 `iw` |
| Packet Injection | ✅ **支援** | 透過 mac80211 framework |
| 5 GHz 掃描 | ✅ **支援** | 插入後顯示為 `wlan3` |
| USB 2.0 頻寬 | ⚠️ **受限** | 實際 5 GHz 吞吐量約 150–250 Mbps |
| 供電預算 | ✅ **安全** | 380 mA 峰值 vs. 500 mA USB 限制 |
| LED 行為 | ℹ️ **設計如此** | MT7612U 驅動不點亮 LED——非故障 |

USB 2.0 瓶頸是唯一有意義的限制，且僅影響大量資料傳輸速度。Monitor Mode 捕獲、Handshake 收集與 Injection 測試不受影響。

---

## 5. 逐步設定指南

### 前置條件

- WiFi Pineapple MK7 運行 **Firmware 2.x**（建議 2.1.3 Stable 或更新）
- ALFA AWUS036ACM——驗證正版晶片：`lsusb` 應顯示 PID `7612`
- MK7 上的網際網路連線（供 `opkg update` 使用，若需要）
- SSH 客戶端（macOS/Linux 內建 terminal；Windows 使用 PuTTY 或 MobaXterm）

---

### 步驟 1：連接並確認 USB 偵測

將 AWUS036ACM 插入 MK7 的 USB Type-A 埠。透過 SSH 登入 Pineapple：

```bash
ssh root@172.16.42.1
```

確認 USB 裝置已被識別：

```bash
lsusb
```

**預期輸出**（應包含以下行）：

```
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

> ⚠️ 若 PID 不是 `7612`，你的網卡就不是 AWUS036ACM (MT7612U)。仿冒或標籤錯誤、搭載 RTL8812AU 晶片（PID `8812`）的網卡將**無法**使用預載驅動。

---

### 步驟 2：確認驅動已載入

```bash
lsmod | grep mt76
```

**預期輸出：**

```
mt76x2u
mt76x2_common
mt76x02_usb
mt76_usb
mt76x02_lib
mt76
```

若缺少上述模組（在 Firmware 2.x 上不太可能），手動載入：

```bash
modprobe mt76x2u
```

或透過 `opkg` 安裝：

```bash
opkg update
opkg install kmod-mt76x2u
```

---

### 步驟 3：確認無線介面出現

```bash
iw dev
```

**預期輸出**（尋找 `wlan3` 或類似介面）：

```
phy#3
    Interface wlan3
        ifindex 7
        wdev 0x300000001
        addr aa:bb:cc:dd:ee:ff
        type managed
        channel 6 (2437 MHz), width: 20 MHz
```

介面編號取決於現有無線電。典型對應關係：
- `wlan0` — Management AP（內建 2.4 GHz）
- `wlan1` — PineAP Engine（內建 2.4 GHz）
- `wlan2` — Client Mode（若有設定）
- `wlan3` — **AWUS036ACM**（外接 USB）

---

### 步驟 4：啟用 Monitor Mode

**方法 A — airmon-ng（建議）：**

```bash
airmon-ng check kill
airmon-ng start wlan3
```

介面重新命名為 `wlan3mon`。驗證：

```bash
iwconfig wlan3mon
```

**預期輸出：**

```
wlan3mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz ...
```

**方法 B — iw（輕量化，無需 airmon-ng）：**

```bash
ip link set wlan3 down
iw wlan3 set monitor control
ip link set wlan3 up
```

---

### 步驟 5：鎖定 5 GHz 頻道並掃描

切換至 5 GHz 頻道（範例：Channel 36，5180 MHz）：

```bash
iw wlan3mon set channel 36
```

啟動 airodump-ng 掃描 5 GHz 頻段：

```bash
airodump-ng --band a wlan3mon
```

`--band a` 參數指定目標為 802.11a/n/ac（5 GHz）。你應該會在掃描輸出中看到 5 GHz 基地台。

---

### 步驟 6：測試封包注入（可選）

驗證注入能力：

```bash
aireplay-ng --test wlan3mon
```

**預期輸出（成功）：**

```
09:14:22  Trying injection in the monitor interface... wlan3mon
09:14:22  Injection is working!
```

---

### 步驟 7：開機自動啟用（可選）

若要讓 MK7 每次開機時自動將已插入的 AWUS036ACM 設為 Monitor Mode，將以下內容加入 `/etc/rc.local`：

```bash
cat >> /etc/rc.local << 'EOF'
# Auto-enable AWUS036ACM monitor mode on boot
sleep 5
if iw dev wlan3 info > /dev/null 2>&1; then
    ip link set wlan3 down
    iw wlan3 set monitor control
    ip link set wlan3 up
    logger "AWUS036ACM wlan3 set to monitor mode"
fi
EOF
```

---

## 6. 滲透測試拓撲

下圖說明 AWUS036ACM 整合至 WiFi Pineapple MK7 部署後的完整拓撲。該網卡以 `wlan3` 出現，在 MK7 內建 PineAP Engine（2.4 GHz）之旁提供專屬的 5 GHz 監聽能力。

![HAK5 WiFi Pineapple MK7 + AWUS036ACM 滲透測試拓撲](/images/blog/hak5-pineapple-topology.svg)

| 介面 | 角色 | 頻段 |
|---|---|---|
| `wlan0` | Management AP — 操作員連線管理 MK7 | 2.4 GHz |
| `wlan1` | PineAP Engine — SSID 廣播、Deauth、Probe 捕獲 | 2.4 GHz |
| `wlan2` | Client Mode — 上游 AP 連線供網際網路 | 2.4 / 5 GHz |
| `wlan3` | **AWUS036ACM** — 5 GHz Monitor、Injection、Handshake 捕獲 | **5 GHz** |

> **注意**：Firmware 2.x 的 PineAP Web UI 主要管理內建無線電。AWUS036ACM 的 5 GHz 掃描需透過 CLI（SSH）配置，或使用步驟 7 的啟動腳本自動化。

---

## 7. 驗證結果

所有測試均在 MK7 Firmware 2.1.3 上使用正版 ALFA AWUS036ACM 執行：

| 測試項目 | 指令 | 結果 |
|---|---|---|
| USB 裝置偵測 | `lsusb \| grep 7612` | ✅ PASS |
| 驅動模組載入 | `lsmod \| grep mt76x2u` | ✅ PASS |
| 介面出現（wlan3） | `iw dev` | ✅ PASS |
| Monitor Mode 啟用 | `airmon-ng start wlan3` | ✅ PASS |
| 5 GHz 頻道切換 | `iw wlan3mon set channel 36` | ✅ PASS（頻道 36–165） |
| 5 GHz AP 掃描 | `airodump-ng --band a wlan3mon` | ✅ PASS |
| 封包注入 | `aireplay-ng --test wlan3mon` | ✅ PASS |
| WPA Handshake 捕獲 | `airodump-ng -c 36 wlan3mon` | ✅ PASS（EAPOL 已捕獲） |
| 供電穩定性 | 連續掃描 30 分鐘 | ✅ PASS（無斷線） |
| LED 指示燈 | 視覺檢查 | ℹ️ 預期行為（驅動設計） |

---

## 8. 建議

**ALFA AWUS036ACM 是目前能買到、最適合擴充 WiFi Pineapple Mark VII 至 5 GHz 的網卡。**

它與 Hak5 自家的 MK7AC Adapter 採用完全相同的 MT7612U 晶片組，使用核心內建驅動、無需編譯，電流消耗完全在 MK7 USB 供電預算內，且支援完整的滲透測試工具鏈：Monitor Mode、Packet Injection 與跨所有 5 GHz 頻道的 Handshake 捕獲。

**立即在 Yupitek 購買 AWUS036ACM：**

👉 [ALFA AWUS036ACM 產品頁面](/zh-tw/products/alfa/awus036acm/)

我們是 ALFA Network 授權經銷商，為所有 ALFA × HAK5 整合場景提供完整技術支援。瀏覽我們完整的 [ALFA 網卡產品線](/zh-tw/products/alfa/) 以找到適合你測試需求的工具。

**Yupitek 相關資源：**
- [AWUS036ACH vs AWUS036ACM — Kali Linux 完整比較](/zh-tw/blog/awus036ach-vs-awus036acm/)
- [2026 年 Kali Linux 最佳 WiFi 網卡推薦](/zh-tw/blog/best-wifi-adapter-kali-linux-2026/)
- [Kali Linux 啟用 Monitor Mode 完整指南](/zh-tw/blog/enable-monitor-mode-kali-linux/)

**外部參考資源：**
- [Hak5 官方文件 — 相容 802.11ac 網卡](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
- [OpenWrt mt76 驅動倉庫](https://github.com/openwrt/mt76)
- [morrownr USB-WiFi 相容性清單](https://github.com/morrownr/USB-WiFi)

---

*需要設定協助？聯絡 Yupitek 技術支援團隊：[yupitek.com/support](/zh-tw/support/)*
