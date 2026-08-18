---
title: "ROS 2 Humble 機器人斷網與延遲排障：利用高功率外接網卡突破金屬屏蔽限制"
date: 2026-08-18
draft: false
slug: "ros2-humble-robot-wifi-signal-optimization-awus036axml"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "剖析移動機器人金屬與碳纖維外殼的法拉第籠效應，示範如何以 AWUS036AXML 外接天線改善 DDS 節點同步，並提供完整排障檢測流程。"
featureimage: "/images/blog/02_ros2_robot_rf_coverage.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "碳纖維外殼是否也會屏蔽 Wi-Fi 訊號？"
    answer: "是的。導電碳纖維具有導體特性，會造成顯著的射頻信號衰減，建議將天線外置。"
---

![ROS 2 Humble Robot Wireless Optimization Blueprint](/images/blog/02_ros2_robot_rf_coverage.jpg)

> **適用平台**：Ubuntu 22.04 / 24.04 上的 ROS 2 Humble 開源機器人開發平台（AMR、人形、四足等）
> **引導硬體**：ALFA AWUS036AXML（MediaTek MT7921AU 晶片，原生核心支援）
> **本篇定位**：本方案為開源學術平台 bench-test 評估，非商用成品之官方支援。

---

## 前言：你的機器人是不是「一進車間就失聯」？

做過機器人開發的朋友應該都有這種經驗：實驗室裡一切正常，一旦把 AMR（自走式機器人）開進金屬貨架、鋁製測試倉、或裝了碳纖維外罩的場域，畫面變成「節點時好時壞」、「指令延遲幾百毫秒」、「rviz2 地圖一閃一閃」，嚴重的直接斷線必須重啟 agent。

這篇文章要用**物理層 → 中介軟體層 → 設定層**三個角度，陪你一步步把這個「斷網與延遲」問題拆乾淨，並示範如何用**外接高增益天線的 USB 網卡（AWUS036AXML）**突破金屬外殼屏蔽，讓 ROS 2 的 DDS 即時節點同步恢復穩定。

如果你是第一次處理這類問題，強烈建議先跑過最後一章的「排障工作表」，再決定要不要動硬體。

---

## 1. 為什麼機器人一裝殼就斷線？金屬與碳纖維的「法拉第籠效應」

### 1.1 法拉第籠（Faraday Cage）原理

法拉第籠是一個導電外殼，外部的電磁波會在導體表面產生感應電流，使內部電場被削弱乃至隔離。機器人外殼只要是**連續的金屬導體**（鋁合金、鋼板、鋅合金）或**導電性碳纖維**，就會形成接近封閉的屏蔽體。

關鍵點：
- **屏蔽效果取決於連續性**：縫隙、開孔、橡膠墊圈、接縫都會漏波，所以你的機器人有時還收得到，只是訊號被大幅衰減。
- **衰減量很可觀**：單層金屬殼在 2.4GHz 下動輒衰減 -20dB 到 -40dB，5GHz 更嚴重（頻率越高，穿透越難）。
- **內建天線的位置最吃虧**：主控板上的 PCB 天線或小型陶瓷天線通常貼在機殼內側，天線本體就在「籠子裡」，訊號要先穿過金屬殼再跟外界通訊——《不是干擾問題，是物理上出不來》。

### 1.2 碳纖維的誤解

很多人以為碳纖維是「複合材料所以不擋訊號」，這其實是錯的。**導電碳纖維（含碳布、碳板材）本質上依然是導體**，對無線訊號同樣有屏蔽效果，只是因為不是完美連續導體，衰減比鋁合金略輕，但仍足以讓內建 Wi-Fi 天線收不到穩定的封包。

### 1.3 常見的「假排障」方向

遇到場域斷線，很多團隊第一個反應是：
1. 一直重啟 agent 或改 ROS 2 的 QoS 參數 → **治標不治本**，訊號弱時重啟也沒用。
2. 換一台貴的內建網卡主機板 → **換湯不換藥**，只要天線還在殼內，問題就還在。
3. 把 AP（無線基地台）功率調到最大 → **效果有限**，鏈路的雙向性（uplink/downlink）同受屏蔽影響。

正確的第一步，是**把天線物理上移出屏蔽殼**。這正是外接網卡的價值所在。

---

## 2. 外接雙 RP-SMA 5dBi 高增益天線，為何能改善 DDS 即時同步？

### 2.1 先認識 ROS 2 的 DDS

ROS 2 底層中介軟體採用 **DDS（Data Distribution Service）** 標準，Humble 預設的 RMW（ROS Middleware）實現是 **FastDDS**，也可切換到 **CycloneDDS**。DDS 做三件事：

1. **Discovery（探索）**：節點透過 RTPS discovery 協定互相找到對方（以 UDP multicast 發送）。
2. **Pub/Sub 資料流**：發佈者（publisher）把資料拆成 RTPS 封包送給訂閱者（subscriber）。
3. **可靠度管理**：QoS 決定資料是「盡力送（BEST_EFFORT）」還是「可靠送達（RELIABLE）」，以及心跳（Heartbeat）、ACK 等流量。

> **白話文**：ROS 2 的每一個 topic、service、action，背後都是一堆**即時 UDP 封包**。這些封包對網路品質（延遲、掉包、抖動）極度敏感。

### 2.2 訊號弱時，DDS 會發生什麼事？

| 網路症狀 | DDS 層的具體影響 |
|---|---|
| RSSI 低（-75dBm 以下） | Discovery 封包遺失 → 節點互相找不到，`ros2 node list` 時有時無 |
| 封包掉包 | RELIABLE 的 topic 不斷重傳（Heartbeat/ACK 迴圈）→ 延遲暴增、CB 回呼堆積 |
| 抖動（Jitter） | `sensor_msgs`（LaserScan、PointCloud2、影像）時間戳錯亂 → 定位與導航抖動 |
| 瞬間斷線 | 整個 agent 的 node 全部失聯 → 需要重啟，韌性（resilience）歸零 |

關鍵理解：**DDS 的 discovery 與 reliability 機制建立在「幾百 ms 內就要來回的即時封包」之上**。Wi-Fi 不是有線網路，它會重送、會退避（backoff），一旦訊號在 -70dBm 以下且伴隨金屬屏蔽，節點同步就像在暴風雨中對講機——不是不能用，是不可靠。

### 2.3 為什麼「外接天線」是解方：把天線擺出籠子外

AWUS036AXML 的設計剛好打中這個痛點：

- **雙 RP-SMA 母座 + 隨附雙 5dBi 外接全向天線**：你可以在機器人外殼鑽孔或利用現有孔位，把天線裝在**機殼外側**，讓輻射面朝外。這是「實體上把天線移出法拉第籠」最直接的作法。
- **5dBi 增益**：高於筆電內建 PCB 天線（通常僅 1–2dBi），在干擾場域中有效提升了有效輻射功率（EIRP）與接收靈敏度。
- **可更換/可升級**：萬一全向天線還不夠，可換成高增益定向天線（例如 9dBi 平板天線）指向場域中的 AP，做**定向長距離**部署。

> **實務小提醒**：外接天線自己也要注意「天線本體 + 同軸線」不貼緊金屬機殼，否則等效於又把天線裝回籠子裡。出線孔如果很小，別忘了用橡膠套圈避免同軸線被銳角割傷。

### 2.4 你要怎麼驗證「改善有效」？

在改硬體前後，各做一次 30 秒的量測，留下數字證據：

```bash
# 在機器人上（ROS 2 端）觀察無線訊號品質
iw dev wlan0 link                 # 看 RSSI
watch -n1 "iw dev wlan0 link | grep -E 'signal|tx bitrate'"

# 或用更簡潔的方式看訊號強度等級(每隔1秒印出)
while true; do
  iw dev wlan0 link | grep signal; sleep 1
done
```

建議記錄三組數據：
1. 實驗室（無屏蔽、近距離）— 基準值
2. 金屬倉內、內建天線 （改造前）
3. 金屬倉內、外接天線（改造後）

如果改造後 RSSI 從 -78dBm 回到 -58dBm 以上，又輔以下面的 DDS 壓力測試，你就有客觀證據證明「不是心理作用」。

---

## 3. ROS 2 環境下的網路最佳化：DDS 設定與頻段鎖定

> 先講結論：**硬體把天線移出殼外**解決的是「訊號強度」；**軟體設定**解決的是「把有限的訊號用好」。兩者要一起做。

### 3.1 切換到 CycloneDDS 並設定組態檔

Humble 的 FastDDS 預設在慢速網路上可以運作，但**對於「點對點、機器人近場」場景，CycloneDDS 的 discovery 較精簡、預設參數較省頻寬**，現場實驗常能獲得較低延遲。

安裝與套用：

```bash
# 安裝 CycloneDDS 的 RMW 實作
sudo apt install ros-humble-rmw-cyclonedds-cpp

# 啟動前設定環境變數
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

若要進一步降低背景廣播量、並把流量導向穩定的網段，建立 `cyclonedds.xml`：

```xml
<CycloneDDS>
  <Domain>
    <General>
      <MaxMessageSize>65500</MaxMessageSize>
    </General>
    <Internal>
      <Watermarks>
        <WhcHigh>100000</WhcHigh>
      </Watermarks>
    </Internal>
  </Domain>
</CycloneDDS>
```

```bash
export CYCLONEDDS_URI=file:///home/<user>/ros2_ws/cyclonedds.xml
```

> 若仍想留在 FastDDS，可在 `FASTRTPS_DEFAULT_PROFILES_FILE` 指定 profile，或直接採用 ROS 2 預設——重點是**先穩定再談調校**。

### 3.2 鎖定 Wi-Fi 頻段：5GHz 優先、關閉漫遊

機器人場域最常見的干擾源是 **2.4GHz：藍牙、微波爐、隔壁廠房的 AP**。2.4GHz 只有 3 個不重疊通道且穿透性太好（互相打架），而 5GHz 通道較多、較乾淨。**6GHz（Wi-Fi 6E）在乾淨環境下延遲最低**，但如果你的 AP 是 6E 機種，優先鎖定 6GHz 也可行。

鎖定頻段的兩個層級：

**① AP 端（最少動手）：** 在基地台上建立一個「**僅 5GHz / 僅 6GHz**」的專用 SSID，`band_steering` 關閉，讓機器人 RTK 只連這條乾淨通道。

**② 機器人端（NetworkManager）：** 直接指定頻段，避免它自己漫遊到擁擠的 2.4GHz：

```bash
# 查看目前連線名稱
nmcli c

# 建立/調整連線，鎖定 5GHz 頻段（band a = 5GHz）
nmcli con mod <連線名稱> 802-11-wireless.band a

# 也可以鎖定特定通道與停用隨機 MAC（讓 AP 端辨識穩定）
nmcli con mod <連線名稱> 802-11-wireless.channel 36

# 重新啟動連線套用設定
nmcli con up <連線名稱>
```

**③ 停用不必要的網卡漫遊：** 無線網卡在訊號變弱時會嘗試換 AP，每次漫遊 = 幾百 ms 斷流 = DDS discovery 中斷。若場域只有單一 AP，優先鎖定它。

### 3.3 QoS 與 Topic 的實務取捨

在 ROS 2 中，**影像與雷射點雲建議使用 `BEST_EFFORT`**（寧可掉一幀，不要整條管道卡住），**導航制限與狀態機則用 `RELIABLE`**。在訊號弱的 Wi-Fi 上，全 RELIABLE 會造成重傳風暴。

```bash
# 範例：訂閱點雲時指定 BEST_EFFORT QoS
ros2 run your_pkg your_node --ros-args \
  -p sensor_qos:=best_effort
```

（RDI 應用、Sensor Data QoS 的完整對照表可參考 ROS 2 Humble 官方文件。）

### 3.4 檢查驅動與韌體：原生支援不等於不用更新

AWUS036AXML 使用 MediaTek **MT7921AU** 晶片，在 Ubuntu 22.04（Kernel 5.15+）/ 24.04 與 Kali 2025 皆為**核心內建 `mt7921u` 驅動，隨插即用、不需編譯**。但韌體（firmware）仍要確保新：

```bash
sudo apt update
sudo apt install linux-firmware firmware-misc-nonfree
sudo reboot

# 確認介面出現
ip link show            # 應出現 wlan0 或 wlan1
iw dev                 # 可列出無線介面
```

> **支援邊界**：AWUS036AXML **不支援 macOS（Intel 與 Apple Silicon 皆不支援）**。若你的 ROS 2 開發主機是 Mac，請改用具備原生支援的 Linux 主機或 Linux 機器人控制器；本產品的任何排障流程都以 Linux 為前提。

---

## 4. 排障工作表：斷網與延遲標準檢查清單

> 遇到「ROS 2 節點斷線 / 延遲」時，依序按下表檢查並記錄，作為向技術客服求助時最有效的資訊封包（Intake）。

### Step 1：確認 OS 與網卡狀態

| 檢查項 | 指令 | 記錄欄 |
|---|---|---|
| 作業系統與核心 | `lsb_release -a && uname -r` | \_\_\_\_\_ |
| 無線介面存在 | `ip link show` / `iw dev` | \_\_\_\_\_ |
| 訊號強度（RSSI） | `iw dev wlanX link \| grep signal` | \_\_\_dBm |
| 連線速率 | `iw dev wlanX link \| grep bitrate` | \_\_\_\_ Mbps |
| 驅動有無 | `lsmod \| grep mt7921` | \_\_\_\_\_ |

### Step 2：確認網路拓撲

| 檢查項 | 選項 |
|---|---|
| AP 型號與頻段 | 2.4GHz / 5GHz / 6GHz |
| 機器人到 AP 距離 | ____ 公尺 |
| 中間是否隔金屬/碳纖維 | 是 / 否 |
| 天線位置 | 機殼內 / 機殼外 |

### Step 3：DDS / RMW 檢查

| 檢查項 | 指令 |
|---|---|
| 目前 RMW | `echo $RMW_IMPLEMENTATION` |
| CycloneDDS 組態檔 | `echo $CYCLONEDDS_URI` |
| 節點可否發現彼此 | `ros2 node list`（在多台機器上各自執行比對）|
| topic 是否有動態 | `ros2 topic hz /your_topic` |

### Step 4：壓力測試（30 秒封包回報）

```bash
# 在機器人端發布一個高頻 topic
ros2 run demo_nodes_cpp talker

# 在另一端訂閱並看實際頻率穩不穩
ros2 topic hz /chatter
```

**判定原則**：
- 目標 30Hz 而實際只有 8–12Hz 且抖動大 → 多半是**網路品質**（檢查 RSSI、換天線位置）。
- RSSI 已 > -60dBm 但仍不穩 → 檢查 **AP 通道干擾、頻段鎖定、DDS 設定**。
- 兩個都正常仍斷線 → 檢查**供電**（高功率網卡建議接獨立供電的 USB Port / Powered Hub，避免瞬間壓降）。

### 客服 Intake 資訊封包

向技術支援求助時，請一次附上：**OS+核心版號、網卡型號、RSSI、bitrate、AP 頻段、天線位置、`ros2 topic hz` 輸出**。這些資訊能讓客服直接定位到「硬體屏蔽問題」還是「組態問題」，大幅縮短來回時間。

---

## 5. 免責聲明與安全紅線

本方案為開源學術平台 bench-test 評估，非商用成品之官方支援。

- **僅限你擁有所有權或已獲授權的開發設備**進行測試，不代表任何機器人原廠之官方認證。
- 本文不涉及任何**商用閉源機器人/無人機品牌**的相容性宣稱；如你的平台為商用封閉系統，請洽原廠技術支援。
- 若你的開發平台涉足**工業安全關鍵控制系統（Safety-critical control systems）**，請勿將本案的無線化改造直接套用於安全迴路，維持有線或既有安全通道。
- 請勿關閉作業系統安全防護（如 Secure Boot、防火牆）來遷就網路問題；本文全部設定均在安全防護開啟下運作。

---

## 結語與硬體建議

金屬與碳纖維外殼造成的法拉第籠效應，是移動機器人無線化的第一道牆；**把天線移出籠子**（外接高增益天線）是投入產出比最高的一招。搭配 ROS 2 的 DDS 設定與頻段鎖定，讓節點同步恢復「即時且可靠」。

**推薦硬體**：ALFA AWUS036AXML（MediaTek MT7921AU，Linux 原生免編譯核心支援、雙 RP-SMA 外接天線、Wi-Fi 6E 三頻，Kali / Ubuntu 隨插即用）。如果你偏好較舊但同樣成熟的 Realtek 方案，也可參考 AWUS036ACH（RTL8812AU，5GHz 雙天線），但需留意核心更新後的 DKMS 驅動編譯事項（我們會在另一篇文章詳細拆解）。

**下一步**：把這份排障工作表印出來，跟你的夾具、量測工具一起送進場域——資料治百病。
