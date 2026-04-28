---
title: "ALFA AWUS036AXM 驅動程式 (driver) 安裝指南（中國區）：Kali Linux, Ubuntu, Debian 和樹莓派"
description: "專為國內用戶準備的 ALFA AWUS036AXM 驅動程式 (driver) 分步安裝教程。使用國內鏡像源，涵蓋 MT7921AUN WiFi 6E 內核驅動程式 (driver)，支持監聽模式 (monitor mode) 和 VIF。適用於 Kali Linux, Ubuntu, Debian 以及樹莓派。無需訪問 GitHub。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["驅動程式指南"]
series: ["Alfa 中國安裝指南"]
related_product: "/zh-tw/products/alfa/awus036axm/"
---

AWUS036AXM 是 ALFA 的 WiFi 6E 三頻適配器，配有節省空間的 L 型 USB-A 接口。它的 MT7921AUN 芯片使用 `mt7921u` 驅動程式 (driver)，自 5.18 版本起已內置於 Linux 內核中。L 型接口可以讓筆記本電腦上相鄰的 USB 端口保持空閒。本指南將帶你完成完整安裝——包括固件 (firmware)、驅動程式 (driver) 驗證、監聽模式 (monitor mode)、數據包注入 (packet injection) 和 VIF——全程無需訪問 GitHub。

## 開始之前

請確保你已準備好：

1. **ALFA AWUS036AXM** 適配器
2. 有源 USB 集線器（Hub）——如果你使用的是樹莓派，這是必須的
3. 能夠連接國內鏡像源的互聯網連接

插入適配器，然後確認系統識別到了它：

```bash
lsusb
```

在輸出中尋找這一行：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

如果你看到了 `0e8d:7961`，說明系統已檢測到適配器。請移步下方對應的操作系統部分。

如果沒看到，請嘗試換一個 USB-A 端口，然後再次運行 `lsusb`。

## 選擇你的操作系統

點擊跳轉到適合你系統的部分：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 (Raspberry Pi) 4B / 5](#raspberry-pi-4b--5)

已經安裝好了？直接跳轉到：

- [開啟監聽模式 (monitor mode)](#enable-monitor-mode)
- [測試數據包注入 (packet injection)](#test-packet-injection)
- [虛擬接口 (VIF)](#virtual-interface-vif)
- [虛擬機 USB 透傳](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7921AUN 的驅動程式 (driver) 已經包含在 Kali 內核中了。你只需要從國內鏡像源安裝 MediaTek 的固件 (firmware) 包即可。

### 第一步：切換到國內鏡像源

在終端中打開軟件源列表。

```bash
sudo nano /etc/apt/sources.list
```

刪除其中的所有內容，然後粘貼下面這一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：按 **Ctrl+O**，然後回車，最後按 **Ctrl+X** 退出。刷新軟件包索引。

```bash
sudo apt update
```

> **備用鏡像：** 如果中科大 (USTC) 速度較慢，可以改用清華大學鏡像：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安裝固件 (firmware)

MT7921AUN 需要來自 `firmware-misc-nonfree` 和 `linux-firmware` 的固件 (firmware) 文件。如果沒有這些文件，驅動程式 (driver) 雖然能加載，但適配器將無法初始化。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 第三步：驗證驅動程式 (driver)

重啟後，插入適配器並進行檢查。

```bash
lsmod | grep mt7921
```

你應該在輸出中看到 `mt7921u`。然後確認是否出現了無線接口。

```bash
iwconfig
```

尋找 `wlan0` 或 `wlan1`。如果出現了，說明驅動程式 (driver) 工作正常。

---

### 第四步：開啟監聽模式 (monitor mode) {#enable-monitor-mode}

先檢查接口名稱。

```bash
iwconfig
```

使用你看到的名稱（例如 `wlan1`）。殺掉干擾進程，然後切換到監聽模式 (monitor mode)。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

確認切換成功。

```bash
iwconfig
```

在對應的接口上尋找 `Mode:Monitor` 字樣。

---

### 第五步：測試數據包注入 (packet injection) {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

成功的結果如下：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

如果失敗了，請重啟系統再試一次。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 內核 6.8，即插即用

Ubuntu 24.04 搭載了 6.8 內核，原生支持 MT7921AUN 驅動程式 (driver)。

### 第一步：切換到國內鏡像源

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

刪除所有內容並粘貼：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

```bash
sudo apt update
```

### 第二步：安裝固件 (firmware)

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### 第三步：驗證並開啟監聽模式 (monitor mode)

重啟後，運行 `lsmod | grep mt7921` 確認驅動程式 (driver) 已加載，然後按照上方 Kali 的步驟（第四步）操作。

---

### Ubuntu 22.04 (Jammy) — 需要 HWE 內核

Ubuntu 22.04 默認搭載的是 5.15 內核。MT7921AUN 的驅動程式 (driver) 需要 5.18 或更高版本的內核。請先安裝 HWE 內核。

### 第一步：切換到國內鏡像源

```bash
sudo nano /etc/apt/sources.list
```

將所有行替換為：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

保存並退出（`Ctrl+O`，然後 `Ctrl+X`）。

```bash
sudo apt update
```

### 第二步：安裝 HWE 內核

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

重啟後，確認內核版本：

```bash
uname -r
```

你應該能看到 5.19 或更高版本。接著按照上文安裝固件 (firmware) 並開啟監聽模式 (monitor mode)。

### 第三步：安裝固件 (firmware)

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### 第一步：切換到國內鏡像源

```bash
sudo nano /etc/apt/sources.list
```

刪除所有內容並粘貼（針對 Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

```bash
sudo apt update
```

### 第二步：安裝固件 (firmware)

Debian 12 Bookworm 搭載的是 6.1 內核——完美兼容 MT7921AUN。

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### 第三步：驗證並開啟監聽模式 (monitor mode)

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 第四步：測試數據包注入 (packet injection)

```bash
sudo aireplay-ng --test wlan1
```

看到 `Injection is working!` 就說明你的適配器已經完全準備就緒了。

---

## 樹莓派 (Raspberry Pi) 4B / 5

> AWUS036AXM 在負載下功耗可達 2.7W。在樹莓派上使用時，請務必連接有源 USB 集線器。

### 第一步：下載 Kali Linux ARM64 鏡像

官方頁面：https://www.kali.org/get-kali/#kali-arm

選擇 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)** —— 必須使用 64 位版本。

> **國內鏡像：** https://repo.huaweicloud.com/kali-images/ —— 瀏覽到最新版本文件夾並下載 ARM64 鏡像。

### 第二步：燒錄到 MicroSD 卡

```bash
lsblk
# 將 /dev/sdX 替換為你實際的 SD 卡盤符
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

默認賬號密碼：**kali / kali**。

### 第三步：切換國內鏡像源並安裝固件 (firmware)

```bash
sudo nano /etc/apt/sources.list
```

替換為：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

然後運行：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### 第四步：驗證驅動程式 (driver)

```bash
lsmod | grep mt7921
```

應該會出現 `mt7921u`。

### 第五步：開啟監聽模式 (monitor mode)

在帶有內置 Wi-Fi 的樹莓派上，AWUS036AXM 通常顯示為 `wlan1`。

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 第六步：測試數據包注入 (packet injection)

```bash
sudo aireplay-ng --test wlan1
```

---

## 虛擬機 USB 透傳 {#virtual-machine-usb-passthrough}

### VirtualBox

1. 關閉虛擬機。進入 **設置 → USB**。
2. 啟用 **USB 3.0 (xHCI) 控制器**。
3. 點擊 **+** 圖標添加 USB 篩選器。
4. 選擇：**MediaTek Inc.** (ID: 0e8d:7961)。
5. 啟動虛擬機 —— 適配器就會出現在 Kali 中。

在虛擬機中運行 `lsusb` 確認看到 `0e8d:7961`，然後按照上文 Kali 的步驟操作。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. 啟動虛擬機。
2. 菜單：**虛擬機 → USB 和藍牙**。
3. 找到 **MediaTek MT7921AUN** 並點擊 **連接**。
4. 在虛擬機中運行 `lsusb` 確認，然後按照上文 Kali 的步驟操作。

---

## 虛擬接口 (VIF) {#virtual-interface-vif}

MT7921AUN 具有完美的內核原生 VIF 支持。你可以在同一個適配器上同時運行監聽接口和普通接口——無需任何補丁。

### 在普通模式旁創建一個監聽接口

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

你應該能看到 `wlan0`（普通模式）和 `mon0`（監聽模式）同時處於活動狀態。

### 在保持連接的同時進行監聽

```bash
sudo airodump-ng mon0
```

`wlan0` 保持連接，而 `mon0` 負責抓取範圍內的所有數據。

### Fake AP + 監聽

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> **關於 hostapd 的提示：** 完整的 AP 運行需要配置 `hostapd`。上述步驟僅確認適配器可以創建該接口——具體的 AP 配置是一個獨立的話題。

---

## 常見問題排查

| 現象 | 可能原因 | 解決方法 |
|---------|-------------|-----|
| `lsusb` 不顯示 0e8d:7961 | 適配器未通電或線纜不良 | 嘗試換一個 USB-A 端口。在樹莓派上請使用有源集線器。 |
| `lsmod` 不顯示 mt7921u | 未安裝固件 (firmware) 或內核版本過低 | 運行 `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` |
| Ubuntu 22.04 無法加載驅動程式 (driver) | 5.15 內核太舊了 | 安裝 HWE：`sudo apt install linux-generic-hwe-22.04` |
| 接口出現了但無法連接 | 缺少固件 (firmware) 文件 | 運行 `sudo apt install firmware-misc-nonfree` 然後重啟 |
| 切換監聽模式 (monitor mode) 失敗 | 接口仍處於開啟狀態 | 在執行 `iw dev` 命令前先運行 `sudo ip link set wlan1 down` |
| 注入測試顯示 "No Answer" | AP 太遠或接口選錯 | 靠近一些。使用 `iwconfig` 確認 `Mode:Monitor`。 |
| 創建 VIF 接口失敗 | 驅動程式 (driver) 未完全加載 | 拔掉適配器，然後運行：`sudo rmmod mt7921u && sudo modprobe mt7921u` |

## 中國區鏡像源參考

| 資源 | 網址 | 用途 |
|----------|-----|---------|
| Alfa 官方驅動程式 (driver) | [files.alfa.com.tw](https://files.alfa.com.tw) | 驅動包、固件 (firmware) |
| Alfa 文檔中心 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 產品手冊 |
| 清華大學鏡像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里雲鏡像站 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (推薦) |
| 中科大鏡像站 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (推薦) |
| 華為雲鏡像站 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 鏡像 (備用) |

## 更多針對中國區的 Alfa 適配器指南

這是 **Alfa 中國安裝指南** 系列文章的一部分：

- [AWUS036ACH 中國安裝指南](/zh-tw/blog/awus036ach-china-install-guide/) — RTL8812AU, 高功率
- [AWUS036ACM 中國安裝指南](/zh-tw/blog/awus036acm-china-install-guide/) — MT7612U, 完整 VIF 支持
- [AWUS036ACS 中國安裝指南](/zh-tw/blog/awus036acs-china-install-guide/) — RTL8811AU, 監聽模式 (monitor mode)
- [AWUS036AX 中國安裝指南](/zh-tw/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中國安裝指南](/zh-tw/blog/awus036axer-china-install-guide/) — RTL8832BU, 迷你型
- AWUS036AXM ← 你在這裡
- [AWUS036AXML 中國安裝指南](/zh-tw/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中國安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows 版

有問題？歡迎在下方留言，或通過 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯繫我們。
