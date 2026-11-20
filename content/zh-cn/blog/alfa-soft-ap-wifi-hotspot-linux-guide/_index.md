---
title: "ALFA 网卡 Soft AP 完整指南 2026：Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5 创建 WiFi 热点"
description: "深度调查 ALFA Network USB 无线网卡在 Kali Linux、Ubuntu、Debian、Raspberry Pi 4 与 Pi 5 上使用 Soft AP（WiFi Hotspot / hostapd）的完整兼容性。涵盖 AWUS036ACM、AWUS036ACH、AWUS036AXML 详细设置、社区反馈、常见疑难排解与产品选购建议。"
date: 2026-05-21
author: "benny-lai"
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi", "USB-无线网卡", "树莓派-WiFi-热点"]

featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
faq:
  - question: "ALFA USB 网卡可以在 Linux 上当 WiFi 热点用吗？"
    answer: "视芯片组而定。AWUS036ACM（MT7612U）完整支持且即插即用，AWUS036ACH（RTL8812AU）有条件支持，AWUS036AXML 部分支持需调校。"
  - question: "哪款 ALFA 网卡最适合在 Raspberry Pi 上创建 Soft AP？"
    answer: "AWUS036ACM 是最佳选择。in-kernel 驱动即插即用、耗电仅 400mA 适合 Pi 供电、支持 WPA3 与 VIF 虚拟接口，全平台稳定。"
  - question: "如何确认网卡支持 AP 模式？"
    answer: "执行 iw list | grep -A 10 'Supported interface modes'，若输出包含 * AP 即代表驱动支持 Soft AP，hostapd 才能正常运行。"
  - question: "RTL8812AU 驱动的 Soft AP 有哪些限制？"
    answer: "不支持 WPA3 仅能用 WPA2-PSK、不支持 VIF 虚拟接口需两张卡分工、耗电约 800mA 在 Pi 上需有源 USB Hub。"
  - question: "AWUS036AXML 跑 Soft AP 时 WiFi 突然断线怎么办？"
    answer: "MT7921AUN 内置 Bluetooth 5.2 会干扰 WiFi。执行 echo 'install btusb /bin/false' 写入 /etc/modprobe.d/ 永久禁用蓝牙驱动后重开机。"
---
> 「ALFA 的 USB 无线网卡，可以在 Kali Linux / Ubuntu / Raspberry Pi 上当 WiFi 热点（Soft AP）用吗？」

## 前言

{{< tldr >}}
ALFA 网卡 Soft AP 兼容性取决于芯片驱动。AWUS036ACM 为全平台稳定首选，AWUS036ACH 可用但无 WPA3，AWUS036AXML 需禁用蓝牙并更新固件，RTL8832BU（AX / AXER）在 kernel 6.17 以上以内置驱动可用。
{{< /tldr >}}


ALFA AWUS036ACM（MT7612U）是 Linux Soft AP 最佳首选，in-kernel 驱动即插即用、支持 WPA3 与 VIF 虚拟接口。RTL8812AU 有条件支持，MT7921AUN 需手动调校。




这是榆閤科技最常收到的客户询问之一。问题听起来简单，但答案因型号和芯片组的不同而大相径庭——**不是每一张 USB 无线网卡都能跑 Soft AP。**

本文汇整 GitHub 上超过 500 则社区讨论（morrownr/USB-WiFi 知识库）、Reddit 技术论坛、Raspberry Pi 官方论坛纪录，以及实际用户反馈，给出一份诚实、完整的调查报告，告诉你哪些 ALFA 网卡适合、哪些不适合，以及从头到尾的完整设置步骤。

---

## 一、什么是 Soft AP？Linux 如何运作 {#what-is-softap}

**Soft AP（Software Access Point，软件访问点）** 是指透过软件（主要是 **hostapd**），将一张普通的 USB 无线网卡变成无线基地台（Access Point），让其他设备（手机、笔电、IoT 设备）可以连上网络，不需要购买专用路由器或 AP 硬件。

这个功能在以下场景中极其实用：

- **旅行 / 家用路由器**：出差或露营时，笔电或 Raspberry Pi 插上 ALFA 网卡，立刻变成随身 WiFi 热点
- **渗透测试练习环境**：在隔离环境中创建 Rogue AP 进行安全研究
- **IoT 设备中继**：在信号死角创建中继站，让传感器回传数据
- **边缘 AI 部署**：工业场景中没有有有线网络，需要让设备作为热点让其他设备连入
- **灾难应变通信**：断网时快速创建临时通信网络

### Linux Soft AP 的四大核心组件

| 组件 | 功能 |
|------|------|
| **hostapd** | 创建无线基地台的核心程序，负责管理 SSID、认证、加密 |
| **nl80211** | Linux 无线子系统标准接口，驱动必须支持此框架才能与 hostapd 协作 |
| **dnsmasq** | DHCP 服务器，自动为连接设备分配 IP 地址 |
| **iptables / nftables** | 网络地址转换（NAT），让连接设备共享上游网络 |

### 关键概念：Master Mode

**Master Mode**（又称 AP Mode、Infrastructure Mode）是芯片驱动层面的能力。如果驱动不支持 Master Mode，hostapd 就无法启动——无论你的设置多完美都没有用。

验证一张网卡是否支持 AP 模式：

```bash
iw list | grep -A 10 "Supported interface modes"
```

如果输出中包含 `* AP`，代表该网卡的驱动支持 Soft AP。如果没有有，那这张卡就无法用于此用途。

### 💡 In-kernel vs Out-of-kernel 驱动

这是选择 Soft AP 网卡时**最重要**的概念：

| 类型 | 说明 | 对 Soft AP 的影响 |
|------|------|------------------|
| **In-kernel 驱动** | 已被合并进 Linux 官方源代码，系统开机即自动加载，无需手动安装 | ✅ 长期稳定，kernel 升级后仍可使用 |
| **Out-of-kernel 驱动** | 需自行从 GitHub 下载、编译，kernel 升级后可能需要重新编译 | ⚠️ 每次 kernel 更新都可能失效 |

**对 Soft AP 的长期稳定性而言，in-kernel 驱动远优于 out-of-kernel。**

---

## 二、ALFA 产品线与芯片速览 {#product-lineup}

以下是 Yopitek 目前销售的 ALFA 网卡型号、核心芯片与 Soft AP 初步评级：

| 型号 | 芯片组 | 驱动类型 | WiFi 标准 | Soft AP 评级 |
|------|--------|----------|-----------|-------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel（kernel 4.19+） | WiFi 5 AC1200 双频 | ✅ 完整支持 |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel（kernel 6.13+ 纳入 in-kernel） | WiFi 5 AC1200 双频 | ⚠️ 有条件支持 |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel（kernel 5.18+，AP 模式 5.19+） | WiFi 6E AX3000 三频 | ⚠️ 部分支持 |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel（同上） | WiFi 6E AX3000 三频 | ⚠️ 部分支持 |
| AWUS036AX | Realtek RTL8832BU | 内置 rtw89_8852bu（kernel 6.17+）；较旧 kernel 需社区 DKMS 驱动 | WiFi 6 AX1800 双频 | ✅ 可用（kernel 6.17+） |
| AWUS036AXER | Realtek RTL8832BU | 内置 rtw89_8852bu（kernel 6.17+，同 AX） | WiFi 6 AX1800 双频 | ✅ 可用（kernel 6.17+） |

> **备注**：AWUS036ACHM（MT7610U）已停产，Yopitek 产品页面不再列出。本文以现售产品为主。

---

## 三、AWUS036ACM（MT7612U）— ⭐ Soft AP 最佳首选 {#acm}

### Soft AP 支持状态：✅ 完整支持

MT7612U 是目前 ALFA 现售产品中，Soft AP 表现最稳定的芯片。它的驱动 `mt76x2u` 早在 2018 年（kernel 4.19）就进入 Linux 官方 kernel，意味着只要你的系统够新，**插上去就能用**——不需要 `git clone`，不需要 `dkms`，不需要在 kernel 升级后重新编译。

### 核心优势

- **WPA2 + WPA3 双重支持**：MediaTek in-kernel 驱动原生支持 WPA3 SAE，是 Realtek 驱动无法比拟的优势
- **VIF 虚拟接口支持**：同一张卡可同时以 AP + Managed + Monitor 三种模式并行，无需额外添购第二张卡。你可以一边分享网络，一边同时监控无线频谱
- **超低耗电**：最大约 400mA，非常适合 Raspberry Pi（Pi 4 USB 子系统总供电仅 1200mA）
- **全平台兼容**：在 Kali Linux 2022.x–2025.x、Ubuntu 22.04/24.04、Debian 11/12、Raspberry Pi OS（Pi 3B+、4、5）均有大量成功案例

### hostapd 正确设置示例（MT7612U 专用）

以下是社区（morrownr/USB-WiFi）多年测试确认的能力标志，**必须完全对应 MT7612U 的实际硬件能力**：

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; 改为 g 则使用 2.4GHz
channel=36                    # UNII-1, 非 DFS, 最安全的选择
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U 正确的 HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # channel 36 对应的中心频道索引

# 安全性: WPA2 + WPA3 混合模式
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 双支持
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ 最常见错误

若 `ht_capab` 包含 MT7612U 不支持的能力标志（尤其在 USB 2.0 端口上强制使用某些 HT40 设置时），hostapd 会直接崩溃退出，错误消息非常不明显。**请务必只使用上方确认的标志组合**，不要复制其他芯片（如 RTL8812AU）的设置。（来源：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)）

### 社区真实评价

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> — **morrownr**，GitHub morrownr/7612u（Linux USB WiFi 最具权威的社区知识库维护者）

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> — eBay 用户评论

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> — GitHub issue #2 讨论串

---

## 四、AWUS036ACH（RTL8812AU）— 可用，但有限制 {#ach}

### Soft AP 支持状态：⚠️ 有条件支持

RTL8812AU 是 ALFA 最具知名度的渗透测试芯片，长期以来是 Kali Linux 社区的最爱。它的 Soft AP 功能确实存在——单纯创建热点可以正常运作——但 Realtek 的 out-of-kernel 驱动架构带来几个长期限制：

### 已知限制清单

1. **WPA3 不支持**：RTL8812AU 驱动虽然在接口上显示支持 WPA3，但多名用户确认实际上无法运作，**只能使用 WPA2-PSK**
2. **VIF 虚拟接口不支持**：无法同时在同一张卡上跑 AP + Monitor 模式。需要 AP 兼监控时，必须使用两张不同的网卡分工
3. **Kali Linux 2025.x 驱动问题**：最新版 Kali 的 aircrack-ng/rtl8812au 驱动有兼容性问题，需回退至特定的旧版 commit（`63cf0b4`）才能正常运作。Kernel 6.13+ 的 in-kernel rtw88 驱动有望改善此问题
4. **高耗电**：最大约 800mA，在 Raspberry Pi 上若同时连接多个 USB 设备，可能导致系统不稳定，建议使用有源 USB Hub

### hostapd 设置示例（RTL8812AU）

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# 注意: 与 MT7612U 的 capabilities 完全不同!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# 安全性: 只能用 WPA2, WPA3 不要加
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

### 社区评价

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> — GitHub issue #2 用户

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> — morrownr 技术说明

### 针对 ACH 的建议

若你已经拥有 AWUS036ACH，可以用于 Soft AP（单纯创建热点没有问题）。但如果你尚未购买且主要目的是 Soft AP，**请选 ACM**。

---

## 五、AWUS036AXML / AWUS036AXM（MT7921AUN）— 谨慎选择 {#axml}

### Soft AP 支持状态：⚠️ 部分支持，有已知固件/驱动问题

AWUS036AXML 与 AWUS036AXM 是 ALFA 的 WiFi 6E 三频旗舰，依规格能覆盖 2.4 GHz、5 GHz 和全新的 6 GHz 频段（AXML 的 6 GHz 本机实测可用，AXM 的 6 GHz 未实测）。它的 in-kernel 驱动 `mt7921u` 从 kernel 5.18 起就已内建，AP 模式支持则在 kernel 5.19 正式加入。然而，MT7921AUN 芯片同时集成了 Bluetooth 5.2，这成为了 2024–2025 年社区最头疼的问题根源。

### AP 模式支持的 kernel 版本里程碑

| 模式 | 最低 kernel 版本 |
|------|-----------------|
| Managed（一般连接） | 5.18+ |
| **AP 模式（Soft AP）** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO（Wi-Fi Direct AP） | 6.4+ |

### 已知问题与解决方案

#### 问题一：Bluetooth 干扰导致 WiFi 崩溃

在 kernel 6.6 以后的版本，BT 子系统的变动导致 mt7921u 的 WiFi 功能偶发崩溃，重现率因系统环境而异。**目前最有效的解决方案是禁用 btusb 驱动：**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### 问题二：固件版本过旧

若系统的 MediaTek 固件过旧，网卡可能无法被正确识别。需安装 2024 年 11 月以后的最新固件：

```bash
# 确认当前固件版本
dmesg | grep "WM Firmware"
# 应显示: Build Time: 20241106151045 或更新

# 若版本过旧, 从 kernel.org 下载更新
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### 问题三：hostapd 版本需求

部分用户回报需要从 git 编译最新版 hostapd 才能完整支持 WiFi 6 AP 功能，系统套件管理器安装的版本可能不完整。

#### 问题四：AP 模式下 Tx Power 显示异常

`iw` 显示仅 3 dBm，无法调整，但实际上芯片有内建放大器，此为 kernel 驱动的显示问题而非硬件限制。

#### 问题五：部分 kernel 版本下 monitor mode 异常

截至 2025 年 12 月，kernel 6.18 及部分较早版本的 mt7921u 驱动有 monitor mode 问题。

### 社区评价

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> — **fhteagle**，[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### 针对 AXML/AXM 的建议

如果你需要 WiFi 6E 的 6GHz 频段功能，且愿意接受偶尔需要调整设置，可以选择。**对稳定度要求高的生产环境 Soft AP，建议选 ACM。**

---

## 六、AWUS036AX / AWUS036AXER（RTL8832BU）— kernel 6.17 以上可用于 Soft AP {#ax}

### Soft AP 支持状态：✅ kernel 6.17 以上可用（旧 kernel 需社区 DKMS 驱动）

在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17）上以内置 `rtw89_8852bu` 驱动实测，AWUS036AX 与 AWUS036AXER（同芯片、同驱动）行为相同，2.4 GHz 与 5 GHz 的 Soft AP 均可用。

**实测结果（kernel 6.17）：**

1. **AP 模式**：2.4 GHz（802.11n）与 5 GHz（VHT 80 MHz）均可用
2. **VIF（STA + AP）**：可用——同一信道上同时保持客户端连接与 AP 接口
3. **WPA3-SAE AP**：2.4 GHz 可用（iPhone 15 Pro 连入，MFP 启用；5 GHz 未实测）
4. **Monitor／注入**：2.4 与 5 GHz 的 monitor 接收强；2.4 GHz 注入 AX 96%、AXER 73%，5 GHz 可用；端到端 WPA handshake 抓取成功
5. **不支持**：IBSS、Mesh、Active monitor

**注意事项：**

- **kernel 版本是前提**：rtw89_8852bu 自 kernel 6.17 起内置；较旧 kernel 需使用社区 DKMS 驱动（rtl8852bu），该驱动下 monitor 可能受限，且不支持 VIF。
- **USB 模式**：部分设备可能以光盘模式（`0bda:1a2b`）枚举，需执行 `usb_modeswitch -v 0bda -p 1a2b -K`；本次测试的设备直接以无线网卡模式枚举。
- **社区案例**：相较于 MT7612U 与 RTL8812AU，该芯片的 Soft AP 社区案例仍较少。

> Yopitek 实测结果（ASUS GX10、kernel 6.17）：AWUS036AX / AWUS036AXER 在内置驱动下 monitor 接收强、封包注入可用，也可用于渗透测试。monitor 受限仅限于旧 kernel 搭配社区 DKMS 驱动的情况。
>
> 补充：在 stock kernel 6.16 以上（实测 6.17）上，AWUS036AXML 的 monitor、AP、WPA3、VIF 均可用，但封包注入测试未通过（aireplay-ng --test 显示 Found 0 APs / No Answer），原因是 mac80211 chanctx 回归，并非芯片先天限制。需要封包注入请改用 AWUS036ACH、EACS、ACS 或 AX。

---

## 七、各平台兼容性总表 {#compat-matrix}

### AWUS036ACM（MT7612U）

| 平台 | Soft AP | 备注 |
|------|---------|------|
| Kali Linux 2022.x – 2025.x | ✅ | In-kernel，即插即用，kernel 5.x / 6.x 均适用 |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel，零设置，建议使用 LTS 版 |
| Debian 11 / 12 | ✅ | In-kernel，稳定 |
| Raspberry Pi 4（RPi OS） | ✅ | 最低耗电（400mA），morrownr 长期验证。Pi 4 USB 3.0 端口性能更佳 |
| Raspberry Pi 5（RPi OS） | ✅ | 与 Pi 4 相同驱动，稳定 |

### AWUS036ACH（RTL8812AU）

| 平台 | Soft AP | 备注 |
|------|---------|------|
| Kali Linux 2022.x – 2025.x | ⚠️ | 需安装外部驱动；2025.x 需用旧版 commit `63cf0b4`。Kernel 6.13+ 后 in-kernel rtw88 有望改善 |
| Ubuntu 22.04 / 24.04 | ⚠️ | 需手动安装 rtw88 或 aircrack-ng 社区驱动 |
| Debian 11 / 12 | ⚠️ | 同上 |
| Raspberry Pi 4 | ⚠️ | 可运作，但高耗电（800mA），建议有源 USB Hub |
| Raspberry Pi 5 | ⚠️ | 同上，Pi 5 USB controller 差异可能有不同表现 |

### AWUS036AXML / AWUS036AXM（MT7921AUN）

| 平台 | Soft AP | 备注 |
|------|---------|------|
| Kali Linux 2022.x（kernel 5.18+） | ✅ | 需禁用 btusb，需更新固件 |
| Kali Linux 2024.x / 2025.x | ⚠️ | Kernel 6.11+ BT/WiFi 冲突问题，不稳定 |
| Ubuntu 24.04（kernel 6.8+） | ⚠️ | 2024 年底有问题回报 |
| Ubuntu 25.04 / CachyOS（kernel 6.14+） | ✅ | 即插即用，新版 kernel 改善明显 |
| Debian 12 | ⚠️ | 视 kernel 版本而定 |
| Raspberry Pi 4 / 5 | ⚠️ | 有成功案例，但需确认固件版本并禁用 BT |

### AWUS036AX / AWUS036AXER（RTL8832BU）

| 平台 | Soft AP | 备注 |
|------|---------|------|
| Kali Linux | ✅ | kernel 6.17+ 内置 rtw89_8852bu；较旧 kernel 需社区 DKMS 驱动 |
| Ubuntu / Debian | ✅ | Ubuntu 24.04 需 HWE kernel 6.17+（GA 6.8／HWE 6.14 需社区 DKMS 驱动）；Debian 需 kernel 6.17+ |
| Raspberry Pi 4 / 5 | ⚠️ | 未在树莓派上测试；kernel 低于 6.17 需社区 DKMS 驱动 |

---

## 八、Soft AP 完整设置步骤（AWUS036ACM）{#setup-guide}

以下以 AWUS036ACM 在 Raspberry Pi 4 上创建 5GHz Soft AP 为例，提供从头到尾的完整步骤。

### Step 1：确认网卡辨识与驱动

```bash
# 确认网卡已辨识
lsusb | grep MediaTek
# 预期输出: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# 检查驱动已加载
dmesg | grep mt76
# 预期输出: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

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

创建 `/etc/hostapd/hostapd.conf`：

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1 非 DFS, 最安全
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT 设置 (MT7612U 专用)
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

创建 `/etc/dnsmasq.conf`：

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Step 5：设置静态 IP 与 NAT

```bash
# 为 wlan0 设置静态 IP
sudo ip addr add 192.168.10.1/24 dev wlan0

# 启用 IP 转送
sudo sysctl net.ipv4.ip_forward=1

# 设置 NAT (假设 eth0 是上游网络接口)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# 永久存储 iptables 规则
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

# 让 hostapd 开机自动启动
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

完成后，用手机或笔电搜索 WiFi，应该可以看到 `Yupitek_AP` 这个 SSID。

---

## 九、常见疑难排解 {#troubleshooting}

### Q1：hostapd 启动后直接崩溃

**症状**：`sudo systemctl status hostapd` 显示 `exited` 或 `failed`

**可能原因**：`hostapd.conf` 中的 `ht_capab` 包含芯片不支持的能力标志

**解法**：移除多余的标志。对 MT7612U（ACM）而言，使用本文第 3 节提供的设置档是最安全的选择。**不要复制其他芯片的 ht_capab 设置。**

---

### Q2：客户端连接后无法上网

**症状**：WiFi 已连接，取得 IP，但 ping 8.8.8.8 无回应

**检查清单**：

```bash
# 1. 检查 IP 转送是否启用
cat /proc/sys/net/ipv4/ip_forward
# 应输出: 1

# 2. 检查 NAT 规则是否存在
sudo iptables -t nat -L POSTROUTING -v
# 应该能看到 MASQUERADE 规则

# 3. 确认上游网络接口是否正常
ping -I eth0 8.8.8.8
```

---

### Q3：5GHz AP 找不到或断断续续

**可能原因**：

1. **使用了 DFS 频道（100–144）**：MT7612U / MT7610U 缺乏 DFS 支持，应使用 UNII-1 频道（36–48）
2. **发射功率不足**：确认天线已正确锁紧于 RP-SMA 接头
3. **USB 供电不足**（Raspberry Pi）：使用官方 5A 电源或外置有源 USB Hub

---

### Q4：Raspberry Pi 上的 hostapd 一直重启

**症状**：`dmesg` 中出现大量 USB reset 消息

**可能原因**：USB 端口供电不足（特别是 AWUS036ACH 高耗电芯片，最大 800mA）

**解法**：
- 使用官方 Pi 5A 电源供应器
- 使用外部有源 USB Hub
- 将网卡插入 USB 3.0 端口（Pi 4 才有）

---

### Q5：AWUS036AXML/AXM 的 WiFi 突然断线或无法启动

**可能原因**：Bluetooth 子系统干扰 WiFi（MT7921AUN 内建 BT 5.2）

**解法**：永久禁用蓝牙驱动

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 十、技术深入：VIF、WPA3、DFS 频道 {#technical}

### VIF（虚拟接口）：一张卡同时做多件事

VIF（Virtual Interface）让同一张物理网卡可以同时以多个逻辑接口运作。例如：一个接口连上游路由器（managed 模式），同时另一个接口作为 AP（master 模式）供其他设备连入。

三种常见场景的需求分析：

| 场景 | 是否需要 VIF | 最佳网卡 |
|------|-------------|---------|
| 基本 NAT 路由（eth0 上游 + wlan AP） | ❌ 不需要 | 所有支持 AP 的即可 |
| 无线桥接（WiFi 接收 + WiFi AP 同时） | ✅ 需要 | ACM（MT7612U） |
| 监控 + AP 同时（安全研究 / Rogue AP） | ✅ 需要 | ACM（MT7612U） |

**VIF 实战示例（MT7612U）：**

```bash
# 在现有 wlan1 之外建立额外的 AP 虚拟接口
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# 现在 wlan1 可以连上游网络, ap0 跑 hostapd
```

仅 MediaTek in-kernel 驱动（mt76x2u、mt7921u）完整支持 VIF。Realtek out-of-kernel 驱动基本上无此能力，若需要 AP + Monitor 同时运作，必须使用两张不同的网卡。

---

### WPA3 支持对照表

| 芯片 | 对应型号 | WPA2 | WPA3 |
|------|---------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ 原生支持 SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ 原生支持 SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ 宣称支持但实际无效 |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ kernel 6.17 实测可用（`sae_pwe=0`，MFP 启用） |

---

### 5GHz Soft AP 的频道选择：避开 DFS

DFS（Dynamic Frequency Selection）频道（ch100–ch140）需要 kernel 层面的雷达检测机制。MT7612U 等芯片缺乏 DFS 支持，使用 5GHz AP 时应选择：

| 频段 | 建议频道 | 原因 |
|------|---------|------|
| **UNII-1** | **36, 40, 44, 48** | 全芯片支持，最安全的选择 |
| UNII-2（DFS） | 52–144 | 大部分不支持，不建议 |
| UNII-3 | 149–165 | 部分支持（依地区法规） |

---

## 十一、社区真实案例整理 {#real-cases}

### 案例 1：RPi4B + AWUS036ACM = 长期稳定家用 5GHz AP

**来源**：morrownr/7612u GitHub 知识库
**场景**：morrownr 长期以 RPi4B + AWUS036ACM 作为家用 5GHz AP，搭配 Pi 内建 2.4GHz 提供双频服务
**结果**：长期稳定运作，无需重启，「outstanding」评价
**配置**：hostapd + dnsmasq + iptables NAT

### 案例 2：RPi3B+ + ACM — 初始崩溃，调整后成功

**来源**：[GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**问题**：在 RPi3B+ 上以 USB 2.0 端口运行，hostapd 崩溃
**根本原因**：`ht_capab` 包含 USB 2.0 带宽限制下不支持的 HT40 设置标志
**解决**：移除多余标志后，在 Kali Linux 上成功启动

### 案例 3：Pi PwnBox + AWUS036ACH = 红队测试 Rogue AP

**来源**：GitHub koutto/pi-pwnbox-rogueap
**场景**：以 RPi3B+ 创建 Rogue AP 平台：一张 RTL8812AU（AWUS036ACH）负责跑 AP，另一张 RT3070（AWUS036NEH）负责数据包注入攻击
**关键发现**：因 RTL8812AU 不支持 VIF，必须使用两张卡分工（而非像 ACM 可以单卡搞定）

### 案例 4：AWUS036AXML 在 RPi3B ArchLinux ARM 上稳定跑 AP

**来源**：[GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**场景**：用户在 RPi3B ArchLinux aarch64 上成功跑 AWUS036AXML AP 模式
**评语**：「It's the most stable mt7921 in my collection.」
**关键条件**：从 git 编译最新版 hostapd，并禁用 btusb

### 案例 5：AWUS036ACHM（MT7610U，已停产）在 Pi4 上达到全速 AP

**来源**：[GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**问题**：初始配置只达 65 Mbps link speed，未达 AC 5GHz 全速
**解决**：加入正确的 `vht_oper_chwidth=1` 和 `vht_oper_centr_freq_seg0_idx` 设置后达到 433 Mbps link rate
**对于 ACM 的启示**：同样的 VHT 参数设置对 MT7612U（ACM）也至关重要

---


{{< faq >}}

## 十二、选购建议与最终结论 {#recommendations}

### 快速决策指南

| 推荐等级 | 型号 | 适合对象 | 一句话总结 |
|---------|------|---------|-----------|
| 🥇 **首选** | **AWUS036ACM** | 所有人，尤其第一次创建 Soft AP | 全平台稳定，零烦恼 |
| 🥈 有条件可用 | AWUS036ACH | 已拥有此型号的用户 | 需装驱动，无 WPA3 |
| 🥉 进阶选择 | AWUS036AXML | 需要 WiFi 6E 且愿意花时间调校 | 6GHz 优势，需手动排除问题 |
| ✅ kernel 6.17+ 可用 | AWUS036AX / AXER | Wi-Fi 6 AP，同时可用于 monitor 与注入 | 内置驱动；2.4 / 5 GHz AP、VIF 已实测，WPA3 于 2.4 GHz 实测 |

### 🎯 简明决策指南

- **需要在 Kali Linux / Ubuntu / Debian / Raspberry Pi 4 或 5 上创建稳定 Soft AP？**
  → 直接选 **AWUS036ACM**，没有有之一。

- **已有 AWUS036ACH，想测试 Soft AP？**
  → 可以用，但只支持 WPA2，且需要安装驱动。接受这些限制的话没有问题。

- **需要 WiFi 6E（6GHz 频段）且愿意花时间设置？**
  → AWUS036AXML，记得禁用 BT 驱动、确认 kernel ≥ 6.6 LTS。

- **主要目的是 Soft AP 而非渗透测试？**
  → AWUS036ACM 是唯一在所有平台上均有大量验证案例的选择。

---

### 结语

创建 Soft AP 的核心关键，不在于 WiFi 速率有多快，也不在于天线有几根——**真正的关键，是芯片驱动对 AP 模式的支持程度。**

在我们调查的所有 ALFA 产品中，**AWUS036ACM（MT7612U）** 是唯一同时满足「in-kernel 驱动、WPA3 原生支持、VIF 虚拟接口、低耗电、全平台稳定」的选择。morrownr 亲测、GitHub 社区验证、eBay 用户背书——ACM 是 Soft AP 用途中，你唯一不会后悔的选择。

AWUS036ACH（RTL8812AU）可以用，但需要接受 WPA3 不支持和驱动维护成本。AWUS036AXML/AXM（MT7921AUN）潜力很大，但目前驱动成熟度仍在路上。AWUS036AX/AXER（RTL8832BU）在 kernel 6.17 以上以内置驱动即可使用（AP、VIF、WPA3 已实测）；旧 kernel 需社区 DKMS 驱动。

**如果你是第一次尝试在 Raspberry Pi 或 Kali Linux 上创建 Soft AP——选 ACM。**

---

### 购买链接

- [AWUS036ACM — Soft AP 首选](/zh-cn/products/alfa/awus036acm/)
- [AWUS036ACH — 经典渗透测试卡](/zh-cn/products/alfa/awus036ach/)
- [AWUS036AXML — WiFi 6E 三频旗舰](/zh-cn/products/alfa/awus036axml/)
- [ALFA Network 全系列产品](/zh-cn/products/alfa/)

### 延伸阅读

- [AWUS036ACH vs AWUS036ACM：芯片驱动方式完整比较](/zh-cn/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM IBSS & Mesh on Raspberry Pi](/zh-cn/blog/)
- [morrownr/USB-WiFi — 最权威的 Linux USB WiFi 知识库](https://github.com/morrownr/USB-WiFi)（4,100+ stars）
- [morrownr/7612u — MT7612U 专属文档（含 RPi4B Bridged AP 完整教程）](https://github.com/morrownr/7612u)
- [DeepWiki — morrownr/USB-WiFi 自动整理知识库](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 数据来源

本文数据汇整自：
- **morrownr/USB-WiFi** GitHub 知识库（4,100+ stars）及完整的 iw_list 记录
- **morrownr/7612u** — MT7612U Bridged AP on RPi4B 完整教程
- **GitHub issue tracker** — issue #2（ACM AP 设置）、#476（AXML AP 测试）、Discussion #31（ACHM 全速 AP）
- **koutto/pi-pwnbox-rogueap** — Alfa 网卡 RogueAP 实战案例
- **Rokland** 授权零售商 Linux 支持页面
- **Lab401** 技术评测与 2025 渗透测试最佳选择报告
- **Raspberry Pi 官方论坛** — Pi 4/5 USB WiFi 兼容性讨论
- **Yopitek 现有博客** — ACM China Install Guide、AXML WiFi 6E Review、Kali Linux 2026 最佳网卡

---

> **标签**：#ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi4 #RaspberryPi5 #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #LinuxWiFiAP #USB无线网卡 #树莓派WiFi热点 #Yopitek
>
> **作者**：榆閤科技 (Yopitek Ltd) — ALFA Network 台湾授权总代理
>
> **免责声明**：本文研究数据截至 2026 年 5 月。Linux Kernel 与各发行版持续更新，驱动支持状况可能随版本变动。部署前建议确认目标平台的 kernel 版本与驱动兼容性。
>
> **技术支持**：如有 Soft AP 设置问题，欢迎联系榆閤科技台湾本地技术支持团队。产品购买与咨询请至 [yupitek.com](/zh-cn/)。

## 参考文献

1. [morrownr/USB-WiFi GitHub 知识库](https://github.com/morrownr/USB-WiFi)
2. [hostapd 官方文档](https://w1.fi/cgit/hostap/)
3. [Linux Wireless mt76 驱动程序](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Raspberry Pi 官方文档](https://www.raspberrypi.com/documentation/)
5. [Kali Linux 官方文档](https://www.kali.org/docs/)
