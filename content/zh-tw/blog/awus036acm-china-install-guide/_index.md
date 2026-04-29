---
title: "ALFA AWUS036ACM 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "驅動", "中國", "monitor-mode", "vif"]
categories: ["驅動安裝指南"]
series: ["alfa-china-install-guide"]
description: "手把手教你在中國網路環境下安裝 ALFA AWUS036ACM 驅動，全程使用國內鏡像，無需翻牆。MT7612U 核心原生驅動，完整 VIF 支援。涵蓋 Kali Linux、Ubuntu 22/24、Debian 和樹莓派。"
related_product: "/zh-tw/products/alfa/awus036acm/"
series_order: 2
---

AWUS036ACM 是 Alfa 無線網卡裡最好裝的一款。它使用 MT7612U 晶片，驅動 `mt76x2u` 從 Linux 4.19 起就已經內建在核心裡了。大多數情況下，插上就能用，最多跑兩三條指令。這篇文章涵蓋完整流程：驅動驗證、監聽模式、封包注入，以及 VIF（虛擬介面）——全部使用國內鏡像，不需要訪問 GitHub。

## 準備工作

請確認以下幾樣東西都備齊了：

1. **ALFA AWUS036ACM** 無線網卡
2. USB 傳輸線（盒子裡附帶的就行）
3. 帶獨立供電的 USB Hub——樹莓派使用者必備
4. 能存取國內鏡像的網路連線

把網卡插上，確認系統能識別：

```bash
lsusb
```

在輸出裡找這一行：

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

看到 `0e8d:7612` 就說明識別成功了，直接跳到對應系統的章節。

如果沒看到，換個 USB 埠或者換根線，再執行一次 `lsusb`。

## 選擇你的系統

直接跳到對應的章節：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 4B / 5](#樹莓派-4b--5)

已經裝好驅動了？直接跳到：

- [開啟監聽模式](#開啟監聽模式)
- [測試封包注入](#測試封包注入)
- [虛擬介面（VIF）](#虛擬介面vif)
- [虛擬機器 USB 直通](#虛擬機器-usb-直通)

---

## Kali Linux

MT7612U 的驅動已經內建在 Kali 核心裡了。絕大多數情況下，網卡插上去就可以用。下面的步驟幫你確認驅動已經載入，然後直接進入監聽模式。

### 第一步：切換到國內鏡像

開啟軟體來源檔案：

```bash
sudo nano /etc/apt/sources.list
```

把裡面的內容全刪掉，貼上下面這一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

儲存：按 **Ctrl+O**，Enter，再按 Ctrl+X 離開。刷新套件索引：

```bash
sudo apt update
```

> **備用鏡像：** 如果中科大鏡像速度慢，換清華大學鏡像：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：驗證驅動

檢查插上網卡後核心有沒有自動載入模組：

```bash
lsmod | grep mt76
```

輸出裡應該有 `mt76x2u`。如果沒有，手動載入：

```bash
sudo modprobe mt76x2u
```

再執行一次 `lsmod | grep mt76` 確認。然後驗證網卡介面是否出現：

```bash
iwconfig
```

如果看到 `wlan0` 或 `wlan1` 的介面，驅動就沒問題了。

---

### 第二步（備選）：安裝額外核心模組

如果 `modprobe mt76x2u` 回報「找不到模組」，說明你的核心沒有包含 MT76 模組，從國內鏡像安裝：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

裝完再載入一次：

```bash
sudo modprobe mt76x2u
```

如果連這個套件都找不到，就從原始碼編譯：

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **注意：** 如果那個 Gitee 網址打不開，在 Gitee 搜尋 `mt76` 找最近更新的 fork。也可以直接從 [files.alfa.com.tw](https://files.alfa.com.tw) 下載驅動套件。

---

### 第三步：開啟監聽模式 {#開啟監聽模式}

先看看系統給網卡分配了什麼介面名稱：

```bash
iwconfig
```

找到 `wlan0` 或 `wlan1`，記下來，下面的指令用那個名稱。

停掉 NetworkManager 和 wpa_supplicant，不然它們會搶佔介面：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

確認切換成功：

```bash
iwconfig
```

看到 `wlan0mon` 且顯示 `Mode:Monitor`，就說明監聽模式開啟成功了。

---

### 第四步：測試封包注入 {#測試封包注入}

```bash
sudo aireplay-ng --test wlan0mon
```

成功的輸出長這樣：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

如果失敗了，重新開機再試一次。還是不行的話，用 `iwconfig` 確認沒有其他程序佔用這個介面。

---

## Ubuntu 22.04 / 24.04

MT7612U 驅動同樣內建在 Ubuntu 核心裡，不過有時候需要安裝 `linux-modules-extra` 才能載入。

### 第一步：切換到國內鏡像

#### Ubuntu 24.04 (Noble)

開啟 DEB822 格式的軟體來源檔案：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

全部刪掉，貼上以下內容：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

`Ctrl+O` 儲存，`Ctrl+X` 離開。

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

替換全部內容為：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

儲存離開，然後刷新：

```bash
sudo apt update
```

---

### 第二步：載入驅動

直接嘗試載入模組：

```bash
sudo modprobe mt76x2u
```

如果提示找不到模組，安裝額外模組套件：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

確認介面出現：

```bash
iwconfig
```

---

### 第三步：安裝無線工具

```bash
sudo apt install -y aircrack-ng
```

---

### 第四步：開啟監聽模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **注意：** 如果有其他無線網卡，介面名稱可能是 `wlan1`，先用 `iwconfig` 確認。

---

### 第五步：測試封包注入

```bash
sudo aireplay-ng --test wlan0mon
```

出現 `Injection is working!` 就成功了。

---

## Debian

MT7612U 的驅動在 Debian 核心裡，但有時候需要安裝 `firmware-misc-nonfree` 韌體套件才能完整初始化。

### 第一步：切換到國內鏡像

```bash
sudo nano /etc/apt/sources.list
```

全部刪掉，貼上以下內容（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

儲存離開，刷新：

```bash
sudo apt update
```

### 第二步：安裝非自由韌體

MT7612U 需要 `firmware-misc-nonfree` 裡的韌體檔案，少了這個網卡能識別但無法正常運作：

```bash
sudo apt install -y firmware-misc-nonfree
```

### 第三步：載入驅動

```bash
sudo modprobe mt76x2u
```

如果模組找不到：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

用 `iwconfig` 確認介面出現。

### 第四步：開啟監聽模式

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

用 `iwconfig` 確認出現 `wlan0mon` 且模式為 `Monitor`。

### 第五步：測試封包注入

```bash
sudo aireplay-ng --test wlan0mon
```

看到 `Injection is working!` 就完成了。

---

## 樹莓派 4B / 5

> AWUS036ACM 滿載約消耗 400mW，建議使用帶獨立供電的 USB Hub，避免樹莓派限速。

---

### 第一步：下載 Kali Linux ARM64 映像

前往官方 Kali ARM 下載頁面：
https://www.kali.org/get-kali/#kali-arm

選 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)**，不要選 32 位版本。

> **國內鏡像：** kali.org 慢的話用華為雲：
> https://repo.huaweicloud.com/kali-images/
> 找最新版本資料夾，下載同款 ARM64 映像。

---

### 第二步：寫入 MicroSD

先查 SD 卡的裝置路徑：

```bash
lsblk
```

找到你的卡（例如 `sdb` 或 `mmcblk0`），然後寫入：

```bash
# 把 /dev/sdX 換成你實際的 SD 卡路徑（用 lsblk 確認）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

等 `sync` 跑完再拔卡，用 SD 卡啟動樹莓派。預設帳號：**kali / kali**。

---

### 第三步：切換到國內鏡像

```bash
sudo nano /etc/apt/sources.list
```

全部替換為：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

儲存，更新並升級：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### 第四步：驗證驅動

重新開機後插上網卡，檢查模組：

```bash
lsmod | grep mt76
```

看到 `mt76x2u` 就沒問題。如果沒有：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### 第五步：開啟監聽模式

樹莓派有內建 Wi-Fi，AWUS036ACM 通常會被分配到 `wlan1`：

```bash
iwconfig
```

確認介面名稱，然後：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

用 `iwconfig` 確認出現 `wlan1mon` 且模式為 `Monitor`。

---

### 第六步：測試封包注入

```bash
sudo aireplay-ng --test wlan1mon
```

看到 `Injection is working!` 就完成了。如果失敗，檢查是否使用了帶供電的 USB Hub。

---

## 虛擬機器 USB 直通

### VirtualBox

1. 關閉虛擬機器，進入 **設定 → USB**。
2. 啟用 **USB 3.0 (xHCI) 控制器**。
3. 點 **+** 新增 USB 篩選器。
4. 選擇：**MediaTek Inc. MT7612U**（ID: 0e8d:7612）。
5. 啟動虛擬機器，網卡就會出現在 Kali 裡。

在虛擬機器裡用 `lsusb` 確認 `0e8d:7612`，然後按上面的 Kali 步驟操作。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. 啟動虛擬機器。
2. 選單：**虛擬機器 → USB 與藍牙**。
3. 找到 **MediaTek MT7612U**，點 **連接**。
4. 在虛擬機器裡 `lsusb` 確認，然後按 Kali 步驟操作。

---

## 虛擬介面（VIF）

這是 AWUS036ACM 比 AWUS036ACH 強的地方。MT7612U 晶片完整支援核心原生 VIF，可以在同一張網卡上同時執行監聽介面和管理模式（或 AP 模式）——不需要打補丁，開箱即用。

### 建立第二個虛擬介面

在網卡以 `wlan0` 連接網路（管理模式）的同時，再新增一個監聽介面：

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

驗證兩個介面都在執行：

```bash
iwconfig
```

你應該能同時看到 `wlan0`（已連線，管理模式）和 `mon0`（監聽模式）。一張網卡，兩個功能同時跑。

### 用法一：連著網同時抓封包

`wlan0` 保持連線，`mon0` 在背景掃描流量：

```bash
sudo airodump-ng mon0
```

適合需要同時在線又要分析周邊流量的情境。

### 用法二：假 AP + 監聽

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

`iwconfig` 確認 `wlan0`、`ap0`、`mon0` 三個介面都在。

> **注意：** 完整的 AP 運作還需要設定 `hostapd`，那是另一個主題。上面的指令只是驗證網卡能建立這些介面。

---

## 故障排查

| 問題 | 可能原因 | 解決方法 |
|------|---------|---------|
| `lsusb` 看不到 0e8d:7612 | 網卡沒通電或傳輸線有問題 | 換 USB 埠，樹莓派用帶供電的 Hub |
| `modprobe mt76x2u` 說找不到模組 | 核心缺少額外模組 | 執行 `sudo apt install linux-modules-extra-$(uname -r)` |
| 介面出現但無法連線 | 韌體檔案缺失 | Debian 執行 `sudo apt install firmware-misc-nonfree` |
| `airmon-ng start wlan0` 失敗 | NetworkManager 還在執行 | 先執行 `sudo airmon-ng check kill` |
| 監聽模式開啟但抓不到流量 | 頻道或介面名稱錯誤 | 設定頻道：`iwconfig wlan0mon channel 6` |
| 注入測試回傳「No Answer」 | AP 太遠或介面名稱錯誤 | 靠近 AP，確認用的是 `wlan0mon` |
| VIF 介面建立失敗 | 驅動未完整載入 | `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## 國內鏡像參考

本文用到的所有資源，全部不需要 GitHub：

| 資源 | 網址 | 用途 |
|------|------|------|
| Alfa 官方驅動 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驅動套件、韌體 |
| Alfa 文件 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 產品手冊 |
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推薦） |
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推薦） |
| 華為雲鏡像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 映像（備用） |
| MT76 驅動（Gitee） | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | 手動編譯備選 |

## 系列文章

本文是 **Alfa 網卡中國安裝全攻略** 系列的一部分，每篇文章對應一款型號：

- [AWUS036ACH 中國安裝全攻略](/zh-tw/blog/awus036ach-china-install-guide/) — RTL8812AU，大功率
- AWUS036ACM ← 目前文章
- [AWUS036ACS 中國安裝全攻略](/zh-tw/blog/awus036acs-china-install-guide/)
- [AWUS036AX 中國安裝全攻略](/zh-tw/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 中國安裝全攻略](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 中國安裝全攻略](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 中國安裝全攻略](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 中國安裝全攻略](/zh-tw/blog/awus036eacs-china-install-guide/)

有問題？在下方留言，或透過 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
