---
title: "ALFA AWUS036EACS 單卡實測：RTL8821CU（BT + WiFi 複合）在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP・端到端 handshake"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS（藍牙+Wi-Fi 複合）在 Ubuntu 24.04 ARM64 實測：免裝驅動，兩頻注入 100%、Monitor、AP、WPA3-SAE，端到端 handshake（79 ACKs、.22000）通過。附 USB 重插風險。平台 ASUS GX10、RTL8821CU。"
faq:
  - question: "AWUS036EACS 在 Ubuntu 24.04 ARM64 要裝驅動嗎？"
    answer: "在本文測試的 kernel 6.17（ASUS GX10）上不用：RTL8821CU 由內建 rtw88_8821cu 驅動，插上即辨識，免編譯、免 DKMS；介面名稱為 wlx 加 MAC，重插後不變。"
  - question: "AWUS036EACS 的 monitor mode 與封包注入表現如何？"
    answer: "monitor 在 2.4G、5G 都穩，多數頻道收滿 300 frames；aireplay-ng --test 兩頻皆 30/30（100%）。5G 注入前需 iw reg set US 解除 TW 對 TX 的限制。"
  - question: "AWUS036EACS 能擷取 WPA handshake 嗎？"
    answer: "能。自有 AP 加自有 iPhone 7 Plus 端到端實測：deauth 收到 79 ACKs，擷取完整 M1–M4，hcxpcapngtool --all 轉出 .22000（784 bytes、2 組 EAPOL pairs）。僅限自有或已授權網路。"
  - question: "AWUS036EACS 插上後 lsusb 看得到、卻沒有 wlx 網路介面怎麼辦？"
    answer: "這是 BT+Wi-Fi 複合裝置的 probe 競態：藍牙已綁 btusb，Wi-Fi 的 rtw88_8821cu 卡住。實測重載模組、手動 bind 多半無效，可靠解法是拔卡後換另一個 USB 孔重插。"
  - question: "AWUS036EACS 支援 mesh、IBSS 或 hcxdumptool 嗎？"
    answer: "不支援。rtw88 的 active-monitor、IBSS、mesh、P2P 回 -95 或 join 無效；hcxdumptool 8.x 僅在 2.4 GHz 可 arm（5 GHz 會 failed to arm），請改用 airodump-ng + aireplay-ng。VHT 僅 80 MHz。要 mesh / IBSS 請選 AWUS036ACM / ACHM。"
draft: false
---

> 測試單位：Yupitek（ALFA Network 台灣經銷）｜測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia｜測試裝置：自有 iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）｜測試對象：自有辦公室 Wi-Fi（SSID YUPITEK，2.4G ch5 / 5G ch36、157）。
>
> 本文為 AWUS036EACS 單卡的能力與相容性實測。所有 Monitor / Injection / handshake 擷取，均於 Yupitek 自有設備、自有辦公室 Wi-Fi、對自有測試手機進行，屬經銷商對硬體的正當能力驗證；不針對任何第三方網路，亦不提供攻擊操作步驟。

**重點摘要（TL;DR）**：AWUS036EACS 在 GX10 / Ubuntu 24.04（kernel 6.17）免裝驅動；兩頻注入 100%，端到端 .22000 通過（79 ACKs）；BT+Wi-Fi 複合卡須留意重插。

## 1. 這張卡與測試平台

AWUS036EACS 是 ALFA 的輕量隨身型 Wi-Fi 5（802.11ac）USB 網卡，晶片是 Realtek RTL8821CU，1x1 單串流、2.4GHz 與 5GHz 雙頻，還內建藍牙，屬於 BT + WiFi 複合裝置。這篇把它單獨搬上 Yupitek 的實驗桌，在 ASUS GX10（ARM64）配 Ubuntu 24.04 的環境逐項驗收，回答客戶最在意的幾個問題：驅動在 ARM64 上認不認、能進哪些模式、效能到哪裡。

先把定位講清楚。這是經銷商對自家貨的相容性與能力邊界驗證，不是攻擊教學。文中所有 injection 與 handshake 相關的能力量測，一律在自有封閉環境、對自有裝置進行，不提供任何對外部網路的操作步驟。

測試平台與方法比照本批其他單卡文：

- 運算平台：ASUS GX10（ARM64 / aarch64）
- 作業系統：Ubuntu 24.04 LTS，kernel 6.17.0-1014-nvidia
- 驅動策略：使用 kernel 內建（in-kernel）驅動，插上即辨識，不裝任何第三方 DKMS 模組
- 測試裝置：Apple iPhone 7 Plus（WPA3-SAE 另以 iPhone 15 Pro 複測）
- 測試環境：自有辦公室 Wi-Fi，SSID YUPITEK，2.4GHz ch5 / 5GHz ch36、ch157
- 安全守則：全程只操作 `wlx*` 介面，不碰內建對外上網主線；絕不執行 `airmon-ng check kill`（會關掉 NetworkManager 使 GX10 對外斷線）

## 2. 硬體與驅動：BT + WiFi 複合裝置的真相

先看底細。下表是 AWUS036EACS 在 kernel 6.17 上實際掛載的狀態：

| 項目 | 內容 |
|---|---|
| 晶片 | Realtek RTL8821CU（1x1 單串流） |
| 世代 | Wi-Fi 5（802.11ac），2.4 + 5GHz |
| 複合功能 | BT + WiFi 複合裝置（內含藍牙） |
| USB ID | `0bda:c820` |
| 驅動 | `rtw88_8821cu`（in-kernel，kernel 6.2 起支援 USB） |
| 韌體 | 24.11.0（H2C version 12，實測 dmesg） |
| VHT 頻寬 | 僅 80MHz（無 160 / 80+80） |

以 `iw phy` 查詢，支援的 interface mode 為 `managed` / `AP` / `AP/VLAN` / `monitor`（`IBSS` 有列出但實測 join 無效）；頻段涵蓋 2.4GHz ch1–13 與 5GHz ch36–165（其中 ch52–144 為 DFS 頻段）；cipher 含 CCMP-256、GCMP-128 / GCMP-256 與 CMAC，具備在 AP 端跑 WPA3 的條件。

驅動部分沒有懸念。RTL8821CU 的 USB 支援自 kernel 6.2 併入主線 `rtw88`，GX10 的 kernel 6.17 已內建 `rtw88_8821cu`，插上即載入，不需要編譯或 DKMS。早期 in-kernel 版本的 AP mode 曾有 bug，已由 macid patch（linux-next-20240911 起）修復，本次 kernel 6.17 上的 AP 三模式實測皆正常收尾。確認方式：

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Wi-Fi 介面載入後會以 `wlx` + MAC 命名（例如 `wlx00c0cab3a52e`），而非 `wlan0`；重插後名稱不變，寫腳本時可穩定引用。

真正要留意的是「複合裝置」這件事。用 `lsusb -t` 檢視，會看到同一顆 RTL8821CU 底下掛了多個 USB interface：藍牙功能綁 `btusb`，Wi-Fi 功能另外綁 `rtw88_8821cu`。

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- 藍牙
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- 藍牙
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

（Bus／Port 編號會隨插拔次數改變；重點是 interface 0/1 走 `btusb`、interface 2 才是 Wi-Fi 的 `rtw88_8821cu`。）

**BT + WiFi 複合裝置的重插風險（部署前必讀）。** 因為藍牙與 Wi-Fi 共用同一個 USB 裝置，在某些 USB 孔或快速重插的情況下，可能發生藍牙已經綁上 `btusb`、但 Wi-Fi 那個 interface 的 probe 卡住，結果 `lsusb` 看得到 `0bda:c820`、卻生不出 `wlx` 介面的競態。實測中，`modprobe -r` 後重載、或手動 `bind` 多半無效（`bind` 會回 `Operation already in progress`）。可靠解法只有一個：拔卡、換一個 USB 孔重插，換孔後列舉乾淨、`wlx` 介面即正常出現。這是這張卡相較於非複合的 AWUS036ACS（RTL8811AU）額外要知道的操作細節，先知道就不會誤判成卡片故障。

## 3. 實測能力：Monitor / Injection / AP / WPA3

下表是 AWUS036EACS 的核心能力實測摘要，每條均於 2026-11-18 在 GX10 實機執行：

| 能力項目 | 2.4GHz | 5GHz | 實測重點 |
|---|---|---|---|
| Monitor | ✅ 強 | ✅ 強 | 多數頻道滿額 300 frames；社群 #453「ch1 卡死」未重現 |
| Injection | ✅ 100%（30/30） | ✅ 100%（30/30） | Power 2.4G -38.27 / 5G -76.10；本批 ac 卡注入最強 |
| AP 熱點 | ✅ 乾淨收尾 | ✅ VHT 80MHz | `hostapd` 建站，iPhone 7 Plus 連入並完成 4-way |
| WPA3-SAE（AP 端） | ✅ iPhone 連入 | 未實測 | SAE-only + 強制 PMF（`ieee80211w=2`、`sae_pwe=0`） |
| WPA handshake 擷取 | — | ✅ 端到端 | M1–M4 完整，deauth 收 79 ACKs，轉出 `.22000` |

Monitor（監聽模式）在 2.4 與 5GHz 都穩。六個頻道逐一擷取，多數都收到滿額 300 frames。對 8821cu 來說，這裡還有一個很重要的正面結果：rtw88 社群長期追蹤的 GitHub #453「8821cu 在 kernel ≥6.9、STA up 時 monitor 卡在 ch1」，在 GX10 這個環境並未重現，5GHz 的 ch36、ch149、ch157 都能穩定收滿 300 幀。要跨 2.4 / 5GHz 做頻譜勘查或封包解析，這張卡的 monitor 可以放心用。

Injection（封包注入）的表現最亮眼。以 `aireplay-ng --test` 量測，2.4GHz 與 5GHz 都是 30/30、100%，是本批 ac 卡裡注入最強的一張（同為 1x1 的 AWUS036ACS 在 5G 只有 96%）。這裡有個台灣在地的細節：5GHz 的 TX 在 regulatory domain 設為 TW 時會被鎖，量測前先 `iw reg set US` 解鎖，測完再 `iw reg set TW` 還原。

AP 熱點這邊，以 `hostapd` 分別架 2.4GHz（WPA2）、5GHz（VHT 80MHz）、WPA3-SAE 三種，iPhone 7 Plus 都能連入並完成 4-way handshake，關站也收尾乾淨（`AP-DISABLED` / `TERMINATING`）。沒有出現某些卡會有的 beacon re-key 問題，2.4G 這點比姊妹卡 ACS 更穩。WPA3 採 SAE-only 搭配強制 PMF（`ieee80211w=2`、`sae_pwe=0`），以 iPhone 15 Pro 成功連入，確認 RTL8821CU 在 AP 端的 WPA3-SAE 可用。

Kali 工具鏈（平台層）在這張卡上也都帶得起來：`airmon-ng` 偵測得到 EACS（`rtw88_8821cu`），但一樣不要用 `check kill`；`kismet` 以本卡當 data source 啟動成功，實測產出約 733 KB 的 `.kismet` log；`bettercap` 2.32 的 `wifi.recon on` 正常運作（txpower 警告可忽略）；`wifite`（git 3.0.0）掃到 10 台以上 AP、含自家 YUPITEK（ch5、PWR 84），這一版沒有 `--band` 旗標，要改用 `-c 1,6,11,36,149,157` 指定頻道；`Wireshark` / `tshark` 4.x 在 monitor ch6 實擷取並解析 325 frames；`macchanger` 的隨機 MAC 偽裝也能用。工具層這一段跟本批其他卡一致，差異主要落在前面的 injection 與 monitor 硬體能力。

## 4. 端到端 handshake：亮點與誠實限制

這張卡的亮點能力，是把 injection 與 capture 串成一條完整可用的鏈。在自家 YUPITEK AP 與自有 iPhone 7 Plus 之間，整條鏈實機跑通：對自有 iPhone 送出 deauth（injection，實測收到 79 個 ACKs，證實注入封包確實到達 client）→ iPhone 重新連線時收齊完整的 4-way handshake（握手，M1、M2、M3、M4 各 1）→ 以 `hcxpcapngtool --all` 轉出 hashcat 格式的 `.22000`（784 bytes，2 組 EAPOL pairs，RC checked）。整個流程只為驗證卡片能力，對象全程是自家 AP 與自有手機，不涉及任何第三方網路。

實務上兩個關鍵細節值得記下：辦公室同時有多台同名 YUPITEK AP 在 ch36，擷取時不要鎖 `--bssid`，直接收整個頻道，才不會把 iPhone 實際連的那台濾掉；另外 `hcxpcapngtool` 預設較嚴格，要加 `--all` 才轉得出 `.22000`。

誠實限制也要一次講清楚：

- **不支援 active-monitor / IBSS（Ad-hoc）/ Mesh（802.11s）/ Wi-Fi Direct（P2P）。** 這些模式在 `rtw88` 下回 `-95`（Operation not supported），或列得出來但 join 無效，屬驅動層限制，無解。需要 mesh / IBSS 實驗的客戶應改走 MediaTek 的 AWUS036ACM / ACHM。
- **`hcxdumptool` 8.x 受限。** 它需要 active-monitor；本卡僅在 2.4 GHz 可 arm、5 GHz 會 `failed to arm`（其餘各卡皆 `failed to arm interface`）；改用 `airodump-ng` + `aireplay-ng` 即可，本卡注入 100%，不受影響。
- **VHT 僅 80MHz。** 單串流、無 160MHz 或 80+80，定位就是輕量隨身卡，不是衝吞吐的角色。
- **VIF 僅部分支援。** 只能做到被動 monitor 與 managed 在同一頻道並存（software monitor，實測擷取 100 frames）；不支援獨立的雙 VIF。

## 5. 適用情境與選型

綜合實測，AWUS036EACS 的定位很清楚：需要雙頻 Monitor + Injection + 端到端 handshake 驗證，又想要一張輕巧、內建藍牙的隨身卡，它就是合適解。兩頻注入 100% 與乾淨的 AP / WPA3 表現，讓它在授權範圍內的無線稽核與資安教學用途上，和 AWUS036ACH、AWUS036ACS 同列首選群。

什麼情況建議改選別張：

- **現場會頻繁重插、或機箱 USB 孔品質參差** → 複合裝置的 probe 競態會增加困擾，可考慮非複合的 AWUS036ACS（RTL8811AU，同為 1x1 ac，少了藍牙那層變數）。
- **要做 mesh / IBSS 實驗** → `rtw88` 不支援，改用 MediaTek 的 AWUS036ACM / ACHM。
- **追求最強接收或長距離 monitor** → 雙天線的 AWUS036ACH 或 Wi-Fi 6 的 AWUS036AXER 更合適。
- **避雷**：若用途是 injection / handshake，不要選 MT7921 的 AWUS036AXM / AXML，注入在本平台直接失敗。

想一次看完 9 款 ALFA 卡的 Monitor / Injection / AP / WPA3 橫向對照與完整選型矩陣，請回到總表：[2026 最完整實測：9 款 ALFA 無線網卡在 ASUS GX10 的全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 常見問題（FAQ）

**Q：AWUS036EACS 在 Ubuntu 24.04 ARM64 要裝驅動嗎？**
在本文測試的 kernel 6.17（ASUS GX10）上不用：RTL8821CU 由內建 rtw88_8821cu 驅動，插上即辨識，免編譯、免 DKMS；介面名稱為 wlx 加 MAC，重插後不變。

**Q：AWUS036EACS 的 monitor mode（監聽模式）與封包注入表現如何？**
monitor 在 2.4G、5G 都穩，多數頻道收滿 300 frames；`aireplay-ng --test` 兩頻皆 30/30（100%）。5G 注入前需 `iw reg set US` 解除 TW 對 TX 的限制。

**Q：AWUS036EACS 能擷取 WPA handshake（握手封包）嗎？**
能。自有 AP 加自有 iPhone 7 Plus 端到端實測：deauth 收到 79 ACKs，擷取完整 M1–M4，`hcxpcapngtool --all` 轉出 .22000（784 bytes、2 組 EAPOL pairs）。僅限自有或已授權網路。

**Q：AWUS036EACS 插上後 lsusb 看得到、卻沒有 wlx 網路介面怎麼辦？**
這是 BT+Wi-Fi 複合裝置的 probe 競態：藍牙已綁 btusb，Wi-Fi 的 rtw88_8821cu 卡住。實測重載模組、手動 bind 多半無效，可靠解法是拔卡後換另一個 USB 孔重插。

**Q：AWUS036EACS 支援 mesh、IBSS 或 hcxdumptool 嗎？**
不支援。rtw88 的 active-monitor、IBSS、mesh、P2P 回 -95 或 join 無效；hcxdumptool 8.x 僅在 2.4 GHz 可 arm（5 GHz 會 failed to arm），請改用 airodump-ng + aireplay-ng。VHT 僅 80 MHz。要 mesh / IBSS 請選 AWUS036ACM / ACHM。

---

## 6. 延伸閱讀

- [2026 最完整實測：9 款 ALFA 無線網卡在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP 全矩陣](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)（Hub 總表）
- [WPA3-SAE 時代的無線稽核：9 款 ALFA 卡 handshake 擷取能力實測](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [免裝驅動：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驅動啟用 ALFA 網卡 Monitor 與 AP 模式](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 同屬 rtw88 USB ac 卡 → [AWUS036ACS 單卡實測報告（RTL8811AU）](/zh-tw/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*測試單位：Yupitek（ALFA Network 台灣經銷）— https://www.yupitek.com*
