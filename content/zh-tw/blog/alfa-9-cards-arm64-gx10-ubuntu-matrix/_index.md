---
title: "2026 最完整實測：9 款 ALFA 無線網卡在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP 全矩陣"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "實測 9 款 ALFA Wi-Fi USB 網卡在 Ubuntu 24.04 ARM64（GX10）的 Monitor、Injection、AP 與 WPA3-SAE 表現，含 Kali 常用工具相容性與選型建議，AWUS036ACH / EACS 注入達 100%。"
faq:
  - question: "AWUS036AXM 在 Ubuntu 能注入（injection）嗎？"
    answer: "在本平台不能。實測中 AWUS036AXM 與 AWUS036AXML（皆為 MT7921 晶片）在 2.4GHz 與 5GHz 的 injection 皆失敗，主因是 stock kernel 6.16+ 的 mac80211 chanctx 回歸（非晶片先天），因此不建議在本平台用於需要注入或 handshake 擷取的用途。"
  - question: "哪一款 ALFA 網卡在 Ubuntu 上 injection 成功率最高？"
    answer: "實測中 AWUS036ACH 與 AWUS036EACS 在 2.4GHz 與 5GHz 的 injection 成功率皆達 100%，是本批 9 款中表現最好的兩款。"
  - question: "9 款 ALFA 網卡在 Ubuntu 24.04 需要另外裝驅動嗎？"
    answer: "不需要。9 款在 kernel 6.17 上全部走 kernel 內建（in-kernel）驅動（rtw88 / rtw89 / mt76 家族），插上即被辨識，不需編譯 DKMS 模組。"
  - question: "ALFA 網卡在 Ubuntu 可以架 WPA3-SAE 的熱點嗎？"
    answer: "可以，9 款實測都能成功架設 WPA3-SAE 熱點並讓裝置連入（除 ACS 於 5 GHz 實測外，其餘皆於 2.4 GHz 實測；AXML 另於 6 GHz 實測）；唯 AWUS036ACHM 需把 hostapd 的 sae_pwe 設為 0，否則舊款 iPhone 7 Plus 會連線失敗。"
  - question: "這份 Ubuntu 的測試結果，Kali Linux 使用者可以參考嗎？"
    answer: "Kali Linux 基於 Debian/Ubuntu 體系，使用同一套 rtw88 / rtw89 / mt76 in-kernel 驅動，因此本文的驅動相容性與能力矩陣原則上可作為 Kali 使用者的參考依據；但本文實測平台為 Ubuntu 24.04，尚未在 Kali 上正式複測，結果請以日後複測為準。"
draft: false
---

## 重點摘要（TL;DR）

Yupitek（ALFA Network 台灣經銷）在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）實測 9 款 ALFA USB 無線網卡：9 款都能進 monitor mode 並當 AP，AWUS036ACH 與 AWUS036EACS 兩頻注入達 100%，MT7921 的 AWUS036AXM / AWUS036AXML 在本平台注入失敗。

- **Monitor 全員可用**：9 款都能進 monitor mode，差別只在收訊強弱。
- **Injection 是分水嶺**：Realtek `rtw88` 的 ACH、EACS 兩頻注入達 100%，ACS 次之；MT7921 的 AXM / AXML 在本平台注入失敗。
- **端到端 handshake（擷取 → 轉出 `.22000`）已實證，9 款中共 7 款**：ACM、ACHM、ACH、ACS、EACS、AX、AXER。
- **AP 與 WPA3-SAE 幾乎全員過關**：僅 AWUS036ACHM 需設 `sae_pwe=0` 以相容舊款 iPhone。
- **ARM64 免編譯**：9 款全走 kernel 6.17 內建驅動，插上即用、免 DKMS。

Yupitek 是 ALFA Network 的台灣經銷商。客戶選購 USB 無線網卡時，最常問的三個問題幾乎都一樣：「這張卡在我的 Linux 環境能不能進 monitor mode？能不能做 injection？能不能架 AP？」與其憑規格表回答，我們直接把 9 款現役 ALFA 網卡搬上自家實驗桌，在 **ASUS GX10（ARM64）** 搭配 **Ubuntu 24.04 LTS** 的環境逐張實測，把 Monitor、Injection、AP、WPA3-SAE 四條能力線一次拉出來比較，並且誠實標注哪幾張「在這個平台做不到什麼」。

需要先講清楚定位：本文所有測試都在 Yupitek 自有的設備與自有辦公室 Wi-Fi 上完成，對象是我們自己的測試手機。這是經銷商對產品相容性與能力邊界的硬體驗證，不是針對第三方網路的攻擊教學。文中不提供任何對外部網路的操作步驟；injection 與 handshake 相關能力，一律在自有封閉環境、對自有裝置量測。

這是一篇總表型的 Hub 文章。每一張卡的逐步設定與完整證據，會另外拆成單卡深入文（見文末延伸閱讀）。

## 測試平台與方法

- **運算平台**：ASUS GX10（ARM64 / aarch64）
- **作業系統**：Ubuntu 24.04 LTS
- **核心版本**：kernel 6.17.0-1014-nvidia
- **驅動策略**：9 款全部使用 kernel 內建（in-kernel）驅動，插上即辨識，不安裝任何第三方 DKMS 模組
- **測試裝置**：Apple iPhone 7 Plus（WPA3-SAE 相容性另以 iPhone 15 Pro 複測）
- **測試環境**：自有辦公室 Wi-Fi，SSID `YUPITEK`，2.4GHz ch5 / 5GHz ch36、ch157
- **測試期間**：2026-11-16 至 2026-11-18 實機量測

方法上，我們對每張卡都跑同一組流程：先確認驅動載入與介面生成（`wlx*`），再依序驗證 2.4GHz / 5GHz 的 monitor、injection、AP 與 WPA3-SAE 連線，最後對自有測試手機做端到端 handshake 擷取鏈路的驗收。每一項結果都以實際量到的數字或狀態記錄，不以規格書推測。

本文表格採用以下圖例：

> ✅ 通過 ｜ 🟡 部分或單機可成立 ｜ ⚠️ 有限制 ｜ ❌ 不支援或測試失敗 ｜ N/A 驅動不具此模式 ｜ ⬜ 未測（缺第二台設備）

## 一、硬體與驅動對照

先看 9 款的硬體底細與在 kernel 6.17 上實際掛載的驅動。

| # | 型號 | 晶片 | USB ID | 驅動（in-kernel） | 韌體 | 世代 / 串流 | 備註 |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | morrownr 推薦 Kali 卡 |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R（AC600） | 單天線 |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R（AC1200） | 雙天線高增益 |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | 輕量隨身 |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | BT + WiFi 複合 |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | 同晶片，內嵌天線（Nano） |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

幾個重點：

**兩大驅動陣營。** 9 款分屬 MediaTek（`mt76x2u` / `mt76x0u` / `mt7921u`）與 Realtek（`rtw88_*` / `rtw89_8852bu`）兩套 in-kernel 驅動。晶片世代涵蓋 Wi-Fi 5（6 款）與 Wi-Fi 6（3 款：AX、AXER 走 `rtw89_8852bu`；AXM、AXML 走 `mt7921u`）。

**ARM64 上最實際的優勢是「免編譯」。** 這 9 款在 kernel 6.17 全走 in-kernel 驅動，插上即被辨識，不需要在 aarch64 上處理 out-of-tree DKMS 模組。這點在 ARM64 上特別有感：許多第三方 Realtek 驅動缺 aarch64 的 prebuilt，往往得自原始碼編譯、對核版，踩雷機率高。這批卡直接免除這段流程。

**同晶片不同型號。** AWUS036AX 與 AWUS036AXER 是同一顆 RTL8832BU、同一支 `rtw89_8852bu` 驅動，差別在天線設計（AXER 採內嵌天線 Nano 設計，無 RP-SMA），這會反映在後面的收訊與注入數字上。

**兩款是 BT + WiFi 複合裝置。** AWUS036EACS（RTL8821CU）與 AWUS036AXML（MT7921AUN）同時帶藍牙，這個特性在重插卡時有個實務副作用，後面「平台注意事項」會說明。

## 二、核心能力矩陣：Monitor / Injection / AP / WPA3

這是本文的主表，也是選型時最該先看的一張。

| # | 型號 | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ 僅廣播 | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅（頻寬未確認） | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 6 | AWUS036AX | ✅ 強 | ✅ 強 | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ 強 | ✅ 強 | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ 弱 | ✅ 弱 | ❌ **失敗** | ❌ **失敗** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ 弱 | ✅ 弱 | ❌ **失敗** | ❌ **失敗** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* AWUS036ACHM 的 WPA3 需設 `sae_pwe=0`；在 `sae_pwe=2` 時 iPhone 7 Plus 連不上。
>
> WPA3-SAE 欄所標頻段為實際測過的頻段（除 ACS 於 5G 實測外，其餘皆為 2.4G；AXML 另於 6G 實測），其他頻段未實測。

逐項解讀：

**Monitor：9 款全數可用，差在收訊強弱。** 不論 2.4GHz 或 5GHz，9 款都能進 monitor mode，沒有例外。差別在掃描的積極度與收訊靈敏度：Wi-Fi 6 的 AX / AXER 收訊最強、掃描最積極；MT7921 的 AXM / AXML 可進 monitor，但相對弱。只需要被動側錄或頻譜盤點的話，9 款都能用。

**Injection：差距從這裡開始拉開。** Realtek `rtw88` 系列表現最好：ACH 與 EACS 在 2.4GHz / 5GHz 都達 **100%**，ACS 也有 2.4GHz 100% / 5GHz 96%。MediaTek `mt76` 的 ACM 可用但數字落在中段（2.4GHz 63–83%、5GHz 76%）；ACHM 的 5GHz 只能廣播、無法對特定目標注入。`rtw89` 的 AX / AXER 可注入，其中 AXER 的 2.4GHz 注入率（73%）比 AX（96%）低一截。

**最重要的誠實限制：MT7921（AXM / AXML）injection 在本平台失敗。** 這不是參數沒調好，也不是晶片先天不能注入——主因是 kernel 6.16+ 的 mac80211 chanctx 回歸；社群同型號改用 git／patched 驅動雖可運作，但 firmware 會鎖速率（對應 morrownr/USB-WiFi #387、morrownr/mt76 #18）。在本平台因注入失敗，這兩款無法 deauth，也就無法走完 handshake 擷取鏈路。需要 injection 的用途，這兩張在本平台請直接排除。

**AP 與 WPA3：幾乎全數過關。** 9 款都能當 AP，多數支援 5GHz VHT80（80MHz）；WPA3-SAE 連線在已實測的頻段上也全數可成立（見表下註記）。唯一要注意的是 AWUS036ACHM，WPA3 需把 hostapd 的 `sae_pwe` 設為 0，否則舊款 iPhone 7 Plus 會連不上（以 iPhone 15 Pro 複測可連，屬相容性設定差異）。

## 三、進階功能與 handshake 能力摘要

把範圍再拉深一層，看 handshake 端到端、虛擬介面（VIF）、active monitor 與 mesh / IBSS。

| # | 型號 | WPA handshake 擷取 | VIF | Active monitor | Ad-hoc（IBSS） | Mesh（802.11s） |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **端到端**（.22000） | ✅ STA+AP / AP+mon | 🟡 可設定，ACK 未驗 | 🟡 單機 | 🟡 單機 |
| 2 | AWUS036ACHM | ✅ **端到端**（.22000，5 GHz ch36） | ✅ | 🟡 | 🟡 單機 | 🟡 單機 |
| 3 | AWUS036ACH | ✅ **端到端**（.22000） | ✅ STA+mon | ❌ -95 | 🟡 單機 | ❌ -95 |
| 4 | AWUS036ACS | ✅ **端到端**（.22000） | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **端到端**（.22000，79 ACKs） | 🟡 被動 monitor 與 managed 同頻道並存（software monitor）；不支援獨立雙 VIF | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **端到端**（.22000） | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **端到端**（.22000） | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ 注入失敗 | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ 注入失敗 | ✅ | 🟡 | N/A | N/A |

這裡的「端到端」有明確定義：用該卡對 **Yupitek 自有的 iPhone 7 Plus**（連在自家 `YUPITEK` SSID 上）執行 injection，擷取完整的 4-way handshake（M1–M4），再用 `hcxpcapngtool --all` 轉成 hashcat 的 `.22000` 格式。整條鏈路能不能跑通，才是「滲透測試能力」的驗收點，不是「能進 monitor」就算。

- **端到端通過（9 款中共 7 款）**：ACM、ACHM、ACH、ACS、EACS、AX、AXER 都能產出 `.22000`，其中 EACS 收到 79 個 ACK，訊號回饋最紮實；ACH 兩頻注入 100%，已於 2026-11-19 補測轉出 47 行 hashline 的 `.22000`。ACHM 在 5GHz（ch36）完成；ACM 雖注入成功率較低，仍完成端到端。
- **端到端斷鏈**：AXM / AXML 因 injection 失敗，整條 handshake 跟著斷。這再次印證：MT7921 在本平台不適合滲透測試用途。
- **VIF（虛擬介面並存）**：9 款都支援某種形式的多介面並存；Realtek rtw89 可同時跑 STA + AP，EACS 則只支援被動 monitor 與 managed 同頻道並存（software monitor），不支援獨立雙 VIF。
- **Active monitor（帶 ACK 回報）**：`rtw88` 的 ACH / ACS / EACS 回報 -95（不支援）；`rtw89` 的 AX / AXER 驅動不具此模式（N/A）；`mt76` / `mt7921u` 為部分可（🟡）。
- **Mesh（802.11s）**：只有 `mt76` 的 ACM / ACHM 能在單機建立（🟡，需第二台卡才能完整互連驗證）；Realtek `rtw88` 回 -95 不支援、`rtw89` 與 `mt7921u` 的驅動不具此模式。做 mesh 實驗，MediaTek `mt76` 是這批裡唯一的選項。
- **IBSS（Ad-hoc）**：`mt76` 的 ACM / ACHM 與 `rtw88` 的 ACH 均可單機 join（🟡）；EACS 雖列出 iftype 但實測 join 無效，`rtw89` 的 AX / AXER 則無 IBSS iftype（N/A）。

### Kali / aircrack 工具層級相容性（平台共通）

以下工具在 9 款上屬平台層級表現，與個別卡無關：

| 工具 | 狀態 | 說明 |
|---|---|---|
| airmon-ng | ✅ | 全卡可偵測 / 管理；**嚴禁 `check kill`**（會關掉 NetworkManager 使 GX10 斷網） |
| kismet | ✅ | 各卡可當 data source 啟動並產出 `.kismet` log |
| bettercap | ✅ | `wifi.recon` 與 channel hopper 正常 |
| wifite（git 3.0.0） | ✅ | 可掃描建目標清單（須用 git 版，apt 版與自編 aircrack-ng 衝突） |
| Wireshark / tshark | ✅ | monitor 擷取與解析正常 |
| **hcxdumptool 8.x** | ⚠️ | **全卡 failed to arm，唯 EACS 在 2.4 GHz 可 arm（5 GHz 失敗）**：需要 active-monitor，而 `rtw88` / `rtw89` / `mt7921u` 皆不支援 → 改用 `airodump-ng` + `aireplay-ng` |

ARM64 補充：`aircrack-ng` 需自原始碼編譯，`wifite` 建議用 git 3.0.0 版，以繞開 apt 套件與自編版本之間的依賴衝突。

## 四、依用途選型建議

把上面三張表收斂成「照用途直接選」。

| 用途 | 首選 | 說明 |
|---|---|---|
| **滲透測試（injection + handshake）** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | 兩頻注入最佳（EACS、ACH 達 100%）；端到端 `.22000` 以 EACS、ACS、ACH 佐證（ACH 於 2026-11-19 補測） |
| **最強接收 / 長距離 monitor** | **AWUS036AXER** / AWUS036ACH | AXER 跳頻一次掃到 63 個 AP + 12 個 client；ACH 雙天線高增益 |
| **Wi-Fi 6 + AP 熱點** | AWUS036AX / AWUS036AXER | 2x2 VHT80，AP 穩定且注入可用 |
| **純 AP / 一般連線（不需注入）** | AWUS036AXM / AWUS036AXML | MediaTek 連線穩定，但**注入失敗**，不適合滲透用途 |
| **mesh / IBSS 實驗** | AWUS036ACM / AWUS036ACHM | `mt76` 驅動單機可建立 mesh 與 IBSS（`rtw88` 的 ACH 僅 IBSS 單機可 join、不支援 mesh；`rtw89` 兩者皆未宣告） |

幾句白話總結：

- **要做滲透測試、要擷取 handshake**：端到端 `.22000` 已落檔實證的 9 款中共 7 款——**AWUS036EACS**（最紮實，79 ACKs）、**AWUS036ACS**，Wi-Fi 6 的 AWUS036AX / AWUS036AXER、**AWUS036ACM** 與 **AWUS036ACHM**（5 GHz），以及 **AWUS036ACH**（兩頻注入 100%，於 2026-11-19 補測轉出 47 行 hashline 的 `.22000`）。
- **要最遠的接收距離、最廣的側錄**：AWUS036AXER（Wi-Fi 6，內嵌天線 Nano 設計＋晶片調校，跳頻掃描最積極）或雙天線高增益的 AWUS036ACH。
- **要架 Wi-Fi 6 熱點**：AWUS036AX / AWUS036AXER，2x2 VHT80 且同時支援注入。
- **只要穩定連線 / 單純當 AP**：AWUS036AXM / AWUS036AXML 的 MediaTek 方案連線穩定，日常使用沒問題。
- **要玩 mesh**：這批裡只有 `mt76` 的 AWUS036ACM / AWUS036ACHM 做得到（IBSS 單機另有 `rtw88` 的 AWUS036ACH 可 join）。

**避雷（最重要的一條）**：如果你的用途是 **injection 或 handshake**，**請勿選 AWUS036AXM / AWUS036AXML**。MT7921 在 ASUS GX10（ARM64 / Ubuntu 24.04 / stock kernel 6.17）這個平台上注入失敗，主因是 kernel 6.16+ 的 mac80211 chanctx 回歸（非晶片先天），不是設定問題；社群同型號改用 git／patched 驅動雖可運作，但 firmware 會鎖速率，本平台 stock kernel 下仍無法注入。把它們留給「純連線 / 純 AP」的場景即可。

## 五、平台注意事項（GX10 ARM64 實務）

這些是在 ASUS GX10 + Ubuntu 24.04（ARM64）上操作這批卡時，9 款共通的實務要點：

1. **別切斷自己的網路**：絕對不要執行 `airmon-ng check kill`，它會關掉 NetworkManager 導致整台 GX10 斷網。操作時只動外接的 `wlx*` 介面，不要碰內建的對外上網主線。
2. **RX stall 排除**：反覆切換 monitor / AP 之後，若突然掃不到任何東西，通常是 RX stall，把卡拔插一次即可復原（USB 重新列舉，介面名以 MAC 命名、不會改變）。
3. **BT + WiFi 複合裝置**：EACS 與 AXML 同時帶藍牙，重插時偶爾會卡在 WiFi probe、生不出 `wlx` 介面；換一個 USB 孔通常就能解決。
4. **5GHz 的 TX 解鎖**：在自有環境做 5GHz injection 前，需先設定正確的法規網域（regulatory domain）以解鎖 TX 功率，測試結束後再設回在地網域。這是 5GHz 能否正常發射的前提。
5. **handshake 擷取的小技巧**：辦公室內常有多台同名 AP，實務上不鎖定單一 BSSID、改擷取整個頻道較穩，轉檔時用 `hcxpcapngtool --all`。
6. **hcxdumptool 全平台 failed to arm（EACS 在 2.4 GHz 為例外）**：三頻內建卡與上述驅動都不支援 active-monitor，直接改用 aircrack-ng 套件（`airodump-ng` + `aireplay-ng`）。
7. **ARM64 的編譯細節**：`aircrack-ng` 需自原始碼編譯，`wifite` 用 git 版繞過 apt 依賴衝突。

再次強調定位：上述 injection / deauth / handshake 的能力，全部在 Yupitek 自有封閉環境、對自有測試裝置量測，用途是驗證產品能力與相容性邊界。本文不提供、也不建議對任何第三方網路進行上述操作。

## 小結

在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）這個平台上，9 款 ALFA 卡的總評可以濃縮成三句話：**Monitor 全員可用、AP 與 WPA3 幾乎全員過關、分水嶺在 Injection。** 需要注入與 handshake 的專業用途，Realtek `rtw88` 的 EACS / ACH / ACS 是最穩的選擇；要收訊與 Wi-Fi 6，看 AXER / AX；MT7921 的 AXM / AXML 留給純連線場景。全數免編譯、插上即用，是這批卡在 ARM64 上最大的共同優點。

## 常見問題（FAQ）

**Q：AWUS036AXM 在 Ubuntu 能注入（injection）嗎？**
A：在本平台不能。實測中 AWUS036AXM 與 AWUS036AXML（皆為 MT7921 晶片）在 2.4GHz 與 5GHz 的 injection 皆失敗，主因是 stock kernel 6.16+ 的 mac80211 chanctx 回歸（非晶片先天），因此不建議在本平台用於需要注入或 handshake 擷取的用途。

**Q：哪一款 ALFA 網卡在 Ubuntu 上 injection 成功率最高？**
A：實測中 AWUS036ACH 與 AWUS036EACS 在 2.4GHz 與 5GHz 的 injection 成功率皆達 100%，是本批 9 款中表現最好的兩款。

**Q：9 款 ALFA 網卡在 Ubuntu 24.04 需要另外裝驅動嗎？**
A：不需要。9 款在 kernel 6.17 上全部走 kernel 內建（in-kernel）驅動（rtw88 / rtw89 / mt76 家族），插上即被辨識，不需編譯 DKMS 模組。

**Q：ALFA 網卡在 Ubuntu 可以架 WPA3-SAE 的熱點嗎？**
A：可以，9 款實測都能成功架設 WPA3-SAE 熱點並讓裝置連入（除 ACS 於 5 GHz 實測外，其餘皆於 2.4 GHz 實測；AXML 另於 6 GHz 實測）；唯 AWUS036ACHM 需把 hostapd 的 `sae_pwe` 設為 0，否則舊款 iPhone 7 Plus 會連線失敗。

**Q：這份 Ubuntu 的測試結果，Kali Linux 使用者可以參考嗎？**
A：Kali Linux 基於 Debian/Ubuntu 體系，使用同一套 rtw88 / rtw89 / mt76 in-kernel 驅動，因此本文的驅動相容性與能力矩陣原則上可作為 Kali 使用者的參考依據；但本文實測平台為 Ubuntu 24.04，尚未在 Kali 上正式複測，結果請以日後複測為準。

## 延伸閱讀

本文為總表 Hub。以下深入文與逐卡實測陸續上線（連結施工中）：

- 《免裝驅動：在 Ubuntu（ARM64）上啟用 Monitor 與 AP 模式》 → [`/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE handshake 擷取實務（自有環境驗證）》 → [`/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 篇逐卡深入實測：

- [AWUS036ACM 單卡實測](/zh-tw/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM 單卡實測](/zh-tw/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH 單卡實測](/zh-tw/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS 單卡實測](/zh-tw/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS 單卡實測](/zh-tw/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX 單卡實測](/zh-tw/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER 單卡實測](/zh-tw/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM 單卡實測](/zh-tw/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML 單卡實測](/zh-tw/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*測試單位：Yupitek（ALFA Network 台灣經銷）｜ 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）｜ 測試環境：自有辦公室 Wi-Fi。本文為產品相容性與能力驗證，非針對第三方網路之操作教學。*
