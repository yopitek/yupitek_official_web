---



title: "ALFA 无线网卡搭配 Kali NetHunter 完整技术指南 2026"
description: "ALFA USB 无线网卡搭配 Kali NetHunter 移动渗透测试完整技术参考。涵盖台湾上市手机兼容性、MT7610U/MT7612U 免驱动 vs RTL8812AU DKMS 驱动分析、OTG 设置指南及实测验证结果。"
date: 2026-06-09
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
featureimage: /images/blog/alfa-nethunter-technical-guide-hero.png
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
faq:
  - question: "ALFA 无线网卡搭配 Kali NetHunter 需要哪些手机条件？"
    answer: "需要支持 OTG 的 Android 手机、已 root 并刷入 Kali NetHunter 核心。已验证兼容的机型包括 Google Pixel 系列、OnePlus 较旧旗舰机型。具体兼容性取决于内核版本与网卡芯片驱动位置。"
  - question: "MT7610U/MT7612U 和 RTL8812AU 驱动有什么差别？"
    answer: "MT7610U/MT7612U 驱动位于核心树内，插上即用不需编译；RTL8812AU 需通过 DKMS 外部驱动编译安装，内核更新后可能需要重新编译。对于安全现场使用，核心树内驱动稳定性更高。"
  - question: "ALFA 网卡在 NetHunter 上支持 Monitor Mode 吗？"
    answer: "是的，MT7610U/MT7612U 支持 Monitor Mode 与数据包注入。RTL8812AU 在核心 < 6.12 时也支持，但核心 6.12 以上 Monitor Mode 受限。建议安全研究优先选用 MT7610U/MT7612U 网卡。"
---




如果你已经按照基础的 OTG 说明完成了 ALFA 网卡与 NetHunter 的初始设置，想要快速入门版本，我们的 [OTG 设置指南](/zh-cn/blog/alfa-adapter-nethunter-android-otg/) 涵盖了基础知识。本文则更加深入——这是一份面向安全从业人员的完整技术参考，适合需要在采购硬件前评估手机与网卡兼容性、了解哪种驱动方式能够在内核更新后持续工作，以及在决定具体组合之前查看实测验证结果的读者。

{{< tldr >}}
MT7610U/MT7612U 核心原生驱动即插即用，RTL8812AU 需 DKMS 编译。NetHunter 手机需 root + OTG 支持，优先选 MT7612U 网卡避免驱动问题。
{{< /tldr >}}


我们聚焦于一个大多数 NetHunter 指南都跳过的问题：**哪款网卡是真正的即插即用，哪款会在最不合适的时刻把你拖进驱动编译的无底洞？** 答案取决于芯片组、手机的内核版本，以及驱动是内置于内核树中还是存在于外部 DKMS 仓库。如果选错了，你的网卡只能躺在包里，而你只能在现场盯着 `modprobe` 报错。选对了，插入即用，立刻开始扫描。

---

## 1. 客户需求

### 1.1 使用场景

移动渗透测试人员需要一套完全替代笔记本的方案。手机运行 Kali NetHunter，ALFA 网卡通过 USB OTG 连接，操作人员在无需携带笔记本的情况下执行 Wi-Fi 安全评估。核心工作流——现场勘查、Monitor Mode 捕获、Packet Injection、WPA 握手包收集——必须在电池供电下可靠运行。

### 1.2 核心需求

| 需求 | 详细说明 |
|---|---|
| 平台 | Android 手机 + Kali NetHunter（完整版，需自定义内核） |
| 连接方式 | USB OTG 线或带供电的 OTG Hub |
| 网卡 | ALFA USB 无线网卡，支持 Monitor Mode 和 Packet Injection |
| 驱动方式 | 优先选择内置内核（免驱动）芯片组，消除编译依赖 |
| 台湾市场 | 手机需为台湾正式上市型号，2024–2026 年 |
| 供电 | 电池供电；强烈建议使用带供电的 OTG Hub 以维持持续运行 |

---

## 2. 目标硬件与软件分析

### 2.1 台湾可购买的 NetHunter 兼容手机

NetHunter 支持超过 117 个设备模块，但大多数是旧型号。经过筛选，以下设备同时满足：(a) 台湾正式上市，(b) 2024 年及以后推出，(c) 具有可用的 NetHunter 自定义内核，三款机型脱颖而出：

| 型号 | 代号 | CPU | 内核版本 | 预构建镜像数 | 台湾供货情况 |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ 通过进口渠道可获取，2023 年发布 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ 台湾正式发布，社区活跃 |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ 台湾有售——**必须是 Snapdragon 版本** |

{{< alert "triangle-exclamation" >}}
**Samsung Exynos 警告：**大部分通过台湾电信运营商销售的 Samsung 设备使用 Exynos 芯片组。NetHunter 内核仅支持 Snapdragon 版本（`r8q`）。购买 Samsung 设备用于 NetHunter 前，务必确认 CPU 型号——如果商品信息写的是"Exynos"，则无法使用。请购买 Snapdragon 水货版本，或选择 OnePlus 11。
{{< /alert >}}

**NetHunter Rootless** 可以在任何 Android 设备上运行，无需 root，但无法支持外部 USB 无线网卡的 Monitor Mode。如果你需要数据包捕获和注入功能，必须使用完整版 NetHunter 及自定义内核。

### 2.2 平台技术规格

以 OnePlus 11 5G 为参考平台：

| 参数 | 规格 |
|---|---|
| CPU 架构 | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| USB 控制器 | USB 3.1 Gen 1，支持 OTG |
| USB 供电 | 5V / 900mA（建议使用带供电的 OTG Hub 以维持网卡持续运行） |

### 2.3 软件环境

| 组件 | 需求 | 推荐版本 |
|---|---|---|
| 宿主系统 | Android + Kali chroot | Android 11+ |
| NetHunter | 完整版（需自定义内核）| 2024.4（最新稳定版） |
| Linux Kernel | 设备特定自定义内核 | 建议 5.x 及以上 |
| 预载驱动 | 详见第 4 节矩阵 | — |
| DKMS | 仅 RTL8812AU 芯片组网卡需要 | 内核头文件必须匹配 |
| 无线工具 | aircrack-ng、Kismet、MANA Toolkit | 由 NetHunter chroot 提供 |
| Root | 完整功能需要 | Magisk 26.0+ |

---

## 3. ALFA 网卡规格与驱动来源

### 3.1 AWUS036ACHM — NetHunter 首选

| 参数 | 规格 |
|---|---|
| 芯片组 | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| 频段 | 2.4 GHz + 5 GHz (AC433) |
| 最大传输速率 | 150 Mbps (2.4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| Monitor Mode | ✅ 完整支持 |
| Packet Injection | ✅ 完整支持 |
| 天线 | 1× 可拆卸高增益天线 (RP-SMA) |
| 驱动 | **内置内核** — 无需安装 |
| 内核模块 | `mt76x0u` |
| 内核要求 | Linux 4.19+ |
| 产品页面 | [/zh-cn/products/alfa/awus036achm/](/zh-cn/products/alfa/awus036achm/) |

MT7610U 芯片组被 Kali 和 NetHunter 社区广泛推荐，因为其 `mt76x0u` 驱动自 4.19 版本起已进入 Linux 主线内核。插入即识别，立刻开始工作。无需编译工具链、无需内核头文件、无需 DKMS——只需 `lsusb` 确认，然后 `airmon-ng start`。

### 3.2 AWUS036ACM — 高性能备选

| 参数 | 规格 |
|---|---|
| 芯片组 | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| 频段 | 2.4 GHz + 5 GHz (AC1200) |
| 最大传输速率 | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ 完整支持 |
| Packet Injection | ✅ 经 Kali 2024.3 / 2025.1 确认稳定 |
| 天线 | 2× 双天线 (RP-SMA)，MIMO 2T2R |
| 驱动 | **内置内核** — 无需安装 |
| 内核模块 | `mt76x2u` |
| 内核要求 | Linux 4.19+ |
| 产品页面 | [/zh-cn/products/alfa/awus036acm/](/zh-cn/products/alfa/awus036acm/) |

ACM 增加了 AC1200 双频及 MIMO 2T2R，搭配 USB 3.0 吞吐量。`mt76x2u` 驱动同样自内核 4.19 起进入主线。需要注意：部分较旧的 NetHunter 自定义内核（尤其是 OnePlus 7T 的 4.14 版本）在编译时未包含 `mt76x2u` 模块。对于任何 4.19 及以上的内核，这不是问题，但如果你的设备运行较旧的内核版本，请用 `lsmod | grep mt76x2u` 检查。

### 3.3 AWUS036ACH — 最广泛的社区支持

| 参数 | 规格 |
|---|---|
| 芯片组 | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| 频段 | 2.4 GHz + 5 GHz (AC1200) |
| 最大传输速率 | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Monitor Mode | ✅ 完整支持 |
| Packet Injection | ✅ 完整支持 |
| 天线 | 2× 5dBi 外接天线 (RP-SMA) |
| 驱动 | 外部 DKMS（大多数 NetHunter 内核预编译） |
| 内核模块 | `88XXau` |
| 驱动仓库 | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| 产品页面 | [/zh-cn/products/alfa/awus036ach/](/zh-cn/products/alfa/awus036ach/) |

ACH 多年来一直是 Kali 和 NetHunter 配置的事实标准。大多数 NetHunter 自定义内核预编译了 `88XXau` 模块，因此通常无需从源码编译。但如果你的内核版本未包含该模块，则需要完整的编译环境及匹配的内核头文件——这正是 MT7610U 和 MT7612U 芯片组所避免的依赖链。双 5dBi 天线使其在所有型号中信号覆盖范围最远，这对于长距离捕获场景至关重要。

### 3.4 AWUS036ACS — 紧凑便携

| 参数 | 规格 |
|---|---|
| 芯片组 | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| 频段 | 2.4 GHz + 5 GHz (AC433) |
| USB | USB 2.0 |
| Monitor Mode | ✅ 支持（与 RTL8812AU 同驱动系列） |
| Packet Injection | ✅ 支持 |
| 天线 | 内置天线，55 mm 超薄机身 |
| 功耗 | ~300mW — 全系列功耗最低 |
| 驱动 | 外部驱动（与 RTL8812AU 共享 aircrack-ng 仓库） |
| 产品页面 | [/zh-cn/products/alfa/awus036acs/](/zh-cn/products/alfa/awus036acs/) |

ACS 是最便携的选择。300mW 的功耗对手机电池最为友好，超薄的外形可以轻松放入口袋。不足之处在于单流 AC433 性能以及与 RTL8812AU 系列共享的外部 DKMS 驱动依赖。

### 3.5 不推荐用于 NetHunter 的网卡

| 网卡 | 芯片组 | 原因 |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | 需内核 6.14+；Monitor Mode 在 Android 内核上稳定性未经验证 |
| AWUS036AXML / AWUS036AXM | MT7921AUN | WiFi 6E / 6 GHz 在当前 NetHunter 内核版本中支持不稳定；不适合作为主要渗透测试网卡 |

### 3.6 驱动源码仓库

| 芯片组 | 驱动 | 来源 |
|---|---|---|
| MT7610U | `mt76x0u`（内置内核） | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u`（内置内核） | 与上方同内核树 |
| RTL8812AU | `88XXau`（外部） | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau`（外部，共享） | 与上方同 aircrack-ng 仓库 |

---

## 4. 驱动兼容性分析

### 4.1 内置内核 vs 外部 DKMS

选择 NetHunter 网卡时，最关键的决定因素是驱动位于内核树内还是内核树外。以下是原因：

| | 内置内核 (MT7610U, MT7612U) | 外部 DKMS (RTL8812AU, RTL8811AU) |
|---|---|---|
| 即插即用 | ✅ 是 — 插入即识别 | ⚠️ 取决于内核是否预编译 `88XXau` |
| 内核更新后仍可用 | ✅ 是 — 驱动是内核构建的一部分 | ❌ 内核更新后可能失效；需重新编译 |
| 需要 linux-headers | ❌ 不需要 | ✅ 如需手动编译则需要 |
| 需要 DKMS | ❌ 不需要 | ✅ 如内核未预编译则需要 |
| 社区文档 | 中等 | 广泛（ACH 教程最多） |
| 现场故障风险 | 低 | 中等（编译依赖） |

**结论：**如果你希望将现场驱动问题的风险降到最低，选择 MT7610U 或 MT7612U 网卡。驱动已在内核中——无需编译，不会因更新而失效，现场也无需排查。

### 4.2 NetHunter 内核模块支持矩阵

| 设备 | NetHunter 内核 | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Android 13 kernel | ✅ 支持 | ✅ 支持 | ✅ 支持 |
| Samsung S20 FE (Snapdragon) | Android 12 kernel (4.19) | ✅ 支持 | ✅ 支持 | ✅ 支持（请核实 XDA 报告） |
| Nothing Phone (1) | Android 12/13 kernel | ✅ 支持 | 检查内核配置 | ✅ 支持 |
| OnePlus 7/7T | 4.14（较旧） | ✅ 支持 | ⚠️ 可能未编入内核 | ✅ 支持 |

来源：NetHunter GitLab、XDA Forums 社区报告（2024–2026）。

### 4.3 已知问题

**问题 1：MT7612U 在旧内核上不显示接口**

症状：`lsusb` 显示 `0e8d:7612`，但 `ip link` 中无 `wlan1`。  
根本原因：自定义内核编译时未包含 `mt76x2u` 模块。此问题影响部分基于 4.14 的 NetHunter 内核（OnePlus 7T 时代）。  
解决方法：使用包含该模块的内核版本，或改用支持更广泛的 AWUS036ACHM (MT7610U)。

**问题 2：USB 供电不足导致网卡断连**

症状：网卡在扫描过程中突然消失，`dmesg` 显示 USB reset 错误。  
根本原因：手机 USB 端口无法持续提供网卡所需的电流，USB 3.0 网卡尤甚（ACH 功耗约 500mW）。  
解决方法：使用带独立供电的 OTG Hub，从电源适配器为网卡提供 5V 供电，同时向手机传输数据。

**问题 3：chroot 启动前插入网卡**

症状：Android 弹出 USB 权限对话框，但 Kali 工具无法访问网卡。  
根本原因：NetHunter chroot 环境必须先运行，USB 设备才能暴露给 chroot。  
解决方法：先启动 chroot（Kali Services → Start），再连接网卡并授予 USB 权限。

---

## 5. 设置指南

### 5.1 前置条件

连接任何硬件之前，请确认：

```bash
# 确认设备已 root
su -c "id"

# 验证 NetHunter chroot 版本
cat /kali/etc/os-release
# 应显示 Kali Linux with NetHunter

# 确认 USB OTG 已启用
# 设置 → 开发人员选项 → OTG（具体位置因 Android 版本而异）
```

### 5.2 硬件连接顺序

顺序很重要：

1. 启动 **NetHunter App** → 打开 **Kali Services** → 点击 **Start** 启动 chroot
2. 将 **带供电的 OTG Hub** 连接到手机的 USB 端口
3. 将 **ALFA 网卡** 插入 OTG Hub
4. 弹出 Android USB 权限对话框时，点击 **确定** 并勾选 **始终允许**

{{< alert "circle-info" >}}
持续运行强烈建议使用带供电的 OTG Hub。AWUS036ACH 功耗约 500mW——直接从手机电池供电会显著加速电量消耗，并可能导致 USB 不稳定。使用从电源适配器取电并向手机传输数据的 Hub 可以同时解决这两个问题。
{{< /alert >}}

### 5.3 验证网卡识别

```bash
# 列出 USB 设备——确认网卡已显示
lsusb

# 各型号预期输出：
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

如果网卡未出现：尝试更换 OTG 线、确认开发人员选项中已启用 OTG，或将网卡连接到电脑上测试其功能是否正常。

### 5.4 加载驱动

**MT7610U (AWUS036ACHM) — 大多数内核自动加载：**

```bash
# 验证自动加载
lsmod | grep mt76

# 如需手动加载（不常见）
sudo modprobe mt76x0u
```

**MT7612U (AWUS036ACM) — 内核 4.19+ 自动加载：**

```bash
# 验证
lsmod | grep mt76

# 如需手动加载
sudo modprobe mt76x2u
```

**RTL8812AU (AWUS036ACH) — 大多数 NetHunter 内核预编译：**

```bash
# 加载预编译模块
sudo modprobe 88XXau

# 验证加载结果
lsmod | grep 88XX
```

### 5.5 确认网络接口

```bash
# 列出无线接口
ip link show | grep wlan

# 或使用 iw
iw dev

# 外部网卡通常显示为 wlan1
# （wlan0 通常是手机内置 WiFi）
```

### 5.6 启用 Monitor Mode

```bash
# 终止可能干扰的进程
sudo airmon-ng check kill

# 在网卡上启动 Monitor Mode
sudo airmon-ng start wlan1

# 验证 Monitor Mode 已启用
iwconfig wlan1mon
# 预期输出：Mode:Monitor

# 扫描附近网络（仅限授权测试）
sudo airodump-ng wlan1mon

# 扫描所有频段（2.4 GHz + 5 GHz）
sudo airodump-ng --band abg wlan1mon
```

### 5.7 恢复 Managed Mode

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. 应用架构图

<img src="/images/blog/nethunter-topology.png" alt="NetHunter + ALFA Application Topology Diagram" loading="eager" style="max-width:100%;height:auto;display:block">

---

## 7. 验证结果

### 7.1 测试矩阵

以下组合已通过社区测试和厂商文档验证：

| 手机 | ALFA 网卡 | 芯片组 | Monitor Mode | Packet Injection | 状态 |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | 已验证 |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | 已验证 |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | 已验证 |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | 社区报告——请核实内核配置 |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | 社区报告 |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | 社区报告 |

来源：XDA Forums、Reddit r/NetHunter、Kali NetHunter GitLab Issues（2024–2026）。

### 7.2 预期 `lsusb` 输出

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 Monitor Mode 验证

```bash
# 预期 iwconfig 输出（成功时）
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. 推荐

### 8.1 首选：OnePlus 11 5G + AWUS036ACHM

在所有测试过的组合中，此配置的摩擦系数最低。OnePlus 11 是目前台湾市场仍可获取的、具备官方 NetHunter 内核支持的最新旗舰机。AWUS036ACHM 的 MT7610U 芯片组使用 `mt76x0u` 驱动——自 4.19 起已进入主线内核，无需任何编译，国际安全社区（Lab401、morrownr USB-WiFi 数据库）一致将其评为 Kali 和 NetHunter 最安全的选择。该网卡体积小巧、单天线、USB 2.0 接口，这些在移动场景中都是优点——功耗更低、发热更少、故障点更少。

### 8.2 性能之选：OnePlus 11 5G + AWUS036ACM

如果你需要 AC1200 双频性能及 MIMO 2T2R 来实现远距离 5 GHz 捕获，ACM 可以在不离开内置内核驱动生态的前提下满足需求。MT7612U 的 `mt76x2u` 驱动同样自 4.19 起在主线内核中。代价是：USB 3.0 功耗更高，双天线机身更大。确认内核包含 `mt76x2u`——在 OnePlus 11 上已确认支持。

### 8.3 社区首选：任何 NetHunter 设备 + AWUS036ACH

ACH 拥有 NetHunter 生态中最多的教程、最庞大的社区故障排查库和最丰富的第三方文档资源。其双 5dBi 天线提供了 ALFA 系列中最强的信号覆盖范围。大多数 NetHunter 内核预编译了 `88XXau` 模块，因此基本无需编译。如果你更看重社区支持和长距离捕获能力而非即插即用的简便性，这是最佳选择。

### 8.4 场景化选择

| 场景 | 推荐组合 | 理由 |
|---|---|---|
| 初次 NetHunter 配置，风险最小化 | OnePlus 11 + AWUS036ACHM | 内置内核驱动，无需编译，最小机身 |
| 远距离双频捕获 | OnePlus 11 + AWUS036ACM | AC1200 + MIMO，仍为内置内核 |
| 长距离勘查，最多教程 | 任何支持的设备 + AWUS036ACH | 最强天线，最广泛社区支持 |
| 超便携，最低功耗 | 任何支持的设备 + AWUS036ACS | 300mW 功耗，可放入任何口袋 |

### 8.5 支持资源

| 资源 | 链接 |
|---|---|
| Yupitek — ALFA 台湾授权经销商 | [yupitek.com](https://www.yupitek.com) |
| ALFA Network 官方产品页面 | [alfa.com.tw](https://www.alfa.com.tw) |
| MT7610U 驱动（内核树） | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| RTL8812AU 驱动（aircrack-ng） | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| NetHunter 支持设备列表 | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| NetHunter 官方文档 | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| XDA NetHunter 论坛 | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Yupitek ALFA 产品目录 | [/zh-cn/products/alfa/](/zh-cn/products/alfa/) |

---

## 附录：快速故障排除

**网卡未出现在 `lsusb` 中：**
1. 确认开发人员选项中已启用 OTG
2. 更换 OTG 线——线材品质是最常见的故障点
3. 使用带供电的 OTG Hub
4. 确认 NetHunter chroot 已启动

**设备在 `lsusb` 中可见但无 `wlan1` 接口：**

```bash
# 检查内核日志中的驱动错误
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# 确认内核模块是否存在
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# 尝试手动加载
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**Monitor Mode 已启动但扫描不到任何网络：**

```bash
# 先终止干扰进程
sudo airmon-ng check kill

# 重新扫描所有频段
sudo airodump-ng --band abg wlan1mon

# 确认频道设置
sudo iw dev wlan1mon info
```

**使用过程中网卡断连（USB reset）：**

```bash
# 临时方法——降低发射功率
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# 根本解决方法——使用带供电的 OTG Hub
```

---


{{< faq >}}

## 相关指南

- [ALFA 网卡与 NetHunter 基础 OTG 设置](/zh-cn/blog/alfa-adapter-nethunter-android-otg/)
- [ALFA WiFi 网卡选购指南 2026](/zh-cn/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [在 Kali Linux 和 Ubuntu 上安装 ALFA 驱动](/zh-cn/blog/install-alfa-driver-kali-ubuntu/)
- [ALFA 网卡搭配 Raspberry Pi 和 Kali 使用](/zh-cn/blog/alfa-adapter-raspberry-pi-kali/)

---

*本文档由 **Yupitek Ltd**（ALFA Network 台湾授权经销商）编写。*  
*数据截止日期：2026-06-09。Linux 内核及 NetHunter 版本持续更新，请以官方最新资料为准。*

## 参考文献

1. [Kali NetHunter 官方文档](https://www.kali.org/docs/nethunter/)
2. [Linux Kernel mt76 驱动原始码](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek/mt76)
3. [aircrack-ng RTL8812AU 驱动](https://github.com/aircrack-ng/rtl8812au)
4. [ALFA Network 官方网站](https://alfa.com.tw/)
5. [Android USB OTG 官方文档](https://developer.android.com/guide/topics/connectivity/usb)
