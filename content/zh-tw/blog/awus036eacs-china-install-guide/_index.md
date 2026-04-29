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
description: "手把手教你在中國境內安裝 ALFA AWUS036EACS。這款納米網卡在 Windows 下表現極佳，但在 Linux 下有一定局限性，請務必閱讀本指南再開始。"
related_product: "/zh-tw/products/alfa/awus036eacs/"
series_order: 8
---

AWUS036EACS 是 ALFA 家族中最迷你的成員之一，它不僅有 WiFi 5，還自帶了藍牙 4.2。它非常適合那些想給老筆電升級，但又不想要個大天線在外面晃的人。不過，買之前你要搞清楚一件事：它在 Windows 上很好用，但在 Linux（特別是 Kali）上並不推薦。

## Linux 用戶請注意！

> **AWUS036EACS 在 Kali Linux、Ubuntu 或樹莓派上工作並不穩定。** 它的晶片組 RTL8821CU 沒有被良好維護的 Linux 驅動，開啟監聽模式（monitor mode）非常困難且容易報錯。
>
> 如果你需要做無線安全研究，建議換成這兩款：
> - **[AWUS036ACM 中國安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)** — 真正免驅，完美支持監聽模式
> - **[AWUS036ACS 中國安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)** — 性價比最高的監聽網卡

---

## Windows 10 / 11 安裝步驟

在 Windows 下，這款網卡表現非常出色。

### 第一步：下載驅動

中國境內訪問 Alfa 官網驅動庫是沒問題的：

[https://files.alfa.com.tw](https://files.alfa.com.tw)

進去後找 **AWUS036EACS** 文件夾，下載最新的 Windows 驅動包（一般是 `.zip` 或 `.exe`）。

### 第二步：安裝

1. 解壓下載的壓縮包。
2. 右鍵點擊安裝程序，選擇「以管理員身份運行」。
3. 一路點「下一步」，最後重啟電腦。

### 第三步：確認狀態

右鍵點擊「此電腦」 -> 「管理」 -> 「設備管理器」 -> 「網絡適配器」。

你應該能看到：`Realtek 8821CU Wireless LAN 802.11ac USB NIC`。看到它，就說明你可以正常上網了。

---

## 藍牙如何開啟？

裝好驅動後，藍牙通常會自動啟用：

1. 打開 Windows 的「設置」 -> 「藍牙和其他設備」。
2. 把藍牙開關推到「開」。
3. 現在你可以連接藍牙鼠標、耳機或鍵盤了。

---

## 常見問題

| 現象 | 可能原因 | 解決辦法 |
|---------|-------------|-----|
| 網卡搜不到 5G 訊號 | 頻道不匹配 | 嘗試在網卡屬性裡把區域設為美國（US） |
| 藍牙連不上 | 驅動衝突 | 確認禁用電腦自帶的板載藍牙 |

## 更多 Alfa 網卡指南

- [AWUS036ACH 中國安裝指南](/zh-tw/blog/awus036ach-china-install-guide/) — 經典大天線
- [AWUS036AX 中國安裝指南](/zh-tw/blog/awus036ax-china-install-guide/) — WiFi 6 新款

有問題？歡迎在下方留言，或者在 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯繫我們。
