---
title: ALFA 網路卡 Soft AP 完整指南：在 Kali Linux、Ubuntu、Debian 與 Raspberry Pi 4/5 上建立 WiFi 熱點
created: 2026-05-22
type: article
tags: [blog, alfa-network, yupitek, soft-ap, hostapd, kali-linux, raspberry-pi, usb-wifi, awus036acm, awus036ach, awus036axml]
summary: 深度分析 Yupitek 銷售的 ALFA Network USB 無線網卡在 Linux 平台上的 Soft AP（WiFi 熱點）功能支援狀況。從晶片驅動、hostapd 設定到各平台相容性，附完整指令與疑難排解。
---

# ALFA 網路卡 Soft AP 完整指南：在 Kali Linux、Ubuntu、Debian 與 Raspberry Pi 4/5 上建立 WiFi 熱點

## 前言：為什麼你需要知道 Soft AP？

Soft AP（Software Access Point，軟體存取點）是指不使用專用 AP 硬體，而是透過軟體（主要是 **hostapd**）將 USB 無線網路卡直接變成一台 WiFi 基地台。

這個功能在以下場景中極其實用：

- **旅行/家用路由器**：出差或露營時，筆電或 Raspberry Pi 插上 ALFA 網卡，立刻變成隨身 WiFi 熱點
- **滲透測試練習環境**：在隔離環境中建立 Rogue AP 進行安全研究
- **IoT 設備中繼**：在訊號死角建立中繼站，讓 IoT 感測器回傳資料
- **邊緣 AI 部署**：工業場景中沒有有線網路，但需要讓設備作為熱點讓其他裝置連入
- **災難應變通訊**：斷網時快速建立臨時通訊網路

但問題來了：**不是每一張 USB 無線網卡都能跑 Soft AP。**

這篇文章基於我們對 GitHub（morrownr/USB-WiFi）、Reddit、Raspberry Pi 論壇和 Yupitek 內部測試的深度調查，告訴你哪些 ALFA 網卡適合、哪些不適合，以及完整的設定步驟。

---

## 一、Soft AP 的技術基礎：hostapd 如何運作？

在 Linux 環境中，Soft AP 依賴以下四個核心元件：

| 元件 | 功能 |
|------|------|
| **nl80211** | Linux 無線子系統標準框架，驅動與 userspace 之間的橋樑 |
| **hostapd** | 建立 AP 的主程式，將網卡切換到 Master Mode |
| **dnsmasq** | DHCP 伺服器，派發 IP 位址給連線的客戶端 |
| **iptables / nftables** | NAT 路由，讓客戶端可以透過 AP 上網 |

### 關鍵概念：Master Mode

**Master Mode**（又稱 AP Mode、Infrastructure Mode）是晶片驅動層面的能力。如果驅動不支援 Master Mode，hostapd 就無法啟動，也就無法建立 Soft AP。

驅動支援 Master Mode 與否，可以用以下指令快速確認：

```bash
iw list | grep -A 10 "Supported interface modes"
```

如果輸出中包含 `* AP`，代表該網卡的驅動支援 Soft AP。如果沒有，那這張卡就無法用於此用途。

---

## 二、Yupitek 銷售的 ALFA 產品線晶片一覽

| 型號 | 晶片組 | 驅動類型 | WiFi 標準 | Soft AP 支援 |
|------|--------|----------|-----------|-------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel（kernel 4.19+） | WiFi 5 AC1200 雙頻 | ✅ 完整支援 |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel（kernel 6.14+ 納入 in-kernel） | WiFi 5 AC1200 雙頻 | ⚠️ 有條件支援 |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel（kernel 5.18+，AP 模式 kernel 5.19+） | WiFi 6E AX3000 三頻 | ⚠️ 部分支援 |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel（同上） | WiFi 6E AX3000 三頻 | ⚠️ 部分支援 |
| AWUS036AX | Realtek RTL8832BU | Out-of-kernel（kernel 6.12+ 建議） | WiFi 6 AX1800 雙頻 | ❌ 不建議 |
| AWUS036AXER | Realtek RTL8832BU | Out-of-kernel（同上） | WiFi 6 AX1800 雙頻 | ❌ 不建議 |

> **備註**：AWUS036ACHM（MT7610U）已停產，Yupitek 產品頁面不再列出，本文以現售產品為主。

---

## 三、各型號 Soft AP 詳細分析

---

### 3.1 AWUS036ACM（MT7612U）— ⭐ Soft AP 最佳首選

**驅動**：`mt76x2u`，Linux kernel 4.19 起內建，零編譯、插上即用。

#### Soft AP 支援狀態：✅ 完整支援

AWUS036ACM 是 ALFA 現售產品中 **Soft AP 支援最完整、最穩定** 的選擇。

#### 核心優勢

- **WPA2 / WPA3 雙重支援**：MediaTek in-kernel 驅動原生支援 WPA3，安全性更有保障
- **VIF 虛擬介面支援**：可同時以 AP 模式 + Managed 模式 + Monitor 模式於同一張網卡運作，無需額外設備。這意味著你可以一邊分享網路，一邊同時監控無線頻譜
- **低耗電**：最大電流需求約 400mA，非常適合 Raspberry Pi（Pi 4 USB 子系統總供電僅 1200mA）
- **跨平台穩定性**：在 Kali Linux 2022.x–2025.x、Ubuntu 22.04/24.04、Debian 11/12、Raspberry Pi OS（Pi 3B+、4、5）均有大量成功案例

#### hostapd 正確設定範例（MT7612U）

以下為在 AWUS036ACM 上建立 5GHz AC Soft AP 的 `hostapd.conf`：

```ini
interface=wlan0
driver=nl80211
ssid=ALFA-ACM-AP
hw_mode=a
channel=36
wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0

wpa=2
wpa_passphrase=your_secure_password
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP

# MT7612U 專屬 HT/VHT capability 設定
ieee80211n=1
ieee80211ac=1
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
require_ht=1
require_vht=1
```

**常見錯誤提醒**：若 `ht_capab` 包含不符合 MT7612U 能力的旗標（尤其在 USB 2.0 埠上強制使用某些 HT40 設定時），hostapd 會直接崩潰。移除多餘的 capability 旗標即可解決。（來源：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)）

#### 社群評價

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. In my opinion, it is an outstanding USB WiFi adapter."
> — morrownr，GitHub USB-WiFi 知識庫維護者

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBay 使用者評論

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 討論串

---

### 3.2 AWUS036ACH（RTL8812AU）— Soft AP 可用，但有取捨

**驅動**：長期依賴社群維護的 aircrack-ng/rtl8812au out-of-kernel 驅動；kernel 6.14 起已合併 in-kernel 支援（rtw88 框架）。

#### Soft AP 支援狀態：⚠️ 有條件支援

#### 已知限制

1. **WPA3 不支援**：RTL8812AU 驅動雖宣稱支援 WPA3，但實際上無法正常運作，已有多位使用者確認。**只能使用 WPA2。**
2. **VIF 虛擬介面不支援**：無法同時跑 AP + Monitor 模式。如果需要同時做 AP 和監控，需要兩張網卡。
3. **驅動安裝較複雜**：Kali Linux 2025.x 下，最新版 aircrack-ng/rtl8812au 驅動有相容性問題，需回退至特定 commit（`63cf0b4`）才能正常運作。Kernel 6.14 後改用 in-kernel rtw88 驅動可能改善此問題。
4. **高耗電**：最大約 800mA，在 Raspberry Pi 上使用時需注意 USB 電源供應。

#### hostapd 設定範例（RTL8812AU）

```ini
interface=wlan0
driver=nl80211
ssid=ALFA-ACH-AP
hw_mode=a
channel=36
wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0

wpa=2
wpa_passphrase=your_secure_password
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP

# RTL8812AU 專屬 HT/VHT capability 設定
ieee80211n=1
ieee80211ac=1
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
```

#### 社群評價

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 使用者

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr 技術說明

#### 針對 ACH 的建議

若你已經擁有 AWUS036ACH，可以用於 Soft AP（單純建立熱點沒問題）。但如果你尚未購買且主要目的是 Soft AP，**請選 ACM**。

---

### 3.3 AWUS036AXML / AWUS036AXM（MT7921AUN）— 部分支援，需手動排除問題

AWUS036AXML 和 AWUS036AXM 是 WiFi 6E 三頻（2.4/5/6 GHz）產品，in-kernel 驅動 `mt7921u` 已列出 AP 模式支援，但實際回報問題較多。

#### Soft AP 支援狀態：⚠️ 部分支援，有已知韌體/驅動問題

#### AP 模式的 kernel 版本需求

| 模式 | 最低 kernel 版本 |
|------|-----------------|
| Managed（一般連線） | 5.18+ |
| **AP 模式** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO（Wi-Fi Direct AP） | 6.4+ |

#### 已知問題

1. **Bluetooth 衝突導致 WiFi 崩潰**：MT7921AUN 晶片同時整合 BT 5.2，在部分 kernel（6.6 以後至近期）存在 BT 子系統影響 WiFi 穩定性的問題。**解決方案：禁用 Bluetooth 驅動**

   ```bash
   echo "install btusb /bin/false" >> /etc/modprobe.d/local-dontload.conf
   ```

2. **韌體版本問題**：需安裝最新韌體（2024 年 11 月版）才能穩定運作。
3. **AP 模式下 Tx Power 顯示異常**：`iw` 顯示僅 3 dBm，無法調整，但實際上晶片有內建放大器，此為 kernel 驅動的顯示問題而非硬體限制。
4. **部分 kernel 版本下 monitor mode 異常**：截至 2025 年 12 月，kernel 6.18 及部分較早版本的 mt7921u 驅動有 monitor mode 問題。
5. **hostapd 版本需求**：部分使用者回報需要從 git 編譯最新版 hostapd 才能完整支援 AX 功能。

#### 韌體更新步驟（若系統韌體過舊）

```bash
# 從 kernel.org 下載最新 MediaTek 韌體
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### 社群評價

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — fhteagle，[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

#### 針對 AXML/AXM 的建議

如果你需要 WiFi 6E 的 6GHz 頻段掃描能力，且願意接受偶爾需要調整設定，可以選擇。**對穩定度要求高的生產環境 Soft AP，建議選 ACM。**

---

### 3.4 AWUS036AX / AWUS036AXER（RTL8832BU）— 不建議用於 Soft AP

這兩款使用 Realtek RTL8832BU 晶片，是 Multi-state 裝置（內建 Windows 驅動），需要用 USB mode switch 才能在 Linux 下正常運作。

#### Soft AP 支援狀態：❌ 不建議

主要問題：

1. **Multi-state 裝置**：增加部署複雜度，插上去不會直接變成網卡
2. **Monitor Mode 限制**：kernel 6.14 以下支援不完整
3. **Soft AP 社群案例極少**：相較於 MT7612U 和 RTL8812AU，RTL8832BU 用於 Soft AP 的實際案例幾乎找不到
4. **社群文件明確不推薦**：morrownr/USB-WiFi 將此晶片標記為「不建議用於 penetration testing」

> Yupitek 官方文章已明確指出：「AWUS036AX / AWUS036AXER 的 RTL8832BU 晶片在 kernel 6.14 以下有有限的 monitor mode 支援，不建議用於 penetration testing。」

---

## 四、各平台相容性矩陣

### AWUS036ACM（MT7612U）

| 平台 | Soft AP 支援 | 備註 |
|------|-------------|------|
| Kali Linux 2022.x – 2025.x | ✅ 完整支援 | 所有版本 kernel 5.x / 6.x，in-kernel，即插即用 |
| Ubuntu 22.04 / 24.04 | ✅ 完整支援 | 零設定 |
| Debian 11 / 12 | ✅ 完整支援 | 零設定 |
| Raspberry Pi 4（RPi OS） | ✅ 完整支援 | 最低耗電，morrownr 親自驗證 |
| Raspberry Pi 5（RPi OS） | ✅ 完整支援 | 與 Pi 4 相同驅動 |

### AWUS036ACH（RTL8812AU）

| 平台 | Soft AP 支援 | 備註 |
|------|-------------|------|
| Kali Linux 2022.x – 2025.x | ⚠️ 有條件支援 | 需安裝外部驅動；kernel 6.14+ 改善 |
| Ubuntu 22.04 / 24.04 | ⚠️ 有條件支援 | 可能需手動安裝驅動 |
| Debian 11 / 12 | ⚠️ 有條件支援 | 同上 |
| Raspberry Pi 4 | ⚠️ 注意電源 | 可運作，高耗電，建議有源 USB Hub |
| Raspberry Pi 5 | ⚠️ 注意電源 | 同上 |

### AWUS036AXML / AWUS036AXM（MT7921AUN）

| 平台 | Soft AP 支援 | 備註 |
|------|-------------|------|
| Kali Linux 2022.x（kernel 5.18+） | ✅ 支援，需禁 BT | 須更新韌體，禁用 btusb |
| Kali Linux 2024.x / 2025.x | ⚠️ 不穩定 | kernel 6.11+ 有 BT/WiFi 衝突 |
| Ubuntu 24.04（kernel 6.8+） | ⚠️ 部分問題 | morrownr 2024 年底報告有問題 |
| Ubuntu 25.04 / CachyOS（kernel 6.14+）| ✅ 即插即用 | 新版 kernel 改善明顯 |
| Raspberry Pi 4/5 | ⚠️ 有案例成功 | 需確認韌體版本 |

### AWUS036AX / AWUS036AXER（RTL8832BU）

| 平台 | Soft AP 支援 | 備註 |
|------|-------------|------|
| Kali Linux | ❌ 不建議 | Multi-state，mode switch 需求 |
| Ubuntu / Debian | ❌ 不建議 | 同上，Soft AP 實測案例極少 |
| Raspberry Pi 4/5 | ❌ 不建議 | 同上 |

---

## 五、Soft AP 完整設定步驟（AWUS036ACM）

以下以 AWUS036ACM 在 Raspberry Pi 4 上建立 5GHz Soft AP 為例，提供完整可執行的步驟。

### Step 1：確認網卡辨識與驅動

```bash
# 確認網卡已辨識
lsusb | grep MediaTek
# 預期輸出：Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# 檢查驅動已載入
dmesg | grep mt76
# 預期輸出：mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# 確認 AP 模式支援
iw list | grep -A 10 "Supported interface modes"
# 檢查輸出是否包含 "* AP"
```

### Step 2：安裝必要套件

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Step 3：設定 hostapd

建立 `/etc/hostapd/hostapd.conf`：

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a
channel=36

# WPA2 加密
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP

# HT/VHT 設定
ieee80211n=1
ieee80211ac=1
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
```

### Step 4：設定 dnsmasq（DHCP）

建立 `/etc/dnsmasq.conf`：

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Step 5：設定靜態 IP 與 NAT

```bash
# 為 wlan0 設定靜態 IP
sudo ip addr add 192.168.10.1/24 dev wlan0

# 啟用 IP 轉送
sudo sysctl net.ipv4.ip_forward=1

# 設定 NAT（假設 eth0 是上游網路介面）
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# 永久儲存 iptables 規則
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Step 6：啟動服務

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# 確認服務狀態
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# 讓 hostapd 開機自動啟動
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

完成後，用手機或筆電搜尋 WiFi，應該可以看到 `Yupitek_AP` 這個 SSID。

---

## 六、常見疑難排解

### Q1：hostapd 啟動後直接崩潰

**症狀**：`sudo systemctl status hostapd` 顯示 `exited` 或 `failed`

**可能原因**：`hostapd.conf` 中的 `ht_capab` 包含晶片不支援的能力旗標

**解法**：移除多餘的旗標。對 MT7612U（ACM）而言，使用本文第 3.1 節提供的設定檔是最安全的選擇。

---

### Q2：客戶端連線後無法上網

**症狀**：WiFi 已連線，取得 IP，但 ping 8.8.8.8 無回應

**檢查清單**：

```bash
# 1. 檢查 IP 轉送是否啟用
cat /proc/sys/net/ipv4/ip_forward
# 應輸出：1

# 2. 檢查 NAT 規則是否存在
sudo iptables -t nat -L POSTROUTING -v
# 應該能看到 MASQUERADE 規則

# 3. 確認上游網路介面是否正常
ping -I eth0 8.8.8.8
```

---

### Q3：5GHz AP 找不到或斷斷續續

**可能原因**：

1. **使用了 DFS 頻道（100–144）**：MT7612U 缺乏 DFS 支援，應使用 UNII-1 頻道（36–48）
2. **發射功率不足**：確認天線已正確鎖緊
3. **USB 供電不足**（Raspberry Pi）：使用官方 5A 電源或外接有源 USB Hub

---

### Q4：Raspberry Pi 上的 hostapd 一直重啟

**症狀**：`dmesg` 中出現大量 USB reset 訊息

**可能原因**：USB 埠供電不足（特別是 AWUS036ACH 高耗電晶片）

**解法**：
- 使用官方 Pi 5A 電源供應器
- 使用外部有源 USB Hub
- 將網卡插入 USB 3.0 埠（Pi 4 才有）

---

### Q5：AWUS036AXML/AXM 的 WiFi 突然斷線或無法啟動

**可能原因**：Bluetooth 子系統干擾 WiFi

**解法**：永久禁用藍牙驅動

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 七、重要技術議題

### VIF（虛擬介面）對 Soft AP 的價值

VIF 允許同一張網路卡同時以多種模式運作。以下是三種常見場景的需求分析：

| 場景 | 是否需要 VIF | 最佳網卡 |
|------|-------------|---------|
| 基本 NAT 路由（eth0 上游 + wlan AP） | ❌ 不需要 | 所有支援 AP 的即可 |
| 無線橋接（WiFi 接收 + WiFi AP 同時） | ✅ 需要 | ACM（MT7612U） |
| 監控 + AP 同時（安全研究） | ✅ 需要 | ACM（MT7612U） |

僅 MediaTek in-kernel 驅動（mt76x2u、mt7921u）完整支援 VIF。Realtek out-of-kernel 驅動基本上不支援。

---

### WPA3 支援狀況

| 晶片 | 對應型號 | WPA2 | WPA3 |
|------|---------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ |
| RTL8812AU | AWUS036ACH | ✅ | ❌ |
| RTL8832BU | AWUS036AX / AXER | ✅ | 未確認 |

---

### DFS（Dynamic Frequency Selection）與 5GHz 頻道選擇

DFS 頻道（ch100–ch140）需要 kernel 層面的 DFS 雷達偵測支援。MediaTek 的 MT7612U 缺乏 DFS 支援，因此在 5GHz AP 模式時建議使用 **非 DFS 頻道**：

| 頻段 | 建議頻道 | 原因 |
|------|---------|------|
| UNII-1 | **36, 40, 44, 48** | 全晶片支援，最安全 |
| UNII-2（DFS） | 52–144 | 大部分不支援，不建議 |
| UNII-3 | 149–165 | 部分支援（區域性） |

---

## 八、產品選購建議：哪張 ALFA 網卡適合你的 Soft AP 需求？

### 🥇 首選推薦 — AWUS036ACM（MT7612U）

**適合誰**：所有人，尤其如果你是第一次建立 Soft AP

- ✅ In-kernel 驅動，零編譯、即插即用
- ✅ WPA2 + WPA3 雙重支援
- ✅ VIF 虛擬介面，可同時多模式運作
- ✅ 低耗電（400mA），完美搭配 Raspberry Pi
- ✅ Kali / Ubuntu / Debian / RPi 全平台穩定

[查看產品頁面 →](https://yupitek.com/en/products/alfa/awus036acm/)

---

### 🥈 次要選擇 — AWUS036ACH（RTL8812AU）

**適合誰**：已擁有此型號的使用者

- ⚠️ 需要手動安裝驅動
- ⚠️ 僅支援 WPA2，不支援 WPA3
- ⚠️ 不支援 VIF
- ⚠️ 耗電較高（800mA），Raspberry Pi 需注意電源
- ✅ 單純建立熱點功能正常

[查看產品頁面 →](https://yupitek.com/en/products/alfa/awus036ach/)

---

### 🥉 謹慎選擇 — AWUS036AXML / AWUS036AXM（MT7921AUN）

**適合誰**：需要 WiFi 6E 6GHz 功能且願意處理已知問題的進階使用者

- ⚠️ BT/WiFi 干擾問題，需手動禁用藍牙
- ⚠️ 部分 kernel 版本不穩定
- ⚠️ 生產環境不建議
- ✅ WiFi 6E 三頻，最高速率

[查看產品頁面 →](https://yupitek.com/en/products/alfa/awus036axml/)

---

### ❌ 不建議用於 Soft AP — AWUS036AX / AWUS036AXER（RTL8832BU）

軟體 AP 用途缺乏社群驗證，Multi-state 裝置增加部署複雜度。如果需要 WiFi 6 速度但用途是 Soft AP，建議改選 AWUS036AXML。

---

## 九、真實案例摘要

### 案例 1：Raspberry Pi 4B + AWUS036ACM 家用雙頻 AP

**來源**：morrownr GitHub 7612u repo
**場景**：RPi4B 作為家用 5GHz AP，搭配內建 2.4GHz 提供雙頻服務
**結果**：長期穩定運作，「outstanding」評價
**配置**：hostapd + dnsmasq + NAT

### 案例 2：RPi3B+ + ACM hostapd 崩潰後成功修復

**來源**：[GitHub issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**問題**：hostapd 崩潰，原因為 `ht_capab` 包含不支援的旗標
**解決**：移除多餘旗標（USB 2.0 限制下部分 HT40 設定不可用），在 Kali 上成功啟動

### 案例 3：Pi PwnBox RogueAP 使用 ACH 跑 AP

**來源**：GitHub koutto/pi-pwnbox-rogueap
**場景**：紅隊滲透測試，RPi3B+ 同時使用兩張 Alfa 網卡分工（一張 AP、一張攻擊）
**結果**：RTL8812AU 跑 AP 模式成功，但因不支援 VIF，需要兩張卡分工

### 案例 4：AXML 在 RPi3B ArchLinux 上穩定運作

**來源**：[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**評語**：「It's the most stable mt7921 in my collection.」
**備註**：需從 git 編譯最新版 hostapd 才能完整支援 AX 功能

---

## 結語：Soft AP，選對晶片就是選對一切

建立 Soft AP 的核心關鍵，不在於 WiFi 速率有多快，也不在於天線有幾根——**真正的關鍵，是晶片驅動對 AP 模式的支援程度。**

在我們調查的所有 ALFA 產品中，**AWUS036ACM（MT7612U）** 是唯一一張同時滿足「in-kernel 驅動、WPA3、VIF、低耗電、全平台穩定」的選擇。它是 Soft AP 的金標準。

AWUS036ACH（RTL8812AU）可以用，但你需要接受一些限制。AWUS036AXML/AXM（MT7921AUN）潛力很大，但目前仍有驅動成熟度問題需要時間解決。而 AWUS036AX/AXER（RTL8832BU），我們不建議你用於此用途。

如果你是第一次嘗試在 Raspberry Pi 或 Kali Linux 上建立 Soft AP，**選 ACM，你不會後悔。**

---

### 購買連結

- [AWUS036ACM — Soft AP 首選](https://yupitek.com/en/products/alfa/awus036acm/)
- [AWUS036ACH — 經典滲透測試卡](https://yupitek.com/en/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E 三頻旗艦](https://yupitek.com/en/products/alfa/awus036axml/)
- [ALFA Network 全系列產品](https://yupitek.com/en/products/category/alfa-network/)

### 延伸閱讀

- [AWUS036ACH vs AWUS036ACM：晶片驅動方式完整比較](https://yupitek.com/en/blog/awus036ach-vs-awus036acm/)
- [Best WiFi Adapters for Kali Linux in 2026](https://yupitek.com/en/blog/best-wifi-adapters-kali-linux-2026/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](https://yupitek.com/en/blog/)
- [morrownr/USB-WiFi — 最權威的 Linux USB WiFi 知識庫](https://github.com/morrownr/USB-WiFi)
- [morrownr/7612u — MT7612U 專屬文件](https://github.com/morrownr/7612u)

---

> **標籤**：#ALFANetwork #SoftAP #hostapd #KaliLinux #RaspberryPi #USBWiFi #AWUS036ACM #Yupitek
>
> **作者**：榆閤科技 (Yupitek Ltd) — ALFA Network 台灣授權代理商
>
> **免責聲明**：本文研究資料截至 2026 年 5 月。Linux Kernel 與各發行版持續更新，驅動支援狀況可能隨版本變動。部署前建議確認目標平台的 kernel 版本與驅動相容性。
>
> **技術支援**：如有 Soft AP 設定問題，歡迎聯繫榆閤科技台灣本地技術支援團隊。
