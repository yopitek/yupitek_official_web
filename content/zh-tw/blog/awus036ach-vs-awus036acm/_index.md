---
title: "ALFA AWUS036ACH vs AWUS036ACM：Kali Linux 完整比較（2026）"
description: "深入比較 ALFA AWUS036ACH 與 AWUS036ACM，包含晶片組、監聽模式、封包注入、驅動支援，以及哪款更適合 Kali Linux 滲透測試。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "比較", "Kali-Linux", "RTL8812AU", "MT7612U"]
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACH 和 AWUS036ACM 驅動安裝有什麼差異？"
    answer: "AWUS036ACH 採 RTL8812AU 晶片，需透過 DKMS 編譯安裝 aircrack-ng 社群驅動，核心更新後可能需重新編譯；AWUS036ACM 的 MT7612U 驅動自核心 4.19 起整合進主線，即插即用無需編譯。"
  - question: "哪款更適合 Monitor Mode 監聽？"
    answer: "AWUS036ACH 監聽模式更穩定，雙天線與 30 dBm 高功率在密集 AP 環境下封包遺失率更低；ACM 亦支援監聽但單天線功率較低，適合近距離擷取。"
  - question: "新手應該選 ACH 還是 ACM？"
    answer: "新手建議選 AWUS036ACM，MT7612U 核心原生驅動即插即用免編譯；若需最強訊號與最多教學資源且不怕 DKMS 編譯流程，再選 AWUS036ACH。"
  - question: "VM 虛擬機環境推薦哪款？"
    answer: "VM 環境推薦 AWUS036ACM，USB 直通後核心原生驅動立即識別可用，無需在虛擬機內安裝編譯工具鏈；ACH 需在 VM 內額外安裝驅動方能使用。"
---

## 結論先講

專業滲透測試選 [AWUS036ACH](/zh-tw/products/alfa/awus036ach/)：RTL8812AU 驅動成熟、30 dBm 雙天線帶來最強監聽與封包注入。求即插即用便攜選 [AWUS036ACM](/zh-tw/products/alfa/awus036acm/)：MT7612U 核心原生驅動，自核心 4.19 起即插即用零編譯。

{{< tldr >}}
AWUS036ACH 適合專業任務，RTL8812AU 驅動搭配 30 dBm 雙天線，監聽注入最強；AWUS036ACM 求便攜，MT7612U 核心原生驅動零編譯，價格約 $30–40。
{{< /tldr >}}

兩款都是 ALFA Network 專為 Kali Linux 滲透測試設計的 USB WiFi 網路卡，各自站在效能與便攜性光譜的不同位置。**AWUS036ACH** 是高功率、雙天線的主力機型，擁有歷經考驗的驅動程式資歷。**AWUS036ACM** 則是輕巧、核心原生的替代方案，以部分功率換取更簡便的使用體驗。本文逐一拆解所有對實戰滲透測試真正重要的面向。

---

## AWUS036ACH — AC1200、RTL8812AU、高功率

[AWUS036ACH](/zh-tw/products/alfa/awus036ach/) 自上市以來，一直是專業與業餘 Wi-Fi 安全稽核的標配。在 2017 年至今發布的 Kali Linux 無線滲透測試教學、課程與文章中，它是被引用次數最多的無線網路卡。其 TX 功率最高達 30 dBm，為 USB 網路卡中的頂尖水準（[ALFA Network 官方規格 — alfa.com.tw](https://www.alfa.com.tw)）。

**完整規格：**
- **Wi-Fi 標準：** IEEE 802.11a/b/g/n/ac（Wi-Fi 5）
- **晶片組：** Realtek RTL8812AU
- **頻段：** 2.4 GHz + 5 GHz（雙頻）
- **最大傳輸速率：** AC1200（300 + 867 Mbps）
- **天線：** 2× 可拆式 RP-SMA 接頭（雙天線多樣性）
- **預設天線：** 2× 5 dBi 全向天線
- **USB 接頭：** USB-C（相容 USB 3.0）
- **TX 功率：** 最高 30 dBm — 為 USB 網路卡中的頂尖水準
- **外形尺寸：** 較大機身（適合桌面或差旅使用）

雙 RP-SMA 接頭是一大優勢：可自由更換高增益定向或全向天線，大幅延伸訊號範圍，在長距離稽核場景中至關重要。

---

## AWUS036ACM — AC600、MT7612U、輕巧便攜

[AWUS036ACM](/zh-tw/products/alfa/awus036acm/) 的目標族群是注重簡便、便攜性與核心原生驅動支援的使用者。它採用 MediaTek MT7612U（或 MT7612UN）晶片組，自 Linux 核心 4.19 版起已納入主線，意味著在任何現代 Kali Linux 系統上**無需編譯驅動程式**。

**完整規格：**
- **Wi-Fi 標準：** IEEE 802.11a/b/g/n/ac（Wi-Fi 5）
- **晶片組：** MediaTek MT7612U / MT7612UN
- **頻段：** 2.4 GHz + 5 GHz（雙頻）
- **最大傳輸速率：** AC600（150 + 433 Mbps）
- **天線：** 1× 可拆式 RP-SMA 接頭
- **預設天線：** 1× 5 dBi 全向天線
- **USB 接頭：** USB-C（相容 USB 3.0）
- **TX 功率：** 標準功率（低於 ACH）
- **外形尺寸：** 輕巧機身（適合行動使用）

單天線與較低的 TX 功率使其長距離性能不及 ACH，但乾淨的核心驅動程式體驗與緊緻的機身，讓它在需要低調或高度機動性的任務場景中極為實用。

---

## 完整規格比較表

| 功能項目 | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Wi-Fi 標準** | 802.11ac（Wi-Fi 5） | 802.11ac（Wi-Fi 5） |
| **晶片組** | RTL8812AU | MT7612U / MT7612UN |
| **頻段** | 2.4 GHz + 5 GHz | 2.4 GHz + 5 GHz |
| **最大傳輸速率** | AC1200 | AC600 |
| **RP-SMA 接頭** | 2× | 1× |
| **TX 功率** | 最高 30 dBm | 標準 |
| **USB 類型** | USB-C | USB-C |
| **驅動程式來源** | 樹外（DKMS） | 主線核心（4.19+） |
| **驅動程式安裝** | 手動編譯 | 即插即用 |
| **監聽模式** | ★★★★★ | ★★★★☆ |
| **封包注入** | ★★★★★ | ★★★★☆ |
| **外形尺寸** | 較大 | 輕巧 |
| **價格區間** | 約 $40–50 | 約 $30–40 |

---

## 晶片組深入解析

### RTL8812AU（AWUS036ACH）

AWUS036ACH 搭載 Realtek RTL8812AU 晶片，TX 功率最高達 30 dBm，為 USB 網路卡中的頂尖水準。其社群維護驅動由 [aircrack-ng](https://github.com/aircrack-ng/rtl8812au) 社群維護，自 2017 年起持續開發與修補，是無線安全研究領域中測試最為徹底的晶片組之一（[github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)）。

**在 Kali Linux 上安裝驅動程式：**

```bash
sudo apt update
sudo apt install dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

安裝完成後，模組透過 DKMS 在核心更新後仍可持續使用。此驅動程式支援：

- **監聽模式** — 完整功能，極為穩定可靠
- **幀注入** — 支援所有注入類型（取消認證、beacon、probe、data）
- **多重虛擬介面** — 可同時執行監聽模式與管理模式
- **WPA3-SAE 握手封包擷取** — 已確認在近期核心與驅動程式組合上正常運作

主要取捨在於：每當安裝新核心時，**必須重新編譯**（或由 DKMS 自動處理）。偶爾會遇到新版 Kali 核心暫時導致編譯失敗，需等待驅動程式更新才能恢復正常。這是可以應對的問題，但在實際作業中確實存在。

### MT7612U（AWUS036ACM）

MediaTek MT7612U 驅動程式（`mt76x2u`）在 **4.19 版（2018 年 10 月）** 合併進 Linux 核心主線，目前由核心社群維護於 [kernel.org — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)。這意味著在所有執行 4.19 或更新版核心的 Kali Linux 環境中——涵蓋 2018 年底以來的每一個 Kali 發行版——AWUS036ACM 都是**即插即用**。

```bash
# 確認模組已載入
lsmod | grep mt76x2u

# 如有需要，手動載入
sudo modprobe mt76x2u
```

驅動程式主要特性：

- **無需編譯** — 非常適合氣隙或受限環境
- **監聽模式** — 支援且功能正常
- **封包注入** — 支援，整體表現穩定
- **穩定性** — 核心原生驅動程式在核心更新後通常更為穩定
- **社群支援** — 持續成長中，但規模仍小於 RTL8812AU 生態系

值得注意的是：部分 ACM 批次使用的 MT7612UN 變體，在 Linux 上的行為與 MT7612U 完全相同，兩者均由同一個 `mt76x2u` 模組處理。

---

## 監聽模式比較

兩款網路卡均支援監聽模式，但在實際使用上存在差異。

**AWUS036ACH（RTL8812AU）：**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# 建立 wlan0mon 並進入監聽模式
iwconfig wlan0mon
```

在監聽模式下切換頻道迅速且穩定。介面在高流量擷取環境（密集 AP、大量客戶端）中，於正常擷取速率下不會發生封包遺失。

**AWUS036ACM（MT7612U）：**

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# 或透過 airmon-ng：
sudo airmon-ng start wlan0
```

監聽模式功能正常，已確認可搭配 Wireshark、tcpdump、airodump-ng 與 Kismet 使用。不過，部分使用者回報在特定核心版本上，直接使用 `iw` 比使用 airmon-ng 能獲得更穩定的結果。

---

## 封包注入比較

**AWUS036ACH：** 封包注入是其最強的賣點之一。所有 aireplay-ng 攻擊模式均能穩定運作：

```bash
# 測試注入能力
sudo aireplay-ng --test wlan0mon

# 取消認證攻擊
sudo aireplay-ng -0 5 -a [BSSID] wlan0mon

# 透過取消認證擷取 WPA 握手封包
sudo airodump-ng -c [CH] --bssid [BSSID] -w capture wlan0mon &
sudo aireplay-ng -0 3 -a [BSSID] wlan0mon
```

**AWUS036ACM：** 所有標準攻擊類型均支援注入，但部分使用者回報，在特定核心版本上以極高速率注入時，偶爾會導致介面停滯。對於典型的滲透測試工作流程（受控取消認證、PMKID 擷取、KRACK 測試），整體表現穩定可靠。

---

## 驅動程式安裝複雜度

| 情境 | AWUS036ACH | AWUS036ACM |
|---|---|---|
| 全新安裝 Kali，插入網路卡 | 無法識別 — 需安裝驅動程式 | 立即識別 |
| 核心更新後 | DKMS 自動重建（通常如此） | 無需任何操作 |
| 氣隙機器 | 需準備離線安裝套件 | 原生支援，直接使用 |
| Kali Live USB | 需在當次工作階段中安裝驅動程式 | 開箱即用 |
| VirtualBox／VMware 直通 | 在虛擬機內安裝驅動程式後可用 | 在虛擬機內立即可用 |

ACM 的零安裝體驗，在 Live 開機環境、客戶提供的設備，或時間緊迫的 CTF 競賽設置等場景中，是真實且顯著的優勢。

---

## 尺寸與便攜性

**AWUS036ACH** 的 PCB 與外殼明顯較大，這部分是因為雙 RP-SMA 接頭以及 30 dBm 輸出所需的較大功率元件所致。放入筆電包沒有問題，但不算是「口袋型」網路卡。

**AWUS036ACM** 則明顯輕巧許多，可在實體安全任務中低調使用，或在大型 USB 網路卡容易引起注意的環境中發揮優勢。它的耗電量也較低，在長時間外勤作業中靠筆電電池供電時，這一點相當重要。

---

## 價格與價值

售價約 $40–50 的 **AWUS036ACH**，其溢價主要來自雙天線配置、高 TX 功率與久經驗證的驅動程式傳承。對於可靠性與訊號強度直接影響交付品質的專業任務而言，這筆溢價是合理的。

**AWUS036ACM** 售價約 $30–40，對以下使用族群提供絕佳的性價比：
- 希望即插即用的無線安全學習者
- 主要在近距離環境作業的測試人員
- 需要備用或次要網路卡的團隊
- 偏好乾淨、無編譯工作流程的任何人

---

{{< faq >}}

---

## 結論

**選擇 [AWUS036ACH](/zh-tw/products/alfa/awus036ach/)，適合：**
- 正式的專業滲透測試任務
- 最高等級的監聽模式與封包注入可靠性
- 需搭配外接天線的長距離評估（雙 RP-SMA）
- 訊號強度至關重要的環境（停車場稽核、定向目標）
- 與現有教學、課程與文件的最大相容性

**選擇 [AWUS036ACM](/zh-tw/products/alfa/awus036acm/)，適合：**
- 零驅動程式編譯的即插即用簡便體驗
- 輕便、低調的行動任務
- 預算有限的設置或作為備用網路卡
- Kali Live USB 工作流程
- 偏好核心原生穩定性而非社群驅動程式的場景

如果只能選擇一款，**AWUS036ACH** 在滲透測試上是更強的選擇。若想要一款零設定摩擦的可靠隨行夥伴，**AWUS036ACM** 同樣能在工具庫中占有一席之地。

---

## 參考來源

1. aircrack-ng 社群維護 RTL8812AU 驅動程式儲存庫 — [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. Linux 核心主線 MT76 驅動程式（`mt76x2u`，自核心 4.19 起整合）— [kernel.org — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
3. ALFA Network 官方網站與產品規格 — [alfa.com.tw](https://www.alfa.com.tw)
4. Yupitek — ALFA Network 台灣授權經銷商 — [yupitek.com](https://www.yupitek.com)
