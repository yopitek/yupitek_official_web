---
title: "ALFA AWUS036ACH × 樹莓派：標準 Remote ID 無人機偵測套件完整教學（2026）"
description: "用 ALFA AWUS036ACH ＋ 樹莓派打造合法被動式 Remote ID 無人機偵測套件，涵蓋 ASTM F3411 標準解析、硬體清單、Step-by-Step 設定，以及與 DJI OcuSync 的技術釐清。"
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "無人機偵測", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "為什麼 AWUS036ACH 是首選，而不是更新的 Wi-Fi 6/6E 網卡？"
    answer: "Remote ID 擷取需要穩定的監聽模式與原始封包注入，目前社群驅動最成熟的是 Realtek rtl88xxau 分支（RTL8812AU / RTL8814AU）。Wi-Fi 6/6E（MediaTek MT7921AUN、Realtek RTL8832BU）在主流滲透／監聽工具鏈中尚無對應注入驅動，會被忽略。AWUS036ACH 是經社群與本套件雙重驗證的選擇。"
  - question: "nRF52840 是必要的嗎？"
    answer: "若只需 Wi-Fi Remote ID（NAN / Beacon），不需要；AWUS036ACH 即可。若要同時擷取 Bluetooth 5 Long Range 廣播，則需要 nRF52840（燒錄 sniffer 韌體）。建議套件含此模組以達完整覆蓋。"
  - question: "這套件能解碼 DJI 無人機嗎？"
    answer: "能處理 DJI 的標準 Wi-Fi / BT Remote ID 廣播；但 DJI 私有 OcuSync 的 DroneID 不在標準協定內，ALFA 卡無法解碼，需另購 SDR（ANTSDR / HackRF）＋ Kismet 外掛。兩者可並行部署。"
  - question: "樹莓派用哪一代？"
    answer: "Raspberry Pi 4（2 GB+）最平衡；Pi 3B 已被 unix_rid_capture 原作者在測試中驗證可用；Pi 5 亦可（注意散熱與電源）。Pi 內建 Wi-Fi 因無法穩定進監聽模式，必須外接 AWUS036ACH。"
  - question: "被動接收合法嗎？"
    answer: "接收無人機公開廣播的 Remote ID 屬合法接收，等同讀取公開資訊；但主動干擾（jamming）受嚴格管制，不在此套件範圍。"
---
> 榆閤科技 Yupitek 技術團隊｜ALFA Network 台灣授權代理

{{< tldr >}}
Remote ID 偵測套件用 **ALFA AWUS036ACH** 網卡的監聽模式，被動接收無人機依法必須廣播的身分與位置資訊（等同無人機的「空中車牌」），是場域安全管理者合法、低成本的態勢感知手段。
{{< /tldr >}}

{{< alert "circle-info" >}}
**第一次看無人機技術文章？先搞懂這篇跟另一篇的差別**

我們部落格另有一篇《[自製長距離數位圖傳 / 遙測鏈路（基於 wfb-ng）](/zh-tw/blog/wfb-ng-long-range-link/)》，同樣用 ALFA AWUS036ACH，但用途完全相反：

- **本文（這篇）＝「接收端」**：教你用 ALFA 網卡**被動接收**別人無人機廣播出來的身分資訊（如同看到無人機的車牌號碼）。適合你是**場域安全管理者 / 監管單位**。
- **另一篇＝「發射端」**：教你把 ALFA 網卡裝在**自己的無人機**上，做出長距離、可加密的影像／遙測傳輸鏈路。適合你是**無人機操作者 / 開發者**。

兩篇的共同點只有「同一張網卡、同一個 monitor mode 監聽模式技術」，實際應用情境與立場完全不同，別搞混了。

不熟悉 Remote ID、SDR 等名詞的讀者，也可以先跳到文末的「新手必懂名詞表」附錄快速掃過一遍。
{{< /alert >}}

---

## 1. 為什麼需要 Remote ID 偵測套件

各國無人機監管已進入「廣播式身分識別」時代。依照標準，無人機必須在空中持續廣播自身資訊：

| 廣播欄位 | 說明 |
|---|---|
| UAS / 操作者 ID | 序號或註冊碼 |
| 即時位置（經緯度、高度） | WGS-84 / 氣壓高度 |
| 速度、航向 | 水平 / 垂直速度 |
| 操作者位置 | 起降點或即時位置 |

廣播透過兩類無線載波：

- **Bluetooth**：BT4 Legacy Advertising、BT5 Long Range（Extended Advertising）
- **Wi-Fi**：NAN（Wi-Fi Aware，2.4 / 5 GHz）、Beacon（2.4 / 5 GHz）

對機場、園區、監獄、大型活動等場域管理者而言，**被動接收這些公開廣播**（等同於看見無人機的「機尾編號」）是合規且低成本的態勢感知手段，無須主動干擾。

{{< alert "triangle-exclamation" >}}
**合法性提示**：本文所有做法均為**被動接收公開廣播**；主動干擾（jamming）受各國嚴格管制，不在本套件範圍內，也不建議導入。
{{< /alert >}}

---

## 2. 產品定位：技術風險最低的開源路徑

我們評估多條技術路徑後，選定以 **ALFA AWUS036ACH** 為核心的組合：

- ALFA AWUS036ACH 採用 **Realtek RTL8812AU**，雙頻 2.4 + 5 GHz（802.11ac）、2×2 MIMO，雙根可拆卸 5 dBi 高增益天線（RP-SMA），USB 3.0 頻寬充足。
- 社群維護的 `rtl88xxau` 驅動讓它能穩定進入**監聽模式（Monitor Mode）**並支援**原始封包注入（raw packet injection）**——這正是擷取 Wi-Fi RID Beacon / NAN 訊框的前提。
- 最重要的是：`sxjack/unix_rid_capture` 的 README **明載「Tested using an rtl8812au based WiFi dongle, an nRF52840 dongle and a Raspberry Pi 3B」**，等於社群已幫我們完成硬體驗證。直接複製其架構做產品化，技術風險最低。

---

## 3. 硬體清單

| 項目 | 型號 / 規格 | 角色 | 必要性 |
|---|---|---|---|
| **核心網卡** | ALFA **AWUS036ACH**（RTL8812AU，雙頻 2.4/5 GHz，USB 3.0，雙 5 dBi RP-SMA 天線） | Wi-Fi Remote ID 擷取（監聽模式） | **必要** |
| 單板電腦 | Raspberry Pi 4（建議 2 GB+；3B / 5 亦可） | 運算主機 | **必要** |
| 儲存 | microSD 16 GB+（Samsung / SanDisk Endurance 建議） | 系統碟 | **必要** |
| Bluetooth 5 擷取 | **nRF52840** USB Dongle（燒錄 sniffer 韌體，如 Nordic Sniffer） | 擷取 BT5 Long Range Remote ID | 推薦（可選） |
| 電源 | 5 V / 3 A USB-C（官方 Pi PSU） | 供電 | **必要** |
| 網路 | 乙太網路線 或 Wi-Fi 憑證 | 上傳 / 管理 | **必要** |
| 天線升級 | ALFA **APA-M25** 定向面板天線 | 拉長接收距離、抑制環境雜訊 | 選用 |

> 註：社群專案 `DroneAware` 原始清單指定 **AWUS036N（Ralink RT3070，2.4 GHz 單頻）**。本套件升級為 **AWUS036ACH（雙頻）**，可同時涵蓋 2.4 / 5 GHz 的 **NAN 與 Beacon** 兩種 Wi-Fi RID 傳輸方式，覆蓋更完整、未來擴充性更好。

---

## 4. 軟體清單

| 軟體 / 套件 | 用途 | 來源 |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | 作業系統（headless） | raspberrypi.com |
| **rtl88xxau 驅動** | RTL8812AU 監聽 / 注入驅動 | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`、`libbluetooth-dev`、`libncurses-dev` | `unix_rid_capture` 編譯依賴 | APT |
| **opendroneid-core-c** | Open Drone ID 訊息編解碼 C 函式庫（ASTM F3411 / EN 4709-002） | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Linux Wi-Fi / BT RID 擷取程式（JSON 輸出） | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node（選用） | 一鍵接入社群即時地圖 | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + ANTSDR 外掛（DJI 路徑） | 解碼 DJI OcuSync DroneID（需 SDR 硬體） | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) ＋ [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. GitHub 專案連結

```text
# 核心解碼庫（ASTM F3411 / EN 4709-002 訊息編解碼）
https://github.com/opendroneid/opendroneid-core-c

# Linux 擷取程式（本套件主程式，已驗證 rtl8812au + nRF52840 + RPi）
https://github.com/sxjack/unix_rid_capture

# 社群即時地圖網路（一鍵安裝，自動上傳 droneaware.io）
https://github.com/fduflyer/DroneAware-Node-Releases

# 無線偵測框架（DJI OcuSync 路徑需搭配 SDR 外掛）
https://github.com/kismetwireless/kismet

# RTL8812AU 監聽 / 注入驅動（AWUS036ACH 必裝）
https://github.com/morrownr/8812au-20210629
```

---

## 6. Step-by-Step 設定

### 步驟 1 — 燒錄系統

使用 **Raspberry Pi Imager** 寫入 **Raspberry Pi OS Lite (64-bit)**。點齒輪（進階設定）：

- 主機名：`droneid-kit`
- 開啟 SSH 並設定帳號密碼
- 填入 Wi-Fi 憑證（避免後續接乙太）

### 步驟 2 — 連接與硬體驗證

將 AWUS036ACH 直接插上 Pi 的 **USB 3.0** 埠（藍色 / 標 `SS`），確認雙天線鎖緊。啟動後 SSH 進入：

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

應見：

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### 步驟 3 — 安裝 rtl88xxau 監聽驅動

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### 步驟 4 — 驗證監聽模式

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

輸出應顯示 **`Mode:Monitor`**。

### 步驟 5 — 安裝編譯依賴

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### 步驟 6 — 編譯 opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# 產出 libopendroneid/libopendroneid.so 與 test/odidtest
```

### 步驟 7 — 編譯 unix_rid_capture

`unix_rid_capture` 需要 `opendroneid.c` / `opendroneid.h`，將其從上一步複製進來：

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### 步驟 8 — 執行擷取

需 root 權限或 `cap_net_raw`：

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # 擷取並存 JSON
```

即時 UDP 輸出（另開終端）：

```bash
nc -lu 32001
```

### 步驟 9 — 視覺化軌跡（GPX → Google Earth）

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # 產生 .gpx
```

用 Google Earth 開啟即可看到無人機飛行路徑。典型偵測 JSON 範例：

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### 步驟 10 —（選用）接入 DroneAware 社群即時地圖

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**安全提醒**：對任何 `curl ... | sudo bash` 第三方腳本，建議先下載審閱再執行：`curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`。安裝程式會自動偵測 USB 網卡、提示節點名稱並引導至 droneaware.io 註冊，偵測結果即時顯示於 live map。
{{< /alert >}}

---

## 7. 重要技術釐清：標準 RID vs DJI OcuSync

這是專業價值所在，請務必講清楚給客戶：

| 路徑 | 負責對象 | 硬體 | 能否用 ALFA AWUS036ACH |
|---|---|---|---|
| **標準 Remote ID** | ASTM F3411 Wi-Fi / BT 廣播 | AWUS036ACH + nRF52840 | ✅ 可以（本文主體） |
| **DJI OcuSync DroneID** | DJI 私有協定（非標準 Wi-Fi） | 完整 SDR（ANTSDR / HackRF / USRP）＋ Kismet `kismet_cap_antsdr_droneid` 外掛 | ❌ 不行 |

- ALFA AWUS036ACH 是 **Wi-Fi 頻段（2.4 / 5 / 6 GHz）接收器**，能完整處理標準 RID。
- DJI 私有 **OcuSync** 的 DroneID 不走標準 Wi-Fi 協定，**ALFA 卡無法解碼**；必須用覆蓋到 2.4 / 5.8 GHz 的 SDR（如 ANTSDR E200）配合 `alphafox02/antsdr_dji_droneid` + Kismet 外掛。
- ⚠️ 注意：**RTL-SDR 頻寬上限約 1.7 GHz**，看不到 2.4 / 5.8 GHz 的 OcuSync，必須選支援高頻的 SDR。
- 兩條路徑**互補**：ALFA 卡做標準 RID 廣播偵測，SDR 做 DJI 私有協定解碼，組成完整的 Counter-UAV / RF 態勢感知前端。

---

{{< faq >}}

---

## 附錄：新手必懂名詞表（關鍵字白話文）

如果你是第一次接觸無人機監管 / 反無人機（Counter-UAV）技術，以下用白話文快速說明本文常出現的名詞：

| 名詞 | 白話解釋 |
|---|---|
| **Remote ID（遠端識別）** | 無人機的「空中車牌」。法規要求無人機起飛後要一直對外廣播自己的身分、位置等資訊，讓地面上的人（尤其是監管單位）能知道「這是誰的機、飛去哪」。 |
| **ASTM F3411 / EN 4709-002** | 分別是美國、歐盟制定的 Remote ID 廣播標準規格，規定廣播的內容、格式該長什麼樣子，讓不同廠牌的無人機與偵測設備能互通。 |
| **被動偵測（Passive Detection）** | 只是「聽」廣播出來的公開訊息，不會主動發射訊號去干擾或攻擊無人機，合法性與主動干擾（jamming）完全不同。 |
| **monitor mode（監聽模式）** | 讓 WiFi 網卡不去連任何路由器，改成「單純聽」空氣中的無線電封包，是擷取 Remote ID 廣播的前提。 |
| **NAN（Wi-Fi Aware）／ Beacon** | 兩種無人機用來廣播 Remote ID 的 Wi-Fi 訊框格式，本套件會同時嘗試解析這兩種。 |
| **Bluetooth 5 Long Range** | 除了 Wi-Fi，部分無人機也會用藍牙廣播 Remote ID，需要額外的 nRF52840 才能擷取。 |
| **DJI OcuSync / DroneID** | DJI 自家的私有影像 / 遙測傳輸協定，**不是**標準 Wi-Fi，也不是本文能解的 Remote ID；需要完全不同的 SDR 硬體與外掛才能解讀，本文有特別在第 7 節說明。 |
| **SDR（Software Defined Radio，軟體定義無線電）** | 一種可以用軟體調整接收頻率範圍與解調方式的通用無線電硬體，像 ANTSDR、HackRF，能涵蓋 ALFA 網卡收不到的頻段（如 DJI OcuSync）。 |
| **RTL8812AU** | ALFA AWUS036ACH 網卡內部使用的 Realtek 晶片型號，決定了這張卡支不支援監聽模式。 |
| **GPX 檔案** | 一種記錄 GPS 座標軌跡的通用格式，可以直接用 Google Earth 等軟體開啟，畫出無人機飛過的路徑。 |

> 一句話總結：本文教你把 ALFA 網卡變成一台「無人機身分掃描器」——被動接收天上無人機依法必須廣播的公開資訊，屬於場域安全管理的合法手段。

---

## 參考來源

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — WiFi/BT RID capture（rtl8812au + nRF52840 + RPi 驗證）](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — 社群 Remote ID 偵測網路](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — 無線偵測框架](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — DJI OcuSync DroneID SDR 解碼](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — RTL8812AU Linux 監聽 / 注入驅動](https://github.com/morrownr/8812au-20210629)
7. [ALFA AWUS036ACH 產品頁（Yupitek）](https://yupitek.com/zh-tw/products/alfa/awus036ach/)
8. [Yupitek 聯絡與訂購](https://www.yupitek.com/zh-tw/contact/)

---

## 延伸閱讀

- [用 ALFA AWUS036ACH 自製長距離數位圖傳 / 遙測鏈路（wfb-ng）](/zh-tw/blog/wfb-ng-long-range-link/) — 同一張網卡的「發射端」應用，教你把它裝上自己的無人機做長距離圖傳
- [ALFA AWUS036ACH 產品頁](https://yupitek.com/zh-tw/products/alfa/awus036ach/) — 規格、選購與技術支援
- [ALFA Network 全系列產品](https://yupitek.com/zh-tw/products/alfa/) — 依晶片、頻段、用途挑選其他型號

---

*本文由榆閤科技 Yupitek 技術團隊整理。AWUS036ACH 與相關硬體均可經 Yupitek 取得授權代理與技術支援。*
