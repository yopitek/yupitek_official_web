---
title: "AWUS036AXER 實測報告：ASUS GX10 + Ubuntu 24.04（ARM64）上接收最強的 Wi-Fi 6 網卡"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER 在 ASUS GX10／Ubuntu 24.04 ARM64 免裝驅動（rtw89_8852bu）：monitor 60 秒掃到 63 AP＋12 client，注入 73%（2.4G）、5G VHT80 AP 與 WPA3 皆通過。"
faq:
  - question: "AWUS036AXER 在 Ubuntu 24.04 或 Kali 需要另外裝驅動嗎？"
    answer: "在 Ubuntu 24.04（ARM64，kernel 6.17.0-1014-nvidia）不用：內建的 rtw89_8852bu 驅動插上即辨識，免編譯、免 DKMS（firmware rtw8852b_fw 0.29.29.5）。本文平台是 Ubuntu 而非 Kali 發行版，Kali 本體未測；Kali 常用工具 airmon-ng、kismet、bettercap、wifite、Wireshark 在此平台可使用。kernel 較舊時不保證內建，請先確認版本。"
  - question: "AWUS036AXER 支援 monitor mode 嗎？接收有多強？"
    answer: "支援，2.4 GHz 與 5 GHz 都能進 monitor。我們在自有辦公室用 airodump-ng 跳頻掃描 60 秒，掃到 63 個 AP 與 12 個 client，是我們同場測試的九款卡中接收最強的一張；同晶片的 AWUS036AX 另次測試為 14 AP＋4 client（兩次非同步量測，僅供參考）。"
  - question: "AWUS036AXER 能做封包注入（packet injection）嗎？"
    answer: "可以。2.4 GHz 的 aireplay-ng --test 回應率 73%（22/30）並顯示 Injection is working!，5 GHz 逐台自測也通過；我們在自有網路與自有裝置上完成 handshake 擷取並轉出 .22000。若要兩頻接近 100%，本平台實測以 AWUS036EACS、ACH、ACS 更穩。僅限自有或已授權的網路。"
  - question: "AWUS036AXER 和 AWUS036AX 差在哪？"
    answer: "兩者同為 Realtek RTL8832BU、同用 rtw89_8852bu，在本平台的模式支援與注入行為一致；差別在天線調校與增益帶來的接收表現（AXER 60 秒 63 AP＋12 client，AX 為 14 AP＋4 client）。兩者皆為內嵌天線、無 RP-SMA，天線規格請以產品頁為準。"
  - question: "AWUS036AXER 可以當 AP 或開 WPA3 嗎？不支援哪些模式？"
    answer: "可以。2.4 GHz 802.11n 與 5 GHz VHT80（VHT-NSS2、351 Mbit）都有 iPhone 連入並 authorized；WPA3-SAE 以 sae_pwe=0 讓 iPhone 15 Pro 連入（於 2.4 GHz；5 GHz 的 WPA3 未實測）；STA＋AP 並行可用。但 rtw89_8852bu 不支援 active monitor、IBSS、mesh。"
draft: false
---

{{< tldr >}}AWUS036AXER 在 ASUS GX10／Ubuntu 24.04 ARM64 插上即用（內建 rtw89_8852bu）；monitor 60 秒掃到 63 AP＋12 client，2.4 GHz 注入 73%，AP 與 WPA3 皆通過；不支援 active monitor、IBSS、mesh。{{< /tldr >}}

> 本文為 Yopitek（ALFA 台灣經銷）於自有設備上的產品相容性與能力實測。
> 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。測試環境為自有辦公室 Wi-Fi（SSID `YUPITEK`），對自有測試手機 iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）進行。
> ⚠️ **合法使用**：Monitor 與 Injection 僅限自己擁有或已取得授權的網路與裝置；AP 模式請遵守當地無線電法規。本文聚焦網卡能力、相容性、設定與選型，不涉及針對第三方網路的任何攻擊操作。

---

## 1. 這張卡與測試平台

AWUS036AXER 是 ALFA 的 Wi-Fi 6（802.11ax）2x2 USB 網卡，採 Realtek RTL8832BU 晶片（無藍牙）。它與同廠的 AWUS036AX 用的是**同一顆晶片、同一支驅動**（`rtw89_8852bu`），在本平台上的模式支援與行為一致；兩者真正的差別在**天線調校與增益**，而不是外接或內建——AXER 採**內嵌（Nano）天線設計、無 RP-SMA**，靠晶片與 RF 調校把接收拉到最滿。先記住這篇的核心結論：在我們同場比較的九張 ALFA 卡裡，AXER 的**接收是最強的一張**。

測試平台為 ASUS GX10，搭載 NVIDIA GB10 超級晶片與 128GB 統一記憶體，作業系統 Ubuntu 24.04 LTS、架構 ARM64（aarch64）、kernel `6.17.0-1014-nvidia`。所有結果均於 2026-11-18 在這台機器實機跑出，測試裝置為自有的 iPhone 7 Plus（WPA3 另測 iPhone 15 Pro），測試網路為自有辦公室 Wi-Fi。對經銷驗證而言，ARM64 搭配新版 kernel 是相對嚴苛的組合，底下第 2 節會說明為什麼這一代反而更省事。

補一點規格脈絡：AXER 是 2x2（雙空間串流）的 Wi-Fi 6 卡，可同時收發兩條空間串流，這也對應到後面 5 GHz AP 實測協商出的 VHT-NSS2。但這張卡在本輪勝出，靠的是天線設計與 RF 調校，不是串流數（AX 同樣是 2x2）。晶片、驅動、平台三者全部相同，天線調校幾乎是唯一變因，所以 AXER 和 AX 的接收差距可以乾淨地歸到內嵌天線設計與增益調校。

---

## 2. 硬體與驅動（內嵌天線，免裝驅動）

AWUS036AXER 在 Ubuntu 24.04 的 6.17 kernel 上**插上即認、免編譯、免 DKMS**。驅動 `rtw89_8852bu` 已經是 in-kernel 模組，firmware 為 `rtw8852b_fw`（版本 0.29.29.5），開機即載入，不需要再去 GitHub 抓 out-of-tree 專案或綁 DKMS。對需要長期維運、跨多次 kernel 更新的經銷與教學環境來說，少掉編驅動這一步就是少掉一個最常見的故障點。

對照舊路會更有感：過去 Realtek 這類 USB 晶片多半沒進 mainline kernel，使用者得從 GitHub 抓 out-of-tree 專案（例如 `morrownr/USB-WiFi`）再用 DKMS 綁當前 kernel 編譯，每逢 kernel 更新就要重編一次，一旦編譯失敗網卡就直接消失。rtw89 正式納入 in-kernel 之後，這些步驟在 6.17 上可以整段省略，同一套操作也能跨多張同驅動的卡重複沿用。

先確認卡被正確辨識：

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

正常 WLAN 模式的 USB ID 是 `0bda:b832`。如果看到的是 `0bda:1a2b`，代表卡還停在「光碟模式」（CD-ROM mode），執行一次 `sudo usb_modeswitch -v 0bda -p 1a2b -K` 切成 WLAN 模式即可；本測試單位這張卡是直接以 WLAN 模式列舉，沒有遇到光碟模式。

介面名稱採 `wlx` + MAC 命名（例如 `wlxAABBCCDDEEFF`），插在哪台機器都不會變，方便腳本固定綁定。查詢這張卡支援哪些模式：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

實測回報的模式為 managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO。這裡沒有 IBSS、mesh，也沒有 active monitor，這是 rtw89 驅動的先天限制，第 4 節會誠實說明，別在選型時誤判。

天線部分：AXER 採內嵌（Nano）天線設計、無 RP-SMA，和同晶片的 AX 相比，差別在天線調校與增益，實務上最直接的反映就是收訊。下一節的 monitor 數據會把這點講清楚。

---

## 3. 實測能力

把三項核心能力（Monitor / Injection / AP）與 WPA3 的實測結果先列成一張表，細節在表後逐項展開：

| 能力 | 2.4 GHz | 5 GHz | 實測重點 |
|---|---|---|---|
| **Monitor（監聽）** | ✅ 強 | ✅ 強 | 跳頻掃到 **63 AP + 12 client**，九張卡中接收最強 |
| **Injection（注入）** | ✅ 73% | ✅ 可用 | 2.4G `22/30 73%`；5G `Injection is working!` |
| **AP（熱點）** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone 連入；5G VHT-NSS2、351 Mbit |
| **WPA3-SAE** | ✅ | 未實測 | AP 端 iPhone 15 Pro 連入（`sae_pwe=0`）；僅在 2.4 GHz 實測 |
| **WPA handshake 擷取** | ✅ 端到端 | — | 自有網路＋自有裝置，4-way（M1–M4）→ `.22000` |

### 3-1. Monitor（本篇亮點：接收最強）

切 monitor 是標準的 `iw` 流程：先把介面交回自己管（`nmcli dev set $IF managed no`）、關介面、設 monitor type、開介面、設頻道：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; 2.4 GHz 用 channel 6
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

2.4 GHz 與 5 GHz 各在 6 秒內收滿 100 frames。真正拉開差距的是跳頻掃描：`sudo airodump-ng --band abg $IF` 跑 60 秒，**掃到 63 個 AP 加 12 個 client**。這是本輪九張卡裡抓到最多目標的一張，直接反映內嵌天線設計與 RF 調校帶來的接收優勢。對於現場盤點（site survey）、長距離監聽、或是訊號偏弱的環境，這個接收能力就是 AXER 的核心價值。

### 3-2. Injection（注入）

Injection 用 aireplay-ng 的自測模式驗證，測的是網卡本身的能力，不是對外攻擊：

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

2.4 GHz 回應率 73%（22/30），判定為可用。5 GHz 逐台對指定 AP 自測也回報 `Injection is working!`。補一個平台通則：**5 GHz 要發送/注入前，先 `iw reg set US` 解鎖 TX 功率，測完記得 `iw reg set TW` 切回台灣法規頻段**。

### 3-3. AP 熱點（2.4 GHz 802.11n、5 GHz VHT 80 MHz）

AXER 兩個頻段都能起 hostapd AP。2.4 GHz 以 `hw_mode=g` + `ieee80211n=1` 起 802.11n 熱點，iPhone 7 Plus 連入協商到 MCS 15、authorized。5 GHz 以 `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1` 起 VHT 80 MHz 熱點，iPhone 7 Plus 連入協商到 **VHT-NSS2、80 MHz、351 Mbit、authorized**。起 AP 的前置是 `sudo nmcli dev set $IF managed no`，`wpa_passphrase` 至少 8 碼，否則 hostapd 會回 `invalid WPA passphrase length`。

### 3-4. WPA3-SAE 與 handshake 擷取

WPA3-SAE 在 AP 端設 `wpa_key_mgmt=SAE`、`ieee80211w=2`、`sae_pwe=0`，實測 iPhone 15 Pro 連入。**`sae_pwe` 是 ALFA 這批卡上的相容性雷區**：部分裝置在 `sae_pwe=2`（Hash-to-Element）時連不上，設 `sae_pwe=0` 可相容較舊的 iPhone。

handshake 能力則是在**自有辦公室 Wi-Fi（YUPITEK）＋ 自有測試裝置**上做的端到端驗證：擷取到完整 4-way（M1/M2/M3/M4），再用 `hcxpcapngtool` 轉出 hashcat 可讀的 `.22000`。這裡要點出一個 GX10 平台的共通現象：**`hcxdumptool` 在本平台除 AWUS036EACS 的 2.4 GHz 外，所有 USB 卡都會 `failed to arm`**（GX10 三頻內建網卡列舉衝突，加上驅動沒有 active monitor），所以 handshake 流程改走 aircrack-ng 套件（airodump-ng + aireplay-ng）。AXER 的注入能力在這條路上是夠用的。

---

## 4. 進階功能與誠實限制

**VIF（STA + AP 並行）✅**：AXER 可以同時當 station 連上游 Wi-Fi、又開一個 AP VIF。實測主介面連 YUPITEK、AP VIF 開在 ch36 VHT80 並行，STA 端 ping 3.5 ms，適合要「邊連網邊開熱點」的場景。

**Wi-Fi Direct（P2P）未測（⬜）**：驅動有宣告 P2P-client / P2P-GO，但要完整驗證需要第二台對接設備，本輪略過，因此不列入已驗證能力。這類「驅動宣告支援、但未實機跑過」的項目，我們一律誠實標為未測，不灌水當成通過。

**不支援的三個模式（N/A）**：`rtw89_8852bu` 驅動**不提供 active monitor、Ad-hoc（IBSS）、Mesh（802.11s）**。`iw dev $IF set type ibss` 或 `mp` 會直接失敗，這是驅動層的限制，無法用設定繞過。如果用途是 mesh 或 IBSS 實驗，要改看 MediaTek mt76 系列（如 AWUS036ACM / ACHM）。

**平台共通注意事項：**

- 絕對不要跑 `airmon-ng check kill`，它會關掉 NetworkManager，讓 GX10 對外斷線。只操作 `wlx*` 介面，不要碰內建的對外上網網卡。
- 反覆切 monitor/AP 後若突然掃不到東西（RX stall），把卡**拔插一次**即可復原（USB 重列舉，介面名由 MAC 決定，不會變）。
- ARM64 平台上 aircrack-ng 需要自原始碼編譯；wifite 用 git 版，繞過 apt 依賴衝突。

**Kali 工具相容性**：airmon-ng、kismet 2026.10、bettercap 2.32、wifite（git）、Wireshark / tshark 4.2 都能正常把 AXER 當資料來源或管理介面使用。

---

## 5. 適用情境與選型建議

一句話定位：**AXER 是「接收取向」的 Wi-Fi 6 卡**。它和 AX 同晶片、功能一致，差別在天線調校與增益帶來的收訊優勢，所以選型邏輯很清楚：

| 你的需求 | AXER 是否首選 | 說明 |
|---|---|---|
| 最強接收 / 長距離 monitor / 現場盤點 | ✅ **首選** | 跳頻掃到 63 AP + 12 client，九張卡最強；可搭 AWUS036ACH（雙天線高增益）互補 |
| Wi-Fi 6 + AP 熱點 | ✅ 適合 | 2x2、5G VHT80；與 AWUS036AX 同級 |
| Injection + 端到端 handshake | 🟡 可用 | 2.4G 73% 可用；若要兩頻接近 100%，AWUS036EACS / ACH / ACS 更穩 |
| mesh / IBSS 實驗 | ❌ 不適合 | rtw89 不支援，改用 AWUS036ACM / ACHM（mt76） |

典型落地場景：把 AXER 當成**遠端無線監測節點**，放在訊號較弱或距離較遠的點位，靠它內嵌天線的接收優勢把現場的 AP / client 盡量收全，掃描結果再彙整回中央主機統一檢視。由於是內嵌（Nano）天線、無 RP-SMA，天線不可更換；需要更高增益或更強指向性時，改搭雙天線高增益的 AWUS036ACH 互補即可。

反過來說，如果用途是純 AP 或一般連線、完全不需要注入，MediaTek 的 AWUS036AXM / AXML 也能用；但**只要牽涉注入或 handshake，就不要選 AXM / AXML**，它們在本平台注入是失敗的（主因是 kernel 6.16 以後的 mac80211 chanctx 回歸，另有韌體把注入速率鎖在 1／6 Mbps，並非晶片本身的限制）。AXER 剛好相反：注入可用、接收又最強。

想一次看完九款卡的完整矩陣與交叉比較，可回到總評頁 → [`/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

---

## 常見問題（FAQ）

**Q1. AWUS036AXER 在 Ubuntu 24.04 或 Kali 需要另外裝驅動嗎？**
在 Ubuntu 24.04（ARM64，kernel 6.17.0-1014-nvidia）不用：內建的 `rtw89_8852bu` 驅動插上即辨識，免編譯、免 DKMS（firmware `rtw8852b_fw` 0.29.29.5）。本文平台是 Ubuntu 而非 Kali 發行版，Kali 本體未測；Kali 常用工具 airmon-ng、kismet、bettercap、wifite、Wireshark 在此平台可使用。kernel 較舊時不保證內建，請先確認版本。

**Q2. AWUS036AXER 支援 monitor mode 嗎？接收有多強？**
支援，2.4 GHz 與 5 GHz 都能進 monitor。我們在自有辦公室用 airodump-ng 跳頻掃描 60 秒，掃到 63 個 AP 與 12 個 client，是我們同場測試的九款卡中接收最強的一張；同晶片的 AWUS036AX 另次測試為 14 AP＋4 client（兩次非同步量測，僅供參考）。

**Q3. AWUS036AXER 能做封包注入（packet injection）嗎？**
可以。2.4 GHz 的 `aireplay-ng --test` 回應率 73%（22/30）並顯示 `Injection is working!`，5 GHz 逐台自測也通過；我們在自有網路與自有裝置上完成 handshake 擷取並轉出 `.22000`。若要兩頻接近 100%，本平台實測以 AWUS036EACS、ACH、ACS 更穩。僅限自有或已授權的網路。

**Q4. AWUS036AXER 和 AWUS036AX 差在哪？**
兩者同為 Realtek RTL8832BU、同用 `rtw89_8852bu`，在本平台的模式支援與注入行為一致；差別在天線調校與增益帶來的接收表現（AXER 60 秒 63 AP＋12 client，AX 為 14 AP＋4 client）。兩者皆為內嵌天線、無 RP-SMA，天線規格請以產品頁為準。

**Q5. AWUS036AXER 可以當 AP 或開 WPA3 嗎？不支援哪些模式？**
可以。2.4 GHz 802.11n 與 5 GHz VHT80（VHT-NSS2、351 Mbit）都有 iPhone 連入並 authorized；WPA3-SAE 以 `sae_pwe=0` 讓 iPhone 15 Pro 連入（於 2.4 GHz；5 GHz 的 WPA3 未實測）；STA＋AP 並行可用。但 `rtw89_8852bu` 不支援 active monitor、IBSS、mesh。

---

## 6. 延伸閱讀

- 九款 ALFA 卡總矩陣與選型總表（Monitor・Injection・AP 全比較）→ `/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- 同晶片的 AWUS036AX 實測（天線調校不同） → `/zh-tw/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- 免裝驅動：in-kernel 驅動啟用 Monitor 與 AP 模式 → `/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- WPA3-SAE 時代的 handshake 擷取能力與 `sae_pwe` 相容性 → `/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- 延伸閱讀內鏈待定稿後補上正式 hreflang 對應 URL；上列為 zh-TW slug placeholder。 -->

---

*測試單位：Yopitek（ALFA 經銷）— https://www.yupitek.com ｜ 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）*
