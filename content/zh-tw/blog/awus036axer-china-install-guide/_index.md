---
title: "ALFA AWUS036AXER 中國安裝全攻略：Kali Linux / Ubuntu / Debian / 樹莓派"
description: "手把手教你在中國網路環境下安裝 ALFA AWUS036AXER 驅動，編譯工具使用國內鏡像，驅動原始碼取自 GitHub。RTL8832BU 晶片，WiFi 6 迷你網卡。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "驅動", "中國", "wifi6", "rtl8832bu"]
categories: ["驅動安裝指南"]
series: ["alfa-china-install-guide"]
related_product: "/zh-tw/products/alfa/awus036axer/"
series_order: 5
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036AXER 用什麼晶片？跟 AWUS036AX 一樣嗎？"
    answer: "同樣採用 Realtek RTL8832BU 晶片，支援 WiFi 6，但體積更小更便攜。"
  - question: "AWUS036AXER 在 Ubuntu 24.04 上需要安裝驅動嗎？"
    answer: "需要。RTL8832BU 不在 Ubuntu 24.04 核心中，請透過 DKMS 編譯一次社群版 rtl8852bu 驅動（morrownr/rtl8852bu-20250826），之後核心更新時會自動重新編譯。"
  - question: "AWUS036AXER 適合做無線安全研究嗎？"
    answer: "不適合。社群版 rtl8852bu 驅動不支援 Monitor mode 與封包注入，建議改用核心內建 MediaTek 驅動的 AWUS036ACM。"
  - question: "AWUS036AXER 的 USB ID 是多少？"
    answer: "Realtek RTL8832BU 的廠商 ID 為 0bda，產品 ID 依機種為 8832 或 885a，請用 lsusb 確認你手上的裝置。"
  - question: "在中國安裝 AWUS036AXER 需要翻牆嗎？"
    answer: "不一定。從已驗證的 GitHub 儲存庫（morrownr/rtl8852bu-20250826）下載驅動原始碼；若 GitHub 速度較慢，請使用你信任的代理或鏡像。編譯工具仍可用國內鏡像安裝。"
---

AWUS036AXER 的 RTL8832BU 晶片沒有 Linux 核心內建驅動，因此在所有發行版（包括 Ubuntu 24.04）上都需要透過 DKMS 編譯一次社群版 rtl8852bu 驅動。驅動原始碼從已驗證的 GitHub 儲存庫下載；若 GitHub 速度較慢，請使用你信任的代理或鏡像。此驅動不支援 Monitor mode。

{{< tldr >}}
AWUS036AXER 採用 RTL8832BU 晶片，支援 WiFi 6。驅動不在核心中：所有發行版（包括 Ubuntu 24.04）都需要透過 DKMS 編譯 rtl8852bu。不支援 Monitor mode。
{{< /tldr >}}

剛拿到這台輕巧迷你、方便攜帶的 AWUS036AXER，插上去結果 Linux 一點反應都沒有？別擔心，這再正常不過了。

考慮到大家在國內存取 GitHub 可能比較慢，這份指南的驅動原始碼取自已驗證的 GitHub 儲存庫；若速度不佳，請使用你信任的代理或鏡像。咱們現在就開始吧！

> **資安研究提示：** 社群版 rtl8852bu 驅動不支援 Monitor mode 與封包注入。做資安研究請改用核心內建 MediaTek 驅動的網卡，例如 [AWUS036ACM](/zh-tw/blog/awus036acm-china-install-guide/)。

## 開始前的準備

1. **ALFA AWUS036AXER** 網卡本人
2. 能存取國內鏡像的網路環境

插好網卡，我們先確認系統有沒有認到它。打開終端機輸入：

```bash
lsusb
```

在輸出中找找看有沒有類似這樣的一行（以下為範例輸出；廠商 ID 一律是 `0bda`，產品 ID 依機種為 `8832` 或 `885a`）：

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

只要看到廠商 ID 為 `0bda`（產品 ID 為 `8832` 或 `885a`）就沒問題了。接著，根據你的系統選擇對應的章節。

## 你的系統是哪一個？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 (Raspberry Pi) 4B / 5](#raspberry-pi-4b--5)

如果是老手已經裝好驅動了，可以直接跳轉到：
- [虛擬機 USB 直通避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 1. 先換個「快車道」（切換國內鏡像）

為了下載不卡頓，我們先把系統源換成中科大的鏡像源。

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

> **注意：** 維護中的上游驅動為 [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)。如果 GitHub 速度較慢，請使用你信任的代理或鏡像。你也可以從 [files.alfa.com.tw](https://files.alfa.com.tw) 下載壓縮檔。

---

### 4. 正式安裝並重新啟動

```bash
sudo ./install-driver.sh
sudo reboot
```

重新開機後，可用 `lsmod | grep 8852bu` 與 `iwconfig` 確認驅動已載入。

### 5. 開啟監聽模式 {#enable-monitor-mode}

> **不支援：** RTL8832BU 的社群版 rtl8852bu 驅動不支援 Monitor mode，這裡沒有可執行的指令。如需 Monitor mode，請改用核心內建 MediaTek 驅動的網卡，例如 [AWUS036ACM](/zh-tw/blog/awus036acm-china-install-guide/)。

### 6. 測試封包注入 {#test-packet-injection}

> **不支援：** 封包注入依賴 Monitor mode，而此驅動不提供 Monitor mode。請使用 [AWUS036ACM](/zh-tw/blog/awus036acm-china-install-guide/)（核心內建 MediaTek 驅動）進行注入測試。

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
sudo nano /etc/apt/sources.list
# deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
# deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
# deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

此驅動不支援 Monitor mode（見 Kali 第 5 步）。

---

## 樹莓派 (Raspberry Pi) 4B / 5

先切換到國內鏡像：

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## 虛擬機 USB 直通避坑指南 {#virtual-machine-usb-passthrough}

很多朋友卡在虛擬機找不到網卡，通常是因為這幾步沒設定好：

### VirtualBox
1. 先關掉虛擬機。
2. **設定 → USB** → 勾選 **USB 3.0 (xHCI)**。
3. 點選右邊的 **+** 圖示，選擇 **Realtek (廠商 ID：0bda，產品 ID：8832 或 885a)**。

### VMware
1. 在頂部選單選 **虛擬機 -> USB 與藍牙**。
2. 找到 **Realtek RTL8832BU**，點選 **連接**。

---

## 故障排查「救火站」

| 遇到的麻煩 | 可能的原因 | 解決方法 |
|------|----------|----------|
| `lsusb` 沒顯示 0bda:8832 或 0bda:885a | 未偵測到網卡 | 換個 USB 埠試試 |
| `install-driver.sh` 報錯 | 缺少核心標頭檔 | 跑一下 `sudo apt install linux-headers-$(uname -r)` |
| GitHub 下載失敗或很慢 | 網路問題 | 使用你信任的代理或鏡像 |
| `modprobe 8852bu` 失敗 | 驅動尚未編譯或未載入 | 重新執行 `sudo ./install-driver.sh`，用 `sudo dkms status` 檢查後重新開機 |
| Monitor mode／封包注入無法使用 | rtl8852bu 驅動不支援 | 做滲透測試請改用 AWUS036ACM |

> **關於 VIF：** RTL8832BU 的核心外驅動不支援虛擬介面（VIF）。

## 國內鏡像速查表

| 資源名稱 | 網址 | 用途 |
|------|------|------|
| 清華大學鏡像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 華為雲鏡像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | 驅動原始碼 |

{{< faq >}}

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/)
- AWUS036AXER ← 你在這裡
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安裝指南](/zh-tw/blog/awus036eacs-china-install-guide/)

折騰過程中遇到搞不定的？歡迎在下面留言，或者到 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。

## 參考來源

1. [Realtek 官方網站](https://www.realtek.com/)
2. [ALFA Network 官網](https://www.alfa.com.tw/)
3. [Kali Linux 官方文件](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
