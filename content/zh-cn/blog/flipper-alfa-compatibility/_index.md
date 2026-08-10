---
title: "Flipper Zero 与 Flipper One 搭配 ALFA 无线网卡：完整兼容性指南"
description: "Flipper Zero 能接 ALFA USB 无线网卡做数据包注入吗？不行——这里解释为什么。Flipper One 支持 ALFA AWUS036AXML，完整监听模式与数据包注入。包含芯片分析、驱动兼容性与设置步骤的完整指南。"
date: 2026-06-10
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-alfa-compatibility"
tags: ["flipper-zero", "flipper-one", "alfa-network", "wifi-adapter", "monitor-mode", "packet-injection", "kali-linux", "pentesting", "AWUS036AXML", "wireless-security"]
categories: ["Technical"]
featureimage: "/images/blog/flipper-alfa-compatibility.webp"
faq:
  - question: "Flipper Zero 可以连接 ALFA USB 无线网卡吗？"
    answer: "不行。Flipper Zero 的 STM32WB55 微控制器仅支持 USB device 模式，硬件上无法作为 USB host 驱动外接网卡。"
  - question: "Flipper One 支持哪些 ALFA 网卡型号？"
    answer: "Flipper One 创办人特别测试 AWUS036AXML 为首选，AWUS036ACM 为最佳 CP 值，两者驱动皆已内置于 mainline Linux 核心。"
  - question: "为什么 AWUS036AXML 是 Flipper One 首选网卡？"
    answer: "AWUS036AXML 采用 MT7921AUN 芯片，mt7921u 驱动自 Linux 5.18 起内置于核心，支持完整 2.4/5/6 GHz 三频段与监听模式。"
  - question: "Flipper One 何时正式上市？"
    answer: "Flipper One 当前处于开发者预览阶段，正式上市时间与定价将通过群众募资公布，详情请追踪 flipper.net。"
  - question: "Flipper Zero 的 WiFi Dev Board 能取代 ALFA 网卡吗？"
    answer: "不能。WiFi Dev Board 仅支持 2.4 GHz 基本功能，无 USB host，范围与注入可靠性远不及专用 ALFA 网卡。"
---




{{< alert "triangle-exclamation" >}}
**法律声明：** Monitor Mode 与 Packet Injection 仅限于在您拥有或已取得明确书面授权的网络上进行测试。未经授权的无线通信拦截在大多数司法管辖区属违法行为。本指南中的所有技术仅供**授权渗透测试、自有设备安全研究及教育目的**使用。
{{< /alert >}}

{{< tldr >}}
Flipper Zero 的 STM32WB55 仅支持 USB device 模式，无法驱动任何 ALFA 网卡；Flipper One 搭载 RK3576 与完整 Debian Linux，支持 AWUS036AXML 执行三频监听与注入。
{{< /tldr >}}

如果你拥有一台 Flipper Zero——或正在考虑购买——而且听过 ALFA Network 在无线安全测试领域大名鼎鼎的 USB 无线网卡，你可能也问过自己：**"我可以把 ALFA 网卡插到 Flipper Zero 上，开始捕获 WPA2 握手数据包吗？"**



## 前言：每个渗透测试人员都会问的问题

如果你拥有一台 Flipper Zero——或正在考虑购买——而且听过 ALFA Network 在无线安全测试领域大名鼎鼎的 USB 无线网卡，你可能也问过自己：**"我可以把 ALFA 网卡插到 Flipper Zero 上，开始捕获 WPA2 握手数据包吗？"**

简短的答案是：不行——但完整的答案有趣多了。

**Flipper Zero 无法连接任何 ALFA USB 无线网卡。** 这是硬件限制，不是软件问题。Flipper Zero 内部的 STM32WB55 微控制器，其 USB 控制器只能在 **device-only 模式**下运作——它物理上无法作为 USB host 来驱动外部设备，例如 WiFi 网卡。

但 Flipper Devices 已经宣布了一款全新的产品：**Flipper One**。基于 Rockchip RK3576 处理器，配备 8 GB 内存，运行完整的 Debian Linux，Flipper One 拥有两个 USB 3.1 host 端口，可以直接使用 ALFA 网卡进行完整的无线安全测试——包括 6 GHz Wi-Fi 6E 分析。事实上，Flipper One 创始人 Pavel Zhovner 在产品公告中，特别指名 **ALFA AWUS036AXML** 为官方测试网卡。

本文将完整说明兼容性全貌：什么能用、什么不行、为什么，以及如何设置。

---

## Flipper Zero：为什么不能使用 ALFA 网卡

要理解这个限制，你需要了解 Flipper Zero 内部有什么。

### 硬件规格

| 组件 | 规格 |
|-----------|--------------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **架构** | ARM Cortex-M4（应用核心）@ 64 MHz + ARM Cortex-M0+（无线核心）@ 32 MHz |
| **RAM** | 256 KB（核心之间共享） |
| **存储** | 1 MB Flash + MicroSD |
| **操作系统** | FreeRTOS（实时操作系统） |
| **USB** | USB Type-C，USB 2.0 Full Speed（12 Mbps） |
| **USB 模式** | **Device only**——无 host 或 OTG 能力 |

### USB 限制

STM32WB55 的 USB 控制器是一个 **USB Full-Speed Device Controller**。它可以让 Flipper Zero 以 USB 设备的身份连接到电脑（用于文件传输、固件更新和 CLI 界面），但无法作为 USB host。这颗芯片上没有 host 控制器硬件——再多的固件修改也无法增加这项能力。

要使用 ALFA USB 无线网卡，设备需要：
1. **USB Host 控制器硬件**——用于枚举并与 USB 设备通信
2. **Linux 内核与 WiFi 驱动支持**——加载 `mt7921u`、`mt76` 或 `rtw88` 等驱动程序
3. **足够的供电能力**——ALFA 网卡通常消耗 500 mA 至 900 mA @ 5V

Flipper Zero 三项全都不符合：
- ❌ 无 USB Host 控制器（硬件限制）
- ❌ 运行 FreeRTOS，非 Linux——不存在内核驱动框架
- ⚠️ GPIO 5V 输出在所有引脚总和不超 1.2A，且需手动启用

> **结论：** 将任何 ALFA USB 无线网卡连接到 Flipper Zero 是**物理上不可能**的。这不是可以通过软件、固件更新或扩展板绕过的硬件限制——它已刻在芯片设计中。

---

## Flipper Zero + WiFi Dev Board：有限的替代方案

Flipper Devices 销售一款基于 **ESP32-S2** 微控制器的官方 **WiFi Dev Board**。这块板子通过 GPIO 排针插入 Flipper Zero，提供基本的 2.4 GHz WiFi 功能——但它**不会**改变 USB host 的情况。

| 方面 | 能力 |
|--------|-----------|
| **WiFi 芯片** | ESP32-S2（Xtensa LX7 单核，240 MHz） |
| **频率** | 仅 2.4 GHz，802.11 b/g/n |
| **USB Host** | ❌ WiFi Dev Board 未暴露 USB Host——ESP32-S2 通过 GPIO 连接 Flipper Zero，非 USB |
| **固件** | ESP32 Marauder（社区开发） |

安装 **ESP32 Marauder 固件**后，WiFi Dev Board 可以执行：

- ✅ Deauthentication 攻击（仅 2.4 GHz）
- ✅ PMKID 捕获（仅 2.4 GHz）
- ✅ 接入点扫描与 SSID 广播
- ✅ 基本数据包嗅探（仅 2.4 GHz）

它**无法**做到：

- ❌ 使用外部 ALFA USB 网卡（无 USB host）
- ❌ 在 5 GHz 或 6 GHz 频段上运作
- ❌ 达到专用 ALFA 网卡的范围或注入可靠性
- ❌ 运行基于 Linux 的工具，如 aircrack-ng、Kismet 或 Wireshark

> **如果你只有 Flipper Zero 且需要基本的 2.4 GHz 测试**，WiFi Dev Board 搭配 ESP32 Marauder 是一个可行但**严重受限**的变通方案。若需要更多功能，你需要不同的硬件。

---

## Flipper One：ALFA 等待已久的平台

2026 年 5 月 21 日，Flipper Devices 创始人 Pavel Zhovner 发表了一篇博客文章，标题为 *"Flipper One — We Need Your Help"*，宣布了一款全新的产品。Flipper One 不是 Flipper Zero 的升级版——它是一个完全不同的设备类别，设计用于不同的协议层级。

> *"Flipper Zero 是 Layer 0——离线点对点访问控制：NFC、RFID、Sub-GHz、红外线。Flipper One 是 Layer 1——IP 连接：Wi-Fi、Ethernet、5G、卫星。两者不互相取代。"*
> —— Pavel Zhovner，flipper.net

{{< alert "circle-info" >}}
**供货状态提示：** Flipper One 目前处于**开发者预览**阶段。正式上市时间、定价及地区销售将通过众筹公布。请关注 [flipper.net](https://flipper.net) 和 [Flipper One Developer Portal](https://docs.flipper.net/one) 获取最新消息。
{{< /alert >}}

### 硬件规格

| 组件 | 规格 |
|-----------|--------------|
| **CPU** | Rockchip RK3576：4× Cortex-A72 + 4× Cortex-A53，最高 2.2 GHz |
| **GPU** | ARM Mali-G52 MC3（OpenGL ES 3.2、Vulkan 1.2） |
| **NPU** | 6 TOPS @ INT8（可本地运行 LLM） |
| **协处理器** | Raspberry Pi RP2350B（双 M33 + 双 RISC-V），负责屏幕/按键/电源 |
| **RAM** | 8 GB LPDDR5 |
| **存储** | 64 GB UFS 2.2 + MicroSD |
| **操作系统** | Debian 13（Trixie）——Flipper Devices 声称将采用 mainline Linux Kernel 7.0，无 out-of-tree patch 依赖 |
| **USB Host** | USB-C2 + USB-A，皆为 USB 3.1（5 Gbps），皆支持 host 模式 |
| **内置 WiFi** | Wi-Fi 6E via MT7921AUN（2.4/5/6 GHz，2×2 MIMO） |
| **Ethernet** | 2× RJ45 Gigabit（支持 inline/MitM 嗅探） |
| **M.2 扩展** | Key-B：PCIe 2.1 ×1 / USB 3.1 / SATA3 / SIM 卡 |

### 为什么 Flipper One 能使用 ALFA 网卡

与 Flipper Zero 不同，Flipper One 满足全部三项要求：

1. ✅ **USB 3.1 Host 控制器**：两个 host-capable USB 端口，可枚举并供电给外部设备
2. ✅ **完整 Debian Linux**：标准 Linux 内核，支持 `mt7921u`、`mt76` 和 `rtw88` 的 in-kernel 驱动
3. ✅ **充足供电**：USB 端口可提供标准总线电源；GPIO 提供 5V @ 2A 和 3.3V @ 2A，含 eFuse 保护

USB 3.1 的带宽（5 Gbps）绰绰有余——即使是最快的 ALFA 网卡（AWUS036AXML，AXE3000），也受限于 USB 3.0 的实际吞吐量约 1.2 Gbps。

### 软件环境

Flipper One 运行标准的 Debian 环境，意味着你可以直接通过 `apt` 安装无线安全工具：

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

Flipper One 还引入了 **Flipper OS Profiles**——一种基于快照的系统，让你可以创建干净、隔离的环境。你可以维护一个专门的"Pentest" profile，安装所有无线工具，并在需要日常使用时切换回干净的 profile，互不干扰。

---

## Flipper One 推荐 ALFA 网卡

并非所有 ALFA 网卡在无线安全测试上的表现都一样好。关键因素是**芯片组**、**驱动成熟度**和 **in-kernel 支持**（表示无需 DKMS 编译）。

### ⭐⭐⭐⭐⭐ 首选：AWUS036AXML（Wi-Fi 6E）

| 规格 | 详情 |
|------|--------|
| **芯片组** | MediaTek MT7921AUN |
| **频段** | 2.4 / 5 / 6 GHz（Wi-Fi 6E） |
| **最大速率** | AXE3000（理论值），实用约 1.2 Gbps |
| **驱动** | `mt7921u`——自 Linux 5.18 起 in-kernel |
| **需要 DKMS** | ❌ 不需要 |
| **天线** | 双 RP-SMA（可更换）+ Bluetooth 5.2 |

> **为什么是最佳选择：** 这是 Flipper One 创始人特别测试过的网卡。`mt7921u` 驱动已在 mainline kernel 中，无需任何 vendor patch。它支持全部三个 WiFi 频段（2.4/5/6 GHz），使 Wi-Fi 6E 安全评估具备前瞻性。Monitor Mode 和 Packet Injection 稳定且经过充分测试。

### ⭐⭐⭐⭐⭐ 最佳性价比：AWUS036ACM（Wi-Fi 5 AC1200）

| 规格 | 详情 |
|------|--------|
| **芯片组** | MediaTek MT7612U |
| **频段** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速率** | AC1200（300 + 867 Mbps） |
| **驱动** | `mt76`——自 Linux 4.19 起 in-kernel |
| **需要 DKMS** | ❌ 不需要 |
| **天线** | 双 5 dBi RP-SMA（可更换） |

> **为什么是最佳性价比：** MT7612U 芯片组在渗透测试社区中历经考验。`mt76` 驱动已在内核中存在多年，异常稳定。在内核 6.5 及以上版本中，Monitor Mode 和 Injection 运作无瑕。价格低于 AXML，为 2.4/5 GHz 测试提供最佳的价格能力比。

### ⭐⭐⭐⭐ 轻量选择：AWUS036ACHM（Wi-Fi 5 AC433）

| 规格 | 详情 |
|------|--------|
| **芯片组** | MediaTek MT7610U |
| **频段** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速率** | AC433（理论值） |
| **驱动** | `mt76`——自 Linux 4.19 起 in-kernel |
| **需要 DKMS** | ❌ 不需要 |
| **天线** | 单高增益 RP-SMA（可更换） |

> **为什么是轻量选择：** 最便携的选项——USB 2.0、单天线、最低功耗。使用与 ACM 相同的 `mt76` 驱动家族。适合重视体积与功耗胜过吞吐量的现场工作。**注意：** 在 ARM64 平台（包括 RK3576）上，同时运行 `airodump-ng` 和 `aireplay-ng` 可能触发已知的 interface 消失 bug（morrownr issue #379）。使用时请留意。

### ⭐⭐⭐ 替代方案：AWUS036ACH（Wi-Fi 5 AC1200，RTL8812AU）

| 规格 | 详情 |
|------|--------|
| **芯片组** | Realtek RTL8812AU |
| **频段** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速率** | AC1200（300 + 867 Mbps） |
| **驱动** | `rtw88`——预期在 Flipper One 规划的内核上为 in-kernel；旧系统可能需要 DKMS |
| **需要 DKMS** | ❌ Flipper One 上不需要 / ⚠️ 旧内核可能需要 [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS |
| **天线** | 双 6 dBi RP-SMA（高 TX 功率） |

> **为什么是替代方案：** RTL8812AU 芯片组在渗透测试领域历史悠久。预期在 Flipper One 规划的内核上无需额外 DKMS 模块即可支持。对于旧系统，aircrack-ng DKMS 驱动仍可使用。高增益 6 dBi 天线提供优异的覆盖范围，但 MediaTek 系列的网卡因其更成熟的 in-kernel 驱动支持而通常更受推荐。

### ⚠️ 不建议用于渗透测试

以下 ALFA 型号使用 Monitor Mode 和 Packet Injection 的 Linux 驱动不成熟或不稳定的 Realtek 芯片组。**请避免在 Flipper One 的无线安全工作中使用这些型号：**

| 型号 | 芯片组 | 问题 |
|-------|---------|-------|
| AWUS036AX | RTL8832BU | Wi-Fi 6 芯片，2026 年驱动支持仍在发展中 |
| AWUS036AXER | RTL8832BU | 与 AWUS036AX 相同的芯片组问题 |
| AWUS036ACS | RTL8811AU | Monitor Mode 有限，Injection 不稳定 |
| AWUS036EACS | RTL8811CU | Monitor Mode 有限，Injection 不稳定 |

---

## 设置指南：Flipper One + ALFA AWUS036AXML

本指南假设你有一台运行 Debian Linux 的 Flipper One，且网卡已实际连接到 USB host 端口。

### 步骤 1：确认网卡已被识别

```bash
# 检查 USB 设备枚举
lsusb
# 预期输出（示例）：
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# 列出无线接口
iw dev
# 预期：wlan0（若内置 WiFi 占用 wlan0，则为 wlan1）

# 替代检查方式
ip link show
```

### 步骤 2：确认驱动已加载

```bash
# AWUS036AXML / AWUS036AXM（MT7921AUN）：
lsmod | grep mt7921u

# AWUS036ACM / AWUS036ACHM（MT7612U / MT7610U）：
lsmod | grep mt76

# AWUS036ACH（RTL8812AU）：
lsmod | grep rtw88

# 检查内核版本（最佳 MT7921AUN 支持建议 6.12+）：
uname -r
```

如果驱动模块有列出，表示已加载且就绪。不需要进一步安装——这些全部都是 in-kernel 驱动。

### 步骤 3：启用 Monitor Mode

```bash
# 终止干扰进程（NetworkManager、wpa_supplicant 等）
# 注意：这也会同时中断 Flipper One 的内置 WiFi——请使用专用的
# Flipper OS Profile 进行渗透测试，避免干扰正常网络连接。
sudo airmon-ng check kill

# 在网卡上启动 Monitor Mode
sudo airmon-ng start wlan0
# 接口重命名为 wlan0mon

# 确认 Monitor Mode 已启用
iw dev wlan0mon info
# 应显示：type monitor
```

手动方法（若不偏好使用 airmon-ng）：

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### 步骤 4：测试 Packet Injection

```bash
# 测试注入能力
sudo aireplay-ng --test wlan0mon
# 看到 "Injection is working!" 表示成功

# 执行基本扫描
sudo airodump-ng wlan0mon

# 扫描所有支持频段（仅 AWUS036AXML）
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz（aircrack-ng 1.7+）

# 指定信道扫描
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### 步骤 5：捕获 WPA2 握手数据包

```bash
# Terminal 1：在目标信道上开始捕获
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Terminal 2：发送 deauth 强制重新连接
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# 在 Terminal 1 中查看握手捕获：
# 当出现 "WPA handshake: AA:BB:CC:DD:EE:FF" 表示已捕获
```

### 步骤 6：恢复正常操作

```bash
# 停止 Monitor Mode 并恢复 managed mode
sudo airmon-ng stop wlan0mon

# 重新启动网络服务
sudo systemctl restart NetworkManager
```

### 架构总览

下图展示 Flipper One 搭配 ALFA 网卡的完整无线渗透测试架构：

![Flipper One + ALFA 无线网卡渗透测试架构](diagram/flipper-alfa-topology.svg)

*拓扑：Flipper One 平台 → ALFA USB 网卡 → 渗透测试工具链 → 无线功能*

---

## Flipper Zero vs. Flipper One：并列对比

| 功能 | Flipper Zero | Flipper One |
|---------|:-----------:|:----------:|
| **操作系统** | FreeRTOS | Debian 13（Trixie） |
| **CPU** | STM32WB55（Cortex-M4，64 MHz） | RK3576（8 核 ARM，2.2 GHz） |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **存储** | 1 MB Flash + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB Host** | ❌ Device only | ✅ USB-C2 + USB-A（USB 3.1） |
| **ALFA 网卡支持** | ❌ | ✅ |
| **内置 WiFi** | ❌（仅 BLE） | ✅ Wi-Fi 6E（MT7921AUN） |
| **5 GHz / 6 GHz WiFi** | ❌ | ✅ |
| **Gigabit Ethernet** | ❌ | ✅ 2× RJ45 |
| **Monitor Mode** | ❌（原生） | ✅ |
| **Packet Injection** | ❌（原生） | ✅ |
| **M.2 扩展** | ❌ | ✅ Key-B（PCIe / USB 3.1 / SATA） |
| **价格** | ~$169 USD（量产中） | 开发者预览（众筹待公布） |

---


{{< faq >}}

## 结语：对的工具做对的事

如果你打算使用 ALFA 无线网卡进行无线安全测试，**Flipper Zero 是错误的平台**——这并非它的错。它被设计用于不同的目的：离线访问控制测试（NFC、RFID、Sub-GHz、红外线）。它在这些任务上表现出色，但 USB host 能力从未纳入其设计。

针对**Monitor Mode 和 Packet Injection 搭配 ALFA 网卡**的特定用途，你有两条路径：

| 路径 | 平台 | ALFA 网卡 | 能力 |
|------|----------|-------------|------------|
| **最佳** | Flipper One | AWUS036AXML（MT7921AUN） | 完整 2.4/5/6 GHz，in-kernel 驱动，官方支持 |
| **超值** | Flipper One | AWUS036ACM（MT7612U） | 完整 2.4/5 GHz，in-kernel 驱动，稳定性经过验证 |
| **变通** | Flipper Zero + WiFi Dev Board | 无（ESP32-S2 内置） | 仅 2.4 GHz，范围有限，基本功能 |

**Flipper One 代表了一次代际飞跃**——它将完整 Debian Linux 环境与 USB 3.1 host 能力的强大功能，带入一台便携式、专用硬件平台。搭配 ALFA AWUS036AXML（Flipper One 创始人特别测试的网卡），你就能在口袋中拥有一套完整的无线安全评估工具。

---

### 哪里买

所有推荐的 ALFA 网卡均可从 Yupitek——ALFA Network 授权经销商处购得。浏览完整型号或对比规格：

- [ALFA USB 无线网卡——完整目录](https://yupitek.com/zh-cn/products/alfa/)——所有型号含规格与定价
- [ALFA 产品对比表](/en/alfa_compare/)——芯片组、频段、驱动的并列对比

### 延伸阅读

- [Flipper One 官方博客文章](https://blog.flipper.net/flipper-one-we-need-your-help/)——Pavel Zhovner，2026 年 5 月
- [Flipper One Developer Portal](https://docs.flipper.net/one)——技术规格与文档
- [什么是 Packet Injection？](/en/blog/packet-injection-guide/)——我们的数据包注入基础指南
- [AWUS036AXML WiFi 6E 评测](/en/blog/awus036axml-wifi-6e-review/)——旗舰网卡深度评测
- [ALFA 产品对比](/en/alfa_compare/)——所有 ALFA 型号的并列规格

---

*关于 Flipper One 与 ALFA 网卡兼容性的售前咨询，请联系 Yupitek 客服：support@yupitek.com 或致电 +886-2-87325338。*

## 参考文献

1. [Flipper One 官方部落格 — Pavel Zhovner 产品公告](https://blog.flipper.net/flipper-one-we-need-your-help/)
2. [Flipper One Developer Portal — 技术规格与文件](https://docs.flipper.net/one)
3. [Flipper Zero 官方网站](https://flipperzero.one/)
4. [aircrack-ng — 无线安全工具组官方网站](https://www.aircrack-ng.org/)
5. [ALFA Network 官方网站](https://www.alfa.com.tw/)
