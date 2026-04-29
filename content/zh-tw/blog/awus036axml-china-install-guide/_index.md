---
title: "ALFA AWUS036AXML 驅動程式安裝全攻略（中國適用）：Kali Linux、Ubuntu、Debian 和 Raspberry Pi"
description: "在中國使用國內鏡像站安裝 ALFA AWUS036AXML 驅動程式的完整步驟。MT7921AUN WiFi 6E 內核驅動程式，完整支援監控模式與 VIF。涵蓋 Kali Linux、Ubuntu 22/24、Debian 和 Raspberry Pi，無需訪問 GitHub。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 7
related_product: "/zh-tw/products/alfa/awus036axml/"
---

AWUS036AXML 是 ALFA 的 WiFi 6E 旗艦機種——一款三頻 USB-C 無線網路卡，涵蓋 2.4 GHz、5 GHz 及較少壅塞的 6 GHz 頻段。其 MT7921AUN 晶片使用 `mt7921u` 驅動程式，自 Linux 核心 5.18 版起已內建支援。在 Ubuntu 24.04 與 Kali 2025 上，只需從國內鏡像站安裝韌體套件即可即插即用。本指南涵蓋完整設定步驟——韌體、驅動程式驗證、監控模式、封包注入與 VIF——無需訪問 GitHub。

## 開始前的準備

請確認以下項目已就緒：

1. **ALFA AWUS036AXML** 網路卡及 USB-C 連接線
2. 附電源USB集線器——若在 Raspberry Pi 上使用則為必要
3. 可連線至國內鏡像站的網路連線

插入網路卡後，確認系統是否偵測到它：

```bash
lsusb
```

在輸出中尋找以下資訊：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

若看到 `0e8d:7961`，表示網路卡已被偵測，請前往下方對應的作業系統章節。

若未看到，請嘗試不同的 USB-C 連接埠或連接線，再次執行 `lsusb`。

## 選擇您的作業系統

請直接跳至適合您作業系統的章節：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

已完成安裝？直接跳至：

- [啟用監控模式](#enable-monitor-mode)
- [測試封包注入](#test-packet-injection)
- [虛擬介面 (VIF)](#virtual-interface-vif)
- [虛擬機器 USB 直通](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7921AUN 驅動程式已內建於 Kali 核心。您只需安裝 MediaTek 韌體套件，可從國內鏡像站取得。

### 步驟 1：切換至中國鏡像站

在終端機中開啟套件來源清單。

```bash
sudo nano /etc/apt/sources.list
```

刪除現有內容，貼上以下這行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

儲存：按 **Ctrl+O**，再按 Enter，然後按 Ctrl+X 退出。更新套件索引。

```bash
sudo apt update
```

> **備用鏡像站：** 若 中科大 (USTC) 速度較慢，請改用 清华 (Tsinghua)：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 步驟 2：安裝韌體

MT7921AUN 需要來自 `firmware-misc-nonfree` 與 `linux-firmware` 的韌體檔案。若未安裝，驅動程式雖可載入但網路卡將無法初始化。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 步驟 3：驗證驅動程式

重新開機後，插入網路卡並進行確認。

```bash
lsmod | grep mt7921
```

輸出中應出現 `mt7921u`。接著確認無線介面是否已建立。

```bash
iwconfig
```

尋找 `wlan0` 或 `wlan1`。若出現，表示驅動程式運作正常。

---

### 步驟 4：啟用監控模式 {#enable-monitor-mode}

首先確認介面名稱。

```bash
iwconfig
```

使用您看到的介面名稱（例如 `wlan1`）。終止可能干擾的程序，然後切換至監控模式。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

確認切換結果。

```bash
iwconfig
```

在該介面上尋找 `Mode:Monitor`。

---

### 步驟 5：測試封包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

成功的結果如下：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

若失敗，請重新開機後再試。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)——核心 6.8，即插即用

Ubuntu 24.04 搭載核心 6.8，已原生包含 MT7921AUN 驅動程式。

### 步驟 1：切換至中國鏡像站

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

刪除所有內容並貼上：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

以 `Ctrl+O` 儲存，再以 `Ctrl+X` 退出。

```bash
sudo apt update
```

### 步驟 2：安裝韌體

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### 步驟 3：驗證並啟用監控模式

重新開機後，執行 `lsmod | grep mt7921` 確認驅動程式已載入，然後依照上方 Kali 的監控模式步驟進行（步驟 4）。

---

### Ubuntu 22.04 (Jammy)——需要 HWE 核心

Ubuntu 22.04 搭載核心 5.15。MT7921AUN 驅動程式需要核心 ≥ 5.18，請先安裝 HWE 核心。

### 步驟 1：切換至中國鏡像站

```bash
sudo nano /etc/apt/sources.list
```

將所有行替換為：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

儲存並退出（`Ctrl+O`，再按 `Ctrl+X`）。

```bash
sudo apt update
```

### 步驟 2：安裝 HWE 核心

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

重新開機後，確認核心版本：

```bash
uname -r
```

應顯示 5.19 或更高版本。接著按照上方步驟安裝韌體並啟用監控模式。

### 步驟 3：安裝韌體

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### 步驟 1：切換至中國鏡像站

```bash
sudo nano /etc/apt/sources.list
```

刪除所有內容並貼上（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

以 `Ctrl+O` 儲存，再以 `Ctrl+X` 退出。

```bash
sudo apt update
```

### 步驟 2：安裝韌體

Debian 12 Bookworm 搭載核心 6.1——與 MT7921AUN 相容。

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### 步驟 3：驗證並啟用監控模式

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 步驟 4：測試封包注入

```bash
sudo aireplay-ng --test wlan1
```

出現 `Injection is working!` 即確認網路卡完全正常運作。

---

## Raspberry Pi 4B / 5

> AWUS036AXML 在負載下最高耗電 2.7W。在 Raspberry Pi 上務必使用附電源USB集線器。

### 步驟 1：下載 Kali Linux ARM64 映像檔

官方頁面：https://www.kali.org/get-kali/#kali-arm

選擇 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)**——必須選擇 64 位元版本。

> **中國鏡像站：** https://repo.huaweicloud.com/kali-images/ — 瀏覽至最新發布資料夾並下載 ARM64 映像檔。

### 步驟 2：燒錄至 MicroSD

```bash
lsblk
# Replace /dev/sdX with your actual SD card
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

預設帳號密碼：**kali / kali**。

### 步驟 3：切換至中國鏡像站並安裝韌體

```bash
sudo nano /etc/apt/sources.list
```

替換為：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

接著執行：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### 步驟 4：驗證驅動程式

```bash
lsmod | grep mt7921
```

應出現 `mt7921u`。

### 步驟 5：啟用監控模式

在已內建 Wi-Fi 的 Pi 上，AWUS036AXML 會顯示為 `wlan1`。

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 步驟 6：測試封包注入

```bash
sudo aireplay-ng --test wlan1
```

---

## 虛擬機器 USB 直通 {#virtual-machine-usb-passthrough}

### VirtualBox

1. 關閉虛擬機器。前往 **設定 → USB**。
2. 啟用 **USB 3.0 (xHCI) 控制器**。
3. 點擊 **+** 新增 USB 篩選器。
4. 選擇：**MediaTek Inc.**（ID：0e8d:7961）。
5. 啟動虛擬機器——網路卡將出現在 Kali 內部。

在虛擬機器中執行 `lsusb` 確認 `0e8d:7961`，然後依照上方 Kali 步驟進行。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. 啟動虛擬機器。
2. 選單：**虛擬機器 → USB 與藍牙**。
3. 找到 **MediaTek MT7921AUN** 並點擊**連線**。
4. 在虛擬機器中執行 `lsusb` 確認，然後依照上方 Kali 步驟進行。

---

## 虛擬介面 (VIF) {#virtual-interface-vif}

MT7921AUN 具備完整的核心原生 VIF 支援。您可以在同一張網路卡上同時執行監控介面和受管介面——無需任何補丁。

### 在受管模式旁建立監控介面

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

您應同時看到 `wlan0`（受管）與 `mon0`（監控）處於啟用狀態。

### 保持連線的同時進行監控

```bash
sudo airodump-ng mon0
```

`wlan0` 保持連接狀態，同時 `mon0` 擷取範圍內的所有封包。

### 假 AP + 監控

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> **關於 hostapd 的注意事項：** 完整的 AP 操作需要設定 `hostapd`。上述步驟僅確認網路卡可以建立該介面——實際的 AP 設定屬於另一個主題。

---

## 疑難排解

| 問題 | 可能原因 | 解決方法 |
|---------|-------------|-----|
| `lsusb` 未顯示 0e8d:7961 | 網路卡未供電或連接線不良 | 嘗試不同的 USB-C 連接埠。在 Raspberry Pi 上使用附電源USB集線器。 |
| `lsmod` 未顯示 mt7921u | 韌體未安裝或核心版本過舊 | 執行 `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` |
| Ubuntu 22.04 無法載入驅動程式 | 核心 5.15 版本過舊 | 安裝 HWE：`sudo apt install linux-generic-hwe-22.04` |
| 介面出現但無法連線 | 韌體檔案缺失 | 執行 `sudo apt install firmware-misc-nonfree` 後重新開機 |
| 切換監控模式失敗 | 介面仍處於啟用狀態 | 在執行 `iw dev` 指令前先執行 `sudo ip link set wlan1 down` |
| 注入測試顯示「No Answer」 | AP 距離過遠或介面錯誤 | 移近距離。以 `iwconfig` 確認 `Mode:Monitor`。 |
| VIF 介面建立失敗 | 驅動程式未完全載入 | 拔除後執行：`sudo rmmod mt7921u && sudo modprobe mt7921u` |

## 中國鏡像站參考

| 資源 | 網址 | 用途 |
|----------|-----|---------|
| Alfa 官方驅動程式 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驅動程式套件、韌體 |
| Alfa 文件 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 產品手冊 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推薦） |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推薦） |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 映像檔（備用） |

## 更多中國適用的 Alfa 網路卡安裝指南

本文是 **Alfa China Install Guide** 系列的一部分：

- [AWUS036ACH 中國安裝指南](/zh-tw/blog/awus036ach-china-install-guide/) — RTL8812AU，高功率
- [AWUS036ACM 中國安裝指南](/zh-tw/blog/awus036acm-china-install-guide/) — MT7612U，完整 VIF
- [AWUS036ACS 中國安裝指南](/zh-tw/blog/awus036acs-china-install-guide/) — RTL8811AU，監控模式
- [AWUS036AX 中國安裝指南](/zh-tw/blog/awus036ax-china-install-guide/) — RTL8832BU，WiFi 6
- [AWUS036AXER 中國安裝指南](/zh-tw/blog/awus036axer-china-install-guide/) — RTL8832BU，nano
- [AWUS036AXM 中國安裝指南](/zh-tw/blog/awus036axm-china-install-guide/) — MT7921AUN，L 型 USB-A
- AWUS036AXML ← 您在此
- [AWUS036EACS 中國安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/) — RTL8821CU，Windows

有疑問？請在下方留言，或透過 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
