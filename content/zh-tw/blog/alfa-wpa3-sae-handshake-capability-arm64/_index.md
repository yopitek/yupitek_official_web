---
title: "WPA3-SAE 時代的無線稽核：9 款 ALFA 卡 handshake 擷取能力實測，與 iPhone 連線的 sae_pwe 相容性雷區"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "ALFA 網卡在 Ubuntu（可延伸至 Kali）的 WPA3-SAE handshake 擷取能力實測：9 款注入率與端到端 .22000 擷取結果，sae_pwe 相容性雷區與選型建議。"
faq:
  - question: "AWUS036AXM 在 Ubuntu 能擷取 WPA handshake 嗎？"
    answer: "在本平台不能。實測中 AWUS036AXM 與 AWUS036AXML（MT7921 晶片）因 injection 失敗、無法送出 deauth，整條 4-way handshake 擷取鏈路跟著斷，不適合需要 handshake 擷取的用途。"
  - question: "哪一款 ALFA 網卡的 WPA handshake 擷取最可靠？"
    answer: "實測中 AWUS036EACS 表現最紮實：兩頻 injection 皆達 100%，deauth 後收到 79 個 ACK 回報，並成功轉出 hashcat 可用的 .22000 檔案，是本批端到端驗證最完整的一款。"
  - question: "WPA3-SAE 的熱點為什麼舊 iPhone 連不上？"
    answer: "關鍵在 hostapd 的 sae_pwe 參數：設為 2（強制 H2E）時 iPhone 7 Plus 會連線失敗；改回 sae_pwe=0（Hunting-and-Pecking）後才能正常完成 4-way 交握並連入。"
  - question: "WPA3 環境下還能擷取到 4-way handshake 嗎？"
    answer: "純 WPA3-SAE 環境會強制啟用 PMF（ieee80211w=2），傳統針對管理框的手法會被擋下；實務上仍能擷取到 handshake，多半是因為目標跑的是 WPA2/WPA3 過渡模式，而非純 WPA3。"
  - question: "ALFA 網卡的 5GHz injection 測不出來，是硬體問題嗎？"
    answer: "不一定。預設法規網域會限制部分 5GHz 頻段的發射功率，導致注入「發不出去」；實測中把法規網域切換為可發射狀態後，原本失敗的 5GHz 注入即轉為可用，建議先確認法規網域設定，再判斷是否為硬體限制。"
draft: false
---

> 測試單位：Yopitek（ALFA Network 台灣經銷）｜測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17｜測試裝置：自有 iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）｜測試對象：自有辦公室 Wi-Fi（SSID YUPITEK，2.4G ch5 / 5G ch36、157）。
>
> 本文為 ALFA 無線網卡的能力與相容性總覽。所有 Monitor / Injection / handshake 擷取，均於 Yopitek 自有設備、自有辦公室 Wi-Fi、對自有測試手機進行，屬經銷商對硬體的正當能力驗證；不針對任何第三方網路，亦不提供攻擊操作步驟。

## 重點摘要（TL;DR）

在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）實測的 9 款 ALFA 網卡中，共 7 款（ACM、ACHM、ACH、ACS、EACS、AX、AXER）完成端到端 WPA handshake 擷取並轉出 `.22000`；AWUS036EACS 兩頻注入 100%、收到 79 個 ACK，MT7921 的 AXM / AXML 則在本平台注入失敗。

- WPA3-SAE 普及後，稽核重點從「能不能 monitor」轉為「端到端 handshake 擷取能力」與「`sae_pwe` 端點相容性」。
- **端到端 `.22000` 已實證，9 款中共 7 款**：ACM、ACHM、ACH、ACS、EACS、AX、AXER；其中 EACS 最紮實（兩頻注入 100%、79 ACKs）。
- **AXM / AXML（MT7921）在本平台 injection 失敗**，無法 deauth，擷取不到 handshake，稽核用途務必避開。
- `sae_pwe` 雷區：舊款 iPhone 需 `sae_pwe=0` 才連得上；5G 注入前先 `iw reg set US` 解鎖 TX。
- 純 WPA3 強制 PMF（`ieee80211w=2`），現場仍能擷取多半因目標跑 WPA2/WPA3 過渡模式。

## 1. WPA3-SAE 普及，把無線稽核的門檻整個抬高了

過去十年，授權範圍內的無線稽核（authorized wireless audit）幾乎都圍著 WPA2-PSK 的 4-way handshake 打轉：擷取一次完整握手，後端就能離線比對。但自從 Wi-Fi 6 認證把 WPA3 納入強制項目，SAE（Simultaneous Authentication of Equals，俗稱 Dragonfly）逐步取代 PSK，把「擷取握手、離線驗證」這條老路堵得越來越窄。

對經銷商與第一線工程師來說，WPA3-SAE 帶來三個實務上的改變：

1. **PMF（Protected Management Frame）變成強制**。WPA3-SAE 規範強制開啟 `ieee80211w=2`，management frame 受到保護，傳統那種「隨手一個 deauth 把裝置踢下線」的做法，在純 WPA3 環境會被直接擋下。
2. **過渡模式（transition mode）仍保留 4-way**。現實中大量 AP 跑的是 WPA2/WPA3 混合過渡模式，為了相容舊裝置仍會保留 WPA2 的 4-way handshake，這也是目前授權稽核仍擷取得到握手的主因。能不能擷取到握手，很大一部分要看現場目標開在哪一種模式。
3. **端點相容性成為新雷區**。SAE 有不同的 password element 推導方式（由 `sae_pwe` 控制），AP 參數一旦設錯，連自家的舊 iPhone 都連不上，更別說要在稽核現場重現客戶端點的連線行為。

因此，當客戶問「哪一張 ALFA 卡能拿來做 WPA3 相關的授權稽核」，答案已經不是「能不能 monitor」這麼簡單，而是要看兩件事：**端到端的 handshake 擷取能力**，以及**對 WPA3-SAE 參數與實機端點的相容性**。這份報告就是用 9 款 ALFA 卡、在同一套 ARM64 平台上實測後，整理出的能力對照。

## 2. 什麼叫「端到端 handshake 擷取能力」（概念層）

這裡先把能力拆成三段，純概念說明，不涉及任何針對第三方網路的操作指令：

- **第一段：Injection（主動注入）**。網卡要能「發得出去」特定的管理框，才能促使一個已連線的 client 重新進行關聯。很多卡只能被動 monitor（收封包），卻無法 injection（主動發送）。這是整條鏈最容易卡關的一段。本批測試以 `aireplay-ng --test` 量化注入成功率，並在 handshake 測試中以 client 回傳的 ACKs 數，驗證框是否真的送達。
- **第二段：4-way handshake 擷取**。當 client 重新關聯時，WPA 會交換四個 EAPOL 訊息（M1–M4）。網卡在 monitor 模式下，必須把這四框完整收齊，缺一不可。
- **第三段：轉出 hashcat `.22000`**。把擷取到的 pcap 用 `hcxpcapngtool --all` 轉成 hashcat 的 `.22000` 格式，交由後端做離線驗證。

**三段全部在實機跑通，才算「端到端」**：真的對自家 iPhone 7 Plus 送出 deauth（injection）→ 收齊完整 M1–M4 → 轉出 `.22000` 落檔。只能收不能發、或四框收不齊、或轉不出檔，都不算端到端。本文不列任何逐步攻擊指令；下列對照只回答一個問題：哪一張卡在這條能力鏈上走得完。

以本批最紮實的 EACS 為例，一次成功的端到端長這樣：deauth 送出後 client 回傳 **79 個 ACKs**（確認框確實到達那支手機）、`aircrack-ng` 判定 YUPITEK 有 1 個 handshake、EAPOL 的 M1 / M2 / M3 / M4 四框各收到 1 份、擷取到的 client MAC 開頭為 Apple OUI（確認就是那支 iPhone 7 Plus），最後 `hcxpcapngtool --all` 轉出約 784 bytes 的 `.22000`。這四個條件缺一，這場擷取就不算數。這也是為什麼「能 monitor」和「能端到端擷取」是兩件完全不同的事。

## 3. 9 款卡 handshake 能力對照表

| # | 型號 | 晶片 / 世代 | Injection 2.4G | Injection 5G | WPA handshake 擷取能力 |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5・2T2R | 可用 63–83% | 可用 76% | **端到端 `.22000` 已實證**（注入率較低） |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5・1T1R | 可用 96–100% | 僅廣播 | **端到端 `.22000` 已實證（5 GHz ch36）** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5・2T2R | **100%** | **100%** | **端到端 `.22000` 已實證（2026-11-19 補測）** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5・1x1 | **100%** | 96% | **端到端 `.22000` 已實證** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5・1x1 | **100%** | **100%** | **端到端 `.22000` 已實證（79 ACKs）** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6・2x2 | 96% | 可用 | **端到端 `.22000` 已實證** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6・2x2 | 73% | 可用 | **端到端 `.22000` 已實證** |
| 8 | AWUS036AXM | MT7921AU / Wi-Fi 6・2x2 | 失敗 | 失敗 | 不支援：注入失敗，無法擷取 |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6・2x2 | 失敗 | 失敗 | 不支援：注入失敗，無法擷取 |

**兩個梯隊，一眼看懂：**

- **端到端已實證（擷取 → `.22000` 落檔，9 款中共 7 款）**：AWUS036ACM、AWUS036ACHM、AWUS036ACH、AWUS036ACS、AWUS036EACS、AWUS036AX 與 AWUS036AXER。其中 EACS 兩頻注入都 100%、deauth 收到 79 個 ACKs，是本批握手能力最紮實的一張；AWUS036ACH（RTL8812AU 雙天線高增益）兩頻注入 100%，於 2026-11-19 補測轉出 47 行 hashline 的 `.22000`，與 EACS 並列滲透測試首選。**完成端到端 handshake 擷取的型號共七款：ACM、ACHM、ACH、ACS、EACS、AX、AXER。** ACM 注入率較低（2.4G 63–83% / 5G 76%），ACHM 則是在 5 GHz（ch36）完成，兩者皆已轉出 `.22000`。
- **無法擷取（2 款）**：AWUS036AXM 與 AWUS036AXML（MT7921 在本平台 injection 失敗，無法 deauth、自然也擷取不到 handshake）。

需要特別點名的是 **AXM / AXML**：兩款都是 Wi-Fi 6、monitor 與 AP 都正常，唯獨在本平台 injection 無法運作——主因是 stock kernel 6.16+ 的 mac80211 chanctx 回歸（非晶片先天），社群同型號改用 git／patched 驅動雖可運作但 firmware 會鎖速率（對應 morrownr/USB-WiFi #387、morrownr/mt76 #18）。純上網、做熱點沒問題，但**凡是要注入或擷取 handshake 的稽核用途，在本平台一律避開**。

## 4. WPA3-SAE 相容雷區：參數設錯，自家 iPhone 都連不上

能力之外，WPA3-SAE 的參數相容性，是最容易在現場翻車的地方。本批實測踩到兩個關鍵雷：

### 4-1. ACHM 必須 `sae_pwe=0`，否則 iPhone 7 Plus 連不上

SAE 的 password element 推導有不同方式，hostapd 以 `sae_pwe` 控制。本批把 AWUS036ACHM 架成純 WPA3-SAE（`wpa_key_mgmt=SAE` + 強制 PMF `ieee80211w=2`）時，一旦 `sae_pwe` 設成 `2`，**iPhone 7 Plus 直接連不上**；改回 `sae_pwe=0`（Hunting-and-Pecking，相容舊端點）之後，iPhone 7 Plus（iOS 15）才順利連入並完成 4-way。

這條雷的意義在於：當你要在稽核現場「重現」一個以舊 iOS 端點為主的 WPA3 環境，AP 端的 `sae_pwe` 必須配合端點能力，否則得到的會是「連不上」的假陰性，而不是真正的相容性結論。EACS、ACS 的 WPA3-SAE AP 測試同樣採 `sae_pwe=0` + `ieee80211w=2`，iPhone 7 Plus 均能連入；`sae_pwe=0` 就是本批對舊 iPhone 端點驗證過的安全值。

### 4-2. 5G injection 前，先 `iw reg set US` 解鎖 TX

第二個雷與法規域（regulatory domain）有關。預設 `reg=TW` 會鎖住部分 UNII 頻段的 TX，導致 5 GHz 的 injection / deauth「發不出去」。本批在做 5G 注入前一律先 `iw reg set US` 解鎖 TX，測完立即 `iw reg set TW` 還原。ACS 的 5G 注入在解鎖後由失敗轉為 96%，EACS、ACH 則直上 100%。忘了解鎖 reg，會把一張注入能力正常的卡誤判成「5G 不能用」。

### 4-3. 順帶一提：PMF 在 WPA3 是強制的

WPA3-SAE 規範強制 `ieee80211w=2`（Management Frame Protection）。這代表純 WPA3 環境下，傳統針對 management frame 的手法會被 PMF 擋住；現實稽核之所以還能擷取到 4-way，多半是因為目標仍跑 WPA2/WPA3 過渡模式。選卡時把這點一併納入考量，才不會對純 WPA3 目標抱錯期待。

## 5. 工具鏈概述：ARM64 平台上實際能跑的那一套

硬體能力之外，平台工具鏈同樣影響稽核效率。以下是本批在 GX10（ARM64）上整理出的幾個實測心得：

- **轉檔一律 `hcxpcapngtool --all`**。預設參數較嚴格，常回「not enough M1」而轉不出檔；加上 `--all`，才能由完整的 M1–M4 穩定轉出 `.22000`。
- **辦公室多台同名 AP 時，不要鎖 `--bssid`**。Yopitek 辦公室同一個頻道上有多台同名 YUPITEK AP，iPhone 會連上訊號最強的那一台。擷取時若用 `--bssid` 鎖單一 BSSID，很可能把 iPhone 實際連上的那台濾掉、整場擷取落空。實測結論是**不鎖 BSSID、直接擷取整個頻道**，再從落檔裡挑出完整握手。
- **`hcxdumptool` 8.x 在本平台除 EACS 的 2.4 GHz 外全軍 `failed to arm`（5 GHz 失敗）**。rtw88 / rtw89 / mt7921u 都不提供 active-monitor，而 hcxdumptool 8.x 需要它；解法是改用 `airodump-ng` + `aireplay-ng` 這套傳統 aircrack-ng 流程。
- **反覆切換模式後掃不到東西，先拔插卡**。rtw88 / rtw89 在反覆切 monitor / AP 之後可能發生 RX stall（掃描 0 封包）；USB 重新列舉即可復原，且介面名由 MAC 決定、拔插後不變。擷取 handshake 前，建議第一件事就是重插一次卡。
- **BT+WiFi 複合裝置（EACS / AXML）重插有競態**。含藍牙的複合卡在重插、或插在某些 USB 孔時，會發生 WiFi 功能 probe 卡死、生不出 `wlx` 介面；解法是換一個 USB 孔重插，`modprobe` 或手動 bind 多半無效。
- **ARM64 的工具安裝眉角**。aircrack-ng 在 aarch64 常缺 prebuilt 套件，需自原始碼編譯；wifite 則用 git 版（apt 版與自編 aircrack-ng 相依衝突）。
- **安全守則：絕不 `airmon-ng check kill`**。GX10 對外上網靠內建網卡，`check kill` 會連 NetworkManager 一起關掉、使主機斷網。本批全程只操作 ALFA 卡的 `wlx*` 介面，不碰內建對外主線。

## 6. 選型小結：要做 WPA3 相關稽核，該選哪幾款

把能力、相容性與平台工具鏈合在一起看，對「WPA3 相關的授權稽核」用途，本批的建議是：

| 需求情境 | 建議型號 | 理由 |
|---|---|---|
| 綜合首選（注入 + 端到端 handshake） | **AWUS036EACS** | 兩頻注入 100%、deauth 收 79 ACKs、端到端 `.22000` 已實證；唯一要注意的是 BT+WiFi 複合裝置，重插偶爾要換 USB 孔 |
| 高增益 / 長距離 + 強注入 | **AWUS036ACH** | RTL8812AU 雙天線、兩頻注入 100%，接收能力強 |
| 輕量隨身 | **AWUS036ACS** | 單串流、端到端 `.22000` 已實證，5G 注入 96% |
| Wi-Fi 6 需求 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80、端到端 `.22000` 已實證；AXER 內嵌天線（Nano）設計＋晶片調校、掃描覆蓋最廣 |
| **務必避開** | AWUS036AXM / AWUS036AXML | MT7921 在本平台 injection 失敗，無法擷取 handshake |

一句話總結：**要做 WPA3 相關稽核，優先 EACS，其次 ACH / ACS；需要 Wi-Fi 6 選 AX / AXER；務必避開 AXM / AXML。** 七款完成端到端 handshake 擷取的卡裡，Realtek（rtw88 / rtw89）全數可注入，MediaTek 的 ACM 與 ACHM（mt76）也成功跑通；MT7921 的 AXM / AXML 則不可用。選型時，認晶片比認型號名更準。

## 常見問題（FAQ）

**Q：AWUS036AXM 在 Ubuntu 能擷取 WPA handshake 嗎？**
A：在本平台不能。實測中 AWUS036AXM 與 AWUS036AXML（MT7921 晶片）因 injection 失敗、無法送出 deauth，整條 4-way handshake 擷取鏈路跟著斷，不適合需要 handshake 擷取的用途。

**Q：哪一款 ALFA 網卡的 WPA handshake 擷取最可靠？**
A：實測中 AWUS036EACS 表現最紮實：兩頻 injection 皆達 100%，deauth 後收到 79 個 ACK 回報，並成功轉出 hashcat 可用的 `.22000` 檔案，是本批端到端驗證最完整的一款。

**Q：WPA3-SAE 的熱點為什麼舊 iPhone 連不上？**
A：關鍵在 hostapd 的 `sae_pwe` 參數：設為 2（強制 H2E）時 iPhone 7 Plus 會連線失敗；改回 `sae_pwe=0`（Hunting-and-Pecking）後才能正常完成 4-way 交握並連入。

**Q：WPA3 環境下還能擷取到 4-way handshake 嗎？**
A：純 WPA3-SAE 環境會強制啟用 PMF（`ieee80211w=2`），傳統針對管理框的手法會被擋下；實務上仍能擷取到 handshake，多半是因為目標跑的是 WPA2/WPA3 過渡模式，而非純 WPA3。

**Q：ALFA 網卡的 5GHz injection 測不出來，是硬體問題嗎？**
A：不一定。預設法規網域會限制部分 5GHz 頻段的發射功率，導致注入「發不出去」；實測中把法規網域切換為可發射狀態後，原本失敗的 5GHz 注入即轉為可用，建議先確認法規網域設定，再判斷是否為硬體限制。

## 7. 延伸閱讀

- [9 款 ALFA 無線網卡 ARM64 實測總表與選型總評](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 各型號逐卡實測：[AWUS036EACS 單卡實測](/zh-tw/blog/awus036eacs-asus-gx10-ubuntu-test-report/)、[AWUS036ACS 單卡實測](/zh-tw/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*本文所有測試均於 Yopitek 自有辦公室 Wi-Fi（SSID YUPITEK）、對自有 iPhone 7 Plus 進行，屬經銷商對 ALFA 無線網卡的正當能力驗證。數據引用自 2026-11-16～11-18 的實機測試報告，不針對任何第三方網路，亦不提供攻擊操作步驟。測試單位：Yopitek（ALFA Network 台灣經銷）— https://www.yupitek.com*
