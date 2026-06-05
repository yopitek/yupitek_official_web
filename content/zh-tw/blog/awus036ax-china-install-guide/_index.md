---
title: "ALFA AWUS036AX 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
description: "手把手教你在中國網路環境下安裝 ALFA AWUS036AX 驅動，全程使用國內鏡像，無需翻牆。RTL8832BU 晶片，支援 WiFi 6 高速網路。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "驅動", "中國", "wifi6", "rtl8832bu"]
categories: ["驅動安裝指南"]
series: ["alfa-china-install-guide"]
related_product: "/zh-tw/products/alfa/awus036ax/"
series_order: 4
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
---

想在 Linux 上體驗 WiFi 6 的飆速快感？剛拿到這台 AWUS036AX，插上去發現沒反應？別擔心，這很正常。因為它採用的 RTL8832BU 晶片在較舊的核心版本上需要手動安裝驅動。不過有個好消息：如果你是用 Ubuntu 24.04，驅動已經內建好了，插上就能直接起飛。

考慮到國內存取 GitHub 不太方便，這份指南全程會帶大家使用 Gitee 鏡像，不用翻牆也能輕鬆搞定。咱們現在就開始吧！

> **安全研究避坑指南：** 雖然這張網卡速度很快，但 RTL8832BU 的監聽模式支援有限。如果你是為了 Kali Linux 深度滲透和封包注入而來，我更推薦你參考 [AWUS036ACM](/zh-tw/blog/awus036acm-china-install-guide/) 或 [AWUS036ACH](/zh-tw/blog/awus036ach-china-install-guide/)。

## 開始前的準備

1. **ALFA AWUS036AX** 網卡本人
2. 隨附的 USB 3.0 連接線
3. 能存取國內鏡像的網路

插好網卡，我們先確認系統有沒有認到它。打開終端機輸入：

```bash
lsusb
```

在輸出中找找看有沒有這一行：

```
Bus 001 Device 003: ID 0bda:8832 Realtek Semiconductor Corp.
```

只要看到 `0bda:8832` 就沒問題了。接著，根據你的系統選擇對應的章節。

## 你的系統是哪一個？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 (Raspberry Pi) 4B / 5](#raspberry-pi-4b--5)

如果是老司機已經裝好驅動了，可以直接跳轉到：
- [虛擬機 USB 直通避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 1. 先換個「快車道」（切換國內鏡像）

為了下載不卡頓，我們先把系統源換成中科大的。

```bash
sudo nano /etc/apt/sources.list
```

貼上這行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 儲存，**Enter** 確認，再按 **Ctrl+X** 離開。然後跑一下更新：

```bash
sudo apt update
```

---

### 2. 安裝編譯相依套件

我們先幫驅動準備好「手術台」：

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### 3. 從 Gitee 下載驅動原始碼

既然 GitHub 連不上，咱們改走 Gitee 鏡像：

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

---

### 4. 正式安裝並重新啟動

```bash
sudo ./install-driver.sh
sudo reboot
```

重啟回來後，驗證一下網卡有沒有乖乖上線：

```bash
lsmod | grep 88x2bu
iwconfig
```

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 內建驅動，插上即用

24.04 核心已經原生支援，插上通常就能用了。建議換個阿里雲鏡像讓下載更快：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 將 URIs 改為 http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo modprobe 88x2bu
iwconfig
```

---

### Ubuntu 22.04 (Jammy) — 需要手動安裝

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

### 1. 換成清華大學鏡像

```bash
sudo nano /etc/apt/sources.list
# 貼上這行：deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware

sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 虛擬機 USB 直通避坑指南 {#virtual-machine-usb-passthrough}

很多小夥伴卡在虛擬機找不到網卡，通常是因為這幾步沒設定好：

### VirtualBox
1. 先關掉虛擬機。
2. **Settings → USB** → 勾選 **USB 3.0 (xHCI)**。
3. 點選右邊的 **+** 圖示，選擇 **Realtek (ID: 0bda:8832)**。

### VMware
1. 在頂部選單選 **虛擬機 -> USB 與藍牙**。
2. 找到 **Realtek RTL8832BU**，點選 **連接**。

---

## 故障排查「救火站」

| 遇到的麻煩 | 可能的原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 沒反應 | 供電不足 | 換個 USB 3.0 埠（藍色的）試試，或者插在主板後方 |
| `install-driver.sh` 報錯 | 缺少核心標頭檔 | 跑一下 `sudo apt install linux-headers-$(uname -r)` |
| 監聽模式不穩定 | 晶片限制 | 此型號主打 WiFi 6 高速上網，監聽模式支援較弱 |

## 國內鏡像速查表

| 資源名稱 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推薦 |
| rtl8852bu (Gitee) | [Gitee 鏡像](https://gitee.com/mirrors/rtl8852bu) | 驅動原始碼 |

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)
- AWUS036AX ← 你在這裡
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

折騰過程中遇到搞不定的？歡迎在下面留言，或者到 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
