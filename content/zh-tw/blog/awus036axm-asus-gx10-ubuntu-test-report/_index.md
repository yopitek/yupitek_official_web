---
title: "AWUS036AXM 單卡實測：MediaTek MT7921AU（Wi-Fi 6 2x2）在 ASUS GX10 + Ubuntu 24.04（ARM64）的 Monitor・AP・WPA3 能力與 Injection 限制"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM（mt7921u）在 ASUS GX10／Ubuntu 24.04 ARM64 實測：monitor、AP、WPA3 可用，但 packet injection 失敗，不適合滲透測試，定位純 AP 與連線。"
faq:
  - question: "AWUS036AXM 能做封包注入（packet injection）嗎？"
    answer: "在我們的測試平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。aireplay-ng --test 在 2.4 GHz 與 5 GHz 都回報 No Answer、Found 0 APs，因此也無法 deauth 或擷取 WPA handshake。根因是 kernel 6.16+ 的 mac80211 chanctx 回歸，並非晶片先天不能注入；同系列的 AWUS036AXML 結果相同。需要注入請改選實測可用的 AWUS036EACS、ACH 或 ACS。"
  - question: "AWUS036AXM 適合拿來做滲透測試或 Kali 嗎？"
    answer: "不建議。monitor 能用但接收偏弱、client 與 data 封包常漏接，而且本平台 injection 失敗，無法 deauth 或擷取 handshake。本文平台是 Ubuntu 24.04，未在 Kali 發行版本身測試。它適合純 AP、一般連線與 WPA3 熱點；滲透測試請選 AWUS036EACS、ACH 或 ACS。"
  - question: "AWUS036AXM 在 Ubuntu 24.04 要另外裝驅動嗎？"
    answer: "不用。mt7921u 驅動在 kernel 6.17 內建，插上即辨識（USB ID 0e8d:7961），免 DKMS、免編譯。驅動不提供 IBSS（Ad-hoc）與 mesh 模式，這是限制而非設定問題。"
  - question: "AWUS036AXM 可以當 AP 開熱點嗎？支援 WPA3 嗎？"
    answer: "可以，這是它最拿手的用途。2.4 GHz（802.11n）與 5 GHz VHT80 都有 iPhone 連入並 authorized；WPA3-SAE 在 2.4 GHz 可用（MFP: yes；5 GHz 的 WPA3 未實測），舊款 iPhone 需設 sae_pwe=0；STA＋AP 並行（VIF）也可用。本輪只測 2.4 與 5 GHz，6 GHz 與藍牙未單獨實測。"
  - question: "AWUS036AXM 的 monitor mode 好用嗎？"
    answer: "能進 monitor，2.4 GHz 與 5 GHz 都收得到 beacon，但接收偏弱、client 與 data 封包量少，建議鎖定單一頻道而非跳頻。要大範圍或長距離監聽，我們的測試中 AWUS036AXER 與 ACH 明顯更強。"
draft: false
---

{{< tldr >}}AWUS036AXM 在 ASUS GX10／Ubuntu 24.04 ARM64 上 monitor、AP、WPA3、VIF 可用，但 packet injection 實測失敗（No Answer／Found 0 APs），無法 deauth 或擷取 handshake，不建議用於滲透測試；定位純 AP 與連線。{{< /tldr >}}

Yopitek 是 ALFA Network 的台灣經銷商。這篇是 AWUS036AXM 的逐卡實測，目的很單純：把這張 Wi-Fi 6 網卡在 **ASUS GX10（ARM64）+ Ubuntu 24.04** 上「能做什麼、不能做什麼」量到清楚，讓選購的客戶不必靠規格表猜。

先把定位講明白：以下所有測試都在 Yopitek 自有設備、自有辦公室 Wi-Fi 上完成，對象是我們自己的測試手機。這是經銷商對產品相容性與能力邊界的硬體驗證，不是針對第三方網路的攻擊教學。文中不提供任何對外部網路的操作步驟；monitor 與注入相關的量測，一律在自有封閉環境、對自有裝置進行。

這張卡最需要先知道的一件事：**它在本平台的 injection（注入）是失敗的**。如果你的用途會用到注入或 handshake 擷取，可以直接跳到第四、第五節看選型結論；如果你要的是穩定連線與架 AP，那 AWUS036AXM 會是一張很稱職的卡。

## 一、卡片與測試平台

AWUS036AXM 採用 MediaTek **MT7921AU** 晶片，走 kernel 內建的 **mt7921u** 驅動，規格為 **Wi-Fi 6（802.11ax）、2x2** 雙空間流。同晶片的 **AWUS036AXML**（MT7921AUN，多了藍牙）在本平台的 Wi-Fi monitor／AP／注入行為完全相同，兩張可互相參照；差別是 AXML 另有藍牙，且本機實測 6 GHz band 可用，而 AXM 的 6 GHz 與藍牙本輪未單獨實測。

- **運算平台**：ASUS GX10（ARM64 / aarch64）
- **作業系統**：Ubuntu 24.04 LTS
- **核心版本**：kernel 6.17.0-1014-nvidia
- **測試裝置**：Apple iPhone 7 Plus（WPA3-SAE 與 VIF 另以 iPhone 15 Pro 複測）
- **測試環境**：自有辦公室 Wi-Fi，SSID `YUPITEK`，2.4GHz ch5 / 5GHz ch36
- **測試期間**：2026-11-16 至 2026-11-18 實機量測

## 二、硬體與驅動（免裝即用）

mt7921u 驅動已內建於 kernel 6.17，AWUS036AXM 插上 GX10 就被辨識，不需要 DKMS、不需要自行編譯任何第三方驅動。這是這代 MediaTek 卡在 ARM64 上最省事的地方。

| 項目 | 內容 |
|---|---|
| 型號 | AWUS036AXM |
| 晶片 | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| 驅動（in-kernel） | `mt7921u` |
| 世代 / 串流 | Wi-Fi 6（802.11ax）/ 2x2 |
| 介面模式 | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| 不支援模式 | IBSS（Ad-hoc）、Mesh（802.11s） |

確認網卡被辨識：

```bash
lsusb | grep 0e8d:7961
```

預期輸出為 `ID 0e8d:7961 MediaTek Inc. Wireless_Device`。另外留意一下，`iw phy info` 列出的介面模式裡沒有 IBSS 與 mesh point，這是 mt7921u 的先天限制，不是設定問題；要跑 mesh / IBSS 的場景，改用 `mt76` 的 AWUS036ACM / ACHM。

## 三、實測能力：Monitor / AP / WPA3，以及 Injection 失敗的誠實說明

先給一張核心能力矩陣，再逐項說明。

| 能力項目 | 2.4 GHz | 5 GHz | 實測備註 |
|---|---|---|---|
| Monitor（監聽） | ✅ 可用（接收較弱） | ✅ 可用（接收較弱） | 收得到 beacon，client / data frame 量偏少 |
| **Injection（注入）** | ❌ **本平台失敗** | ❌ **本平台失敗** | 根因為 kernel 6.16+ mac80211 chanctx 回歸（非晶片先天） |
| AP（熱點） | ✅ 含 802.11n（HT20） | ✅ VHT 80 MHz | iPhone 7 Plus 實機連入、authorized |
| WPA3-SAE | ✅ | 未實測 | MFP: yes，`sae_pwe=0` 相容舊 iPhone；僅在 2.4 GHz 實測 |
| VIF（STA + AP） | ✅ | ✅ | 一卡兩用，STA 側 ping 17 ms |

### Monitor（監聽）✅ 可用，但接收偏弱

2.4GHz 與 5GHz 都能切進 monitor 模式，也都收得到 beacon。但要誠實說：AWUS036AXM 的接收明顯比同平台的 AWUS036ACM / ACHM 弱，實測 frame 數偏少，client 與 data 封包擷取量不多。實務上建議**鎖定單一頻道**側錄，不要跳頻，收穫會穩定一些。

還有一個容易誤判的點：monitor 模式下 `txpower` 會回報 3 dBm，這是回報假象（硬體實際 TX 約 20 dBm，已由 `txpower_sku` 驗證），不代表發射真被壓到那麼低。AWUS036AXM 本來就不是為大範圍側錄設計的；要掃得廣、收得遠，就看天線調校更強、跳頻更積極的 AWUS036AXER，或雙天線高增益的 AWUS036ACH，這兩張在同平台的 monitor 收訊明顯更強。

### AP（熱點）✅ 這是 AXM 最拿手的場景

2.4GHz 開 AP 可同時開 802.11n（HT20），iPhone 7 Plus 連入協商到 MCS 7、authorized。5GHz 可開到 **VHT 80 MHz**，iPhone 連入為 VHT-NSS2、authorized。無論 2.4G 或 5G，AWUS036AXM 當熱點都穩定，這是它在本平台最值得買單的能力。

### WPA3-SAE ✅

AP 端開 WPA3-SAE，iPhone 7 Plus 成功連入，MFP（Management Frame Protection）顯示 `yes`。實務提醒：設 `sae_pwe=0` 可相容 iPhone 7 Plus 這類較舊裝置；若設 `sae_pwe=2`，舊 iPhone 可能連不上。

### VIF（STA + AP 一卡兩用）✅

AWUS036AXM 可以同時當 STA 連上既有 Wi-Fi，又開一個 AP 虛擬介面（VIF）。實測 iPhone 15 Pro 連入 AP VIF 時，STA 這端對 `YUPITEK` 的 ping 約 17 ms，連線正常。對「一張卡同時上網又分享熱點」的需求是可用的。

### Injection（注入）❌ 本平台失敗 —— 這是選型的分水嶺

這是 AWUS036AXM 最重要、也最需要誠實交代的一條。實測 `aireplay-ng --test` 的輸出是：

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

2.4GHz 與 5GHz 都一樣失敗。先釐清一個常見誤會：monitor 模式下 `iw` 回報 txpower 只有 3 dBm 是**回報假象**，硬體實際 TX 約 20–23 dBm（已由 `txpower_sku` 驗證），發射功率並沒有被壓低，不是失敗主因。真正的根因在**軟體層**：kernel 6.16 之後 mac80211 的 channel context（chanctx）出現回歸，讓 stock 驅動在 active monitor／注入情境下收不到目標 beacon，`aireplay-ng` 於是判定 `No Answer`。這是 **kernel 端的回歸，不是 MT7921 晶片先天不能注入**。現象記錄在 morrownr/USB-WiFi issue #387，根因分析則在 morrownr/mt76 issue #18。

要補充的是：社群實測指出，在同型號上改用 git／patched 驅動，確實能讓 active monitor 加注入運作起來；但即使如此，MT7921 firmware 仍把注入**鎖在 1 Mbps／6 Mbps 的基礎速率**，無法以 HT／VHT 速率注入。換句話說，就算繞過 kernel 回歸，這張卡的注入能力也受限。對照 Realtek 的 rtw89 卡（如 AWUS036AX／AXER）在同一套 aircrack-ng、同一個 GX10 平台上注入可用，MT7921 這條路在 **stock kernel 6.17** 上是不通的。

再強調一次，這不是單張卡故障，也不是設定調錯。同晶片的 AWUS036AXML 行為一模一樣，在 stock kernel 6.17 上改參數、換頻道、改 regulatory domain 都救不回來——根因是 kernel 6.16+ 的 mac80211 chanctx 回歸，再加上 firmware 的注入速率鎖，並非晶片硬體缺陷。直接的後果：AWUS036AXM 在本平台**無法 deauth、無法主動擷取 WPA handshake**。需要這些能力，請改用下一節的 Realtek / mt76x 方案。

至於進階功能，整理如下：

| 進階功能 | 狀態 | 說明 |
|---|---|---|
| WPA handshake 擷取 | ❌ | 因注入失敗而不可用，改用 ACM / ACHM / ACH / ACS / EACS |
| VIF（STA + AP） | ✅ | 一卡兩用可用 |
| Active monitor | 🟡 | `set monitor active` 被接受，ACK 未驗證 |
| Ad-hoc（IBSS） | N/A | mt7921u 不支援 |
| Mesh（802.11s） | N/A | mt7921u 不支援 |
| Wi-Fi Direct（P2P） | ⬜ | 驅動宣告支援，缺第二台設備未測 |

### 操作安全與實務提醒

幾個在 GX10 上操作這張卡的實務重點，先講在前面可以少踩雷：

- **別切斷自己的網路**：絕對不要執行 `airmon-ng check kill`，它會關掉 NetworkManager、讓整台 GX10 斷網。操作時只動外接的 `wlx*` 介面，不要碰 GX10 內建的對外上網主線。
- **AP 密碼要 8 碼以上**：否則 hostapd 會回 `invalid WPA passphrase length` 而起不來。
- **手機掃不到 SSID 時**：把網卡拔插一次重置、或把手機靠近即可解決（monitor 模式回報的 3 dBm 是假象、非真實功率，並非主因）。
- **RX stall 排除**：反覆切換 monitor / AP 之後若突然掃不到任何東西，多半是 RX stall，拔插網卡一次即可復原（介面名以 MAC 命名、不會改變）。

## 四、適合與不適合的用途

把上面的量測收斂成一句話：AWUS036AXM 是張優秀的「連線 / AP」卡，但不是「注入 / 攻防」卡。

**適合的用途**

- 穩定的日常連線（Wi-Fi 6、2x2）
- 架設 2.4GHz / 5GHz AP 熱點（含 802.11n 與 VHT80）
- WPA3-SAE 相容性驗證與佈建測試
- STA + AP 一卡兩用（VIF）
- 被動側錄 beacon 的輕量 monitor 需求

**不適合的用途（避雷）**

- injection / deauth
- WPA handshake 擷取、主動式攻防演練
- 需要 IBSS（Ad-hoc）或 Mesh 的實驗
- 需要長距離、高靈敏度的大範圍 monitor 側錄

**最重要的一條避雷**：如果你的用途是 **injection 或 handshake**，**請勿選 AWUS036AXM（或同晶片的 AWUS036AXML）**。MT7921 在 ASUS GX10（ARM64 / Ubuntu 24.04 / stock kernel 6.17）這個平台上注入失敗，根因是 kernel 6.16+ 的 mac80211 chanctx 回歸、並非晶片先天不能注入；截至 2026-11-18 的 stock 環境無法以調參解決，把它留給「純連線 / 純 AP」的場景即可。

## 五、選型建議（純 AP／連線）

| 你的需求 | 建議選擇 | 理由 |
|---|---|---|
| 純 AP / 穩定連線（不需注入） | **AWUS036AXM** / AWUS036AXML | MediaTek 連線穩定，AP 與 WPA3 表現好 |
| 滲透測試（injection + handshake） | AWUS036EACS / AWUS036ACH / AWUS036ACS | 兩頻注入可用，端到端 handshake 跑得通 |
| 最強接收 / 長距離 monitor | AWUS036AXER / AWUS036ACH | AXER 跳頻掃描積極，ACH 雙天線高增益 |
| Wi-Fi 6 + AP 且要注入 | AWUS036AX / AWUS036AXER | 2x2 VHT80，AP 穩定且注入可用 |
| mesh / IBSS 實驗 | AWUS036ACM / AWUS036ACHM | `mt76` 驅動單機可建立 |

一句白話：要穩定連線、要當 AP，AWUS036AXM 很稱職；只要牽涉注入或 handshake，就換 Realtek 的 EACS / ACH / ACS。同一批卡在 ARM64 上的完整比較，以及 9 款 Monitor / Injection / AP / WPA3 全矩陣，請見總表 Hub：

- [2026 最完整實測：9 款 ALFA 無線網卡在 ASUS GX10（ARM64 / Ubuntu 24.04）全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

再次強調定位：本文所有 monitor / 注入相關的量測，全部在 Yopitek 自有封閉環境、對自有測試裝置進行，用途是驗證產品能力與相容性邊界，不提供也不建議對任何第三方網路進行上述操作。

## 常見問題（FAQ）

**Q1. AWUS036AXM 能做封包注入（packet injection）嗎？**
在我們的測試平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。`aireplay-ng --test` 在 2.4 GHz 與 5 GHz 都回報 `No Answer`、`Found 0 APs`，因此也無法 deauth 或擷取 WPA handshake。根因是 kernel 6.16+ 的 mac80211 chanctx 回歸，並非晶片先天不能注入；同系列的 AWUS036AXML 結果相同。需要注入請改選實測可用的 AWUS036EACS、ACH 或 ACS。

**Q2. AWUS036AXM 適合拿來做滲透測試或 Kali 嗎？**
不建議。monitor 能用但接收偏弱、client 與 data 封包常漏接，而且本平台 injection 失敗，無法 deauth 或擷取 handshake。本文平台是 Ubuntu 24.04，未在 Kali 發行版本身測試。它適合純 AP、一般連線與 WPA3 熱點；滲透測試請選 AWUS036EACS、ACH 或 ACS。

**Q3. AWUS036AXM 在 Ubuntu 24.04 要另外裝驅動嗎？**
不用。mt7921u 驅動在 kernel 6.17 內建，插上即辨識（USB ID `0e8d:7961`），免 DKMS、免編譯。驅動不提供 IBSS（Ad-hoc）與 mesh 模式，這是限制而非設定問題。

**Q4. AWUS036AXM 可以當 AP 開熱點嗎？支援 WPA3 嗎？**
可以，這是它最拿手的用途。2.4 GHz（802.11n）與 5 GHz VHT80 都有 iPhone 連入並 authorized；WPA3-SAE 在 2.4 GHz 可用（`MFP: yes`；5 GHz 的 WPA3 未實測），舊款 iPhone 需設 `sae_pwe=0`；STA＋AP 並行（VIF）也可用。本輪只測 2.4 與 5 GHz，6 GHz 與藍牙未單獨實測。

**Q5. AWUS036AXM 的 monitor mode 好用嗎？**
能進 monitor，2.4 GHz 與 5 GHz 都收得到 beacon，但接收偏弱、client 與 data 封包量少，建議鎖定單一頻道而非跳頻。要大範圍或長距離監聽，我們的測試中 AWUS036AXER 與 ACH 明顯更強。

## 六、延伸閱讀

以下相關文章陸續上線（連結施工中）：

- 《免裝驅動：在 Ubuntu（ARM64）上啟用 Monitor 與 AP 模式》 → [`/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE 能力與 handshake 實務（自有環境驗證）》 → [`/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 《AWUS036AXML 單卡實測（同 MT7921 晶片 + BT）》 →（施工中）
- 《為什麼 mt7921u 在 kernel 6.16 以後無法注入：chanctx 回歸與韌體速率鎖說明》 →（施工中）

---

*測試單位：Yopitek（ALFA 經銷）｜ 平台：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 / VIF 另測 iPhone 15 Pro）*
