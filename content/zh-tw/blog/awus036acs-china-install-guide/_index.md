---
title: "ALFA AWUS036ACS 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
description: "手把手教你在中國網路環境下安裝 ALFA AWUS036ACS 驅動，全程使用國內鏡像，無需翻牆。RTL8811AU 晶片，支援監聽模式與封包注入。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "驅動", "中國", "monitor-mode", "rtl8811au"]
categories: ["驅動安裝指南"]
series: ["Alfa 中國安裝全攻略"]
related_product: "/zh-tw/products/alfa/awus036acs/"
---

剛拿到 AWUS036ACS，插上去 Linux 沒反應？正常。這張網卡用的是 RTL8811AU 晶片，驅動不是開箱即用的。這款網卡雖然小，但支援監聽模式和封包注入，性價比極高。整個安裝過程約 15 分鐘，全程用國內鏡像。

## 開始之前

1. **ALFA AWUS036ACS** 網卡
2. 能存取國內鏡像的網路

插好網卡，確認系統認到了：

```bash
lsusb
```

找這一行：

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
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

### 第二步：安裝驅動

Kali 的套件庫裡就有驅動：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

驗證驅動：

```bash
modinfo 88XXau | grep version
```

### 第三步：開啟監聽模式 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

確認看到 `wlan0mon` 即表示成功。

---

## Ubuntu 22.04 / 24.04

### 第一步：切換國內鏡像源（阿里雲）

Ubuntu 24.04 使用 `ubuntu.sources`，22.04 使用 `sources.list`。請根據系統選擇。

### 第二步：安裝編譯相依套件

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 第三步：從 Gitee 下載驅動原始碼

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
```

> **注意：** RTL8811AU 與 RTL8812AU 使用相同的驅動套件。

### 第四步：編譯並安裝

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

貼上清華大學源：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
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

## Raspberry Pi 4B / 5

```bash
sudo apt update
sudo apt install -y realtek-rtl88xxau-dkms
```

如果 `apt` 找不到，請參考上面的原始碼編譯步驟。

---

## 虛擬機 USB 直通 {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Settings → USB** → 啟用 **USB 3.0 (xHCI)**。
2. 新增篩選器：**Realtek** (ID: 0bda:0811)。

---

## 故障排查

| 問題 | 可能原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 沒反應 | 沒插好 | 換個埠試試 |
| 驅動裝了但沒訊號 | 需要重新啟動 | `sudo reboot` |
| 監聽模式開不了 | 行程佔用 | 跑 `sudo airmon-ng check kill` |

## 国内镜像速查

| 资源 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- AWUS036ACS ← 你在這裡
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

有問題？在下面留言，或者來 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
