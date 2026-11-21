---
title: "ALFA Network 無線網卡完整比較"
description: "ALFA Network 9 款 USB 無線網卡完整規格比較：晶片、Linux 驅動、Monitor／Injection／AP 能力，含 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17）實測結果。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

下表彙整 ALFA Network 9 款 USB 無線網卡的完整規格，Monitor、Injection、AP 與端到端 handshake 欄位均為 Yopitek 於 ASUS GX10（Ubuntu 24.04 LTS / ARM64 / kernel 6.17）自有設備與自有辦公室 Wi-Fi 的實測結果，非規格書推測。

## 完整規格比較

手機請左右滑動表格；點型號可前往產品頁。

| 型號 | Wi-Fi 世代 | 晶片 | 頻段 | 最高速率 | USB 介面 | 天線 | MIMO | Monitor 模式 | 封包注入 | 端到端 handshake（GX10 實測） | Linux 驅動 | 驅動類型 | AP 模式 | 最大功耗 | 藍牙 | 適合用途 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/zh-tw/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支援 | ❌ 原生 6.17 失敗 | ❌ 否（注入失敗） | 核心內建 ≥5.18 | 核心內建（免安裝） | ✅ Native | 3.6W | BT 5.2 | Wi-Fi 6E＋Linux＋USB-C |
| [AWUS036AXM](/zh-tw/products/alfa/awus036axm/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz（6 GHz 未測） | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支援 | ❌ 原生 6.17 失敗 | ❌ 否（注入失敗） | 核心內建 ≥5.18 | 核心內建（免安裝） | ✅ Native | 3.6W | BT 5.2 | Wi-Fi 6E＋雙天線 |
| [AWUS036AX](/zh-tw/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支援 | ✅ 支援 | ✅ 端到端（.22000） | 核心內建 ≥6.17 | 核心內建（免安裝） | ✅ Native | 3.6W | — | Wi-Fi 6＋AP 熱點 |
| [AWUS036AXER](/zh-tw/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | 內建（nano） | 2×2 MIMO | ✅ 支援 | ✅ 支援 | ✅ 端到端（.22000） | 核心內建 ≥6.17 | 核心內建（免安裝） | ✅ Native | 3.0W | — | 輕巧隨身型 |
| [AWUS036ACH](/zh-tw/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ 最佳 | ✅✅ 最佳 | ✅ 端到端（.22000） | 核心內建 ≥6.13 | 核心內建（免安裝） | ✅ Native | 3.6W | — | Kali Linux 首選 |
| [AWUS036ACM](/zh-tw/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支援 | ✅ 支援 | ✅ 端到端（.22000） | 核心內建 ≥4.19 | 核心內建（免安裝） | ✅ Native | 3.0W | — | Linux 免驅動 |
| [AWUS036ACHM](/zh-tw/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ 支援 | ✅ 2.4 GHz／⚠️ 5 GHz 僅廣播 | ✅ 端到端（.22000） | 核心內建 ≥4.19 | 核心內建（免安裝） | ✅ Native | — | — | 輕巧 AC600，Linux 免驅動 |
| [AWUS036ACS](/zh-tw/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ 支援 | ✅ 支援 | ✅ 端到端（.22000） | 核心內建 ≥6.13 | 核心內建（免安裝） | ✅ Native (5 GHz tested as 802.11a 20 MHz; VHT80 not tested) | 2.5W | — | 平價資安測試 |
| [AWUS036EACS](/zh-tw/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | 內建 2dBi | 1×1 SISO | ✅ 支援 | ✅✅ 最佳 | ✅ 端到端（.22000） | 核心內建 ≥6.2 | 核心內建（免安裝） | ✅ Native (5 GHz tested as 802.11a 20 MHz; VHT80 not tested) | 2.5W | BT 4.2 | Windows 家用 Wi-Fi＋藍牙 |

## 依用途快速選型

**🔴 Kali Linux / Pentesting** — 推薦: AWUS036ACH

RTL8812AU — most mature monitor mode & packet injection on Kali; 100% injection on both bands on GX10 (kernel 6.17). In-kernel rtw88_8812au since 6.13. Tip: On older kernels, use the aircrack-ng DKMS driver pinned to stable commit 63cf0b4.

**🔵 WiFi 6E (Tri-Band) Power User** — 推薦: AWUS036AXML or AWUS036AXM

MT7921AUN — in-kernel Linux driver since 5.18, 6 GHz band (verified on AXML; AXM untested), Bluetooth 5.2. Note: packet injection fails on stock kernel 6.17 (mac80211 regression since 6.16), so not for pentesting. Form factors: AXML has a detachable USB-C connector and a single-antenna body with dual outputs; AXM has a built-in L-shaped USB-A format.

**🌐 Soft-AP / Hotspot Emulation** — 推薦: AWUS036ACM

MT7612U — plug-and-play AP mode support via native hostapd in Linux kernel. Unlike Realtek adapters which require problematic custom hostapd builds, MediaTek is seamless and stable for Rogue AP / Evil Twin simulation.

**🟢 Linux Daily Driver (Plug & Play)** — 推薦: AWUS036ACM

MT7612U — in-kernel since kernel 4.19, zero driver setup on Ubuntu / Debian / Fedora. Most hassle-free Linux experience.

**🟣 Raspberry Pi / Embedded** — 推薦: AWUS036ACM

Low power consumption + in-kernel driver makes it ideal for Raspberry Pi. Note: High-power models (ACH, AXML) will draw up to 3.6W and require a powered USB hub to prevent voltage drops and connection resets on Pi.

**🟡 Budget / Beginner Security** — 推薦: AWUS036ACS

RTL8811AU — affordable entry point with monitor mode and packet injection support. Single antenna, compact design.

**⚡ Compact Travel Adapter** — 推薦: AWUS036AXER

Ultra-thin nano body at only 10.5g. WiFi 6 (1800 Mbps), USB-A. Great for business travel, Windows-focused.

**🏠 Windows Home User + Bluetooth** — 推薦: AWUS036EACS

RTL8821CU — dual-mode WiFi 5 + Bluetooth 4.2 combo. Nano form factor. Best for desktops needing quick wireless + BT without PCIe slot.

**🍎 macOS Compatibility** — 推薦: AWUS036ACH or AWUS036AXML

ACH has good macOS support via third-party driver. AXML's MT7921AUN has community macOS support. Always verify macOS version compatibility. Intel Macs have better driver legacy support than M-series.

## 依平台／作業系統快速選型

| 平台／作業系統 | 首選 | 次選 | 說明 |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = best monitor mode; ACM = easiest kernel support. For VMs: Configure VM to use USB 3.0 (xHCI) controller to prevent drops. |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U in-kernel since 4.19; MT7921AUN since 5.18 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | Low power + in-kernel driver; no manual compile needed. Recommends powered USB hub for high-power cards to avoid resets. |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | WiFi 6 performance; EACS adds Bluetooth combo |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | Third-party drivers available; verify macOS version. Intel Macs have legacy drivers; Apple Silicon (M1/M2/M3) has restricted experimental support. |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU & RTL8811AU have NetHunter support; OTG adapter & custom kernel compilation required. |

---

實測平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia（2026-11）。完整逐卡報告請見[部落格](/zh-tw/blog/)。
