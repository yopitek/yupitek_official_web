---
title: "Kali Linux 2026 啟用監聽模式完整教學：WiFi 網路卡設定指南"
description: "逐步說明如何在 Kali Linux 2024/2025 使用 airmon-ng 或 iw 指令啟用監聽模式，涵蓋相容 ALFA 網路卡、除錯方法，以及用 airodump-ng 驗證。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["監聽模式", "Kali-Linux", "airmon-ng", "iw", "WiFi網路卡", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "監聽模式與受管理模式有何不同？"
    answer: "監聽模式讓網卡擷取空中所有 802.11 訊框，不受管理模式只接收目標 MAC 符合自身封包的限制，是無線滲透測試的基礎。"
  - question: "airmon-ng 與 iw 指令啟用監聽模式有何差異？"
    answer: "airmon-ng 會自動處理干擾行程並建立 wlan0mon 虛擬介面；iw 則直接修改現有介面，不另建介面，適合需要精簡控制時使用。"
  - question: "啟用監聽模式後介面自動切回受管理模式怎麼辦？"
    answer: "wpa_supplicant 或 NetworkManager 在背景重新啟動所致。執行 airmon-ng check kill 終止這些行程即可解決。"
  - question: "哪些 ALFA 網卡在 Kali Linux 上完整支援監聽模式？"
    answer: "AWUS036ACH（RTL8812AU）、AWUS036AXML（MT7921AUN）、AWUS036ACM（MT7612U）三款均完整支援，其中 ACM 為即插即用。"
  - question: "airodump-ng 顯示 Fixed channel wlan0mon: -1 錯誤如何解決？"
    answer: "表示 airodump-ng 無法切換頻道。執行 iwconfig wlan0mon channel 1 指定頻道，並終止殘留的 wpa_supplicant 程序。"
---

監聽模式讓無線網卡擷取空中所有 802.11 訊框，是 airodump-ng、Wireshark、Kismet 等工具運作的基礎。Kali Linux 上可透過 airmon-ng 或 iw 指令啟用。

{{< tldr >}}
監聽模式解除網卡只接收自身封包的限制，是無線滲透測試的根基。使用 airmon-ng 或 iw 指令搭配 ALFA 網卡即可在 Kali Linux 上穩定啟用。
{{< /tldr >}}

## 什麼是監聽模式？為何滲透測試非它不可

監聽模式是無線網路介面卡（NIC）的一種特殊操作模式，讓網路卡能擷取空中**所有** 802.11 訊框，而不只是傳送給自身裝置的封包。在一般「受管理模式」下，網路卡只接收目標 MAC 位址符合自身的封包，其餘一律丟棄。監聽模式則完全解除這道過濾機制。

對無線滲透測試人員來說，監聽模式是一切的基礎。少了它，**airodump-ng**、**Wireshark**（無線擷取模式）或 **Kismet** 等工具就無法被動攔截網路流量。監聽模式能支援以下應用場景：

- **被動偵察** — 掃描周邊所有基地台與客戶端裝置，全程不發送任何訊框。
- **握手封包擷取** — 在客戶端認證過程中監聽 WPA/WPA2 四向握手封包。
- **取消認證攻擊** — 發送 802.11 管理訊框（除監聽模式外，還需具備封包注入能力）。
- **流氓基地台偵測** — 識別網路中未經授權的基地台。
- **協定分析** — 深度檢視 802.11 管理、控制與資料訊框。

並非所有無線網路卡都支援監聽模式。能否啟用，取決於**晶片組**及編譯進核心的**驅動程式**。面向一般家用市場的消費性網路卡幾乎都不相容。專為資安研究設計的網路卡——例如 ALFA Network 系列——採用的晶片組與驅動程式，能乾淨地開放監聽模式。

---

## 事前準備

啟用監聽模式前，請確認以下條件：

1. 系統為 **Kali Linux**（建議 2024.1 以上版本），並搭載相容核心。
2. 無線網路卡已插入（USB 介面）或安裝完成（PCIe/mini-PCIe 介面）。
3. 擁有 **root 或 sudo** 權限。
4. 已確認介面名稱：執行 `ip link` 或 `iwconfig`，記下無線介面名稱（通常為 `wlan0`、`wlan1` 或 `wlx...`）。

```bash
ip link show
```

尋找以 `wlan` 開頭，或以 `wlx` 加上長串 MAC 位址命名的項目。

---

## 方法一：使用 airmon-ng 啟用監聽模式

`airmon-ng` 是 **aircrack-ng** 套件的一部分，也是 Kali Linux 上切換監聽模式最常用的工具。它會自動處理許多邊緣情況，包括停止可能干擾模式切換的背景程序。

### 步驟一：終止干擾程序

NetworkManager、wpa_supplicant 和 dhclient 都會與監聽模式競搶介面控制權，必須先行終止：

```bash
sudo airmon-ng check kill
```

預期輸出：

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **注意：** 此操作會中斷現有的網路連線。若測試期間仍需存取網際網路，請改用有線連線，或以第二張無線網路卡保持受管理模式連線。

### 步驟二：啟動監聽模式

```bash
sudo airmon-ng start wlan0
```

預期輸出：

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtl8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

網路卡現已進入監聽模式，同時建立一個新的虛擬介面——通常命名為 **wlan0mon**。

### 步驟三：指定頻道（選用，但建議設定）

預設情況下，網路卡會在各頻道之間跳頻。若要針對特定目標擷取封包，建議鎖定頻道：

```bash
sudo iwconfig wlan0mon channel 6
```

---

## 方法二：使用 iw 啟用監聽模式

`iw` 是現代化的底層無線設定工具，提供更直接的控制方式。當 `airmon-ng` 無法使用或出現異常時，此方法是很好的替代方案。

```bash
# 關閉介面
sudo ip link set wlan0 down

# 設定為監聽模式
sudo iw dev wlan0 set type monitor

# 重新啟用介面
sudo ip link set wlan0 up
```

三道指令串接執行：

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

此方法直接修改現有的 `wlan0` 介面，不會另外建立 `wlan0mon` 虛擬介面。執行後請驗證設定是否生效：

```bash
iw dev wlan0 info
```

在輸出結果中確認是否出現 `type monitor`。

---

## 驗證監聽模式

### 使用 iwconfig

```bash
iwconfig
```

處於監聽模式的介面會顯示：

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

關鍵欄位為 **Mode:Monitor**。

### 使用 iw dev

```bash
iw dev
```

在對應介面項目下找到 `type monitor`。若顯示 `type managed`，表示監聽模式未成功套用。

---

## 使用 airodump-ng 進行功能測試

監聽模式啟用後，使用 `airodump-ng` 進行端到端測試：

```bash
sudo airodump-ng wlan0mon
```

畫面應立即出現周邊基地台的即時清單，顯示 BSSID、頻道、訊號強度（PWR）、加密類型及 ESSID。若畫面空白或出現錯誤，請參閱下方的故障排除章節。

僅掃描 5 GHz 頻段：

```bash
sudo airodump-ng --band a wlan0mon
```

擷取指定網路並將結果儲存以供後續分析：

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## ALFA 網路卡相容性對照表

[ALFA Network](/zh-tw/products/alfa/) 網路卡是 Kali Linux 無線滲透測試的業界標準。以下型號均完整支援監聽模式：

| 型號 | 晶片組 | 頻段 | 監聽模式 | 封包注入 | 備註 |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ | ✅ | 滲透測試最熱門首選 |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ | ✅ | Wi-Fi 6E，需核心 5.18 以上 |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ | ✅ | Linux 驅動程式支援優異 |

上表所有型號均已在 Kali Linux 2024.x 與 2025.x 上驗證驅動程式相容性。針對 RTL8812AU 等晶片組，若您的核心版本較新，可能需要從 Aircrack-ng GitHub 儲存庫安裝對應驅動程式。

---

## 故障排除

### 「無法啟用監聽模式」或介面消失

這通常是 NetworkManager 重新接管介面所致。再次執行 `airmon-ng check kill`，然後重試。若問題持續，請手動停止 NetworkManager：

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### 監聽模式自動還原為受管理模式

部分驅動程式會在幾秒後自動切回受管理模式，通常是因為 wpa_supplicant 在背景重新啟動。確認目前執行中的程序：

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

依 PID 終止找到的程序，再重新啟用監聽模式。

### 執行 airmon-ng 後介面名稱不同

在某些系統上，新介面可能命名為 `wlan0mon`、`mon0` 或其他名稱。執行 `airmon-ng start` 後，務必以 `iwconfig` 或 `iw dev` 確認實際介面名稱，再傳入 airodump-ng 使用。

### airodump-ng 出現「Fixed channel wlan0mon: -1」錯誤

這表示 airodump-ng 無法切換頻道。嘗試以下指令：

```bash
sudo iwconfig wlan0mon channel 1
```

若仍無效，終止所有殘留的 wpa_supplicant 程序後再試一次。

### RTL8812AU 驅動程式在新版核心上的問題

極新版本核心內建的 RTL8812AU 驅動程式，有時缺乏完整的監聽模式支援。請安裝社群維護版驅動程式：

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

安裝完成後重新開機。

---

## 測試完畢後關閉監聽模式

測試結束後，務必將網路卡還原為受管理模式。保持監聽模式會導致裝置無法正常連線網路。

### 使用 airmon-ng：

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### 使用 iw：

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

使用 `iwconfig` 確認介面已回到受管理模式，再重新連線至網路。

---

{{< faq >}}

## 總結

在 Kali Linux 上啟用監聽模式分為兩個步驟：停止干擾服務，再以 `airmon-ng` 或 `iw` 切換介面模式。成功的關鍵在於使用具備受支援晶片組的網路卡。搭載 RTL8812AU、MT7921AUN、MT7612U 晶片組的 ALFA Network 網路卡，在 Kali Linux 上提供最可靠的開箱即用體驗。

立即瀏覽 [Yopitek 提供的完整 ALFA Network 無線網路卡系列](/zh-tw/products/alfa/)——台灣 ALFA Network 授權經銷商——找到最適合您無線資安研究的網路卡。

## 參考來源

1. [aircrack-ng 官方文件](https://www.aircrack-ng.org/documentation.html)
2. [Kali Linux 官方文件](https://www.kali.org/docs/)
3. [Linux Wireless mac80211 子系統](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [iw 指令使用說明](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
