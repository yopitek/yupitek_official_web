---
title: "Flipper Zero 與 Flipper One 搭配 ALFA 無線網卡：完整相容性指南"
description: "Flipper Zero 能接 ALFA USB 無線網卡做封包注入嗎？不行——這裡解釋為什麼。Flipper One 支援 ALFA AWUS036AXML，完整監聽模式與封包注入。包含晶片分析、驅動相容性與設定步驟的完整指南。"
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-alfa-compatibility"
tags: ["flipper-zero", "flipper-one", "alfa-network", "wifi-adapter", "monitor-mode", "packet-injection", "kali-linux", "pentesting", "AWUS036AXML", "wireless-security"]
categories: ["Technical"]
featureimage: "/images/blog/flipper-alfa-compatibility.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Flipper Zero 可以連接 ALFA USB 無線網卡嗎？"
    answer: "不行。Flipper Zero 的 STM32WB55 微控制器僅支援 USB device 模式，硬體上無法作為 USB host 驅動外接網卡。"
  - question: "Flipper One 支援哪些 ALFA 網卡型號？"
    answer: "Flipper One 創辦人特別測試 AWUS036AXML 為首選，AWUS036ACM 為最佳 CP 值，兩者驅動皆已內建於 mainline Linux 核心。"
  - question: "為什麼 AWUS036AXML 是 Flipper One 首選網卡？"
    answer: "AWUS036AXML 採用 MT7921AUN 晶片，mt7921u 驅動自 Linux 5.18 起內建於核心，支援完整 2.4/5/6 GHz 三頻段與監聽模式。"
  - question: "Flipper One 何時正式上市？"
    answer: "Flipper One 目前處於開發者預覽階段，正式上市時間與定價將透過群眾募資公布，詳情請追蹤 flipper.net。"
  - question: "Flipper Zero 的 WiFi Dev Board 能取代 ALFA 網卡嗎？"
    answer: "不能。WiFi Dev Board 僅支援 2.4 GHz 基本功能，無 USB host，範圍與注入可靠性遠不及專用 ALFA 網卡。"
---

Flipper Zero 因硬體限制無法使用任何 ALFA USB 無線網卡；Flipper One 則完整支援 AWUS036AXML 等型號，可執行監聽模式與封包注入。

{{< tldr >}}
Flipper Zero 的 STM32WB55 僅支援 USB device 模式，無法驅動任何 ALFA 網卡；Flipper One 搭載 RK3576 與完整 Debian Linux，支援 AWUS036AXML 執行三頻監聽與注入。
{{< /tldr >}}

{{< alert "triangle-exclamation" >}}
**法律聲明：** Monitor Mode 與 Packet Injection 僅限在您擁有或已取得明確書面授權的網路上進行測試。未經授權的無線通訊攔截在大多數司法管轄區屬違法行為。本指南中的所有技術僅供**授權滲透測試、自有設備安全研究及教育目的**使用。
{{< /alert >}}

## 前言：每個滲透測試人員都會問的問題

如果你擁有一台 Flipper Zero——或正在考慮購買——而且聽過 ALFA Network 在無線安全測試領域鼎鼎大名的 USB 無線網卡，你可能也問過自己：**「我可以把 ALFA 網卡插到 Flipper Zero 上，開始捕捉 WPA2 握手封包嗎？」**

簡短的答案是：不行——但完整的答案有趣多了。

**Flipper Zero 無法連接任何 ALFA USB 無線網卡。** 這是硬體限制，不是軟體問題。Flipper Zero 內部的 STM32WB55 微控制器，其 USB 控制器只能在 **device-only 模式**下運作——它實體上無法作為 USB host 來驅動外接裝置，例如 WiFi 網卡。

但 Flipper Devices 已經宣布了一款全新的產品：**Flipper One**。基於 Rockchip RK3576 處理器，配備 8 GB 記憶體，運行完整的 Debian Linux，Flipper One 擁有兩個 USB 3.1 host 連接埠，可以直接使用 ALFA 網卡進行完整的無線安全測試——包括 6 GHz Wi-Fi 6E 分析。事實上，Flipper One 創辦人 Pavel Zhovner 在產品公告中，特別指名 **ALFA AWUS036AXML** 為官方測試網卡。

本文將完整說明相容性全貌：什麼能用、什麼不行、為什麼，以及如何設定。

---

## Flipper Zero：為什麼不能使用 ALFA 網卡

要理解這個限制，你需要了解 Flipper Zero 內部有什麼。

### 硬體規格

| 元件 | 規格 |
|-----------|--------------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **架構** | ARM Cortex-M4（應用核心）@ 64 MHz + ARM Cortex-M0+（無線核心）@ 32 MHz |
| **RAM** | 256 KB（核心之間共享） |
| **儲存** | 1 MB Flash + MicroSD |
| **作業系統** | FreeRTOS（即時作業系統） |
| **USB** | USB Type-C，USB 2.0 Full Speed（12 Mbps） |
| **USB 模式** | **Device only**——無 host 或 OTG 能力 |

### USB 限制

STM32WB55 的 USB 控制器是一個 **USB Full-Speed Device Controller**。它可以讓 Flipper Zero 以 USB 裝置的身份連接到電腦（用於檔案傳輸、韌體更新和 CLI 介面），但無法作為 USB host。這顆晶片上沒有 host 控制器硬體——再多的韌體修改也無法增加這項能力。

要使用 ALFA USB 無線網卡，裝置需要：
1. **USB Host 控制器硬體**——用於列舉並與 USB 裝置通訊
2. **Linux 核心與 WiFi 驅動支援**——載入 `mt7921u`、`mt76` 或 `rtw88` 等驅動程式
3. **足夠的供電能力**——ALFA 網卡通常消耗 500 mA 至 900 mA @ 5V

Flipper Zero 三項全都不符合：
- ❌ 無 USB Host 控制器（硬體限制）
- ❌ 運行 FreeRTOS，非 Linux——不存在核心驅動框架
- ⚠️ GPIO 5V 輸出在所有腳位總和不超過 1.2A，且需手動啟用

> **結論：** 將任何 ALFA USB 無線網卡連接到 Flipper Zero 是**實體上不可能**的。這不是可以透過軟體、韌體更新或擴充板繞過的硬體限制——它已刻在晶片設計中。

---

## Flipper Zero + WiFi Dev Board：有限的替代方案

Flipper Devices 銷售一款基於 **ESP32-S2** 微控制器的官方 **WiFi Dev Board**。這塊板子透過 GPIO 排針插入 Flipper Zero，提供基本的 2.4 GHz WiFi 功能——但它**不會**改變 USB host 的情況。

| 面向 | 能力 |
|--------|-----------|
| **WiFi 晶片** | ESP32-S2（Xtensa LX7 單核，240 MHz） |
| **頻率** | 僅 2.4 GHz，802.11 b/g/n |
| **USB Host** | ❌ WiFi Dev Board 未暴露 USB Host——ESP32-S2 透過 GPIO 連接 Flipper Zero，非 USB |
| **韌體** | ESP32 Marauder（社群開發） |

安裝 **ESP32 Marauder 韌體**後，WiFi Dev Board 可以執行：

- ✅ Deauthentication 攻擊（僅 2.4 GHz）
- ✅ PMKID 捕捉（僅 2.4 GHz）
- ✅ 存取點掃描與 SSID 廣播
- ✅ 基本封包嗅探（僅 2.4 GHz）

它**無法**做到：

- ❌ 使用外接 ALFA USB 網卡（無 USB host）
- ❌ 在 5 GHz 或 6 GHz 頻段上運作
- ❌ 達到專用 ALFA 網卡的範圍或注入可靠性
- ❌ 執行基於 Linux 的工具，如 aircrack-ng、Kismet 或 Wireshark

> **如果你只有 Flipper Zero 且需要基本的 2.4 GHz 測試**，WiFi Dev Board 搭配 ESP32 Marauder 是一個可行但**嚴重受限**的變通方案。若需要更多功能，你需要不同的硬體。

---

## Flipper One：ALFA 等待已久的平台

2026 年 5 月 21 日，Flipper Devices 創辦人 Pavel Zhovner 發表了一篇部落格文章，標題為 *「Flipper One — We Need Your Help」*，宣布了一款全新的產品。Flipper One 不是 Flipper Zero 的升級版——它是一個完全不同的裝置類別，設計用於不同的協議層級。

> *「Flipper Zero 是 Layer 0——離線點對點存取控制：NFC、RFID、Sub-GHz、紅外線。Flipper One 是 Layer 1——IP 連線：Wi-Fi、Ethernet、5G、衛星。兩者不互相取代。」*
> —— Pavel Zhovner，flipper.net

{{< alert "circle-info" >}}
**供貨狀態提示：** Flipper One 目前處於**開發者預覽**階段。正式上市時間、定價及地區銷售將透過群眾募資公布。請追蹤 [flipper.net](https://flipper.net) 和 [Flipper One Developer Portal](https://docs.flipper.net/one) 取得最新消息。
{{< /alert >}}

### 硬體規格

| 元件 | 規格 |
|-----------|--------------|
| **CPU** | Rockchip RK3576：4× Cortex-A72 + 4× Cortex-A53，最高 2.2 GHz |
| **GPU** | ARM Mali-G52 MC3（OpenGL ES 3.2、Vulkan 1.2） |
| **NPU** | 6 TOPS @ INT8（可本地執行 LLM） |
| **協處理器** | Raspberry Pi RP2350B（雙 M33 + 雙 RISC-V），負責螢幕/按鍵/電源 |
| **RAM** | 8 GB LPDDR5 |
| **儲存** | 64 GB UFS 2.2 + MicroSD |
| **作業系統** | Debian 13（Trixie）——Flipper Devices 聲稱將採用 mainline Linux Kernel 7.0，無 out-of-tree patch 依賴 |
| **USB Host** | USB-C2 + USB-A，皆為 USB 3.1（5 Gbps），皆支援 host 模式 |
| **內建 WiFi** | Wi-Fi 6E via MT7921AUN（2.4/5/6 GHz，2×2 MIMO） |
| **Ethernet** | 2× RJ45 Gigabit（支援 inline/MitM 嗅探） |
| **M.2 擴充** | Key-B：PCIe 2.1 ×1 / USB 3.1 / SATA3 / SIM 卡 |

### 為什麼 Flipper One 能使用 ALFA 網卡

與 Flipper Zero 不同，Flipper One 滿足全部三項要求：

1. ✅ **USB 3.1 Host 控制器**：兩個 host-capable USB 連接埠，可列舉並供電給外接裝置
2. ✅ **完整 Debian Linux**：標準 Linux 核心，支援 `mt7921u`、`mt76` 和 `rtw88` 的 in-kernel 驅動
3. ✅ **充足供電**：USB 連接埠可提供標準匯流排電源；GPIO 提供 5V @ 2A 和 3.3V @ 2A，含 eFuse 保護

USB 3.1 的頻寬（5 Gbps）綽綽有餘——即使是最快的 ALFA 網卡（AWUS036AXML，AXE3000），也受限於 USB 3.0 的實際吞吐量約 1.2 Gbps。

### 軟體環境

Flipper One 運行標準的 Debian 環境，意味著你可以直接透過 `apt` 安裝無線安全工具：

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

Flipper One 還引入了 **Flipper OS Profiles**——一種基於快照的系統，讓你可以建立乾淨、隔離的環境。你可以維護一個專門的「Pentest」profile，安裝所有無線工具，並在需要日常使用時切換回乾淨的 profile，互不干擾。

---

## Flipper One 推薦 ALFA 網卡

並非所有 ALFA 網卡在無線安全測試上的表現都一樣好。關鍵因素是**晶片組**、**驅動成熟度**和 **in-kernel 支援**（表示無需 DKMS 編譯）。

### ⭐⭐⭐⭐⭐ 首選：AWUS036AXML（Wi-Fi 6E）

| 規格 | 詳情 |
|------|--------|
| **晶片組** | MediaTek MT7921AUN |
| **頻段** | 2.4 / 5 / 6 GHz（Wi-Fi 6E） |
| **最大速率** | AXE3000（理論值），實用約 1.2 Gbps |
| **驅動** | `mt7921u`——自 Linux 5.18 起 in-kernel |
| **需要 DKMS** | ❌ 不需要 |
| **天線** | 雙 RP-SMA（可更換）+ Bluetooth 5.2 |

> **為什麼是最佳選擇：** 這是 Flipper One 創辦人特別測試過的網卡。`mt7921u` 驅動已在 mainline kernel 中，無需任何 vendor patch。它支援全部三個 WiFi 頻段（2.4/5/6 GHz），使 Wi-Fi 6E 安全評估具備未來性。Monitor Mode 和 Packet Injection 穩定且經過充分測試。

### ⭐⭐⭐⭐⭐ 最佳 CP 值：AWUS036ACM（Wi-Fi 5 AC1200）

| 規格 | 詳情 |
|------|--------|
| **晶片組** | MediaTek MT7612U |
| **頻段** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速率** | AC1200（300 + 867 Mbps） |
| **驅動** | `mt76`——自 Linux 4.19 起 in-kernel |
| **需要 DKMS** | ❌ 不需要 |
| **天線** | 雙 5 dBi RP-SMA（可更換） |

> **為什麼是最佳 CP 值：** MT7612U 晶片組在滲透測試社群中歷經考驗。`mt76` 驅動已在 kernel 中存在多年，異常穩定。在 kernel 6.5 及以上版本中，Monitor Mode 和 Injection 運作無瑕。價格低於 AXML，為 2.4/5 GHz 測試提供最佳的價格能力比。

### ⭐⭐⭐⭐ 輕量選擇：AWUS036ACHM（Wi-Fi 5 AC433）

| 規格 | 詳情 |
|------|--------|
| **晶片組** | MediaTek MT7610U |
| **頻段** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速率** | AC433（理論值） |
| **驅動** | `mt76`——自 Linux 4.19 起 in-kernel |
| **需要 DKMS** | ❌ 不需要 |
| **天線** | 單高增益 RP-SMA（可更換） |

> **為什麼是輕量選擇：** 最便攜的選項——USB 2.0、單天線、最低功耗。使用與 ACM 相同的 `mt76` 驅動家族。適合重視體積與功耗勝於傳輸量的現場工作。**注意：** 在 ARM64 平台（包括 RK3576）上，同時執行 `airodump-ng` 和 `aireplay-ng` 可能觸發已知的 interface 消失 bug（morrownr issue #379）。使用時請留意。

### ⭐⭐⭐ 替代方案：AWUS036ACH（Wi-Fi 5 AC1200，RTL8812AU）

| 規格 | 詳情 |
|------|--------|
| **晶片組** | Realtek RTL8812AU |
| **頻段** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速率** | AC1200（300 + 867 Mbps） |
| **驅動** | `rtw88`——預期在 Flipper One 規劃的核心上為 in-kernel；舊系統可能需要 DKMS |
| **需要 DKMS** | ❌ Flipper One 上不需要 / ⚠️ 舊核心可能需要 [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS |
| **天線** | 雙 6 dBi RP-SMA（高 TX 功率） |

> **為什麼是替代方案：** RTL8812AU 晶片組在滲透測試領域歷史悠久。預期在 Flipper One 規劃的核心上無需額外 DKMS 模組即可支援。對於舊系統，aircrack-ng DKMS 驅動仍可使用。高增益 6 dBi 天線提供優異的覆蓋範圍，但 MediaTek 系列的網卡因其更成熟的 in-kernel 驅動支援而通常更受推薦。

### ⚠️ 不建議用於滲透測試

以下 ALFA 型號使用 Monitor Mode 和 Packet Injection 的 Linux 驅動不成熟或不穩定的 Realtek 晶片組。**請避免在 Flipper One 的無線安全工作中使用這些型號：**

| 型號 | 晶片組 | 問題 |
|-------|---------|-------|
| AWUS036AX | RTL8832BU | Wi-Fi 6 晶片，2026 年驅動支援仍在發展中 |
| AWUS036AXER | RTL8832BU | 與 AWUS036AX 相同的晶片組問題 |
| AWUS036ACS | RTL8811AU | Monitor Mode 有限，Injection 不穩定 |
| AWUS036EACS | RTL8811CU | Monitor Mode 有限，Injection 不穩定 |

---

## 設定指南：Flipper One + ALFA AWUS036AXML

本指南假設你有一台運行 Debian Linux 的 Flipper One，且網卡已實際連接到 USB host 連接埠。

### 步驟 1：確認網卡已被識別

```bash
# 檢查 USB 裝置列舉
lsusb
# 預期輸出（範例）：
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# 列出無線介面
iw dev
# 預期：wlan0（若內建 WiFi 佔用 wlan0，則為 wlan1）

# 替代檢查方式
ip link show
```

### 步驟 2：確認驅動已載入

```bash
# AWUS036AXML / AWUS036AXM（MT7921AUN）：
lsmod | grep mt7921u

# AWUS036ACM / AWUS036ACHM（MT7612U / MT7610U）：
lsmod | grep mt76

# AWUS036ACH（RTL8812AU）：
lsmod | grep rtw88

# 檢查核心版本（最佳 MT7921AUN 支援建議 6.12+）：
uname -r
```

如果驅動模組有列出，表示已載入且就緒。不需要進一步安裝——這些全部都是 in-kernel 驅動。

### 步驟 3：啟用 Monitor Mode

```bash
# 終止干擾程序（NetworkManager、wpa_supplicant 等）
# 注意：這會同時中斷 Flipper One 的內建 WiFi——請使用專用的
# Flipper OS Profile 進行滲透測試，避免干擾正常網路連線。
sudo airmon-ng check kill

# 在網卡上啟動 Monitor Mode
sudo airmon-ng start wlan0
# 介面重新命名為 wlan0mon

# 確認 Monitor Mode 已啟用
iw dev wlan0mon info
# 應顯示：type monitor
```

手動方法（若不偏好使用 airmon-ng）：

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### 步驟 4：測試 Packet Injection

```bash
# 測試注入能力
sudo aireplay-ng --test wlan0mon
# 看到 "Injection is working!" 表示成功

# 執行基本掃描
sudo airodump-ng wlan0mon

# 掃描所有支援頻段（僅 AWUS036AXML）
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz（aircrack-ng 1.7+）

# 指定頻道掃描
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### 步驟 5：捕捉 WPA2 握手封包

```bash
# Terminal 1：在目標頻道上開始捕捉
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Terminal 2：發送 deauth 強制重新連線
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# 在 Terminal 1 中查看握手捕捉：
# 當出現 "WPA handshake: AA:BB:CC:DD:EE:FF" 表示已捕捉
```

### 步驟 6：恢復正常操作

```bash
# 停止 Monitor Mode 並恢復 managed mode
sudo airmon-ng stop wlan0mon

# 重新啟動網路服務
sudo systemctl restart NetworkManager
```

### 架構總覽

下圖展示 Flipper One 搭配 ALFA 網卡的完整無線滲透測試架構：

![Flipper One + ALFA 無線網卡滲透測試架構](diagram/flipper-alfa-topology.svg)

*拓樸：Flipper One 平台 → ALFA USB 網卡 → 滲透測試工具鏈 → 無線功能*

---

## Flipper Zero vs. Flipper One：並列對照

| 功能 | Flipper Zero | Flipper One |
|---------|:-----------:|:----------:|
| **作業系統** | FreeRTOS | Debian 13（Trixie） |
| **CPU** | STM32WB55（Cortex-M4，64 MHz） | RK3576（8 核 ARM，2.2 GHz） |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **儲存** | 1 MB Flash + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB Host** | ❌ Device only | ✅ USB-C2 + USB-A（USB 3.1） |
| **ALFA 網卡支援** | ❌ | ✅ |
| **內建 WiFi** | ❌（僅 BLE） | ✅ Wi-Fi 6E（MT7921AUN） |
| **5 GHz / 6 GHz WiFi** | ❌ | ✅ |
| **Gigabit Ethernet** | ❌ | ✅ 2× RJ45 |
| **Monitor Mode** | ❌（原生） | ✅ |
| **Packet Injection** | ❌（原生） | ✅ |
| **M.2 擴充** | ❌ | ✅ Key-B（PCIe / USB 3.1 / SATA） |
| **價格** | ~$169 USD（量產中） | 開發者預覽（群眾募資待公布） |

---

{{< faq >}}

---

## 結語：對的工具做對的事

如果你打算使用 ALFA 無線網卡進行無線安全測試，**Flipper Zero 是錯誤的平台**——這並非它的錯。它被設計用於不同的目的：離線存取控制測試（NFC、RFID、Sub-GHz、紅外線）。它在這些任務上表現出色，但 USB host 能力從未納入其設計。

針對**Monitor Mode 和 Packet Injection 搭配 ALFA 網卡**的特定用途，你有兩條路徑：

| 路徑 | 平台 | ALFA 網卡 | 能力 |
|------|----------|-------------|------------|
| **最佳** | Flipper One | AWUS036AXML（MT7921AUN） | 完整 2.4/5/6 GHz，in-kernel 驅動，官方支援 |
| **超值** | Flipper One | AWUS036ACM（MT7612U） | 完整 2.4/5 GHz，in-kernel 驅動，穩定性經過驗證 |
| **變通** | Flipper Zero + WiFi Dev Board | 無（ESP32-S2 內建） | 僅 2.4 GHz，範圍有限，基本功能 |

**Flipper One 代表了一次世代躍進**——它將完整 Debian Linux 環境與 USB 3.1 host 能力的強大功能，帶入一台可攜式、專用硬體平台。搭配 ALFA AWUS036AXML（Flipper One 創辦人特別測試的網卡），你就能在口袋中擁有一套完整的無線安全評估工具。

---

### 哪裡買

所有推薦的 ALFA 網卡均可從 Yupitek——ALFA Network 授權經銷商處購得。瀏覽完整型號或比較規格：

- [ALFA USB 無線網卡——完整型錄](https://yupitek.com/zh-tw/products/alfa/)——所有型號含規格與定價
- [ALFA 產品比較表](/en/alfa_compare/)——晶片組、頻段、驅動的並列比較

### 延伸閱讀

- [Flipper One 官方部落格文章](https://blog.flipper.net/flipper-one-we-need-your-help/)——Pavel Zhovner，2026 年 5 月
- [Flipper One Developer Portal](https://docs.flipper.net/one)——技術規格與文件
- [什麼是 Packet Injection？](/en/blog/packet-injection-guide/)——我們的封包注入基礎指南
- [AWUS036AXML WiFi 6E 評測](/en/blog/awus036axml-wifi-6e-review/)——旗艦網卡深度評測
- [ALFA 產品比較](/en/alfa_compare/)——所有 ALFA 型號的並列規格

---

*關於 Flipper One 與 ALFA 網卡相容性的售前諮詢，請聯絡 Yupitek 客服：support@yupitek.com 或致電 +886-2-87325338。*

---

## 參考來源

1. [Flipper One 官方部落格 — Pavel Zhovner 產品公告](https://blog.flipper.net/flipper-one-we-need-your-help/)
2. [Flipper One Developer Portal — 技術規格與文件](https://docs.flipper.net/one)
3. [Flipper Zero 官方網站](https://flipperzero.one/)
4. [aircrack-ng — 無線安全工具組官方網站](https://www.aircrack-ng.org/)
5. [ALFA Network 官方網站](https://www.alfa.com.tw/)
