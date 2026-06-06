---

title: "ALFA 网络卡 Soft AP 完整指南 2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5 建立 WiFi 热点"
description: "深度调查 ALFA Network USB 无线网卡在 Kali Linux、Ubuntu、Debian、Raspberry Pi 4 与 Pi 5 上使用 Soft AP（WiFi Hotspot / hostapd）的完整兼容性。涵盖 AWUS036ACM、AWUS036ACH、AWUS036AXML 详细设置、社群反馈、常见疑难排解与产品选购建议。"
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi", "USB-无线网络卡", "树莓派-WiFi-热点"]

featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
---


# ALFA 网络卡 Soft AP 完整指南 2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5 建立 WiFi 热点

## 前言

> 「ALFA 的 USB 无线网络卡，可以在 Kali Linux / Ubuntu / Raspberry Pi 上当 WiFi 热点（Soft AP）用嗎？」

这是榆合科技最常收到的客户詢問之一。问题听起来简单，但答案因型號和芯片组的不同而大相逕庭——**不是每一张 USB 无线网卡都能跑 Soft AP。**

本文汇整 GitHub 上超过 500 则社群讨论（morrownr/USB-WiFi 知識庫）、Reddit 技术論壇、Raspberry Pi 官方論壇紀錄，以及实际用户反馈，给出一份誠實、完整的调查报告，告訴你哪些 ALFA 网卡適合、哪些不適合，以及从头到尾的完整设置步驟。

---

## 一、什麼是 Soft AP？Linux 如何運作 {#what-is-softap}

**Soft AP（Software Access Point，软件存取点）** 是指透过软件（主要是 **hostapd**），将一张普通的 USB 无线网络卡變成无线基地台（Access Point），让其他设备（手機、筆電、IoT 設備）可以連上网络，不需要购买專用路由器或 AP 硬件。

这个功能在以下場景中極其實用：

- **旅行 / 家用路由器**：出差或露營時，筆電或 Raspberry Pi 插上 ALFA 网卡，立刻變成隨身 WiFi 热点
- **渗透测试練習环境**：在隔離环境中建立 Rogue AP 進行安全研究
- **IoT 設備中繼**：在信号死角建立中繼站，让感測器回傳資料
- **邊緣 AI 部署**：工业場景中没有有有线网络，需要让設備作为热点让其他设备連入
- **災難應變通訊**：斷网時快速建立臨時通訊网络

### Linux Soft AP 的四大核心组件

| 组件 | 功能 |
|------|------|
| **hostapd** | 建立无线基地台的核心程式，負責管理 SSID、认证、加密 |
| **nl80211** | Linux 无线子系统標準接口，驱动必須支持此框架才能与 hostapd 協作 |
| **dnsmasq** | DHCP 伺服器，自動为连接设备分配 IP 位址 |
| **iptables / nftables** | 网络位址轉換（NAT），让连接设备共享上游网络 |

### 关鍵概念：Master Mode

**Master Mode**（又称 AP Mode、Infrastructure Mode）是芯片驱动层面的能力。如果驱动不支持 Master Mode，hostapd 就无法启动——无論你的设置多完美都没有用。

验证一张网络卡是否支持 AP 模式：

```bash
iw list | grep -A 10 "Supported interface modes"
```

如果输出中包含 `* AP`，代表該网卡的驱动支持 Soft AP。如果没有有，那这张卡就无法用於此用途。

### 💡 In-kernel vs Out-of-kernel 驱动

这是选择 Soft AP 网卡時**最重要**的概念：

| 类型 | 说明 | 对 Soft AP 的影響 |
|------|------|------------------|
| **In-kernel 驱动** | 已被合併進 Linux 官方源代码，系统开機即自動加载，无需手動安装 | ✅ 长期稳定，kernel 升級后仍可使用 |
| **Out-of-kernel 驱动** | 需自行从 GitHub 下載、编译，kernel 升級后可能需要重新编译 | ⚠️ 每次 kernel 更新都可能失效 |

**对 Soft AP 的长期稳定性而言，in-kernel 驱动远優於 out-of-kernel。**

---

## 二、ALFA 产品线与芯片速覽 {#product-lineup}

以下是 Yupitek 目前销售的 ALFA 网络卡型號、核心芯片与 Soft AP 初步評級：

| 型號 | 芯片组 | 驱动类型 | WiFi 標準 | Soft AP 評級 |
|------|--------|----------|-----------|-------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel（kernel 4.19+） | WiFi 5 AC1200 双频 | ✅ 完整支持 |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel（kernel 6.14+ 納入 in-kernel） | WiFi 5 AC1200 双频 | ⚠️ 有条件支持 |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel（kernel 5.18+，AP 模式 5.19+） | WiFi 6E AX3000 三频 | ⚠️ 部分支持 |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel（同上） | WiFi 6E AX3000 三频 | ⚠️ 部分支持 |
| AWUS036AX | Realtek RTL8832BU | Out-of-kernel（kernel 6.12+ 建议） | WiFi 6 AX1800 双频 | ❌ 不建议 |
| AWUS036AXER | Realtek RTL8832BU | Out-of-kernel（同上） | WiFi 6 AX1800 双频 | ❌ 不建议 |

> **備註**：AWUS036ACHM（MT7610U）已停產，Yupitek 产品页面不再列出。本文以現售产品为主。

---

## 三、AWUS036ACM（MT7612U）— ⭐ Soft AP 最佳首选 {#acm}

### Soft AP 支持状态：✅ 完整支持

MT7612U 是目前 ALFA 現售产品中，Soft AP 表現最稳定的芯片。它的驱动 `mt76x2u` 早在 2018 年（kernel 4.19）就進入 Linux 官方 kernel，意味著只要你的系统夠新，**插上去就能用**——不需要 `git clone`，不需要 `dkms`，不需要在 kernel 升級后重新编译。

### 核心優勢

- **WPA2 + WPA3 双重支持**：MediaTek in-kernel 驱动原生支持 WPA3 SAE，是 Realtek 驱动无法比擬的優勢
- **VIF 虛擬接口支持**：同一张卡可同时以 AP + Managed + Monitor 三种模式並行，无需額外添購第二张卡。你可以一邊分享网络，一邊同时监控无线頻譜
- **超低耗電**：最大約 400mA，非常適合 Raspberry Pi（Pi 4 USB 子系统總供電僅 1200mA）
- **全平台兼容**：在 Kali Linux 2022.x–2025.x、Ubuntu 22.04/24.04、Debian 11/12、Raspberry Pi OS（Pi 3B+、4、5）均有大量成功案例

### hostapd 正確设置示例（MT7612U 專用）

以下是社群（morrownr/USB-WiFi）多年测试确认的能力标志，**必須完全对應 MT7612U 的实际硬件能力**：

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz；改为 g 则使用 2.4GHz
channel=36                    # UNII-1，非 DFS，最安全的选择
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U 正確的 HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # channel 36 对應的中心频道索引

# 安全性：WPA2 + WPA3 混合模式
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 双支持
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ 最常见错误

若 `ht_capab` 包含 MT7612U 不支持的能力标志（尤其在 USB 2.0 端口上强制使用某些 HT40 设置時），hostapd 会直接崩潰退出，错误消息非常不明顯。**請務必只使用上方确认的标志组合**，不要複製其他芯片（如 RTL8812AU）的设置。（来源：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)）

### 社群真實評價

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> — **morrownr**，GitHub morrownr/7612u（Linux USB WiFi 最具權威的社群知識庫维护者）

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBay 用户評論

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 讨论串

---

## 四、AWUS036ACH（RTL8812AU）— 可用，但有限制 {#ach}

### Soft AP 支持状态：⚠️ 有条件支持

RTL8812AU 是 ALFA 最具知名度的渗透测试芯片，长期以来是 Kali Linux 社群的最愛。它的 Soft AP 功能確實存在——單純建立热点可以正常運作——但 Realtek 的 out-of-kernel 驱动架构带来幾个长期限制：

### 已知限制清單

1. **WPA3 不支持**：RTL8812AU 驱动雖然在接口上显示支持 WPA3，但多名用户确认实际上无法運作，**只能使用 WPA2-PSK**
2. **VIF 虛擬接口不支持**：无法同时在同一张卡上跑 AP + Monitor 模式。需要 AP 兼监控時，必須使用兩张不同的网络卡分工
3. **Kali Linux 2025.x 驱动问题**：最新版 Kali 的 aircrack-ng/rtl8812au 驱动有兼容性问题，需回退至特定的旧版 commit（`63cf0b4`）才能正常運作。Kernel 6.14+ 的 in-kernel rtw88 驱动有望改善此问题
4. **高耗電**：最大約 800mA，在 Raspberry Pi 上若同时連接多个 USB 设备，可能導致系统不稳定，建议使用有源 USB Hub

### hostapd 设置示例（RTL8812AU）

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# 注意：与 MT7612U 的 capabilities 完全不同！
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# 安全性：只能用 WPA2，WPA3 不要加
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### 安装驱动（Kali Linux / Ubuntu / Debian）

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x 需要指定旧版 commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### 社群評價

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 用户

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr 技术说明

### 針对 ACH 的建议

若你已经擁有 AWUS036ACH，可以用於 Soft AP（單純建立热点没有问题）。但如果你尚未购买且主要目的是 Soft AP，**請選 ACM**。

---

## 五、AWUS036AXML / AWUS036AXM（MT7921AUN）— 謹慎选择 {#axml}

### Soft AP 支持状态：⚠️ 部分支持，有已知固件/驱动问题

AWUS036AXML 与 AWUS036AXM 是 ALFA 的 WiFi 6E 三频旗舰，能覆蓋 2.4 GHz、5 GHz 和全新的 6 GHz 频段。它的 in-kernel 驱动 `mt7921u` 从 kernel 5.18 起就已内建，AP 模式支持则在 kernel 5.19 正式加入。然而，MT7921AUN 芯片同时整合了 Bluetooth 5.2，这成为了 2024–2025 年社群最头疼的问题根源。

### AP 模式支持的 kernel 版本里程碑

| 模式 | 最低 kernel 版本 |
|------|-----------------|
| Managed（一般连接） | 5.18+ |
| **AP 模式（Soft AP）** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO（Wi-Fi Direct AP） | 6.4+ |

### 已知问题与解决方案

#### 问题一：Bluetooth 干擾導致 WiFi 崩潰

在 kernel 6.6 以后的版本，BT 子系统的變動導致 mt7921u 的 WiFi 功能偶發崩潰，重現率因系统环境而異。**目前最有效的解决方案是禁用 btusb 驱动：**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### 问题二：固件版本过旧

若系统的 MediaTek 固件过旧，网络卡可能无法被正確识别。需安装 2024 年 11 月以后的最新固件：

```bash
# 确认当前固件版本
dmesg | grep "WM Firmware"
# 應显示：Build Time: 20241106151045 或更新

# 若版本过旧，从 kernel.org 下載更新
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### 问题三：hostapd 版本需求

部分用户回報需要从 git 编译最新版 hostapd 才能完整支持 WiFi 6 AP 功能，系统套件管理器安装的版本可能不完整。

#### 问题四：AP 模式下 Tx Power 显示異常

`iw` 显示僅 3 dBm，无法調整，但实际上芯片有内建放大器，此为 kernel 驱动的显示问题而非硬件限制。

#### 问题五：部分 kernel 版本下 monitor mode 異常

截至 2025 年 12 月，kernel 6.18 及部分較早版本的 mt7921u 驱动有 monitor mode 问题。

### 社群評價

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — **fhteagle**，[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### 針对 AXML/AXM 的建议

如果你需要 WiFi 6E 的 6GHz 频段功能，且願意接受偶爾需要調整设置，可以选择。**对稳定度要求高的生产环境 Soft AP，建议選 ACM。**

---

## 六、AWUS036AX / AWUS036AXER（RTL8832BU）— 不建议用於 Soft AP {#ax}

### Soft AP 支持状态：❌ 不建议

AWUS036AX 和 AWUS036AXER 雖然是 WiFi 6 規格，但 RTL8832BU 芯片是所謂的「multi-state」设备——出厂預設以 USB 大量存储模式枚舉，Linux 需要先做 USB mode switch 才能切換为无线网络卡模式。

**主要问题：**

1. **Multi-state 设备**：增加部署复杂度，插上去不会直接變成网卡
2. **Monitor Mode 限制**：kernel 6.14 以下支持不完整
3. **Soft AP 社群案例極少**：相較於 MT7612U 和 RTL8812AU，RTL8832BU 用於 Soft AP 的实际案例幾乎找不到
4. **社群文档明确不推荐**：morrownr/USB-WiFi 将此芯片標記为「不建议用於 penetration testing」

> Yupitek 官方文章已明确指出：「AWUS036AX / AWUS036AXER 的 RTL8832BU 芯片在 kernel 6.14 以下有有限的 monitor mode 支持，不建议用於 penetration testing，請改用 AWUS036ACH 或 AWUS036AXML。」

---

## 七、各平台兼容性總表 {#compat-matrix}

### AWUS036ACM（MT7612U）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel，即插即用，kernel 5.x / 6.x 均適用 |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel，零设置，建议使用 LTS 版 |
| Debian 11 / 12 | ✅ | In-kernel，稳定 |
| Raspberry Pi 4（RPi OS） | ✅ | 最低耗電（400mA），morrownr 长期验证。Pi 4 USB 3.0 端口效能更佳 |
| Raspberry Pi 5（RPi OS） | ✅ | 与 Pi 4 相同驱动，稳定 |

### AWUS036ACH（RTL8812AU）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux 2022.x – 2025.x | ⚠️ | 需安装外部驱动；2025.x 需用旧版 commit `63cf0b4`。Kernel 6.14+ 后 in-kernel rtw88 有望改善 |
| Ubuntu 22.04 / 24.04 | ⚠️ | 需手動安装 rtw88 或 aircrack-ng 社群驱动 |
| Debian 11 / 12 | ⚠️ | 同上 |
| Raspberry Pi 4 | ⚠️ | 可運作，但高耗電（800mA），建议有源 USB Hub |
| Raspberry Pi 5 | ⚠️ | 同上，Pi 5 USB controller 差異可能有不同表現 |

### AWUS036AXML / AWUS036AXM（MT7921AUN）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux 2022.x（kernel 5.18+） | ✅ | 需禁用 btusb，需更新固件 |
| Kali Linux 2024.x / 2025.x | ⚠️ | Kernel 6.11+ BT/WiFi 衝突问题，不稳定 |
| Ubuntu 24.04（kernel 6.8+） | ⚠️ | 2024 年底有问题回報 |
| Ubuntu 25.04 / CachyOS（kernel 6.14+） | ✅ | 即插即用，新版 kernel 改善明顯 |
| Debian 12 | ⚠️ | 視 kernel 版本而定 |
| Raspberry Pi 4 / 5 | ⚠️ | 有成功案例，但需确认固件版本並禁用 BT |

### AWUS036AX / AWUS036AXER（RTL8832BU）

| 平台 | Soft AP | 備註 |
|------|---------|------|
| Kali Linux | ❌ | Multi-state，需 USB mode switch，社群案例極少 |
| Ubuntu / Debian | ❌ | 同上 |
| Raspberry Pi 4 / 5 | ❌ | 同上 |

---

## 八、Soft AP 完整设置步驟（AWUS036ACM）{#setup-guide}

以下以 AWUS036ACM 在 Raspberry Pi 4 上建立 5GHz Soft AP 为例，提供从头到尾的完整步驟。

### Step 1：确认网卡辨識与驱动

```bash
# 确认网卡已辨識
lsusb | grep MediaTek
# 預期输出：Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# 检查驱动已加载
dmesg | grep mt76
# 預期输出：mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# 确认 AP 模式支持
iw list | grep -A 10 "Supported interface modes"
# 检查输出是否包含 "* AP"
```

### Step 2：安装必要套件

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Step 3：设置 hostapd

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

# HT/VHT 设置（MT7612U 專用）
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

### Step 4：设置 dnsmasq（DHCP）

建立 `/etc/dnsmasq.conf`：

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Step 5：设置靜態 IP 与 NAT

```bash
# 为 wlan0 设置靜態 IP
sudo ip addr add 192.168.10.1/24 dev wlan0

# 启用 IP 轉送
sudo sysctl net.ipv4.ip_forward=1

# 设置 NAT（假設 eth0 是上游网络接口）
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# 永久存储 iptables 規则
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Step 6：启动服务

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# 确认服务状态
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# 让 hostapd 开機自動启动
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

完成后，用手機或筆電搜尋 WiFi，應該可以看到 `Yupitek_AP` 这个 SSID。

---

## 九、常见疑难排解 {#troubleshooting}

### Q1：hostapd 启动后直接崩潰

**症狀**：`sudo systemctl status hostapd` 显示 `exited` 或 `failed`

**可能原因**：`hostapd.conf` 中的 `ht_capab` 包含芯片不支持的能力标志

**解法**：移除多餘的标志。对 MT7612U（ACM）而言，使用本文第 3 節提供的设置檔是最安全的选择。**不要複製其他芯片的 ht_capab 设置。**

---

### Q2：客户端连接后无法上网

**症狀**：WiFi 已连接，取得 IP，但 ping 8.8.8.8 无回應

**检查清單**：

```bash
# 1. 检查 IP 轉送是否启用
cat /proc/sys/net/ipv4/ip_forward
# 應输出：1

# 2. 检查 NAT 規则是否存在
sudo iptables -t nat -L POSTROUTING -v
# 應該能看到 MASQUERADE 規则

# 3. 确认上游网络接口是否正常
ping -I eth0 8.8.8.8
```

---

### Q3：5GHz AP 找不到或斷斷續續

**可能原因**：

1. **使用了 DFS 频道（100–144）**：MT7612U / MT7610U 缺乏 DFS 支持，應使用 UNII-1 频道（36–48）
2. **发射功率不足**：确认天线已正確鎖緊於 RP-SMA 接头
3. **USB 供電不足**（Raspberry Pi）：使用官方 5A 电源或外接有源 USB Hub

---

### Q4：Raspberry Pi 上的 hostapd 一直重启

**症狀**：`dmesg` 中出現大量 USB reset 消息

**可能原因**：USB 端口供電不足（特別是 AWUS036ACH 高耗電芯片，最大 800mA）

**解法**：
- 使用官方 Pi 5A 电源供應器
- 使用外部有源 USB Hub
- 将网卡插入 USB 3.0 端口（Pi 4 才有）

---

### Q5：AWUS036AXML/AXM 的 WiFi 突然斷线或无法启动

**可能原因**：Bluetooth 子系统干擾 WiFi（MT7921AUN 内建 BT 5.2）

**解法**：永久禁用藍牙驱动

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 十、技术深入：VIF、WPA3、DFS 频道 {#technical}

### VIF（虛擬接口）：一张卡同时做多件事

VIF（Virtual Interface）让同一张物理网络卡可以同时以多个邏輯接口運作。例如：一个接口連上游路由器（managed 模式），同时另一个接口作为 AP（master 模式）供其他设备連入。

三种常见場景的需求分析：

| 場景 | 是否需要 VIF | 最佳网卡 |
|------|-------------|---------|
| 基本 NAT 路由（eth0 上游 + wlan AP） | ❌ 不需要 | 所有支持 AP 的即可 |
| 无线橋接（WiFi 接收 + WiFi AP 同时） | ✅ 需要 | ACM（MT7612U） |
| 监控 + AP 同时（安全研究 / Rogue AP） | ✅ 需要 | ACM（MT7612U） |

**VIF 实战示例（MT7612U）：**

```bash
# 在現有 wlan1 之外建立額外的 AP 虛擬接口
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# 現在 wlan1 可以連上游网络，ap0 跑 hostapd
```

僅 MediaTek in-kernel 驱动（mt76x2u、mt7921u）完整支持 VIF。Realtek out-of-kernel 驱动基本上无此能力，若需要 AP + Monitor 同时運作，必須使用兩张不同的网络卡。

---

### WPA3 支持对照表

| 芯片 | 对應型號 | WPA2 | WPA3 |
|------|---------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ 原生支持 SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ 原生支持 SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ 宣称支持但实际无效 |
| RTL8832BU | AWUS036AX / AXER | ✅ | ⚠️ 未确认 |

---

### 5GHz Soft AP 的频道选择：避开 DFS

DFS（Dynamic Frequency Selection）频道（ch100–ch140）需要 kernel 层面的雷達检测機制。MT7612U 等芯片缺乏 DFS 支持，使用 5GHz AP 時應选择：

| 频段 | 建议频道 | 原因 |
|------|---------|------|
| **UNII-1** | **36, 40, 44, 48** | 全芯片支持，最安全的选择 |
| UNII-2（DFS） | 52–144 | 大部分不支持，不建议 |
| UNII-3 | 149–165 | 部分支持（依地區法規） |

---

## 十一、社群真實案例整理 {#real-cases}

### 案例 1：RPi4B + AWUS036ACM = 长期稳定家用 5GHz AP

**来源**：morrownr/7612u GitHub 知識庫
**場景**：morrownr 长期以 RPi4B + AWUS036ACM 作为家用 5GHz AP，搭配 Pi 内建 2.4GHz 提供双频服务
**结果**：长期稳定運作，无需重启，「outstanding」評價
**配置**：hostapd + dnsmasq + iptables NAT

### 案例 2：RPi3B+ + ACM — 初始崩潰，調整后成功

**来源**：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**问题**：在 RPi3B+ 上以 USB 2.0 端口运行，hostapd 崩潰
**根本原因**：`ht_capab` 包含 USB 2.0 带宽限制下不支持的 HT40 设置标志
**解决**：移除多餘标志后，在 Kali Linux 上成功启动

### 案例 3：Pi PwnBox + AWUS036ACH = 紅隊测试 Rogue AP

**来源**：GitHub koutto/pi-pwnbox-rogueap
**場景**：以 RPi3B+ 建立 Rogue AP 平台：一张 RTL8812AU（AWUS036ACH）負責跑 AP，另一张 RT3070（AWUS036NEH）負責数据包注入攻擊
**关鍵發現**：因 RTL8812AU 不支持 VIF，必須使用兩张卡分工（而非像 ACM 可以單卡搞定）

### 案例 4：AWUS036AXML 在 RPi3B ArchLinux ARM 上稳定跑 AP

**来源**：[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**場景**：用户在 RPi3B ArchLinux aarch64 上成功跑 AWUS036AXML AP 模式
**評語**：「It's the most stable mt7921 in my collection.」
**关鍵条件**：从 git 编译最新版 hostapd，並禁用 btusb

### 案例 5：AWUS036ACHM（MT7610U，已停產）在 Pi4 上達到全速 AP

**来源**：[GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**问题**：初始配置只達 65 Mbps link speed，未達 AC 5GHz 全速
**解决**：加入正確的 `vht_oper_chwidth=1` 和 `vht_oper_centr_freq_seg0_idx` 设置后達到 433 Mbps link rate
**对於 ACM 的啟示**：同樣的 VHT 参数设置对 MT7612U（ACM）也至关重要

---

## 十二、选购建议与最終结论 {#recommendations}

### 快速決策指南

| 推荐等級 | 型號 | 適合对象 | 一句話總結 |
|---------|------|---------|-----------|
| 🥇 **首选** | **AWUS036ACM** | 所有人，尤其第一次建立 Soft AP | 全平台稳定，零煩惱 |
| 🥈 有条件可用 | AWUS036ACH | 已擁有此型號的用户 | 需裝驱动，无 WPA3 |
| 🥉 进阶选择 | AWUS036AXML | 需要 WiFi 6E 且願意花时间調校 | 6GHz 優勢，需手動排除问题 |
| ❌ 不建议 | AWUS036AX / AXER | N/A | Soft AP 未经社群验证 |

### 🎯 簡明決策指南

- **需要在 Kali Linux / Ubuntu / Debian / Raspberry Pi 4 或 5 上建立稳定 Soft AP？**
  → 直接選 **AWUS036ACM**，没有有之一。

- **已有 AWUS036ACH，想测试 Soft AP？**
  → 可以用，但只支持 WPA2，且需要安装驱动。接受这些限制的話没有问题。

- **需要 WiFi 6E（6GHz 频段）且願意花时间设置？**
  → AWUS036AXML，記得禁用 BT 驱动、确认 kernel ≥ 6.6 LTS。

- **主要目的是 Soft AP 而非渗透测试？**
  → AWUS036ACM 是唯一在所有平台上均有大量验证案例的选择。

---

### 結語

建立 Soft AP 的核心关鍵，不在於 WiFi 速率有多快，也不在於天线有幾根——**真正的关鍵，是芯片驱动对 AP 模式的支持程度。**

在我们调查的所有 ALFA 产品中，**AWUS036ACM（MT7612U）** 是唯一同时滿足「in-kernel 驱动、WPA3 原生支持、VIF 虛擬接口、低耗電、全平台稳定」的选择。morrownr 親測、GitHub 社群验证、eBay 用户背書——ACM 是 Soft AP 用途中，你唯一不会后悔的选择。

AWUS036ACH（RTL8812AU）可以用，但需要接受 WPA3 不支持和驱动维护成本。AWUS036AXML/AXM（MT7921AUN）潛力很大，但目前驱动成熟度仍在路上。AWUS036AX/AXER（RTL8832BU），不建议用於 Soft AP。

**如果你是第一次嘗試在 Raspberry Pi 或 Kali Linux 上建立 Soft AP——選 ACM。**

---

### 购买链接

- [AWUS036ACM — Soft AP 首选](/zh-cn/products/alfa/awus036acm/)
- [AWUS036ACH — 经典渗透测试卡](/zh-cn/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E 三频旗舰](/zh-cn/products/alfa/awus036axml/)
- [ALFA Network 全系列产品](/zh-cn/products/alfa/)

### 延伸閱讀

- [AWUS036ACH vs AWUS036ACM：芯片驱动方式完整比较](/zh-cn/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](/zh-cn/blog/)
- [morrownr/USB-WiFi — 最權威的 Linux USB WiFi 知識庫](https://github.com/morrownr/USB-WiFi)（4,100+ stars）
- [morrownr/7612u — MT7612U 專屬文档（含 RPi4B Bridged AP 完整教程）](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi 自動整理知識庫](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 資料来源

本文資料汇整自：
- **morrownr/USB-WiFi** GitHub 知識庫（4,100+ stars）及完整的 iw_list 记录
- **morrownr/7612u** — MT7612U Bridged AP on RPi4B 完整教程
- **GitHub issue tracker** — issue #2（ACM AP 设置）、#476（AXML AP 测试）、Discussion #31（ACHM 全速 AP）
- **koutto/pi-pwnbox-rogueap** — Alfa 网卡 RogueAP 实战案例
- **Rokland** 授权零售商 Linux 支持页面
- **Lab401** 技术評測与 2025 渗透测试最佳选择报告
- **Raspberry Pi 官方論壇** — Pi 4/5 USB WiFi 兼容性讨论
- **Yupitek 現有博客** — ACM China Install Guide、AXML WiFi 6E Review、Kali Linux 2026 最佳网卡

---

> **標籤**：#ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi4 #RaspberryPi5 #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #LinuxWiFiAP #USB无线网络卡 #树莓派WiFi热点 #Yupitek
>
> **作者**：榆合科技 (Yupitek Ltd) — ALFA Network 台湾授权总代理
>
> **免責聲明**：本文研究資料截至 2026 年 5 月。Linux Kernel 与各發行版持續更新，驱动支持狀況可能隨版本變動。部署前建议确认目標平台的 kernel 版本与驱动兼容性。
>
> **技术支持**：如有 Soft AP 设置问题，歡迎联系榆合科技台湾本地技术支持团队。产品购买与咨询請至 [yupitek.com](/zh-cn/)。
