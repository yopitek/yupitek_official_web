---
title: "AWUS036ACHM 逐卡實測：MediaTek MT7610U 單天線 AC600 在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP・WPA3 能力"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "AWUS036ACHM（MT7610U）在 Ubuntu 24.04 免裝驅動，雙頻監聽模式可用、2.4G 封包注入 96–100%；開 AP 須關 802.11n，WPA3 須設 sae_pwe=0 舊 iPhone 才連得上。"
faq:
  - question: "AWUS036ACHM 在 Ubuntu 24.04 需要裝驅動嗎？"
    answer: "不需要。MT7610U 由 kernel 內建的 mt76x0u 驅動接管，Ubuntu 24.04（kernel 6.17）插上即認，不用 DKMS、不用額外韌體；lsusb 可看到 USB ID 0e8d:7610。"
  - question: "AWUS036ACHM 能進 monitor mode 嗎？能掃到多少 AP？"
    answer: "能。2.4GHz 與 5GHz 都能進 monitor mode；用 airodump-ng 跳頻全頻掃描 120 秒，實測掃到 19 個 AP、14 個用戶端，分布在 ch1、2、5、6、36、149、157。"
  - question: "AWUS036ACHM 的封包注入成功率多少？5GHz 可以嗎？"
    answer: "2.4GHz 第 6 頻道逐台注入回應率 96–100%（aireplay-ng --test，找到 4 台 AP）。5GHz（ch36、ch149）只驗到廣播注入可用，逐台測試回報 Found 0 APs，本次沒有取得百分比，原因待查。"
  - question: "AWUS036ACHM 開 AP 時 iPhone 顯示「無法加入網路」或「密碼錯誤」怎麼辦？"
    answer: "先關掉 802.11n：hostapd 設定檔不要加 ieee80211n=1 與 ht_capab，2.4GHz 用純 hw_mode=g、5GHz 用純 hw_mode=a（20 MHz）。否則 hostapd 會反覆出現 handle_assoc_cb: STA not found，畫面像密碼錯誤，其實是 802.11n 關聯失敗。"
  - question: "AWUS036ACHM 的 WPA3-SAE 為什麼舊 iPhone 連不上？"
    answer: "多半是 hostapd 的 sae_pwe 設定。實測 sae_pwe=0 時 iPhone 7 Plus 與 iPhone 15 Pro 都連得上；sae_pwe=2 時 iPhone 7 Plus 會關聯成功但 4-way 交握失敗而斷線，看起來像密碼錯誤。請搭配 ieee80211w=2，改完設定後讓 iPhone 先忘記此網路再重連。"
draft: false
---

> 測試單位：Yupitek（ALFA Network 台灣經銷）｜測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`|測試裝置：自有 iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）|測試對象：自有辦公室 Wi-Fi（SSID `YUPITEK`，2.4G ch5 / 5G ch36、157）。
>
> 本文為經銷商對產品相容性與能力邊界的硬體驗證。所有 Monitor / Injection / AP / WPA3 測試均於 Yupitek 自有設備、自有辦公室 Wi-Fi、對自有測試手機進行，屬正當能力驗證；不針對任何第三方網路，亦不提供攻擊操作步驟。文中 injection 僅送 probe request 做能力自測，不送攻擊封包。

## 重點摘要（TL;DR）

AWUS036ACHM 於 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）實測：雙頻 monitor 可用，2.4G 封包注入 96–100%（5G 只驗到廣播注入），雙頻皆可架 AP 熱點（須關閉 802.11n）。

- Ubuntu 24.04 免裝驅動：MT7610U 由 kernel 6.17 內建的 mt76x0u 接管，插上即認，不用 DKMS、不用額外韌體。
- 雙頻監聽模式（monitor mode）可用；2.4G 封包注入 96–100%。
- 5GHz 只驗到廣播注入，逐台回應率本次未取得（原因待查）。
- 開 AP 須關閉 802.11n；WPA3 須設 `sae_pwe=0`，舊款 iPhone 才連得上。
- 單天線 1T1R（AC600），吞吐與定位和 2T2R 的 ACM / ACH 不同級。

## 1. 這張卡與這個平台

AWUS036ACHM 是 ALFA 的單天線 AC600 卡，晶片為 MediaTek MT7610U，對應 Linux 內建驅動 `mt76x0u`。它是 AWUS036ACM（MT7612U、2T2R）的單流姊妹款：規格上是 1T1R（AC600），少了一條空間串流，但換來更小的體積與社群公認的長距離接收。morrownr/USB-WiFi 社群把它列入 Kali 推薦清單與「The Short List」，並標注 VIF、Active monitor、WPA3 皆為 Yes、Very Long range、單流、in-kernel。

我們把它插上 ASUS GX10（NVIDIA GB10、128GB UMA、ARM64），在 Ubuntu 24.04 LTS、kernel 6.17 上逐項量測 Monitor、Injection、AP 與 WPA3-SAE。先講結論：這張卡在本平台能用，2.4GHz 的能力也相當完整。但有兩個相容雷得先知道：開 AP 必須關 802.11n，WPA3 必須設 `sae_pwe=0`；另外 5GHz 的逐台 injection 本次只驗到廣播。下表是整體速覽：

| 能力項目 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor（側錄） | ✅ | ✅ |
| Injection（注入） | ✅ 96–100% | ⚠️ 僅廣播可用，逐台回應率未取得 |
| AP 熱點 | ✅（須純 802.11g） | ✅（須純 802.11a，20 MHz） |
| WPA3-SAE | ✅（須 `sae_pwe=0`） | 未實測 |

> 圖例：✅ 實測通過 ｜ 🟡 部分或單機可成立 ｜ ⚠️ 有限制 ｜ ❌ 不支援或失敗。

## 2. 硬體與驅動（免裝）

ACHM 插上 GX10 後，kernel 6.17 內建的 `mt76x0u` 直接辨識，不需要 DKMS、不需要額外韌體、也不必從 GitHub 編 out-of-tree 驅動。確認網卡的三個指令：

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

介面名以 MAC 命名（`wlx<MAC>`），重插卡後名稱不變，寫腳本時可直接綁定。`iw phy info` 宣告支援的介面模式包含 `managed`、`AP`、`monitor`、`mesh point`、`IBSS`、`P2P-client`、`P2P-GO`，涵蓋本文要測的全部情境。

平台共通的兩條安全守則，在 ACHM 上一樣適用：第一，絕不執行 `airmon-ng check kill`，那會關掉 NetworkManager，讓 GX10 對外斷線；第二，全程只操作 `wlx*` 介面，不碰內建的 `wlP9s9`（GX10 對外上網主線）。要進 monitor／AP 一律用 `iw` 搭配 `nmcli dev set $IF managed no`，不動到系統主網卡。

## 3. 實測能力：Monitor / Injection / AP / WPA3

### 3-1. Monitor（2.4 + 5 GHz）✅

兩個頻段的側錄都正常。2.4GHz 第 6 頻道，8 秒就收滿 300 封包的擷取上限；5GHz 依頻率活動量不同：ch36（5180）8 秒收滿 300、5745 收 254、5785 收 54（某頻道封包少通常代表當下該頻道沒有活躍 AP，不是網卡問題）。

跳頻全頻掃描最能看出單天線卡的接收實力：

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

實測 120 秒掃出 19 個基地台、14 個用戶端，分布在 ch1/2/5/6/36/149/157。對一張單流 AC600 卡來說，這個涵蓋度足以當穩定的側錄來源，也呼應社群給它的「Very Long range」評價。

### 3-2. Injection（2.4 + 5 GHz）

這是 ACHM 兩個頻段差異最明顯的地方，也是選型時要特別留意的一項。

2.4GHz 第 6 頻道做 `aireplay-ng --test` 能力自測，結果漂亮：

```text
Injection is working!
Found 4 APs
30/30: 100%
```

四台基地台的回應率落在 96–100%，注入能力完整。

但切到 5GHz（ch36 與 ch149 都試過）就不一樣：

```text
Injection is working!
Found 0 APs
```

也就是說，5GHz 的廣播注入可用（driver 回報 `Injection is working!`），但 `aireplay-ng --test` 的逐台回應率，在兩個 5G 頻道都是 `Found 0 APs`，本次沒有取得百分比。這是 ACHM 這張單天線卡在本平台的實測現象，原因待追查，我們不替它補一個沒量到的數字。老實說：如果你的用途需要穩定的 5GHz 逐台注入，ACHM 本次只在 2.4GHz 驗到完整注入率。

### 3-3. AP 熱點（2.4 + 5 GHz）✅ — 但必須關 802.11n

ACHM 的第一個相容雷在這裡。開 AP 時，hostapd 設定檔不要加 `ieee80211n=1` 與 `ht_capab`：2.4GHz 走純 `hw_mode=g`、5GHz 走純 `hw_mode=a`（20 MHz）。一個最小可用的 2.4GHz 設定長這樣：

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 純 802.11g, 不要加 ieee80211n=1 或 ht_capab
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=請改成你的密碼至少8碼
```

實測 iPhone 7 Plus 兩頻都連入：2.4GHz 可見 `AP-STA-CONNECTED` 接著 `EAPOL-4WAY-HS-COMPLETED`；5GHz（ch36、20 MHz）測到 -71 dBm、rx 54 Mbit、`authorized: yes`。

反過來，如果設定檔保留了 `ieee80211n=1`，hostapd 會反覆噴 `handle_assoc_cb: STA not found`，iPhone 畫面顯示「無法加入網路」或「密碼錯誤」，但那其實是 802.11n 關聯失敗，不是密碼問題。移除 802.11n 就好。ACHM 是單天線卡，5GHz AP 本次採 20 MHz，沒試 VHT80。

### 3-4. WPA3-SAE ✅ — 但必須 `sae_pwe=0`（最容易踩的相容雷）

ACHM 的第二個、也是最值得單獨講的相容雷。WPA3-SAE 的 hostapd 以 `sae_pwe` 控制密碼元素（password element）的推導方式：`0` 是只用傳統 Hunting-and-Pecking、`1` 是只用 Hash-to-Element（H2E）、`2` 是兩者並存（同時支援 Hunting-and-Pecking 與 H2E）。差別直接決定舊 iPhone 連不連得上：

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 強制 PMF
ieee80211w=2
# 關鍵: 相容 iPhone 7 Plus 這類舊端點
sae_pwe=0
sae_password=請改成你的密碼
```

實測對照：

- `sae_pwe=0`：iPhone 15 Pro 與 iPhone 7 Plus **都連入**（`authorized: yes`、`MFP: yes`）。
- `sae_pwe=2`：iPhone 7 Plus 會**關聯成功但 4-way 金鑰交握失敗而斷線**，表面上看起來又像「密碼錯誤」；iPhone 15 Pro 則可以連。

結論很直接：要相容舊 iPhone（含 iPhone 7 Plus 這類 2016 年機種），hostapd 一定要設 `sae_pwe=0`。改完設定後，請讓 iPhone 先「忘記此網路」再重連，避免殘留的關聯狀態造成假性失敗。這一點在 9 款總表上，ACHM 的 WPA3 欄位是以「✅*」加星號特別標注的。

## 4. 進階與限制

先用一張表收斂本次 ACHM 的完整涵蓋範圍與狀態，後續段落再就重點展開：

| 功能 | 狀態 | 本次實測重點 |
|---|---|---|
| Monitor（2.4 + 5 GHz） | ✅ | 跳頻 120 秒掃到 19 AP + 14 client |
| Injection 2.4 GHz | ✅ | 回應率 96–100% |
| Injection 5 GHz | ⚠️ | 廣播可用，逐台回應率未取得 |
| AP（2.4 + 5 GHz） | ✅ | iPhone 兩頻連入，須關 802.11n |
| WPA3-SAE | ✅* | 於 2.4 GHz 實測（5 GHz 未實測）；新舊 iPhone 皆連入，須 `sae_pwe=0` |
| VIF（STA+AP、AP+monitor） | ✅ | 邊上網邊當熱點，下載 198 Mbit/s |
| WPA handshake 擷取 | ✅ 端到端（.22000，5 GHz ch36） | deauth 自有 iPhone，擷取完整 4-way M1–M4，轉出 hashcat `.22000` |
| Active monitor | 🟡 | 可設定側錄，ACK 未驗 |
| Ad-hoc（IBSS） | 🟡 | 單機可建立，未與第二台互連 |
| Mesh（802.11s） | 🟡 | 單機可加入，未 peer link |
| Wi-Fi Direct（P2P） | ⬜ | 需第二台設備，略過 |

> ✅* ＝ WPA3-SAE 可用但須 `sae_pwe=0`；詳見第 3-4 節。

**VIF（虛擬介面，同頻道、最多 2 介面）。** ACHM 支援同一張卡切出多個介面同時運作，前提是各 VIF 用不同 MAC、AP VIF 不交給 NetworkManager 管、所有 VIF 同頻道，ACHM 另需 AP 關 802.11n。兩種組合都實測過：

- **STA + AP（一邊上網一邊當熱點）**：iPhone 7 Plus 連入 AP（-66 dBm、authorized）的同時，主介面連上 YUPITEK，ping 30/30、avg 3.2 ms、下載 198 Mbit/s。
- **AP + Monitor**：開著 AP 的同時側錄，8 秒擷取 300 frame，其中含 46 個自家 AP 的 beacon。

**handshake 擷取。** ACHM 在 5 GHz（ch36）完成端到端流程：deauth 自有 iPhone、擷取完整 4-way（M1–M4）並轉出 hashcat `.22000`，是 9 款中完成端到端的 7 款之一（ACM、ACHM、ACH、ACS、EACS、AX、AXER）。5GHz 的逐台注入回應率（`aireplay-ng --test`）仍未取得。

**mesh / IBSS（單機可建立）。** 這是 mt76 家族相對 Realtek rtw88/rtw89 的差異點。IBSS（Ad-hoc）約 9 秒就 `Joined IBSS`、能發出 beacon；Mesh（802.11s）可進入 `type mesh point`、發出 mesh beacon。兩者本次都是單機成立、沒跟第二台互連（缺第二台設備而略過），所以標 🟡。Realtek 的 rtw88/rtw89 卡（如 AWUS036ACH）在本平台雖可建立單機 IBSS，但不支援 802.11s mesh，所以要做 802.11s mesh 實驗，ACM 與 ACHM 這兩張 mt76 卡反而是少數選擇。

**Active monitor 🟡。** 可設定、側錄正常，但 ACK 回應行為需要第二台設備才能驗證，本次未驗。

**Kali 工具（平台層級，與其他卡共通）。** `airmon-ng`、`kismet`、`bettercap`、`wifite`（git 版）、Wireshark/tshark 都可把 ACHM 當來源使用；只有 `hcxdumptool` 在本平台 `failed to arm interface`（AWUS036EACS 在 2.4 GHz 為例外；內建驅動無 active-monitor 支援），擷取請改用 `airodump-ng` 搭配 aircrack-ng 套件。ARM64 另需注意：`aircrack-ng` 常缺 prebuilt package 要自原始碼編譯、`wifite` 建議用 GitHub 版以繞過 apt 依賴衝突。

## 5. 適用情境與選型（連回 Hub）

把 ACHM 放回 9 款的選型脈絡，它的位置很清楚：

**適合**

- **mesh（802.11s）實驗**：mt76 驅動單機可建立 802.11s mesh（與 IBSS）；Realtek 卡可建立單機 IBSS，但做不到 802.11s mesh。
- **長距離單流 monitor 側錄**：跳頻 120 秒掃到 19 AP + 14 client，社群評為 Very Long range。
- **2.4GHz injection、以及 AP / WPA3 熱點**：2.4G 注入 96–100%，WPA3 設對 `sae_pwe=0` 後新舊 iPhone 都連得上。

**要留意（誠實限制）**

- 5GHz 逐台 injection 本次只驗到廣播，沒有百分比。
- 開 AP 要關 802.11n、WPA3 要 `sae_pwe=0`，兩個設定不對都會讓舊 iPhone「看起來像密碼錯誤」。
- 單天線 1T1R，吞吐與定位和 2T2R 的 ACM／ACH 不同級。

**選型指引**：如果你的核心需求是兩頻穩定注入加端到端 handshake，9 款裡 AWUS036EACS / AWUS036ACH / AWUS036ACS 更合適；要 Wi-Fi 6 + AP 熱點就看 AWUS036AX / AWUS036AXER；若主打 mesh / IBSS 單機實驗或長距離側錄，ACHM（或它的 2T2R 姊妹 ACM）才是對的工具。最後提醒避雷：injection / handshake 用途別選 AWUS036AXM / AXML，這兩張的 MT7921 注入在本平台是失敗的。

完整的 9 型號硬體、驅動、Monitor / Injection / AP / WPA3 全矩陣與依用途的選型總評，見 Hub 總表：[9 款 ALFA 無線網卡 ARM64 / GX10 實測總矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 常見問題（FAQ）

**Q：AWUS036ACHM 在 Ubuntu 24.04 需要裝驅動嗎？**
不需要。MT7610U 由 kernel 內建的 mt76x0u 驅動接管，Ubuntu 24.04（kernel 6.17）插上即認，不用 DKMS、不用額外韌體；lsusb 可看到 USB ID 0e8d:7610。

**Q：AWUS036ACHM 能進 monitor mode 嗎？能掃到多少 AP？**
能。2.4GHz 與 5GHz 都能進 monitor mode；用 airodump-ng 跳頻全頻掃描 120 秒，實測掃到 19 個 AP、14 個用戶端，分布在 ch1、2、5、6、36、149、157。

**Q：AWUS036ACHM 的封包注入成功率多少？5GHz 可以嗎？**
2.4GHz 第 6 頻道逐台注入回應率 96–100%（aireplay-ng --test，找到 4 台 AP）。5GHz（ch36、ch149）只驗到廣播注入可用，逐台測試回報 Found 0 APs，本次沒有取得百分比，原因待查。

**Q：AWUS036ACHM 開 AP 時 iPhone 顯示「無法加入網路」或「密碼錯誤」怎麼辦？**
先關掉 802.11n：hostapd 設定檔不要加 ieee80211n=1 與 ht_capab，2.4GHz 用純 hw_mode=g、5GHz 用純 hw_mode=a（20 MHz）。否則 hostapd 會反覆出現 handle_assoc_cb: STA not found，畫面像密碼錯誤，其實是 802.11n 關聯失敗。

**Q：AWUS036ACHM 的 WPA3-SAE 為什麼舊 iPhone 連不上？**
多半是 hostapd 的 sae_pwe 設定。實測 sae_pwe=0 時 iPhone 7 Plus 與 iPhone 15 Pro 都連得上；sae_pwe=2 時 iPhone 7 Plus 會關聯成功但 4-way 交握失敗而斷線，看起來像密碼錯誤。請搭配 ieee80211w=2，改完設定後讓 iPhone 先忘記此網路再重連。

## 6. 延伸閱讀

- 〔Hub 總表〕9 款 ALFA 無線網卡在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP 全矩陣與選型總評 → [/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 〔姊妹款〕AWUS036ACM（MT7612U / 2T2R）逐卡實測 — 內鏈待補（placeholder）
- 〔平台教學〕免裝驅動：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驅動啟用 ALFA 網卡 Monitor 與 AP — 內鏈待補（placeholder）
- 〔專題〕WPA3-SAE 時代的 handshake 擷取能力與 `sae_pwe` 相容性雷區 — 內鏈待補（placeholder）

---

*測試單位：Yupitek（ALFA Network 台灣經銷）— https://www.yupitek.com ｜ 測試環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）。數據引用自 2026-11-16～11-18 的實機測試報告，不針對任何第三方網路，亦不提供攻擊操作步驟。*
