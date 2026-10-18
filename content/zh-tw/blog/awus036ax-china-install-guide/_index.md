---
title: "ALFA AWUS036AX 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
description: "手把手教你在中國網路環境下安裝 ALFA AWUS036AX 驅動，編譯工具使用國內鏡像，驅動原始碼取自 GitHub。RTL8832BU 晶片，支援 WiFi 6 高速網路。"
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
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036AX 用什麼晶片？支援 WiFi 6 嗎？"
    answer: "採用 Realtek RTL8832BU 晶片，支援 WiFi 6 (802.11ax) 高速網路。"
  - question: "AWUS036AX 在 Ubuntu 24.04 上需要安裝驅動嗎？"
    answer: "需要。RTL8832BU 不在 Ubuntu 24.04 核心中，請透過 DKMS 編譯一次社群版 rtl8852bu 驅動（morrownr/rtl8852bu-20250826），之後核心更新時會自動重新編譯。"
  - question: "AWUS036AX 適合做無線安全研究嗎？"
    answer: "不適合。社群版 rtl8852bu 驅動不支援 Monitor mode 與封包注入，建議改用核心內建 MediaTek 驅動的 AWUS036ACM。"
  - question: "在中國安裝 AWUS036AX 需要翻牆嗎？"
    answer: "不一定。從已驗證的 GitHub 儲存庫（morrownr/rtl8852bu-20250826）下載驅動原始碼；若 GitHub 速度較慢，請使用你信任的代理或鏡像。編譯工具仍可用國內鏡像安裝。"
  - question: "AWUS036AX 的 USB ID 是多少？"
    answer: "Realtek RTL8832BU 的廠商 ID 為 0bda，產品 ID 依機種為 8832 或 885a，請用 lsusb 確認你手上的裝置。"
---

AWUS036AX 的 RTL8832BU 晶片沒有 Linux 核心內建驅動，因此在所有發行版（包括 Ubuntu 24.04）上都需要透過 DKMS 編譯一次社群版 rtl8852bu 驅動。驅動原始碼從已驗證的 GitHub 儲存庫下載；若 GitHub 速度較慢，請使用你信任的代理或鏡像。此驅動不支援 Monitor mode。

{{< tldr >}}
AWUS036AX 採用 RTL8832BU 晶片，支援 WiFi 6。驅動不在核心中：所有發行版（包括 Ubuntu 24.04）都需要透過 DKMS 編譯 rtl8852bu。不支援 Monitor mode。
{{< /tldr >}}

想在 Linux 上體驗 WiFi 6 的飆速快感？剛拿到這台 AWUS036AX，插上去發現沒反應？別擔心，這很正常。

考慮到國內存取 GitHub 可能比較慢，這份指南的驅動原始碼取自已驗證的 GitHub 儲存庫；若速度不佳，請使用你信任的代理或鏡像。咱們現在就開始吧！

> **資安研究提示：** 社群版 rtl8852bu 驅動不支援 Monitor mode 與封包注入。做資安研究請改用核心內建 MediaTek 驅動的網卡，例如 [AWUS036ACM](/zh-tw/blog/awus036acm-china-install-guide/)。

## 開始前的準備

1. **ALFA AWUS036AX** 網卡本人
2. 隨附的 USB 3.0 連接線
3. 能存取國內鏡像的網路

插好網卡，我們先確認系統有沒有認到它。打開終端機輸入：

```bash
lsusb
```

在輸出中找找看有沒有類似這樣的一行（以下為範例輸出；廠商 ID 一律是 `0bda`，產品 ID 依機種為 `8832` 或 `885a`）：

```
Bus 001 Device 003: ID 0bda:8832 Realtek Semiconductor Corp.
```

只要看到廠商 ID 為 `0bda`（產品 ID 為 `8832` 或 `885a`）就沒問題了。接著，根據你的系統選擇對應的章節。

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

### 3. 從 GitHub 下載驅動原始碼

GitHub 較慢時，請先使用你信任的代理或鏡像，再複製驅動原始碼：

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

---

### 4. 正式安裝並重新啟動

```bash
sudo ./install-driver.sh
sudo reboot
```

重啟回來後，驗證一下網卡有沒有乖乖上線：

```bash
lsmod | grep 8852bu
iwconfig
```

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 需要 DKMS

Ubuntu 24.04（核心 6.8）並未內建 RTL8832BU 的驅動。先換成國內鏡像源，再依下方 Ubuntu 22.04 的方式編譯驅動。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 將 URIs 改為 http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

重新開機後執行 `sudo modprobe 8852bu` 與 `iwconfig`。如果模組成功載入並出現網卡介面，就完成了（僅支援 Managed 模式，不支援 Monitor mode）。

---

### Ubuntu 22.04 (Jammy) — 需要手動安裝

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## 虛擬機 USB 直通避坑指南 {#virtual-machine-usb-passthrough}

很多小夥伴卡在虛擬機找不到網卡，通常是因為這幾步沒設定好：

### VirtualBox
1. 先關掉虛擬機。
2. **Settings → USB** → 勾選 **USB 3.0 (xHCI)**。
3. 點選右邊的 **+** 圖示，選擇 **Realtek (廠商 ID：0bda，產品 ID：8832 或 885a)**。

### VMware
1. 在頂部選單選 **虛擬機 -> USB 與藍牙**。
2. 找到 **Realtek RTL8832BU**，點選 **連接**。

---

## 故障排查「救火站」

| 遇到的麻煩 | 可能的原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 沒反應 | 供電不足 | 換個 USB 3.0 埠（藍色的）試試，或者插在主板後方 |
| `install-driver.sh` 報錯 | 缺少核心標頭檔 | 跑一下 `sudo apt install linux-headers-$(uname -r)` |
| Monitor mode／封包注入無法使用 | rtl8852bu 驅動不支援 | 做滲透測試請改用 AWUS036ACM |

## 國內鏡像速查表

| 資源名稱 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推薦 |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | 驅動原始碼 |

{{< faq >}}

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

## 參考來源

1. [Realtek 官方網站](https://www.realtek.com/)
2. [ALFA Network 官網](https://www.alfa.com.tw/)
3. [Kali Linux 官方文件](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
