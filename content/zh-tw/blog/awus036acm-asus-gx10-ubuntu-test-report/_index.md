---
title: "AWUS036ACM 逐卡實測：MediaTek MT7612U（mt76x2u）在 ASUS GX10 + Ubuntu 24.04（ARM64）的 Monitor / Injection / AP 與 mesh 能力報告"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "AWUS036ACM（MT7612U）在 Ubuntu 24.04 ARM64 免裝驅動，雙頻監聽模式與 aircrack-ng（Kali 常用）可用，封包注入 2.4G 63–83%、5G 76%，支援 VIF 與單機 mesh / IBSS。"
faq:
  - question: "AWUS036ACM 在 Ubuntu 或 Kali 需要裝驅動嗎？"
    answer: "不需要。MT7612U 由 kernel 內建的 mt76x2u 驅動接管，Ubuntu 24.04（kernel 6.17）插上即認，不用 DKMS、不用手動灌韌體。本次實測平台是 Ubuntu 24.04 ARM64，Kali 只要核心夠新原則上相同，但本次未在 Kali 實機驗證。"
  - question: "AWUS036ACM 可以進 monitor mode 和做封包注入嗎？成功率多少？"
    answer: "可以。2.4GHz 與 5GHz 都能進 monitor mode 並正常擷取；aireplay-ng 注入測試 2.4GHz 為 63–83%、5GHz 為 76%，在九張卡中屬中段。要雙頻注入都 100%，Yupitek 實測以 AWUS036ACH、AWUS036EACS 為佳。"
  - question: "AWUS036ACM 可以同時開熱點又連上網（VIF）嗎？"
    answer: "可以。實測 STA+AP（一邊連上游、一邊開熱點）與 AP+monitor（開熱點同時監聽）兩種組合都成立，這是 mt76 驅動多介面併發較完整的地方；5GHz 熱點可開到 VHT 80 MHz。"
  - question: "AWUS036ACM 支援 mesh（802.11s）和 IBSS 嗎？"
    answer: "單機可建立。在 Ubuntu 24.04 / kernel 6.17 上，AWUS036ACM 能建立 802.11s mesh 與 IBSS（Ad-hoc）介面；但本次沒有第二台節點，尚未驗證多節點互連，所以只能說單機可建立。"
  - question: "AWUS036ACM 可以擷取 WPA handshake 嗎？"
    answer: "可以。對自有 AP 與自有 iPhone 7 Plus 實測端到端成功：deauth、擷取完整 4-way（M1–M4），並以 hcxpcapngtool --all 轉出 hashcat .22000。僅限自有或已取得授權的網路。"
draft: false
---

> 本文是 Yupitek 針對 ALFA AWUS036ACM 在新版 Linux 平台上的產品相容性與能力實測紀錄，供評估選型用。
> 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。所有數據均為 Yupitek 於**自有設備、自有辦公室 Wi-Fi**（SSID `YUPITEK`，2.4G ch5 / 5G ch36、ch157）對**自有測試手機**（Apple iPhone 7 Plus；WPA3 另以 iPhone 15 Pro 複測）的實測節錄。
> ⚠️ **合法與範圍聲明**：Monitor、injection、handshake 擷取僅於自己擁有或已取得授權的網路與裝置上進行；AP 模式請遵守當地無線電法規。本文聚焦網卡本身的能力、相容性與設定，**不涉及針對第三方網路的任何攻擊操作**。

## 重點摘要（TL;DR）

Yupitek（ALFA Network 台灣經銷）於 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）實測：AWUS036ACM 雙頻 monitor 可用，封包注入 2.4G 為 63–83%、5G 為 76%，雙頻 AP 熱點皆可架設（5G 可跑 VHT 80 MHz）。

- Ubuntu 24.04（ARM64）免裝驅動：MT7612U 由 kernel 6.17 內建的 mt76x2u 接管，插上即認，不用 DKMS。
- 雙頻監聽模式（monitor mode）可用；封包注入 2.4G 為 63–83%、5G 為 76%，在九卡中屬中段。
- 單機可建立 802.11s mesh 與 IBSS，並支援 VIF（STA+AP、AP+monitor）。
- WPA handshake 擷取為端到端（完整 4-way，轉出 hashcat `.22000`）；為 9 款中完成端到端的 7 款之一。
- 要雙頻注入都 100%，建議改選 AWUS036ACH 或 AWUS036EACS。

---

## 1. 這張卡與測試平台

AWUS036ACM 是 ALFA 產品線裡的 MediaTek 雙頻卡，晶片 MT7612U，Wi-Fi 5（802.11ac）、2T2R 雙空間流、2.4GHz / 5GHz 雙頻。它在 morrownr 的清單上長期列為 Kali 推薦卡，靠的不是吞吐數字，而是 `mt76` 系列驅動對 Linux 的 Monitor、injection 與多介面併發（VIF）支援相對完整；802.11s mesh 這類實驗性模式，在本平台也只有 mt76 陣營還起得來（Realtek 卡僅能建立單機 IBSS、起不了 mesh）。所以評估這張卡，重點不在速度，而在能力面齊不齊、mt76 的特色能不能真的落地，以及哪些項目得老實標成邊界。

本輪沿用同一套維運情境：GX10 的內建網卡（`wlP9s9`）負責對外上網，AWUS036ACM 走 USB 外接、只承擔測試任務；切 Monitor 或 AP 都不動到主機本身的網路。全程只操作 ALFA 卡對應的 `wlx*` 介面，不碰內建對外網卡。

| 項目 | 內容 |
|---|---|
| 型號 | AWUS036ACM |
| 晶片 | MediaTek MT7612U（Wi-Fi 5 / 802.11ac，2T2R 雙串流） |
| 驅動 | `mt76x2u`（in-kernel，kernel 6.17 內建） |
| 世代 / 串流 | Wi-Fi 5 / 2T2R |
| 備註 | morrownr 推薦 Kali 卡 |
| 平台 | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| 測試裝置 | Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro） |
| 測試環境 | 自有辦公室 Wi-Fi，SSID `YUPITEK`，2.4G ch5 / 5G ch36、ch157 |

> 本輪總表未登錄 AWUS036ACM 的 USB ID 與韌體版本欄位（標為「—」），故本文不臆測這兩項數值；下文所有能力數據均以總表 ACM 各列為準。

---

## 2. 硬體與驅動（免裝）

這張卡在 GX10 上插上即認，不用編譯、也不用 DKMS。MT7612U 由 mainline kernel 內建的 `mt76x2u` 驅動直接接管，不必外掛任何 out-of-tree 專案，也不必手動灌韌體 blob。對 ARM64 來說這是 mt76 最實際的好處。很多第三方 Realtek 驅動在 aarch64 沒有 prebuilt，得自己對著核心版本編譯；mt76 走 in-kernel，kernel 升級就不會被驅動相依卡住。

插卡後，介面會以 `wlx` + MAC 命名（例如 `wlxXXXXXXXXXXXX`），名稱綁定 MAC、重插不變，利於寫進腳本固定指定。確認驅動綁定與介面生成，可用下列通用檢查（不同機器的介面名與 phy 編號會不同）：

```bash
# 找出 ALFA 卡的介面名 (只挑 wlx 開頭, 不動內建 wlP9s9)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# 確認綁定的驅動為 mt76x2u
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# 列出該 phy 宣告支援的介面模式 (決定後面哪些能力能用)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

依本輪實測，`mt76x2u` 可用的介面模式比 Realtek `rtw88` 完整：managed / AP / monitor 之外，IBSS 與 mesh point 在單機上也都建得起來（見第 4 節）。這就是 ACM 後面能在單機跑 mesh / IBSS 的底氣；同平台的 Realtek 卡（如 AWUS036ACH）雖然單機也能建立 IBSS，但 802.11s mesh 與 active monitor 在本平台起不來。

---

## 3. 實測能力：Monitor / Injection / AP / WPA3

先看核心能力總表（取自九卡總表第 1 列），再逐項展開。所有項目都在自有 `YUPITEK` AP + 自有 iPhone 7 Plus 上完成。

| 能力 | 2.4 GHz | 5 GHz | 說明 |
|---|---|---|---|
| Monitor（監聽接收） | ✅ | ✅ | 兩頻皆可進 monitor、正常擷取 |
| Injection（封包注入） | ✅ 63–83% | ✅ 76% | 標準 injection test 的注入成功率 |
| AP 熱點（hostapd） | ✅ | ✅ 80MHz | 5G 可開到 VHT 80 MHz |
| WPA3-SAE（AP 端） | ✅ | 未實測 | WPA3-SAE 僅在 2.4 GHz 實測；5 GHz 未實測 |

### 3-1. Monitor（2.4 GHz + 5 GHz）✅

2.4 GHz 與 5 GHz 都能正常進入 monitor 並擷取封包，是這張卡最沒有爭議的能力。對 2T2R 的雙天線卡來說，兩頻監聽接收穩定，足以支撐現場頻道盤點與封包診斷。

### 3-2. Injection（封包注入）✅（中段水準）

以標準 injection test 量測封包注入可靠度，AWUS036ACM 在 2.4 GHz 是 63–83%、5 GHz 是 76%。放進九卡裡屬中段，明顯不如 Realtek RTL8812AU（AWUS036ACH，兩頻 100%）和 RTL8821CU（AWUS036EACS，兩頻 100%），但功能完整、實務上夠用。ACM 能注入，只是穩定度不是班上最高；要是客戶把「注入成功率要頂」擺第一，它就不是首選（見第 5 節選型）。

5 GHz 注入前要留意一個設定細節：預設法規網域會鎖住部分 UNII 頻段的主動傳送，測試前需先把 regulatory domain 切到允許發射的設定、測完再設回在地網域（`iw reg set US` → 測試 → `iw reg set TW`）。這是 5 GHz 能否正常發射的前提，與卡本身能力無關。

### 3-3. AP 熱點與 WPA3-SAE ✅

AWUS036ACM 可作為 AP，2.4 GHz 與 5 GHz 都行，5 GHz 還能開到 80 MHz 頻寬（VHT80）。AP 端在 2.4 GHz 啟用 WPA3-SAE 後，自有測試手機可正常連上（5 GHz 的 WPA3 未實測）。

這裡值得對照同為 mt76 的單天線型號 AWUS036ACHM：ACHM 的 WPA3 得特別把 hostapd 的 `sae_pwe` 設成 0，不然 iPhone 7 Plus 會連不上。AWUS036ACM 本輪沒碰到這個限制，WPA3-SAE 直接可用。

---

## 4. 進階能力：VIF / mesh / IBSS 單機與限制

再往深一層看 handshake、虛擬介面（VIF）、active monitor 與 mesh / IBSS。這一節也是 AWUS036ACM 跟 Realtek 卡拉開差距的地方。

| 進階項目 | ACM 結果 | 說明 |
|---|---|---|
| WPA handshake 擷取 | ✅ 端到端（.22000） | deauth 自有 iPhone 7 Plus，擷取完整 4-way M1–M4，轉出 hashcat `.22000` |
| VIF（多介面併發） | ✅ STA+AP / AP+mon | 可同時 STA+AP 或 AP+monitor |
| Active monitor | 🟡 可設定，ACK 未驗 | 模式可建立，ACK 回覆行為未驗證 |
| Ad-hoc（IBSS） | 🟡 單機 | 單機可建立介面，互連需第二台 |
| Mesh（802.11s） | 🟡 單機 | 單機可建立介面，互連需第二台 |
| Wi-Fi Direct（P2P） | ⬜ 需第二台 | 本輪未測 |

### 4-1. VIF（虛擬介面併發）— ACM 的強項 ✅

這張卡能同時跑兩個虛擬介面。本輪實測 STA+AP（一邊連上游、一邊開熱點）和 AP+monitor（一邊開熱點、一邊監聽）兩種組合都成立，適合「邊連線邊觀測」或「單卡同時當 client 與基地台」這類場景。這是 `mt76` 驅動多介面併發較完整的地方。

### 4-2. mesh / IBSS「單機可」— mt76 的關鍵差異 🟡

AWUS036ACM 在單機上能把 802.11s mesh 與 ad-hoc（IBSS）介面建起來；Realtek `rtw88` / `rtw89`（AWUS036ACH、AWUS036AX 等）雖然單機也能建立 IBSS，但在本平台不支援 802.11s mesh。所以要做 802.11s mesh 實驗，mt76 卡（ACM / ACHM）就有 Realtek 卡沒有的起點。

要把邊界標清楚：本輪確認的是「單機可建立介面」，完整的多節點互連還需要第二張卡 / 第二台節點，尚未進行，所以這裡標 🟡（單機）而不是 ✅。

### 4-3. 誠實的能力邊界

- **handshake**：ACM 完成了完整的端到端流程（deauth 自有裝置 → 擷取完整 4-way M1–M4 → `hcxpcapngtool --all` 轉出 hashcat `.22000`），儘管其注入成功率（2.4G 63–83% / 5G 76%）低於 Realtek 卡。
- **active monitor**：模式可以設定起來，但 ACK 回覆行為本輪未驗證（標 🟡）。相關的是，平台層級的 `hcxdumptool` 8.x 除 AWUS036EACS 在 2.4 GHz 之外，在所有卡上都 `failed to arm`（它要 active-monitor，本平台的三頻內建與現行驅動沒提供），所以 ACM 的 handshake 流程改走 `airodump-ng` + `aireplay-ng`。
- **Wi-Fi Direct（P2P）**：本輪未測，需第二台設備。

### 4-4. 平台操作注意（GX10 ARM64，ACM 相關）

1. **別切斷自己的網路**：絕不執行 `airmon-ng check kill`（會關掉 NetworkManager 使 GX10 斷網）；只動 `wlx*`，不碰內建對外的 `wlP9s9`。
2. **RX stall 排除**：反覆切換 monitor / AP 後若突然掃不到東西，把卡**拔插一次**即可復原（USB 重列舉，介面名由 MAC 決定、不變）。
3. **5 GHz TX 解鎖**：做 5 GHz injection 前先設定正確法規網域解鎖 TX 功率，測完設回在地網域。
4. **handshake 擷取技巧**：辦公室常有多台同名 AP，實務上不鎖單一 `--bssid`、改擷取整個頻道較穩；轉檔用 `hcxpcapngtool --all`。
5. **ARM64 工具鏈**：`aircrack-ng` 需自原始碼編譯；`wifite` 用 git 3.0.0 版（繞過 apt 依賴衝突）。

平台層級的 Kali 工具（`airmon-ng`、`kismet`、`bettercap`、`wifite` git 版、Wireshark / tshark）都能正常把 ACM 當 data source 使用；唯一例外是前述需要 active-monitor 的 `hcxdumptool`。

---

## 5. 適用情境與選型（連回 Hub）

把上面的能力對回產品定位，AWUS036ACM 的角色其實很清楚：一張能力均衡、驅動免裝，又獨有 mt76 mesh / IBSS / VIF 優勢的 Wi-Fi 5 2T2R 卡。那它該用在哪些情境？

- **mesh（802.11s）實驗的首選**：這批九卡裡，只有 mt76 的 ACM / ACHM 能在單機建立 802.11s mesh 介面；Realtek `rtw88` / `rtw89` 雖可建立單機 IBSS，但不支援 802.11s mesh。要做 mesh 實驗，ACM 是對的起點。
- **需要 VIF 併發**：STA+AP、AP+monitor 都成立，適合單卡同時當 client 與 AP、或邊連線邊監聽。
- **重視免驅動維運**：in-kernel `mt76x2u`，kernel 升級不卡驅動，ARM64 上免去編譯 out-of-tree 模組的麻煩。
- **不是最佳解的情境**：若核心需求是「最高 injection 成功率」，ACM 的注入（2.4G 63–83% / 5G 76%）不是班上最高，建議改用 Realtek 的 AWUS036EACS / ACH / ACS；若追求最強接收 / 長距離 monitor，則看 AWUS036AXER / ACH。

和同家族相比，定位差異如下：

| 需求 | 建議卡 | 理由 |
|---|---|---|
| mesh（802.11s）單機實驗 | **AWUS036ACM** / AWUS036ACHM | `mt76` 驅動單機可建立 802.11s mesh（Realtek 僅能單機 IBSS、不支援 mesh） |
| VIF 併發（STA+AP / AP+mon） | **AWUS036ACM** | 多介面併發成立 |
| 雙頻注入都要 100% / 端到端 handshake | AWUS036EACS、AWUS036ACH、AWUS036ACS | 兩頻注入最佳，`.22000` 端到端已佐證 |
| 最強接收 / 長距離 monitor | AWUS036AXER、AWUS036ACH | 跳頻掃到更多目標 / 雙天線高增益 |

一句話選型：要玩 mesh / IBSS、要 VIF 併發、又想免驅動維運，AWUS036ACM 是這批裡最對口的 mt76 卡；要雙頻注入都 100%，就往 EACS / ACH 走。完整九卡橫向比較與選型決策，見 [ALFA 無線網卡總評 Hub（九卡總表）](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

---

## 常見問題（FAQ）

**Q：AWUS036ACM 在 Ubuntu 或 Kali 需要裝驅動嗎？**
不需要。MT7612U 由 kernel 內建的 mt76x2u 驅動接管，Ubuntu 24.04（kernel 6.17）插上即認，不用 DKMS、不用手動灌韌體。本次實測平台是 Ubuntu 24.04 ARM64，Kali 只要核心夠新原則上相同，但本次未在 Kali 實機驗證。

**Q：AWUS036ACM 可以進 monitor mode 和做封包注入嗎？成功率多少？**
可以。2.4GHz 與 5GHz 都能進 monitor mode 並正常擷取；aireplay-ng 注入測試 2.4GHz 為 63–83%、5GHz 為 76%，在九張卡中屬中段。要雙頻注入都 100%，Yupitek 實測以 AWUS036ACH、AWUS036EACS 為佳。

**Q：AWUS036ACM 可以同時開熱點又連上網（VIF）嗎？**
可以。實測 STA+AP（一邊連上游、一邊開熱點）與 AP+monitor（開熱點同時監聽）兩種組合都成立，這是 mt76 驅動多介面併發較完整的地方；5GHz 熱點可開到 VHT 80 MHz。

**Q：AWUS036ACM 支援 mesh（802.11s）和 IBSS 嗎？**
單機可建立。在 Ubuntu 24.04 / kernel 6.17 上，AWUS036ACM 能建立 802.11s mesh 與 IBSS（Ad-hoc）介面；但本次沒有第二台節點，尚未驗證多節點互連，所以只能說單機可建立。

**Q：AWUS036ACM 可以擷取 WPA handshake 嗎？**
可以。對自有 AP 與自有 iPhone 7 Plus 實測端到端成功：deauth、擷取完整 4-way（M1–M4），並以 hcxpcapngtool --all 轉出 hashcat .22000。僅限自有或已取得授權的網路。

---

## 6. 延伸閱讀

- 九張 ALFA 卡的完整能力比較與選型總評 → [ALFA 無線網卡總評 Hub（九卡總表）](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 免裝驅動：Ubuntu 24.04 + kernel 6.17 啟用 Monitor / AP（rtw88 / rtw89 / mt76 實測）（placeholder，連結施工中）
- WPA3-SAE 與端到端 handshake 擷取逐步教學（placeholder，連結施工中）
- 同為 mt76 的單天線型號 → AWUS036ACHM 逐卡實測（placeholder，連結施工中）

---

*測試單位：Yupitek（ALFA Network 台灣經銷）— https://www.yupitek.com ｜ 測試環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）*
