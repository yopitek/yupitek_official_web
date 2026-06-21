---
title: "ALFA 無線網卡於 Apple Mac 的完整相容性報告（2026）：M1/M2/M3/M4 與 Intel 處理器全面解析"
description: "ALFA Network USB 無線網卡於 Apple Mac（MacBook、MacBook Pro、MacBook Air、Mac Mini、Mac Studio）的完整相容性指南，涵蓋 Intel 與 Apple Silicon M1/M2/M3/M4 處理器。了解哪些 ALFA 網卡可用、為何 Apple Silicon 完全無法原生支援，以及如何透過 Linux 虛擬機器啟用監控模式。"
keywords: "ALFA 無線網卡 Mac, ALFA macOS 相容性, ALFA 網卡 Apple Silicon, USB WiFi 網卡 M1 M2 M3 M4, ALFA Network MacBook, 監控模式 Mac, AWUS036ACH Mac, AWUS036ACM Mac, ALFA Network Mac Mini, 滲透測試 Apple Silicon"
author: "Yupitek 技術支援團隊"
date: "2026-06-20"
category: "技術指南"
tags: ["Wireless Security", "ALFA Network", "Apple Mac", "Penetration Testing", "macOS Compatibility"]
---
如果你正在使用 Apple Mac（無論搭載 M3 Max 的 MacBook Pro、搭載 M2 Ultra 的 Mac Studio，或是基於 Intel 的 Mac Mini），並且想要使用 ALFA Network 無線網卡進行 Wi-Fi 稽核、監控模式或封包注入，你需要一個明確的答案：**哪張 ALFA 網卡能在哪台 Mac 上運作？**

以下是簡短的答案：

> **Apple Silicon Mac（M1/M2/M3/M4）：沒有任何 ALFA 無線網卡能在 macOS 上原生運作。** 這是架構上的限制。Realtek 的 macOS 核心擴充功能僅為 x86_64 二進位檔，無法在 ARM64 核心上載入。沒有修復方案，也沒有任何廠商計畫變更此狀況。
>
> **Intel Mac：有限支援，僅限客戶端連線。** macOS 10.11–10.15 有部分官方驅動程式，但 **macOS 不支援監控模式與封包注入**，驅動程式根本沒有實作這些功能。
>
> **可行的解決方案：** 在 Apple Silicon Mac 上以 USB 直通方式執行 Kali Linux ARM 虛擬機器。監控模式與封包注入在 Linux 虛擬機器中運作完美。

本指南提供完整的相容性矩陣，說明 Apple Silicon 無法原生支援 ALFA 網卡的六項技術原因，並帶你完成實際可行的虛擬機器設定。

---

## 1. 相容性矩陣：哪張 ALFA 網卡能在哪台 Mac 上運作？

下表是完整的參考資料。它評估了 [Yupitek 的 ALFA 產品線](https://yupitek.com/en/products/alfa/)中目前 9 款（非停產）ALFA 無線網卡，針對四種部署情境進行檢驗。

### 1.1 完整相容性矩陣

| ALFA 型號 | 晶片組 | Apple Silicon（macOS 原生） | Intel Mac（macOS 原生）| 虛擬機器 + USB 直通（Kali ARM）| Raspberry Pi + Kali |
|:---|:---|:---:|:---:|:---:|:---:|
| **AWUS036ACH** | Realtek RTL8812AU |❌ |⚠️ 僅客戶端（≤10.15）|✅ 最佳監控/注入|✅ |
| **AWUS036ACM** | MediaTek MT7612U |❌ |⚠️ 僅客戶端（≤10.12）|✅ 即插即用|✅ 即插即用|
| **AWUS036AXML** | MediaTek MT7921AUN |❌ |❌ |✅ Wi-Fi 6E|✅ |
| **AWUS036AXM** | MediaTek MT7921AUN |❌ |❌ |✅ |✅ |
| **AWUS036ACHM** | MediaTek MT7610U |❌ |❌ |✅ |✅ |
| **AWUS036ACS** | Realtek RTL8811AU |❌ |⚠️ 僅客戶端（≤10.14）|✅ |✅ |
| **AWUS036AX** | Realtek RTL8832BU |❌ |❌ |⚠️ 有限支援|⚠️ 有限支援|
| **AWUS036AXER** | Realtek RTL8832BU |❌ |❌ |⚠️ 有限支援|⚠️ 有限支援|
| **AWUS036EACS** | Realtek RTL8821CU |❌ |⚠️ 僅客戶端|❌ 無監控模式|⚠️ 不建議|

**圖例：**✅ = 已驗證可用 |⚠️ = 有限制 / 需符合條件 |❌ = 不支援

### 1.2 依 Mac 處理器快速結論

| Mac 處理器 | 能在 macOS 上使用 ALFA 網卡嗎？| 能執行監控模式嗎？| 建議方案 |
|:---|:---|:---|:---|
| **Apple Silicon M1/M2/M3/M4** |❌ 否，架構限制|❌ 無法在 macOS 上執行|✅ 以 USB 直通執行 Linux 虛擬機器|
| **Intel（macOS 10.11–10.15）** |⚠️ 有限，僅客戶端，無監控模式|❌ 不支援|✅ 以 USB 直通執行 Linux 虛擬機器|
| **Intel（macOS 11+）** |⚠️ 僅第三方 kext（chris1111）|❌ 不支援|✅ 以 USB 直通執行 Linux 虛擬機器|

> [!IMPORTANT]
> **結論：** 無論你擁有哪款 Mac，**監控模式與封包注入都需要 Linux。** 虛擬機器 + USB 直通是通用方案，適用於從 2012 年 Intel MacBook Pro 到 2025 年 M4 Mac Studio 的所有 Mac。

---

## 2. 為何 Apple Silicon 失敗：六層架構牆

如果你想知道未來的 macOS 更新是否可能解決這個問題，答案是不會。這個不相容性不是等待修復的 bug，而是**六項 Apple 刻意設計決策**的累積結果，這些決策共同使得第三方 USB Wi-Fi 網卡在 Apple Silicon 上成為架構上的不可能。

### 第一層：IO80211Controller 是私有 API

Apple 從未公開原生 Wi-Fi 驅動程式的核心程式介面（KPI）。類別階層如下：

```
IOService
  └─ IONetworkController
       └─ IOEthernetController        公開 KPI
            └─ IO80211Controller      私有（僅 Apple 內部使用）
```

第三方廠商過去直接繼承 `IOEthernetController`，這就是為什麼 macOS 上的 USB Wi-Fi 網卡會顯示為「乙太網路」介面，而非整合到選單列的 Wi-Fi 圖示、AirDrop、Sidecar 或 Find My。

### 第二層：NetworkingDriverKit 僅支援乙太網路

Apple 取代核心擴充功能的現代方案是 **DriverKit**，即不會威脅核心穩定性的使用者空間驅動程式。網路系列 `NetworkingDriverKit` 在 [Apple 官方文件](https://developer.apple.com/documentation/networkingdriverkit)中明確指出：

>「使用 NetworkingDriverKit 開發 USB 乙太網路網卡的驅動程式。請注意，**乙太網路是 NetworkingDriverKit 目前唯一支援的網路介面。**」

不存在 `IOUserNetworkWiFi` 類別。沒有 Wi-Fi 的 DriverKit 框架。即使 Realtek 或 MediaTek 投入工程資源撰寫 DriverKit 驅動程式，**也沒有 Apple 框架可以插入它。**

### 第三層：USB + 網路 kext 組合自 Big Sur 起不再支援

Apple 的 [已淘汰核心擴充功能](https://developer.apple.com/support/kernel-extensions/)頁面指出：

>「同時使用 IONetworkingFamily KPI 與任何 USB KPI（IOUSBHostFamily 或 IOUSBFamily）在 **macOS Big Sur 中不支援。**」

這正是每個 USB Wi-Fi 核心擴充功能所需的 KPI 組合。唯一的逃生門是完全停用 SIP 或使用 MDM 設定檔，這兩者都不適合消費性產品。

### 第四層：Realtek 的 kext 僅支援 x86_64

Realtek 的 macOS 驅動程式以 `RtWlanU.kext` 發行，僅針對 **x86_64** 編譯。Apple Silicon Mac 執行的是 **ARM64** 核心。核心擴充功能在核心空間執行，**Rosetta 2 無法翻譯核心擴充功能。**

[chris1111 討論區 #128](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter/discussions/128) 上的一位使用者記錄了 M1 MacBook Air 搭配 Ventura 13.1 與 ALFA AWUS1900 的確切失敗訊息：

```
Domain=KMErrorDomain Code=71
不相容的架構：二進位檔是 x86_64，但需要 arm64
Kext com.realtek.driver.RtWlanU v1830.32.b27
```

### 第五層：Realtek 已放棄 macOS 驅動程式開發

[chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter)（Realtek macOS Wi-Fi 驅動程式的實際社群發行版）的維護者在 README 中明確表示：

>**「這在 Mac M1、M2、M3、M4 Apple 晶片上似乎無法運作，僅適用於 Mac Intel。」**

並在使用者詢問是否可新增 M1 支援時回應：

>「傳統 kext 擴充功能需要為 M1 Mac 重新撰寫（即使透過 Rosetta 2 也無法運作），這意味著需要大型廠商更新其驅動程式以支援 M1。」

Realtek 從未發行 arm64 kext、DriverKit 驅動程式，或任何針對 Apple Silicon 支援的公開計畫。經濟誘因微乎其微：每台 Apple Silicon Mac 已經內建 Wi-Fi。

### 第六層：Apple Silicon 的 kext 載入是刻意設計的敵對環境

即使存在 arm64 kext，在 Apple Silicon 上載入它也需要：

1. 關閉 Mac
2. **按住並持續按住**電源按鈕直到出現啟動選項
3. 進入唯一真正的復原模式（1TR）
4. 降級為**降低安全性**原則
5. 啟用「允許使用者管理來自已識別開發者的核心擴充功能」
6. 重新啟動、安裝 kext、在系統設定中核准
7. **再次重新啟動**以重建輔助核心集合（AuxKC）

根據 Apple 的 [安全地延伸核心](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web)指南，此流程是刻意設計為困難的：「1TR 與密碼要求的組合使得僅從 macOS 內部啟動的軟體攻擊者難以注入 kext。」

> [!IMPORTANT]
> **結論：** 沒有任何 ALFA 網卡，也沒有任何第三方 USB Wi-Fi 網卡，能在 Apple Silicon macOS 上原生運作。除非 Apple 發布 Wi-Fi DriverKit 框架（他們沒有）且廠商為其撰寫驅動程式（目前沒有），否則此狀況不會改變。

---

## 3. Intel Mac：什麼仍可用（以及什麼不可用）

如果你的團隊仍在使用 Intel Mac，情況較好，但僅限基本 Wi-Fi 連線，不適用於安全稽核。

### 4.1 macOS 版本支援時間軸

| ALFA 型號 | 晶片組 | 官方 macOS 限制 | 社群驅動程式（chris1111）|
|------------|---------|---------------------|------------------------------|
| AWUS036ACH | RTL8812AU | 10.15 Catalina | 11 Big Sur 至 26 Tahoe（僅 Intel）|
| AWUS036ACS | RTL8811AU | 10.14 Mojave | 11 Big Sur 至 26 Tahoe（僅 Intel）|
| AWUS036ACM | MT7612U | **10.12 Sierra** |❌ 不支援（MediaTek）|
| AWUS036ACHM | MT7610U |❌ 無 |❌ 不支援（MediaTek）|
| AWUS036AX/AXER | RTL8832BU |❌ 無 |❌ 無 |
| AWUS036AXML/AXM | MT7921AUN |❌ 無 |❌ 無 |

### 4.2 監控模式的悖論

安全專業人士面臨的關鍵問題是：**即使驅動程式成功安裝在 Intel Mac 上，監控模式與封包注入仍然無法運作。**

ALFA 的 macOS 驅動程式僅實作客戶端連線功能，並未實作監控模式 API。這在 [Super 討論](https://super.com/questions/1597114/alfa-wifi-network-card-monitor-mode-on-mac-os)中獲得確認，一位使用者成功安裝了 AWUS036EAC 驅動程式，但無法進入監控模式：

>「你怎麼認為 ALFA 將監控模式支援放入他們的 macOS 驅動程式？不同作業系統的監控模式 API 不同。我假設他們只是沒有費心為 macOS 實作它。」

這形成了一個悖論：**你購買 ALFA 網卡專門為了監控模式與封包注入，但 macOS 驅動程式不支援這兩項功能。** macOS 內建的 Wi-Fi 網卡實際上支援監控模式（透過 `airport` 公用程式），但 ALFA 的驅動程式沒有為他們的硬體實作此功能。

> [!WARNING]
> 如果你的目標是無線安全稽核（監控模式、封包注入、握手封包擷取、解除驗證攻擊），**macOS 無法做到，無論哪種 Mac、Intel 或 Apple Silicon、搭配任何 ALFA 網卡。** 你需要 Linux。

### 4.3 chris1111 驅動程式：Intel Mac 的最後手段

對於執行 macOS 11 Big Sur 或更新版本的 Intel Mac，唯一的選擇是 [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) 專案，這是一個由社群維護的 Realtek kext 發行版。

**需求：**
- 僅限 Intel Mac（不支援 Apple Silicon）
- 必須停用系統完整性保護（SIP）
- 此 kext 未經 Realtek/ALFA/Apple 簽署

**支援的網卡：** 僅 AWUS036ACH（RTL8812AU）與 AWUS036ACS（RTL8811AU）。

Rokland（ALFA 的美國經銷商）[強烈警告](https://store.rokland.com/blogs/news/apple-mac-os-11-big-sur-compatibility-update-for-alfa-awus036ach-other-products)：「我們強烈建議不要在你的 Mac 是主要電腦且執行關鍵任務時使用此驅動程式。」

---

## 4. 可行的解決方案：虛擬機器 + USB 直通

由於 macOS 無法原生執行 ALFA 網卡（即使能，監控模式也無法運作），Mac 安全團隊的實際解決方案是在**虛擬機器中執行 Linux**，並透過 USB 將 ALFA 網卡直通。

此方案適用於**所有 Apple Silicon Mac**（M1/M2/M3/M4）與所有 Intel Mac。監控模式與封包注入的功能與原生 Linux 機器完全相同。

### 5.1 你需要什麼

| 元件 | 建議 | 價格 |
|-----------|---------------|------|
| 虛擬機器軟體 | [UTM](https://mac.getutm.app/)（免費、開源）| 免費 |
| 替代方案 | Parallels Desktop 或 VMware Fusion（ARM）| 每年 99 美元 |
| Linux ISO | [Kali Linux ARM64](https://www.kali.org/get-kali/) | 免費 |
| ALFA 網卡 | AWUS036ACH（最佳）或 AWUS036ACM（即插即用）| 40–70 美元 |
| USB 轉接器 | USB-C 轉 USB-A 轉接器（如果 ALFA 網卡是 USB-A 接頭）| 10 美元 |

### 5.2 逐步設定

#### 步驟 1：建立 Kali Linux ARM 虛擬機器

下載 Kali Linux ARM64 安裝程式，並在 UTM 中建立新的虛擬機器：
- **架構：** ARM64（aarch64）
- **記憶體：** 最少 2 GB（建議 4 GB）
- **CPU：** 2 核以上
- **USB 控制器：** USB 3.0（xHCI），**這很關鍵**

> [!IMPORTANT]
> 你必須將虛擬機器的 USB 控制器設定為 **USB 3.0（xHCI）**，而非 USB 2.0。USB 2.0 控制器會導致高功率 ALFA 網卡間歇性斷線，特別是在封包注入期間。

#### 步驟 2：在虛擬機器中安裝 ALFA 驅動程式

**AWUS036ACH（RTL8812AU）：**

如果你的 Kali 核心版本**≥6.14**，`rtw88` 主線驅動程式已內建，無需安裝。對於較舊的核心：

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) git
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
```

**AWUS036ACM（MT7612U），零安裝：**

MediaTek MT7612U 驅動程式自 Linux 4.19 版本起已內建於核心。插入即可使用：

```bash
lsusb
# Bus 001 Device 005: ID 0e8d:7612 MediaTek Inc.

iw dev
# wlan0 應該會自動出現
```

**AWUS036AXML / AWUS036AXM（MT7921AUN）：**

自 Linux 5.18 起已內建於核心，但需要韌體檔案：

```bash
sudo apt install -y firmware-misc-nonfree
# 驗證韌體是否存在：
ls /lib/firmware/mediatek/
# WIFI_MT7922_patch_mcu_1_1_hdr.bin
# WIFI_RAM_CODE_MT7922_1.bin
```

#### 步驟 3：設定 USB 直通

1. 將 ALFA 網卡插入 Mac 的 USB-C/Thunderbolt 埠（如需可使用 USB-C 轉 USB-A 轉接器）
2. 在 UTM 中：虛擬機器選單列→USB→選擇 ALFA 裝置→分配給虛擬機器
3. 在 Parallels 中：虛擬機器設定→硬體→USB 與藍牙→勾選「USB 3.0」→將 ALFA 裝置分配給虛擬機器

#### 步驟 4：驗證監控模式與封包注入

```bash
# 驗證虛擬機器內已識別裝置
lsusb
# Bus 003 Device 005: ID 0bda:8812 Realtek ... RTL8812AU

# 啟用監控模式
sudo airmon-ng start wlan0
# (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)

# 確認監控模式已啟用
iw dev wlan0mon info
# Mode: monitor

# 測試封包注入能力
sudo aireplay-ng --test wlan0mon
# "Injection is working!" 確認成功
```

### 5.3 已知問題與疑難排解

| 問題 | 原因 | 解決方案 |
|-------|-------|----------|
| 大量掃描期間網卡斷線 | USB 3.0 模式切換 bug（morrownr/USB-WiFi #676）| 在網卡與 Mac 之間使用 USB 2.0 集線器 |
| `airmon-ng` 看不到網卡 | 虛擬機器設定中的 USB 控制器錯誤 | 將虛擬機器 USB 設定為 USB 3.0（xHCI），而非 USB 2.0 |
| 驅動程式無法在虛擬機器中編譯 | 缺少核心標頭檔 | `sudo apt install linux-headers-$(uname -r)` |
| 網卡已識別但無監控模式 | RTL8832BU 晶片組（AWUS036AX/AXER）| 此晶片組的監控模式支援有限，請改用 AWUS036ACH |

### 5.4 替代方案：以 Raspberry Pi 作為遠端滲透測試節點

對於偏好專用硬體方案的團隊，執行 Kali Linux 的 **Raspberry Pi 4 或 5** 是優秀的行動無線稽核節點。Mac 僅用作 SSH 終端機。

**優勢：**
- 完全避開 macOS 驅動程式問題
- AWUS036ACM 在 Pi 上即插即用（核心內驅動程式，零安裝）
- 成本：Pi 5 + ALFA 網卡低於 200 美元
- 便攜且不影響主要工作機器

```bash
# 從你的 Mac SSH 進入 Pi：
ssh kali@192.168.1.100

# 在 Pi 上執行無線稽核：
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
sudo aireplay-ng --test wlan1mon
```

---

## 5. USB 硬體指南：在 Mac 上使用哪個埠

ALFA 網卡是 USB 2.0 或 USB 3.0 裝置，通常配備 USB-A 接頭，耗電量介於 500 mA（2.5 W）至 900 mA（4.5 W）之間。並非所有 Mac USB 埠都提供足夠的電力，而 Mac Mini M4（2024）有一個你需要知道的關鍵特性。

### 6.1 Mac USB 埠電力參考

| Mac 型號 | USB-A 埠 | USB-A 電力 | USB-C/TB 埠 | USB-C 電力 | ALFA 直接插入？|
|-----------|-------------|-------------|----------------|-------------|-------------------|
| MacBook 12"（2015–2017）|❌ 無 | N/A | 1× USB-C 3.1 Gen 1 | 900 mA |❌ 需要轉接器 |
| MacBook Air Intel（2010–2017）|✅ 2× | 900 mA | 1× TB1/TB2 | N/A |✅ 直接插入 |
| MacBook Air Intel（2018–2020）|❌ 無 | N/A | 2× TB3 | 15 W / 7.5 W |❌ 需要轉接器 |
| MacBook Air M1/M2/M3 |❌ 無 | N/A | 2× TB/USB 4 | 15 W / 7.5 W |❌ 需要轉接器 |
| MacBook Pro Intel（2012–2015）|✅ 2× | 900 mA | 2× TB2 | N/A |✅ 直接插入（最佳世代）|
| MacBook Pro Intel（2016–2019）|❌ 無 | N/A | 4× TB3 | 15 W / 7.5 W |❌ 需要轉接器 |
| MacBook Pro M1（2020）|❌ 無 | N/A | 2× TB/USB 4 | 15 W / 7.5 W |❌ 需要轉接器 |
| MacBook Pro M1 Pro/Max（2021+）|❌ 無 | N/A | 3× TB4 | 15 W 每埠 |❌ 需要轉接器 |
| MacBook Pro M2/M3/M4 Pro/Max |❌ 無 | N/A | 3× TB4 或 TB5 | 每埠 15 W 以上 |❌ 需要轉接器 |
| Mac Mini Intel（2014）|✅ 4× | 900 mA | 2× TB2 | N/A |✅ 直接插入 |
| Mac Mini Intel（2018）|✅ 2× | 900 mA | 4× TB3 | 15 W / 7.5 W |✅ 直接插入 |
| Mac Mini M1（2020）|✅ 2× | 900 mA | 2× TB/USB 4 | 15 W / 7.5 W |✅ 直接插入 |
| Mac Mini M2/M2 Pro（2023）|✅ 2× | 900 mA | 2–4× TB4 | 每埠 15 W |✅ 直接插入 |
| **Mac Mini M4/M4 Pro（2024）**|**❌ 無** | **N/A** | 前方：2× USB-C / 後方：3× TB4 或 TB5 | **前方：500 mA / 後方：900 mA 以上** | **❌ 僅後方 TB 埠** |
| Mac Studio（所有世代）|✅ 2×（後方）| 900 mA | 4× TB4 或 TB5（後方）| 每埠 15 W |✅ 直接插入 |

### 6.2 關鍵警告：Mac Mini M4（2024）

Mac Mini M4/M4 Pro 是**首款沒有 USB-A 埠的 Mac Mini。** 更重要的是，兩個前方 USB-C 埠僅提供**約 500 mA**，不足以供應需要 900 mA 的 USB 3.0 ALFA 網卡。

> [!WARNING]
> 在 Mac Mini M4 上，**請務必將 ALFA 網卡插入後方 Thunderbolt 4/5 埠**，使用 USB-C 轉 USB-A 轉接器。前方 USB-C 埠（500 mA）會導致高功率 ALFA 網卡的電力不穩定與連線斷線。

### 6.3 Thunderbolt 電力分配規則

- **Thunderbolt 3（Intel Mac，2016–2020）：** 前兩個埠 15 W（3 A），額外埠 7.5 W（1.5 A），先到先得。優先插入你的 ALFA 網卡以取得完整 15 W。
- **Thunderbolt 4（Apple Silicon，2021+）：** 每埠 15 W（3 A），無分配限制。
- **USB-A 埠（所有有該埠的 Mac）：** 一律 900 mA（USB 3.0 規格），足以供應任何 ALFA 網卡。

---

## 6. 依使用情境的購買建議

### 7.1 針對 Apple Silicon Mac 使用者（M1/M2/M3/M4）

| 使用情境 | 推薦網卡 | 原因 | 設定方式 |
|----------|-----------------|-----|--------------|
| **最佳監控模式與注入** | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | RTL8812AU，Kali Linux 黃金標準，驅動程式最成熟 | 虛擬機器 + USB 直通 |
| **最佳即插即用體驗** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | MT7612U，自 Linux 4.19 起已內建於核心，零驅動程式安裝 | 虛擬機器 + USB 直通 |
| **Wi-Fi 6E / 6 GHz 測試** | [AWUS036AXML](https://yupitek.com/en/products/alfa/awus036axml/) | MT7921AUN，自 Linux 5.18 起已內建於核心，三頻 + BT 5.2 | 虛擬機器 + USB 直通 |
| **預算 / 初學者** | [AWUS036ACS](https://yupitek.com/en/products/alfa/awus036acs/) | RTL8811AU，價格實惠，支援監控模式與注入 | 虛擬機器 + USB 直通 |
| **行動專用節點** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | 在 Raspberry Pi 上零安裝，低耗電（600 mA）| Raspberry Pi + Kali |

### 7.2 針對 Intel Mac 使用者（僅客戶端連線）

| macOS 版本 | 推薦網卡 | 驅動程式方法 | 限制 |
|---------------|-----------------|---------------|------------|
| 10.15 Catalina 或更早 | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | 官方 ALFA 驅動程式 | 僅客戶端，無監控模式 |
| 11 Big Sur 或更新 | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | [chris1111 驅動程式](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter)（停用 SIP）| 僅客戶端，無監控模式 |

> [!IMPORTANT]
> 要在**任何** Mac（Intel 或 Apple Silicon）上執行無線安全稽核，你仍然需要 Linux，無論是在虛擬機器或 Raspberry Pi 上。macOS 驅動程式不支援監控模式或封包注入，沒有例外。

### 7.3 Mac 使用者應避免的網卡

| 網卡 | 避免原因 |
|------|-----------|
| AWUS036AX / AWUS036AXER（RTL8832BU）| 在 Linux 中監控模式支援有限且不穩定，無 macOS 驅動程式 |
| AWUS036EACS（RTL8821CU）| **完全**不支援監控模式，不適用於安全稽核 |
| AWUS036ACHM（MT7610U）| 無 macOS 驅動程式（chris1111 不支援 MediaTek），需要 Linux 編譯 |

---

## 7. 常見問題：ALFA 無線網卡於 Apple Mac

> [!NOTE]
> 本 FAQ 章節為答案引擎最佳化（AEO）而設計。每個問題在第一句就給出明確答案，以便 AI 搜尋引擎（ChatGPT、Perplexity、Google AI Overviews）能直接引用這些答案。

### ALFA AWUS036ACH 能在 M1/M2/M3/M4 Mac 上運作嗎？

**不能。** AWUS036ACH（RTL8812AU）無法在任何 Apple Silicon Mac 上原生運作。Realtek 的 macOS 驅動程式僅針對 x86_64 編譯，無法在 ARM64 核心上載入。不過，它在 Linux 虛擬機器（UTM/Parallels）中搭配 USB 直通運作完美，包含完整的監控模式與封包注入支援。

### 我能在 macOS 上使用 ALFA 無線網卡執行監控模式嗎？

**不能。** ALFA 的 macOS 驅動程式不實作監控模式或封包注入，僅支援基本 Wi-Fi 客戶端連線。這適用於所有 macOS 版本，無論 Intel 或 Apple Silicon Mac。如需監控模式，你必須使用 Linux（無論是在虛擬機器或獨立裝置如 Raspberry Pi 上）。

### 哪張 ALFA 無線網卡最適合 Mac 使用者？

對於執行無線安全稽核的 Mac 使用者，**AWUS036ACH**（RTL8812AU）是最佳選擇，它是監控模式與封包注入的 Kali Linux 黃金標準。如需零安裝的即插即用體驗，建議選擇 **AWUS036ACM**（MT7612U），因為其驅動程式自 Linux 4.19 起已內建於核心。

### 為什麼我的 ALFA 網卡無法在我的 MacBook Pro M3 上運作？

Apple Silicon Mac（M1/M2/M3/M4）使用無法載入 x86_64 核心擴充功能的 ARM64 核心。Realtek 的 macOS Wi-Fi 驅動程式僅支援 x86_64，而 Rosetta 2 無法翻譯核心擴充功能。此外，Apple 的 NetworkingDriverKit 框架僅支援乙太網路，不支援 Wi-Fi，因此也沒有現代的 DriverKit 路徑。Realtek 已放棄 macOS 驅動程式開發。

### 有任何 USB Wi-Fi 網卡能在 Apple Silicon macOS 上運作嗎？

**沒有。** 截至 2026 年，沒有任何第三方 USB Wi-Fi 網卡（無論 ALFA、TP-Link、Netgear、ASUS 等品牌）能在 Apple Silicon macOS 上原生運作。這是架構限制，而非驅動程式可用性問題。Apple 的官方建議是使用搭配乙太網路的旅行路由器。

### 我能使用 Mac 內建的 Wi-Fi 執行監控模式嗎？

**可以，但有限制。** macOS 內建的 Wi-Fi 支援透過 `airport` 公用程式（`sudo airport en0 sniff 11`）執行基本監控模式。然而，它一次只能偵測一個頻道，不支援封包注入，且內建天線的範圍有限。對於專業的無線稽核，需要搭配 Linux 虛擬機器使用外部 ALFA 網卡。

### 讓 ALFA 網卡在 Mac 上運作的最簡單方法是什麼？

最簡單的方法是：安裝 [UTM](https://mac.getutm.app/)（免費）→ 建立 Kali Linux ARM 虛擬機器→ 插入 AWUS036ACM（MT7612U）→ 透過 USB 直通將它分配給虛擬機器。MT7612U 驅動程式自 Linux 4.19 起已內建於核心，因此無需安裝驅動程式，插入即可使用。

### 我需要在 Mac 上為 ALFA 網卡使用供電 USB 集線器嗎？

在有 USB-A 埠的 Mac 上（Mac Mini、Mac Studio、較舊的 MacBook Pro/Air），不需要，900 mA 輸出已足夠。在僅有 USB-C/Thunderbolt 埠的 Mac 上，15 W（3 A）輸出遠遠足夠。唯一的例外是 Mac Mini M4 的前方 USB-C 埠，僅提供 500 mA，請改用後方 Thunderbolt 埠。

---

## 8. 資源與驅動程式連結

### 官方資源

| 資源 | URL |
|----------|-----|
| Yupitek 官方網站 | [https://www.yupitek.com](https://www.yupitek.com) |
| Yupitek ALFA 產品頁面 | [https://yupitek.com/en/products/alfa/](https://yupitek.com/en/products/alfa/) |
| ALFA Network 官方 | [https://www.alfa.com.tw](https://www.alfa.com.tw) |
| Yupitek ALFA 比較表 | [https://yupitek.com/alfa_compare.html](https://yupitek.com/alfa_compare.html) |

### Linux 驅動程式儲存庫（GitHub）

| 晶片組 | ALFA 型號 | GitHub 儲存庫 | 驅動程式類型 |
|---------|-------------|-------------------|-------------|
| RTL8812AU | AWUS036ACH, AWUS036ACS | [morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820) | DKMS（推薦）|
| RTL8812AU | AWUS036ACH | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) | 社群（已淘汰）|
| RTL8812AU | AWUS036ACH | [lwfinger/rtw88](https://github.com/lwfinger/rtw88) | 主線（核心≥6.14）|
| MT7612U | AWUS036ACM | Linux 核心內建（`mt76`）| 核心內建（≥4.19）|
| MT7921AUN | AWUS036AXML, AWUS036AXM | Linux 核心內建（`mt7921u`）| 核心內建（≥5.18）|
| MT7610U | AWUS036ACHM | [imzyxwvu/mt7610u](https://github.com/imzyxwvu/mt7610u) | 核心外 |
| RTL8832BU | AWUS036AX, AWUS036AXER | [morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi) | 有限支援 |

### macOS 驅動程式（僅 Intel Mac）

| 驅動程式 | URL | 支援的 macOS | Apple Silicon |
|--------|-----|-----------------|---------------|
| chris1111 Wireless-USB-Big-Sur-Adapter | [GitHub](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) | Catalina 至 Tahoe 26 |❌ 僅 Intel |

### Apple 開發者文件

| 文件 | URL |
|----------|-----|
| 已淘汰核心擴充功能 | [developer.apple.com/support/kernel-extensions/](https://developer.apple.com/support/kernel-extensions/) |
| NetworkingDriverKit（僅乙太網路）| [developer.apple.com/documentation/networkingdriverkit](https://developer.apple.com/documentation/networkingdriverkit) |
| 安全地延伸核心 | [support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) |

### 虛擬機器軟體

| 軟體 | URL | 價格 |
|----------|-----|------|
| UTM | [mac.getutm.app](https://mac.getutm.app/) | 免費 |
| Parallels Desktop | [parallels.com](https://www.parallels.com/) | 每年 99 美元 |
| VMware Fusion | [vmware.com](https://www.vmware.com/products/fusion.html) | 個人使用免費 |

---

*本文基於來自 Apple 開發者文件、GitHub 儲存庫（chris1111、aircrack-ng、morrownr）、ALFA Network 產品規格、Reddit/GitHub 社群報告與實際測試文件的技術研究彙整而成。所有產品建議均基於 Yupitek 目前現貨的 ALFA 產品線。*

*⚠️ 本文所述設備與技術僅供授權資訊安全稽核與合法滲透測試使用。使用者必須確保符合當地法律法規。*

---
*文章版本：1.0 | 2026-06-20 | Yupitek Ltd.*