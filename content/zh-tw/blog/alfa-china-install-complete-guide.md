---
title: "完整教學：在中國大陸 Linux 系統安裝所有 Alfa USB WiFi 網卡 — Kali、Ubuntu、Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "驅動程式", "中國", "監控模式", "封包注入", "無線網路"]
categories: ["驅動程式安裝教學"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "終極 Alfa USB WiFi 網卡 Linux 安裝指南，適用於中國大陸用戶。涵蓋 Kali Linux、Ubuntu 22/24、Debian、Raspberry Pi，全程使用境內鏡像，無需訪問 GitHub。"
---

## 歡迎閱讀 Alfa Linux 終極安裝指南

如果您正在閱讀本文，您可能購買了 Alfa USB WiFi 網卡後遇到了以下問題：

- 您在中國大陸，無法訪問 GitHub
- 驅動程式安裝步驟複雜難懂
- 您需要啟用監控模式（Monitor Mode）和封包注入（Packet Injection）進行無線測試
- 不確定您的 Alfa 型號需要哪個驅動程式

本指南解決**所有上述問題**。我們將帶您在**所有主要 Linux 發行版**上安裝**每一款 Alfa USB WiFi 網卡**，全程僅使用**中國大陸可訪問的鏡像**。無需 GitHub，告別挫折感。

---

## 為什麼需要這份指南

Alfa USB WiFi 網卡深受滲透測試員、網路工程師和無線愛好者的歡迎，因為它們支援監控模式和封包注入——這些功能是大多數消費級 WiFi 網卡所沒有的。

但問題在於：**大多數驅動程式安裝教學都假設您能訪問 GitHub**。在中國大陸這是不可能的。本指南專為中國大陸用戶設計，全程僅使用境內可訪問的鏡像和資源。

---

## 快速型號對照表

開始之前，先確認您使用的 Alfa 網卡型號及其晶片組：

### AX 系列（Wi-Fi 6 / 802.11ax）

| 型號 | 晶片組 | 驅動程式 | 最適合 |
|------|--------|---------|--------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | 通用，覆蓋範圍好 |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | 緊湊設計 |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | 超緊湊 |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | 增強功率 |

### AC 系列（Wi-Fi 5 / 802.11ac）

| 型號 | 晶片組 | 驅動程式 | 最適合 |
|------|--------|---------|--------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | 高功率，覆蓋範圍極佳 |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **最佳 VIF 支援**，即插即用 |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | 經濟實惠 |

### 如何確認您的型號？

1. 查看網卡上的標籤
2. 查看原包裝盒
3. 若是網購，查看訂單記錄

確認型號後，直接跳至對應章節，或依照通用流程操作。

---

## 開始前的準備

請確保以下物品就緒：

1. **Alfa USB WiFi 網卡** — 適合您需求的型號
2. **USB 連接線** — 原廠附送的即可
3. **有源 USB Hub** — 若使用 Raspberry Pi 則必備
4. **可用的網路連線** — 用於連接中國大陸境內鏡像
5. **sudo 權限** — 安裝驅動程式需要管理員權限

先插入網卡，確認系統能偵測到：

```bash
lsusb
```

在輸出中尋找網卡的廠商 ID：

- **Alfa 網卡**顯示為 `0e8d`（MediaTek）或 `0bda`（Realtek）
- 範例：`Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- 範例：`Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

若看到 ID，代表網卡已被偵測到，請繼續前往驅動程式安裝章節。

若未看到，請換一個 USB 埠，更換連接線，再次執行 `lsusb`。

---

## 選擇您的作業系統

直接跳至對應章節：

- [Kali Linux](#kali-linux-安裝)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-安裝)
- [Debian 12 (Bookworm)](#debian-12-bookworm-安裝)
- [Raspberry Pi OS（64 位元）](#raspberry-pi-os-安裝)

已安裝驅動程式？直接跳至進階章節：

- [啟用監控模式](#在任何網卡上啟用監控模式)
- [測試封包注入](#測試封包注入)
- [虛擬介面（VIF）支援](#虛擬介面-vif-支援)
- [虛擬機 USB 直通](#虛擬機-usb-直通)

---

## 中國大陸可用鏡像參考

本指南所有步驟僅使用以下中國大陸可訪問的鏡像：

| 資源 | URL | 用途 |
|------|-----|------|
| **Alfa 官方下載** | [files.alfa.com.tw](https://files.alfa.com.tw) | 驅動程式套件、韌體 |
| **Alfa 文件** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 產品手冊（英文）|
| **清華大學鏡像** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里雲鏡像** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推薦）|
| **中科大鏡像** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推薦）|
| **華為雲鏡像** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 映像（備用）|
| **Gitee（GitHub 替代）** | [gitee.com](https://gitee.com) | 驅動程式原始碼 |

---

## Kali Linux 安裝

Kali Linux 已預裝無線工具，讓 Alfa 網卡運作只需幾個步驟。

### 第一步：切換至中國大陸鏡像

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

> **備用鏡像：** 若中科大（USTC）速度慢，改用清華（Tsinghua）：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### 第二步：依晶片組安裝驅動程式

#### AX 系列（RTL8832BU）

```bash
sudo apt install -y rtl8832bu-dkms
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

再次執行 `lsusb`，網卡應會顯示。然後檢查無線介面：

```bash
iwconfig
```

尋找 `wlan0` 或 `wlan1`。若介面出現，代表驅動程式正常運作。

### 第四步：啟用監控模式

停止干擾程序：

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

### 第一步：切換至中國大陸鏡像

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

從 Gitee 克隆：

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC 系列 - Realtek（RTL8812AU）

從 Gitee 克隆：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
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

### 第一步：切換至中國大陸鏡像

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
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC 系列 - Realtek（RTL8812AU）

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
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

> **重要提示：** AWUS036ACH 消耗約 500mW，AWUS036ACM 消耗約 400mW。**務必使用有源 USB Hub** 以防止 Pi 在負載下降頻或當機。

### 第一步：下載 Kali Linux ARM64 映像

前往：https://www.kali.org/get-kali/#kali-arm

選擇 **Raspberry Pi 4（64 位元）** 或 **Raspberry Pi 5（64 位元）**。請勿使用 32 位元版本。

> **中國大陸鏡像：** 若 kali.org 速度慢，使用華為雲：https://repo.huaweicloud.com/kali-images/

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

### 第三步：切換至中國大陸鏡像

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
sudo apt install -y rtl8832bu-dkms
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

Pi 有內建 Wi-Fi，Alfa 網卡通常顯示為 `wlan1`：

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

## 在任何網卡上啟用監控模式

驅動程式安裝完成後，啟用監控模式非常簡單：

### 第一步：確認介面名稱

```bash
iwconfig
```

記下是 `wlan0` 還是 `wlan1`。

### 第二步：停止干擾程序

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

確認網卡可以發送自訂封包——無線測試的必備功能。

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
- 確認沒有其他程序佔用介面（`iwconfig`）
- 靠近 WiFi AP 進行測試
- 確認使用的是 `wlan0mon` 而非 `wlan0`

---

## 虛擬介面（VIF）支援

VIF（虛擬介面功能）允許在單一網卡上同時運行多個介面，例如：

- 同時運行**受管模式**（`wlan0`）和**監控模式**（`mon0`）
- 在保持網路連接的同時捕獲流量

### 哪些網卡支援 VIF？

| 晶片組 | VIF 支援 | 備註 |
|--------|---------|------|
| **MT7612U（AWUS036ACM）** | ✅ 完整原生支援 | VIF 工作流程的最佳選擇 |
| **RTL8812AU（AWUS036ACH）** | ⚠️ 有限 | 無法同時運行受管模式和監控模式 |
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

在虛擬機中運行 Linux？您需要將 USB 網卡直通到虛擬機內部。

### VirtualBox

1. 關閉虛擬機
2. 進入 **設定 → USB**
3. 啟用 **USB 3.0（xHCI）控制器**
4. 點擊 **+** 新增 USB 篩選器
5. 選擇您的 Alfa 網卡（ID：`0bda:8812` 或 `0e8d:7612`）
6. 啟動虛擬機

在虛擬機內執行 `lsusb` 確認，然後依照 Kali Linux 步驟操作。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. 啟動虛擬機
2. 選單：**虛擬機 → USB 與藍牙**
3. 找到您的 Alfa 網卡並點擊 **連接**
4. 網卡出現在虛擬機內

執行 `lsusb` 確認，然後按照驅動程式安裝步驟操作。

---

## 疑難排解

| 問題 | 可能原因 | 解決方法 |
|------|---------|---------|
| `lsusb` 沒有顯示網卡 ID | 連接線故障或供電不足 | 換 USB 埠。Pi 請用有源 Hub |
| `modprobe` 說「Module not found」| 缺少核心模組 | 執行 `sudo apt install linux-modules-extra-$(uname -r)` |
| 驅動程式正常但無法切換監控模式 | NetworkManager 干擾 | 先執行 `sudo airmon-ng check kill` |
| 監控模式已啟動但沒有捕獲到任何東西 | 介面名稱或頻道錯誤 | 執行 `iwconfig`，設定頻道：`iwconfig wlan0mon channel 6` |
| 注入測試失敗 | 使用了錯誤的介面 | 使用 `wlan0mon` 而非 `wlan0` |
| VIF 建立失敗 | 驅動程式未完全載入 | 拔插網卡，或重新載入模組 |

---

## 附錄：完整 Alfa 型號清單

| 型號 | 晶片組 | 驅動程式 | 中國大陸鏡像來源 |
|------|--------|---------|----------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | 核心內建驅動程式 |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## 結語

本指南涵蓋了在**所有主要 Linux 發行版**上安裝**所有 Alfa USB WiFi 網卡**的方法，全程使用**中國大陸可訪問的資源**。完成後您應能：

✅ 為任何 Alfa 網卡安裝驅動程式  
✅ 在 Kali、Ubuntu、Debian 或 Raspberry Pi 上啟用監控模式  
✅ 測試封包注入  
✅ 使用支援型號的虛擬介面（VIF）  
✅ 將網卡直通至虛擬機  

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
