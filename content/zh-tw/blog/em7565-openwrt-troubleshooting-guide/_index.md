---
title: "EM7565 在 OpenWrt／樹莓派上抓不到？QMI／MBIM 除錯完整指南"
description: "EM7565 在 OpenWrt 或樹莓派上抓不到、QMI port 消失？這篇除錯指南帶你從 lsusb、dmesg 查到 USB composition，再到驅動載入與 EM7565 設定步驟，輕鬆排除硬體與軟體連線問題。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/zh-tw/products/sierra/em7565/"
faq:
  - question: "EM7565 在 OpenWrt 上抓不到，最常見的原因是什麼？"
    answer: "最常見的是供電不足（VCC 不在 3.135 至 4.4V 內）導致 lsusb 看不到，或是 USB composition 設定錯誤沒有打開 QMI 介面。"
  - question: "EM7565 反覆重置、卡住不開機，是壞了嗎？"
    answer: "不一定。它有 SED 保護機制，連續 6 次不正常重啟後會進入保護狀態，重新下載韌體即可恢復。"
---

你的 EM7565 在 OpenWrt 或樹莓派上死活抓不到嗎？先別急著換模組。這篇文章幫你整理了官方規格書裡的除錯流程：從 USB 硬體層面確認有沒有上線，檢查 USB composition，載入正確的 Linux 驅動，排除系統服務干擾，以及處理棘手的韌體 SED 狀態。照著這五個步驟做，幫你快速找出問題癥結點！

{{< tldr >}}
EM7565 抓不到時照這五步查：1. 用 `lsusb` 確認 USB 層級（檢查供電與轉接板）。2. 確認 QMI/MBIM 介面與 `/dev/cdc-wdm0` 是否存在，檢查 `qmi_wwan` / `cdc_mbim` 驅動與 USB composition。3. 停用 `ModemManager` 排除系統服務干擾。4. 確認供電時序（上電 100ms 內勿驅動訊號，漣波上限 100mVp-p）。5. 確認韌體狀態：連續 6 次開機失敗會進入 SED 保護，需重新下載韌體。原則：先硬體、再軟體、最後韌體。
{{< /tldr >}}

**EM7565 是一顆基於 Qualcomm MDM9250 的 M.2 WWAN Type 3042-S3-B 4G LTE-Advanced 模組。它同時支援 QMI 與 MBIM 兩種 USB 介面。** 如果它在 OpenWrt 或樹莓派上「抓不到」，通常是三個地方出錯：USB 沒通電、USB composition 停在錯誤的組合，或是 Linux 驅動沒正確載入。偶爾它還會因為連續重啟進入保護模式。這篇文章我們照著 Sierra Wireless 的官方手冊，幫大家整理出一套最不容易出錯的排查流程。

> 產品連結：[Yupitek Sierra Wireless 專區](https://yupitek.com/zh-tw/products/sierra/)

## 快速結論：EM7565 抓不到時，照這五步查

大家在除錯的時候最常犯的錯就是：一上來就急著刷韌體。**先確認硬體再動軟體，最後才搞韌體。**

1. **確認 USB 層級**：打個 `lsusb` 看看有沒有模組。沒有的話，先檢查供電（VCC 要在 3.135 至 4.4V）、轉接板跟 USB 線。
2. **確認 QMI／MBIM 介面**：`lsusb` 看到了，卻沒有 `/dev/cdc-wdm0`？查一下 `qmi_wwan` / `cdc_mbim` 驅動有沒有載入，以及 USB composition 是不是只開了純診斷模式。
3. **確認系統服務**：有時候是系統的 `ModemManager` 把模組佔用了。
4. **確認供電時序**：上電後至少 100ms 內不要驅動任何訊號，而且電源漣波上限是 100mVp-p，電壓不穩會讓 USB 一直斷線重連。
5. **確認韌體狀態**：如果模組連續 6 次開機失敗重置，它會進入 SED（Smart Error Detection）保護狀態，這時候就需要重新下載韌體了。

## 認識 EM7565：它是一顆什麼樣的模組？

在開始除錯前，我們先快速過一下 EM7565 的底細。這是一顆需要外接三支天線（Main、GNSS、Aux）的 M.2 模組，不含天線。

| 項目 | 官方規格（Doc# 41110788，Rev 8） |
|---|---|
| **晶片** | Qualcomm MDM9250 |
| **封裝尺寸** | M.2 (3042-S3-B) / 42 × 30 mm，厚度最高 1.50mm，重量 6.5g |
| **下載峰值** | Cat 12 (3CA, 256QAM) 最高 600 Mbps |
| **上傳峰值** | Cat 13 (2CA, 64QAM) 最高 150 Mbps |
| **LTE 頻段** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66（註：B42/B43/B48 當時列為 disabled，待法規核准） |
| **通訊介面** | USB 2.0 與 USB 3.0；QMI / MBIM / AT 指令 |
| **供電電壓** | VCC 3.135V(min) / 3.3V(typ) / 4.4V(max)，漣波 ≤ 100mVp-p |
| **工作溫度** | 建議內部溫度保持在 <90°C（最好 <80°C） |

## 步驟一：從 USB 層級開始查

這台機器到底有沒有「看見」這個硬體？

```bash
lsusb
```

如果出現 Sierra Wireless 或 1199 開頭的設備，恭喜，硬體連上了。如果看不到：

- 請檢查電源：EM7565 瞬間開機電流可以達到 2.2A 至 2.5A（最大電流 1.5A）。很多樹莓派的 USB 轉接盒根本推不動它。
- 給它一點時間：插上去之後等個 10 秒，讓 USB 慢慢跑完流程。

接著看核心日誌：

```bash
dmesg | tail -50
```

如果你看到 `qmi_wwan` 掛載出 `/dev/cdc-wdm0`，代表它已經準備好連線了。

## 步驟二：檢查 USB composition

如果 `lsusb` 看得到模組，卻沒有 `/dev/cdc-wdm0` 跑出來，可能是模組把 QMI/MBIM 通道關起來了。模組裡面有一個叫做 USB composition 的設定，決定它要露出哪些通道。

這時候你需要用 `AT!USBCOMP?` 指令去查。如果你隨便亂切換，很可能會把通道全部搞丟，所以切換前請先記下原本的參數，並去查閱官方的 AT 指令手冊（Doc#41111748）。

## 步驟三：排除 ModemManager 干擾

在桌機版 Linux 或樹莓派上，有個叫 `ModemManager` 的內建服務會「雞婆」地把 4G 模組搶走。當它搶走控制權後，你自己打 `qmicli` 指令就會卡住。

手動除錯的時候，先把這傢伙關掉：

```bash
sudo systemctl stop ModemManager
```

等你確定模組都沒問題了，再來決定要手動撥號，還是把它交還給 ModemManager。

## 步驟四：韌體是不是鎖死了？（SED 保護機制）

如果你發現模組開機後無限重啟，那它可能已經進入了 **SED（Smart Error Detection）** 狀態。

官方規格書寫得很清楚：只要開機不久後連續發生 6 次重置，模組就會停在 bootloader 裡面裝死，等你重新把韌體刷進去。這通常是因為你的電源太不穩（電壓狂掉）造成的。

這時候不要以為模組壞了，換個好一點的電源，然後用官方工具重刷韌體就能救回來。

## QMI 怎麼撥號上網？（OpenWrt 範例）

當你搞定上面那些問題，`/dev/cdc-wdm0` 出現後，在 OpenWrt 撥號其實超簡單。

1. 裝好必備套件：

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. 到 `/etc/config/network` 設定你的 APN（以電信商為準）：

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. 重啟網路：

```bash
/etc/init.d/network restart
```

這樣 `wwan0` 介面就會出現，開開心心上網去了。

## 總結

EM7565 在 OpenWrt 或樹莓派上抓不到，其實就跟修電腦一樣，順序對了就很快：

1. **看硬體**：`lsusb` 跟電壓穩不穩。
2. **看介面**：USB composition 對不對。
3. **看軟體**：驅動有沒有裝，ModemManager 有沒有打架。
4. **看韌體**：是不是重啟太多次把自己鎖起來了。

只要不一上來就亂刷韌體，大部份問題都能在十分鐘內找出原因！

## 採購資訊（Call To Action）

不確定手上的轉接板、天線能不能配 EM7565？Yupitek（榆閤科技）有提供 Sierra Wireless 全系列產品跟完整的硬體整合方案。

歡迎來信：**sales@yupitek.com**

看看產品：[EM7565 產品頁面](https://yupitek.com/zh-tw/products/sierra/em7565/)
