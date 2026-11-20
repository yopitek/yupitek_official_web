---
title: "AWUS036ACH 單卡實測：Realtek RTL8812AU 雙天線 AC1200 在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP・WPA3 全測報告"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "AWUS036ACH（RTL8812AU）在 Ubuntu 24.04 / kernel 6.17 免裝 DKMS，雙頻監聽模式可用、封包注入 100%，端到端 WPA handshake（.22000）已實證，並附 5G 接收卡死等限制。"
faq:
  - question: "AWUS036ACH 在 Kali 或 Ubuntu 需要裝驅動嗎？"
    answer: "看核心版本。Linux 核心 6.13 以上（本次實測 Ubuntu 24.04 / kernel 6.17）已內建 rtw88_8812au 驅動，插上即認、免編譯、免 DKMS；核心低於 6.13 才需要另外用 DKMS 安裝 lwfinger/rtw88。Kali 請先用 uname -r 確認核心版本，本次未在 Kali 實機驗證。"
  - question: "AWUS036ACH 的 monitor mode 與封包注入表現如何？"
    answer: "2.4GHz 與 5GHz 都能進 monitor mode；aireplay-ng 逐台定向注入在 2.4GHz（對 4 台 AP）與 5GHz（對 YUPITEK ch36）都是 30/30 = 100%。5GHz 注入前要先把法規網域設成允許發射的設定（例如 iw reg set US），預設 country 00 下 5GHz 禁止發射，注入會送不出去。"
  - question: "AWUS036ACH 可以擷取 WPA handshake 嗎？"
    answer: "可以，且端到端已實證。兩頻注入都是 100%；2026-11-19 補測在自有 iPhone 15 Pro、5GHz ch36 上擷到完整 4-way 交握，並用 hcxpcapngtool 轉出 47 筆 hashcat .22000 hashline。僅限自有或已取得授權的網路。"
  - question: "AWUS036ACH 開 WPA3 熱點，iPhone 7 Plus 連不上怎麼辦？"
    answer: "hostapd 要設 sae_pwe=0 並搭配 ieee80211w=2，iPhone 7 Plus 才連得上；用 sae_pwe=2 會連不上。同樣的設定在 AWUS036ACHM 上也是關鍵。"
  - question: "AWUS036ACH 的 5GHz 接收突然卡死（抓到 0 封包）怎麼辦？"
    answer: "這是 rtw88_8812au 的已知現象：反覆切換模式或變更法規網域後，5GHz 接收可能卡死，軟體無法復原，只能實體拔插或重開機。建議 5GHz 測試前先重新插卡，並優先完成 5GHz 項目。"
draft: false
---

> 測試單位：Yupitek（ALFA Network 台灣經銷）｜測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia｜測試裝置：自有 Apple iPhone 7 Plus｜測試對象：自有辦公室 Wi-Fi（SSID `YUPITEK`，2.4G ch5 / 5G ch36、157）｜測試日期：2026-11-18。
>
> 本文屬經銷商對產品相容性與能力邊界的硬體驗證：所有 Monitor / Injection / AP / handshake 量測，皆於 Yupitek 自有設備、自有辦公室 Wi-Fi、對自有測試手機進行，不針對任何第三方網路，亦不提供對外部網路的攻擊操作步驟。文中數據皆為實機量到的數字與狀態，不以規格書推測。

## 重點摘要（TL;DR）

AWUS036ACH 於 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）實測：雙頻 monitor 可用，兩頻逐台封包注入皆為 30/30 = 100%，雙頻皆可架 AP 熱點（純 802.11g / 純 802.11a）。

- kernel 6.13 以上免裝 DKMS（本次 Ubuntu 24.04 / kernel 6.17），rtw88_8812au 內建、插上即認。
- 雙頻監聽模式（monitor mode）可用，兩頻逐台封包注入都是 30/30 = 100%。
- 端到端 WPA handshake 已實證：2026-11-19 補測在自有 iPhone 15 Pro、5G ch36 擷到完整 4-way，轉出 47 筆 .22000 hashline。
- 5GHz 接收可能卡死，只能實體拔插或重開機。
- 單機可建立 IBSS，但不支援 802.11s mesh、active monitor 與 Wi-Fi Direct（P2P）。

## 1. 這張卡與測試平台

AWUS036ACH 是 ALFA Network 定位在「雙天線高增益」的 USB 無線網卡，採用 Realtek RTL8812AU 晶片，規格為 Wi-Fi 5（802.11ac）、2T2R、雙頻 AC1200。相較於同系列單天線的 AWUS036ACHM（MediaTek MT7610U，AC600），ACH 以兩根外接高增益天線換取更好的接收與較穩的 injection 表現，是客戶詢問「長距離 monitor」與「兩頻注入」時的常見候選。

本次測試平台與條件如下：

- 運算平台：ASUS GX10（ARM64 / aarch64）
- 作業系統：Ubuntu 24.04 LTS
- 核心版本：kernel 6.17.0-1014-nvidia
- 測試裝置：Apple iPhone 7 Plus（2.4G / 5G / WPA3 皆以此機實測）
- 測試環境：自有辦公室 Wi-Fi，SSID `YUPITEK`（2.4GHz ch5 / 5GHz ch36、ch157）
- 測試日期：2026-11-18 實機量測

全程只操作 ALFA 卡對應的 `wlx*` 介面，不碰 GX10 對外上網的內建網卡，也不執行 `airmon-ng check kill`（該指令會關掉 NetworkManager，導致主機斷線）。

## 2. 硬體與驅動（晶片 / USB ID / in-kernel 免裝）

| 項目 | 規格 |
|---|---|
| 型號 | AWUS036ACH |
| 晶片 | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| 驅動 | `rtw88_8812au`（kernel 內建，mainline ≥ 6.13） |
| 韌體 | `rtw88/rtw8812a_fw.bin`（系統內附） |
| 世代 / 串流 | Wi-Fi 5（802.11ac）/ 2T2R |
| 頻寬等級 | 雙頻 AC1200 |
| 天線 | 雙天線高增益（外接） |
| USB 介面 | USB 3.0（實測列舉為 5000M） |

ACH 在 GX10 的 6.17 kernel 上是真正的隨插即用：`lsusb` 認到 `0bda:8812`，驅動 `rtw88_8812au` 自動綁定，韌體 `rtw8812a_fw.bin` 系統已內附，免編譯、免 DKMS。這一點對 ARM64 環境特別重要。許多舊的 out-of-tree Realtek 驅動在 aarch64 上得自原始碼編譯，而 morrownr/USB-WiFi 與 aircrack-ng/rtl8812au 這兩個老專案現在都已改導向這顆內建驅動，bug 回報集中到 lwfinger/rtw88。因此 kernel ≥ 6.13（含 GX10 的 6.17）的使用者不必再碰第三方 DKMS；只有舊 kernel（< 6.13）才需要另外 DKMS 安裝 `lwfinger/rtw88`。這個上游專案目前仍在活躍維護（最新 commit 為 2026-10-24，內容包含 8812A 的藍牙 1T1R 修正），代表這顆晶片在主線的支援還在持續更新，不是停更的老驅動。

硬體連接有一個細節要注意：ACH 是 USB-A 公頭，請用 USB-C→A 轉接頭直插 GX10 的 USB-C 埠，走 USB 3.0（列舉顯示 5000M）。若把它接在鍵鼠的 USB 2.0 hub 後面會被限速，量不出 USB3 的行為。

介面模式方面，`iw phy` 回報支援 IBSS / managed / AP / AP-VLAN / monitor，但沒有 mesh、P2P 與 active-monitor，這條界線直接決定了第 4 節的部分限制。

## 3. 實測能力：Monitor / Injection / AP / WPA3

| 功能 | 2.4 GHz | 5 GHz | 實測數據 |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames；5G ch36/149/157 = 260/137/127 frames |
| Injection（廣播探測） | ✅ | ✅ | `aireplay-ng --test` broadcast probe 兩頻皆回 Injection is working |
| Injection（逐台定向） | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G 對 4 台 AP（含 YUPITEK）；5G 對 YUPITEK ch36 |
| AP 熱點（iPhone 7 Plus） | ✅ 純 802.11g | ✅ 純 802.11a（ch36） | 4-way handshake 完成，首次即連上 |
| WPA3-SAE AP | ✅（`sae_pwe=0`） | 未實測 | 搭 `ieee80211w=2`，iPhone 7 Plus 連上（僅在 2.4 GHz 實測） |

**Monitor**：2.4GHz 在 ch1 / ch6 / ch11 分別抓到 92 / 214 / 71 個 frame；5GHz 在 ch36 / ch149 / ch157 抓到 260 / 137 / 127 個 frame。兩頻 monitor 皆正常，5GHz 的收量甚至高於 2.4GHz（ch36 抓到 260 frame），與雙天線高增益的定位相符。

**Injection**：這是 ACH 的強項。2.4GHz 下 `aireplay-ng --test` 先做 broadcast probe（回報 Injection is working、Found 4 APs），再逐台定向，對含 YUPITEK 在內的 4 台 AP 回應率都是 30/30 = 100%，min/avg/max RTT 約 4.9 / 39.2 / 99.0 ms、Power 約 -47。雙天線 ACH 的 2.4G injection 比單天線 ACHM 明顯更穩。實作上要記得加 `--ignore-negative-one`：這是 lwfinger/rtw88 #453 的已知現象：STA 介面開著時，monitor channel 可能回報 `-1`，不加這個旗標會被誤判成注入失敗。另外依上游紀錄，重負載 injection 下內建 driver 偶有 USB reset，但本次約 90 秒的量測並未觀察到。5GHz 下對 YUPITEK（ch36）逐台定向同樣 30/30 = 100%，平均 RTT 13.6 ms、Power -69.1。這是在「新插卡 + regdomain 設為可 TX 的法規」前提下量到的結果（細節見第 4 節的 5G 注意事項）。

**AP 熱點**：以 hostapd 開台，2.4GHz 走純 802.11g（`ieee80211n=0`）、5GHz 走純 802.11a（ch36），iPhone 7 Plus 兩頻都第一次就連上，沒有 association 失敗；log 可見 authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED 完整四步。實測經驗是：ACH 在「關掉 802.11n、純 g / 純 a」的設定下連線最乾淨。

**WPA3-SAE**：開 SAE-only AP 時，關鍵參數是 `sae_pwe=0`（hunting-and-pecking）搭配 `ieee80211w=2`，iPhone 7 Plus 才連得上；若用 `sae_pwe=2` 會連不上。這與同系列 ACHM 踩到的是同一個相容性雷點。

## 4. 進階能力與 handshake：可行範圍與誠實限制

| 進階能力 | 結果 | 說明 / 證據 |
|---|---|---|
| VIF（STA + monitor 同時） | ✅ 實測可用 | 主介面 managed 與 `mon9`（monitor）同時 up，monitor VIF 8 秒抓 100 frame |
| WPA handshake 擷取 | ✅ 端到端（.22000）已實證 | 兩頻注入 100%；2026-11-19 補測 5G ch36 擷到完整 4-way，hcxpcapngtool 轉出 47 筆 `.22000` hashline |
| macchanger（改 MAC） | ✅ | 隨機 MAC 設定與還原皆正常（需先 `ip link down`） |
| Ad-hoc（IBSS） | 🟡 單機 | 單機 `Joined IBSS` 成功；peer link 因無第二台裝置未測 |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh（802.11s） | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct（P2P） | ❌ | `Operation not supported (-95)` |

**handshake 擷取能力要講清楚**：ACH 的兩頻 injection 都是 100%，而 injection 正是「deauth 自有測試手機 → 擷取完整 4-way（M1–M4）→ 以 hcxpcapngtool 轉出 hashcat `.22000`」這條端到端工作流的發動端。2026-11-19 補測在自有 iPhone 15 Pro、5GHz ch36 上擷到完整 4-way 交握，並以 hcxpcapngtool 轉出 47 筆 `.22000` hashline，因此 ACH 的端到端 handshake 擷取已實證。在我們 9 款卡的總表中，端到端（`.22000`）已實證的共 7 款：AWUS036ACM、AWUS036ACHM、AWUS036ACH、AWUS036ACS、AWUS036EACS、AWUS036AX 與 AWUS036AXER。所有擷取僅限於自有或已取得授權的網路。

**VIF**：`iw phy` 的旗標寫 interface combinations are not supported，但實機上 managed 主介面與另開的 monitor 介面 `mon9` 可以同時 up，`mon9` 在 8 秒內抓到 100 個 frame，也就是「邊上網邊側錄」在 ACH 上行得通。要提醒的是：phy 並未保證此組合，長時間或重負載情境建議改用 mt76 系列（ACM / ACHM）。

**三個要特別標注的限制：**

1. **不支援 Active monitor、Mesh（802.11s）與 Wi-Fi Direct（P2P）**：三者實測皆回 `Operation not supported (-95)`。需要這三項能力請改用 mt76 系列卡（ACM / ACHM 的 phy 有宣告 mesh / P2P / active-monitor）。
2. **5G RX 卡死（`rtw88_8812au` 已知現象）**：剛插卡時 5G monitor / injection 正常，但反覆切換模式或變更 regdomain 後，5G 接收可能卡死（抓到 0 封包），且軟體無法復原，只能實體拔插或重開機。建議做 5G 測試前先拔插一次、並優先完成 5G 項目。這裡也補充 5G injection 能送出的前提：預設 `country 00` 下 5G 全是 passive / no-IR（禁止 TX），定向注入根本送不出去；要設成能 TX 的法規（`iw reg set US` 可解鎖 ch36 / ch149，`TW` 只放行 ch149 以上、不含 ch36），測完再設回 `TW`。而「新插卡」指的是實體拔插到 USB 重新列舉：`dmesg` 要看到 `USB disconnect` 與 `renamed from wlan0`、bus 編號改變才算數；若 5G 已卡死，aireplay 會回 `No such BSSID available`。
3. **hcxdumptool 在本平台除 AWUS036EACS 的 2.4 GHz 外，其餘全卡 `failed to arm`**：因為它需要 active-monitor，而 rtw88 / rtw89 / mt7921u 都不支援；要擷取 handshake 請改走 airodump-ng + aireplay-ng 這條路。

### 工具鏈相容性（Kali）

針對 Kali 常用工具對 ACH 做了一輪快篩（環境目標為自有 `YUPITEK`），結果如下：

| 工具 | 狀態 | 說明 |
|---|---|---|
| airmon-ng | ✅ | 正確列出 `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` 抓到 beacon（含 YUPITEK），20 packets captured |
| kismet | ✅ 已安裝 | `/usr/bin/kismet`，可當 data source 啟動 |
| bettercap | ✅ 已安裝 | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | 已安裝，但本平台 `failed to arm`（需 active-monitor，見上） |
| macchanger | ✅ | GNU 1.7.0；`-r` 隨機、`-p` 還原，實測正常 |
| wifite | ❌ 未安裝 | 本機無此指令，需另裝（建議用 git 版，避開與自編 aircrack-ng 的 apt 依賴衝突） |

結論很單純：airmon-ng 能正確辨識並管理 ACH，一般 monitor 與擷取流程走 aircrack-ng 套件（airodump-ng + aireplay-ng）最穩定；需要 active-monitor 的 hcxdumptool 在本平台無法 arm，不要卡在它身上。

## 5. 適用情境與選型建議（回到總表 Hub）

把 ACH 放回整條產品線來看，它的定位很清楚：雙天線高增益、兩頻 injection 100%、端到端 WPA handshake（.22000）已實證，是「需要穩定注入又想要較強接收」的客戶的務實選擇。

- **滲透測試（injection + handshake）**：首選群為 AWUS036EACS / AWUS036ACH / AWUS036ACS，三者兩頻注入表現都在高檔。
- **最強接收 / 長距離 monitor**：AWUS036AXER 與 AWUS036ACH，ACH 以雙天線高增益見長。
- **需要 802.11s mesh / active-monitor / P2P**：ACH（Realtek rtw88）做不到（實測回 `-95`），請改用 mt76 驅動的 AWUS036ACM / AWUS036ACHM；ACH 的 IBSS 僅單機可建立、peer-link 未測。
- **只需純 AP 或一般連線、不做注入**：MediaTek 的 AWUS036AXM / AXML 更穩，但注意它們在本平台 injection 失敗，不適合滲透用途。

一句話避雷：如果客戶的需求明確是注入與 handshake，就不要選 AWUS036AXM / AXML（MT7921 晶片的注入在本平台實測失敗，無法 deauth 或擷取 handshake）；這種需求 ACH 反而是穩妥的候選。選型時也別只看頻寬數字，雙天線高增益帶來的接收穩定度，在實際側錄距離上的差異往往比紙面規格更有感。選型決策與平台共通踩雷點，請見總表 Hub：[9 款 ALFA 無線網卡在 ASUS GX10（ARM64）的 Monitor・Injection・AP 全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 常見問題（FAQ）

**Q：AWUS036ACH 在 Kali 或 Ubuntu 需要裝驅動嗎？**
看核心版本。Linux 核心 6.13 以上（本次實測 Ubuntu 24.04 / kernel 6.17）已內建 rtw88_8812au 驅動，插上即認、免編譯、免 DKMS；核心低於 6.13 才需要另外用 DKMS 安裝 lwfinger/rtw88。Kali 請先用 uname -r 確認核心版本，本次未在 Kali 實機驗證。

**Q：AWUS036ACH 的 monitor mode 與封包注入表現如何？**
2.4GHz 與 5GHz 都能進 monitor mode；aireplay-ng 逐台定向注入在 2.4GHz（對 4 台 AP）與 5GHz（對 YUPITEK ch36）都是 30/30 = 100%。5GHz 注入前要先把法規網域設成允許發射的設定（例如 iw reg set US），預設 country 00 下 5GHz 禁止發射，注入會送不出去。

**Q：AWUS036ACH 可以擷取 WPA handshake 嗎？**
可以，且端到端已實證。兩頻注入都是 100%；2026-11-19 補測在自有 iPhone 15 Pro、5GHz ch36 上擷到完整 4-way 交握，並用 hcxpcapngtool 轉出 47 筆 hashcat .22000 hashline。僅限自有或已取得授權的網路。

**Q：AWUS036ACH 開 WPA3 熱點，iPhone 7 Plus 連不上怎麼辦？**
hostapd 要設 sae_pwe=0 並搭配 ieee80211w=2，iPhone 7 Plus 才連得上；用 sae_pwe=2 會連不上。同樣的設定在 AWUS036ACHM 上也是關鍵。

**Q：AWUS036ACH 的 5GHz 接收突然卡死（抓到 0 封包）怎麼辦？**
這是 rtw88_8812au 的已知現象：反覆切換模式或變更法規網域後，5GHz 接收可能卡死，軟體無法復原，只能實體拔插或重開機。建議 5GHz 測試前先重新插卡，並優先完成 5GHz 項目。

## 6. 延伸閱讀

- 總表 Hub：[9 款 ALFA 無線網卡 ARM64 全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 免裝驅動在 Ubuntu（ARM64）啟用 Monitor 與 AP：[placeholder](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- WPA3-SAE handshake 擷取與 `sae_pwe` 相容性：[placeholder](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 姊妹卡對照：AWUS036ACHM（單天線 AC600）單卡實測 [placeholder]
- 本型號完整證據路徑（內部）：`AWUS036ACH_evidence/`（p0 列舉、p1_gx10 行為、retest 排查）

<!-- hreflang：zh-TW 為主稿；zh-CN / en / ja / ko / de / fr / es 待本稿定稿後生成並補 rel=alternate。 -->
