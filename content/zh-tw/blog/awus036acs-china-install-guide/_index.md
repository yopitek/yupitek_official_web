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
series: ["alfa-china-install-guide"]
related_product: "/zh-tw/products/alfa/awus036acs/"
series_order: 3
featureimage: "/images/blog/awus036acs-china-install-guide.webp"
---

剛拿到這台輕巧的 AWUS036ACS，興沖沖插上去結果 Linux 一點反應都沒有？別擔心，這再正常不過了。雖然它內建的 RTL8811AU 晶片是安全研究的神器，完美支援監聽模式與封包注入，但驅動程式並不在系統核心裡，得靠咱們動手裝一下。

考慮到大家在國內存取 GitHub 可能會卡卡的，我特別找好了 Gitee 鏡像，不用翻牆，跟著我一步步把它「馴服」吧！

## 開始前的準備

在動手折騰之前，先確認你手邊有這些東西：

1. **ALFA AWUS036ACS** 網卡本人
2. 能存取國內鏡像的網路環境（用來下載包）

插好網卡，我們先看看系統有沒有認到它。打開終端機輸入：

```bash
lsusb
```

如果你在輸出中看到這一行：

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

只要看到 `0bda:0811` 就妥當了。接著，請根據你的系統選擇對應的章節。

## 你的系統是哪一個？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 (Raspberry Pi) 4B / 5](#raspberry-pi-4b--5)

如果你是老司機已經裝好驅動了，可以直接跳轉到：

- [開啟監聽模式](#enable-monitor-mode)
- [測試封包注入](#test-packet-injection)
- [虛擬機 USB 直通避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 1. 先換個「快車道」（切換國內鏡像）

為了下載不卡頓，我們先把系統換成中科大的鏡像源。

```bash
sudo nano /etc/apt/sources.list
```

把裡面的內容刪掉，換成這行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 儲存，**Enter** 確認，再按 **Ctrl+X** 離開。接著讓系統重新整理一下：

```bash
sudo apt update
```

---

### 2. 安裝驅動程式

在 Kali 裡，安裝驅動其實很簡單：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

裝完之後，驗證一下驅動有沒有乖乖上線：

```bash
modinfo 88XXau | grep version
```

---

### 3. 開啟監聽模式 {#enable-monitor-mode}

這是最關鍵的一步，把網卡切換到「監聽」狀態：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

確認看到 `wlan0mon` 出現，就代表你成功了！

---

## Ubuntu 22.04 / 24.04

### 1. 切換國內鏡像源（阿里雲）

Ubuntu 24.04 使用 `ubuntu.sources`，22.04 則使用 `sources.list`。換好鏡像後記得跑 `sudo apt update`。

### 2. 安裝編譯必備套件

我們先幫驅動準備好「手術台」：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### 3. 從 Gitee 下載驅動原始碼

既然 GitHub 連不上，咱們改走 Gitee 鏡像：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
```

> **溫馨提示：** RTL8811AU 與 RTL8812AU 是共用同一個驅動程式套件的喔。

### 4. 編譯與安裝

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

## Debian

### 1. 換成清華大學鏡像

```bash
sudo nano /etc/apt/sources.list
```

貼上這幾行（適用於 Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

跑一下更新：`sudo apt update`。

### 2. 安裝步驟

接下來的編譯步驟跟 Ubuntu 是一模一樣的，照著上面的「第三步」和「第四步」操作即可。

---

## 樹莓派 (Raspberry Pi) 4B / 5

建議直接刷 Kali ARM64 版本，省去很多麻煩。

```bash
sudo apt update
sudo apt install -y realtek-rtl88xxau-dkms
```

如果 `apt` 找不到套件，請參考上面的「Ubuntu」章節進行原始碼編譯。

---

## 虛擬機 USB 直通避坑指南 {#virtual-machine-usb-passthrough}

很多小夥伴卡在虛擬機找不到網卡，通常是因為這幾步沒設定好：

### VirtualBox
1. 先關掉虛擬機。
2. **Settings → USB** → 勾選 **USB 3.0 (xHCI)**。
3. 點選右邊的 **+** 圖示，選擇 **Realtek (ID: 0bda:0811)**。
4. 啟動後，進系統下 `lsusb` 檢查。

---

## 故障排查「救火站」

| 遇到的麻煩 | 可能的原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 沒反應 | 沒插好或線材問題 | 換個 USB 埠試試，或者直接插主板後方 |
| 驅動裝了但沒訊號 | 需要重新啟動 | 跑一下 `sudo reboot` 看看 |
| 監聽模式開不了 | 被其他行程佔用了 | 務必先執行 `sudo airmon-ng check kill` |

## 國內鏡像速查表

| 資源名稱 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推薦 |
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 推薦 |

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- AWUS036ACS ← 你在這裡
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

折騰過程中遇到搞不定的？歡迎在下面留言，或者到 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
