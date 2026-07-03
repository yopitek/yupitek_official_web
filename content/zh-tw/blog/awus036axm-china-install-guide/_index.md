---
title: "ALFA AWUS036AXM 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
description: "專為國內用戶準備的 ALFA AWUS036AXM 安裝教程。使用國內鏡像源，涵蓋 MT7921AUN WiFi 6E 驅動配置，支持監聽模式和 VIF。適用於 Kali Linux, Ubuntu, Debian 以及樹莓派。無需訪問 GitHub。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "驅動", "中國", "監聽模式", "wifi6e", "vif"]
categories: ["驅動安裝指南"]
series: ["alfa-china-install-guide"]
related_product: "/zh-tw/products/alfa/awus036axm/"
series_order: 6
featureimage: "/images/blog/awus036axm-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036AXM 用什麼晶片？支援 WiFi 6E 嗎？"
    answer: "採用 MediaTek MT7921AUN 晶片，支援 WiFi 6E 三頻段（2.4G/5G/6G Hz）。"
  - question: "AWUS036AXM 的驅動需要手動安裝嗎？"
    answer: "不需要，mt7921u 驅動自 Linux 核心 5.18 起已內建，僅需安裝韌體套件。"
  - question: "AWUS036AXM 支援 VIF 虛擬介面嗎？"
    answer: "支援，MT7921AUN 完整支援核心原生 VIF，可同時連網與監聽封包。"
  - question: "Ubuntu 22.04 安裝 AWUS036AXM 為什麼驅動載入失敗？"
    answer: "Ubuntu 22.04 預設核心 5.15 太舊，需安裝 HWE 核心升級至 5.18 以上。"
  - question: "AWUS036AXM 的 USB ID 是多少？"
    answer: "MediaTek MT7921AUN 的 USB ID 為 0e8d:7961，用 lsusb 可確認。"
---

ALFA AWUS036AXM 搭載 MT7921AUN 晶片支援 WiFi 6E，驅動自核心 5.18 內建，僅需安裝韌體套件即可支援監聽模式與 VIF。

{{< tldr >}}
AWUS036AXM 採用 MT7921AUN 晶片支援 WiFi 6E，驅動核心內建，安裝韌體套件後即可使用監聽模式、封包注入與 VIF 功能。
{{< /tldr >}}

想體驗 WiFi 6E 的飆速快感？AWUS036AXM 是個非常硬核的選擇，而且它那節省空間的 L 型接口設計真的很貼心，完全不會擋到筆電相鄰的 USB 埠。

它的 MT7921AUN 晶片其實已經內建在 5.18 以上版本的 Linux 核心裡了，但國內的小夥伴在實際使用時，往往會卡在「韌體下載」這一步。這份指南將帶你避開所有網路坑，全程使用國內鏡像源，手把手教你搞定監聽模式、封包注入以及超強大的 VIF 功能。

## 開始前的準備

在動手折騰之前，請確保你手邊有：

1. **ALFA AWUS036AXM** 網卡本人
2. **有源 USB 集線器 (Hub)** —— 如果你用的是樹莓派，這步非常關鍵，因為這張網卡功耗較大
3. 暢通的網路（用來存取國內鏡像源）

插好網卡，我們先看看系統有沒有認到它。打開終端機輸入：

```bash
lsusb
```

在輸出中找找看有沒有這一行：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

只要看到 `0e8d:7961` 就妥當了。接著，根據你的系統選擇對應的章節。

## 你的系統是哪一個？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 (Raspberry Pi) 4B / 5](#raspberry-pi-4b--5)

如果是老司機已經裝好驅動了，可以直接跳轉到：
- [開啟監聽模式](#enable-monitor-mode)
- [測試封包注入](#test-packet-injection)
- [虛擬接口 (VIF) 高級玩法](#virtual-interface-vif)
- [虛擬機 USB 直通避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

好消息是，MT7921AUN 的驅動已經內建在 Kali 核心裡了。咱們只需要把 MediaTek 的韌體包裝好，它就能動起來。

### 1. 先換個「快車道」（切換國內鏡像）

為了下載不卡頓，我們先把系統源換成中科大的鏡像源。

```bash
sudo nano /etc/apt/sources.list
```

貼上這行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 儲存，**Enter** 確認，再按 **Ctrl+X** 離開。接著跑一下更新：

```bash
sudo apt update
```

---

### 2. 安裝韌體 (Firmware)

這步非常關鍵，沒有這些韌體檔，驅動雖然加載了，網卡還是動不了的。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 3. 檢查成果

重啟回來後，驗證一下網卡有沒有乖乖上線：

```bash
lsmod | grep mt7921
iwconfig
```

看到 `mt7921u` 模組和 `wlan0` 或 `wlan1` 接口就算成功了。

---

### 4. 開啟監聽模式 {#enable-monitor-mode}

這是安全研究最關鍵的一步。

```bash
# 殺掉干擾行程
sudo airmon-ng check kill
# 切換模式
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

再用 `iwconfig` 瞧瞧，看到 `Mode:Monitor` 了嗎？

---

## Ubuntu 22.04 / 24.04

### 如果你是 Ubuntu 24.04 (Noble) — 躺平模式

24.04 核心已經原生支援。換個阿里雲鏡像，裝好韌體就搞定了：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 將 URIs 換成阿里雲：http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

### 如果你是 Ubuntu 22.04 (Jammy) — 需要升級核心

Ubuntu 22.04 預設的 5.15 核心太老了，帶不動這張網卡，咱們得換成 HWE 核心。

```bash
# 換成阿里雲
sudo nano /etc/apt/sources.list
# deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse

sudo apt update
sudo apt install -y linux-generic-hwe-22.04 linux-firmware
sudo reboot
```

重啟後下 `uname -r`，看到核心版本大於 5.18 就可以照前面的步驟玩了。

---

## Debian

### 1. 換成清華大學鏡像

```bash
sudo nano /etc/apt/sources.list
# 貼上這行：deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware

sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

之後的操作和 Kali 是一模一樣的。

---

## 樹莓派 (Raspberry Pi) 4B / 5

> **特別提醒：** AXM 在高負載下功耗不小，樹莓派用戶請務必配合 **有源 USB Hub** 使用。

建議直接刷 Kali ARM64 版本（選 64 位版本）。
國內鏡像下載：[華為雲 Kali 鏡像](https://repo.huaweicloud.com/kali-images/)。

```bash
# 換源並安裝韌體
sudo nano /etc/apt/sources.list
# 換成中科大：deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware

sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

## 虛擬機 USB 直通避坑指南 {#virtual-machine-usb-passthrough}

### VirtualBox
1. 先關掉虛擬機，進 **Settings -> USB**。
2. 勾選 **USB 3.0 (xHCI) 控制器**。
3. 點選 **+** 圖示，選擇 **MediaTek Inc. (ID: 0e8d:7961)**。

### VMware
1. 在頂部選單選 **虛擬機 -> USB 與藍牙**。
2. 找到 **MediaTek MT7921AUN**，點選 **連接**。

---

## 虛擬接口 (VIF) 高級玩法 {#virtual-interface-vif}

AXM 的 MT7921AUN 晶片對 VIF 支援得極致完美。你可以一邊連著 WiFi 上網，一邊開著監聽接口抓包，互不干擾！

### 1. 在連網的同時開啟監聽

```bash
# 建立一個新的虛擬接口 mon0
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
# 現在你就可以用 mon0 抓包了，而 wlan0 還能繼續正常上網
sudo airodump-ng mon0
```

### 2. Fake AP + 監聽（同時開三個接口也沒問題）

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 故障排查「救火站」

| 遇到的麻煩 | 可能的原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 刷不出網卡 | 沒插好或供电不足 | 換個埠試試，樹莓派務必加有源 Hub |
| `lsmod` 看不到 mt7921u | 韌體沒裝或核心太老 | 跑一遍韌體安裝命令，Ubuntu 22.04 記得升核心 |
| 封包注入測試顯示 "No Answer" | AP 太遠或接口選錯 | 湊近點，確認用的是正確的接口名稱 |
| 無法建立 VIF 接口 | 驅動沒加載好 | 試試重啟，或者手動 `modprobe mt7921u` |

## 國內鏡像速查表

| 資源名稱 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推薦 |
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 推薦 |

{{< faq >}}

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- AWUS036AXM ← 你在這裡
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

折騰過程中遇到搞不定的？歡迎在下面留言，或者到 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。

## 參考來源

1. [Linux Kernel mt7921 驅動](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng 官方文件](https://www.aircrack-ng.org/)
3. [ALFA Network 官網](https://www.alfa.com.tw/)
4. [Kali Linux 官方文件](https://www.kali.org/docs/)
