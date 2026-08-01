---
title: "Ubuntu / Debian / Linux Mint 安裝 Sierra 4G/5G 模組完整教學：EM7455、EM7565、EM919x、MC7455 設定與 GNSS 定位"
description: "在 Ubuntu/Debian/Linux Mint 上怎麼安裝 Sierra 4G/5G 模組？這篇教學帶你裝好 ModemManager、使用 qmicli/mbimcli 撥號連線，並且設定 GNSS 定位。涵蓋 EM7455、EM7565、EM919x、MC7455。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/zh-tw/products/sierra/"
faq:
  - question: "Ubuntu 可以直接用 Sierra 4G/5G 模組上網嗎？"
    answer: "可以。只要安裝 modemmanager、libqmi-utils 等套件，用 NetworkManager 填入 APN 就能上網。"
  - question: "Sierra 模組在 Linux 下怎麼開 GNSS 定位？"
    answer: "使用 ModemManager 指令：先 mmcli -m 0 --location-enable-gps-raw，再用 --location-get 抓取座標。請確定 GNSS 天線有接好。"
---

想在 Ubuntu、Debian 或 Linux Mint 上安裝 Sierra Wireless 的模組（EM7455、EM7565、MC7455、EM919x）嗎？其實 Linux 原生就支援這些設備，只要你知道怎麼安裝對的軟體包（像是 ModemManager 跟 libqmi-utils）。這篇文章從硬體怎麼接、驅動怎麼裝、怎麼撥號上網，一路講到怎麼把 GNSS 定位功能開起來。不管你是要做無人機還是工業電腦，照著做準沒錯。

{{< tldr >}}
想在 Ubuntu、Debian 或 Linux Mint 上安裝 Sierra Wireless 的模組（EM7455、EM7565、MC7455、EM919x）嗎？其實 Linux 原生就支援這些設備，只要安裝對的軟體包（ModemManager 跟 libqmi-utils）。從硬體怎麼接、驅動怎麼裝、怎麼撥號上網，一路講到怎麼把 GNSS 定位功能開起來。不管你是要做無人機還是工業電腦，照著做準沒錯。
{{< /tldr >}}

**一句話總結：在 Linux 裝這些 Sierra 模組超簡單。只要用 `apt` 裝好 `modemmanager` 跟相關工具，就能用 NetworkManager 連上網路，甚至連 GPS 定位都能輕鬆讀出來！**

很多人拿到 EM7455、EM7565、EM919x 或 MC7455，插上主機板後卻不知道怎麼設定上網。其實，這些模組在 Linux 裡的支援度非常成熟。它們都是透過 USB，用 QMI 或是 MBIM 協定在溝通。接下來我們就一步步帶你把它們設定好。

> 規格數字與技術依據皆來自 Sierra Wireless 官方規格書。本文由榆閤科技（Yupitek）整理。

---

## 動手前：先看懂你手上的硬體

硬體沒搞對，軟體再怎麼打指令都沒用。

| 模組 | 封裝插槽 | 速度等級 | Linux 主流通訊協定 | 天線數量 |
|---|---|---|---|---|
| **EM7455** | M.2 (長 42mm) | Cat 6 (300/50 Mbps) | QMI | 3 個 (Main, GNSS, Aux) |
| **EM7565** | M.2 (長 42mm) | Cat 12 (600/150 Mbps) | QMI / MBIM | 3 個 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (長 **52mm**) | 5G NR / LTE Cat 20 | MBPW 等寬頻套件 | 4 個以上 |
| **MC7455** | mPCIe (舊型插槽) | Cat 6 (300/50 Mbps) | QMI | 3 個 U.FL 接頭 |

**兩個硬體防呆重點：**
1. **EM919x 比較長**：它是 52mm 長，不要硬塞進 42mm 的孔位裡，會弄壞板子。
2. **沒有天線 = 沒訊號**：至少要把主天線（Main）接上。如果要玩定位，一定要買一根 GPS 天線接在 **GNSS 接頭** 上。

---

## 步驟一：安裝 Linux 必備工具

在 Ubuntu / Debian / Linux Mint 裡面，你不用自己寫扣編譯驅動，套件庫都幫你準備好了。

打開終端機，敲這兩行：
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
裝完之後，確認服務有跑起來：
```bash
systemctl status ModemManager
```
有了這幾個工具，你的 Linux 就能看得懂這張 4G/5G 網卡了。

---

## 步驟二：確認系統有抓到網卡

把網卡插好、開機後，用下面三個指令檢查：

1. **查 USB 硬體：**
   ```bash
   lsusb
   ```
   （應該要看到 Sierra 或 Qualcomm 相關的裝置）

2. **查核心驅動：**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   （看到 `cdc-wdm0` 跟 `wwan0` 就是成功掛載了）

3. **查 ModemManager 狀態：**
   ```bash
   mmcli -L
   ```
   （會列出一串數據機的名字跟編號，記下這個編號，通常是 `0`）

---

## 步驟三：超簡單的撥號連線（用 NetworkManager）

如果你用的是桌面版的 Ubuntu 或 Mint，用系統內建的網路管理工具最方便。

```bash
# 新增一個連線（把 "internet" 換成你電信商的 APN）
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# 啟動它！
nmcli connection up mobile
```
就這麼簡單！你可以用 `ip addr show` 看看 `wwan0` 有沒有拿到 IP。

### （進階）沒有桌面環境的純文字連線法
如果是無頭伺服器（headless server）或嵌入式板子，你可以直接用 `qmicli` 下指令：
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## 步驟四：把 GPS 定位功能開起來！

這幾顆模組都有內建強大的 GNSS 定位系統（支援 GPS、GLONASS 等）。
根據官方規格：
- EM7455 / EM7565 / MC7455：熱啟動 1秒、冷啟動 32秒。水平精準度大約在 2~5 公尺內。
- 5G 的 EM919x：冷啟動更快（≤28秒），精準度也略為提升（<4m 95%）。

**要在 Linux 抓座標，這樣做最快：**

1. 啟用 GPS 功能：
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. 抓取目前座標：
```bash
mmcli -m 0 --location-get
```
畫面就會噴出目前的經緯度囉！如果要即時串流給其他程式用，可以搭配 `gpsd` 服用。

---

## 常見的踩坑與急救

1. **`mmcli -L` 什麼都沒顯示**：可能是 `ModemManager` 當掉了，或者你的 USB 供電根本推不動網卡。
2. **GPS 定位一直失敗**：你是不是把 GPS 天線插到 Main 或 Aux 上了？GNSS 有自己專屬的洞！
3. **EM919x 速度上不去**：它是 5G 網卡，支援 USB 3.1 Gen 2 甚至 PCIe Gen 3。如果你把它插在 USB 2.0 的孔，官方是不保證效能的。

## 結論

在 Linux 上玩 Sierra 模組，其實沒有想像中難。確認好硬體插槽跟天線，裝上 `modemmanager` 家族的套件，再設定一下 APN 就能愉快上網了。這套流程非常適合要做邊緣運算（Edge Computing）或是工業物聯網（IIoT）的工程師們！

## 採購資訊（Call To Action）

想要把 Sierra 模組整合進你的 Ubuntu 設備裡嗎？Yupitek（榆閤科技）有提供完整的模組、天線、轉接板方案，並且能提供你第一線的技術支援。
歡迎來信：**sales@yupitek.com**
看看產品：[Sierra Wireless 系列](https://yupitek.com/zh-tw/products/sierra/)

{{< faq >}}
