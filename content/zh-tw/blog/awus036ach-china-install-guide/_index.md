---
title: "ALFA AWUS036ACH 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "驅動", "中國", "monitor-mode"]
categories: ["驅動安裝指南"]
series: ["Alfa 中國安裝全攻略"]
description: "手把手教你在中國網路環境下安裝 ALFA AWUS036ACH 驅動，全程使用國內鏡像，無需翻牆。涵蓋 Kali Linux、Ubuntu 22/24、Debian 和樹莓派。"
related_product: "/zh-tw/products/alfa/awus036ach/"
---

剛拿到 AWUS036ACH，插上去 Linux 沒反應？正常。這張網卡用的是 RTL8812AU 晶片，驅動不是開箱即用的。整個安裝過程大概 30 分鐘，全程用國內鏡像，不需要連 GitHub。

## 開始之前

先把這幾樣東西準備好：

1. **ALFA AWUS036ACH** 網卡
2. USB 連接線（盒子裡附帶的那根就行）
3. 有源 USB 集線器 — 樹莓派必須用，否則供電不夠
4. 能存取國內鏡像源的網路

插好網卡，先確認系統認到了：

```bash
lsusb
```

在輸出裡找這一行：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

看到 `0bda:8812` 就說明網卡已經識別，直接跳到你對應的系統部分。

沒看到？換個 USB 埠試試，或者換根連接線，然後再跑一次 `lsusb`。

## 選擇你的系統

跳到對應章節：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

已經裝好驅動了？直接跳到：

- [開啟監聽模式（Monitor Mode）](#enable-monitor-mode)
- [測試封包注入（Packet Injection）](#test-packet-injection)
- [虛擬機 USB 直通](#virtual-machine-usb-passthrough)

---

## Kali Linux

Kali 自帶了很完整的無線工具鏈。裝好 AWUS036ACH 驅動只需要四步，先切換到國內鏡像源，後面所有下載都快很多。

### 第一步：切換國內鏡像源

在終端機打開軟體來源設定檔：

```bash
sudo nano /etc/apt/sources.list
```

把裡面的內容全部刪掉，貼上這一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

儲存：按 **Ctrl+O**，Enter，再按 Ctrl+X 退出。然後更新套件索引：

```bash
sudo apt update
```

> **備用鏡像：** 如果中科大那邊速度慢，換清華的：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安裝驅動

Kali 的套件庫裡有預先編譯好的 DKMS 驅動套件，一條指令搞定：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

裝了 DKMS 之後，核心升級會自動重新編譯驅動，不用手動重裝。

驗證驅動載入正常：

```bash
modinfo 88XXau | grep -E "filename|version"
```

能看到以 `.ko` 結尾的 `filename` 行和一個版本號（例如 `5.6.4.2`），就說明驅動就緒了。

---

### 第二步（備選方案）：手動從原始碼編譯

只有上面 `apt install` 失敗了才需要走這條路。先裝編譯相依套件：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

從 Gitee 下載驅動原始碼：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **注意：** 如果這個網址打不開，去 Gitee 搜尋 `rtl8812au`，選最近有更新的 fork。也可以直接從 [files.alfa.com.tw](https://files.alfa.com.tw) 下載原始碼包。

進入目錄，編譯並安裝：

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

把驅動載入核心：

```bash
sudo modprobe 88XXau
```

---

### 第三步：開啟監聽模式（Monitor Mode） {#enable-monitor-mode}

切換監聽模式之前，先看看系統給網卡分配了哪個介面名稱：

```bash
iwconfig
```

找 `wlan0` 或 `wlan1` 那一行，後面的指令裡用你實際看到的名稱。

停掉 NetworkManager 和 wpa_supplicant，它們會跟網卡搶佔，導致監聽模式開不起來：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

確認切換成功：

```bash
iwconfig
```

看到 `wlan0mon`，並且 `Mode:Monitor`，網卡就可以抓封包了。

---

### 第四步：測試封包注入（Packet Injection） {#test-packet-injection}

對監聽介面跑注入測試：

```bash
sudo aireplay-ng --test wlan0mon
```

成功的輸出長這樣：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

如果測試失敗，重新開機再試一次。重開機後還是失敗的話，跑 `iwconfig` 確認介面狀態，確保只有 `wlan0mon` 在用，沒有其他行程佔著這張網卡。

---

## Ubuntu 22.04 / 24.04

Ubuntu 兩個版本的軟體來源格式不一樣，下面分別處理。鏡像用**阿里雲**，速度穩定。

### 第一步：切換國內鏡像源

按你的 Ubuntu 版本選一個路徑，只做對應那個就行。

#### Ubuntu 24.04 (Noble)

打開新格式的 DEB822 軟體來源檔案：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

把檔案裡的內容全部清掉，貼上以下內容：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

按 `Ctrl+O` 儲存，`Ctrl+X` 退出。

#### Ubuntu 22.04 (Jammy)

打開舊格式的軟體來源檔案：

```bash
sudo nano /etc/apt/sources.list
```

把所有內容替換成這幾行：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

同樣按 `Ctrl+O` 儲存，`Ctrl+X` 退出。

#### 更新套件索引

兩個版本都要跑這一步：

```bash
sudo apt update
```

---

### 第二步：安裝編譯相依套件

驅動需要從原始碼編譯，先把核心標頭檔和編譯工具裝上：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

`$(uname -r)` 會自動偵測你目前跑的核心版本，不用手動填。

---

### 第三步：下載驅動原始碼（國內鏡像）

從 Gitee 克隆驅動倉庫，國內直接存取：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

進入克隆好的目錄：

```bash
cd rtl8812au
```

> **提示：** 如果這個網址逾時或回傳 404，去 [gitee.com](https://gitee.com) 搜尋 `rtl8812au`，選提交日期最近的 fork。

---

### 第四步：編譯並安裝

編譯核心模組：

```bash
make
```

安裝到系統：

```bash
sudo make install
```

註冊到 DKMS，之後核心升級會自動重建：

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

把模組載入目前核心：

```bash
sudo modprobe 88XXau
```

驗證模組載入成功：

```bash
modinfo 88XXau | grep filename
```

輸出裡能看到 `88XXau.ko` 路徑就說明驅動已經在跑了。

---

### 第五步：開啟監聽模式

先終止可能干擾的行程：

```bash
sudo airmon-ng check kill
```

然後把網卡切換到監聽模式：

```bash
sudo airmon-ng start wlan0
```

> **提示：** 你的介面可能是 `wlan1` 而不是 `wlan0`。先跑 `iwconfig` 看一下所有無線介面，把上面指令裡的名稱換成實際的。

---

### 第六步：測試封包注入

```bash
sudo aireplay-ng --test wlan0mon
```

成功的話會出現 `Injection is working!`。如果報介面相關的錯，用 `iwconfig wlan0mon` 檢查一下監聽模式有沒有真正開起來。

---

## Debian

Debian 預設指向海外伺服器。換成清華大學鏡像之後，下載速度從爬變跑。

### 第一步：切換國內鏡像源

打開軟體來源清單：

```bash
sudo nano /etc/apt/sources.list
```

全部刪掉，貼上這三行（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

按 `Ctrl+O` 儲存，`Ctrl+X` 退出，然後更新索引：

```bash
sudo apt update
```

### 第二步：安裝編譯相依套件

AWUS036ACH 驅動要從原始碼編譯，先把核心標頭檔和工具裝上：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

這條指令會自動對應你目前的核心版本。

### 第三步：下載驅動原始碼（國內鏡像）

從 Gitee 克隆驅動倉庫：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

進入專案目錄：

```bash
cd rtl8812au
```

> **網址打不開？** 去 Gitee 搜尋 `rtl8812au`，選最近更新的 fork。

### 第四步：編譯並安裝

在 `rtl8812au` 目錄裡依序執行：

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

DKMS 會在核心升級後自動重建驅動，不用再手動來一遍。

### 第五步：開啟監聽模式

先終止搶網卡的行程：

```bash
sudo airmon-ng check kill
```

開啟監聽模式：

```bash
sudo airmon-ng start wlan0
```

如果系統沒有 `airmon-ng`，先裝：

```bash
sudo apt install -y aircrack-ng
```

確認介面已經起來：

```bash
iwconfig
```

輸出裡能看到 `wlan0mon` 就對了。

### 第六步：測試封包注入

```bash
sudo aireplay-ng --test wlan0mon
```

看到注入測試結果刷屏說明網卡工作正常，可以開始了。

---

## Raspberry Pi 4B / 5

> AWUS036ACH 功耗約 500mW。直接插樹莓派 USB 埠在高負載下可能導致 Pi 限速甚至重新開機。**一定要用有源 USB 集線器。**

---

### 第一步：下載 Kali Linux ARM64 映像檔

去 Kali 官方 ARM 下載頁：
https://www.kali.org/get-kali/#kali-arm

選 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)**，對應你的板子。不要下 32 位元映像，驅動編譯需要 64 位元核心。

> **國內備用：** kali.org 載入慢的話，用華為雲：
> https://repo.huaweicloud.com/kali-images/
> 進最新版本目錄，下載同款 ARM64 映像。

---

### 第二步：燒錄到 MicroSD 卡

插入 MicroSD 卡，寫入前先確認裝置路徑：

```bash
lsblk
```

找到你的卡，一般顯示為 `sdb` 或 `mmcblk0`。然後燒錄，把 `/dev/sdX` 換成實際路徑：

```bash
# 替換 /dev/sdX 為你的 SD 卡路徑（用 lsblk 確認）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

`sync` 結束後再拔卡。把卡插到 Pi 上開機，預設帳號密碼是 **kali / kali**。

---

### 第三步：切換國內鏡像源

第一次開機後，打開軟體來源檔案：

```bash
sudo nano /etc/apt/sources.list
```

刪掉全部內容，換成這一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 儲存，Enter，Ctrl+X 退出。然後更新並升級系統：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

重新開機是為了把核心更新也帶進來，之後裝驅動才不會出問題。

---

### 第四步：安裝驅動（ARM64）

ARM64 上用 DKMS 套件和 x86 完全一樣，沒有額外步驟：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

如果提示找不到這個套件，就從原始碼編譯：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### 第五步：開啟監聽模式

先看看 Pi 給網卡分配了哪個介面名稱：

```bash
iwconfig
```

Pi 有內建 Wi-Fi，AWUS036ACH 通常會被分配成 `wlan1`，內建網卡佔 `wlan0`。用 `iwconfig` 裡看到的名稱替換下面指令裡的介面名：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

再跑一次 `iwconfig`，看到以 `mon` 結尾的介面（Pi 上通常是 `wlan1mon`）並且 `Mode:Monitor`，說明切換成功了。

---

### 第六步：測試封包注入

```bash
sudo aireplay-ng --test wlan1mon
```

`wlan1mon` 換成你第五步裡看到的實際介面名稱。能看到 `Injection is working!` 說明網卡工作正常。測試失敗的話，重新開機再試一次。Pi 上最常見的原因是 USB 集線器沒有獨立供電，確認一下。

---

## 虛擬機 USB 直通 {#virtual-machine-usb-passthrough}

在 macOS 或 Windows 的虛擬機裡跑 Kali Linux？需要把 USB 網卡直通給虛擬機。

### VirtualBox

1. 關閉虛擬機，進入 **Settings → USB**。
2. 啟用 **USB 3.0 (xHCI) Controller**。
3. 點 **+** 新增 USB 篩選器。
4. 選擇 **Realtek 802.11ac NIC [...]**（ID: 0bda:8812）。
5. 啟動虛擬機，網卡就出現在 Kali 裡了。

進虛擬機後跑 `lsusb` 確認 `0bda:8812` 出現，然後按上面的 Kali Linux 步驟繼續。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. 啟動虛擬機。
2. 選單選 **Virtual Machine → USB & Bluetooth**。
3. 找到 **Realtek 802.11ac NIC**，點 **Connect**。
4. 網卡從主機端斷開，進入虛擬機。

在虛擬機裡跑 `lsusb` 確認後，按 Kali Linux 步驟操作。

### 關於 VIF（虛擬介面）

RTL8812AU 晶片在 Linux 上的 VIF 支援有限制。同一張網卡不能同時可靠地跑管理模式和監聽模式（或 AP 模式）。

如果你需要同時掛多個虛擬介面，例如一邊開假 AP 一邊監聽，AWUS036ACH 不適合這個需求。可以看看 [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)，那款網卡用的是 MT7612U 晶片，核心原生支援 VIF，不需要打補丁。

---

## 故障排查

| 問題 | 可能原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 裡沒有 0bda:8812 | 網卡沒通電或連接線有問題 | 換個 USB 埠試試。樹莓派必須用有源集線器。 |
| `make` 報標頭檔錯誤 | 核心標頭檔缺失或版本不對 | 跑 `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` 失敗 | Secure Boot 攔截了未簽署的模組 | 在 BIOS 裡關掉 Secure Boot，或者給模組簽署 |
| 核心更新後驅動消失 | 驅動沒註冊到 DKMS | 在原始碼目錄重新跑 `sudo dkms install rtl8812au/$(cat VERSION)` |
| `airmon-ng start wlan0` 失敗 | NetworkManager 還在執行 | 先跑 `sudo airmon-ng check kill` |
| 監聽模式開了但抓不到流量 | 頻道不對或介面名用錯了 | 用 `iwconfig` 檢查介面。手動設頻道：`iwconfig wlan0mon channel 6` |
| 注入測試顯示 "No Answer" | AP 太遠，或用錯了介面名 | 靠近 AP。用 `wlan0mon` 而不是 `wlan0` |

## 國內鏡像速查

本文用到的所有資源，不需要 GitHub：

| 資源 | 網址 | 用途 |
|------|------|------|
| Alfa 官方驅動 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驅動套件、韌體 |
| Alfa 文件 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 產品手冊 |
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推薦） |
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推薦） |
| 華為雲鏡像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 映像（備用） |
| RTL8812AU 驅動（Gitee） | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | 手動編譯備選 |

## 更多 Alfa 網卡中國安裝指南

這是 **Alfa 中國安裝全攻略**系列的一部分，每篇文章對應一個型號：

- AWUS036ACH ← 你在這裡
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/) — MT7612U，最佳 VIF 支援
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

有問題？在下面留言，或者來 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
