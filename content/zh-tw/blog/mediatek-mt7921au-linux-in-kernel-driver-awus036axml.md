---
title: "別再折騰驅動編譯！為什麼 MediaTek MT7921AU 是現代 Linux 與 Kali 開發者的首選？"
date: 2026-08-18
draft: false
slug: "mediatek-mt7921au-linux-in-kernel-driver-awus036axml"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "深入解析 MediaTek MT7921AU（AWUS036AXML）的 Linux 核心原生支援優勢，對比 Realtek RTL8812AU DKMS 編譯痛點，提供監聽模式與採購評估工作表。"
featureimage: "/images/blog/01_AWUS036AXML_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "AWUS036AXML 是否支援 macOS？"
    answer: "不支援。目前無適用於 Intel 或 Apple Silicon Mac 的 MT7921AU 驅動程式。"
  - question: "在 Linux 上使用需要手動編譯驅動嗎？"
    answer: "不需要。Linux Kernel 5.18+ 已原生內建 mt7921u 驅動，僅需確保安裝 linux-firmware 韌體套件。"
---

![ALFA AWUS036AXML MediaTek MT7921AU Linux In-Kernel Driver Blueprint](/images/blog/01_AWUS036AXML_blueprint.jpg)

> **對應產品**：ALFA AWUS036AXML（MediaTek MT7921AU / MT7921AUN）｜對照組：ALFA AWUS036ACH（Realtek RTL8812AU）
> **適用讀者**：Kali Linux 滲透測試、Linux 嵌入式開發、Raspberry Pi / 單板電腦使用者
> **文章目標**：在採購前先搞清楚「核心原生命中」與「DKMS 驅動編譯」的差別，降低事後的安裝與排障成本。

---

## 開場：那段「每次系統更新就要重編驅動」的日子

如果你用過 Realtek RTL8812AU 這類晶片的 USB 網卡（例如市售熱門的 AWUS036ACH），你可能也有過類似的經驗：

1. 裝好了社群維護的驅動，上網、監聽一切正常；
2. 某天執行 `sudo apt upgrade`，Linux 核心升級到新版本；
3. 重開機後網卡從系統消失，Wi-Fi 介面（`wlan0` / `wlan1`）完全不見；
4. 只好**重新下載原始碼、安裝 DKMS、重新編譯出核心模組**，折騰半小時到一小時。

問題不在產品本身，而在**驅動程式的存在形式**。Realtek 的 Linux 驅動大多沒有被收錄進 Linux 核心（mainline），必須靠外部原始碼「外掛」到系統裡。核心每升級一次，這份外掛就要重編一次，否則就會跟新的核心版本對不上而失效。

而今天的主角——採用 **MediaTek MT7921AU** 的 **ALFA AWUS036AXML** ——走的是完全不同的路：它的驅動**原生就活在 Linux 核心裡面**。

---

## 一、Linux 核心更新時，Realtek 驅動編譯失敗的常見痛點

先務實地拆解「RTL8812AU 需要 DKMS 編譯」這件事，讓你知道問題到底出在哪裡。

### 1.1 核心模組（Kernel Module）與核心版本綁死的本質

Linux 核心會把裝置驅動以「模組」的形式動態載入。關鍵在於：**模組是針對特定核心版本編譯的**。核心大版本更新（例如 6.8 → 6.9）之後，舊模組通常無法在新核心上載入，必須重新編譯。

### 1.2 DKMS：自動重編的救星與新坑

DKMS（Dynamic Kernel Module Support）就是為了解決「核心一更新模組就要重編」的痛點：它會在每次核心升級時，**自動幫你把驅動重新編譯一次**。聽起來很美好，但實務上仍會遇到：

- **工具鏈問題**：編譯需要 `build-essential`、`dkms`、原生核心標頭檔（`linux-headers-$(uname -r)`）。沒裝齊，DKMS 建置直接失敗。
- **版本不像容**：最高興的是有 DIY 能力的玩家，但你永遠不知道下次 `apt upgrade` 帶來的核心，是不是剛好踩到那份 GitHub 驅動沒有跟上的一處 API 變更。
- **Secure Boot / 核心模組簽署**：若系統啟用 Secure Boot，未簽署的核心模組會**被系統拒絕載入**，網卡介面連出現都不會出現。此時不能靠關閉安全防護解決，正確做法是透過 MOK（Machine Owner Key）機制匯入自簽憑證。這又是一道工序。
- **社群版本選擇焦慮**：同一個晶片在 GitHub 上有 `aircrack-ng/rtl8812au`、`morrownr/8812au-20210820` 等多個分支，版本不同、支援的核心範圍不同，選錯就白編一場。

### 1.3 你的時間成本才是真正的開銷

假設你只在「裝好那一次」要編譯，OK；但**只要系統持續更新，這份驅動就是永久的維護責任**。對滲透測試人員、嵌入式開發者來說，寶貴的時間不該花在重編網卡驅動上，而是花在工具與腳本開發。

---

## 二、MediaTek MT7921AU：為什麼它能「原生支援、隨插即用」

### 2.1 原生整合的底層架構：mt76 與 mt7921u

MediaTek 的 Wi-Fi 晶片驅動長期收錄在 Linux 核心的 **mt76** 無線驅動框架中。MT7921 系列包含 PCIe 版本與 USB 版本：

- MT7921 系列最早自 **Linux Kernel 5.12**（PCIe / M.2 版本）進入主線核心；
- 而 **AWUS036AXML 使用的是 USB 版本的 `mt7921u` 驅動，自 Linux Kernel 5.18** 起原生收錄於 mainline 核心。

換句話說，**驅動本體不用從 GitHub 抓原始碼，不用 DKMS，不用自己編譯**。只要你的發行版核心夠新，插上網卡、補上韌體檔，介面就乖乖出現在 `ip link` 裡。

### 2.2 你只需要韌體（Firmware），不需要驅動原始碼

這裡要釐清一個常見誤會：「不需要編譯驅動」不代表「完全不用安裝任何東西」。MT7921AU 需要的是**韌體檔（firmware）**，而不是驅動原始碼。韌體由發行版套件統一管理，通常一條指令搞定：

```bash
sudo apt update
sudo apt install linux-firmware firmware-misc-nonfree   # Debian / Kali 系列
sudo reboot
```

Ubuntu 慣用：

```bash
sudo apt update
sudo apt install linux-firmware
sudo reboot
```

韌體是「跟著發行版走」的套件，核心升級不會弄壞它——這正是與「DKMS 驅動」在維護成本上的根本差異。

### 2.3 原生與否：一張表格看懂核心版本需求

| 作業系統 / 發行版 | 最低核心需求 | 需要編譯驅動？ |
|---|---|---|
| Kali Linux（Rolling） | 6.x（內含 `mt7921u`） | 否，補韌體即可 |
| Debian 12 | 6.1 LTS | 否 |
| Ubuntu 22.04+ / 24.04 LTS | 5.18 以上（建議 HWE 核心） | 否 |
| Raspberry Pi OS（Bookworm） | 6.1 LTS | 否 |
| 舊型 Linux 發行版 | 5.18 以下 | 需額外部署，不建議 |
| Windows 10 / 11 | — | 原廠驅動 |
| **macOS（Intel / Apple Silicon）** | **不支援** | **無驅動，請勿採購** |

> **⚠️ 採購前最重要的支援性提醒**：AWUS036AXML **不支援 macOS**。無論 Intel 或 Apple Silicon，目前**皆無 MT7921AU 的 macOS 驅動**可用。若你的主力環境是 macOS，這類 Wi-Fi 6 / 6E 外接網卡對你而言就是壞的——請直接排除，別買了才發現。

### 2.4 為什麼「原生支援」對 Kali 開發者特別重要

在 Kali Linux 上，核心升級非常頻繁（Rolling 發行版）。RTL8812AU 使用者每次滾動更新都心驚膽跳；而 `mt7921u` 跟著核心一起被維護、一起被測試，**不存在「核心太新、驅動沒跟上」的窗口期**。加上它的產品定位就是為安全測試而生，監聽模式（Monitor Mode）與封包注入（Packet Injection）是開箱即用的標準功能。

---

## 三、AWUS036AXML 在 Kali Linux 上的隨插即用與監聽模式實測

### 3.1 插上、確認、開工：三步搞定

把網卡插上 USB-C 連接埠後（隨附 2-in-1 USB-C/USB-A 傳輸線），執行：

```bash
lsusb                 # 應看到 0e8d:7961 的 MediaTek 裝置
ip link               # 應出現 wlanX 介面
sudo apt install linux-firmware firmware-misc-nonfree
sudo reboot
```

重開機後確認介面：

```bash
iwconfig              # wlanX 應顯示為 Managed 模式
ip addr show wlanX    # 正常取得位址
```

就算要預設連線，一般發行版（含 Kali）的 NetworkManager 都能直接看到它——**不需要任何 GitHub 原始碼站台**。

### 3.2 切換監聽模式（Monitor Mode）

假設你的介面是 `wlan1`：

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iw dev wlan1 info     # 確認 type 顯示為 monitor
```

恭喜，`wlan1` 現在進入被動監聽 802.11 訊框的狀態，後續即可接上 Wireshark 或 aircrack-ng 套件繼續工作。

### 3.3 封包注入測試（Packet Injection）

```bash
sudo aireplay-ng --test wlan1
```

看到 `Injection is working!`（或等效輸出）即代表注入功能正常。此功能在原生 `mt7921u` 驅動上即為內建能力，無需額外 Hacks。

### 3.4 融合模式（VIF / Fusion）：同時管理＋監聽

許多滲透場景需要「網卡同時扮演用戶端上網、又同時監聽」，原生驅動透過 Virtual Interface 支援：

```bash
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

此時 `wlan1` 保持 managed（上網用），`mon0` 負責監聽。RTL8812AU 驅動要穩定做到這件事，通常得改一堆設定檔——原生驅動直接把這項能力送給你。

> **⚠️ 合法使用紅線**：監聽模式、封包注入、Evil Twin 等能力的測試對象，**僅限你擁有或有明確授權的網路環境**（自有實驗室、公司授權的測試網段）。任何未經授權的網路偵察或入侵行為都可能違反當地法律，請謹守法律界線，本文章僅作為學術與工程開發用途之技術說明。

---

## 四、採購前評估工作表：你該買「原生免編譯」還是「DKMS 網卡」？

為了降低採購後的支援成本，先做這份簡單的評估，再決定買 AWUS036AXML 還是 AWUS036ACH。

### 4.1 兩款網卡快速對照

| 評估項目 | AWUS036AXML（MT7921AU） | AWUS036ACH（RTL8812AU） |
|---|---|---|
| 無線規格 | Wi-Fi 6E 三頻（2.4/5/6 GHz） | AC1200 雙頻（2.4/5 GHz） |
| USB 介面 | USB-C（USB 3.2 Gen 1） | USB 3.0 Type-A |
| Linux 驅動 | `mt7921u` **原生於核心 5.18+** | 需 DKMS 外部編譯 |
| 安裝難度 | 補韌體即可 | 需工具鏈＋編譯＋（Secure Boot 下）簽署 |
| 核心升級影響 | 不受影響 | 每次升級需重新編譯 |
| 監聽模式 | 原生支援 | 支援 |
| 封包注入 | 原生支援 | 支援 |
| macOS | 不支援 | 不支援 |
| 適用對象 | 現代 Linux / Kali / 嵌入式 | 舊系統或需要 2.4/5GHz 場景 |

### 4.2 半分鐘決策清單

勾選越接近下方描述，**越適合直接選 AWUS036AXML**：

- [ ] 我的主力系統是 **Kali Linux / Ubuntu / Debian**，核心版本 5.18 以上。
- [ ] 我**只要插上就能用**，不想碰 `dkms`、`github clone`、編譯工具鏈。
- [ ] 我需要 `mt76` 體系的原生支援，且核心升級不影響網卡。
- [ ] 我需要 **6 GHz 頻段**（Wi-Fi 6E 路由器環境）。
- [ ] 主要用途：監聽、封包注入、Soft AP、融合模式（VIF）。
- [ ] 我會搭配隨附的 USB-C / USB-A 2-in-1 傳輸線接到筆電或單板電腦。

反之，若你**沒有 6 GHz 需求**、系統屬於舊版 5.18 以下核心、且你熟悉 DKMS 維護流程，AWUS036ACH 仍是有其定位的選擇——但請務必做好「每次核心更新都要重編」的心理準備。

---

## 五、結語

對現代 Linux 與 Kali 開發者來說，時間就是最大的成本。**MediaTek MT7921AU（AWUS036AXML）把「驅動維護」這個無止境的負擔從你身上拿掉了**：驅動長在核心裡，韌體一包搞定，監聽與注入開箱即用，核心怎麼滾動更新都不用怕。

採購前只要先確認兩件事：**系統核心 ≥ 5.18**、且 **不是 macOS**。其他交給原生驅動就好。

---

## 附錄：快速排障 Intake（給客服與使用者對照）

如果網卡插上後沒出現介面，依序檢查：

1. `lsusb` 是否有 `0e8d:7961`（MediaTek）裝置 → 沒有則換 USB 連接埠或供電。
2. `sudo apt install linux-firmware firmware-misc-nonfree` 後重開機 → 韌體未裝是頭號原因。
3. `ip link` 是否出現 `wlanX` → 沒有則確認核心版本 `uname -r` 是否 ≥ 5.18。
4. **先確認作業系統不是 macOS**——此產品無 macOS 驅動，此類需求請勿送修。
5. 若以上都正常仍無法監聽，確認是否誤用 managed 模式（`iw dev wlanX info` 檢查 type）。

> 免責聲明：本文所述驅動支援與核心版本，以 Linux mainline 與各大發行版官方套件為主；不同發行版打包與核心組態可能略有差異。本文不構成任何商用閉源平台或品牌的官方相容性承諾，所有功能測試請於合法授權環境中進行。
