---
title: "ALFA AWUS036ACM：在 Raspberry Pi 上啟用 IBSS Ad Hoc 與 802.11s Mesh 網路（MT7612U）"
description: "ALFA AWUS036ACM（MT7612U）是目前唯一現行生產的 ALFA USB WiFi 無線網卡，可在 Raspberry Pi 上完整支援 IBSS Ad Hoc 與 802.11s Mesh 網路——即插即用，無需安裝驅動程式。本文詳解設定步驟。"
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Mesh 網路", "Linux", "無線網路"]
---

# ALFA AWUS036ACM：在 Raspberry Pi 上啟用 IBSS Ad Hoc 與 802.11s Mesh 網路（MT7612U）

如果你曾嘗試在多台 Raspberry Pi 節點之間建立**無需路由器**的 WiFi 網路，或是想打造一個能自動透過中繼節點轉發封包、具備自癒能力的無線 Mesh——你很快就會發現，大多數 USB WiFi 無線網卡根本辦不到。核心驅動程式根本沒有開放對應的模式。

**ALFA AWUS036ACM** 搭載 **MediaTek MT7612U** 晶片組，是這個領域的例外。其內建的 `mt76` 核心驅動程式完整實作了 Linux mac80211 介面，這意味著它在 Raspberry Pi 上原生支援 **IBSS（Ad Hoc）模式**與 **802.11s Mesh Point 模式**——開箱即用，無需編譯任何驅動程式。

本文將深入說明這兩種模式的運作原理、提供逐步設定指引，並協助你判斷何時該選用哪種模式。

---

## 目錄

1. [什麼是 IBSS 與 802.11s Mesh——為何重要？](#1-what-are-ibss-and-80211s-mesh)
2. [ALFA AWUS036ACM 硬體規格](#2-alfa-awus036acm-hardware-specifications)
3. [MT7612U 驅動程式在 Raspberry Pi 上的表現](#3-the-mt7612u-driver-on-raspberry-pi)
4. [模式一：IBSS Ad Hoc 網路](#4-mode-1-ibss-ad-hoc-networking)
5. [模式二：802.11s Mesh Point 網路](#5-mode-2-80211s-mesh-point-networking)
6. [實際應用場景](#6-real-world-use-cases)
7. [為何 AWUS036ACM 是此用途的唯一 ALFA 選擇](#7-why-the-awus036acm-is-the-only-alfa-choice-for-this)
8. [常見問題與疑難排解](#8-faq-and-troubleshooting)
9. [購買管道](#9-where-to-buy)

---

## 1. 什麼是 IBSS 與 802.11s Mesh？

### IBSS——獨立基本服務集（Ad Hoc 模式）

當你將筆電連接到家中的 WiFi 路由器時，無線網卡處於**受管理（Station）模式**——它與單一中央 Access Point 通訊。IBSS 則完全相反：這是 IEEE 802.11 規範中定義的**對等無線網路，不需要任何中央基礎設施**。

在 IBSS 模式下：

- 裝置之間**直接**互相通訊，無需 AP 或路由器介入
- 同一 SSID 與頻道上的任意兩台裝置皆可交換資料
- 網路完全自給自足——不需要網際網路連線
- IP 位址以靜態方式指派（或透過你自行執行的簡單 DHCP 服務分配）
- 第一台「加入」IBSS 的裝置會成為 BSSID（儲存格識別碼）的發起者

可以把它想像成在少數幾台 Pi 節點之間，即時建立一個私有無線區域網路——無論是雙節點直連管道、三節點感測器叢集，還是現場部署的攜帶式通訊套件，都適用。

**IBSS 的已知限制：**
- 所有節點必須在彼此的直接無線電通訊範圍內——沒有自動多跳轉發功能
- IBSS 模式不支援標準 WPA2 加密（技術上可用 WEP，但不建議；大多數部署改用應用層加密）
- 實際使用上，節點數超過 3–5 台後效能便會下滑

### 802.11s Mesh Point——可擴展的替代方案

802.11s 是獨立的 IEEE 修訂標準，定義了**真正的無線 Mesh 網路**。與 IBSS 不同，802.11s Mesh 具備以下特性：

- 自動探索相鄰節點並建立路由表
- 透過中繼節點轉發流量，以觸及超出直接通訊範圍的節點
- 當某節點失效時自動自癒——路徑會自動切換至其他可用路徑
- 預設使用 **Hybrid Wireless Mesh Protocol（HWMP）** 進行路徑選擇

```
範例：4 節點 Mesh

  [Pi A] ──── [Pi B] ──── [Pi C]
                │
              [Pi D]

Pi A 可自動透過 Pi B 抵達 Pi C。
Pi A 可自動透過 Pi B 抵達 Pi D。
若 Pi B 失效，Mesh 會嘗試尋找替代路徑。
```

當你有超過 3–4 個節點、節點分布在較大的區域，或希望網路在不需手動管理的情況下保持韌性時，802.11s 就是正確的選擇。

### 為何很難找到可用的無線網卡

上述兩種模式都要求 WiFi 驅動程式建構於 Linux 的 **mac80211** 軟體 MAC 層之上——這是核心中的官方 802.11 協定堆疊。只有符合 mac80211 規範的驅動程式，才能將 IBSS 和 Mesh Point 作為可用的介面類型開放出來。

許多常見的 USB WiFi 無線網卡使用**核心外驅動程式**，自行實作了簡化版的無線協定堆疊，刻意略過 IBSS 和 Mesh 支援。即便是部分較新晶片組的核心內驅動程式，也不一定開放這些模式。

MT7612U 是少數可以對兩者都給出清楚、明確「是」的晶片組之一。

---

## 2. ALFA AWUS036ACM 硬體規格

AWUS036ACM 是 ALFA Network 的 AC1200 雙頻 USB 3.0 無線網卡，專為 Linux 進階使用者與嵌入式開發者所設計。

![ALFA AWUS036ACM](/images/products/alfa/awus036acm.png)

### 核心規格

| 參數 | 數值 |
|---|---|
| **晶片組** | MediaTek MT7612U |
| **WiFi 標準** | IEEE 802.11 a/b/g/n/ac（WiFi 5） |
| **頻段** | 2.4 GHz（2.412–2.472 GHz）+ 5 GHz（5.15–5.825 GHz） |
| **頻道頻寬** | 20 / 40 / 80 MHz |
| **最高速率（5 GHz）** | 867 Mbps（802.11ac） |
| **最高速率（2.4 GHz）** | 300 Mbps（802.11n） |
| **合計速率** | AC1200（867 + 300 Mbps） |
| **USB 介面** | USB 3.0 Type-A（向下相容 USB 2.0） |
| **天線** | 2× RP-SMA 母座，2× 5 dBi 雙頻全向天線（可拆卸） |
| **USB VID/PID** | 0e8d:7612 |
| **LED 指示燈** | 電源 + 無線網路活動 |
| **隨附配件** | USB 3.0 延長線、驅動程式光碟（Windows） |
| **尺寸** | 62 × 85.3 × 24 mm |
| **重量** | 60 g |
| **原產地** | 台灣（Alfa Network Inc.） |

### 發射功率

| 標準 | 發射功率 |
|---|---|
| 802.11a | 20 dBm |
| 802.11b | 23 dBm |
| 802.11g | 23 dBm |
| 802.11n | 21 dBm |
| 802.11ac | 20 dBm |

### 接收靈敏度

| 標準 | 靈敏度 |
|---|---|
| 802.11a | −92 dBm |
| 802.11b | −97 dBm |
| 802.11g | −90 dBm |
| 802.11n | −90 dBm |
| 802.11ac | −86 dBm |

### 支援的介面模式（完整清單）

這是關鍵的能力對照表。MT7612U / mt76x2u 驅動程式支援所有主要的 mac80211 介面模式：

| 模式 | 支援狀態 | 說明 |
|---|---|---|
| **IBSS** | ✅ 支援 | Ad Hoc 對等連線，無需 AP |
| **Managed（Station）** | ✅ 支援 | 標準用戶端模式 |
| **AP** | ✅ 支援 | 軟體 Access Point（hostapd） |
| **AP/VLAN** | ✅ 支援 | AP 上的虛擬區域網路 |
| **Monitor** | ✅ 支援 | 被動封包擷取 + 封包注入 |
| **Mesh Point** | ✅ 支援 | 802.11s 多跳 Mesh 網路 |
| **P2P-client** | ✅ 支援 | Wi-Fi Direct 用戶端 |
| **P2P-GO** | ✅ 支援 | Wi-Fi Direct 群組擁有者 |

### 無線安全性
WPA2 / WPA / WEP / WPA-PSK / 802.1X / 64–128 位元 WEP

### 支援的作業系統

| 作業系統 | 狀態 | 備註 |
|---|---|---|
| Raspberry Pi OS（2020 年以後） | ✅ 即插即用 | 零驅動程式安裝 |
| Ubuntu 20.04 LTS+ | ✅ 即插即用 | 核心內建 mt76 驅動程式 |
| Kali Linux 2019.3+ | ✅ 即插即用 | 完整支援監控模式、封包注入與 VIF |
| Debian 11+ | ✅ 可用 | 可能需要 firmware-misc-nonfree |
| Arch Linux | ✅ 即插即用 | 4.19 起核心內建 |
| Windows 10/11 | ✅ 支援 | 官方驅動程式可從 Alfa 官網下載 |
| Android NetHunter | ✅ 支援 | OTG USB |
| macOS 11+ / Apple Silicon | ❌ 不支援 | 僅支援 macOS 10.7–10.12 |

---

## 3. MT7612U 驅動程式在 Raspberry Pi 上的表現

### 驅動程式：mt76x2u（mt76 家族成員）

MediaTek MT7612U 由 `mt76x2u` 驅動程式負責處理，這個驅動程式隸屬於更廣泛的 **mt76** 驅動程式專案——由 MediaTek 維護並已整合進 Linux 核心主線。

**關鍵數字：**
- 核心內建自：**Linux 核心 4.19**（2018 年 10 月釋出）
- Raspberry Pi OS 搭載核心 **5.15+**（Pi 4/5）和 **5.10+**（Pi 3B+）——均遠高於 4.19
- **在任何現代 Raspberry Pi OS 上均無需任何安裝步驟**

### 如何確認驅動程式已載入

插入 AWUS036ACM 後，執行：

```bash
lsusb
```

找到以下項目：
```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

接著確認驅動程式已啟用：

```bash
dmesg | grep mt76
```

預期輸出（精簡版）：
```
mt76x2u 1-1.4:1.0: ASIC revision: 76120044
mt76x2u 1-1.4:1.0: Firmware Version: 0.1
mt76x2u 1-1.4:1.0: loaded firmware from mediatek/mt7662u_rom_patch.bin
```

列出新介面：
```bash
iw dev
```

你應該會看到一個新介面（若 Pi 內建 WiFi 為 `wlan0`，通常會是 `wlan1`）：
```
phy#1
    Interface wlan1
        ifindex 4
        wdev 0x100000001
        addr xx:xx:xx:xx:xx:xx
        type managed
        channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
```

查看無線網卡的完整能力清單：
```bash
iw phy phy1 info | grep -A 20 "Supported interface modes"
```

你將看到：
```
Supported interface modes:
     * IBSS
     * managed
     * AP
     * AP/VLAN
     * monitor
     * mesh point
     * P2P-client
     * P2P-GO
```

### 驅動程式架構為何重要

AWUS036ACM 的驅動程式堆疊結構如下：

```
你的應用程式（ping、iperf3、batman-adv……）
        ↓
nl80211 / cfg80211  ← 核心 WiFi 設定 API
        ↓
mac80211            ← IEEE 802.11 軟體 MAC 層
        ↓
mt76x2u             ← MT7612U USB 硬體驅動程式
        ↓
MediaTek MT7612U    ← 實體晶片（2×2 MIMO，USB 3.0）
```

**mac80211** 是 Linux 核心對完整 802.11 狀態機的實作——負責處理信標管理、幀構建、省電模式、IBSS 對等節點探索，以及 Mesh 路徑路由。建構在 mac80211 之上的驅動程式會自動繼承這些所有能力。

繞過 mac80211 的驅動程式（例如 Realtek 的核心外驅動程式）僅實作它們選擇開放的模式——而 IBSS 和 Mesh Point 幾乎總是被省略。

---

## 4. 模式一：IBSS Ad Hoc 網路

### IBSS 的運作原理

在 IBSS 模式下，每個無線網卡自行管理 802.11 幀。當兩個無線網卡設定為相同的 SSID 與頻道時：

1. 第一台裝置產生一個隨機的 **BSSID**（IBSS 儲存格 ID）
2. 它在所選頻道上廣播信標
3. 第二台裝置掃描後找到該信標，並**加入**儲存格
4. 兩台裝置現在可以直接交換資料幀——中間沒有 AP

從作業系統的角度來看，IBSS 介面的行為與普通乙太網路介面無異——你可以像平常一樣指派 IP 位址並使用 TCP/IP。

### IBSS 與受管理模式的快速比較

| 功能 | IBSS（Ad Hoc） | Managed（Station） |
|---|---|---|
| 需要中央 AP？ | ❌ 不需要 | ✅ 需要 |
| 需要網際網路？ | ❌ 不需要 | 通常需要 |
| 設定複雜度 | 低 | 極低 |
| 實際最大節點數 | 3–5 | 無限制（透過 AP） |
| WPA2 支援 | ❌ 不支援 | ✅ 支援 |
| 最適合 | 隔離的 Pi 叢集、現場套件 | 家庭/辦公室網路 |

### 逐步教學：兩台 Raspberry Pi IBSS 網路

此範例在兩台 Raspberry Pi 之間建立 5 GHz 直連連結。請根據你的部署需求調整 IP 位址與 SSID。

**在兩個節點上——識別正確的介面：**

```bash
iw dev
```

AWUS036ACM 通常會顯示為 `wlan1`（若 Pi 內建 WiFi 為 `wlan0`）。可透過比對 `lsusb` 的 MAC 位址來確認。以下所有指令中，請將 `wlan1` 替換為你實際的介面名稱。

---

#### 節點 1（Pi #1——IP：192.168.88.1）

**步驟 1——停止 NetworkManager / wpa_supplicant 的干擾：**

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```

**步驟 2——關閉介面：**

```bash
sudo ip link set wlan1 down
```

**步驟 3——將介面設為 IBSS 模式：**

```bash
sudo iw dev wlan1 set type ibss
```

**步驟 4——重新啟用介面：**

```bash
sudo ip link set wlan1 up
```

**步驟 5——加入（或建立）5 GHz 頻道 36 上的 IBSS 儲存格：**

```bash
sudo iw dev wlan1 ibss join RaspberryMesh 5180
```

> **頻率對應參考：**
> - 5180 MHz = 5 GHz 頻道 36（常見室內頻道，吞吐量佳）
> - 5200 MHz = 5 GHz 頻道 40
> - 2412 MHz = 2.4 GHz 頻道 1（涵蓋範圍較廣，速度較低）
> - 2437 MHz = 2.4 GHz 頻道 6

**步驟 6——指派靜態 IP 位址：**

```bash
sudo ip addr add 192.168.88.1/24 dev wlan1
```

---

#### 節點 2（Pi #2——IP：192.168.88.2）

執行相同指令，僅變更 IP 位址：

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
sudo ip link set wlan1 down
sudo iw dev wlan1 set type ibss
sudo ip link set wlan1 up
sudo iw dev wlan1 ibss join RaspberryMesh 5180
sudo ip addr add 192.168.88.2/24 dev wlan1
```

---

#### 驗證連結

在節點 1 上：
```bash
iw dev wlan1 link
```

預期輸出（節點 2 加入後）：
```
Connected to xx:xx:xx:xx:xx:xx (on wlan1)
    IBSS cell ID/AP: xx:xx:xx:xx:xx:xx
    SSID: RaspberryMesh
    freq: 5180
    RX: 1204 bytes (12 packets)
    TX: 852 bytes (8 packets)
    signal: -48 dBm
    tx bitrate: 300.0 MBit/s MCS 15 40MHz
```

測試連線：
```bash
ping -c 4 192.168.88.2
```

```
PING 192.168.88.2 (192.168.88.2) 56(84) bytes of data.
64 bytes from 192.168.88.2: icmp_seq=1 ttl=64 time=1.84 ms
64 bytes from 192.168.88.2: icmp_seq=2 ttl=64 time=1.92 ms
64 bytes from 192.168.88.2: icmp_seq=3 ttl=64 time=2.01 ms
64 bytes from 192.168.88.2: icmp_seq=4 ttl=64 time=1.88 ms
```

以 iperf3 測試吞吐量：
```bash
# 在節點 2（伺服器端）：
iperf3 -s

# 在節點 1（用戶端）：
iperf3 -c 192.168.88.2 -t 10
```

### 讓 IBSS 在重開機後持續生效

在每個節點上建立 `/etc/systemd/system/ibss-mesh.service`：

```ini
[Unit]
Description=IBSS Ad Hoc Mesh Network
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  ip link set wlan1 down && \
  iw dev wlan1 set type ibss && \
  ip link set wlan1 up && \
  iw dev wlan1 ibss join RaspberryMesh 5180 && \
  ip addr add 192.168.88.1/24 dev wlan1'
ExecStop=/bin/bash -c '\
  iw dev wlan1 ibss leave && \
  ip link set wlan1 down'

[Install]
WantedBy=multi-user.target
```

啟用服務：
```bash
sudo systemctl daemon-reload
sudo systemctl enable ibss-mesh.service
sudo systemctl start ibss-mesh.service
```

> **注意：** 請為每個節點修改服務檔案中的 IP 位址（`.1`、`.2`、`.3`，以此類推）

### 新增第三個節點

對節點 3 使用相同步驟，IP 位址設為 `192.168.88.3`。三個節點必須全部在彼此的直接無線電通訊範圍內。若要讓節點 1 與節點 3 之間的流量透過節點 2 路由，請在節點 2 上啟用 IP 轉發：

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

## 5. 模式二：802.11s Mesh Point 網路

### 802.11s 的運作原理

802.11s 修訂標準在 802.11 MAC 中直接加入了一層 **Mesh 協調層**。節點不再全部連向同一個中央 AP，而是各自：

1. 在所選頻道與 `mesh_id` 上廣播 **Mesh 信標**幀，以探索鄰近的 Mesh 節點
2. 執行 **HWMP（Hybrid Wireless Mesh Protocol）** 計算到達各目的地的最佳路徑
3. 在資料幀上封裝 **Mesh 表頭**，其中包含來源與目的地 MAC 位址以及 Mesh 序列號
4. 當目的地超出直接通訊範圍時，自動透過中繼節點轉發幀

Linux 核心透過 `iw` 中的 `mp`（Mesh Point）介面類型開放此功能，核心本身的 802.11s 實作負責處理所有對等連線與路徑管理。

### 802.11s 與 IBSS 的比較

| 功能 | IBSS（Ad Hoc） | 802.11s Mesh Point |
|---|---|---|
| IEEE 標準 | 802.11 IBSS | 802.11s |
| 多跳路由 | ❌ 僅限手動 | ✅ 自動（HWMP） |
| 節點覆蓋範圍 | 全部需在直接通訊範圍內 | 可延伸超出單跳範圍 |
| 可擴展性 | 實際 3–5 個節點 | 搭配 batman-adv 可支援 10+ 節點 |
| 設定複雜度 | 低 | 中 |
| 自癒能力 | ❌ 無 | ✅ 有 |
| 最適合 | 簡單 2–3 節點設定 | 較大型的分散式系統 |

### 逐步教學：多節點 802.11s Mesh

此範例在 5 GHz 頻道 36 上建立三節點 Mesh。每個節點會自動探索其他節點並建立路徑。

---

#### 在每個節點上——建立 Mesh 介面

**步驟 1——識別實體裝置（phy）名稱：**

```bash
iw dev
```

找到與 AWUS036ACM 對應的 phy（通常為 `phy1`）：
```
phy#1
    Interface wlan1
        ...
```

**步驟 2——新增名為 `mesh0` 的 Mesh Point 介面：**

```bash
sudo iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh
```

> 這會在與 `wlan1` 相同的實體無線電上建立一個新的虛擬介面 `mesh0`。原有的 `wlan1` 可同時保持受管理模式以存取網際網路——這正是 VIF（虛擬介面）的作用。

**步驟 3——設定工作頻道（5 GHz 頻道 36）：**

```bash
sudo iw dev mesh0 set channel 36
```

**步驟 4——啟用 Mesh 介面：**

```bash
sudo ip link set mesh0 up
```

**步驟 5——為每個節點指派唯一 IP 位址：**

```bash
# 節點 1：
sudo ip addr add 10.88.0.1/24 dev mesh0

# 節點 2：
sudo ip addr add 10.88.0.2/24 dev mesh0

# 節點 3：
sudo ip addr add 10.88.0.3/24 dev mesh0
```

---

#### 驗證 Mesh 建立狀況

**確認對等節點已被探索：**

```bash
iw dev mesh0 station dump
```

範例輸出（節點 1 看到節點 2 和節點 3）：
```
Station xx:xx:xx:xx:xx:02 (on mesh0)
    inactive time:  120 ms
    rx bytes:       4820
    tx bytes:       3560
    signal:         -52 dBm
    tx bitrate:     300.0 MBit/s MCS 15 40MHz
    mesh plink:     ESTAB
    mesh local PS mode: ACTIVE

Station xx:xx:xx:xx:xx:03 (on mesh0)
    mesh plink:     ESTAB
```

**查看 Mesh 路由路徑：**

```bash
iw dev mesh0 mpath dump
```

```
DEST ADDR         NEXT HOP          IFACE   SN      METRIC  QLEN    EXPTIME         DTIM    DRET    FLAGS
xx:xx:xx:xx:xx:02 xx:xx:xx:xx:xx:02 mesh0   32      1158    0       0       100     0       0x4
xx:xx:xx:xx:xx:03 xx:xx:xx:xx:xx:02 mesh0   18      2316    0       0       100     0       0x14
```

> 節點 3 的下一跳為節點 2——表示節點 1 會自動透過節點 2 抵達節點 3。

**跨 Mesh 進行 Ping 測試：**

```bash
# 從節點 1：
ping -c 4 10.88.0.3
```

### 進階：加入 batman-adv 實現第二層 Mesh 路由

針對正式部署，以 **batman-adv** 取代核心內建的 HWMP，可獲得更進階的路由能力、在節點移動時有更好的效能，以及與更高層網路工具的相容性。

**安裝 batman-adv：**

```bash
sudo apt install batctl
```

**載入模組：**

```bash
sudo modprobe batman-adv
```

**將 Mesh 介面設為 batman-adv 從屬介面：**

```bash
# 先讓 mesh0 啟用但不配置 IP
sudo ip link set mesh0 up
sudo batctl if add mesh0

# 啟用 batman 介面
sudo ip link set bat0 up

# 將 IP 指派給 batman 介面（而非 mesh0）
sudo ip addr add 10.88.0.1/24 dev bat0
```

**查看 batman 路由表：**

```bash
sudo batctl n    # 鄰居節點
sudo batctl o    # 發起者表（所有已知節點）
sudo batctl tg   # 轉換表（MAC → IP 對應）
```

### 讓 802.11s Mesh 在重開機後持續生效

建立 `/etc/systemd/system/mesh-point.service`：

```ini
[Unit]
Description=802.11s Mesh Point Network
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh && \
  iw dev mesh0 set channel 36 && \
  ip link set mesh0 up && \
  ip addr add 10.88.0.1/24 dev mesh0'
ExecStop=/bin/bash -c '\
  ip link set mesh0 down && \
  iw dev mesh0 del'

[Install]
WantedBy=multi-user.target
```

啟用：
```bash
sudo systemctl daemon-reload
sudo systemctl enable mesh-point.service
sudo systemctl start mesh-point.service
```

---

## 6. 實際應用場景

### 場景一——離網感測器網路（智慧農業／環境監測）

**情境：** 三台 Raspberry Pi 部署於農田各處，各自搭載土壤濕度、溫度與濕度感測器。現場沒有行動網路或 WiFi 基礎設施。

**設定：** 使用 2.4 GHz 頻道 1（2412 MHz）的 IBSS，以獲得最大通訊範圍。每個節點每 30 秒收集一次感測器資料，並傳送至中央紀錄節點（節點 1）。

**選用 AWUS036ACM 的理由：** 5 dBi 天線搭配 2.4 GHz 的 23 dBm 發射功率，讓這張無線網卡擁有高於平均的通訊範圍——對於覆蓋農田中的行間距離非常實用。透過選配 RP-SMA 天線升級（例如方向性八木天線），通訊距離還可大幅延伸。

**資料流程範例：**
```
[感測器 Pi A] ──IBSS──> [邊緣 Pi B（記錄器）]
[感測器 Pi C] ──IBSS──> [邊緣 Pi B（記錄器）]
```

---

### 場景二——無人機／機器人叢集通訊

**情境：** 兩三台以 Raspberry Pi 為核心的無人機或地面機器人，需要在不透過地面站的情況下共享遙測資料並協調行動。

**設定：** 使用 5 GHz 頻道 36（5180 MHz）的 IBSS，以獲得低延遲與高吞吐量。每台裝置串流 1080p H.264 影片（約 5 Mbps）以及低於 100 Kbps 的遙測資料。

**選用 5 GHz 的理由：** AWUS036ACM 在 5 GHz 達到 AC1200 速率（867 Mbps），足以應付多路同步影像串流。5 GHz 頻段也避開了都市環境中擁擠的 2.4 GHz 干擾。

**網路拓撲：**
```
[無人機 1 / 192.168.88.1] ──5GHz IBSS──> [無人機 2 / 192.168.88.2]
```

---

### 場景三——災難應變／緊急通訊套件

**情境：** 快速部署小隊抵達無任何基礎設施的現場。每位隊員攜帶一台 Raspberry Pi Zero 2W + AWUS036ACM + 行動電源。在 60 秒內，一個可運作的多節點 Mesh 即可啟動，用於文字通訊、檔案共享與協調。

**設定：** 使用 2.4 GHz 的 802.11s Mesh，在建築物與障礙物間取得最大通訊範圍。batman-adv 負責路由，無需隊員手動管理 IP 位址。

**選用 802.11s / batman-adv 的理由：** 隊員移動時，Mesh 拓撲隨之改變，batman-adv 會自動更新路徑。沒有單點故障問題。

---

### 場景四——Raspberry Pi 運算叢集骨幹網路

**情境：** 開發者以 4–6 台 Raspberry Pi 4 建立 Beowulf 風格的運算叢集，希望有一條獨立於主要乙太網路之外的專用低延遲互連通道。

**設定：** 使用 5 GHz 的 802.11s Mesh，mesh_id 設為 `ClusterBackbone`。各節點透過 Mesh 進行行程間通訊（MPI、Redis pub/sub、ZeroMQ）。

**使用專用 Mesh 的理由：** 將叢集流量與主要網路分離，可避免佔用共用乙太網路交換器的頻寬，且在主要網路不可用時，叢集網路依然正常運作。

---

### 場景五——資安研究實驗室／隔離測試環境

**情境：** 滲透測試員或資安研究員想要模擬一個私有的 802.11 IBSS 網路，以測試 Ad Hoc 特有漏洞或驗證偵測工具。

**設定：** 在乾淨頻道上建立 IBSS，與生產 WiFi 隔離；同時透過 VIF，以同一張 AWUS036ACM 啟用監控模式。一個介面處於 IBSS 模式（參與網路），另一個處於監控模式（擷取所有幀供 Wireshark 分析）。

```bash
# 在 IBSS 旁建立監控介面
sudo iw phy phy1 interface add mon0 type monitor
sudo ip link set mon0 up
# 開始擷取：
sudo tcpdump -i mon0 -w capture.pcap
```

---

## 7. 為何 AWUS036ACM 是此用途的唯一 ALFA 選擇

### 關鍵因素：mac80211 相容性

USB WiFi 無線網卡是否能在 Linux 上支援 IBSS 和 802.11s Mesh，完全取決於其驅動程式架構。只有**基於 mac80211 的核心內驅動程式**才會開放這些模式。自行實作 WiFi 協定堆疊的驅動程式（大多數核心外 Realtek 驅動程式）根本不包含 IBSS 或 Mesh 功能。

### 其他現行 ALFA 無線網卡的狀況

| 型號 | 晶片組 | 驅動程式 | IBSS | 802.11s Mesh | 備註 |
|---|---|---|---|---|---|
| **AWUS036ACM** | MT7612U | mt76x2u（核心內建 ≥ 4.19） | ✅ | ✅ | **唯一選擇** |
| AWUS036ACH | RTL8812AU | rtw88（核心內建 ≥ 6.14） | ✅（僅限核心 ≥ 6.14） | ❌ | 新版核心內驅動程式；不支援 Mesh Point |
| AWUS036ACS | RTL8811AU | rtl8812au-dkms（核心外） | ❌ | ❌ | 核心外驅動程式；不支援 IBSS/Mesh |
| AWUS036AX | RTL8832BU | rtw88（核心內建） | ❌ | ❌ | 不支援 Raspberry Pi |
| AWUS036AXER | RTL8832BU | rtw88（核心內建） | ❌ | ❌ | 不支援 Raspberry Pi |
| AWUS036AXM | MT7921AUN | mt7921u（核心內建 ≥ 5.18） | ❌ | ❌ | mt7921u 未開放 IBSS |
| AWUS036AXML | MT7921AUN | mt7921u（核心內建 ≥ 5.18） | ❌ | ❌ | mt7921u 未開放 IBSS |
| ~~AWUS036ACHM~~ | ~~MT7610U~~ | ~~mt76x0u~~ | ~~✅~~ | ~~✅~~ | **已停產** |
| ~~AWUS1900~~ | ~~RTL8814AU~~ | ~~核心外~~ | ~~有限支援~~ | ~~❌~~ | **已停產** |

### 這對你意味著什麼

AWUS036ACHM（MT7610U）曾是支援這些模式的前代 ALFA 無線網卡，但現已停產。目前 ALFA 現行製造的 USB 無線網卡中，沒有任何其他型號能在 Raspberry Pi 上提供乾淨、即插即用的 IBSS 與 802.11s Mesh 支援。

**AWUS036ACM 不只是最佳選擇——在 ALFA 的現行產品線中，它是此用途的唯一選擇。**

此外，AWUS036ACM 還提供：
- **AC1200 雙頻**——可在 2.4 GHz（涵蓋範圍）或 5 GHz（吞吐量）上運行 IBSS/Mesh
- **USB 3.0**——在 Pi 4/5 的 USB 3.0 埠上充分利用頻寬
- **2 支可拆卸 RP-SMA 天線**——可升級至高增益方向性天線，將 Mesh 通訊距離大幅延伸，遠超隨附的 5 dBi 全向天線
- **VIF 支援**——可在同一張無線網卡上同時運行 Mesh 骨幹與 AP 模式
- **支援 Raspberry Pi 3B+、4 和 5**——跨所有 Pi 世代均保持一致

---

## 8. 常見問題與疑難排解

**問：我的 Pi 只顯示 `wlan0`，`wlan1` 在哪裡？**

AWUS036ACM 介面會在插入無線網卡後才出現。插入後執行 `iw dev`。若 10 秒內仍未出現，請檢查 `dmesg | grep -i mt76` 是否有錯誤訊息。在 Raspberry Pi OS Lite 上，若套件尚未安裝，可能需要執行 `sudo apt install iw`。

---

**問：`iw dev wlan1 set type ibss` 回傳「Device or resource busy」**

NetworkManager 或 `wpa_supplicant` 正在佔用該介面。請先停止它們：
```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```
然後重試。在有桌面環境的 Raspberry Pi OS 上，`dhcpcd` 也可能佔用介面——請在 `/etc/dhcpcd.conf` 中加入 `denyinterfaces wlan1`，然後重新啟動 `dhcpcd`。

---

**問：`iw phy phy1 interface add mesh0 type mp` 回傳「Operation not supported」**

無線網卡的 phy 名稱可能不是 `phy1`。請執行 `iw dev` 確認 AWUS036ACM 對應的 phy，並替換為正確名稱。

---

**問：IBSS 已設定完成，但節點之間的 Ping 失敗**

請檢查：
1. 兩個節點使用**完全相同的頻率**（例如都是 `5180`，而非一個 `5180` 一個 `5200`）
2. 兩個節點的 **IP 位址不同**，且位於同一子網路
3. 沒有防火牆封鎖 ICMP——執行 `sudo iptables -L` 確認
4. 執行 `iw dev wlan1 link` 確認兩個節點的 IBSS 儲存格 ID（BSSID）相符

---

**問：mesh0 介面在重開機後消失了**

透過 `iw` 建立的虛擬介面不會在重開機後保留。請使用[第 5 節](#making-80211s-mesh-persistent)中的 systemd 服務，讓它們在開機時自動重建。

---

**問：我可以在 IBSS 上使用 WPA2 加密嗎？**

Linux 核心的 IBSS 模式不支援標準 WPA2-Personal（PSK）。若需要安全的 IBSS 連線，可使用應用層加密（WireGuard、OpenVPN 或 SSH 通道）。802.11s Mesh 則支援搭配 `wpa_supplicant` 使用 SAE（WPA3 風格的認證）。

---

**問：AWUS036ACM 可以同時處於 IBSS 和受管理模式嗎？**

可以——這正是 VIF（虛擬介面）的用途。你可以讓 `wlan1` 保持受管理模式連接家用路由器以存取網際網路，同時新增第二個虛擬介面處於 IBSS 或 Mesh 模式，用於 Pi 對 Pi 網路：

```bash
# wlan1 保持受管理模式（網際網路）
# 新增第二個介面用於 IBSS
sudo iw phy phy1 interface add adhoc0 type ibss
sudo ip link set adhoc0 up
sudo iw dev adhoc0 ibss join LocalNet 5180
sudo ip addr add 192.168.88.1/24 dev adhoc0
```

---

**問：最大通訊距離是多少？**

使用隨附的 5 dBi 天線，在 5 GHz 開放空間戶外環境下預期可達 20–50 公尺，2.4 GHz 可達 50–100 公尺。將天線更換為高增益 RP-SMA 方向性天線（另售），在視線良好的條件下，距離可延伸至數百公尺。AWUS036ACM 上的 RP-SMA 接頭為標準尺寸，與大量第三方天線相容。

---

**問：這適用於 Raspberry Pi Zero 2W 嗎？**

適用——Raspberry Pi Zero 2W 有完整尺寸的 USB-A 埠（透過 OTG 轉接頭），運行的 Raspberry Pi OS 核心版本遠高於 4.19。AWUS036ACM 可在其上正常運作，但請注意 Zero 2W 的 USB 埠為 USB 2.0，實際頻寬上限約為 300–400 Mbps。對於 IBSS/Mesh 控制流量和感測器資料而言，這已綽綽有餘。

---

## 9. 購買管道

ALFA AWUS036ACM 可在 [yupitek.com](https://yupitek.com) 購買——ALFA Network 的官方授權經銷商。透過授權經銷商購買，可確保你取得的是 Alfa Network Inc. 提供正規保固的原廠硬體。

**產品頁面：** [ALFA AWUS036ACM on Yupitek](https://yupitek.com)

盒裝內容：
- 1× AWUS036ACM 無線網卡
- 2× 可拆卸 5 dBi 雙頻全向天線（RP-SMA）
- 1× USB 3.0 延長線
- 1× 驅動程式光碟（Windows）

---

## 總結

| 功能 | AWUS036ACM |
|---|---|
| 晶片組 | MediaTek MT7612U |
| WiFi | AC1200（867 + 300 Mbps），雙頻 |
| IBSS Ad Hoc | ✅ 2020 年以後所有 Raspberry Pi OS 版本 |
| 802.11s Mesh | ✅ 即插即用 |
| 核心內驅動程式 | ✅ mt76x2u（自核心 4.19 起） |
| Pi 上即插即用 | ✅ 無需安裝 |
| 可拆卸天線 | ✅ 2× 5 dBi RP-SMA |
| 目前唯一支援 IBSS + Mesh 的 ALFA 型號 | ✅ 是 |

無論你需要在 Raspberry Pi 節點之間建立何種無線網路——從雙裝置直連到多跳自癒 Mesh——ALFA AWUS036ACM 都是讓這一切成真的無線網卡。

---

*文章由 Yupitek 技術團隊撰寫 · [yupitek.com](https://yupitek.com)*

*參考資料：[Alfa Network 官方文件](https://docs.alfa.com.tw/Product/AWUS036ACM/) · [Linux Wireless Wiki — 介面類型](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif) · [MediaTek mt76 Linux 驅動程式](https://wireless.wiki.kernel.org/en/users/drivers/mediatek) · [morrownr USB-WiFi 核心內清單](https://github.com/morrownr/USB-WiFi)*
