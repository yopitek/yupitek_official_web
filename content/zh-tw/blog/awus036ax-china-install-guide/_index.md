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
series: ["Alfa 中國安裝全攻略"]
related_product: "/zh-tw/products/alfa/awus036ax/"
---

剛拿到 AWUS036AX，插上去 Linux 沒反應？正常。這張網卡用的是 RTL8832BU 晶片，在核心 6.14 以下需要手動安裝驅動。好在 Ubuntu 24.04 已經內建，其他系統我們用 Gitee 鏡像也能搞定。

## 開始之前

1. **ALFA AWUS036AX** 網卡
2. USB 3.0 連接線
3. 能存取國內鏡像的網路

插好網卡，確認系統認到了：

```bash
lsusb
```

找這一行：

```
Bus 001 Device 003: ID 0bda:8832 Realtek Semiconductor Corp.
```

## 選擇你的系統

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### 第一步：切換國內鏡像源

```bash
sudo nano /etc/apt/sources.list
```

貼上這行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### 第二步：安裝編譯相依套件

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### 第三步：從 Gitee 下載驅動原始碼

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

### 第四步：編譯並安裝

```bash
sudo ./install-driver.sh
sudo reboot
```

驗證驅動：

```bash
lsmod | grep 88x2bu
iwconfig
```

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 核心內建

24.04 核心較新，通常插上就能用。先換個阿里雲鏡像：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```bash
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

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 虛擬機 USB 直通 {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Settings → USB** → 啟用 **USB 3.0 (xHCI)**。
2. 新增篩選器：**Realtek** (ID: 0bda:8832)。

---

## 故障排查

| 問題 | 可能原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 沒反應 | 供電不足 | 換個 USB 3.0 埠試試 |
| `install-driver.sh` 報錯 | 缺少標頭檔 | `sudo apt install linux-headers-$(uname -r)` |
| 監聽模式不穩定 | 晶片限制 | 此型號主打 WiFi 6 高速上網，監聽模式支援較弱 |

## 國內鏡像速查

| 资源 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | 驅動原始碼 |

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)
- AWUS036AX ← 你在這裡
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

有問題？在下面留言，或者來 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
