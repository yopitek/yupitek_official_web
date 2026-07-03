---
title: "ALFA 無線網卡搭配 Kali NetHunter 完整技術指南 2026"
description: "ALFA USB 無線網卡搭配 Kali NetHunter 行動滲透測試完整技術參考。涵蓋台灣上市手機相容性、MT7610U/MT7612U 免驅動 vs RTL8812AU DKMS 驅動分析、OTG 設定指南及實測驗證結果。"
date: 2026-06-09
draft: false
showBreadcrumbs: true
showTableOfContents: true
featureimage: /images/blog/alfa-nethunter-technical-guide-hero.png
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFA 無線網卡搭配 Kali NetHunter 需要哪些手機條件？"
    answer: "需要支援 OTG 的 Android 手機、已 root 並刷入 Kali NetHunter 核心。已驗證相容的機型包括 Google Pixel 系列、OnePlus 較舊旗艦機型。具體相容性取決於核心版本與網卡晶片驅動位置。"
  - question: "MT7610U/MT7612U 和 RTL8812AU 驅動有什麼差別？"
    answer: "MT7610U/MT7612U 驅動位於核心樹內，插上即用不需編譯；RTL8812AU 需透過 DKMS 外部驅動編譯安裝，核心更新後可能需要重新編譯。對於資安現場使用，核心樹內驅動穩定性更高。"
  - question: "ALFA 網卡在 NetHunter 上支援 Monitor Mode 嗎？"
    answer: "是的，MT7610U/MT7612U 支援 Monitor Mode 與封包注入。RTL8812AU 在核心 < 6.12 時也支援，但核心 6.12 以上 Monitor Mode 受限。建議資安研究優先選用 MT7610U/MT7612U 網卡。"
---

如果你已經完成基本的 OTG 設定，想看快速入門版本，我們的 [OTG 設定指南](/zh-tw/blog/alfa-adapter-nethunter-android-otg/) 涵蓋了所有基本步驟。本文是更深入的完整技術參考，為資安專業人員撰寫——在採購硬體前評估手機與網卡相容性、理解哪種驅動方式能跨核心更新持續運作、以及查看已驗證的測試結果後再決定特定組合。

我們聚焦大多數 NetHunter 指南跳過的核心問題：**哪張網卡真正插上就能用，哪張會在最重要的時刻讓你陷入驅動編譯的泥沼？** 答案取決於 chipset、手機核心版本，以及驅動是位於核心樹內還是外部 DKMS 儲存庫。弄錯了，你的網卡就只能躺在包包裡，你卻在現場盯著 `modprobe` 錯誤訊息。弄對了，插上去就能開始掃描。

{{< tldr >}}
MT7610U/MT7612U 核心原生驅動即插即用，RTL8812AU 需 DKMS 編譯。NetHunter 手機需 root + OTG 支援，優先選 MT7612U 網卡避免驅動問題。
{{< /tldr >}}

> **免責聲明**：本文件僅供合法授權的資安測試與研究使用。未經授權存取網路設備屬違法行為。

---

## 1. 客戶需求定義

### 1.1 使用情境

行動滲透測試人員希望利用 Android 手機搭配 Kali NetHunter，透過 USB OTG 連接 ALFA 外接無線網卡，在不攜帶筆電的情況下執行 Wi-Fi 安全評估工作。核心工作流程——site survey、monitor mode 封包擷取、packet injection、WPA handshake 收集——必須在電池供電下穩定運作。

### 1.2 核心需求

| 需求項目 | 說明 |
|---------|------|
| 平台 | Android 手機 + Kali NetHunter（Full 版，需自訂核心） |
| 連接方式 | USB OTG 線或有獨立供電的 OTG Hub |
| 無線網卡 | ALFA USB 無線網卡，支援 monitor mode 與 packet injection |
| 驅動策略 | **優先選擇免驅動（In-kernel）chipset**，消除編譯依賴 |
| 台灣市場 | 手機為台灣有上市的近期型號（2024–2026） |
| 供電 | 電池供電；強烈建議使用有獨立供電的 OTG Hub 以維持長時間運作 |

---

## 2. 目標硬體與軟體分析

### 2.1 NetHunter 相容手機：台灣可取得型號

NetHunter 支援超過 117 款裝置模組，但多數為舊型號。經過篩選符合以下條件：(a) 台灣有上市、(b) 2024 年後推出、(c) 具有可用的 NetHunter 自訂核心——以下三款手機脫穎而出：

| 型號 | 代號 | CPU | 核心版本數 | 預建映像數 | 台灣狀況 |
|-----|------|-----|:---:|:---:|------|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ 2023 年在台上市，2024 年仍有庫存 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ 台灣正式上市，社群活躍 |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ 台灣有售——**必須是 Snapdragon 版** |

{{< alert "triangle-exclamation" >}}
**Samsung Exynos 警告：** Samsung 在台灣電信商銷售的型號大多使用 Exynos 晶片組。NetHunter 核心僅支援 Snapdragon 版本（代號 `r8q`）。購買 Samsung 裝置用於 NetHunter 前，務必確認 CPU 型號——若商品標示「Exynos」，將無法使用。請購買 Snapdragon 水貨版，或改選 OnePlus 11。
{{< /alert >}}

**NetHunter Rootless** 可在任何 Android 裝置上執行，無需 root，但無法支援外接 USB 無線網卡的 monitor mode。若你需要封包擷取與 packet injection，必須使用完整版 NetHunter 搭配自訂核心。

### 2.2 目標平台技術規格

以 OnePlus 11 5G 為參考平台：

| 參數 | 規格 |
|-----|------|
| CPU 架構 | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| USB 控制器 | USB 3.1 Gen 1，支援 OTG |
| USB 供電能力 | 5V / 900mA（建議使用有獨立供電的 OTG Hub 以維持網卡長時間運作） |

### 2.3 軟體環境需求

| 項目 | 需求 | 建議版本 |
|-----|------|---------|
| 主機 OS | Android + Kali Linux chroot | Android 11+ |
| NetHunter | Full 版（自訂核心） | 2024.4（最新穩定版） |
| Linux Kernel | 裝置專屬自訂核心 | 建議 5.x 以上 |
| 預載驅動 | 見第 4 章矩陣 | — |
| DKMS | 僅 RTL8812AU 網卡需要 | 核心 headers 必須版本匹配 |
| 無線工具 | aircrack-ng、Kismet、MANA Toolkit | NetHunter chroot 內建提供 |
| Root | 完整功能需要 | Magisk 26.0+ |

---

## 3. ALFA 網卡規格與驅動來源

### 3.1 AWUS036ACHM — NetHunter 首選 ⭐

| 參數 | 規格 |
|-----|------|
| Chipset | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| 支援頻段 | 2.4 GHz + 5 GHz（雙頻 AC433） |
| 最大傳輸速率 | 150 Mbps（2.4 GHz）/ 433 Mbps（5 GHz） |
| USB 版本 | USB 2.0 |
| Monitor Mode | ✅ 完整支援 |
| Packet Injection | ✅ 完整支援 |
| 天線 | 1× 可更換高增益天線（RP-SMA） |
| 驅動模式 | **In-kernel（免驅動安裝）** |
| 核心模組名稱 | `mt76x0u` |
| 核心版本需求 | Linux 4.19+ |
| 產品頁面 | [/zh-tw/products/alfa/awus036achm/](/zh-tw/products/alfa/awus036achm/) |

MT7610U chipset 被 Kali 與 NetHunter 社群廣泛推薦，因為其 `mt76x0u` 驅動自 Linux 4.19 起就在主線核心中。插上即用，核心自動識別，直接開工。不需要編譯工具鏈、不需要核心 headers、不需要 DKMS——只要 `lsusb` 確認後，接著 `airmon-ng start` 即可。

**業界評價**：Lab401、morrownr USB-WiFi 資料庫均將 AWUS036ACHM 列為「最佳 Kali Linux 無線網卡」之一，理由是 MT7610U 的 in-kernel 支援確保跨 OS 版本更新的相容性穩定性。

### 3.2 AWUS036ACM — 高性能替代選擇 ⭐

| 參數 | 規格 |
|-----|------|
| Chipset | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| 支援頻段 | 2.4 GHz + 5 GHz（雙頻 AC1200） |
| 最大傳輸速率 | 300 Mbps（2.4 GHz）/ 867 Mbps（5 GHz） |
| USB 版本 | USB 3.0 |
| Monitor Mode | ✅ 完整支援 |
| Packet Injection | ✅ 確認穩定（Kali 2024.3 / 2025.1） |
| 天線 | 2× 雙天線（RP-SMA），MIMO 2T2R |
| 驅動模式 | **In-kernel（免驅動安裝）** |
| 核心模組名稱 | `mt76x2u` |
| 核心版本需求 | Linux 4.19+ |
| 產品頁面 | [/zh-tw/products/alfa/awus036acm/](/zh-tw/products/alfa/awus036acm/) |

ACM 增加了 AC1200 雙頻與 MIMO 2T2R，搭配 USB 3.0 傳輸效能。`mt76x2u` 驅動同樣自核心 4.19 起在主線中。注意：部分較舊的 NetHunter 自訂核心（尤其是 OnePlus 7T 的 4.14 版本）未包含 `mt76x2u` 模組——即使 `lsusb` 能辨識 `0e8d:7612`，仍無法建立網路介面。在核心 4.19 以上這不成問題，但若你使用較舊的核心，請先用 `lsmod | grep mt76x2u` 檢查。

### 3.3 AWUS036ACH — 社群支援最廣泛

| 參數 | 規格 |
|-----|------|
| Chipset | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| 支援頻段 | 2.4 GHz + 5 GHz（雙頻 AC1200） |
| 最大傳輸速率 | 300 Mbps（2.4 GHz）/ 867 Mbps（5 GHz） |
| USB 版本 | USB 3.0 |
| Monitor Mode | ✅ 完整支援 |
| Packet Injection | ✅ 完整支援 |
| 天線 | 2× 5dBi 外接天線（RP-SMA） |
| 驅動模式 | 外部 DKMS（大多數 NetHunter 核心預編譯） |
| 核心模組名稱 | `88XXau` |
| 驅動 Repo | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| 產品頁面 | [/zh-tw/products/alfa/awus036ach/](/zh-tw/products/alfa/awus036ach/) |

ACH 多年來一直是 Kali 與 NetHunter 環境的預設標準。大多數 NetHunter 自訂核心已預編譯 `88XXau` 模組，通常不需要手動從原始碼編譯。但若你的核心版本未包含該模組，則需要完整的編譯環境與匹配的核心 headers——這正是 MT7610U 和 MT7612U 能避免的依賴鏈。雙 5dBi 天線提供此系列中最強的訊號範圍，對長距離擷取場景特別有價值。

### 3.4 AWUS036ACS — 極致便攜

| 參數 | 規格 |
|-----|------|
| Chipset | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| 支援頻段 | 2.4 GHz + 5 GHz（AC433） |
| USB 版本 | USB 2.0 |
| Monitor Mode | ✅ 支援（與 RTL8812AU 相同驅動家族） |
| Packet Injection | ✅ 支援 |
| 天線 | 內建天線，55mm 超薄機身 |
| 功耗 | ~300mW——此系列中最低 |
| 驅動模式 | 外部驅動（與 RTL8812AU 共用 aircrack-ng repo） |
| 產品頁面 | [/zh-tw/products/alfa/awus036acs/](/zh-tw/products/alfa/awus036acs/) |

ACS 是最便攜的選擇。300mW 的功耗對手機電池最友善，超薄機身可輕鬆放入口袋。取捨在於單串流 AC433 效能以及與 RTL8812AU 家族共有的外部 DKMS 驅動依賴。

### 3.5 不建議用於 NetHunter 的型號

| 網卡型號 | Chipset | 原因 |
|---------|---------|------|
| AWUS036AX / AWUS036AXER | RTL8832BU | 需要 kernel 6.14+；Monitor Mode 穩定性在 Android 核心上未經驗證 |
| AWUS036AXML / AWUS036AXM | MT7921AUN | WiFi 6E / 6 GHz 在目前 NetHunter 核心版本上支援不穩定；不適合作為主要滲透測試網卡 |

### 3.6 驅動程式來源

| Chipset | 驅動 | 來源 |
|---------|------|------|
| MT7610U | `mt76x0u`（In-kernel） | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u`（In-kernel） | 同上核心樹 |
| RTL8812AU | `88XXau`（外部） | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau`（外部，共用） | 同上 aircrack-ng 儲存庫 |

---

## 4. 驅動相容性分析

### 4.1 In-Kernel vs 外部 DKMS

選擇 NetHunter 網卡時最關鍵的決策：驅動在核心樹內還是核心樹外。原因如下：

| | In-Kernel（MT7610U、MT7612U） | 外部 DKMS（RTL8812AU、RTL8811AU） |
|---|---|---|
| 隨插即用 | ✅ 是——插入即識別 | ⚠️ 取決於核心是否已預編譯 `88XXau` |
| 核心更新後仍可用 | ✅ 是——驅動是核心建置的一部份 | ❌ 核心更新後可能失效；需重新編譯 |
| 需要 linux-headers | ❌ 不需要 | ✅ 需要（若需手動編譯） |
| 需要 DKMS | ❌ 不需要 | ✅ 需要（若未預編譯於核心中） |
| 社群文件量 | 中等 | 豐富（ACH 擁有最多的教學資源） |
| 現場故障風險 | 低 | 中等（編譯依賴） |

**底線：** 若你希望在現場將驅動問題風險降到最低，選擇 MT7610U 或 MT7612U 網卡。驅動已在核心中——不需編譯、沒有更新時損壞的風險、沒有在客戶現場需要排除的依賴問題。

### 4.2 NetHunter 核心模組支援矩陣

| 裝置 | NetHunter 核心 | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|-----|:|:---:|:---:|:---:|
| OnePlus 11 5G | Android 13 kernel | ✅ 支援 | ✅ 支援 | ✅ 支援 |
| Samsung S20 FE (Snapdragon) | Android 12 kernel (4.19) | ✅ 支援 | ✅ 支援 | ✅ 支援（請確認 XDA 回報） |
| Nothing Phone (1) | Android 12/13 kernel | ✅ 支援 | 需確認核心 config | ✅ 支援 |
| OnePlus 7/7T | 4.14（較舊） | ✅ 支援 | ⚠️ 版本可能缺少此模組 | ✅ 支援 |

來源：NetHunter GitLab、XDA Forums 社群回報（2024–2026）。

### 4.3 已知問題

**問題 1：MT7612U 在舊核心（4.14）上不建立介面**

- 症狀：`lsusb` 能看到 `0e8d:7612`，但 `ip link` 無 `wlan1`
- 根本原因：自訂核心編譯時未包含 `mt76x2u` 模組。這影響部分基於 4.14 的 NetHunter 核心（OnePlus 7T 時期）
- 解決方案：使用包含該模組的核心版本，或改用 AWUS036ACHM（MT7610U）——後者在舊核心上有更廣泛的支援

**問題 2：USB 供電不足導致網卡斷線**

- 症狀：網卡在掃描中途消失，`dmesg` 顯示 USB reset 錯誤
- 根本原因：手機 USB 埠無法維持網卡的電流消耗，尤其是 USB 3.0 網卡（ACH 約 500mW）
- 解決方案：使用有獨立供電的 OTG Hub，從變壓器提供 5V 給網卡，同時將資料傳遞給手機

**問題 3：chroot 啟動前插入網卡**

- 症狀：Android 跳出 USB 權限對話框，但 Kali 工具無法存取網卡
- 根本原因：NetHunter chroot 環境必須先執行，USB 裝置才能被暴露給 chroot
- 解決方案：先啟動 chroot（Kali Services → Start），再連接網卡並授予 USB 權限

---

## 5. 設定步驟

### 5.1 前置需求確認

連接任何硬體前，請先確認：

```bash
# 確認裝置已 root
su -c "id"

# 確認 NetHunter chroot 版本
cat /kali/etc/os-release
# 應顯示 Kali Linux with NetHunter

# 確認 USB OTG 已啟用
# 設定 → 開發人員選項 → OTG（實際位置依 Android 版本而異）
```

### 5.2 硬體連接順序

順序很重要：

1. 啟動 **NetHunter App** → 前往 **Kali Services** → 點擊 **Start** 啟動 chroot 環境
2. 將**有獨立供電的 OTG Hub** 連接到手機 USB 埠
3. 將 **ALFA 網卡** 插入 OTG Hub
4. 當 Android USB 權限對話框出現時，點擊**確定**並勾選「**永遠允許**」

{{< alert "circle-info" >}}
強烈建議使用有獨立供電的 OTG Hub。AWUS036ACH 消耗約 500mW——直接從手機電池供電會顯著加速耗電並可能造成 USB 不穩定。使用能從變壓器取電同時傳遞資料的 Hub 可同時解決這兩個問題。
{{< /alert >}}

### 5.3 驗證網卡識別

```bash
# 列出 USB 裝置——確認網卡出現
lsusb

# 各型號預期輸出：
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

若網卡未出現：更換 OTG 線、確認 OTG 已在開發人員選項中啟用，或在電腦上測試網卡以確認功能正常。

### 5.4 載入驅動

**MT7610U（AWUS036ACHM）——大多數核心會自動載入：**

```bash
# 確認模組自動載入
lsmod | grep mt76

# 若未自動載入（少見情況）
sudo modprobe mt76x0u
```

**MT7612U（AWUS036ACM）——核心 4.19+ 會自動載入：**

```bash
# 確認模組
lsmod | grep mt76

# 若未自動載入
sudo modprobe mt76x2u
```

**RTL8812AU（AWUS036ACH）——大多數 NetHunter 核心已預編譯：**

```bash
# 載入預編譯模組
sudo modprobe 88XXau

# 確認已載入
lsmod | grep 88XX
```

### 5.5 確認網路介面

```bash
# 列出所有無線介面
ip link show | grep wlan

# 或使用 iw 工具
iw dev

# 外接網卡通常顯示為 wlan1
#（wlan0 通常為手機內建 WiFi）
```

### 5.6 啟用 Monitor Mode

```bash
# 終止可能干擾的進程
sudo airmon-ng check kill

# 對網卡啟用 Monitor Mode
sudo airmon-ng start wlan1

# 確認 Monitor Mode 已啟用
iwconfig wlan1mon
# 預期輸出：Mode:Monitor

# 掃描周圍網路（僅限授權測試）
sudo airodump-ng wlan1mon

# 掃描所有頻段（2.4 GHz + 5 GHz）
sudo airodump-ng --band abg wlan1mon
```

### 5.7 恢復 Managed Mode

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. 應用架構圖

<img src="/images/blog/nethunter-topology.png" alt="NetHunter + ALFA Application Topology Diagram" loading="eager" style="max-width:100%;height:auto;display:block">

---

## 7. 驗證結果

### 7.1 測試組合矩陣

以下組合已透過社群測試與廠商文件驗證：

| 手機型號 | ALFA 網卡 | Chipset | Monitor Mode | Packet Injection | 狀態 |
|---------|---------|---------|:---:|:---:|------|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | 已驗證 |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | 已驗證 |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | 已驗證 |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | 社群回報——請確認核心 config |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | 社群回報 |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | 社群回報 |

來源：XDA Forums、Reddit r/NetHunter、Kali NetHunter GitLab Issues（2024–2026）。

### 7.2 `lsusb` 預期輸出

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 Monitor Mode 驗證

```bash
# 成功時的預期 iwconfig 輸出
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. 建議與總結

### 8.1 首選組合：OnePlus 11 5G + AWUS036ACHM

此組合在已測試的所有設定中阻力最低。OnePlus 11 是目前在台灣市場仍可取得、具備官方 NetHunter 核心支援的最新旗艦機。AWUS036ACHM 的 MT7610U chipset 使用 `mt76x0u` 驅動——自核心 4.19 起就在主線中，完全免編譯，國際資安社群（Lab401、morrownr USB-WiFi 資料庫）一致將其列為 Kali 與 NetHunter 最安全的選擇。網卡體積小巧、單天線、USB 2.0——這些在行動場景中都是優點：功耗更低、發熱更少、出錯機會更少。

### 8.2 高性能選擇：OnePlus 11 5G + AWUS036ACM

若你需要雙頻 AC1200 效能與 MIMO 2T2R 以進行長距離 5 GHz 擷取，ACM 讓你在不離開 in-kernel 驅動生態系的前提下獲得這些能力。MT7612U 的 `mt76x2u` 驅動同樣自核心 4.19 起在主線中。取捨：USB 3.0 功耗較高、雙天線機身較大。請確認核心包含 `mt76x2u`——在 OnePlus 11 上已確認具備。

### 8.3 社群最愛：任何 NetHunter 裝置 + AWUS036ACH

ACH 擁有 NetHunter 生態系中最豐富的教學資源、最大的社群故障排除資料庫，以及最完善的第三方文件。雙 5dBi 天線提供 ALFA 系列中最強的訊號範圍。大多數 NetHunter 核心已預編譯 `88XXau` 模組，幾乎不需要手動編譯。若你重視社群支援與長距離擷取勝過隨插即用的簡潔性，這是你的選擇。

### 8.4 情境式選擇

| 情境 | 推薦組合 | 理由 |
|-----|---------|------|
| 首次 NetHunter 設定、最小化風險 | OnePlus 11 + AWUS036ACHM | In-kernel 驅動、免編譯、體積最小 |
| 雙頻長距離擷取 | OnePlus 11 + AWUS036ACM | AC1200 + MIMO，同樣 in-kernel |
| 長距離 survey、最多教學資源 | 任何支援機型 + AWUS036ACH | 最強天線、最廣泛社群支援 |
| 超便攜、最低功耗 | 任何支援機型 + AWUS036ACS | 300mW 功耗、可放入任何口袋 |

### 8.5 後續支援資源

| 資源 | 連結 |
|-----|------|
| Yupitek — ALFA 台灣授權經銷商 | [yupitek.com](https://www.yupitek.com) |
| ALFA Network 官方產品頁面 | [alfa.com.tw](https://www.alfa.com.tw) |
| MT7610U 驅動（核心樹） | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| RTL8812AU 驅動（aircrack-ng） | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| NetHunter 支援裝置清單 | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| NetHunter 官方文件 | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| XDA NetHunter 論壇 | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Yupitek ALFA 產品型錄 | [/zh-tw/products/alfa/](/zh-tw/products/alfa/) |

---

## 附錄：快速故障排除

**網卡未出現在 `lsusb`：**
1. 確認 OTG 已在開發人員選項中啟用
2. 更換 OTG 線——線材品質是最常見的故障點
3. 使用有獨立供電的 OTG Hub
4. 確認 NetHunter chroot 已啟動

**`lsusb` 看得到但無 `wlan1` 介面：**

```bash
# 查看核心訊息中的驅動錯誤
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# 確認核心模組是否存在
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# 嘗試手動載入
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**Monitor Mode 已啟動但掃描不到任何網路：**

```bash
# 先終止干擾進程
sudo airmon-ng check kill

# 重新掃描所有頻段
sudo airodump-ng --band abg wlan1mon

# 確認頻道設定
sudo iw dev wlan1mon info
```

**網卡使用中斷線（USB reset）：**

```bash
# 降低發射功率（臨時解法）
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# 根本解法：使用有獨立供電的 OTG Hub
```

---

{{< faq >}}

---

## 相關指南

- [ALFA 網卡搭配 NetHunter 基本 OTG 設定](/zh-tw/blog/alfa-adapter-nethunter-android-otg/)
- [ALFA WiFi 網卡選購指南 2026](/zh-tw/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [在 Kali Linux 與 Ubuntu 上安裝 ALFA 驅動](/zh-tw/blog/install-alfa-driver-kali-ubuntu/)
- [ALFA 網卡搭配 Raspberry Pi 與 Kali 使用](/zh-tw/blog/alfa-adapter-raspberry-pi-kali/)

---

## 參考來源

1. [Kali NetHunter 官方文件](https://www.kali.org/docs/nethunter/) — NetHunter 安裝與核心刷入指南
2. [Linux Kernel mt76 驅動原始碼](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt76) — MT7610U/MT7612U 主線驅動
3. [aircrack-ng RTL8812AU 驅動](https://github.com/aircrack-ng/rtl8812au) — DKMS 外部驅動儲存庫
4. [ALFA Network 官方網站](https://alfa.com.tw/) — 產品規格與驅動下載
5. [Android USB OTG 官方文件](https://developer.android.com/guide/topics/connectivity/usb) — OTG API 與硬體需求
