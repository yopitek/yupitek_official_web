---
title: "AWUS036ACS 逐卡實測：RTL8811AU 輕量隨身卡在 ASUS GX10 + Ubuntu 24.04（ARM64）的相容性與能力報告"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS 在 Ubuntu 24.04 ARM64 實測：免裝驅動，Monitor、注入（2.4G 100%、5G 96%）、AP、WPA3-SAE 與端到端 handshake（.22000）皆通過。平台 ASUS GX10、kernel 6.17、RTL8811AU。"
faq:
  - question: "AWUS036ACS 在 Ubuntu 24.04 ARM64 要裝驅動嗎？"
    answer: "在本文測試的 kernel 6.17（ASUS GX10）上不用：RTL8811AU 由內建 rtw88_8821au 驅動，插上即認，免編譯、免 DKMS。kernel 較舊時，先用 modinfo rtw88_8821au 確認模組存在。"
  - question: "AWUS036ACS 支援 monitor mode 和 packet injection 嗎？"
    answer: "支援。2.4 GHz、5 GHz 都能 monitor；aireplay-ng --test 注入 2.4G 為 100%（30/30）、5G 為 96%（29/30，需先 iw reg set US 解除 TW 限制）。不支援 active monitor。"
  - question: "AWUS036ACS 能擷取 WPA handshake 並轉成 hashcat .22000 嗎？"
    answer: "能。在自有 AP 與自有 iPhone 7 Plus 上端到端實測：定向 deauth 觸發重連，擷取完整 4-way（M1–M4），再用 hcxpcapngtool --all 轉出 .22000。僅限自己擁有或已授權的網路。"
  - question: "AWUS036ACS 可以當 AP 熱點嗎？支援 WPA3 嗎？"
    answer: "可以。hostapd 開 2.4G 與 5G 熱點（5G 以 802.11a、20 MHz 實測；VHT80 未測），iPhone 7 Plus 連入並完成 4-way；5G 的 WPA3-SAE（SAE-only、ieee80211w=2、sae_pwe=0）也連入成功（2.4G 的 WPA3 未實測）。"
  - question: "AWUS036ACS 不支援哪些模式？hcxdumptool 能用嗎？"
    answer: "不支援 active monitor、IBSS、mesh（802.11s）、Wi-Fi Direct（P2P）。hcxdumptool 8.x 會 failed to arm interface，請改用 airodump-ng + aireplay-ng。要 mesh / IBSS 請選 AWUS036ACM / ACHM。"
draft: false
---

**重點摘要（TL;DR）**：Yopitek（ALFA Network 台灣經銷）實測，AWUS036ACS 在 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）免裝驅動，雙頻 monitor 與 AP（5G AP 可用：802.11a、20 MHz 實測；VHT80 未測）可用；注入 2.4G 100%、5G 96%，端到端 .22000 通過，不支援 mesh / IBSS。

> 本文是 Yopitek 針對 ALFA AWUS036ACS 在新版 Linux 平台上的產品相容性與能力實測紀錄，供評估選型用。
> 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。所有數據均為 Yopitek 於**自有設備、自有辦公室 Wi-Fi**（SSID `YUPITEK`，2.4G ch5 / 5G ch36）對**自有測試手機**（Apple iPhone 7 Plus）的實測節錄，MAC 位址部分遮蔽。
> ⚠️ **合法與範圍聲明**：Monitor、Injection、handshake 擷取僅於自己擁有或已取得授權的網路與裝置上進行；AP 模式請遵守當地無線電法規。本文聚焦網卡本身的能力、相容性與設定，**不涉及針對第三方網路的任何攻擊操作**。

---

## 1. 這張卡與測試平台

AWUS036ACS 是 ALFA 產品線裡的輕量隨身型無線網卡，晶片是 Realtek RTL8811AU，Wi-Fi 5（802.11ac）世代、1x1 單空間流。定位很直白：體積小、功耗低、單天線，是帶出門做現場盤點的卡，不是拚最高吞吐或最遠距離的重裝卡。所以評估它的時候，問題不在「它多快」，而在「這麼輕的規格下，哪些實務能力還是完整可用」。

這一輪測試把它擺進一個典型的維運情境：GX10 的內建網卡（`wlP9s9`）負責對外上網，AWUS036ACS 走 USB 外接，只扛測試任務。這樣切 Monitor 或 AP，都動不到主機自己的網路。全程只碰 ALFA 卡對應的 `wlx*` 介面，不去動內建的對外網卡。

| 項目 | 內容 |
|---|---|
| 型號 | AWUS036ACS |
| 晶片 | Realtek RTL8811AU（Wi-Fi 5 / 802.11ac，1x1 單串流） |
| USB ID | `0bda:0811` |
| 驅動 | `rtw88_8821au`（in-kernel，kernel 6.17 內建） |
| 韌體 | 42.4.0（實測 dmesg） |
| 平台 | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| 測試裝置 | Apple iPhone 7 Plus |

---

## 2. 硬體與驅動（免裝）

這張卡在 GX10 上插上就認，不必編譯、也不用 DKMS。RTL8811AU / RTL8821AU 這顆晶片自 mainline kernel 6.13 起正式併入 Realtek 的 in-kernel `rtw88` 驅動家族，GX10 搭的 6.17 已內建 `rtw88_8821au` 模組，不需要再去 GitHub 抓任何 out-of-tree 專案。（與舊版安裝指南不同：早期站文以 `morrownr` out-of-tree 驅動或較舊 kernel 為前提，稱需自行 DKMS 編譯；在 kernel 6.17 的 in-kernel 驅動下這已不再需要。）過去常見的 `morrownr/8821au-20210708` 現在已轉為 legacy（只建議低於 6.13 的核心使用，而且裝了它會把內建驅動 blacklist 掉），新 kernel 上沒必要再走這條舊路。維運成本上的好處更實在：in-kernel 驅動跟著 kernel 一起更新，使用者不必各自維護分支，也不會每次升級就卡在 DKMS 編譯失敗，同一套操作跨好幾次 kernel 更新都能重複用。韌體由 `linux-firmware` 隨系統帶，本機實測是 42.4.0，一樣不用手動處理。

確認卡片已被辨識、驅動已綁定、介面也生出來了：

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

韌體版本可從 `dmesg` 確認（實測為 42.4.0）：

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

宣告支援的介面模式（這決定後面哪些能力能用）：

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

這份清單列出了 `IBSS / managed / AP / AP/VLAN / monitor`。這裡要特別提醒：雖然清單列了 IBSS，實測 `ibss join` 之後 `iw link` 卻顯示 Not connected，連不起來；mesh、active-monitor、P2P 則根本不在清單上（詳見第 4 節限制）。這是 RTL8811AU 的硬體與驅動現況，跟天線數無關。

頻段涵蓋：2.4 GHz ch1–13（ch14 disabled）；5 GHz ch36–165（其中 ch52–144 標記 radar / DFS）。預設 regdomain 為 `TW`，TX 功率 2.4 GHz 30 dBm、5 GHz UNII-1/2 23 dBm、UNII-3 30 dBm。

---

## 3. 實測能力：Monitor / Injection / AP / WPA3

先看核心能力總表，再逐項展開。所有項目都在自有 YUPITEK AP + 自有 iPhone 7 Plus 上完成。

| 能力 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor（監聽接收） | ✅ 強 | ✅ 強 |
| Injection（封包注入） | ✅ **100%**（30/30） | ✅ **96%**（29/30，需先解鎖 reg） |
| AP 熱點（hostapd） | ✅ iPhone 連入 + 完成 handshake | ✅ **穩定**（802.11a、20 MHz 實測；VHT80 未測） |
| AP WPA3-SAE | 未實測 | ✅ iPhone 連入（SAE-only + PMF） |

### 3-1. Monitor（監聽模式，2.4 GHz + 5 GHz）✅

切到 monitor 後，六個頻道各做一次定長擷取，接收都正常。熱門頻道在 6 秒內即達 300 幀的擷取上限：

| 頻道 | 擷取 frames |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

2.4 GHz 與 5 GHz 都收得穩。對一張單天線的隨身卡來說，這個接收表現足以應付現場頻道盤點和封包診斷。ch11、ch149、ch157 的幀數偏低，是那幾個頻道當下空中流量本來就少，不是網卡收不到；熱門的 ch1、ch6、ch36 六秒內就打滿 300 幀上限，接收顯然不是它的瓶頸。

### 3-2. Injection（封包注入）✅

以 `aireplay-ng --test` 對自家 YUPITEK AP 做定向注入測試。2.4 GHz 達 100%（30/30，`Injection is working!`），5 GHz 則是 96%（29/30）。5 GHz 有個設定細節要留意：預設 `reg=TW` 會鎖住部分 UNII 頻段的主動傳送，測試前先 `sudo iw reg set US` 解鎖、測完再 `sudo iw reg set TW` 設回。

```bash
# 2.4 GHz (YUPITEK 實際在 ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

單天線卡能在 2.4 GHz 拿到 100%、5 GHz 拿到 96%，已經是相當可靠的注入能力，這也是它能完成後面端到端 handshake 擷取的基礎。

### 3-3. AP 熱點（2.4 GHz / 5 GHz）✅

用 `hostapd` 把卡變成基地台，三種設定都讓 iPhone 7 Plus 成功連入並完成 4-way handshake（`EAPOL-4WAY-HS-COMPLETED`）：

- **5 GHz（802.11a、20 MHz 實測；VHT80 未測）**：最穩定的一組，iPhone 連入、handshake 完成、`AP-DISABLED` 乾淨收尾。
- **2.4 GHz（WPA2-PSK）**：iPhone 連入、handshake 完成，斷線後乾淨關閉。這裡誠實記一個狀況：前一輪同樣設定，曾在 STA 斷線後出現 `key not allowed / Failed to set beacon parameters` 而中止，重測卻無法重現，判定是 rtw88_8821au 偶發的 beacon re-key，不是固定瑕疵。長時間、高頻率重連的場景還是建議留意，或乾脆改用 5 GHz AP。
- **WPA3-SAE（5 GHz，PMF 強制；2.4 GHz 未實測）**：關鍵設定為 `wpa_key_mgmt=SAE`（純 WPA3、無 WPA2 fallback）、`ieee80211w=2`（強制 Management Frame Protection）、`sae_pwe=0`（相容舊端點）。iPhone 7 Plus（iOS 15）以 SAE 成功連入。AP 只開 SAE、沒有 WPA2 退路，能完成關聯就代表 SAE 認證握手成立。RTL8811AU + rtw88_8821au 在 AP 端的 WPA3-SAE 可用。

---

## 4. 端到端 handshake 能力與限制

### 4-1. 端到端 handshake 擷取 ✅

這是驗證注入加擷取能不能真正「串起來」的綜合測試，全程在自有 YUPITEK AP、自有 iPhone 7 Plus、已授權的前提下進行。流程是：monitor 到目標頻道 → 對自有裝置送定向 deauth 觸發重連 → 擷取完整的 4-way（M1–M4）→ 用 `hcxpcapngtool --all` 轉出 hashcat 可讀的 `.22000`。

實測結果：`aircrack-ng` 判定 YUPITEK 取得 1 個 handshake，EAPOL 四個訊息 M1–M4 全到齊，client 為 Apple OUI（`b8:53:ac`，確認是 iPhone 7 Plus），轉出的 `.22000` 可直接餵 hashcat。這代表 AWUS036ACS 具備完整的端到端 handshake 擷取能力。

兩個實測要點值得記錄（完整逐步設定另見專文）：

1. **辦公室同頻有多台同名 AP 時，不要用 `--bssid` 鎖單一台**，改擷取整個頻道，才不會漏掉連在另一台上的裝置。
2. `hcxpcapngtool` 預設較嚴格，可能回「not enough M1」；加 `--all` 即可由完整 M1–M4 轉出 `.22000`。

這條握手（handshake）擷取鏈所用的 Kali 常用工具（aircrack-ng、hcxtools）都是直接在 Ubuntu 24.04 ARM64 上執行，airodump-ng、aireplay-ng、hcxpcapngtool 皆正常運作。

### 4-2. VIF（虛擬介面）✅

`iw dev $IF interface add mon9 type monitor` 可建立 monitor VIF 並擷取到 100 frames；另以腳本建立「主介面連 YUPITEK 當 STA + 一個 AP VIF」，單晶片可同時扮演 STA 與 AP。

### 4-3. 誠實限制（實測回報）

| 進階模式 / 工具 | 狀態 | 實測 |
|---|---|---|
| Active monitor | ❌ 不支援 | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc（IBSS） | ❌ 不支援 | 模式列出但 `ibss join` 後 `iw link` = Not connected |
| Mesh（802.11s） | ❌ 不支援 | `set type mp` → `-95` |
| Wi-Fi Direct（P2P） | ❌ 不支援 | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ 無法 arm | `failed to arm interface`：rtw88_8821au 不提供 active-monitor；改用 airodump-ng + aireplay-ng |

另外還有兩個維運面的限制要知道。單串流 1x1 決定了它的理論上限（HT Max RX 150 Mbps、VHT80 約 433 Mbps），吞吐本來就不是它的強項。反覆切換 monitor / AP 之後，RX 偶爾會短暫 degraded（掃不到東西），這時實體拔插一次卡就能復原，介面名稱由 MAC 決定，拔插後維持不變。

---

## 5. 適用情境與選型（輕量隨身，連回 Hub）

把上面這些能力對回產品定位，AWUS036ACS 的角色很清楚：一張能力完整、但主打輕便的隨身卡。那它適合用在哪些情境？

- **現場快速盤點 / 隨身診斷**：單天線、小體積、低功耗，帶出門做頻道盤點、訊號巡檢、封包診斷都合用。搭配 GX10 這類中央平台，隨身卡在現場擷取，把資料連回 Hub 做集中分析，分工清楚。
- **教學與驗證**：Monitor / Injection / AP / WPA3-SAE / 端到端 handshake 這條主線它全數走得通，適合當示範與授權範圍內的驗證用卡。
- **不適合的情境**：需要最高吞吐、最遠距離，或需要 mesh / IBSS / P2P / active-monitor 的場景，這張卡不是對的選擇。

輕量不等於功能縮水。主線能力它一條都沒少，被取捨掉的是吞吐天花板和進階介面模式。所以選不選它，看你要的是「帶著走」還是「跑得滿」。

和同家族相比，定位差異如下：

| 需求 | 建議卡 | 理由 |
|---|---|---|
| 輕量隨身 + 主線能力完整 | **AWUS036ACS** | 2.4G 注入 100%、5G 96%、端到端 handshake 可用，單天線輕便 |
| 雙頻注入都要 100% / 更穩的滲透驗證 | AWUS036EACS、AWUS036ACH | 兩頻注入 100%，EACS 另含 BT |
| 最強接收 / 長距離 monitor | AWUS036AXER、AWUS036ACH | 跳頻掃到更多目標 / 雙天線高增益 |
| mesh / IBSS 單機實驗 | AWUS036ACM、AWUS036ACHM | mt76 驅動單機可建立（Realtek rtw88 不支援） |

一句話選型：要輕便、又要主線能力齊全，AWUS036ACS 是合適的隨身選擇；要雙頻注入都 100%、或更重的滲透驗證，就往 EACS / ACH 走。

---

## 常見問題（FAQ）

**Q：AWUS036ACS 在 Ubuntu 24.04 ARM64 要裝驅動嗎？**
在本文測試的 kernel 6.17（ASUS GX10）上不用：RTL8811AU 由內建 rtw88_8821au 驅動，插上即認，免編譯、免 DKMS。kernel 較舊時，先用 `modinfo rtw88_8821au` 確認模組存在。

**Q：AWUS036ACS 支援 monitor mode（監聽模式）和 packet injection（封包注入）嗎？**
支援。2.4 GHz、5 GHz 都能 monitor；`aireplay-ng --test` 注入 2.4G 為 100%（30/30）、5G 為 96%（29/30，需先 `iw reg set US` 解除 TW 限制）。不支援 active monitor。

**Q：AWUS036ACS 能擷取 WPA handshake（握手封包）並轉成 hashcat .22000 嗎？**
能。在自有 AP 與自有 iPhone 7 Plus 上端到端實測：定向 deauth 觸發重連，擷取完整 4-way（M1–M4），再用 `hcxpcapngtool --all` 轉出 .22000。僅限自己擁有或已授權的網路。

**Q：AWUS036ACS 可以當 AP 熱點嗎？支援 WPA3 嗎？**
可以。`hostapd` 開 2.4G 與 5G 熱點（5G 以 802.11a、20 MHz 實測；VHT80 未測），iPhone 7 Plus 連入並完成 4-way；5G 的 WPA3-SAE（SAE-only、ieee80211w=2、sae_pwe=0）也連入成功（2.4G 的 WPA3 未實測）。

**Q：AWUS036ACS 不支援哪些模式？hcxdumptool 能用嗎？**
不支援 active monitor、IBSS、mesh（802.11s）、Wi-Fi Direct（P2P）。hcxdumptool 8.x 會 failed to arm interface，請改用 airodump-ng + aireplay-ng。要 mesh / IBSS 請選 AWUS036ACM / ACHM。

---

## 6. 延伸閱讀

- 九張 ALFA 卡的完整能力比較與選型總評 → [ALFA 無線網卡總評 Hub（總表）](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [免裝驅動：Ubuntu 24.04 + kernel 6.17 啟用 Monitor / AP（rtw88 / rtw89 / mt76 實測）](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [WPA3-SAE 與端到端 handshake 擷取逐步教學](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 同家族 BT+WiFi 複合卡 → [AWUS036EACS 逐卡實測](/zh-tw/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*測試單位：Yopitek（ALFA Network 台灣經銷）— https://www.yupitek.com ｜ 測試環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 測試裝置：Apple iPhone 7 Plus*
