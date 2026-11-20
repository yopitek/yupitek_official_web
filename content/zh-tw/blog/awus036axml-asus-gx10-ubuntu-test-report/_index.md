---
title: "AWUS036AXML 實測：Wi-Fi 6 + 藍牙複合卡在 ASUS GX10（ARM64 / Ubuntu 24.04）——AP 穩定、注入失敗的誠實報告"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML（Wi-Fi＋藍牙）在 ASUS GX10／Ubuntu 24.04 ARM64 實測：AP、WPA3、monitor 可用，但 injection 失敗、無法擷取 handshake，不建議滲透測試。"
faq:
  - question: "AWUS036AXML 能做封包注入（packet injection）嗎？"
    answer: "在我們的測試平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。aireplay-ng --test 回報 No Answer、Found 0 APs；指定 AP 逐台測也只得到 No such BSSID available。即使一般掃描看得到該 AP（約 -54 dBm），注入工具情境下仍收不到它的 beacon，所以 deauth 與 handshake 擷取（0 筆）都無法使用。根因是 kernel 6.16+ 的 mac80211 chanctx 回歸，非晶片先天不能注入；AWUS036AXM 結果相同。需要注入請改選 AWUS036EACS、ACH 或 ACS。"
  - question: "AWUS036AXML 的藍牙在 Ubuntu 上能用嗎？"
    answer: "本機實測藍牙可用：以 bluetoothctl／hciconfig 確認 hci 控制器為 UP，可掃到 BLE 與經典藍牙裝置，且 Wi-Fi 與藍牙能同時使用（共存）。它是 Wi-Fi＋藍牙複合裝置；提醒：重插偶爾會卡在 WiFi probe、生不出 wlx 介面，換一個 USB 孔重插即可恢復。"
  - question: "AWUS036AXML 在 Ubuntu 24.04 要另外裝驅動嗎？"
    answer: "不用。mt7921u 驅動在 kernel 6.17 內建，插上後 dmesg 會看到 mt7921u 把介面改名為 wlx 加 MAC（USB ID 0e8d:7961），免 DKMS、免編譯。驅動不提供 IBSS 與 mesh 模式。"
  - question: "AWUS036AXML 可以開 AP、支援 WPA3 嗎？"
    answer: "可以，這是它最穩的用途。2.4 GHz（802.11n，MCS 10）與 5 GHz VHT80（VHT-NSS2）都有 iPhone 連入並 authorized；WPA3-SAE 以 sae_pwe=0 讓 iPhone 15 Pro 連入（MFP: yes；於 2.4 GHz 與 6 GHz 實測，5 GHz 未實測）；STA＋AP 並行時 STA 端 ping 約 4.4 ms。雖然定位為 Wi-Fi 6 晶片，本機另實測 6 GHz band 可用（自架 6135 MHz AP，iPhone 15 Pro 以 802.11ax 連上並取得 IP）。"
  - question: "AWUS036AXML 和 AWUS036AXM 差在哪、該選哪張？"
    answer: "在本平台兩張的 Wi-Fi 行為相同：同用 mt7921u、injection 同樣失敗、monitor 接收同樣偏弱，AP、WPA3、VIF 同樣可用。差別是 AXML 另有藍牙（本機實測可用）且本機實測 6 GHz band 可用，而 AXM 的藍牙與 6 GHz 本輪未單獨實測。純 AP 或一般連線選哪張都可以；要 injection 或 handshake，兩張都不要選。"
draft: false
---

{{< tldr >}}AWUS036AXML 在 ASUS GX10／Ubuntu 24.04 ARM64 上 AP、WPA3、VIF 與被動 monitor 可用，藍牙與 6 GHz band 本機實測亦可用，但 injection 實測失敗（No Answer／Found 0 APs），無法 deauth 或擷取 handshake，不建議用於滲透測試；定位純 AP 與一般連線。{{< /tldr >}}

ALFA AWUS036AXML 是這批 9 款網卡裡唯一「MediaTek Wi-Fi 6 + 藍牙」的複合型號。它和不帶藍牙的 AWUS036AXM 是同一世代晶片（MT7921，走 `mt7921u` 驅動），差別就在多了一組藍牙。客戶最常問的還是那三題：monitor 進得去嗎？能不能 injection？能不能架 AP？這篇把 AWUS036AXML 單獨拉出來，在 ASUS GX10（ARM64）搭配 Ubuntu 24.04 逐項實測，做得到、做不到的一次講清楚，尤其是最關鍵的那條限制：**injection 在這個平台上失敗**。

先把定位講明白：以下所有量測都在 Yopitek 自有設備、自有辦公室 Wi-Fi（SSID `YUPITEK`）、對自有測試手機（iPhone 7 Plus，WPA3 另以 iPhone 15 Pro 複測）上完成。這是經銷商對產品相容性與能力邊界的硬體驗證，不是針對第三方網路的操作教學。文中的 monitor、AP、injection 自我測試，全部在自有封閉環境、對自有裝置進行。

## 一、這張卡與測試平台

- **運算平台**：ASUS GX10（ARM64 / aarch64）
- **作業系統**：Ubuntu 24.04 LTS
- **核心版本**：kernel 6.17.0-1014-nvidia
- **受測網卡**：ALFA AWUS036AXML（MediaTek MT7921AUN，Wi-Fi 6 / 2x2 / +BT）
- **測試裝置**：Apple iPhone 7 Plus（WPA3-SAE 另以 iPhone 15 Pro 複測）
- **測試環境**：自有辦公室 Wi-Fi，SSID `YUPITEK`，2.4GHz ch5 / 5GHz ch36、ch157
- **測試期間**：2026-11-16 至 2026-11-18 實機量測

所有結果都以實際量到的數字或狀態記錄，不以規格書推測；MAC 位址於輸出中以 `xx` 遮蔽。

## 二、硬體與驅動：MT7921AUN，插上即用

| 項目 | 規格 |
|---|---|
| 型號 | AWUS036AXML |
| 晶片 | MediaTek MT7921AUN |
| USB ID | `0e8d:7961`（MediaTek Inc. Wireless_Device） |
| in-kernel 驅動 | `mt7921u` |
| 世代 / 串流 | Wi-Fi 6 / 2x2（2T2R） |
| 藍牙 | 有（BT + WiFi 複合裝置；本機實測 hci 控制器 UP、可掃到 BLE 與經典藍牙裝置、WiFi+BT 共存） |
| USB 列舉 | USB 3 |
| 介面命名 | `wlx<MAC>`（例：`wlx00c0cabd65b9`） |

辨識方式很直接：插上後用 `lsusb` 看到 MediaTek 的 USB ID，`dmesg` 看到 `mt7921u` 掛載、把介面改名：

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

兩個重點。第一是免編譯：AWUS036AXML 走 kernel 6.17 內建的 `mt7921u` 驅動，插上即辨識，不必在 aarch64 上處理任何 out-of-tree DKMS 模組，這在 ARM64 平台特別省事。第二是它以 USB 3 列舉（前代部分型號的 OTG 線只有 USB 2.0），傳輸頻寬不是瓶頸。

補一個常被誤會的點：AWUS036AXML 定位是 Wi-Fi 6（非 6E）晶片，但**本機實測 6 GHz band 可用**——我們自架 6135 MHz 的 AP，iPhone 15 Pro 以 802.11ax 連上並取得 IP。另外藍牙也實測可用：`hciconfig`／`bluetoothctl` 看到 hci 控制器狀態 UP，可掃到 BLE 與經典藍牙裝置，Wi-Fi 與藍牙能同時運作（共存）。

再查一下支援的介面模式，會看到一個對選型有意義的細節，就是沒有 IBSS、也沒有 mesh point：

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

也就是說，managed、AP、monitor、P2P 都有，但 ad-hoc（IBSS）與 802.11s mesh 這兩種模式，`mt7921u` 驅動根本不提供。要做 mesh / IBSS 實驗的客戶，這張直接排除（改看 `mt76` 的 ACM / ACHM）。

## 三、實測能力：Monitor / AP / WPA3，以及 injection 的誠實限制

核心能力一次看完：

| 能力 | 2.4GHz | 5GHz | 說明 |
|---|---|---|---|
| Monitor | ✅（弱） | ✅（弱） | 可側錄 beacon；client / data 封包常漏接 |
| **Injection** | ❌ **失敗** | ❌ **失敗** | `aireplay-ng` 注入 / deauth 無法運作；根因為 kernel 6.16+ mac80211 chanctx 回歸（非晶片先天） |
| AP 熱點 | ✅ 含 802.11n | ✅ VHT80（80MHz） | iPhone 7 Plus 連入，`authorized: yes` |
| WPA3-SAE | ✅ | 未實測 | iPhone 15 Pro 連入，`MFP: yes`（`sae_pwe=0`）；6 GHz 亦已實測（ch37、6135 MHz） |

### Monitor：兩頻都進得去，但收訊偏弱

AWUS036AXML 在 2.4GHz（ch1 / 6 / 11）與 5GHz（ch36 / 149 / 157）都能進 monitor mode，側錄 beacon 沒問題。設定流程是標準的 `iw dev` 四步：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # 2.4GHz 改用 set channel 6
```

誠實說一句：它的 monitor 收訊明顯比同批的 MT7612U（ACM）或 Wi-Fi 6 的 AXER 弱。beacon 抓得到，但 client / data 封包常常漏接；用 `airodump-ng` 跳頻掃描時容易漏掉部分 AP。實務上建議鎖定單一頻道（`-c <ch>`）而不是跳頻，收穫會穩一些。另外，monitor 模式下 `iw info` 會回報 txpower 只有 3 dBm，這是**回報假象**（硬體實際 TX 約 20–23 dBm，已由 `txpower_sku` 驗證），並不是功率真被壓到 3 dBm，這點後面「注意事項」會一起談。

### AP 熱點：2.4GHz 含 HT、5GHz 上得了 VHT80

AP 是 AWUS036AXML 最穩的一塊。2.4GHz 可以直接保留 802.11n（HT），不必像單天線的 ACHM 那樣關掉 HT；5GHz 則能開到 VHT 80MHz。兩頻都實測讓 iPhone 7 Plus 連入、`authorized: yes`。

5GHz VHT80 的 hostapd 關鍵設定：

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

實測連入後是 VHT-NSS2、80MHz。2.4GHz 版本把 `hw_mode` 換成 `g`、`channel=6`，保留 `ieee80211n=1` 與 `ht_capab=[HT20]` 即可，iPhone 連入是 MCS 10（802.11n）。

### WPA3-SAE：可用，記得 sae_pwe=0

把 AP 的 `wpa_key_mgmt` 換成 `SAE`、加上 `ieee80211w=2` 與 `sae_pwe=0`，就能開 WPA3-SAE。實測 iPhone 15 Pro 於 2.4 GHz 連入（6 GHz 亦連入；5 GHz 未實測）、`authorized: yes`、`MFP: yes`。`sae_pwe=0` 是為了相容舊款 iPhone，這點和 ACHM 的雷一樣，`sae_pwe=2` 時舊機常常連不上。

### VIF：一邊上網一邊當熱點，可行

AWUS036AXML 支援多介面並存。建一個 AP VIF（不同 MAC、unmanage）、主介面連上 Wi-Fi、同頻道開 AP，實測 iPhone 7 Plus 連入 AP VIF 時，STA 對 `YUPITEK` 的 ping 是 4.4 ms。對「一張卡同時上網 + 分享熱點」的需求是成立的。

### 誠實限制：injection 在本平台失敗

這是 AWUS036AXML（以及它的無藍牙雙胞胎 AXM）最需要講清楚的一條。在 ASUS GX10 + kernel 6.17 上，我們對自有測試環境做 injection 自我測試，結果是失敗：

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

就算指定自家 AP 的 BSSID 逐台測，也只回 `No such BSSID available`。關鍵在於：一般掃描明明看得到該 AP（訊號 -54 dBm），但一進到注入工具的情境，這張卡就「聽不到」目標的 beacon，deauth 送不出去，4-way handshake 擷取數為 0。

這不是參數沒調好，也不是單張網卡故障。真正的根因在**軟體層**：kernel 6.16 之後 mac80211 的 channel context（chanctx）出現回歸，讓 stock 驅動在注入情境下收不到目標 beacon，`aireplay-ng` 因此判定 `No Answer`，並**不是 MT7921 晶片先天不能注入**。現象記錄在 morrownr/USB-WiFi issue #387，根因分析在 morrownr/mt76 issue #18。社群實測指出，在同型號上以 git／patched 驅動可讓 active monitor 加注入運作，但 MT7921 firmware 仍把注入鎖在 1 Mbps／6 Mbps 基礎速率、無法以 HT／VHT 注入；AXM 與 AXML 兩款在 **stock kernel 6.17** 上同樣中獎，截至 2026-11-18 無法靠調參解決。

因此，凡是牽涉 injection 的能力，像 deauth、WPA handshake 擷取、以注入為前提的滲透測試，AWUS036AXML 在本平台都做不到。這類用途請改用實測注入可用的型號（見下方選型）。

### 其他進階模式一覽

| 進階功能 | 狀態 | 說明 |
|---|---|---|
| VIF（STA + AP 並存） | ✅ | 同頻道 ch36；iPhone 連入時 STA ping 4.4 ms |
| WPA handshake 擷取 | ❌ | 注入失敗 → deauth 送不出、handshake 0 |
| Active monitor | 🟡 | `set monitor active` 被接受，ACK 未驗證 |
| Ad-hoc（IBSS） | N/A | `mt7921u` 驅動不具此模式 |
| Mesh（802.11s） | N/A | `mt7921u` 驅動不具此模式 |
| Wi-Fi Direct（P2P） | ⬜ | 驅動宣告支援，需第二台設備，略過 |

## 四、藍牙複合注意事項與適用／不適用用途

### BT + WiFi 複合卡的實務副作用

AWUS036AXML 內含藍牙，是這批裡兩款複合裝置之一（另一款是 Realtek 的 EACS）。藍牙本機已實測可用（hci 控制器 UP、可掃到 BLE 與經典藍牙裝置、與 Wi-Fi 共存，見前文），這裡補一個複合裝置的實務副作用：重插時偶爾會卡在 WiFi probe、生不出 `wlx` 介面，症狀是拔插後 `ls /sys/class/net` 遲遲等不到網卡。解法很單純：**換一個 USB 孔**重插，通常就能正常列舉。

另一個要記住的小動作：AP 模式下如果手機突然掃不到你的 SSID，把網卡**拔插一次**重置即可，不必改設定。（注意：前面提到 monitor 回報的 3 dBm 是假象、非真實功率，不是 SSID 消失的主因。）

### 平台安全守則

- 絕對不要執行 `airmon-ng check kill`：它會關掉 NetworkManager，讓整台 GX10 斷網。操作時只動外接的 `wlx*` 介面，不要碰內建的對外上網主線。
- `hcxdumptool 8.x` 在這台機器上會 `failed to arm`（AWUS036EACS 在 2.4 GHz 除外；GX10 三頻內建卡列舉衝突 + 驅動無 active-monitor），這是全平台通病、與 AXML 無關；需要類似功能時改用 `airodump-ng` 搭配其他 aircrack-ng 工具。
- ARM64 補充：`aircrack-ng` 需自原始碼編譯，`wifite` 建議用 git 版以繞過 apt 依賴衝突。

### 適用 / 不適用一覽

| 適用情境 | 不適用情境 |
|---|---|
| 純 AP / 熱點（2.4G 含 HT、5G VHT80） | injection / deauth |
| WPA3-SAE 熱點 | WPA handshake 擷取 |
| 一般 managed 連線 | 以注入為前提的滲透測試主力卡 |
| 被動 monitor / 頻譜盤點（鎖單一頻道） | mesh / IBSS 實驗 |
| STA + AP 並存（VIF、一邊上網一邊分享） | 需要強收訊的長距離側錄 |

## 五、選型建議（連回總表）

把 AWUS036AXML 放回 9 款的全貌來看，它的定位很清楚：MediaTek 的連線穩定、免編譯、兩頻 AP 都上得了 VHT80，是一張稱職的「純連線 / 純 AP」卡；只要沾到 injection，就不是它的場子。

| 需求 | 建議型號 |
|---|---|
| 純 AP / 一般連線（不需注入） | **AWUS036AXML / AWUS036AXM**（本卡適用） |
| injection + handshake（滲透測試） | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| mesh / IBSS 實驗 | AWUS036ACM / AWUS036ACHM |
| 最強接收 / 長距離 monitor | AWUS036AXER / AWUS036ACH |

如果你正在 9 款之間做取捨，完整的 Monitor / Injection / AP / WPA3 全矩陣與依用途的選型，請看總表：

- [2026 最完整實測：9 款 ALFA 無線網卡在 ASUS GX10 的全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

一句話避雷：**要 injection 或 handshake，別選 AWUS036AXML / AWUS036AXM**；要純連線或架熱點，它很好用。

## 常見問題（FAQ）

**Q1. AWUS036AXML 能做封包注入（packet injection）嗎？**
在我們的測試平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。`aireplay-ng --test` 回報 `No Answer`、`Found 0 APs`；指定 AP 逐台測也只得到 `No such BSSID available`。即使一般掃描看得到該 AP（約 -54 dBm），注入工具情境下仍收不到它的 beacon，所以 deauth 與 handshake 擷取（0 筆）都無法使用。根因是 kernel 6.16+ 的 mac80211 chanctx 回歸，非晶片先天不能注入；AWUS036AXM 結果相同。需要注入請改選 AWUS036EACS、ACH 或 ACS。

**Q2. AWUS036AXML 的藍牙在 Ubuntu 上能用嗎？**
本機實測藍牙可用：以 `bluetoothctl`／`hciconfig` 確認 hci 控制器為 UP，可掃到 BLE 與經典藍牙裝置，且 Wi-Fi 與藍牙能同時使用（共存）。它是 Wi-Fi＋藍牙複合裝置；提醒：重插偶爾會卡在 WiFi probe、生不出 `wlx` 介面，換一個 USB 孔重插即可恢復。

**Q3. AWUS036AXML 在 Ubuntu 24.04 要另外裝驅動嗎？**
不用。mt7921u 驅動在 kernel 6.17 內建，插上後 dmesg 會看到 mt7921u 把介面改名為 `wlx` 加 MAC（USB ID `0e8d:7961`），免 DKMS、免編譯。驅動不提供 IBSS 與 mesh 模式。

**Q4. AWUS036AXML 可以開 AP、支援 WPA3 嗎？**
可以，這是它最穩的用途。2.4 GHz（802.11n，MCS 10）與 5 GHz VHT80（VHT-NSS2）都有 iPhone 連入並 authorized；WPA3-SAE 以 `sae_pwe=0` 讓 iPhone 15 Pro 連入（`MFP: yes`；於 2.4 GHz 與 6 GHz 實測，5 GHz 未實測）；STA＋AP 並行時 STA 端 ping 約 4.4 ms。雖然定位為 Wi-Fi 6 晶片，本機另實測 6 GHz band 可用（自架 6135 MHz AP，iPhone 15 Pro 以 802.11ax 連上並取得 IP）。

**Q5. AWUS036AXML 和 AWUS036AXM 差在哪、該選哪張？**
在本平台兩張的 Wi-Fi 行為相同：同用 mt7921u、injection 同樣失敗、monitor 接收同樣偏弱，AP、WPA3、VIF 同樣可用。差別是 AXML 另有藍牙（本機實測可用）且本機實測 6 GHz band 可用，而 AXM 的藍牙與 6 GHz 本輪未單獨實測。純 AP 或一般連線選哪張都可以；要 injection 或 handshake，兩張都不要選。

## 延伸閱讀

（連結陸續上線，施工中）

- 同晶片無藍牙版：[AWUS036AXM 單卡實測](/zh-tw/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- 注入可用的替代方案：[AWUS036EACS 單卡實測](/zh-tw/blog/awus036eacs-asus-gx10-ubuntu-test-report/)、[AWUS036ACH 單卡實測](/zh-tw/blog/awus036ach-asus-gx10-ubuntu-test-report/)、[AWUS036ACS 單卡實測](/zh-tw/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- 主題文：[免裝驅動：在 Ubuntu（ARM64）上啟用 Monitor 與 AP 模式](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 主題文：[WPA3-SAE 連線與 handshake 實務（自有環境驗證）](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 總表 Hub：[9 款 ALFA 網卡在 ASUS GX10 的全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*測試單位：Yopitek（ALFA Network 台灣經銷）｜ 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）｜ 測試環境：自有辦公室 Wi-Fi（SSID YUPITEK）。本文為產品相容性與能力驗證，非針對第三方網路之操作教學。*
