---
title: "完整教學：在中國大陸 Linux 系統安裝所有 Alfa USB WiFi 網路卡 — Kali、Ubuntu、Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "驅動程式", "中國", "監控模式", "封包注入", "無線網路"]
categories: ["驅動程式安裝教學"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "終極 Alfa USB WiFi 網路卡 Linux 安裝指南，適用於中國大陸使用者。涵蓋 Kali Linux、Ubuntu 22/24、Debian、Raspberry Pi，系統套件使用境內鏡射站，驅動原始碼取自已驗證的 GitHub 儲存庫。"
featureimage: "/images/blog/alfa-china-install-complete-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "在中國安裝 Alfa WiFi 網路卡需要翻牆嗎？"
    answer: "不一定。系統套件使用國內鏡射站（中科大、阿里雲、清華等）安裝；未內建於核心的驅動則從 morrownr 已驗證的 GitHub 儲存庫複製原始碼。若 GitHub 速度較慢，請使用你信任的代理或鏡射站。"
  - question: "哪款 Alfa 網路卡最適合監聽模式和封包注入？"
    answer: "AWUS036ACM 搭載 MT7612U 晶片，驅動核心內建且完整支援 VIF，是最佳選擇。"
  - question: "哪款 Alfa 網路卡支援 WiFi 6？"
    answer: "AWUS036AX 和 AWUS036AXER 採用 RTL8832BU 晶片支援 WiFi 6，Ubuntu 24.04 免驅即用。"
  - question: "哪款 Alfa 網路卡支援 WiFi 6E？"
    answer: "AWUS036AXM 和 AWUS036AXML 採用 MT7921AUN 晶片支援 WiFi 6E 三頻段。"
  - question: "樹莓派上使用 Alfa 網路卡需要注意什麼？"
    answer: "務必搭配外接供電 USB Hub 供電，並刷 Kali ARM64 版本以獲得最佳驅動支援。"
---

本指南涵蓋在中國大陸所有主要 Linux 發行版上安裝每一款 Alfa USB WiFi 網路卡的完整步驟，系統套件使用國內鏡射站，驅動原始碼取自已驗證的 GitHub 儲存庫。

{{< tldr >}}
中國大陸 Alfa WiFi 網路卡 Linux 安裝終極指南，涵蓋 Kali、Ubuntu、Debian、樹莓派，支援 RTL8812AU、MT7612U、RTL8832BU 等所有晶片，全程國內鏡射站免翻牆。
{{< /tldr >}}

## 歡迎閱讀 Alfa Linux 終極安裝指南

如果您正在閱讀本文，您可能購買了 Alfa USB WiFi 網路卡後遇到了以下問題：

- 您在中國大陸，無法訪問 GitHub
- 驅動程式安裝步驟複雜難懂
- 您需要啟用監控模式（Monitor Mode）和封包注入（Packet Injection）進行無線測試
- 不確定您的 Alfa 型號需要哪個驅動程式

本指南解決**所有上述問題**。我們將帶您在**所有主要 Linux 發行版**上安裝**每一款 Alfa USB WiFi 網路卡**，系統套件使用**中國大陸可訪問的鏡射站**，驅動原始碼取自已驗證的 GitHub 儲存庫。告別挫折感。

---

## 為什麼需要這份指南

Alfa USB WiFi 網路卡深受滲透測試員、網路工程師和無線愛好者的歡迎，因為它們支援監控模式和封包注入——這些功能是大多數消費級 WiFi 網路卡所沒有的。

但問題在於：**大多數驅動程式安裝教學都假設您能順暢訪問 GitHub**。在中國大陸，GitHub 可能較慢或不穩定。本指南使用國內鏡射站安裝系統套件，並從已驗證的 GitHub 儲存庫複製驅動原始碼；若 GitHub 速度較慢，請使用您信任的代理或鏡射站。

---

## 快速型號對照表

開始之前，先確認您使用的 Alfa 網路卡型號及其晶片組：

### AX 系列（Wi-Fi 6 / 802.11ax）

| 型號 | 晶片組 | 驅動程式 | 最適合 |
|------|--------|---------|--------|
| AWUS036AX | Realtek RTL8832BU | `8852bu` | 通用，覆蓋範圍好 |
| AWUS036AXM | MediaTek MT7921AUN | `mt7921u` | 緊湊設計 |
| AWUS036AXML | MediaTek MT7921AUN | `mt7921u` | 超緊湊 |
| AWUS036AXER | Realtek RTL8832BU | `8852bu` | 增強功率 |

### AC 系列（Wi-Fi 5 / 802.11ac）

| 型號 | 晶片組 | 驅動程式 | 最適合 |
|------|--------|---------|--------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | 高功率，覆蓋範圍極佳 |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **最佳 VIF 支援**，即插即用 |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | 經濟實惠 |

### 如何確認您的型號？

1. 查看網路卡上的標籤
2. 查看原包裝盒
3. 若是網購，查看訂單記錄

確認型號後，直接跳至對應章節，或依照通用流程操作。

---

## 開始前的準備

請確保以下物品就緒：

1. **Alfa USB WiFi 網路卡** — 適合您需求的型號
2. **USB 連接線** — 原廠附送的即可
3. **外接供電 USB Hub** — 若使用 Raspberry Pi 則必備
4. **可用的網路連線** — 用於連接中國大陸境內鏡射站
5. **sudo 權限** — 安裝驅動程式需要管理員權限

先插入網路卡，確認系統能偵測到：

```bash
lsusb
```

在輸出中尋找網路卡的廠商 ID：

- **Alfa 網路卡**顯示為 `0e8d`（MediaTek）或 `0bda`（Realtek）
- 範例：`Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- 範例：`Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

若看到 ID，代表網路卡已被偵測到，請繼續前往驅動程式安裝章節。

若未看到，請換一個 USB 埠，更換連接線，再次執行 `lsusb`。

---

## 選擇您的作業系統

直接跳至對應章節：

- [Kali Linux](#kali-linux-安裝)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-安裝)
- [Debian 12 (Bookworm)](#debian-12-bookworm-安裝)
- [Raspberry Pi OS（64 位元）](#raspberry-pi-os-安裝)

已安裝驅動程式？直接跳至進階章節：

- [啟用監控模式](#在任何網路卡上啟用監控模式)
- [測試封包注入](#測試封包注入)
- [虛擬介面（VIF）支援](#虛擬介面-vif-支援)
- [虛擬機 USB 直通](#虛擬機-usb-直通)

---

## 中國大陸可用鏡射站參考

本指南所有步驟僅使用以下中國大陸可訪問的鏡射站：

| 資源 | URL | 用途 |
|------|-----|------|
| **Alfa 官方下載** | [files.alfa.com.tw](https://files.alfa.com.tw) | 驅動程式套件、韌體 |
| **Alfa 文件** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 產品手冊（英文）|
| **清華大學鏡射站** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里雲鏡射站** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推薦）|
| **中科大鏡射站** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推薦）|
| **華為雲鏡射站** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 映像（備用）|
| **GitHub (morrownr)** | [github.com/morrownr](https://github.com/morrownr) | 驅動程式原始碼 |

---

## Kali Linux 安裝

Kali Linux 已預裝無線工具，讓 Alfa 網路卡運作只需幾個步驟。

### 第一步：切換至中國大陸鏡射站

開啟軟體源清單：

```bash
sudo nano /etc/apt/sources.list
```

將所有內容替換為：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

儲存：**Ctrl+O**，Enter，再 **Ctrl+X**。更新：

```bash
sudo apt update
```

> **備用鏡射站：** 若中科大（USTC）速度慢，改用清華（Tsinghua）：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### 第二步：依晶片組安裝驅動程式

#### AX 系列（RTL8832BU）

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
```

#### AC 系列 - Realtek（RTL8812AU / RTL8811AU）

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC 系列 - MediaTek（MT7612U）

MT7612U 驅動程式已內建於 Kali 核心，確認是否已載入：

```bash
lsmod | grep mt76
```

若看到 `mt76x2u`，已完成。若未出現：

```bash
sudo modprobe mt76x2u
```

### 第三步：確認驅動程式已載入

再次執行 `lsusb`，網路卡應會顯示。然後檢查無線介面：

```bash
iwconfig
```

尋找 `wlan0` 或 `wlan1`。若介面出現，代表驅動程式正常運作。

### 第四步：啟用監控模式

停止干擾程式：

```bash
sudo airmon-ng check kill
```

啟動監控模式：

```bash
sudo airmon-ng start wlan0
```

驗證：

```bash
iwconfig
```

尋找顯示 `Mode:Monitor` 的 `wlan0mon`，完成！

---

## Ubuntu 22.04 / 24.04 安裝

### 第一步：切換至中國大陸鏡射站

#### Ubuntu 24.04（Noble）

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

替換為：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

**Ctrl+O** 儲存，**Ctrl+X** 離開。

#### Ubuntu 22.04（Jammy）

```bash
sudo nano /etc/apt/sources.list
```

替換為：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

儲存並離開。

#### 更新套件索引

```bash
sudo apt update
```

### 第二步：安裝編譯依賴

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 第三步：安裝驅動程式

#### AX 系列（RTL8832BU）

從 GitHub 克隆：

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo modprobe 8852bu
```

#### AC 系列 - Realtek（RTL8812AU）

從 GitHub 克隆：

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
sudo modprobe 8812au
```

#### AC 系列 - MediaTek（MT7612U）

驅動程式已內建於 Ubuntu 核心，直接載入：

```bash
sudo modprobe mt76x2u
```

### 第四步：啟用監控模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

尋找顯示 `Mode:Monitor` 的 `wlan0mon`。

---

## Debian 12 (Bookworm) 安裝

### 第一步：切換至中國大陸鏡射站

```bash
sudo nano /etc/apt/sources.list
```

替換為：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

儲存並離開，更新：

```bash
sudo apt update
```

### 第二步：安裝非自由韌體

```bash
sudo apt install -y firmware-misc-nonfree
```

### 第三步：安裝編譯依賴

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 第四步：安裝驅動程式

#### AX 系列（RTL8832BU）

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo modprobe 8852bu
```

#### AC 系列 - Realtek（RTL8812AU）

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
sudo modprobe 8812au
```

#### AC 系列 - MediaTek（MT7612U）

```bash
sudo modprobe mt76x2u
```

### 第五步：安裝 Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### 第六步：啟用監控模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

尋找顯示 `Mode:Monitor` 的 `wlan0mon`。

---

## Raspberry Pi OS 安裝

> **重要提示：** AWUS036ACH 消耗約 500mW，AWUS036ACM 消耗約 400mW。**務必使用外接供電 USB Hub** 以防止 Pi 在負載下降頻或當機。

### 第一步：下載 Kali Linux ARM64 映像

前往：https://www.kali.org/get-kali/#kali-arm

選擇 **Raspberry Pi 4（64 位元）** 或 **Raspberry Pi 5（64 位元）**。請勿使用 32 位元版本。

> **中國大陸鏡射站：** 若 kali.org 速度慢，使用華為雲：https://repo.huaweicloud.com/kali-images/

### 第二步：燒錄至 MicroSD

確認 SD 卡的裝置路徑：

```bash
lsblk
```

燒錄映像（將 `/dev/sdX` 替換為您的實際路徑）：

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

等待 `sync` 完成。啟動 Pi，預設帳號密碼：**kali / kali**。

### 第三步：切換至中國大陸鏡射站

```bash
sudo nano /etc/apt/sources.list
```

替換為：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

儲存並套用：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 第四步：安裝驅動程式

#### AX 系列（RTL8832BU）

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
```

#### AC 系列 - Realtek（RTL8812AU）

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC 系列 - MediaTek（MT7612U）

```bash
sudo modprobe mt76x2u
```

### 第五步：啟用監控模式

Pi 有內建 Wi-Fi，Alfa 網路卡通常顯示為 `wlan1`：

```bash
iwconfig
```

然後：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

尋找顯示 `Mode:Monitor` 的 `wlan1mon`。

---

## 在任何網路卡上啟用監控模式

驅動程式安裝完成後，啟用監控模式非常簡單：

### 第一步：確認介面名稱

```bash
iwconfig
```

記下是 `wlan0` 還是 `wlan1`。

### 第二步：停止干擾程式

```bash
sudo airmon-ng check kill
```

### 第三步：啟動監控模式

```bash
sudo airmon-ng start wlan0
```

若介面名稱不同，請替換 `wlan0`。

### 第四步：驗證

```bash
iwconfig
```

尋找介面名稱末尾加上 `mon`（如 `wlan0mon`）且顯示 `Mode:Monitor`。

---

## 測試封包注入

確認網路卡可以發送自訂封包——無線測試的必備功能。

```bash
sudo aireplay-ng --test wlan0mon
```

**成功的輸出如下：**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**若失敗：**
- 重新啟動後再試
- 確認沒有其他程式佔用介面（`iwconfig`）
- 靠近 WiFi AP 進行測試
- 確認使用的是 `wlan0mon` 而非 `wlan0`

---

## 虛擬介面（VIF）支援

VIF（虛擬介面功能）允許在單一網路卡上同時執行多個介面，例如：

- 同時執行**受管模式**（`wlan0`）和**監控模式**（`mon0`）
- 在保持網路連接的同時捕獲流量

### 哪些網路卡支援 VIF？

| 晶片組 | VIF 支援 | 備註 |
|--------|---------|------|
| **MT7612U（AWUS036ACM）** | ✅ 完整原生支援 | VIF 工作流程的最佳選擇 |
| **RTL8812AU（AWUS036ACH）** | ⚠️ 有限 | 無法同時執行受管模式和監控模式 |
| **RTL8832BU（AX 系列）** | ⚠️ 有限 | 請查閱特定型號文件 |

### 建立虛擬介面（MT7612U）

若您使用 AWUS036ACM（MT7612U）：

```bash
# 在 wlan0 保持受管模式的同時建立監控介面
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

確認兩個介面均已啟用：

```bash
iwconfig
```

您應看到：
- `wlan0` — 受管模式（已連接至 AP）
- `mon0` — 監控模式（捕獲所有流量）

### 使用場景

**保持連接的同時捕獲流量：**

```bash
sudo airodump-ng mon0
```

`wlan0` 繼續正常運作，`mon0` 同時捕獲所有流量。

**假冒 AP + 監控：**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 虛擬機 USB 直通

在虛擬機中執行 Linux？您需要將 USB 網路卡直通到虛擬機內部。

### VirtualBox

1. 關閉虛擬機
2. 進入 **設定 → USB**
3. 啟用 **USB 3.0（xHCI）控制器**
4. 點擊 **+** 新增 USB 篩選器
5. 選擇您的 Alfa 網路卡（ID：`0bda:8812` 或 `0e8d:7612`）
6. 啟動虛擬機

在虛擬機內執行 `lsusb` 確認，然後依照 Kali Linux 步驟操作。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. 啟動虛擬機
2. 選單：**虛擬機 → USB 與藍牙**
3. 找到您的 Alfa 網路卡並點擊 **連接**
4. 網路卡出現在虛擬機內

執行 `lsusb` 確認，然後按照驅動程式安裝步驟操作。

---

## 疑難排解

| 問題 | 可能原因 | 解決方法 |
|------|---------|---------|
| `lsusb` 沒有顯示網路卡 ID | 連接線故障或供電不足 | 換 USB 埠。Pi 請用有源 Hub |
| `modprobe` 說「Module not found」| 缺少核心模組 | 執行 `sudo apt install linux-modules-extra-$(uname -r)` |
| 驅動程式正常但無法切換監控模式 | NetworkManager 干擾 | 先執行 `sudo airmon-ng check kill` |
| 監控模式已啟動但沒有捕獲到任何東西 | 介面名稱或頻道錯誤 | 執行 `iwconfig`，設定頻道：`iwconfig wlan0mon channel 6` |
| 注入測試失敗 | 使用了錯誤的介面 | 使用 `wlan0mon` 而非 `wlan0` |
| VIF 建立失敗 | 驅動程式未完全載入 | 拔插網路卡，或重新載入模組 |

---

## 附錄：完整 Alfa 型號清單

| 型號 | 晶片組 | 驅動程式 | 中國大陸鏡射站來源 |
|------|--------|---------|----------------|
| AWUS036ACH | RTL8812AU | `8812au` | GitHub: morrownr/8812au-20210820 |
| AWUS036ACM | MT7612U | `mt76x2u` | 核心內建驅動程式 |
| AWUS036ACS | RTL8811AU | `8821au` | GitHub: morrownr/8821au-20210708 |
| AWUS036AX | RTL8832BU | `8852bu` | GitHub: morrownr/rtl8852bu-20250826 |
| AWUS036AXM | MT7921AUN | `mt7921u` | 核心內建驅動程式 |
| AWUS036AXML | MT7921AUN | `mt7921u` | 核心內建驅動程式 |
| AWUS036AXER | RTL8832BU | `8852bu` | GitHub: morrownr/rtl8852bu-20250826 |
| AWUS036EAC | RTL8814AU | `8814au` | GitHub: morrownr/8814au |

---

{{< faq >}}

## 結語

本指南涵蓋了在**所有主要 Linux 發行版**上安裝**所有 Alfa USB WiFi 網路卡**的方法，全程使用**中國大陸可訪問的資源**。完成後您應能：

✅ 為任何 Alfa 網路卡安裝驅動程式  
✅ 在 Kali、Ubuntu、Debian 或 Raspberry Pi 上啟用監控模式  
✅ 測試封包注入  
✅ 使用支援型號的虛擬介面（VIF）  
✅ 將網路卡直通至虛擬機  

**有疑問或問題？** 請查閱本系列中特定型號的教學，或透過 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。

---

## 相關教學

本文是 **Alfa 中國大陸安裝指南**系列的一部分：

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/) — RTL8812AU，高功率
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/) — MT7612U，最佳 VIF 支援
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/) — RTL8811AU，經濟實惠
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/) — Wi-Fi 6，RTL8832BU
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/) — Wi-Fi 6，緊湊設計
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/) — Wi-Fi 6，超緊湊
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/) — Wi-Fi 6，增強功率
- [AWUS036EAC 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/) — RTL8814AU，高功率

---

*最後更新：2026 年 4 月 24 日*

## 參考來源

1. [aircrack-ng 官方文件](https://www.aircrack-ng.org/)
2. [Linux Kernel mt76 驅動](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
3. [ALFA Network 官網](https://www.alfa.com.tw/)
4. [Kali Linux 官方文件](https://www.kali.org/docs/)
5. [GitHub: morrownr](https://github.com/morrownr)
