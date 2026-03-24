---
title: "什麼是封包注入？測試你的 WiFi 網路卡在 Kali Linux 的相容性"
description: "了解 WiFi 封包注入的原理、為何需要特定網路卡、如何用 aireplay-ng 測試你的 ALFA Network 網路卡，以及哪些晶片組支援 Kali Linux 封包注入。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["封包注入", "aireplay-ng", "Kali-Linux", "WiFi網路卡", "RTL8812AU", "ALFA-Network"]
---

## 什麼是封包注入？

封包注入——正式名稱為 **802.11 訊框注入**——是無線網路卡將任意 802.11 訊框直接傳送至無線媒介的能力，包含那些並非由網路卡自身網路堆疊所產生的訊框。在正常運作下，無線驅動程式只會建構並傳送作業系統合法產生的訊框：關聯請求、已連線網路的資料訊框等。封包注入繞過這些限制，讓 `aireplay-ng` 之類的工具能夠自行建構並傳送任意類型的訊框——不論是管理訊框、控制訊框還是資料訊框——並可自由指定內容、來源位址與目的地位址。

這項能力是多種無線安全評估場景的核心需求：

- **WPA/WPA2 握手封包加速擷取** — 傳送取消認證訊框，強制用戶端重新驗證，進而產生新的四向握手封包，供後續離線分析使用。
- **WPA 握手封包驗證** — 確認已擷取的握手封包檔案完整且可用於離線破解。
- **重放攻擊** — 重放擷取到的 ARP 封包，產生 IV（初始向量）流量，用於 WEP 破解（舊式測試環境）。
- **偽冒基地台建構** — 注入信標訊框與探測訊框，模擬無線存取點。
- **DoS 測試** — 在授權測試條件下，評估網路對取消認證洪泛攻擊的應對能力。

> **法律聲明：** 對未取得明確書面授權的網路或裝置執行封包注入，在大多數司法管轄區屬於違法行為。本文所述的所有技術，僅供授權滲透測試、針對自有設備的安全研究，以及學術用途使用。

---

## 為何大多數網路卡無法注入封包

這項限制主要不在於硬體，而在於**驅動程式**。消費級無線網路卡的標準驅動程式，是依照 802.11 標準的正常操作模型所撰寫的。驅動程式會驗證輸出訊框、強制執行關聯狀態，並拒絕不符合預期流程的訊框。

要支援封包注入，驅動程式必須開放一條繞過上述檢查的原始訊框傳送路徑。Linux 核心的 **mac80211** 子系統透過 `IEEE80211_HW_SUPPORTS_RAW_TX` 旗標提供此能力，但前提是驅動程式必須明確啟用它。大多數廠商為消費級網路卡提供的驅動程式並未啟用原始 TX——消費端沒有這方面的需求，而啟用它也會帶來潛在的濫用風險。

此外，部分晶片組採用**專有韌體**，在內部直接處理 MAC 層，即使驅動程式有意支援注入，主機驅動程式也無法注入任意訊框。這種情況在為企業或消費級筆電設計的 Broadcom 與 Intel 晶片中相當常見。

---

## 支援封包注入的晶片組

以下晶片組在 Kali Linux 上具備完善的封包注入支援，並廣泛用於 ALFA Network 無線網路卡：

### Realtek RTL8812AU

截至 2024–2026 年，滲透測試領域最受歡迎的晶片組。支援雙頻（2.4/5 GHz）、802.11ac，並由 aircrack-ng GitHub 儲存庫維護的社群版 `rtl8812au` 驅動程式提供支援。監聽模式與封包注入均可穩定運作。

### Realtek RTL8814AU

RTL8812AU 的升級版：4×4 MIMO、802.11ac、雙頻。由 `rtl8814au` 驅動程式支援。在基地台密度高的環境中，更強的訊號有助於提升擷取品質，因此表現尤為出色。完整支援封包注入。

### Mediatek MT7612U

雙頻 802.11ac 晶片組，搭載維護完善的核心內建驅動程式（`mt76`）。監聽模式與封包注入均已納入上游核心支援，在大多數當前版本的 Kali Linux 上無需額外安裝外部驅動程式。

### Atheros AR9271

具有悠久無線安全工具使用歷史的經典單頻（2.4 GHz）晶片組。`ath9k_htc` 驅動程式內建於核心，經過長期實戰驗證，封包注入支援穩定，在各核心版本間表現一致。雖僅支援 2.4 GHz，對於舊式網路的測試需求仍是可靠的選擇。

### Mediatek MT7921AUN（Wi-Fi 6E）

本清單中最新的晶片組，搭載於 AWUS036AXML。支援 2.4/5/6 GHz 三頻及 802.11ax。`mt7921u` 驅動程式需要 kernel 5.18 或更新版本。監聽模式與封包注入支援均已獲確認，但由於驅動程式較新，在舊版發行版上可能存在邊緣案例問題。

---

## 使用 aireplay-ng 測試封包注入

在實際測試中使用封包注入之前，務必先驗證你的網路卡與驅動程式組合是否正常運作。注入支援會因核心版本與驅動程式修訂版本而有所不同。

### 事前準備

網路卡必須已進入監聽模式。若尚未啟用，請先執行：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

確認監聽介面已建立：

```bash
iwconfig
# 確認出現：Mode:Monitor
```

### 執行注入測試

```bash
sudo aireplay-ng --test wlan0mon
```

### 成功輸出範例

```
09:15:34  Trying broadcast probe requests...
09:15:34  Injection is working!
09:15:36  Found 3 APs

09:15:36  Trying directed probe requests...
09:15:36   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:37  Ping (min/avg/max): 1.153ms/5.464ms/12.214ms Power: -62
09:15:37  29/30: 96%

09:15:37   AA:BB:CC:DD:EE:02 - channel: 11 - 'OfficeWiFi'
09:15:38  Ping (min/avg/max): 2.101ms/6.322ms/14.881ms Power: -71
09:15:38  28/30: 93%
```

封包注入運作正常時，會顯示 **「Injection is working!」**，並列出對附近基地台的 ping 成功率。成功率高於 80% 通常代表運作可靠；低於 50% 則可能意味著有干擾、距離過遠，或驅動程式存在問題。

### 失敗輸出範例

```
09:15:34  Trying broadcast probe requests...
09:15:36  No Answer...
09:15:36  Injection is working! (RTL)
09:15:36  Trying directed probe requests...
09:15:37   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:39  Failed!
```

或在完全失敗的情況下：

```
09:15:34  Trying broadcast probe requests...
09:15:46  No Answer...
09:15:46  Injection is NOT working!
```

出現「Injection is NOT working!」即為明確的失敗訊號。代表該網路卡不支援封包注入，或驅動程式未正確安裝。

---

## 支援封包注入的 ALFA 無線網路卡

搭配正確驅動程式在 Kali Linux 上使用時，所有主要 [ALFA Network](/zh-tw/products/alfa/) 網路卡型號均支援封包注入：

| 型號 | 晶片組 | 頻段 | 封包注入支援 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ 完整支援 |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ 完整支援（需 kernel 5.18+） |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ 完整支援 |
| AWUS036NHA | AR9271 | 2.4 GHz | ✅ 完整支援 |
| AWUS036NH | RTL8187 | 2.4 GHz | ✅ 完整支援 |
| AWUS1900 | RTL8814AU | 2.4 / 5 GHz | ✅ 完整支援 |

---

## 常見注入測試失敗原因與解決方式

### 啟用監聽模式後立即顯示「Injection is NOT working!」

最常見的原因是 NetworkManager 或 wpa_supplicant 仍在背景執行。請終止這些程序後重新測試：

```bash
sudo airmon-ng check kill
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

### 成功率過低（低於 50%）

- **距離問題：** 靠近附近的基地台後重新測試。
- **頻道不匹配：** 將監聽介面鎖定至目標基地台所在的相同頻道：`sudo iwconfig wlan0mon channel 6`
- **驅動程式問題：** 重新安裝外部驅動程式。針對 RTL8812AU：從 `https://github.com/aircrack-ng/rtl8812au` 複製儲存庫，並執行 `sudo make dkms_install`。

### 核心模組無法載入

```bash
sudo modprobe -r rtl8812au
sudo modprobe rtl8812au
dmesg | tail -20
```

檢查 `dmesg` 中關於模組的錯誤訊息。缺少韌體檔案是常見問題——請安裝 `firmware-linux-nonfree` 或對應晶片組的韌體套件。

### 插入網路卡後裝置未出現

```bash
lsusb
dmesg | tail -30
```

若 `lsusb` 顯示裝置，但 `ip link` 中未出現任何無線介面，代表驅動程式繫結失敗。通常是驅動程式未安裝，或核心模組載入失敗所致。

---

## 應用場景：在授權測試中使用封包注入

### WPA2 握手封包擷取

這是專業滲透測試中最常見的封包注入應用。在目標基地台的頻道上以 airodump-ng 開始擷取，接著以 aireplay-ng 傳送取消認證訊框，強制用戶端重新連線：

```bash
# 終端機 1：擷取封包
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# 終端機 2：取消認證（對特定用戶端傳送 5 個取消認證訊框）
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

切換回終端機 1，留意 airodump-ng 右上角是否出現 `WPA handshake: AA:BB:CC:DD:EE:FF` 的訊息。

### 取消認證測試（DoS 評估）

安全評估人員透過傳送取消認證洪泛，測試無線網路的韌性，評估用戶端是否能安全地重新關聯，以及基地台是否有記錄或緩解此類攻擊的機制。此類測試須在已簽署的工作授權書範圍內執行。

---

## 負責任地使用封包注入

封包注入是一項功能強大的技術。其在授權滲透測試中的合法應用已有充分實績——擷取握手封包、驗證無線安全控制措施、測試用戶端行為。濫用此技術既有害且違法。

在進行任何測試前，請務必確認：
- 已取得網路擁有者的書面授權
- 工作授權書範圍明確包含無線測試項目
- 充分了解當地關於無線安全測試的相關法規

本文所述的工具（aireplay-ng、airodump-ng、aircrack-ng）內建於 Kali Linux，專供授權安全測試使用。請依此原則使用。

---

如需選購已確認支援封包注入的無線網路卡，歡迎瀏覽 [Yopitek 的 ALFA Network 產品系列](/zh-tw/products/alfa/)——台灣授權 ALFA Network 經銷商。
