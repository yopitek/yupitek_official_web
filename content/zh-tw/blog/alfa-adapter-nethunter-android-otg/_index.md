---
title: "在 Android 上透過 USB OTG 搭配 Kali NetHunter 使用 ALFA WiFi 網卡"
description: "如何透過 USB OTG 在 Android 的 Kali NetHunter 上使用 ALFA USB WiFi 網卡。涵蓋 AWUS036ACH 驅動程式、監聽模式指令、OTG 傳輸線需求及支援裝置。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
featureimage: "/images/blog/alfa-adapter-nethunter-android-otg.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Kali NetHunter 使用 ALFA 網卡需要 Root 嗎？"
    answer: "需要。完整 NetHunter 版本需已 Root 的 Android 裝置與自定義核心，才能載入 RTL8812AU 模組並啟用 USB OTG 網卡支援。"
  - question: "哪一款 ALFA 網卡最適合 NetHunter？"
    answer: "AWUS036ACH（RTL8812AU）是最佳選擇。NetHunter 自定義核心已內建 88XXau 模組，監聽模式與封包注入完全支援。"
  - question: "為什麼需要帶電源的 USB OTG 集線器？"
    answer: "AWUS036ACH 從 USB 汲取約 500mW 功率，直接由手機電池供電會快速耗電並可能在負載下斷線。帶電源集線器從牆壁插座取電可完全解決此問題。"
  - question: "WiFi 6E 網卡（AWUS036AXML）能在 NetHunter 上使用嗎？"
    answer: "支援有限。MT7921AUN 晶片的核心模組可用性取決於裝置與核心版本，NetHunter 核心中尚未普遍支援，建議使用 RTL8812AU 網卡。"
  - question: "哪些 Android 裝置支援 NetHunter？"
    answer: "官方支援裝置包括 OnePlus、Google Pixel 及部分 Samsung Galaxy 機型。完整清單請參閱 NetHunter 官方裝置頁面，並確認裝置支援 USB OTG。"
---

在 Android 上透過 USB OTG 搭配 Kali NetHunter 使用 ALFA WiFi 網卡，需要已 Root 的裝置、完整 NetHunter 版本（含自定義核心），以及 AWUS036ACH 等支援監聽模式的 USB 網卡。

{{< tldr >}}
已 Root 的 Android 手機安裝 Kali NetHunter 後，透過 USB OTG 插入 ALFA AWUS036ACH 即可成為口袋型滲透測試平台。需完整 NetHunter 版本、帶電源 OTG 集線器，RTL8812AU 網卡相容性最佳。
{{< /tldr >}}

您的 Android 手機本身就是一台放在口袋裡的強大電腦。在已 Root 的裝置上安裝 Kali NetHunter，並透過 USB OTG 插入 ALFA WiFi 網卡，它就成為一個真正具備實力的口袋型滲透測試平台。不需要筆記型電腦，不需要笨重的硬體，只需要您的手機、一條短小的 OTG 傳輸線，以及一支支援監聽模式和封包注入的網卡。

本指南涵蓋讓 ALFA AWUS036ACH（或相容網卡）在 NetHunter 下正常運作所需的一切——從硬體選擇到驅動程式載入、監聽模式啟動，以及 NetHunter 應用程式內建的無線工具。

---

## 什麼是 Kali NetHunter？

Kali NetHunter 是 Kali Linux 官方的行動裝置滲透測試平台。NetHunter 不會取代 Android，而是在現有的 Android 系統上安裝一個 Kali Linux chroot 環境。您的手機繼續作為普通 Android 裝置運作，同時執行完整的 Kali Linux 使用者空間及其所有工具。

**主要特點：**

- 不需要清除 Android 資料——您的應用程式、聯絡人和資料保持完整
- 包含 NetHunter 應用程式，這是一個專用的攻擊模組和硬體控制啟動器
- 提供完整的終端機，可存取 Kali 工具集（Metasploit、Aircrack-ng、Nmap 等數百種工具）
- 需要已 Root 的 Android 裝置才能獲得完整功能

**三種版本：**

| 版本 | 需要 Root | 核心修改 | 使用場景 |
|---|---|---|---|
| NetHunter（完整版）| 是 | 是（自定義核心）| 完整攻擊面、硬體介面支援 |
| NetHunter Lite | 是 | 否 | 僅 Root 工具，無需自定義核心 |
| NetHunter Rootless | 否 | 否 | 有限工具，不支援硬體攻擊 |

若要透過 USB OTG 網卡支援監聽模式，您需要搭載包含 RTL8812AU 模組之自定義核心的**完整 NetHunter 版本**。

**官方支援裝置**包括 OnePlus、Google Pixel 及部分 Samsung Galaxy 機型。完整且最新的清單請參閱 [NetHunter 官方裝置頁面](https://www.kali.org/docs/nethunter/)。

**USB OTG 是必要條件。** 購買硬體前，請確認您的特定裝置型號支援 USB OTG。大多數現代裝置支援，但部分入門級機型和舊款硬體可能缺乏必要的 USB 控制器支援。

---

## 硬體需求

正確配置此設定意味著在每個層面選擇相容的硬體。鏈路中任何一個不匹配——裝置、傳輸線或網卡——都會導致網卡無法出現在 `lsusb`、間歇性斷線或驅動程式失敗。

| 項目 | 需求 | 備註 |
|---|---|---|
| Android 裝置 | 已 Root、支援 NetHunter、支援 USB OTG | 購買前確認 OTG 支援；需要搭載自定義核心的完整 NetHunter |
| USB OTG 傳輸線 / 轉接頭 | 根據裝置連接埠選擇 USB-C OTG 或 Micro-USB OTG | 品質很重要——劣質傳輸線會導致間歇性斷線 |
| ALFA WiFi 網卡 | 推薦 AWUS036ACH 或 AWUS036ACM | AWUS036ACH（RTL8812AU）在 NetHunter 中擁有最佳核心模組支援；AWUS036ACM（MT7612U）亦相容 |
| 帶電源的 USB OTG 集線器 | 強烈推薦 | 防止網卡引起的電池耗盡和 USB 不穩定 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH 從 USB 連接埠汲取約 **500mW** 的功率。在沒有專用電源的情況下直接從手機電池供電，將大幅加快電池耗電速度，並可能導致網卡在負載下重置或斷線。帶電源的 OTG 集線器——從牆壁插座取電並將資料傳遞給手機——可以完全解決此問題。
{{< /alert >}}

**選擇帶電源 OTG 集線器的注意事項：**

尋找明確標示支援 USB OTG 電力傳遞直通的集線器。這意味著集線器從 USB 充電器取得 5V 電源，從充電器（而非手機）為連接的裝置供電，並仍在手機和連接裝置之間傳遞資料。並非所有 USB 集線器都支援這一點——購買前請仔細查看產品規格。

---

## NetHunter 支援的 ALFA 網卡

NetHunter 的自定義核心包含針對特定晶片組預先編譯的核心模組。RTL8812AU 晶片組系列擁有最強的支援，因為它很早就被整合進來，並持續獲得維護。

| 網卡 | 晶片組 | NetHunter 支援 | 備註 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ 最佳支援 | NetHunter 核心包含 `88XXau` 模組；監聽模式和封包注入完全支援 |
| AWUS036ACM | MT7612U | ✅ 良好支援 | 替代晶片組；通常可用；請根據您的特定裝置核心進行確認 |
| AWUS036ACS | RTL8811AU | ✅ 可用 | 與 RTL8812AU 同一驅動程式系列；功耗較低（約 300mW） |
| AWUS036AXM | MT7921AUN | ⚠️ 有限 | WiFi 6E 網卡；核心模組可用性取決於裝置和核心版本 |
| AWUS036AXML | MT7921AUN | ⚠️ 有限 | 與 AXM 相同晶片組；NetHunter 核心中未普遍支援 |

**建議：** 為了可靠的 NetHunter 操作，請堅持使用基於 RTL8812AU 的網卡。`88XXau` 驅動程式已特別包含在大多數 NetHunter 自定義核心中，您可以找到大量社群文件，故障排除路徑也已完整記錄。若您需要具備廣泛 NetHunter 相容性的雙頻 AC1200 功能，**AWUS036ACH** 是正確的選擇。

---

## 設定步驟

以下步驟假設您擁有一台已安裝完整 NetHunter 的已 Root Android 裝置，以及已備妥的 USB OTG 傳輸線或集線器。

### 步驟 1：開啟 NetHunter 應用程式

在 Android 裝置上啟動 NetHunter 應用程式，前往 **Kali Services** 確認 chroot 環境正在運行。若未運行，請點選 **Start** 啟動它。在核心能夠將 USB 裝置暴露給 Kali 工具之前，chroot 必須處於活動狀態。

### 步驟 2：透過 OTG 連接 ALFA 網卡

將 USB OTG 傳輸線或集線器插入手機的 USB 連接埠，然後將 ALFA 網卡連接到 OTG 傳輸線或集線器。若使用帶電源的集線器，請先將集線器的電源轉接器連接到牆壁插座。

### 步驟 3：授予 USB 權限

Android 將顯示一個權限對話框，詢問是否允許 NetHunter 應用程式存取 USB 裝置。點選 **確定**，若您希望在未來的操作中跳過此提示，請勾選**一律允許**。若您在未授予權限的情況下關閉此對話框，網卡將無法從 Kali chroot 存取。

### 步驟 4：在 `lsusb` 中確認網卡

開啟 NetHunter 終端機並執行：

```bash
lsusb
```

您應該看到包含 **Realtek Semiconductor** 及裝置 ID 的條目。對於 AWUS036ACH，預期輸出類似於：

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

若 Realtek 裝置未出現，問題在硬體層面——請檢查 OTG 傳輸線，嘗試不同的傳輸線，或確認裝置的開發人員設定中已啟用 OTG。

### 步驟 5：載入驅動程式

```bash
sudo modprobe 88XXau
```

在大多數 NetHunter 版本中，驅動程式會在偵測到網卡時自動載入。若連接網卡後介面未出現，請手動執行此指令。

### 步驟 6：確認介面

```bash
ip link show | grep wlan
```

您應該看到 `wlan1`（若您的裝置內建 WiFi 介面佔用 `wlan0`，則可能是 `wlan2`）。

### 步驟 7：啟用監聽模式

```bash
sudo airmon-ng start wlan1
```

若 `airmon-ng` 回報可能干擾監聽模式的程序，請先終止它們（請參閱下方的指令區段），然後重新執行此指令。監聽模式啟動後，介面將重新命名為 `wlan1mon`。

---

## NetHunter 上的監聽模式指令

```bash
# 確認系統識別網卡
lsusb | grep -i realtek

# 若連接網卡後未自動載入，手動載入驅動程式
sudo modprobe 88XXau

# 終止干擾監聽模式的程序（NetworkManager、wpa_supplicant 等）
sudo airmon-ng check kill

# 在 ALFA 網卡介面上啟動監聽模式
sudo airmon-ng start wlan1

# 掃描所有可見網路（按 Ctrl+C 停止）
sudo airodump-ng wlan1mon

# 擷取特定網路的流量
# -c：頻道，--bssid：目標 AP MAC 位址，-w：輸出檔案前綴
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

---

## NetHunter WiFi 攻擊（僅限授權測試）

{{< alert "triangle-exclamation" >}}
所有無線安全測試必須**僅在您擁有或已取得明確書面授權進行測試的網路和裝置上**執行。未經授權存取電腦網路在全球大多數司法管轄區屬於違法行為。此處描述的工具僅供授權滲透測試、安全研究和教育目的使用。Yupitek 對任何濫用行為不承擔任何責任。
{{< /alert >}}

**WiFi Evil Portal（WPS3）：** 可直接在 NetHunter 應用程式主選單中使用。在授權的社交工程評估中建立一個帶有強制入口網站的惡意存取點，用於憑證收集。需要支援 AP 模式的外部網卡。

**MANA Rogue AP 工具組：** 位於 **NetHunter 應用程式 > Wireless Attacks > MANA Toolkit**。MANA 透過 KARMA 式攻擊和 SSL 剝離功能擴展了標準惡意 AP 的概念。完整功能需要相容的外部 WiFi 網卡——Android 內建 WiFi 晶片對於大多數 MANA 設定並不足夠。

---

## 電池與電源管理

**功耗：** AWUS036ACH 在主動使用期間持續汲取約 500mW。在典型的 3,500 mAh Android 電池上，與正常手機使用相比，這將使您的電池耗電速度大約翻倍。

**使用帶電源的 OTG 集線器：** 這是最有效的解決方案。集線器從牆壁插座取電並將其提供給 ALFA 網卡。手機 USB 連接埠僅傳輸資料，不為網卡供電。

**同時充電操作：** 若沒有帶電源的集線器，您可以使用支援 PD 直通的 USB-C 集線器同時為手機充電來緩解電池耗盡問題。

**螢幕管理：** 將顯示逾時設定為 30 秒（**設定 > 顯示 > 休眠**）並將亮度降至最低。

**散熱考量：** 長時間使用網卡加上手機殼可能導致熱量積聚。若手機的熱保護機制限制了 USB 控制器，可能會發生網卡斷線。長時間擷取操作時請移除手機殼。

---

## 故障排除

**網卡未被識別（`lsusb` 什麼都沒顯示）：**
1. 確認已啟用 USB OTG——查看**設定 > 開發人員選項 > OTG**
2. 嘗試不同的 OTG 傳輸線——傳輸線品質是常見的失敗點
3. 確認您的裝置支援 USB OTG

**驅動程式未載入（`modprobe` 後沒有 `wlan1` 介面）：**
1. 在 NetHunter 終端機中查看 `dmesg` 中的錯誤訊息：`dmesg | tail -30`
2. 確認 NetHunter chroot 正在運行
3. 確認您的 NetHunter 版本包含 `88XXau` 模組：`find /lib/modules -name "*88XX*"`

**`wlan1` 介面在使用中消失：**
幾乎必定是 USB 電源問題。使用帶電源的 OTG 集線器。

**權限被拒絕錯誤：**
確保您在 NetHunter chroot 中以 root 身份執行指令。先執行 `sudo su`，然後再執行指令。

**監聽模式已啟動但 `airodump-ng` 中未顯示任何網路：**
1. 嘗試 `sudo airodump-ng --band abg wlan1mon` 掃描所有頻段
2. 確認在啟動監聽模式前已執行 `airmon-ng check kill`
3. 確認天線已正確連接到網卡

---

{{< faq >}}

## 相關指南

- [AWUS036ACH 在 Kali Linux（桌機/筆電）上的設定指南](/zh-tw/blog/awus036ach-kali-linux-setup/)
- [在 Raspberry Pi 和 Kali 上使用 ALFA 網卡](/zh-tw/blog/alfa-adapter-raspberry-pi-kali/)

## 參考來源

1. [Kali NetHunter 官方文件](https://www.kali.org/docs/nethunter/)
2. [aircrack-ng rtl8812au 驅動專案](https://github.com/aircrack-ng/rtl8812au)
3. [ALFA Network 官方網站](https://www.alfa.com.tw/)
4. [Android USB OTG 開發者文件](https://developer.android.com/guide/topics/connectivity/usb)
