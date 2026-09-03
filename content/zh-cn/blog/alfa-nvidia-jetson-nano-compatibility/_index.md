---
title: "ALFA 无线网卡是否支持 NVIDIA Jetson Nano"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "边缘 AI / 单板电脑"
description: "Jetson Nano 可使用多数 ALFA 网卡，但关键限制在于 JetPack 4.x 的 Linux kernel 4.9 版本较旧（判定母体：ALFA 现役 9 款 USB 网卡，其中 3 款成熟可用、2 款需进阶编译、2 款未验证、2 款不可用）。Realtek 晶片机型（AWUS036ACH / ACS / EACS）可直接编译 out-of-tree 驱动，是 Jetson N..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 问题摘要

客户询问：「ALFA 系列 USB 无线网卡能否在 NVIDIA Jetson Nano 开发板上使用？」

简短结论：Jetson Nano 可使用多数 ALFA 网卡，但关键限制在于 JetPack 4.x 的 Linux kernel 4.9 版本较旧（判定母体：ALFA 现役 9 款 USB 网卡，其中 3 款成熟可用、2 款需进阶编译、2 款未验证、2 款不可用）。Realtek 晶片机型（AWUS036ACH / ACS / EACS）可直接编译 out-of-tree 驱动，是 Jetson Nano 上的实用选择；MediaTek MT7612U / MT7610U 需 backport 或自行编译 mt76 驱动；Wi-Fi 6E 的 MT7921AUN 机型（AWUS036AXML / AXM）因需要 kernel 5.19+，在 Jetson Nano 上实际不可用。渗透测试场景首选 AWUS036ACH（RTL8812AU），一般上网场景首选 AWUS036ACH（稳定）或 AWUS036ACM（需编译 mt76）。

## 2. 分析目标硬体规格架构

### 2.1 NVIDIA Jetson Nano 硬体规格

| 项目 | 规格 |
|---|---|
| 模组 | Jetson Nano 模组（P3448） |
| CPU | Quad-core ARM Cortex-A57（ARMv8-A / aarch64） |
| GPU | NVIDIA Maxwell 架构，128 CUDA 核心 |
| 记忆体 | 4GB LPDDR4（64-bit，25.6 GB/s） |
| 储存 | microSD（开发板）/ eMMC（生产版模组） |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B（Device Mode / 供电） |
| 网路 | 1x Gigabit Ethernet（RJ45） |
| 无线 | 无内建 WiFi / 蓝牙（需外接 USB 或 M.2 扩充） |
| 供电 | 5V/4A DC 接头（建议）或 micro-USB 5V/2A |
| 尺寸 | 100mm × 80mm（开发板） |

### 2.2 软体环境：JetPack 4.x

| 项目 | 内容 |
|---|---|
| 作业系统 | Linux for Tegra（L4T），基于 Ubuntu 18.04 LTS |
| Kernel 版本 | Linux 4.9（L4T R32.x / JetPack 4.6.x） |
| 架构 | aarch64（ARM64） |
| 编译器 | GCC 7.5（预设）/ GCC 8（可安装） |
| 最新版本 | JetPack 4.6.4（L4T R32.7.4），已进入维护模式 |
| 后续升级 | Jetson Nano 不支持 JetPack 5.x（kernel 5.10），因硬体限制 |

### 2.3 关键限制：Kernel 4.9

Jetson Nano 的 kernel 4.9 是相容性判定的核心变数：

| 驱动 | 进入 mainline 的 kernel 版本 | Jetson Nano（kernel 4.9）可用性 |
|---|---|---|
| mt76x2u（MT7612U） | 4.19 | ❌ 需 backport / 自行编译 |
| mt76x0u（MT7610U） | 4.19 | ❌ 需 backport / 自行编译 |
| mt7921u（MT7921AUN） | 5.19 | ❌ 无法实用（差距过大） |
| rtl8812au（RTL8812AU） | 从未进入 mainline | ✅ 可编译 out-of-tree 驱动 |
| rtl8821cu（RTL8811CU） | 从未进入 mainline | ✅ 可编译 out-of-tree 驱动 |
| rtw89（RTL8832BU） | 5.16（PCIe）/ USB 陆续合入 | ❌ 需自行编译，相容性未知 |

### 2.4 USB 供电限制

Jetson Nano 开发板的 4 个 USB 3.0 Type-A 埠共用电源预算：

- 使用 DC 供电（5V/4A）时，USB 埠总输出约 1.5A（5V）
- 使用 micro-USB 供电（5V/2A）时，USB 埠总输出仅约 0.5A
- ALFA 高功率网卡（AWUS036ACH）峰值可达 800mA-1A
- 建议：使用 DC 供电 + 有电源的 USB 3.0 Hub，避免供电不足导致断线或系统重启

## 3. 分析目前 ALFA 网路卡规格和晶片组

截至 2026 年 9 月，ALFA Network 现役 USB 无线网卡产品线如下：

| 机型 | Wi-Fi 等级 | 晶片组 | 介面 | Jetson Nano 适用性 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ 需 kernel 5.19+，不可用 |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ 同上 |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 需自编 rtl8852bu，未验证 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ 编译 morrownr/8812au，成熟 |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ⚠️ 需 backport mt76x0u |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ⚠️ 需 backport mt76x2u |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ✅ 由 8812au 驱动涵盖 |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ✅ 编译 morrownr/8821cu |

## 4. 适用机型与晶片组

### 4.1 推荐等级分类

| 推荐等级 | 机型（晶片组） | 说明 |
|---|---|---|
| ⭐ 强烈推荐（渗透测试） | AWUS036ACH（RTL8812AU） | 驱动成熟，支持 Monitor Mode + Packet Injection，Jetson Nano 上最常被使用的 ALFA 网卡 |
| ✅ 推荐（一般上网） | AWUS036ACH（RTL8812AU） | 双频 AC1200，驱动安装简单，稳定 |
| ✅ 推荐（低功耗） | AWUS036EACS（RTL8811CU） | AC600 双频，USB 2.0 低功耗，适合简单上网 |
| ✅ 推荐（入门） | AWUS036ACS（RTL8811AU） | AC433 双频，由 8812au 驱动涵盖 |
| ⚠️ 可用但需手动编译 | AWUS036ACM（MT7612U） | 需 backport mt76 驱动到 kernel 4.9，技术门槛较高 |
| ⚠️ 可用但需手动编译 | AWUS036ACHM（MT7610U） | 同上，仅 433Mbps |
| ⚠️ 未验证 / 不建议 | AWUS036AX / AXER（RTL8832BU） | Wi-Fi 6，需编译 rtl8852bu，kernel 4.9 相容性未验证 |
| ❌ 不可用 | AWUS036AXML / AXM（MT7921AUN） | Wi-Fi 6E，需 kernel 5.19+，Jetson Nano 无法升级 |

### 4.2 使用场景建议

| 使用场景 | 建议机型 | 说明 |
|---|---|---|
| 无线渗透测试 / 监听 / 注入 | AWUS036ACH | RTL8812AU 驱动支持 Monitor + Injection，社群验证充分 |
| 机器人 / 无人机无线控制 | AWUS036ACH 或 AWUS036EACS | 稳定连线，低延迟 |
| 一般 IoT 闸道上网 | AWUS036EACS / ACS | 低功耗，USB 2.0 即可，省电 |
| 需要 5GHz 高速上网 | AWUS036ACH | AC1200，5GHz 867Mbps |
| Wi-Fi 6 / 6E 需求 | ❌ 无可用选项 | Jetson Nano 不支持现代 Wi-Fi 6/6E 晶片 |

## 5. 环境需求

### 5.1 硬体需求

| 项目 | 最低需求 | 建议 |
|---|---|---|
| Jetson Nano 开发板 | B01 / A02 版本均可 | B01（2 条 CSI 摄影机埠） |
| 供电方式 | 5V/2A micro-USB | 5V/4A DC 接头（USB 设备多时必须） |
| USB Hub | 可不用 | 有电源的 USB 3.0 Hub（使用高功率网卡时） |
| 散热 | 散热片（预设附带） | 风扇 + 散热片（长时间高负载时） |
| 储存 | 16GB microSD | 32GB+ UHS-I microSD（编译驱动需要空间） |

### 5.2 软体需求

| 项目 | 需求 |
|---|---|
| JetPack 版本 | 4.6.x（L4T R32.7.x） |
| 核心工具 | build-essential、git、bc、libssl-dev、flex、bison |
| Kernel 原始码 | 需要下载对应 L4T 版本的 kernel source（编译 mt76 backport 时） |
| 网路 | 编译期间需有线网路连线（透过 Gigabit Ethernet 埠） |

## 6. 相容性判定

### ALFA 现役机型 × NVIDIA Jetson Nano 相容性矩阵

| 机型 | 晶片组 | 驱动方式 | USB 侦测 | STA 上网 | AP 模式 | Monitor | 安装难度 | 综合评价 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 编译 8812au | ✅ | ✅ | ✅ | ✅ | 中 | ⭐ 最佳 |
| AWUS036ACS | RTL8811AU | 8812au 涵盖 | ✅ | ✅ | ⚠️ | ❌ | 中 | ✅ 良好 |
| AWUS036EACS | RTL8811CU | 编译 8821cu | ✅ | ⚠️ | ❌ | ❌ | 中 | ✅ 良好 |
| AWUS036ACM | MT7612U | backport mt76x2u | ✅ | ✅ | ✅ | ✅ | 高 | ⚠️ 可用 |
| AWUS036ACHM | MT7610U | backport mt76x0u | ✅ | ✅ | ⚠️ | ⚠️ | 高 | ⚠️ 可用 |
| AWUS036AX | RTL8832BU | 编译 rtl8852bu | ⚠️ | ❌ | ❌ | ❌ | 高 | ❌ 不建议 |
| AWUS036AXER | RTL8832BU | 同上 | ⚠️ | ❌ | ❌ | ❌ | 高 | ❌ 不建议 |
| AWUS036AXML | MT7921AUN | 需 kernel 5.19+ | ❌ | ❌ | ❌ | ❌ | — | ❌ 不可用 |
| AWUS036AXM | MT7921AUN | 同上 | ❌ | ❌ | ❌ | ❌ | — | ❌ 不可用 |

判定依据：Jetson Nano JetPack 4.x kernel 4.9 的驱动可用性 + 社群实测回报（Jetson Nano 论坛、GitHub morrownr 驱动 issue）。MT7921AUN 因 Jetson Nano 无法升级至 kernel 5.19+，判定为不可用。

## 7. 超详细 Step by Step 设定步骤

### 7.1 前置作业：系统更新与编译环境

**步骤 1：开机并透过 SSH 登入 Jetson Nano**

```bash
ssh username@<jetson-nano-ip>
```

**步骤 2：更新系统套件**

```bash
sudo apt update
sudo apt upgrade -y
```

**步骤 3：安装编译工具与依赖**

```bash
sudo apt install -y build-essential git bc libssl-dev flex bison dkms
```

**步骤 4：确认 kernel 版本**

```bash
uname -r
# 预期输出：4.9.337-tegra（或类似 4.9.x-tegra）
```

### 7.2 路径 A：Realtek 晶片机型（AWUS036ACH / ACS / EACS）— 推荐

以 AWUS036ACH（RTL8812AU）为例：

**步骤 1：下载驱动原始码**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**步骤 2：（可选）调整编译参数 for ARM64**

编辑 Makefile，确认以下设定：

```
CONFIG_PLATFORM_ARM64 = y
```

（多数新版本 Makefile 已自动侦测 aarch64）

**步骤 3：编译与安装**

```bash
make
sudo make install
```

**步骤 4：载入驱动模组**

```bash
sudo modprobe 8812au
# 或重新开机
sudo reboot
```

**步骤 5：插入 ALFA 网卡，确认网路介面**

```bash
ip link show
# 预期出现 wlan0 介面
# 若无，检查 dmesg
dmesg | grep -i "8812au\|rtl8812\|usb"
```

**步骤 6：扫描 WiFi 网路（验证功能）**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**步骤 7：连线到 WiFi 网路（使用 NetworkManager / nmcli）**

```bash
# Jetson Nano 预设安装 NetworkManager
nmcli dev wifi list
nmcli dev wifi connect "你的WiFi名称" password "你的WiFi密码"
```

**步骤 8：（可选）设定为 AP 热点模式**

```bash
# 安装 hostapd 与 dnsmasq
sudo apt install -y hostapd dnsmasq
# 参考 ALFA Soft AP 指南进行设定
# https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/
```

**步骤 9：启用监听模式（渗透测试用）**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# 验证
sudo iw dev wlan0 info
# type 应显示 monitor
# 测试封包注入
sudo aireplay-ng --test wlan0
```

### 7.3 路径 B：MediaTek 晶片机型（AWUS036ACM / ACHM）— 进阶

以 AWUS036ACM（MT7612U）为例，需 backport mt76 驱动：

**步骤 1：下载 Jetson Nano kernel 原始码**

```bash
# 根据 L4T 版本下载对应 kernel source
# 例如 L4T R32.7.4：
wget https://developer.nvidia.com/embedded/l4t/r32_release_v7.4/sources/public_sources.tbz2
tar -xjf public_sources.tbz2
cd Linux_for_Tegra/source/public
tar -xjf kernel_src.tbz2
```

**步骤 2：准备 kernel 编译环境**

```bash
cd kernel/kernel-4.9
# 产生预设设定
make tegra_defconfig
# 启用 mt76 相关选项（menuconfig）
make menuconfig
# 导航到：Device Drivers > Network device support > Wireless LAN
# 选取：<M> MediaTek MT76x2U USB support
# 选取：<M> MediaTek MT76x0U USB support
```

**步骤 3：编译 kernel modules**

```bash
make modules_prepare
make M=drivers/net/wireless/mediatek/mt76 modules
```

**步骤 4：安装模组**

```bash
sudo make M=drivers/net/wireless/mediatek/mt76 modules_install
sudo depmod -a
```

**步骤 5：载入驱动**

```bash
sudo modprobe mt76x2u
# 插入 AWUS036ACM
dmesg | grep mt76
ip link show
```

⚠️ 注意：backport mt76 到 kernel 4.9 可能遇到编译错误，需要手动修补原始码。这是进阶操作，建议仅对 kernel 编译有经验的使用者尝试。若遇到困难，建议改用 AWUS036ACH（RTL8812AU）。

### 7.4 路径 C：Wi-Fi 6 / 6E 机型（AWUS036AX / AXER / AXML / AXM）

- AWUS036AXML / AXM（MT7921AUN）：不可用。Jetson Nano 的 kernel 4.9 无法升级至 5.19+，mt7921u 驱动无法 backport（差距过大，依赖现代 kernel 基础设施）。
- AWUS036AX / AXER（RTL8832BU）：不建议。理论上可尝试编译 morrownr/rtl8852bu 驱动，但 kernel 4.9 相容性未经社群验证，且 Wi-Fi 6 功能可能无法正常运作。若需要 Wi-Fi 6，建议使用 Jetson Orin Nano（JetPack 5.x，kernel 5.10+）或 x86 电脑。

## 8. 常见错误与排解

| 症状 | 可能原因 | 排解方式 |
|---|---|---|
| 插入网卡后 dmesg 无任何反应 | USB 供电不足 / 接触不良 |使用 DC 供电（5V/4A）；更换 USB 埠；使用有电源 USB Hub |
| make 编译 8812au 时报错 gcc: error: unrecognized command line option | GCC 版本过旧 | 安装 GCC 8：`sudo apt install gcc-8 g++-8`，并在 Makefile 中指定 `CC = gcc-8` |
| modprobe 8812au 报 Required key not available | Secure Boot 启用（Jetson Nano 通常无此问题） | 确认 Jetson Nano 未启用 Secure Boot；重新签章模组或关闭 Secure Boot |
| wlan0 介面出现但无法扫描 AP | Regulatory Domain 未设定 / 驱动韧体缺失 | 设定法规区域：`sudo iw reg set TW`；检查 dmesg 是否有 firmware 载入错误 |
| 高功率输出时系统重启或网卡断线 | USB 供电不足 | 使用 DC 供电 + 有电源 USB Hub；降低 TX Power：`sudo iw dev wlan0 set txpower fixed 2000` |
| 监听模式下 aireplay-ng --test 显示 Injection is working! 但实际攻击无效 | 驱动注入功能有限 / 通道冲突 | RTL8812AU 注入功能基本可用；确认 `airmon-ng check kill` 已停止 NetworkManager；尝试不同通道 |
| mt76 backport 编译失败 | kernel 4.9 与现代 mt76 原始码差距过大 | 尝试使用较旧版本的 mt76（对应 kernel 4.19 时期的 commit）；或改用 AWUS036ACH |
| 系统唤醒后网卡消失 | USB 省电设定 | 停用 USB 自动暂停：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |
| AWUS036ACH 的 5GHz 无法使用 | 法规区域限制 / 驱动通道表 | 设定 `sudo iw reg set US`（美国法规开放较多 5GHz 通道）；确认使用的通道在当地法规允许范围 |

## 9. 已知限制

- Kernel 版本冻结在 4.9：Jetson Nano 不支持 JetPack 5.x，无法升级 kernel，这是所有相容性问题的根源
- MT7921AUN（Wi-Fi 6E）完全不可用：需要 kernel 5.19+，无法 backport 到 4.9
- MediaTek mt76 晶片需手动 backport：AWUS036ACM / ACHM 的使用者需自行编译 kernel module，技术门槛高
- ⚠️ **Wi-Fi 6（RTL8832BU）驱动维护者已公开建议避免使用**：驱动维护者 morrownr 在其官方公告中明确指出 rtl8852/32au 系列「是很糟糕的驱动，怀疑晶片本身有问题」，并建议 Linux 使用者现阶段避开此晶片（来源见第 10 节）。这比单纯「kernel 4.9 相容性未验证」更严重，本文与其他相关文件对 AWUS036AX / AXER 的判定应理解为「不建议」而非「可尝试但较麻烦」
- USB 供电限制：4 个 USB 埠共用约 1.5A（DC 供电时），高功率网卡需使用有电源 Hub
- AP 模式效能：Jetson Nano 的 CPU 效能有限，USB WiFi 做 AP 时吞吐量可能低于预期
- 监听 / 注入功能差异：RTL8812AU 支持最佳；MediaTek 晶片在 kernel 4.9 backport 后的注入功能可能不稳定
- Long-term 维护：JetPack 4.x 已进入维护模式，未来不会有新功能或驱动更新
- 蓝牙功能：AWUS036AXM 的蓝牙 5.2 功能在 Jetson Nano 上未验证（需 BlueZ 支持）
- 散热：长时间使用 USB WiFi 高功率输出时，Jetson Nano 的整体温度可能升高，建议加装风扇

反驳条件：以上判定以 JetPack 4.6.x（kernel 4.9）为前提。若 NVIDIA 未来为 Jetson Nano 释出 JetPack 5.x 支持（目前官方明确不支持），或社群出现稳定的 kernel 5.x backport，第 4 节的不可用判定需重新验证。

## 10. 参考来源 URL

| 来源 | 说明 | URL | 查核状态 | 查核日期 |
|---|---|---|---|---|
| NVIDIA Jetson Nano 官方页面 | Jetson Nano 硬体规格 | https://developer.nvidia.com/embedded/jetson-nano | ✅ 已查核 | 2026-09-03 |
| NVIDIA JetPack SDK 官方页 | JetPack 版本与 kernel 资讯 | https://developer.nvidia.com/embedded/jetpack | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驱动（Jetson Nano 适用） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux 驱动 | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | ALFA 在 Linux 上的 AP 模式设定指南 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA Network 产品总览（Yupitek） | ALFA 现役产品规格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驱动维护者官方声明：建议避开 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko 需 kernel 5.19+ 才会出现于核心（驱动维护者原话） | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 已查核 | 2026-09-03 |

相关文章：[ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)（GB10 平台对照，kernel 6.x 环境）｜[ALFA 无线网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

免责声明：本文相容性判定以 Jetson Nano JetPack 4.6.x（kernel 4.9）为基准。Realtek 晶片驱动为社群维护（morrownr），实际稳定性可能随版本变化。MediaTek mt76 晶片的 backport 操作需要 kernel 编译经验，不保证 100% 成功。若需要 Wi-Fi 6/6E 或现代 kernel 支持，建议升级至 Jetson Orin 系列（JetPack 5.x+）或使用 x86 电脑。
