---
title: "ALFA 網路卡 Soft AP 完整指南 2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5 建立 WiFi 熱點"
description: "深度調查 ALFA Network USB 無線網卡在 Kali Linux、Ubuntu、Debian、Raspberry Pi 4 與 Pi 5 上使用 Soft AP（WiFi Hotspot / hostapd）的完整相容性。涵蓋 AWUS036ACM、AWUS036ACH、AWUS036AXML 詳細設定、社群反饋、常見疑難排解與產品選購建議。"
date: 2026-05-22
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi", "USB-無線網路卡", "樹莓派-WiFi-熱點"]
---


# ALFA 網路卡 Soft AP 完整指南 2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5 建立 WiFi 熱點

## 前言

> 「ALFA 的 USB 無線網路卡，可以在 Kali Linux / Ubuntu / Raspberry Pi 上當 WiFi 熱點（Soft AP）用嗎？」

這是榆閤科技最常收到的客戶詢問之一。問題聽起來簡單，但答案因型號和晶片組的不同而大相逕庭——**不是每一張 USB 無線網卡都能跑 Soft AP。**

本文彙整 GitHub 上超過 500 則社群討論（morrownr/USB-WiFi 知識庫）、Reddit 技術論壇、Raspberry Pi 官方論壇紀錄，以及實際使用者反饋，給出一份誠實、完整的調查報告，告訴你哪些 ALFA 網卡適合、哪些不適合，以及從頭到尾的完整設定步驟。

---

## 一、什麼是 Soft AP？Linux 如何運作 {#what-is-softap}

**Soft AP（Software Access Point，軟體存取點）** 是指透過軟體（主要是 **hostapd**），將一張普通的 USB 無線網路卡變成無線基地台（Access Point），讓其他裝置（手機、筆電、IoT 設備）可以連上網路，不需要購買專用路由器或 AP 硬體。

這個功能在以下場景中極其實用：

- **旅行 / 家用路由器**：出差或露營時，筆電或 Raspberry Pi 插上 ALFA 網卡，立刻變成隨身 WiFi 熱點
- **滲透測試練習環境**：在隔離環境中建立 Rogue AP 進行安全研究
- **IoT 設備中繼**：在訊號死角建立中繼站，讓感測器回傳資料
- **邊緣 AI 部署**：工業場景中沒有有線網路，需要讓設備作為熱點讓其他裝置連入
- **災難應變通訊**：斷網時快速建立臨時通訊網路

### Linux Soft AP 的四大核心元件

| 元件 | 功能 |
|------|------|
| **hostapd** | 建立無線基地台的核心程式，負責管理 SSID、認證、加密 |
| **nl80211** | Linux 無線子系統標準介面，驅動必須支援此框架才能與 hostapd 協作 |
| **dnsmasq** | DHCP 伺服器，自動為連線裝置分配 IP 位址 |
| **iptables / nftables** | 網路位址轉換（NAT），讓連線裝置共享上游網路 |

### 關鍵概念：Master Mode

**Master Mode**（又稱 AP Mode、Infrastructure Mode）是晶片驅動層面的能力。如果驅動不支援 Master Mode，hostapd 就無法啟動——無論你的設定多完美都沒用。

驗證一張網路卡是否支援 AP 模式：

```bash
iw list | grep -A 10 "Supported interface modes"
```

如果輸出中包含 `* AP`，代表該網卡的驅動支援 Soft AP。如果沒有，那這張卡就無法用於此用途。

### 💡 In-kernel vs Out-of-kernel 驅動

這是選擇 Soft AP 網卡時**最重要**的概念：

| 類型 | 說明 | 對 Soft AP 的影響 |
|------|------|------------------|
| **In-kernel 驅動** | 已被合併進 Linux 官方原始碼，系統開機即自動載入，無需手動安裝 | ✅ 長期穩定，kernel 升級後仍可使用 |
| **Out-of-kernel 驅動** | 需自行從 GitHub 下載、編譯，kernel 升級後可能需要重新編譯 | ⚠️ 每次 kernel 更新都可能失效 |

**對 Soft AP 的長期穩定性而言，in-kernel 驅動遠優於 out-of-kernel。**

---

## 二、ALFA 產品線與晶片速覽 {#product-lineup}

以下是 Yupitek 目前銷售的 ALFA 網路卡型號、核心晶片與 Soft AP 初步評級：

| 型號 | 晶片組 | 驅動類型 | WiFi 標準 | Soft AP 評級 |
|------|--------|----------|-----------|-------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel（kernel 4.19+） | WiFi 5 AC1200 雙頻 | ✅ 完整支援 |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel（kernel 6.14+ 納入 in-kernel） | WiFi 5 AC1200 雙頻 | ⚠️ 有條件支援 |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel（kernel 5.18+，AP 模式 5.19+） | WiFi 6E AX3000 三頻 | ⚠️ 部分支援 |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel（同上） | WiFi 6E AX3000 三頻 | ⚠️ 部分支援 |
| AWUS036AX | Realtek RTL8832BU | Out-of-kernel（kernel 6.12+ 建議） | WiFi 6 AX1800 雙頻 | ❌ 不建議 |
| AWUS036AXER | Realtek RTL8832BU | Out-of-kernel（同上） | WiFi 6 AX1800 雙頻 | ❌ 不建議 |

> **備註**：AWUS036ACHM（MT7610U）已停產，Yupitek 產品頁面不再列出。本文以現售產品為主。

---

## 三、AWUS036ACM（MT7612U）— ⭐ Soft AP 最佳首選 {#acm}

### Soft AP 支援狀態：✅ 完整支援

MT7612U 是目前 ALFA 現售產品中，Soft AP 表現最穩定的晶片。它的驅動 `mt76x2u` 早在 2018 年（kernel 4.19）就進入 Linux 官方 kernel，意味著只要你的系統夠新，**插上去就能用**——不需要 `git clone`，不需要 `dkms`，不需要在 kernel 升級後重新編譯。

### 核心優勢

- **WPA2 + WPA3 雙重支援**：MediaTek in-kernel 驅動原生支援 WPA3 SAE，是 Realtek 驅動無法比擬的優勢
- **VIF 虛擬介面支援**：同一張卡可同時以 AP + Managed + Monitor 三種模式並行，無需額外添購第二張卡。你可以一邊分享網路，一邊同時監控無線頻譜
- **超低耗電**：最大約 400mA，非常適合 Raspberry Pi（Pi 4 USB 子系統總供電僅 1200mA）
- **全平台相容**：在 Kali Linux 2022.x–2025.x、Ubuntu 22.04/24.04、Debian 11/12、Raspberry Pi OS（Pi 3B+、4、5）均有大量成功案例

### hostapd 正確設定範例（MT7612U 專用）

以下是社群（morrownr/USB-WiFi）多年測試確認的能力旗標，**必須完全對應 MT7612U 的實際硬體能力**：

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz；改為 g 則使用 2.4GHz
channel=36                    # UNII-1，非 DFS，最安全的選擇
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U 正確的 HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # channel 36 對應的中心頻道索引

# 安全性：WPA2 + WPA3 混合模式
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 雙支援
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ 最常見錯誤

若 `ht_capab` 包含 MT7612U 不支援的能力旗標（尤其在 USB 2.0 埠上強制使用某些 HT40 設定時），hostapd 會直接崩潰退出，錯誤訊息非常不明顯。**請務必只使用上方確認的旗標組合**，不要複製其他晶片（如 RTL8812AU）的設定。（來源：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)）

### 社群真實評價

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> — **morrownr**，GitHub morrownr/7612u（Linux USB WiFi 最具權威的社群知識庫維護者）

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBay 使用者評論

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 討論串

---

## 四、AWUS036ACH（RTL8812AU）— 可用，但有限制 {#ach}

### Soft AP 支援狀態：⚠️ 有條件支援

RTL8812AU 是 ALFA 最具知名度的滲透測試晶片，長期以來是 Kali Linux 社群的最愛。它的 Soft AP 功能確實存在——單純建立熱點可以正常運作——但 Realtek 的 out-of-kernel 驅動架構帶來幾個長期限制：

### 已知限制清單

1. **WPA3 不支援**：RTL8812AU 驅動雖然在介面上顯示支援 WPA3，但多名使用者確認實際上無法運作，**只能使用 WPA2-PSK**
2. **VIF 虛擬介面不支援**：無法同時在同一張卡上跑 AP + Monitor 模式。需要 AP 兼監控時，必須使用兩張不同的網路卡分工
3. **Kali Linux 2025.x 驅動問題**：最新版 Kali 的 aircrack-ng/rtl8812au 驅動有相容性問題，需回退至特定的舊版 commit（`63cf0b4`）才能正常運作。Kernel 6.14+ 的 in-kernel rtw88 驅動有望改善此問題
4. **高耗電**：最大約 800mA，在 Raspberry Pi 上若同時連接多個 USB 裝置，可能導致系統不穩定，建議使用有源 USB Hub

### hostapd 設定範例（RTL8812AU）

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# 注意：與 MT7612U 的 capabilities 完全不同！
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# 安全性：只能用 WPA2，WPA3 不要加
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### 安裝驅動（Kali Linux / Ubuntu / Debian）

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x 需要指定舊版 commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### 社群評價

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 使用者

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr 技術說明

### 針對 ACH 的建議

若你已經擁有 AWUS036ACH，可以用於 Soft AP（單純建立熱點沒問題）。但如果你尚未購買且主要目的是 Soft AP，**請選 ACM**。

---

## 五、AWUS036AXML / AWUS036AXM（MT7921AUN）— 謹慎選擇 {#axml}

### Soft AP 支援狀態：⚠️ 部分支援，有已知韌體/驅動問題

AWUS036AXML 與 AWUS036AXM 是 ALFA 的 WiFi 6E 三頻旗艦，能覆蓋 2.4 GHz、5 GHz 和全新的 6 GHz 頻段。它的 in-kernel 驅動 `mt7921u` 從 kernel 5.18 起就已內建，AP 模式支援則在 kernel 5.19 正式加入。然而，MT7921AUN 晶片同時整合了 Bluetooth 5.2，這成為了 2024–2025 年社群最頭疼的問題根源。

### AP 模式支援的 kernel 版本里程碑

| 模式 | 最低 kernel 版本 |
|------|-----------------|
| Managed（一般連線） | 5.18+ |
| **AP 模式（Soft AP）** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO（Wi-Fi Direct AP） | 6.4+ |

### 已知問題與解決方案

#### 問題一：Bluetooth 干擾導致 WiFi 崩潰

在 kernel 6.6 以後的版本，BT 子系統的變動導致 mt7921u 的 WiFi 功能偶發崩潰，重現率因系統環境而異。**目前最有效的解決方案是禁用 btusb 驅動：**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### 問題二：韌體版本過舊

若系統的 MediaTek 韌體過舊，網路卡可能無法被正確識別。需安裝 2024 年 11 月以後的最新韌體：

```bash
# 確認當前韌體版本
dmesg | grep "WM Firmware"
# 應顯示：Build Time: 20241106151045 或更新

# 若版本過舊，從 kernel.org 下載更新
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### 問題三：hostapd 版本需求

部分使用者回報需要從 git 編譯最新版 hostapd 才能完整支援 WiFi 6 AP 功能，系統套件管理器安裝的版本可能不完整。

#### 問題四：AP 模式下 Tx Power 顯示異常

`iw` 顯示僅 3 dBm，無法調整，但實際上晶片有內建放大器，此為 kernel 驅動的顯示問題而非硬體限制。

#### 問題五：部分 kernel 版本下 monitor mode 異常

截至 2025 年 12 月，kernel 6.18 及部分較早版本的 mt7921u 驅動有 monitor mode 問題。

### 社群評價

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — **fhteagle**，[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### 針對 AXML/AXM 的建議

如果你需要 WiFi 6E 的 6GHz 頻段功能，且願意接受偶爾需要調整設定，可以選擇。**對穩定度要求高的生產環境 Soft AP，建議選 ACM。**

---

## 六、AWUS036AX / AWUS036AXER（RTL8832BU）— 不建議用於 Soft AP {#ax}

### Soft AP 支援狀態：❌ 不建議

AWUS036AX 和 AWUS036AXER 雖然是 WiFi 6 規格，但 RTL8832BU 晶片是所謂的「multi-state」裝置——出廠預設以 USB 大量儲存模式枚舉，Linux 需要先做 USB mode switch 才能切換為無線網路卡模式。

**主要問題：**

1. **Multi-state 裝置**：增加部署複雜度，插上去不會直接變成網卡
2. **Monitor Mode 限制**：kernel 6.14 以下支援不完整
3. **Soft AP 社群案例極少**：相較於 MT7612U 和 RTL8812AU，RTL8832BU 用於 Soft AP 的實際案例幾乎找不到
4. **社群文件明確不推薦**：morrownr/USB-WiFi 將此晶片標記為「不建議用於 penetration testing」

> Yupitek 官方文章已明確指出：「AWUS036AX / AWUS036AXER 的 RTL8832BU 晶片在 kernel 6.14 以下有有限的 monitor mode 支援，不建議用於 penetration testing，請改用 AWUS036ACH 或 AWUS036AXML。」

---

## 七、各平台相容性總表 {#compat-matrix}

### AWUS036ACM（MT7612U）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel，即插即用，kernel 5.x / 6.x 均適用 |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel，零設定，建議使用 LTS 版 |
| Debian 11 / 12 | ✅ | In-kernel，穩定 |
| Raspberry Pi 4（RPi OS） | ✅ | 最低耗電（400mA），morrownr 長期驗證。Pi 4 USB 3.0 埠效能更佳 |
| Raspberry Pi 5（RPi OS） | ✅ | 與 Pi 4 相同驅動，穩定 |

### AWUS036ACH（RTL8812AU）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux 2022.x – 2025.x | ⚠️ | 需安裝外部驅動；2025.x 需用舊版 commit `63cf0b4`。Kernel 6.14+ 後 in-kernel rtw88 有望改善 |
| Ubuntu 22.04 / 24.04 | ⚠️ | 需手動安裝 rtw88 或 aircrack-ng 社群驅動 |
| Debian 11 / 12 | ⚠️ | 同上 |
| Raspberry Pi 4 | ⚠️ | 可運作，但高耗電（800mA），建議有源 USB Hub |
| Raspberry Pi 5 | ⚠️ | 同上，Pi 5 USB controller 差異可能有不同表現 |

### AWUS036AXML / AWUS036AXM（MT7921AUN）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux 2022.x（kernel 5.18+） | ✅ | 需禁用 btusb，需更新韌體 |
| Kali Linux 2024.x / 2025.x | ⚠️ | Kernel 6.11+ BT/WiFi 衝突問題，不穩定 |
| Ubuntu 24.04（kernel 6.8+） | ⚠️ | 2024 年底有問題回報 |
| Ubuntu 25.04 / CachyOS（kernel 6.14+） | ✅ | 即插即用，新版 kernel 改善明顯 |
| Debian 12 | ⚠️ | 視 kernel 版本而定 |
| Raspberry Pi 4 / 5 | ⚠️ | 有成功案例，但需確認韌體版本並禁用 BT |

### AWUS036AX / AWUS036AXER（RTL8832BU）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux | ❌ | Multi-state，需 USB mode switch，社群案例極少 |
| Ubuntu / Debian | ❌ | 同上 |
| Raspberry Pi 4 / 5 | ❌ | 同上 |

---

## 八、Soft AP 完整設定步驟（AWUS036ACM）{#setup-guide}

以下以 AWUS036ACM 在 Raspberry Pi 4 上建立 5GHz Soft AP 為例，提供從頭到尾的完整步驟。

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
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1 非 DFS，最安全
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT 設定（MT7612U 專用）
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 混合模式
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
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

## 九、常見疑難排解 {#troubleshooting}

### Q1：hostapd 啟動後直接崩潰

**症狀**：`sudo systemctl status hostapd` 顯示 `exited` 或 `failed`

**可能原因**：`hostapd.conf` 中的 `ht_capab` 包含晶片不支援的能力旗標

**解法**：移除多餘的旗標。對 MT7612U（ACM）而言，使用本文第 3 節提供的設定檔是最安全的選擇。**不要複製其他晶片的 ht_capab 設定。**

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

1. **使用了 DFS 頻道（100–144）**：MT7612U / MT7610U 缺乏 DFS 支援，應使用 UNII-1 頻道（36–48）
2. **發射功率不足**：確認天線已正確鎖緊於 RP-SMA 接頭
3. **USB 供電不足**（Raspberry Pi）：使用官方 5A 電源或外接有源 USB Hub

---

### Q4：Raspberry Pi 上的 hostapd 一直重啟

**症狀**：`dmesg` 中出現大量 USB reset 訊息

**可能原因**：USB 埠供電不足（特別是 AWUS036ACH 高耗電晶片，最大 800mA）

**解法**：
- 使用官方 Pi 5A 電源供應器
- 使用外部有源 USB Hub
- 將網卡插入 USB 3.0 埠（Pi 4 才有）

---

### Q5：AWUS036AXML/AXM 的 WiFi 突然斷線或無法啟動

**可能原因**：Bluetooth 子系統干擾 WiFi（MT7921AUN 內建 BT 5.2）

**解法**：永久禁用藍牙驅動

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 十、技術深入：VIF、WPA3、DFS 頻道 {#technical}

### VIF（虛擬介面）：一張卡同時做多件事

VIF（Virtual Interface）讓同一張物理網路卡可以同時以多個邏輯介面運作。例如：一個介面連上游路由器（managed 模式），同時另一個介面作為 AP（master 模式）供其他裝置連入。

三種常見場景的需求分析：

| 場景 | 是否需要 VIF | 最佳網卡 |
|------|-------------|---------|
| 基本 NAT 路由（eth0 上游 + wlan AP） | ❌ 不需要 | 所有支援 AP 的即可 |
| 無線橋接（WiFi 接收 + WiFi AP 同時） | ✅ 需要 | ACM（MT7612U） |
| 監控 + AP 同時（安全研究 / Rogue AP） | ✅ 需要 | ACM（MT7612U） |

**VIF 實戰範例（MT7612U）：**

```bash
# 在現有 wlan1 之外建立額外的 AP 虛擬介面
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# 現在 wlan1 可以連上游網路，ap0 跑 hostapd
```

僅 MediaTek in-kernel 驅動（mt76x2u、mt7921u）完整支援 VIF。Realtek out-of-kernel 驅動基本上無此能力，若需要 AP + Monitor 同時運作，必須使用兩張不同的網路卡。

---

### WPA3 支援對照表

| 晶片 | 對應型號 | WPA2 | WPA3 |
|------|---------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ 原生支援 SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ 原生支援 SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ 宣稱支援但實際無效 |
| RTL8832BU | AWUS036AX / AXER | ✅ | ⚠️ 未確認 |

---

### 5GHz Soft AP 的頻道選擇：避開 DFS

DFS（Dynamic Frequency Selection）頻道（ch100–ch140）需要 kernel 層面的雷達偵測機制。MT7612U 等晶片缺乏 DFS 支援，使用 5GHz AP 時應選擇：

| 頻段 | 建議頻道 | 原因 |
|------|---------|------|
| **UNII-1** | **36, 40, 44, 48** | 全晶片支援，最安全的選擇 |
| UNII-2（DFS） | 52–144 | 大部分不支援，不建議 |
| UNII-3 | 149–165 | 部分支援（依地區法規） |

---

## 十一、社群真實案例整理 {#real-cases}

### 案例 1：RPi4B + AWUS036ACM = 長期穩定家用 5GHz AP

**來源**：morrownr/7612u GitHub 知識庫
**場景**：morrownr 長期以 RPi4B + AWUS036ACM 作為家用 5GHz AP，搭配 Pi 內建 2.4GHz 提供雙頻服務
**結果**：長期穩定運作，無需重啟，「outstanding」評價
**配置**：hostapd + dnsmasq + iptables NAT

### 案例 2：RPi3B+ + ACM — 初始崩潰，調整後成功

**來源**：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**問題**：在 RPi3B+ 上以 USB 2.0 埠執行，hostapd 崩潰
**根本原因**：`ht_capab` 包含 USB 2.0 頻寬限制下不支援的 HT40 設定旗標
**解決**：移除多餘旗標後，在 Kali Linux 上成功啟動

### 案例 3：Pi PwnBox + AWUS036ACH = 紅隊測試 Rogue AP

**來源**：GitHub koutto/pi-pwnbox-rogueap
**場景**：以 RPi3B+ 建立 Rogue AP 平台：一張 RTL8812AU（AWUS036ACH）負責跑 AP，另一張 RT3070（AWUS036NEH）負責封包注入攻擊
**關鍵發現**：因 RTL8812AU 不支援 VIF，必須使用兩張卡分工（而非像 ACM 可以單卡搞定）

### 案例 4：AWUS036AXML 在 RPi3B ArchLinux ARM 上穩定跑 AP

**來源**：[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**場景**：使用者在 RPi3B ArchLinux aarch64 上成功跑 AWUS036AXML AP 模式
**評語**：「It's the most stable mt7921 in my collection.」
**關鍵條件**：從 git 編譯最新版 hostapd，並禁用 btusb

### 案例 5：AWUS036ACHM（MT7610U，已停產）在 Pi4 上達到全速 AP

**來源**：[GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**問題**：初始配置只達 65 Mbps link speed，未達 AC 5GHz 全速
**解決**：加入正確的 `vht_oper_chwidth=1` 和 `vht_oper_centr_freq_seg0_idx` 設定後達到 433 Mbps link rate
**對於 ACM 的啟示**：同樣的 VHT 參數設定對 MT7612U（ACM）也至關重要

---

## 十二、選購建議與最終結論 {#recommendations}

### 快速決策指南

| 推薦等級 | 型號 | 適合對象 | 一句話總結 |
|---------|------|---------|-----------|
| 🥇 **首選** | **AWUS036ACM** | 所有人，尤其第一次建立 Soft AP | 全平台穩定，零煩惱 |
| 🥈 有條件可用 | AWUS036ACH | 已擁有此型號的使用者 | 需裝驅動，無 WPA3 |
| 🥉 進階選擇 | AWUS036AXML | 需要 WiFi 6E 且願意花時間調校 | 6GHz 優勢，需手動排除問題 |
| ❌ 不建議 | AWUS036AX / AXER | N/A | Soft AP 未經社群驗證 |

### 🎯 簡明決策指南

- **需要在 Kali Linux / Ubuntu / Debian / Raspberry Pi 4 或 5 上建立穩定 Soft AP？**
  → 直接選 **AWUS036ACM**，沒有之一。

- **已有 AWUS036ACH，想測試 Soft AP？**
  → 可以用，但只支援 WPA2，且需要安裝驅動。接受這些限制的話沒問題。

- **需要 WiFi 6E（6GHz 頻段）且願意花時間設定？**
  → AWUS036AXML，記得禁用 BT 驅動、確認 kernel ≥ 6.6 LTS。

- **主要目的是 Soft AP 而非滲透測試？**
  → AWUS036ACM 是唯一在所有平台上均有大量驗證案例的選擇。

---

### 結語

建立 Soft AP 的核心關鍵，不在於 WiFi 速率有多快，也不在於天線有幾根——**真正的關鍵，是晶片驅動對 AP 模式的支援程度。**

在我們調查的所有 ALFA 產品中，**AWUS036ACM（MT7612U）** 是唯一同時滿足「in-kernel 驅動、WPA3 原生支援、VIF 虛擬介面、低耗電、全平台穩定」的選擇。morrownr 親測、GitHub 社群驗證、eBay 使用者背書——ACM 是 Soft AP 用途中，你唯一不會後悔的選擇。

AWUS036ACH（RTL8812AU）可以用，但需要接受 WPA3 不支援和驅動維護成本。AWUS036AXML/AXM（MT7921AUN）潛力很大，但目前驅動成熟度仍在路上。AWUS036AX/AXER（RTL8832BU），不建議用於 Soft AP。

**如果你是第一次嘗試在 Raspberry Pi 或 Kali Linux 上建立 Soft AP——選 ACM。**

---

### 購買連結

- [AWUS036ACM — Soft AP 首選](/zh-tw/products/alfa/awus036acm/)
- [AWUS036ACH — 經典滲透測試卡](/zh-tw/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E 三頻旗艦](/zh-tw/products/alfa/awus036axml/)
- [ALFA Network 全系列產品](/zh-tw/products/alfa/)

### 延伸閱讀

- [AWUS036ACH vs AWUS036ACM：晶片驅動方式完整比較](/zh-tw/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](/zh-tw/blog/)
- [morrownr/USB-WiFi — 最權威的 Linux USB WiFi 知識庫](https://github.com/morrownr/USB-WiFi)（4,100+ stars）
- [morrownr/7612u — MT7612U 專屬文件（含 RPi4B Bridged AP 完整教學）](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi 自動整理知識庫](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 資料來源

本文資料彙整自：
- **morrownr/USB-WiFi** GitHub 知識庫（4,100+ stars）及完整的 iw_list 記錄
- **morrownr/7612u** — MT7612U Bridged AP on RPi4B 完整教學
- **GitHub issue tracker** — issue #2（ACM AP 設定）、#476（AXML AP 測試）、Discussion #31（ACHM 全速 AP）
- **koutto/pi-pwnbox-rogueap** — Alfa 網卡 RogueAP 實戰案例
- **Rokland** 授權零售商 Linux 支援頁面
- **Lab401** 技術評測與 2025 滲透測試最佳選擇報告
- **Raspberry Pi 官方論壇** — Pi 4/5 USB WiFi 相容性討論
- **Yupitek 現有部落格** — ACM China Install Guide、AXML WiFi 6E Review、Kali Linux 2026 最佳網卡

---

> **標籤**：#ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi4 #RaspberryPi5 #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #LinuxWiFiAP #USB無線網路卡 #樹莓派WiFi熱點 #Yupitek
>
> **作者**：榆閤科技 (Yupitek Ltd) — ALFA Network 台灣授權總代理
>
> **免責聲明**：本文研究資料截至 2026 年 5 月。Linux Kernel 與各發行版持續更新，驅動支援狀況可能隨版本變動。部署前建議確認目標平台的 kernel 版本與驅動相容性。
>
> **技術支援**：如有 Soft AP 設定問題，歡迎聯繫榆閤科技台灣本地技術支援團隊。產品購買與諮詢請至 [yupitek.com](/zh-tw/)。
