---
title: "ALFA AWUS036EACS 中國安裝指南：Windows 與 Linux 使用說明"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "驅動", "中國", "bluetooth", "rtl8821cu"]
categories: ["驅動指南"]
series: ["alfa-china-install-guide"]
description: "手把手教你在中國境內安裝 ALFA AWUS036EACS。這款納米網路卡在 Windows 下表現極佳；在 Linux 核心 6.2+ 下已由內建的 rtw88_8821cu 驅動支援，免編譯、插上即用，監聽與注入實測可用。"
related_product: "/zh-tw/products/alfa/awus036eacs/"
series_order: 8
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036EACS 用什麼晶片？支援藍牙嗎？"
    answer: "採用 Realtek RTL8821CU 晶片，支援 WiFi 5 與藍牙 4.2。"
  - question: "AWUS036EACS 適合在 Linux 上使用嗎？"
    answer: "適合。Linux 核心 6.2 以上（例如 Ubuntu 24.04 HWE / kernel 6.17）已內建 rtw88_8821cu 驅動，免編譯、插上即用；實測 Monitor mode 與封包注入兩頻（2.4G / 5G）100%，並可端到端擷取 WPA .22000，藍牙亦實測可用。"
  - question: "AWUS036EACS 在 Windows 上怎麼安裝驅動？"
    answer: "從 Alfa 官網 files.alfa.com.tw 下載 Windows 驅動包，以管理員身份安裝後重啟即可。"
  - question: "AWUS036EACS 的藍牙怎麼開啟？"
    answer: "安裝驅動後通常自動啟用，在 Windows 設定中開啟藍牙開關即可連接設備。"
  - question: "如果需要 Linux 上的無線安全研究網路卡，該選哪款？"
    answer: "AWUS036EACS 本身在核心 6.2+ 下即可用於監聽與封包注入，還內建藍牙。若想要更多選擇，AWUS036ACM 或 AWUS036ACS 同樣在 Linux 上完整支援監聽模式。僅限自有或已授權的網路。"
---

ALFA AWUS036EACS 是搭載 RTL8821CU 晶片的迷你 WiFi 5 加藍牙 4.2 網路卡，在 Windows 上安裝簡單；在 Linux 核心 6.2+ 下也由內建的 rtw88_8821cu 驅動支援，免編譯、插上即用。

{{< tldr >}}
AWUS036EACS 採用 RTL8821CU 晶片，WiFi 5 加藍牙 4.2 迷你網路卡，Windows 安裝簡單；Linux 核心 6.2+ 已內建 rtw88_8821cu 驅動，免編譯，Monitor 與封包注入實測可用，藍牙也實測可用。
{{< /tldr >}}

AWUS036EACS 是 ALFA 家族中最迷你的成員之一，它不僅有 WiFi 5，還內建了藍牙 4.2。它非常適合那些想給老筆電升級，但又不想要個大天線在外面晃的人。它不只在 Windows 上很好用，在 Linux 核心 6.2+ 上也由內建的 rtw88_8821cu 驅動支援，插上即用。

## Linux 使用者看這裡：核心 6.2+ 即插即用

> **AWUS036EACS 在 Linux 核心 6.2+ 上即插即用。** 核心 6.2 以上（例如 Ubuntu 24.04 HWE / kernel 6.17）已內建 rtw88_8821cu 驅動，免編譯；實測 Monitor mode 與封包注入兩頻（2.4G / 5G）100%，並可端到端擷取 WPA .22000；藍牙（BT）也實測可用（BR/EDR + BLE 均可掃到裝置，並與 WiFi 共存）。僅限自有或已授權的網路。
>
> **操作提醒：** 這是 BT+WiFi 複合卡，反覆切換模式後 WiFi 接收可能卡住（`ip link set up` 回 `Operation already in progress`、`iw ... set channel` 回 `-16 busy`）。每個測試階段開始前，把網路卡拔下換一個 USB 孔重插即可恢復。
>
> 同系列其他 Linux 網路卡：
> - **[AWUS036ACM 中國安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)** — MT7612U 核心內建，支援 VIF
> - **[AWUS036ACS 中國安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)** — RTL8811AU，監聽模式

---

## Windows 10 / 11 安裝步驟

在 Windows 下，這款網路卡表現非常出色。

### 第一步：下載驅動

中國境內訪問 Alfa 官網驅動庫是沒問題的：

[https://files.alfa.com.tw](https://files.alfa.com.tw)

進去後找 **AWUS036EACS** 資料夾，下載最新的 Windows 驅動包（一般是 `.zip` 或 `.exe`）。

### 第二步：安裝

1. 解壓下載的壓縮包。
2. 右鍵點擊安裝程式，選擇「以系統管理員身分執行」。
3. 一路點「下一步」，最後重啟電腦。

### 第三步：確認狀態

右鍵點擊「此電腦」 -> 「管理」 -> 「設備管理器」 -> 「網路介面卡」。

你應該能看到：`Realtek 8821CU Wireless LAN 802.11ac USB NIC`。看到它，就說明你可以正常上網了。

---

## 藍牙如何開啟？

裝好驅動後，藍牙通常會自動啟用：

1. 開啟 Windows 的「設定」 -> 「藍牙和其他設備」。
2. 把藍牙開關推到「開」。
3. 現在你可以連接藍牙滑鼠、耳機或鍵盤了。

---

## 常見問題

| 現象 | 可能原因 | 解決辦法 |
|---------|-------------|-----|
| 網路卡搜不到 5G 訊號 | 頻道不匹配 | 嘗試在網路卡屬性裡把區域設為美國（US） |
| 藍牙連不上 | 驅動衝突 | 確認禁用電腦內建的板載藍牙 |

{{< faq >}}

## 更多 Alfa 網路卡指南

- [AWUS036ACH 中國安裝指南](/zh-tw/blog/awus036ach-china-install-guide/) — 經典大天線
- [AWUS036AX 中國安裝指南](/zh-tw/blog/awus036ax-china-install-guide/) — WiFi 6 新款

有問題？歡迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯繫我們。

## 參考來源

1. [ALFA Network 官網](https://www.alfa.com.tw/)
2. [Alfa 官方驅動下載](https://files.alfa.com.tw)
3. [Realtek 官方網站](https://www.realtek.com/)
