---
title: "樹莓派 + OpenWrt 打造 4G/5G 路由器：Sierra 模組完整支援矩陣與實作教學"
description: "用樹莓派加 Sierra Wireless 4G/5G 模組（EM7455、EM7565、EM7511、EM919x、MC7455）自製 OpenWrt 路由器。完整支援矩陣、QMI/MBIM 設定、wwan0 上網教學，含供電與天線注意事項，幫你搞定硬體到軟體的疑難雜症。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/zh-tw/products/sierra/"
faq:
  - question: "樹莓派上做 OpenWrt 路由器，Sierra 模組該選哪顆？"
    answer: "新手建議選教學多的 EM7455；要高上傳選 EM7565/EM7511；要 5G 選 EM919x；舊設備 mPCIe 選 MC7455。"
  - question: "QMI 跟 MBIM 差在哪？"
    answer: "QMI 是 Qualcomm 的協定，MBIM 是後續的標準協定。在 OpenWrt 上兩者都能用，但網路教學以 QMI 居多。"
  - question: "樹莓派抓不到模組怎麼辦？"
    answer: "通常是樹莓派 USB 供電不足（需應付 2.5A 突波電流），建議檢查轉接板供電、線材，並等待十秒讓設備完整開機。"
---

樹莓派能不能拿 Sierra Wireless 的 4G/5G 模組直接做成 OpenWrt 路由器？答案是肯定的。EM7455、EM7565、EM7511、EM919x 這些 M.2 模組，在 Linux 系統裡早就是原生可用的乖寶寶。只要裝好 `kmod-usb-net-qmi-wwan` 或 `kmod-usb-net-cdc-mbim` 套件，設定一下 `wwan0`，就能輕鬆上網。這篇文章整理了完整的模組支援矩陣、設定步驟、供電天線等避坑指南，帶你輕鬆動手做！

{{< tldr >}}
用樹莓派加 Sierra 4G/5G 模組當路由器完全可行。多數 M.2 模組（EM7455、EM7565、EM7511）走 USB 介面，EM919x 多一個 PCIe Gen3 通道，MC7455 是 mPCIe 版本的 EM7455。OpenWrt 上最推薦用 QMI 協定加 `wwan0`：裝好 `kmod-usb-net-qmi-wwan`、`uqmi`、`luci-proto-qmi`，在 `/etc/config/network` 設定 APN 後重啟網路即可連線。速度上：EM7455 / MC7455 是 LTE Cat 6（300/50 Mbps），EM7565 / EM7511 是 Cat 12（600/150 Mbps），EM919x 提供 5G Sub-6（EM9190 支援 mmWave）。
{{< /tldr >}}

## Sierra 模組在 OpenWrt 的完整支援矩陣

動手之前，先來對照一下你手邊的模組規格：

| 型號 | 速度等級 | 基頻晶片 | 封裝形式 | Linux 資料通道 | GNSS 衛星定位 |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM（Linux 皆支援） | 多了 QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | 多了 QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6（9190 有 mmWave） | SDX55 | M.2（長度 52mm） | Windows/Linux 皆支援 | L1 + L5（選配） |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50.95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### 該怎麼挑型號？

- **新手村 Maker**：選 **EM7455**，教學多，出錯最好找解答。
- **需要高上傳（開直播、監控）**：選 **EM7565** 或 **EM7511**，上傳高達 150 Mbps。
- **就是要 5G**：選 **EM9190** 體驗 5G 網速。
- **只有舊的 mPCIe 槽**：那就乖乖買 **MC7455**。

## 硬體該怎麼接？三種接法一次看懂

### A. Raspberry Pi 5 + M.2 HAT（走 PCIe）

Pi 5 有 PCIe，加個 M.2 HAT+ 擴充板就能直接插 M.2 WWAN 模組（記得確認是 B-Key）。

### B. Raspberry Pi 4B 或更舊 + USB WWAN 轉接盒

因為 EM 系列模組也支援 USB 2.0/3.0，買個 M.2 轉 USB 的盒子（裡面通常有 SIM 卡座）插到樹莓派的 USB 孔上就好，這是最平易近人的做法。

### C. MC7455（mPCIe）轉接

這顆是舊的 mPCIe 介面，必須買 mPCIe 轉 USB 或轉 M.2 的板子。

> ⚠️ **供電大魔王**：模組吃 3.135 至 4.4 V（一般 3.3V）。「抓不到模組」通常是因為樹莓派 USB 供電不足！瞬間電流可能會飆到 2.5A，所以電源的推力一定要抓寬裕一點。

## 搞懂 QMI 跟 MBIM 協定

這兩個都是控制 4G/5G 模組上網的協定：

- **QMI**：Qualcomm 自己搞的協定，Linux/OpenWrt 上的教學大多是用這個（網卡叫 `wwan0`）。
- **MBIM**：後來標準化的協定，Windows 跟 Linux 都能用（網卡也叫 `wwan0`）。

**選哪個？** 大部分人直接用 QMI 就好。如果你的韌體特別要求 MBIM，再換成 MBIM。

## 實戰 Part 1：在 OpenWrt 設定 QMI 上網

只要四個步驟，不用自己編譯任何東西。

### 1. 裝好套件

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. 確定樹莓派有抓到模組

```bash
lsusb                                  # 看看有沒有 Sierra 裝置
ls /dev/cdc-wdm*                       # QMI 的控制通道
dmesg | grep qmi_wwan                  # 看看驅動有沒有載入
ip link show wwan0                     # 看看有沒有出現網卡
```

### 3. 設定網路檔（`/etc/config/network`）

加一段 QMI 的設定，記得把 APN 改成你電信商的：

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option auth 'none'
```

### 4. 重新啟動網路

```bash
/etc/init.d/network restart
ifup wwan
```

搞定！`wwan0` 拿到 IP 後就能上網了。

## 天線跟 SIM 卡：千萬別漏掉

模組本身**沒有**內建天線！天線的好壞直接決定了你的網速。

- **主天線（Main）**：一定要接。
- **輔助天線（Aux）**：接了才能跑到 MIMO 高速，不接網速打折扣。
- **GNSS 天線**：要玩定位才接，別跟主天線搞混了。

## 常見踩坑清單（新手必看）

1. **`lsusb` 看不到東西**：99% 是供電不足、轉接板沒接好或線壞了。
2. **太心急**：模組插上去要時間開機，等個 10 秒再敲指令。
3. **5G 模組（EM919x）太熱**：5G 模組溫度高達 100 度都很常見（極限 115°C），記得幫它散熱。
4. **樹莓派 ModemManager 打架**：如果在原生 Linux 上手動打指令，記得先把 `ModemManager` 關掉（`systemctl stop ModemManager`），免得控制權被搶走。

## 總結

用樹莓派加 OpenWrt 來驅動 Sierra 模組，其實就是照表操課。先確認硬體規格（封裝、電壓、天線），再到系統裝好 QMI/MBIM 相關驅動，最後設好 APN。希望這篇教學能幫你的專案少走一點彎路，順利讓你的樹莓派飆上 4G/5G 網路！

## 採購資訊（Call To Action）

如果你需要購買 EM7455、EM7565、EM7511 等模組，或是想找搭配的 M.2 轉接板跟天線，Yupitek（榆閤科技）有提供完整的硬體方案跟技術諮詢。

歡迎來信：**sales@yupitek.com**

產品傳送門：[Yupitek Sierra Wireless 全系列](https://yupitek.com/zh-tw/products/sierra/)
