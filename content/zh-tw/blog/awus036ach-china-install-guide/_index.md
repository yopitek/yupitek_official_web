---
title: "ALFA AWUS036ACH 中國安裝指南：Kali Linux, Ubuntu, Debian 和 樹莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "驅動", "中國", "監聽模式"]
categories: ["驅動指南"]
series: ["alfa-china-install-guide"]
description: "手把手教你在中國境內使用國內鏡像源安裝 ALFA AWUS036ACH 驅動。涵蓋 Kali Linux, Ubuntu 22/24, Debian 和 樹莓派。無需訪問 GitHub。"
related_product: "/zh-tw/products/alfa/awus036ach/"
series_order: 1
featureimage: "/images/blog/awus036ach-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACH 用什麼晶片？需要額外安裝驅動嗎？"
    answer: "AWUS036ACH 採用 Realtek RTL8812AU 晶片，驅動不在 Linux 核心內建，需要手動安裝。"
  - question: "在中國安裝 AWUS036ACH 驅動需要翻牆嗎？"
    answer: "不需要，全程使用中科大、阿里雲等國內鏡像及 Gitee 源碼鏡像即可完成安裝。"
  - question: "AWUS036ACH 支援監聽模式和封包注入嗎？"
    answer: "支援，安裝 RTL8812AU 驅動後用 airmon-ng 即可開啟監聽模式，aireplay-ng 可測試封包注入。"
  - question: "AWUS036ACH 在樹莓派上能用嗎？"
    answer: "可以，建議搭配帶供電的 USB Hub 並刷 Kali ARM64 版本使用。"
  - question: "Kali Linux 安裝 AWUS036ACH 驅動的指令是什麼？"
    answer: "Kali 可直接執行 sudo apt install realtek-rtl88xxau-dkms 安裝預編譯驅動。"
---

ALFA AWUS036ACH 搭載 RTL8812AU 晶片，在中國透過國內鏡像源安裝驅動即可支援監聽模式與封包注入，全程無需翻牆。

{{< tldr >}}
AWUS036ACH 採用 RTL8812AU 晶片，Kali 用 apt 裝 DKMS 驅動，Ubuntu/Debian 從 Gitee 編譯，30 分鐘完成監聽模式與封包注入。
{{< /tldr >}}

你剛拿到 ALFA AWUS036ACH，結果 Linux 系統沒反應？別擔心，這很正常。這款網卡用的晶片需要 RTL8812AU 驅動，而且它不是插上就能用的。本指南會帶你花大約 30 分鐘完成安裝，全程只用國內鏡像源，完全不需要翻牆去 GitHub。

## 在你開始之前

請準備好以下物品：

1. **ALFA AWUS036ACH** 網卡
2. USB 數據線（包裝盒裡那根就挺好）
3. 一個帶供電的 USB Hub —— 如果你用的是樹莓派，這很重要
4. 穩定的網路連接

插上網卡，先確認系統有沒有看到它：

```bash
lsusb
```

在輸出裡找這一行：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

只要看到 `0bda:8812`，就說明網卡被識別到了。接下來根據你的系統看下面的步驟。

## 選擇你的操作系統

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [樹莓派 4B / 5](#raspberry-pi-4b--5)

已經安裝好了？直接跳到：

- [開啟監聽模式](#enable-monitor-mode)
- [測試數據包注入](#test-packet-injection)

---

## Kali Linux

Kali 自帶了許多無線工具。裝好 AWUS036ACH 驅動只需要四步。先換到國內鏡像源，這樣下載速度才夠快。

### 第一步：切換到國內鏡像源

打開終端，編輯源列表：

```bash
sudo nano /etc/apt/sources.list
```

刪掉裡面的內容，粘貼這一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，回車，再按 **Ctrl+X** 退出。刷新一下：

```bash
sudo apt update
```

> **小貼士：** 如果中科大（USTC）比較慢，可以試試清華源：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安裝驅動

Kali 的軟體庫裡已經有了預編譯好的 DKMS 驅動。一行命令搞定：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS 的好處是，以後你更新內核時，驅動會自動重新編譯，不用你再動手。

裝完後確認驅動加載成功：

```bash
lsmod | grep 8812au
```

看到 `8812au` 就對了。

---

### 第三步：開啟監聽模式 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

用 `iwconfig` 確認一下，你應該能看到 `wlan1mon`，模式是 `Monitor`。

---

### 第四步：測試數據包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

看到 `Injection is working!` 說明你已經完全準備好了。

---

## Ubuntu 22.04 / 24.04

Ubuntu 不像 Kali 那樣自帶驅動，我們需要手動編譯。

### 第一步：換到阿里雲鏡像

#### Ubuntu 24.04

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

把地址換成：`http://mirrors.aliyun.com/ubuntu/`

#### Ubuntu 22.04

```bash
sudo nano /etc/apt/sources.list
```

把所有的 `archive.ubuntu.com` 換成 `mirrors.aliyun.com`。

然後刷新：

```bash
sudo apt update
```

### 第二步：安裝編譯工具

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

### 第三步：從 Gitee 下載驅動

國內訪問 GitHub 慢，我們用 Gitee 鏡像：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
sudo ./install-driver.sh
sudo reboot
```

重啟後，網卡應該就能正常工作了。

---

## 常見問題

| 現象 | 可能原因 | 解決辦法 |
|---------|-------------|-----|
| `lsusb` 看不到設備 | 線沒插好或供電不足 | 換個 USB 口或用帶供電的 Hub |
| 安裝驅動報錯 | 缺內核頭文件 | 運行 `sudo apt install linux-headers-$(uname -r)` |

## 國內鏡像站參考

| 資源 | 地址 | 用途 |
|----------|-----|---------|
| 中科大鏡像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 首選 |
| 阿里雲鏡像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 首選 |
| Gitee | [gitee.com](https://gitee.com) | 驅動源碼 |

{{< faq >}}

## 更多 Alfa 網卡中國指南

- [AWUS036ACM 中國安裝指南](/zh-tw/blog/awus036acm-china-install-guide/) — MT7612U，免驅首選
- [AWUS036ACS 中國安裝指南](/zh-tw/blog/awus036acs-china-install-guide/) — RTL8811AU
- [AWUS036AXM 中國安裝指南](/zh-tw/blog/awus036axm-china-install-guide/) — WiFi 6E

有問題？歡迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯繫我們。

## 參考來源

1. [aircrack-ng 官方文件](https://www.aircrack-ng.org/)
2. [ALFA Network 官網](https://www.alfa.com.tw/)
3. [Kali Linux 官方文件](https://www.kali.org/docs/)
4. [Gitee rtl8812au 鏡像](https://gitee.com/mirrors/rtl8812au)
5. [Realtek RTL8812AU 驅動](https://www.realtek.com/)
