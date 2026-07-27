---
title: "ALFA AWUS036ACH 自製長距離無人機數位圖傳／遙測鏈路：wfb-ng 開源教學（2026）"
description: "用 ALFA AWUS036ACH 網卡＋開源 wfb-ng，打造低延遲、可加密的長距離無人機數位圖傳與 MAVLink 遙測鏈路。完整硬體清單、Raspberry Pi 設定教學、供電踩坑排錯全攻略。"
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "無人機圖傳", "數位圖傳", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "長距離圖傳", "遙測鏈路"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "wfb-ng 跟一般 WiFi 有什麼不同？"
    answer: "一般 WiFi 需要連線（association）與 ACK 確認，在長距離下效率差、延遲高。wfb-ng 改用 raw 封包注入，繞過 802.11 連線機制，直接用 FEC 前向糾錯抗丟包，端到端延遲可壓到數十毫秒等級。"
  - question: "為什麼機載端 ALFA 網卡需要獨立供電？"
    answer: "AWUS036ACH 在發射（TX）時瞬間耗電很大，直接插 Raspberry Pi 的 USB 2.0 埠會因供電不足導致網卡端口被 reset、鏈路斷線、封包損壞。建議用 5V BEC 獨立供電，並在 +5V 與 GND 間併聯 470µF 低 ESR 電容濾波。"
  - question: "連線後沒有影像也沒有遙測怎麼辦？"
    answer: "最常見的原因是金鑰不對應——檢查機載端的 drone.key 與地面站的 gs.key 是否為同一組。其次確認兩端的 wifi_channel 與 link_domain 設定完全一致。可用 journalctl -xu wifibroadcast@gs 查看即時日誌排錯。"
  - question: "wfb-ng 一定要用 ALFA AWUS036ACH 嗎？"
    answer: "任何 RTL8812AU 晶片網卡理論上都可用，但 AWUS036ACH 是 wfb-ng 專案官方實測的硬體，驅動支援最穩定。尤其在高功率、長距離場景下，ALFA 的功率設計與可拆式天線優勢明顯。"
---
> 作者：榆閤科技 Yupitek（ALFA Network 台灣授權代理商）技術團隊
> 適用對象：無人機同好、Maker、資安研究員、農噴／巡檢機開發者
> 難度：★★★☆☆（需基本 Linux 與飛控概念）

{{< tldr >}}
wfb-ng 是一套開源軟體，能把 **ALFA AWUS036ACH** 這類支援 monitor mode 的 WiFi 網卡「變成」無人機專用的長距離無線電，讓操作者自行架設低延遲、可加密的影像與 MAVLink 遙測傳輸鏈路。
{{< /tldr >}}

{{< alert "circle-info" >}}
**第一次看無人機技術文章？先搞懂這篇跟另一篇的差別**

我們部落格另有一篇《[ALFA AWUS036ACH × 樹莓派：標準 Remote ID 偵測套件](/zh-tw/blog/remote-id-detection-kit/)》，同樣用 ALFA AWUS036ACH，但用途完全相反：

- **本文（這篇）＝「發射端」**：教你把 ALFA 網卡裝在**自己的無人機**上，做出一條長距離、可加密的影像／遙測傳輸鏈路。適合你是**無人機操作者 / 開發者**。
- **另一篇＝「接收端」**：教你用 ALFA 網卡**被動接收**別人無人機廣播出來的身分資訊（如同看到無人機的車牌號碼），適合你是**場域安全管理者 / 監管單位**。

兩篇的共同點只有「同一張網卡、同一個 monitor mode 監聽模式技術」，實際應用情境完全不同，別搞混了。

不熟悉 monitor mode、封包注入等名詞的讀者，也可以先跳到文末的「新手必懂名詞表」附錄快速掃過一遍。
{{< /alert >}}

---

## 一、為什麼要用 ALFA 卡自製數位圖傳？

如果你玩過傳統類比 FPV（5.8GHz 類比圖傳），一定對那根「雪花天線」不陌生：訊號一被遮擋就滿屏雜訊，飛遠了就開始掉畫面，而且**任何人都拿一台接收機就能偷看你畫面**——既不加密、也沒有遙測回傳。

我們團隊最近一年幫不少農噴、巡檢、甚至資安教育訓練的客戶架設鏈路，發現一個很務實的需求：**能不能用一張常見的 ALFA USB 網卡，搭開源軟體，自己做出一套「數位化、可加密、同時傳影像＋遙測」的長距離鏈路？**

答案是可以，而且比你想的簡單。

對比傳統類比圖傳，用 ALFA 網卡跑開源 **wfb-ng** 做數位圖傳有幾個壓倒性優勢：

- **低延遲**：raw WiFi 注入模式繞過一般 802.11 的 ACK 與連線握手，端到端延遲可以壓到數十毫秒等級，FPV 手感接近類比。
- **數位加密**：影像與遙測封包走 libsodium 加密，別人拿接收機也解不開你的畫面與飛控資料。
- **一條鏈路多工**：同一張網卡、同一個頻點，可以**同時**傳：
  - 即時影像（RTP / RTSP）
  - MAVLink 遙測（雙向，飛控 ↔ 地面站）
  - 一條 TCP/IP 隧道（可拿來跑 VPN、SSH、檔案傳輸）
- **TX 分集（發射分集）**：多張網卡可做發射端分集，抗遮蔽、提升穩健性。
- **開源可客製**：主角 ALFA AWUS036ACH 搭配開源 wfb-ng，整套自製鏈路的成本遠低於市售數位圖傳（DJI O3 / Walksnail 等），且**全部開源、可客製**。

{{< alert "circle-info" >}}
小語：這篇文章不是要「取代」大疆原廠圖傳，而是給想要**自己掌握鏈路、做二類備援、或做客製化載荷**的同好一條務實的開源路徑。
{{< /alert >}}

---

## 二、這是什麼：wfb-ng 簡介

**wfb-ng**（Wireless Fibre / WiFi Broadcast – next generation）是一套開源的數位 FPV 與遙測專案，核心想法很聰明：

> 它不把 WiFi 當「網路」用，而是把 WiFi 當「無線電」用。

一般 802.11 為了當區域網路，會做連線（association）、ACK 確認、重傳——這些機制在長距離、移動、低訊號的場景下反而拖慢速度、吃掉距離。wfb-ng 則改用 **raw WiFi 注入（raw WiFi injection）**：

- 網卡進入 **monitor mode（監控模式）**，不跟任何人「連線」。
- 直接注入底層 WiFi 封包，**不需要 ACK、不重傳**（改用 FEC 前向糾錯來抗丟包）。
- 繞過一般 802.11 的距離與延遲限制，把傳輸距離與穩定性拉到硬體極限。

簡單說，它把一張常見的 USB 網卡，變成一對「數位無線電」，上面可以跑 RTP 影像、MAVLink 遙測、甚至一條 IP 隧道。

- 專案首頁（GitHub）：https://github.com/svpcom/wfb-ng.git
- 目前廣泛用於 PX4 / ArduPilot 生態的自製數位圖傳，社群活躍，也是烏克蘭自製無人機社群常用的開源鏈路方案。

---

## 三、主角介紹：ALFA AWUS036ACH

這套鏈路的「無線電」就是它——**ALFA AWUS036ACH**。

它用的是 **Realtek RTL8812AU** 晶片，支援 **802.11ac（WiFi 5）**、**2.4GHz / 5GHz 雙頻**、USB 3.0 Type-C 介面、可拆式天線（RP-SMA）。更重要的是：**wfb-ng 的官方實測硬體，就是在兩端都用 AWUS036ACH、跑 5GHz 模式**。換句話說，這張卡是被專案作者驗證過、驅動支援最穩定的型號。

為什麼選它？三個關鍵理由：

1. **功率夠**：ALFA 一貫的高功率設計，搭配外接高增益天線，長距離表現遠勝一般筆電內建網卡。
2. **監控模式 ＋ 注入支援**：RTL8812AU 在打過 patch 的驅動（見下文）下，穩定支援 monitor mode 與 raw 封包注入，這是 wfb-ng 運作的先決條件。
3. **通用耐用**：USB 介面，機載端、地面站端通用，不用為不同機器買不同網卡；單張網卡損壞時也只需更換該卡，維護容易。

{{< alert "triangle-exclamation" >}}
**注意**：wfb-ng 需要**打過 patch 的專用驅動**（如 `rtl88xxau_wfb`），一般 Linux 內建驅動無法進入 wfb-ng 需要的注入模式。安裝方式見下文「軟體清單」與「Step-by-step 設定」。
{{< /alert >}}

---

## 四、硬體清單（Hardware List）

整個鏈路分成**機載端（Drone）**與**地面站（Ground Station）**兩組。下面分開列出。

### 機載端（Drone）

| 項目 | 建議型號 / 說明 |
|---|---|
| 機載電腦 | Raspberry Pi 3B / 3B+ / Zero 2 W / 4（任選；若要跑 1080p 建議用 **Pi 4 或 Zero 2 W**） |
| 攝影機 | Raspberry Pi Camera（CSI 介面）或 Logitech C920（USB 介面） |
| WiFi 模組 | **ALFA AWUS036ACH**（或任何 RTL8812AU 晶片網卡） |
| 供電 | **5V BEC**（給網卡獨立供電，見下文「踩坑提醒」） |
| 濾波電容 | **470µF 低 ESR 電容**（併聯在網卡 +5V 與 GND 間） |
| 飛控 | Pixhawk 等（走 MAVLink 協定，經 UART 接機載電腦） |

### 地面站（Ground Station）

| 項目 | 建議型號 / 說明 |
|---|---|
| 電腦 | Linux 電腦（Ubuntu / Debian x86-64），或另一台 Raspberry Pi |
| WiFi 模組 | **ALFA AWUS036ACH** |
| 監看軟體 | 執行 **QGroundControl** 的機器（可與地面站電腦同一台） |

> 註：如果**只做接收端（RX）**，任何支援 monitor mode 的網卡都行，例如刷了 OpenWRT 的路由器也能拿來當地面接收。但官方實測與本文設定仍以 AWUS036ACH 為準。

---

## 五、軟體清單（Software List）

### 作業系統

- **Raspberry Pi OS** / **Debian** / **Ubuntu**（Linux kernel ≥ 4.x）

### 核心專案

- **wfb-ng**（svpcom/wfb-ng）：數位圖傳 / 遙測主程式
- **修補版驅動**：
  - RTL8812AU → `svpcom/rtl8812au`（branch **v5.2.20**，用 dkms 安裝）
  - RTL8812EU → `svpcom/rtl8812eu`
  - 驅動載入後網卡名稱會顯示為 `rtl88xxau_wfb`（或 `rtl8812eu`）

### 系統依賴套件

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### 加密

- **libsodium**：用 `wfb_keygen` 產生 `drone.key`（機載端）與 `gs.key`（地面站端）

### 地面站播放

- **QGroundControl**：地面站監控飛控狀態與遙測
- **GStreamer / RTSP**：接收並播放機載端串流的影像

---

## 六、GitHub 連結與 ALFA AWUS036ACH 規格小卡

### 官方連結

| 項目 | 連結 |
|---|---|
| wfb-ng 專案 | https://github.com/svpcom/wfb-ng.git |
| 修補版驅動（RTL8812AU） | https://github.com/svpcom/rtl8812au |
| 修補版驅動（RTL8812EU） | https://github.com/svpcom/rtl8812eu |
| ALFA AWUS036ACH 產品頁 | https://yupitek.com/zh-tw/products/alfa/awus036ach/ |
| PX4 WFB-ng 教學 | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### ALFA AWUS036ACH 規格小卡

| 規格 | 內容 |
|---|---|
| 晶片 | Realtek **RTL8812AU** |
| 無線標準 | 802.11a / b / g / n / **ac（WiFi 5）** |
| 頻段 | **2.4GHz ＋ 5GHz** 雙頻 |
| 介面 | USB 3.0 **Type-C** |
| 天線 | 2 × 可拆式 **RP-SMA**（2T2R MIMO） |
| 監控模式 | 支援 monitor mode ＋ 封包注入（需 wfb-ng patch 驅動） |
| wfb-ng 驅動 | `rtl88xxau_wfb`（svpcom/rtl8812au, v5.2.20） |
| 定位 | wfb-ng **官方實測卡**（兩端 5GHz 模式） |

---

## 七、Step-by-step 設定（核心章節）

下面分四段。最推薦的路徑是 **A（Raspberry Pi 快速起步）**，幾乎是燒錄即用的體驗；**B** 則適合想在 x86 Linux 桌面手動安裝地面站的人；**C / D** 是金鑰配對與設定檔重點，兩條路都會用到。

### A. Raspberry Pi 快速起步（最推薦）

wfb-ng 官方提供預先打包好的 Raspberry Pi 映像檔，機載端與地面站端各燒一張，開機就能用。

**1. 下載並燒錄映像檔**

到 wfb-ng 的 GitHub **Releases** 頁面，下載最新的 `*.img.gz`，解壓後燒錄到**兩張** SD 卡（機載、地面站各一張）。

```bash
# 解壓映像檔（範例，檔名依實際 Release 為準）
gunzip wfb-ng-*.img.gz
# 用 Raspberry Pi Imager 或 dd / balenaEtcher 燒錄到 SD 卡
```

**2. 插入網卡、開機、SSH 登入**

兩張卡都插上 ALFA AWUS036ACH，上電開機，透過 SSH 登入（預設 IP 與帳密如下）：

```bash
ssh pi@192.168.0.111
# 密碼：raspberry
```

**3. 啟用地面站（Ground Station）服務**

在**地面站那張 Pi** 上執行：

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. 啟用機載端（Drone）服務**

在**機載那張 Pi** 上執行：

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. 在地面站監看鏈路狀態**

```bash
wfb-cli gs
```

> 看到連線、頻道、丟包率等資訊就代表鏈路通了。接著打開 QGroundControl，就能看到遙測與影像。

---

### B. Debian / Ubuntu 地面站手動安裝

如果你是用 x86-64 的 Linux 桌機 / 筆電當地面站，可以手動安裝。

**1. 安裝 dkms 與修補版驅動**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. 確認網卡已被 wfb-ng 驅動接管**

```bash
# 應看到 wlan0，且 MTU 為 2312
ifconfig

# 驅動名稱應顯示 rtl88xxau_wfb（RTL8812AU）或 rtl8812eu（RTL8812EU）
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
如果 `ethtool -i wlan0` 顯示的是一般 `rtl8812au` 而非 `rtl88xxau_wfb`，代表 patch 驅動沒裝好，wfb-ng 會無法進入注入模式。請回頭檢查 dkms 安裝有無報錯。
{{< /alert >}}

**3. 執行官方自動安裝腳本**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. 監看鏈路**

```bash
wfb-cli gs
```

---

### C. 金鑰與配對

wfb-ng 的影像與遙測是加密的，機載端與地面站端必須用**對應的金鑰**才能通訊。

```bash
# 產生金鑰（在機載端產生，再分發）
wfb_keygen

# drone.key 放到機載端
# gs.key    放到地面站端
# 兩端必須對應，否則無法解密、鏈路顯示「已連線但無資料」
```

> 如果你是用 **B 段的自動安裝腳本（install_gs.sh）**，腳本會自動產生並配置金鑰，省去手動配對步驟。手動安裝則請務必確認 `drone.key` 與 `gs.key` 是同一組。

---

### D. 設定檔重點：/etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` 是 wfb-ng 的核心設定檔。以下是最常需要調整的幾個參數：

```ini
[common]
# 頻道 165 = 5825 MHz（5.8GHz 頻段）
wifi_channel = 165

# 國碼設為 'BO'（玻利維亞）可解鎖最大發射功率
wifi_region = 'BO'

[drone]
# 機載端與地面站的 link_domain 必須「完全一致」
link_domain = "my_wfb_link_01"

[drone_mavlink]
# 從飛控 UART 接收 MAVLink（需飛控端 UART 設為 1500000 baud）
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# 同上，兩端一致
link_domain = "my_wfb_link_01"
```

**三個最容易出錯的點：**

1. **`wifi_channel` 兩端要一致**：本文用 165（5825 MHz, 5.8GHz），機載與地面站都要設同一個。
2. **`link_domain` 兩端要一致**：這是鏈路的「識別碼」，不一樣就連不上。
3. **飛控 UART 鮑率要設 1500000**：`peer = 'serial:ttyS0:1500000'` 要求飛控那端的 UART 也設成 1500000 baud，否則 MAVLink 收不到。

{{< alert "triangle-exclamation" >}}
**注意**：`wifi_region = 'BO'` 是為了解鎖發射功率上限，但**這不代表你在當地可以合法這樣用**。請務必參考下方「法規提醒」。
{{< /alert >}}

---

## 八、實作注意事項 / 踩坑提醒

這一節是我們實作時真正踩過的坑，請務必看。

### ⚠️ 坑 1：網卡供電不足會 reset 端口、瘋狂掉包

AWUS036ACH 在**發射（TX）時瞬間耗電很大**。如果直接插在 Raspberry Pi 的一般 USB2 埠，Pi 的 USB 供電不足以撐住瞬間電流，結果是：**網卡端口被 reset、鏈路斷線、封包損壞、畫面卡死**。

解法（機載端一定要做）：

- 網卡**直接從 5V BEC 供電**（不要從 Pi 的 USB 取電），BEC 輸出接網卡。
- 在網卡的 **+5V 與 GND 之間併聯一顆 470µF 低 ESR 電容**做濾波，吸收 TX 瞬間的電流尖峰。
- 地面站端如果是**筆電的 USB3 埠、用原廠 USB3 線**，一般可以直接供電，不必額外 BEC。

> 這一步是「穩不穩」的關鍵。我們看過太多人卡在掉包，最後都是供電沒處理好。

### 坑 2：加密錯誤 / 連不上

如果 `wfb-cli gs` 顯示已連線但**沒有影像也沒有遙測**，多半是以下兩種：

- **金鑰不對應**：檢查機載的 `drone.key` 與地面的 `gs.key` 是否為同一組。
- **頻道或 link_domain 不一致**：兩端的 `wifi_channel` 與 `link_domain` 必須完全相同。

排錯指令：

```bash
# 看地面站服務的即時日誌，找加密 / 連線相關錯誤
journalctl -xu wifibroadcast@gs
```

### ⚠️ 坑 3：法規（非常重要）

這套鏈路會主動發射無線電波，屬於無線電設備使用行為。

- **使用前請確認你所在地區允許此種 WiFi 用途的發射功率與頻段。**
- 台灣、中國、歐美對 5.8GHz ISM 頻段的發射功率、可用頻點、以及「非連線式發射」各有規範。
- 本文 `wifi_region = 'BO'` 是為了解鎖硬體功率上限，但**不代表在當地合法**。請依你所在國家／地區的無線電管理法規調整頻道與功率，必要時降低發射功率或改合法頻點。
- 僅用於合法場域（如自有農地、閉場測試、教育訓練），勿干擾他人通訊。

---

## 九、結語

回頭看，我們用一張 ALFA AWUS036ACH，加上開源的 wfb-ng，就做出了一套：

- **成本優勢**：整套自製鏈路的材料費遠低於市售數位圖傳方案；
- **開源**：所有程式碼、驅動、設定都公開可查；
- **可客製**：頻道、功率、金鑰、MAVLink 對外方式全部自己掌控；
- **長距離**：數位圖傳 ＋ 遙測一條龍，5GHz 下實測距離遠超類比、且抗遮蔽、可加密。

對農噴、巡檢、資安教育訓練，或是純粹想搞懂「數位圖傳背後原理」的同好來說，這是一條非常值得動手走的路。

我們團隊會持續在部落格分享 ALFA 網卡在無人機鏈路上的實作筆記。如果你在架設過程遇到問題，歡迎留言交流——**動手做，才是最快的學習方式**。

---

{{< faq >}}

---

## 附錄：新手必懂名詞表（關鍵字白話文）

如果你是第一次接觸這類技術，以下用白話文快速說明本文常出現的名詞：

| 名詞 | 白話解釋 |
|---|---|
| **FPV**（First Person View） | 「第一人稱視角」，就是坐在無人機的「駕駛座」上看它飛，畫面即時從機上鏡頭傳回你眼前的螢幕或眼鏡。 |
| **數位圖傳 vs 類比圖傳** | 類比圖傳像老式電視訊號，訊號差就滿屏雜訊、可被任何人截收；數位圖傳把畫面轉成數位封包傳輸，可加密、抗雜訊能力較好，但硬體與設定較複雜。 |
| **monitor mode（監聽模式）** | 一般 WiFi 網卡只能「連上」路由器收發資料。monitor mode 讓網卡改成「什麼都不連、直接聽 / 發空氣中的無線電訊號」，是本文技術的地基。 |
| **packet injection（封包注入）** | 在 monitor mode 下，直接把自訂的無線電封包「射」到空氣中，不透過一般 WiFi 連線流程。wfb-ng 就是利用這個機制傳影像與遙測。 |
| **wfb-ng** | 一套開源軟體，把 WiFi 網卡「借屍還魂」變成無人機專用的無線電，而不是當一般網路用。本文的核心軟體。 |
| **FEC（前向糾錯，Forward Error Correction）** | 傳輸時故意多送一些「備份資訊」，就算部分封包在空中遺失，接收端也能用備份資訊補回原始畫面，不必要求重傳（重傳在長距離、高速移動場景會拖慢速度）。 |
| **MAVLink** | 無人機飛控（如 Pixhawk）與地面站溝通的「共同語言」協定，用來傳飛行狀態、下達飛行指令等遙測資料。 |
| **RTP / RTSP** | 網路上傳輸即時影像常用的協定，你的手機 IP CAM、監視器很多也是用這一類協定串流畫面。 |
| **libsodium 加密** | 本文用來加密影像與遙測資料的開源加密函式庫，確保只有配對好金鑰的機載端與地面站能解密畫面內容。 |
| **TX 分集（發射分集）** | 用多張網卡同時發射同一份資料，其中一張訊號被遮蔽時，另一張還能補上，類似「雙重保險」。 |
| **BEC（Battery Eliminator Circuit）** | 一種穩壓供電模組，把無人機電池的電壓降到網卡需要的 5V，且能承受網卡瞬間大電流需求，避免供電不穩導致斷線。 |
| **RTL8812AU** | ALFA AWUS036ACH 網卡內部使用的 Realtek 晶片型號，決定了這張卡支不支援 monitor mode 與封包注入。 |

> 一句話總結：wfb-ng 把 ALFA 網卡「偽裝」成無人機專屬的無線電台，讓畫面與飛控資料能用開源、可加密的方式長距離傳輸——這是你（操作者）主動架設的一條「自家專屬頻道」。

---

## 參考資源

- **wfb-ng 專案（svpcom/wfb-ng）**：https://github.com/svpcom/wfb-ng.git
- **ALFA AWUS036ACH 產品頁**：https://yupitek.com/zh-tw/products/alfa/awus036ach/
- **修補版驅動（RTL8812AU）**：https://github.com/svpcom/rtl8812au
- **修補版驅動（RTL8812EU）**：https://github.com/svpcom/rtl8812eu
- **PX4 WFB-ng 教學文件**：https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

## 延伸閱讀

- [ALFA AWUS036ACH × 樹莓派：標準 Remote ID 偵測套件完整技術指南](/zh-tw/blog/remote-id-detection-kit/) — 同一張網卡的「接收端」應用，教你被動偵測別人無人機的身分廣播
- [ALFA AWUS036ACH 產品頁](https://yupitek.com/zh-tw/products/alfa/awus036ach/) — 規格、選購與技術支援
- [ALFA Network 全系列產品](https://yupitek.com/zh-tw/products/alfa/) — 依晶片、頻段、用途挑選其他型號

---

*本文由榆閤科技 Yupitek（ALFA Network 台灣授權代理商）技術團隊撰寫，基於 wfb-ng 官方文件與實作經驗整理。實作前請務必確認所在地區無線電法規，並依規範調整發射功率與頻段。*
