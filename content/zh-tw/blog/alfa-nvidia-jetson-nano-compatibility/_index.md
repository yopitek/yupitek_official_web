---
title: "ALFA 無線網卡是否支援 NVIDIA Jetson Nano"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "邊緣 AI / 單板電腦"
description: "Jetson Nano 可使用多數 ALFA 網卡，但關鍵限制在於 JetPack 4.x 的 Linux kernel 4.9 版本較舊（判定母體：ALFA 現役 9 款 USB 網卡，其中 3 款成熟可用、2 款需進階編譯、2 款未驗證、2 款不可用）。Realtek 晶片機型（AWUS036ACH / ACS / EACS）可直接編譯 out-of-tree 驅動，是 Jetson N..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網卡能否在 NVIDIA Jetson Nano 開發板上使用？」

簡短結論：Jetson Nano 可使用多數 ALFA 網卡，但關鍵限制在於 JetPack 4.x 的 Linux kernel 4.9 版本較舊（判定母體：ALFA 現役 9 款 USB 網卡，其中 3 款成熟可用、2 款需進階編譯、2 款未驗證、2 款不可用）。Realtek 晶片機型（AWUS036ACH / ACS / EACS）可直接編譯 out-of-tree 驅動，是 Jetson Nano 上的實用選擇；MediaTek MT7612U / MT7610U 需 backport 或自行編譯 mt76 驅動；Wi-Fi 6E 的 MT7921AUN 機型（AWUS036AXML / AXM）因需要 kernel 5.19+，在 Jetson Nano 上實際不可用。滲透測試場景首選 AWUS036ACH（RTL8812AU），一般上網場景首選 AWUS036ACH（穩定）或 AWUS036ACM（需編譯 mt76）。

## 2. 分析目標硬體規格架構

### 2.1 NVIDIA Jetson Nano 硬體規格

| 項目 | 規格 |
|---|---|
| 模組 | Jetson Nano 模組（P3448） |
| CPU | Quad-core ARM Cortex-A57（ARMv8-A / aarch64） |
| GPU | NVIDIA Maxwell 架構，128 CUDA 核心 |
| 記憶體 | 4GB LPDDR4（64-bit，25.6 GB/s） |
| 儲存 | microSD（開發板）/ eMMC（生產版模組） |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B（Device Mode / 供電） |
| 網路 | 1x Gigabit Ethernet（RJ45） |
| 無線 | 無內建 WiFi / 藍牙（需外接 USB 或 M.2 擴充） |
| 供電 | 5V/4A DC 接頭（建議）或 micro-USB 5V/2A |
| 尺寸 | 100mm × 80mm（開發板） |

### 2.2 軟體環境：JetPack 4.x

| 項目 | 內容 |
|---|---|
| 作業系統 | Linux for Tegra（L4T），基於 Ubuntu 18.04 LTS |
| Kernel 版本 | Linux 4.9（L4T R32.x / JetPack 4.6.x） |
| 架構 | aarch64（ARM64） |
| 編譯器 | GCC 7.5（預設）/ GCC 8（可安裝） |
| 最新版本 | JetPack 4.6.4（L4T R32.7.4），已進入維護模式 |
| 後續升級 | Jetson Nano 不支援 JetPack 5.x（kernel 5.10），因硬體限制 |

### 2.3 關鍵限制：Kernel 4.9

Jetson Nano 的 kernel 4.9 是相容性判定的核心變數：

| 驅動 | 進入 mainline 的 kernel 版本 | Jetson Nano（kernel 4.9）可用性 |
|---|---|---|
| mt76x2u（MT7612U） | 4.19 | ❌ 需 backport / 自行編譯 |
| mt76x0u（MT7610U） | 4.19 | ❌ 需 backport / 自行編譯 |
| mt7921u（MT7921AUN） | 5.19 | ❌ 無法實用（差距過大） |
| rtl8812au（RTL8812AU） | 從未進入 mainline | ✅ 可編譯 out-of-tree 驅動 |
| rtl8821cu（RTL8811CU） | 從未進入 mainline | ✅ 可編譯 out-of-tree 驅動 |
| rtw89（RTL8832BU） | 5.16（PCIe）/ USB 陸續合入 | ❌ 需自行編譯，相容性未知 |

### 2.4 USB 供電限制

Jetson Nano 開發板的 4 個 USB 3.0 Type-A 埠共用電源預算：

- 使用 DC 供電（5V/4A）時，USB 埠總輸出約 1.5A（5V）
- 使用 micro-USB 供電（5V/2A）時，USB 埠總輸出僅約 0.5A
- ALFA 高功率網卡（AWUS036ACH）峰值可達 800mA-1A
- 建議：使用 DC 供電 + 有電源的 USB 3.0 Hub，避免供電不足導致斷線或系統重啟

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網卡產品線如下：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | Jetson Nano 適用性 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ 需 kernel 5.19+，不可用 |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ 同上 |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 需自編 rtl8852bu，未驗證 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ 編譯 morrownr/8812au，成熟 |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ⚠️ 需 backport mt76x0u |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ⚠️ 需 backport mt76x2u |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ✅ 由 8812au 驅動涵蓋 |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ✅ 編譯 morrownr/8821cu |

## 4. 適用機型與晶片組

### 4.1 推薦等級分類

| 推薦等級 | 機型（晶片組） | 說明 |
|---|---|---|
| ⭐ 強烈推薦（滲透測試） | AWUS036ACH（RTL8812AU） | 驅動成熟，支援 Monitor Mode + Packet Injection，Jetson Nano 上最常被使用的 ALFA 網卡 |
| ✅ 推薦（一般上網） | AWUS036ACH（RTL8812AU） | 雙頻 AC1200，驅動安裝簡單，穩定 |
| ✅ 推薦（低功耗） | AWUS036EACS（RTL8811CU） | AC600 雙頻，USB 2.0 低功耗，適合簡單上網 |
| ✅ 推薦（入門） | AWUS036ACS（RTL8811AU） | AC433 雙頻，由 8812au 驅動涵蓋 |
| ⚠️ 可用但需手動編譯 | AWUS036ACM（MT7612U） | 需 backport mt76 驅動到 kernel 4.9，技術門檻較高 |
| ⚠️ 可用但需手動編譯 | AWUS036ACHM（MT7610U） | 同上，僅 433Mbps |
| ⚠️ 未驗證 / 不建議 | AWUS036AX / AXER（RTL8832BU） | Wi-Fi 6，需編譯 rtl8852bu，kernel 4.9 相容性未驗證 |
| ❌ 不可用 | AWUS036AXML / AXM（MT7921AUN） | Wi-Fi 6E，需 kernel 5.19+，Jetson Nano 無法升級 |

### 4.2 使用場景建議

| 使用場景 | 建議機型 | 說明 |
|---|---|---|
| 無線滲透測試 / 監聽 / 注入 | AWUS036ACH | RTL8812AU 驅動支援 Monitor + Injection，社群驗證充分 |
| 機器人 / 無人機無線控制 | AWUS036ACH 或 AWUS036EACS | 穩定連線，低延遲 |
| 一般 IoT 閘道上網 | AWUS036EACS / ACS | 低功耗，USB 2.0 即可，省電 |
| 需要 5GHz 高速上網 | AWUS036ACH | AC1200，5GHz 867Mbps |
| Wi-Fi 6 / 6E 需求 | ❌ 無可用選項 | Jetson Nano 不支援現代 Wi-Fi 6/6E 晶片 |

## 5. 環境需求

### 5.1 硬體需求

| 項目 | 最低需求 | 建議 |
|---|---|---|
| Jetson Nano 開發板 | B01 / A02 版本均可 | B01（2 條 CSI 攝影機埠） |
| 供電方式 | 5V/2A micro-USB | 5V/4A DC 接頭（USB 設備多時必須） |
| USB Hub | 可不用 | 有電源的 USB 3.0 Hub（使用高功率網卡時） |
| 散熱 | 散熱片（預設附帶） | 風扇 + 散熱片（長時間高負載時） |
| 儲存 | 16GB microSD | 32GB+ UHS-I microSD（編譯驅動需要空間） |

### 5.2 軟體需求

| 項目 | 需求 |
|---|---|
| JetPack 版本 | 4.6.x（L4T R32.7.x） |
| 核心工具 | build-essential、git、bc、libssl-dev、flex、bison |
| Kernel 原始碼 | 需要下載對應 L4T 版本的 kernel source（編譯 mt76 backport 時） |
| 網路 | 編譯期間需有線網路連線（透過 Gigabit Ethernet 埠） |

## 6. 相容性判定

### ALFA 現役機型 × NVIDIA Jetson Nano 相容性矩陣

| 機型 | 晶片組 | 驅動方式 | USB 偵測 | STA 上網 | AP 模式 | Monitor | 安裝難度 | 綜合評價 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 編譯 8812au | ✅ | ✅ | ✅ | ✅ | 中 | ⭐ 最佳 |
| AWUS036ACS | RTL8811AU | 8812au 涵蓋 | ✅ | ✅ | ⚠️ | ❌ | 中 | ✅ 良好 |
| AWUS036EACS | RTL8811CU | 編譯 8821cu | ✅ | ⚠️ | ❌ | ❌ | 中 | ✅ 良好 |
| AWUS036ACM | MT7612U | backport mt76x2u | ✅ | ✅ | ✅ | ✅ | 高 | ⚠️ 可用 |
| AWUS036ACHM | MT7610U | backport mt76x0u | ✅ | ✅ | ⚠️ | ⚠️ | 高 | ⚠️ 可用 |
| AWUS036AX | RTL8832BU | 編譯 rtl8852bu | ⚠️ | ❌ | ❌ | ❌ | 高 | ❌ 不建議 |
| AWUS036AXER | RTL8832BU | 同上 | ⚠️ | ❌ | ❌ | ❌ | 高 | ❌ 不建議 |
| AWUS036AXML | MT7921AUN | 需 kernel 5.19+ | ❌ | ❌ | ❌ | ❌ | — | ❌ 不可用 |
| AWUS036AXM | MT7921AUN | 同上 | ❌ | ❌ | ❌ | ❌ | — | ❌ 不可用 |

判定依據：Jetson Nano JetPack 4.x kernel 4.9 的驅動可用性 + 社群實測回報（Jetson Nano 論壇、GitHub morrownr 驅動 issue）。MT7921AUN 因 Jetson Nano 無法升級至 kernel 5.19+，判定為不可用。

## 7. 超詳細 Step by Step 設定步驟

### 7.1 前置作業：系統更新與編譯環境

**步驟 1：開機並透過 SSH 登入 Jetson Nano**

```bash
ssh username@<jetson-nano-ip>
```

**步驟 2：更新系統套件**

```bash
sudo apt update
sudo apt upgrade -y
```

**步驟 3：安裝編譯工具與依賴**

```bash
sudo apt install -y build-essential git bc libssl-dev flex bison dkms
```

**步驟 4：確認 kernel 版本**

```bash
uname -r
# 預期輸出：4.9.337-tegra（或類似 4.9.x-tegra）
```

### 7.2 路徑 A：Realtek 晶片機型（AWUS036ACH / ACS / EACS）— 推薦

以 AWUS036ACH（RTL8812AU）為例：

**步驟 1：下載驅動原始碼**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**步驟 2：（可選）調整編譯參數 for ARM64**

編輯 Makefile，確認以下設定：

```
CONFIG_PLATFORM_ARM64 = y
```

（多數新版本 Makefile 已自動偵測 aarch64）

**步驟 3：編譯與安裝**

```bash
make
sudo make install
```

**步驟 4：載入驅動模組**

```bash
sudo modprobe 8812au
# 或重新開機
sudo reboot
```

**步驟 5：插入 ALFA 網卡，確認網路介面**

```bash
ip link show
# 預期出現 wlan0 介面
# 若無，檢查 dmesg
dmesg | grep -i "8812au\|rtl8812\|usb"
```

**步驟 6：掃描 WiFi 網路（驗證功能）**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**步驟 7：連線到 WiFi 網路（使用 NetworkManager / nmcli）**

```bash
# Jetson Nano 預設安裝 NetworkManager
nmcli dev wifi list
nmcli dev wifi connect "你的WiFi名稱" password "你的WiFi密碼"
```

**步驟 8：（可選）設定為 AP 熱點模式**

```bash
# 安裝 hostapd 與 dnsmasq
sudo apt install -y hostapd dnsmasq
# 參考 ALFA Soft AP 指南進行設定
# https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/
```

**步驟 9：啟用監聽模式（滲透測試用）**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# 驗證
sudo iw dev wlan0 info
# type 應顯示 monitor
# 測試封包注入
sudo aireplay-ng --test wlan0
```

### 7.3 路徑 B：MediaTek 晶片機型（AWUS036ACM / ACHM）— 進階

以 AWUS036ACM（MT7612U）為例，需 backport mt76 驅動：

**步驟 1：下載 Jetson Nano kernel 原始碼**

```bash
# 根據 L4T 版本下載對應 kernel source
# 例如 L4T R32.7.4：
wget https://developer.nvidia.com/embedded/l4t/r32_release_v7.4/sources/public_sources.tbz2
tar -xjf public_sources.tbz2
cd Linux_for_Tegra/source/public
tar -xjf kernel_src.tbz2
```

**步驟 2：準備 kernel 編譯環境**

```bash
cd kernel/kernel-4.9
# 產生預設設定
make tegra_defconfig
# 啟用 mt76 相關選項（menuconfig）
make menuconfig
# 導航到：Device Drivers > Network device support > Wireless LAN
# 選取：<M> MediaTek MT76x2U USB support
# 選取：<M> MediaTek MT76x0U USB support
```

**步驟 3：編譯 kernel modules**

```bash
make modules_prepare
make M=drivers/net/wireless/mediatek/mt76 modules
```

**步驟 4：安裝模組**

```bash
sudo make M=drivers/net/wireless/mediatek/mt76 modules_install
sudo depmod -a
```

**步驟 5：載入驅動**

```bash
sudo modprobe mt76x2u
# 插入 AWUS036ACM
dmesg | grep mt76
ip link show
```

⚠️ 注意：backport mt76 到 kernel 4.9 可能遇到編譯錯誤，需要手動修補原始碼。這是進階操作，建議僅對 kernel 編譯有經驗的使用者嘗試。若遇到困難，建議改用 AWUS036ACH（RTL8812AU）。

### 7.4 路徑 C：Wi-Fi 6 / 6E 機型（AWUS036AX / AXER / AXML / AXM）

- AWUS036AXML / AXM（MT7921AUN）：不可用。Jetson Nano 的 kernel 4.9 無法升級至 5.19+，mt7921u 驅動無法 backport（差距過大，依賴現代 kernel 基礎設施）。
- AWUS036AX / AXER（RTL8832BU）：不建議。理論上可嘗試編譯 morrownr/rtl8852bu 驅動，但 kernel 4.9 相容性未經社群驗證，且 Wi-Fi 6 功能可能無法正常運作。若需要 Wi-Fi 6，建議使用 Jetson Orin Nano（JetPack 5.x，kernel 5.10+）或 x86 電腦。

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| 插入網卡後 dmesg 無任何反應 | USB 供電不足 / 接觸不良 |使用 DC 供電（5V/4A）；更換 USB 埠；使用有電源 USB Hub |
| make 編譯 8812au 時報錯 gcc: error: unrecognized command line option | GCC 版本過舊 | 安裝 GCC 8：`sudo apt install gcc-8 g++-8`，並在 Makefile 中指定 `CC = gcc-8` |
| modprobe 8812au 報 Required key not available | Secure Boot 啟用（Jetson Nano 通常無此問題） | 確認 Jetson Nano 未啟用 Secure Boot；重新簽章模組或關閉 Secure Boot |
| wlan0 介面出現但無法掃描 AP | Regulatory Domain 未設定 / 驅動韌體缺失 | 設定法規區域：`sudo iw reg set TW`；檢查 dmesg 是否有 firmware 載入錯誤 |
| 高功率輸出時系統重啟或網卡斷線 | USB 供電不足 | 使用 DC 供電 + 有電源 USB Hub；降低 TX Power：`sudo iw dev wlan0 set txpower fixed 2000` |
| 監聽模式下 aireplay-ng --test 顯示 Injection is working! 但實際攻擊無效 | 驅動注入功能有限 / 通道衝突 | RTL8812AU 注入功能基本可用；確認 `airmon-ng check kill` 已停止 NetworkManager；嘗試不同通道 |
| mt76 backport 編譯失敗 | kernel 4.9 與現代 mt76 原始碼差距過大 | 嘗試使用較舊版本的 mt76（對應 kernel 4.19 時期的 commit）；或改用 AWUS036ACH |
| 系統喚醒後網卡消失 | USB 省電設定 | 停用 USB 自動暫停：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |
| AWUS036ACH 的 5GHz 無法使用 | 法規區域限制 / 驅動通道表 | 設定 `sudo iw reg set US`（美國法規開放較多 5GHz 通道）；確認使用的通道在當地法規允許範圍 |

## 9. 已知限制

- Kernel 版本凍結在 4.9：Jetson Nano 不支援 JetPack 5.x，無法升級 kernel，這是所有相容性問題的根源
- MT7921AUN（Wi-Fi 6E）完全不可用：需要 kernel 5.19+，無法 backport 到 4.9
- MediaTek mt76 晶片需手動 backport：AWUS036ACM / ACHM 的使用者需自行編譯 kernel module，技術門檻高
- ⚠️ **Wi-Fi 6（RTL8832BU）驅動維護者已公開建議避免使用**：驅動維護者 morrownr 在其官方公告中明確指出 rtl8852/32au 系列「是很糟糕的驅動，懷疑晶片本身有問題」，並建議 Linux 使用者現階段避開此晶片（來源見第 10 節）。這比單純「kernel 4.9 相容性未驗證」更嚴重，本文與其他相關文件對 AWUS036AX / AXER 的判定應理解為「不建議」而非「可嘗試但較麻煩」
- USB 供電限制：4 個 USB 埠共用約 1.5A（DC 供電時），高功率網卡需使用有電源 Hub
- AP 模式效能：Jetson Nano 的 CPU 效能有限，USB WiFi 做 AP 時吞吐量可能低於預期
- 監聽 / 注入功能差異：RTL8812AU 支援最佳；MediaTek 晶片在 kernel 4.9 backport 後的注入功能可能不穩定
- Long-term 維護：JetPack 4.x 已進入維護模式，未來不會有新功能或驅動更新
- 藍牙功能：AWUS036AXM 的藍牙 5.2 功能在 Jetson Nano 上未驗證（需 BlueZ 支援）
- 散熱：長時間使用 USB WiFi 高功率輸出時，Jetson Nano 的整體溫度可能升高，建議加裝風扇

反駁條件：以上判定以 JetPack 4.6.x（kernel 4.9）為前提。若 NVIDIA 未來為 Jetson Nano 釋出 JetPack 5.x 支援（目前官方明確不支持），或社群出現穩定的 kernel 5.x backport，第 4 節的不可用判定需重新驗證。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| NVIDIA Jetson Nano 官方頁面 | Jetson Nano 硬體規格 | https://developer.nvidia.com/embedded/jetson-nano | ✅ 已查核 | 2026-09-03 |
| NVIDIA JetPack SDK 官方頁 | JetPack 版本與 kernel 資訊 | https://developer.nvidia.com/embedded/jetpack | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動（Jetson Nano 適用） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux 驅動 | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | ALFA 在 Linux 上的 AP 模式設定指南 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA Network 產品總覽（Yupitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驅動維護者官方聲明：建議避開 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko 需 kernel 5.19+ 才會出現於核心（驅動維護者原話） | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)（GB10 平台對照，kernel 6.x 環境）｜[ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

免責聲明：本文相容性判定以 Jetson Nano JetPack 4.6.x（kernel 4.9）為基準。Realtek 晶片驅動為社群維護（morrownr），實際穩定性可能隨版本變化。MediaTek mt76 晶片的 backport 操作需要 kernel 編譯經驗，不保證 100% 成功。若需要 Wi-Fi 6/6E 或現代 kernel 支援，建議升級至 Jetson Orin 系列（JetPack 5.x+）或使用 x86 電腦。
