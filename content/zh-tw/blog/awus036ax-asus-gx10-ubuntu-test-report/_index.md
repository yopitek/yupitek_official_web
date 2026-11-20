---
title: "ALFA AWUS036AX 逐卡實測：ASUS GX10 + Ubuntu 24.04 的 Wi-Fi 6 Monitor / Injection / AP 能力報告（Realtek RTL8832BU / rtw89_8852bu）"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX（Wi-Fi 6）在 Ubuntu 24.04 ARM64 實測：免裝驅動，Monitor、2.4G 注入 96%、5G AP VHT80、WPA3-SAE、端到端 handshake（.22000）通過；不支援 IBSS / mesh。平台 ASUS GX10、RTL8832BU。"
faq:
  - question: "AWUS036AX 在 Ubuntu 24.04 ARM64 要裝驅動嗎？lsusb 顯示 0bda:1a2b 怎麼辦？"
    answer: "在本文測試的 kernel 6.17（ASUS GX10）上不用：RTL8832BU 由內建 rtw89_8852bu 驅動，免編譯、免 DKMS。若 lsusb 顯示 0bda:1a2b（光碟模式），執行 sudo usb_modeswitch -v 0bda -p 1a2b -K 切成 WLAN。"
  - question: "AWUS036AX 支援 monitor mode 與封包注入嗎？"
    answer: "支援。2.4 GHz 注入 29/30（96%）；5 GHz 逐台指定 AP 測試回 Injection is working!；airodump-ng 跳頻 60 秒掃到 14 個 AP 與 4 個 client。不支援 active monitor、IBSS、mesh。"
  - question: "AWUS036AX 能擷取 WPA handshake？MT7921 的 AXM / AXML 行嗎？"
    answer: "AX 能：自有 AP 加自有 iPhone 7 Plus，aireplay-ng -0 觸發重連、airodump-ng 擷取完整 M1–M4，hcxpcapngtool 轉出 .22000。MT7921 的 AXM / AXML 在本平台注入失敗，做不到。僅限自有或已授權網路。"
  - question: "AWUS036AX 可以當 AP 熱點嗎？支援 WPA3 嗎？"
    answer: "可以。hostapd 開 2.4G（802.11n）與 5G（VHT 80 MHz）AP，iPhone 7 Plus 連入顯示 VHT-NSS2 80 MHz；WPA3-SAE（ieee80211w=2、sae_pwe=0）以 iPhone 15 Pro 在 2.4 GHz 連入，MFP: yes（5 GHz 的 WPA3 未實測）。"
  - question: "AWUS036AX 和 AWUS036AXER 差在哪？該選哪張？"
    answer: "兩者同為 RTL8832BU + rtw89_8852bu，能力矩陣一致，差在天線與接收：AXER 外接天線，同批測試跳頻掃到 63 AP + 12 client（AX 為 14 AP + 4 client）。桌面固定選 AX，要長距離或最強接收選 AXER。"
draft: false
---

**重點摘要（TL;DR）**：Yupitek（ALFA Network 台灣經銷）實測，AWUS036AX 在 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）免裝驅動，雙頻 monitor 可用；2.4G 注入 96%、5G AP VHT80，端到端 .22000 通過，不支援 IBSS / mesh。

> 本文為 Yupitek 於**自有設備、自有辦公室 Wi-Fi（SSID `YUPITEK`）、自有測試手機**上完成的產品相容性與能力實測，對象為 ALFA **AWUS036AX**（Realtek RTL8832BU、Wi-Fi 6 2x2）。
> 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`；對照裝置 Apple iPhone 7 Plus（WPA3 與 VIF 另測 iPhone 15 Pro）。
> ⚠️ **合法使用**：Monitor 與 Injection 僅限自己擁有或已取得授權的網路；AP 模式請遵守當地無線電法規。本文不涉及任何針對第三方網路的攻擊操作。

---

## 1. 這張卡與測試平台

AWUS036AX 是 ALFA 這一代的 Wi-Fi 6 USB 網卡，採 Realtek RTL8832BU 晶片、2x2 雙空間串流，支援 2.4 GHz 與 5 GHz 雙頻。在 ALFA 的產品線裡，它和外接天線版的 AWUS036AXER 共用同一顆晶片與同一支驅動，差別在天線形式與接收增益；跟同屬 Wi-Fi 6 的 MediaTek 款 AWUS036AXM / AXML 則是完全不同的晶片路線，實測結論也差很多（第 5 節會交代）。

這次測試不談規格書上的理論速率，只回答經銷與工程現場最在意的三件事：在新版 Linux 上好不好裝？哪些無線能力真的能用？哪些是驅動天生做不到、不該白花時間的？結論要能複現，所以所有指令都在 2026-11-18 當天於 GX10 實機逐條跑過，下文的「實測輸出」都是真實節錄（MAC 位址以 `xx` 遮蔽）。

測試邊界先說清楚：全程在自家辦公室、對自有的 `YUPITEK` 網路與自有手機進行。Monitor 只收自己環境的封包，Injection 與 handshake 只對自家 AP 與自家 iPhone 操作。目的是驗證「這張卡在這台機器上能做到什麼」，不是示範攻擊第三方網路。

---

## 2. 硬體與驅動（Wi-Fi 6，免裝）

這代最實際的好處是：**插上即認、免編譯、免 DKMS**。RTL8832BU 的 `rtw89_8852bu` 驅動已經是 kernel 6.17 的 in-kernel 模組，GX10 開機就綁好，不必再去 GitHub 抓 out-of-tree 專案手動編。

晶片資訊與驗證步驟如下。先用 `lsusb` 確認卡以 WLAN 模式列舉：

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

預期會看到 `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`。本測試單位的這張卡直接以 WLAN 模式現身，沒有卡在光碟（CD-ROM）模式；若你拿到的卡顯示 `0bda:1a2b`，代表它還在光碟模式，用 `sudo usb_modeswitch -v 0bda -p 1a2b -K` 切成 WLAN 即可。

接著確認驅動與韌體載入：

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

實機載入的是 `rtw89/rtw8852b_fw-1.bin`，firmware version `0.29.29.5`。驅動與韌體都隨 kernel 內建，不需要另外安裝套件。

最後一步是先看清楚這顆驅動**宣告支援哪些介面模式**，這一步會直接決定後面哪些能力有、哪些是 N/A：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

實機列出的是 `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`。清單裡看不到 IBSS、mesh point 和 active-monitor。這不是設定沒調對，而是 `rtw89_8852bu` 本來就沒做這三個模式，第 4 節會據此標成 N/A。

---

## 3. 實測能力：Monitor / Injection / AP / WPA3

先給一張能力總表，每一格都對應下面的實測節錄：

| 能力 | 2.4 GHz | 5 GHz | 實測節錄 |
|---|---|---|---|
| **Monitor** | ✅ 強 | ✅ 強 | airodump 跳頻 60 秒掃到 **14 AP + 4 client** |
| **Injection** | ✅ **96%** | ✅ 可用 | 2.4G `aireplay-ng --test` 29/30（96%）；5G 逐台 `Injection is working!` |
| **AP 熱點** | ✅ 802.11n（HT） | ✅ **VHT 80 MHz** | iPhone 7 Plus 連入：2.4G MCS 12、5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | 未實測 | iPhone 15 Pro 連入，MFP: yes（`sae_pwe=0`）；僅在 2.4 GHz 實測 |
| **WPA handshake 擷取** | ✅ **端到端** | — | deauth 自有 iPhone → 擷取完整 4-way → 轉 hashcat `.22000` |

**Monitor（監聽模式／接收）✅ 強。** 切到 monitor 後，2.4 GHz 與 5 GHz 都收得到大量封包（各約 100 封/6 秒）。用 `airodump-ng --band abg` 跳頻掃 60 秒，實測找到 14 個 AP 加 4 個 client，接收表現和 ALFA Wi-Fi 5 的 ACM / ACHM 同級，遠勝 MediaTek MT7921 那兩張（AXM / AXML 實測接收偏弱）。對現場勘查、通道佔用盤點這類工作，這張卡的接收夠用。

**Injection（封包注入）✅ 可用，這也是 AX 對上 MediaTek 款的關鍵差異。** 2.4 GHz（ch6）跑 `aireplay-ng --test`，實測 `29/30: 96%`、`Injection is working!`，回應率 96%。5 GHz（ch36）對廣播測試可能回 `Found 0 APs`（現代 AP 不回廣播 probe，屬正常），但逐台指定 AP BSSID 測就會回 `Injection is working!`，確認 5 GHz 注入可用。相對地，同樣是 Wi-Fi 6 的 MediaTek AXM / AXML 在本平台**注入直接失敗**（主因是 kernel 6.16 以後的 mac80211 chanctx 回歸，另有韌體把注入速率鎖在 1／6 Mbps，並非晶片本身的限制），這點在選型時務必分清楚。

**AP 熱點 ✅ 雙頻可開，5 GHz 上得了 VHT80。** 用 hostapd 起 AP，2.4 GHz 開 802.11n（`ieee80211n=1`、HT20），iPhone 7 Plus 連入後顯示 MCS 12、authorized；5 GHz 開 VHT 80 MHz（`vht_oper_chwidth=1`、`ht_capab=[HT40+]`），iPhone 7 Plus 連入後顯示 VHT-NSS2 80 MHz、authorized。兩頻都能穩定帶起用戶端，80 MHz 頻寬也確實協商成功。

**WPA3-SAE ✅（2.4 GHz；5 GHz 未實測）。** 把 AP 的 `wpa_key_mgmt` 改成 `SAE`、`ieee80211w=2`，實測 iPhone 15 Pro 連入，MFP（Management Frame Protection）顯示 yes。這裡有個相容性細節：`sae_pwe` 要設 `0`（Hunting-and-Pecking），舊款 iPhone 才連得上。

**WPA handshake 擷取 ✅ 端到端成功。** 在自家 `YUPITEK` 網路、對自有 iPhone 7 Plus 走完整流程：monitor 側錄該通道 → `aireplay-ng -0` 送 deauth 觸發重連 → `airodump-ng` 擷取到完整四次握手（M1/M2/M3/M4）→ 用 `hcxpcapngtool` 轉出 hashcat 的 `.22000` 格式。因為這張卡注入可用，整條鏈路才跑得通；注入失敗的卡（如 AXM / AXML）到 deauth 這步就斷了。這條握手（handshake）擷取鏈用到的 Kali 常用工具（aircrack-ng、hcxtools）都直接在 Ubuntu 24.04 ARM64 上執行。

---

## 4. 進階與限制（rtw89 驅動的 N/A 項）

這一節把「能做的進階功能」與「驅動天生做不到的」一次講白，避免現場白花時間。

| 功能 | 狀態 | 說明 |
|---|---|---|
| **VIF（STA + AP 並行）** | ✅ | 主介面連 `YUPITEK`，同時開 AP VIF（ch36 VHT80），兩介面並行；STA 端 ping 3.2 ms |
| **WPA handshake 擷取** | ✅ 端到端 | 擷取 M1–M4，`hcxpcapngtool` 轉出 `.22000` |
| **Active monitor** | **N/A** | `rtw89_8852bu` 不具此模式（不在 `iw phy` 的 supported modes） |
| **Ad-hoc（IBSS）** | **N/A** | 驅動不支援 |
| **Mesh（802.11s）** | **N/A** | 驅動不支援 |
| **Wi-Fi Direct（P2P）** | ⬜ 未測 | 驅動宣告支援，但需第二台設備，本次略過 |

**VIF ✅。** 建一個 AP 虛擬介面（不同 MAC、unmanage），主介面保持連 Wi-Fi，同通道開 AP。實測主介面連 `YUPITEK` 的同時，AP VIF 在 ch36 跑 VHT80，兩個介面並行運作，STA 端 ping 3.2 ms。對「一邊連上網、一邊開測試熱點」的場景可行。

**Active monitor / IBSS / Mesh 是 N/A，不是壞掉。** 這三個模式沒有出現在第 2 節 `iw phy info` 的 supported interface modes 裡，代表 `rtw89_8852bu` 這支驅動根本沒實作。`sudo iw dev $IF set type ibss` 之類的指令會直接失敗，而且沒有解法：這不是參數或韌體能救的，要用到這三個模式就得換晶片路線（例如 MediaTek mt76 的 ACM / ACHM 在單機下可建 IBSS / mesh）。

**一個平台層級的限制要先知道：hcxdumptool 在 GX10 上 `failed to arm`。** 這不是 AX 專屬問題。`hcxdumptool 8.x` 需要 active-monitor，而 GX10 內建三頻網卡，USB 卡列舉時容易被 `-I` 誤映射到內建 phy，所有受測 USB 卡在這台機器上都會 arm 失敗（唯一例外是 AWUS036EACS 在 2.4 GHz）。實務做法是**改用 aircrack-ng 套件**（airodump-ng + aireplay-ng）跑擷取，本卡注入可用，整條鏈路照樣端到端走完（見第 3 節）。

**安全守則（GX10 平台共通）：** 絕對不要跑 `airmon-ng check kill`，它會關掉 NetworkManager 讓 GX10 對外斷線；操作時只動 `wlx*` 介面，不要碰內建的對外上網主線網卡。

---

## 5. 適用情境與選型（Wi-Fi 6 AP 熱點，連回 Hub）

把實測結論換成選型建議：**AWUS036AX 的甜蜜點是「Wi-Fi 6 + AP 熱點」且同時需要注入能力的場景。**

| 用途 | AWUS036AX 適合度 | 說明 |
|---|---|---|
| Wi-Fi 6 AP 熱點 / 邊緣接取 | ★ 首選 | 2x2 VHT80 雙頻可開，WPA3-SAE 可用 |
| Injection + handshake 稽核 | ★ 可勝任 | 2.4G 96%、5G 可用、端到端擷取成功 |
| 最強接收 / 長距離 monitor | ○ 夠用，但首選 AXER | 同晶片的 AXER 外接天線、接收更強 |
| mesh / IBSS 實驗 | ✗ 不適用 | 驅動 N/A，改選 mt76 的 ACM / ACHM |

**典型部署：當成 Wi-Fi 6 熱點，讓邊緣裝置連回中央 Hub。** 用實測過的 AP（VHT80）與 VIF 能力，把 GX10 搭這張卡佈成一個 Wi-Fi 6 接取點，測試手機、IoT 感測器這類邊緣裝置連上後，流量再經主介面回到中央 Hub（gateway）。VIF 實測已證明「主介面連回上層網路」和「對下開 AP」能並行，STA 端延遲 3.2 ms，這個拓撲在本平台驗證過可行。邊緣接取段要再上現代加密，加 WPA3-SAE 即可。

**選型避雷：要注入 / handshake 用途，別挑 AWUS036AXM / AXML。** 這兩張雖然同為 Wi-Fi 6 2x2、AP 也開得起來，但 MediaTek MT7921 在本平台**注入失敗**，無法 deauth、擷取不到 handshake。若客戶只是要一張單純的 Wi-Fi 6 AP / 一般連線卡、完全不碰注入，MediaTek 款穩定也無妨；但只要用途沾到無線稽核，就該選 Realtek 的 AX（或外接天線的 AXER）。

**和同晶片的 AXER 怎麼分？** 兩者晶片、驅動、能力矩陣一致；AXER 是外接天線版，接收與長距離 monitor 更強（同批測試中 AXER 跳頻掃到 63 AP + 12 client）。桌面固定、天線需求不高就選 AX；要拉距離、要最強接收就上 AXER。

---

## 常見問題（FAQ）

**Q：AWUS036AX 在 Ubuntu 24.04 ARM64 要裝驅動嗎？lsusb 顯示 0bda:1a2b 怎麼辦？**
在本文測試的 kernel 6.17（ASUS GX10）上不用：RTL8832BU 由內建 rtw89_8852bu 驅動，免編譯、免 DKMS。若 lsusb 顯示 `0bda:1a2b`（光碟模式），執行 `sudo usb_modeswitch -v 0bda -p 1a2b -K` 切成 WLAN。

**Q：AWUS036AX 支援 monitor mode（監聽模式）與封包注入嗎？**
支援。2.4 GHz 注入 29/30（96%）；5 GHz 逐台指定 AP 測試回 `Injection is working!`；airodump-ng 跳頻 60 秒掃到 14 個 AP 與 4 個 client。不支援 active monitor、IBSS、mesh。

**Q：AWUS036AX 能擷取 WPA handshake（握手封包）？MT7921 的 AXM / AXML 行嗎？**
AX 能：自有 AP 加自有 iPhone 7 Plus，`aireplay-ng -0` 觸發重連、`airodump-ng` 擷取完整 M1–M4，`hcxpcapngtool` 轉出 .22000。MT7921 的 AXM / AXML 在本平台注入失敗，做不到。僅限自有或已授權網路。

**Q：AWUS036AX 可以當 AP 熱點嗎？支援 WPA3 嗎？**
可以。`hostapd` 開 2.4G（802.11n）與 5G（VHT 80 MHz）AP，iPhone 7 Plus 連入顯示 VHT-NSS2 80 MHz；WPA3-SAE（ieee80211w=2、sae_pwe=0）以 iPhone 15 Pro 在 2.4 GHz 連入，MFP: yes（5 GHz 的 WPA3 未實測）。

**Q：AWUS036AX 和 AWUS036AXER 差在哪？該選哪張？**
兩者同為 RTL8832BU + rtw89_8852bu，能力矩陣一致，差在天線與接收：AXER 外接天線，同批測試跳頻掃到 63 AP + 12 client（AX 為 14 AP + 4 client）。桌面固定選 AX，要長距離或最強接收選 AXER。

---

## 6. 延伸閱讀

- 〈9 款 ALFA 無線網卡 ASUS GX10 + Ubuntu ARM64 能力總表〉—— 全型號 Monitor / Injection / AP / handshake 一次對照 → [總表 Hub](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [免裝驅動：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驅動啟用 Monitor 與 AP](/zh-tw/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)——rtw88 / rtw89 / mt76 共通設定流程
- [AWUS036AXER 逐卡實測](/zh-tw/blog/awus036axer-asus-gx10-ubuntu-test-report/)——同晶片外接天線版，接收與長距離 monitor 對比
- [WPA3-SAE handshake 擷取能力實測與 sae_pwe 相容性](/zh-tw/blog/alfa-wpa3-sae-handshake-capability-arm64/)——iPhone 連線的 `sae_pwe` 雷區

---

*測試單位：Yupitek（ALFA 經銷）— https://www.yupitek.com ｜ 測試環境：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 ｜ 對照裝置：Apple iPhone 7 Plus（WPA3 / VIF 另測 iPhone 15 Pro）*
