---
title: "ALFA AWUS036EACS 中國安裝指南：Windows 驅動與 Linux 兼容性說明"
description: "ALFA AWUS036EACS 在中國的安裝指南。RTL8821CU 晶片，WiFi 5 + 藍牙 4.2 二合一迷你網卡。提供 Windows 驅動下載地址，並詳細說明 Linux 下的限制。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "驅動", "中國", "藍牙", "rtl8821cu"]
categories: ["驅動安裝指南"]
series: ["Alfa 中國安裝全攻略"]
related_product: "/zh-tw/products/alfa/awus036eacs/"
---

AWUS036EACS 是 ALFA 的迷你款 WiFi 5 + 藍牙 4.2 二合一網卡，非常適合筆記型電腦用戶擴充無線效能。它採用的是 RTL8821CU 晶片組。**注意：** 這款網卡主要是為 Windows 用戶設計的，如果你想在 Linux 或 Kali 下玩監聽模式，請務必先看下面的「Linux 用戶須知」。

## Linux 用戶請先看這裡

> **AWUS036EACS 無法穩定支援 Kali Linux、Ubuntu、Debian 或樹莓派。** RTL8821CU 晶片組目前沒有官方維護的開源 Linux 驅動，也不支援監聽模式（Monitor Mode）、封包注入（Packet Injection）或 VIF 虛擬介面。
>
> 如果你需要一張網卡做安全滲透測試，強烈建議選擇以下型號：
> - **[AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)** — MT7612U 晶片，原生核心支援，監聽模式 + VIF 的完美選擇。
> - **[AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)** — RTL8811AU 晶片，性價比極高的監聽網卡。

---

## Windows 10 / 11 安裝步驟

### 第一步：從 Alfa 官方下載驅動

Alfa 的官方驅動伺服器在中國是可以正常存取的，速度很快：

https://files.alfa.com.tw

在裡面找到 **AWUS036EACS** 資料夾，下載 Windows 驅動套件（通常是 `.zip` 或 `.exe` 格式）。

### 第二步：安裝驅動

1. 解壓縮下載好的 zip 檔案。
2. 右鍵點擊安裝程式 `.exe`，選擇**以管理員身份執行**。
3. 按照螢幕提示點擊「下一步」。
4. 安裝完成後，建議重新啟動電腦。

### 第三步：驗證安裝

重新啟動後，打開**裝置管理員**（右鍵開始功能表 → 裝置管理員）。

在「網路介面卡」下，你應該能看到：

```
Realtek 8821CU Wireless LAN 802.11ac USB NIC
```

---

## 藍牙設定 (Windows)

AWUS036EACS 自帶藍牙 4.2。驅動裝好後：

1. 打開**設定 → 藍牙與裝置**。
2. 將藍牙開關撥到「開啟」。
3. 點擊「新增裝置」來配對你的鍵盤、滑鼠、耳機或其他藍牙週邊。

---

## Linux 兼容性詳情

### Kali Linux

RTL8821CU 在現代 Kali 核心上沒有穩定維護的 DKMS 驅動。雖然網路上有一些社群維護的驅動，但極不穩定，經常在核心更新後導致系統崩潰或網卡失效。監聽模式和注入功能基本不可用。

**建議：** 玩 Kali 的朋友請直接上 [AWUS036ACM](/zh-tw/blog/awus036acm-china-install-guide/) 或 [AWUS036ACH](/zh-tw/blog/awus036ach-china-install-guide/)。

---

## 國內資源速查

| 资源 | 網址 | 用途 |
|------|------|------|
| Alfa 官方驅動庫 | [files.alfa.com.tw](https://files.alfa.com.tw) | 下載 EACS Windows 驅動 |
| Alfa 官方文件 | [docs.alfa.com.tw](https://docs.alfa.com.tw) | 安裝手冊、常見問題 |

## 更多 Alfa 網卡中國安裝指南

- [AWUS036ACH 安裝指南](/zh-tw/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安裝指南](/zh-tw/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安裝指南](/zh-tw/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安裝指南](/zh-tw/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安裝指南](/zh-tw/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安裝指南](/zh-tw/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安裝指南](/zh-tw/blog/awus036axml-china-install-guide/)
- AWUS036EACS ← 你在這裡

有問題？在下面留言，或者來 [yupitek.com](https://yupitek.com/zh-tw/contact/) 聯絡我們。
