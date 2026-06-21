---
title: "ALFA 无线网卡在 Apple Mac 上的兼容性（2026）：M1/M2/M3/M4 与 Intel 完整兼容报告"
description: "ALFA Network USB 无线网卡在 Apple Mac（MacBook、MacBook Pro、MacBook Air、Mac Mini、Mac Studio）上的完整兼容性指南，涵盖 Intel 和 Apple Silicon M1/M2/M3/M4 处理器。了解哪些 ALFA 网卡可用、为何 Apple Silicon 原生支持为零，以及如何通过 Linux 虚拟机启用监听模式。"
keywords: "ALFA 无线网卡 Mac, ALFA macOS 兼容性, ALFA 网卡 Apple Silicon, USB WiFi 适配器 M1 M2 M3 M4, ALFA Network MacBook, Mac 监听模式, AWUS036ACH Mac, AWUS036ACM Mac, ALFA Network Mac Mini, Apple Silicon 渗透测试"
author: "Yupitek 技术支持团队"
date: "2026-06-20"
category: "技术指南"
tags: ["Wireless Security", "ALFA Network", "Apple Mac", "Penetration Testing", "macOS Compatibility"]
---
如果你正在使用 Apple Mac（无论是搭载 M3 Max 的 MacBook Pro、搭载 M2 Ultra 的 Mac Studio，还是基于 Intel 的 Mac Mini），并且想要使用 ALFA Network 无线适配器进行 Wi-Fi 审计、监听模式或数据包注入，你需要一个明确的答案：**哪款 ALFA 网卡在哪款 Mac 上可用？**

简短回答如下：

> **Apple Silicon Mac（M1/M2/M3/M4）：没有任何 ALFA 无线网卡能在 macOS 上原生运行。** 这是架构层面的限制。Realtek 的 macOS 内核扩展是仅 x86_64 的二进制文件，无法在 ARM64 内核上加载。没有修复方案，也没有任何厂商计划改变这一点。
>
> **Intel Mac：有限支持，仅限客户端连接。** macOS 10.11–10.15 有部分官方驱动程序，但 **macOS 不支持监听模式和数据包注入**，驱动程序根本没有实现这些功能。
>
> **可行的解决方案：** 在 Apple Silicon Mac 上通过 USB 透传运行 Kali Linux ARM 虚拟机（UTM/Parallels/VMware）。监听模式和数据包注入在 Linux 虚拟机中运行完美。

本指南提供完整的兼容性矩阵，解释 Apple Silicon 无法原生支持 ALFA 网卡的六大技术原因，并带你完成实际可行的虚拟机设置。

---

## 1. 兼容性矩阵：哪款 ALFA 网卡在哪款 Mac 上可用？

下表是权威参考。它评估了 [Yupitek 的 ALFA 产品线](https://yupitek.com/en/products/alfa/) 中目前在售的全部 9 款 ALFA 无线适配器（不含已停产型号）在四种部署场景下的表现。

### 1.1 完整兼容性矩阵

| ALFA 型号 | 芯片组 | Apple Silicon（macOS 原生） | Intel Mac（macOS 原生） | 虚拟机 + USB 透传（Kali ARM） | Raspberry Pi + Kali |
|:---|:---|:---:|:---:|:---:|:---:|
| **AWUS036ACH** | Realtek RTL8812AU | ❌ | ⚠️ 仅客户端（≤10.15） | ✅ 最佳监听/注入 | ✅ |
| **AWUS036ACM** | MediaTek MT7612U | ❌ | ⚠️ 仅客户端（≤10.12） | ✅ 即插即用 | ✅ 即插即用 |
| **AWUS036AXML** | MediaTek MT7921AUN | ❌ | ❌ | ✅ Wi-Fi 6E | ✅ |
| **AWUS036AXM** | MediaTek MT7921AUN | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACHM** | MediaTek MT7610U | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACS** | Realtek RTL8811AU | ❌ | ⚠️ 仅客户端（≤10.14） | ✅ | ✅ |
| **AWUS036AX** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ 有限 | ⚠️ 有限 |
| **AWUS036AXER** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ 有限 | ⚠️ 有限 |
| **AWUS036EACS** | Realtek RTL8821CU | ❌ | ⚠️ 仅客户端 | ❌ 无监听模式 | ⚠️ 不推荐 |

**图例：** ✅ = 已验证可用 | ⚠️ = 有限制 / 需要特定条件 | ❌ = 不支持

### 1.2 按 Mac 处理器快速结论

| Mac 处理器 | 能在 macOS 上使用 ALFA 网卡吗？ | 能启用监听模式吗？ | 推荐方案 |
|:---|:---|:---|:---|
| **Apple Silicon M1/M2/M3/M4** | ❌ 不能，架构限制 | ❌ macOS 上不行 | ✅ Linux 虚拟机 + USB 透传 |
| **Intel（macOS 10.11–10.15）** | ⚠️ 有限，仅客户端，无监听模式 | ❌ 不支持 | ✅ Linux 虚拟机 + USB 透传 |
| **Intel（macOS 11+）** | ⚠️ 仅第三方 kext（chris1111） | ❌ 不支持 | ✅ Linux 虚拟机 + USB 透传 |

> [!IMPORTANT]
> **结论：** 无论你拥有哪款 Mac，**监听模式和数据包注入都需要 Linux。** 虚拟机 + USB 透传方案是通用解决方案，适用于从 2012 年 Intel MacBook Pro 到 2025 年 M4 Mac Studio 的所有 Mac。

---

## 2. 为什么 Apple Silicon 无法支持：六层架构壁垒

如果你想知道未来的 macOS 更新是否会解决这个问题，答案是不会。这种不兼容不是等待修复的 bug，而是 **六项 Apple 设计决策** 累积的结果，它们共同使得第三方 USB Wi-Fi 适配器在 Apple Silicon 上从架构层面变得不可能。

### 第一层：IO80211Controller 是私有 API

Apple 从未发布原生 Wi-Fi 驱动的内核编程接口（KPI）。类层次结构如下：

```
IOService
  └─ IONetworkController
       └─ IOEthernetController        公共 KPI
            └─ IO80211Controller      私有（仅限 Apple 内部使用）
```

第三方厂商历史上直接继承 `IOEthernetController`，这就是为什么 macOS 上的 USB Wi-Fi 适配器显示为"以太网"接口，而不是与菜单栏 Wi-Fi 图标、AirDrop、Sidecar 或"查找"集成。

### 第二层：NetworkingDriverKit 仅支持以太网

Apple 对内核扩展的现代替代方案是 **DriverKit**，即不会危及内核稳定性的用户空间驱动。网络驱动家族 `NetworkingDriverKit` 在 [Apple 官方文档](https://developer.apple.com/documentation/networkingdriverkit) 中明确声明：

> "使用 NetworkingDriverKit 开发 USB 以太网适配器的驱动程序。请注意，**以太网是 NetworkingDriverKit 目前唯一支持的网络接口。**"

不存在 `IOUserNetworkWiFi` 类。没有 Wi-Fi 的 DriverKit 框架。即使 Realtek 或 MediaTek 投入工程资源编写 DriverKit 驱动，**也没有 Apple 框架可以接入它。**

### 第三层：USB + 内核扩展组合自 Big Sur 起不再支持

Apple 的 [已弃用的内核扩展](https://developer.apple.com/support/kernel-extensions/) 页面声明：

> "同时使用 IONetworkingFamily KPI 和任何 USB KPI（IOUSBHostFamily 或 IOUSBFamily）在 **macOS Big Sur 中不受支持。**"

这正是每个 USB Wi-Fi 内核扩展所需的 KPI 组合。唯一的变通方案是完全关闭 SIP 或使用 MDM 配置文件，两者都不适合消费级产品。

### 第四层：Realtek 的内核扩展仅支持 x86_64

Realtek 的 macOS 驱动程序以 `RtWlanU.kext` 形式发布，仅针对 **x86_64** 编译。Apple Silicon Mac 运行的是 **ARM64** 内核。内核扩展在内核空间执行，**Rosetta 2 无法翻译内核扩展。**

[chris1111 讨论 #128](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter/discussions/128) 上的一位用户在搭载 Ventura 13.1 的 M1 MacBook Air 上使用 ALFA AWUS1900 时记录了确切的失败信息：

```
Domain=KMErrorDomain Code=71
Incompatible architecture: Binary is for x86_64, but needed arm64
Kext com.realtek.driver.RtWlanU v1830.32.b27
```

### 第五层：Realtek 已放弃 macOS 驱动开发

[chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter)（Realtek macOS Wi-Fi 驱动的事实上的社区分发版）的维护者在 README 中明确声明：

> **"看起来它在 Mac M1、M2、M3、M4 Apple 芯片上无法工作，仅在 Mac Intel 上工作。"**

并在回复一位用户询问是否可以添加 M1 支持时写道：

> "旧版 kext 扩展需要为 M1 Mac 重写（即使通过 Rosetta 2 也无法工作），这意味着需要大型公司更新其驱动程序以支持 M1。"

Realtek 没有发布 arm64 kext、DriverKit 驱动或任何面向 Apple Silicon 支持的公开计划。经济激励几乎为零：每台 Apple Silicon Mac 都已经内置了 Wi-Fi。

### 第六层：Apple Silicon 的内核扩展加载从设计上就充满阻碍

即使存在 arm64 kext，在 Apple Silicon 上加载它也需要执行以下步骤：

1. 关闭 Mac
2. **按住** 电源按钮直到出现启动选项
3. 进入唯一真正的恢复模式（1TR）
4. 降级到 **降低安全性** 策略
5. 启用"允许管理已识别开发者的内核扩展"
6. 重新启动，安装 kext，在系统设置中批准
7. **再次重新启动** 以重建辅助内核集合（AuxKC）

根据 Apple 的 [安全扩展内核](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) 指南，此流程是故意设置障碍的："1TR 和密码要求的组合使得仅通过软件攻击者难以从 macOS 内部注入 kext。"

> [!IMPORTANT]
> **结论：** 没有任何 ALFA 网卡，也没有任何第三方 USB Wi-Fi 适配器能在 Apple Silicon macOS 上原生运行。除非 Apple 发布 Wi-Fi DriverKit 框架（尚未发布）并且有厂商为其编写驱动（目前没有任何厂商这样做），否则这种情况不会改变。

---

## 3. Intel Mac：哪些仍然可用（哪些不可用）

如果你的团队仍在使用 Intel Mac，情况会好一些，但仅限于基本 Wi-Fi 连接，不适用于安全审计。

### 4.1 macOS 版本支持时间线

| ALFA 型号 | 芯片组 | 官方 macOS 限制 | 社区驱动（chris1111） |
|------------|---------|---------------------|------------------------------|
| AWUS036ACH | RTL8812AU | 10.15 Catalina | 11 Big Sur 至 26 Tahoe（仅限 Intel） |
| AWUS036ACS | RTL8811AU | 10.14 Mojave | 11 Big Sur 至 26 Tahoe（仅限 Intel） |
| AWUS036ACM | MT7612U | **10.12 Sierra** | ❌ 不支持（MediaTek） |
| AWUS036ACHM | MT7610U | ❌ 无 | ❌ 不支持（MediaTek） |
| AWUS036AX/AXER | RTL8832BU | ❌ 无 | ❌ 无 |
| AWUS036AXML/AXM | MT7921AUN | ❌ 无 | ❌ 无 |

### 4.2 监听模式的悖论

安全专业人士面临的关键问题是：**即使在 Intel Mac 上成功安装了驱动程序，监听模式和数据包注入也无法工作。**

ALFA 的 macOS 驱动程序仅实现客户端连接功能，不实现监听模式 API。这一点在 [Super 讨论](https://super.com/questions/1597114/alfa-wifi-network-card-monitor-mode-on-mac-os) 中得到了确认，一位用户成功安装了 AWUS036EAC 驱动，但无法进入监听模式：

> *"是什么让你认为 ALFA 在他们的 macOS 驱动中加入了监听模式支持？不同操作系统的监听模式 API 是不同的。我假设他们只是懒得为 macOS 实现它。"*

这就形成了一个悖论：**你购买 ALFA 网卡正是为了监听模式和数据包注入，但 macOS 驱动程序不支持其中任何功能。** macOS 内置 Wi-Fi 卡实际上支持监听模式（通过 `airport` 实用程序），但 ALFA 的驱动程序没有为其硬件实现这一功能。

> [!WARNING]
> 如果你的目标是无线安全审计（监听模式、数据包注入、握手捕获、去认证攻击），**macOS 无法做到，无论 Intel 还是 Apple Silicon Mac，无论使用哪款 ALFA 网卡。** 你需要 Linux。

### 4.3 chris1111 驱动：Intel Mac 的最后选择

对于运行 macOS 11 Big Sur 或更高版本的 Intel Mac，唯一的选择是 [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) 项目，这是一个由社区维护的 Realtek kext 分发版。

**要求：**
- 仅限 Intel Mac（不支持 Apple Silicon）
- 必须禁用系统完整性保护（SIP）
- 该 kext 未经 Realtek/ALFA/Apple 签名

**支持的网卡：** 仅限 AWUS036ACH（RTL8812AU）和 AWUS036ACS（RTL8811AU）。

Rokland（ALFA 的美国经销商）[强烈警告](https://store.rokland.com/blogs/news/apple-mac-os-11-big-sur-compatibility-update-for-alfa-awus036ach-other-products)："我们强烈建议不要在你的 Mac 是主要计算机且用于关键任务时使用此驱动。"

---

## 4. 可行的解决方案：虚拟机 + USB 透传

由于 macOS 无法原生运行 ALFA 网卡（即使可以，监听模式也无法工作），Mac 安全团队的实用解决方案是在**虚拟机中运行 Linux**，并通过 USB 透传 ALFA 网卡。

此方案适用于 **所有 Apple Silicon Mac**（M1/M2/M3/M4）和所有 Intel Mac。监听模式和数据包注入的功能与原生 Linux 机器完全相同。

### 5.1 你需要什么

| 组件 | 推荐 | 费用 |
|-----------|---------------|------|
| 虚拟机软件 | [UTM](https://mac.getutm.app/)（免费、开源） | 免费 |
| 替代方案 | Parallels Desktop 或 VMware Fusion（ARM） | 99 美元/年 |
| Linux ISO | [Kali Linux ARM64](https://www.kali.org/get-kali/) | 免费 |
| ALFA 网卡 | AWUS036ACH（最佳）或 AWUS036ACM（即插即用） | 40–70 美元 |
| USB 适配器 | USB-C 转 USB-A 适配器（如果 ALFA 网卡是 USB-A 接口） | 10 美元 |

### 5.2 逐步设置

#### 第一步：创建 Kali Linux ARM 虚拟机

下载 Kali Linux ARM64 安装程序，在 UTM 中创建新虚拟机：
- **架构：** ARM64（aarch64）
- **内存：** 最低 2 GB（推荐 4 GB）
- **CPU：** 2 核以上
- **USB 控制器：** USB 3.0（xHCI），**这一点至关重要**

> [!IMPORTANT]
> 你必须将虚拟机的 USB 控制器配置为 **USB 3.0（xHCI）**，而不是 USB 2.0。USB 2.0 控制器会导致高功耗 ALFA 网卡间歇性断开连接，尤其是在数据包注入期间。

#### 第二步：在虚拟机中安装 ALFA 驱动

**对于 AWUS036ACH（RTL8812AU）：**

如果你的 Kali 内核版本 **≥6.14**，`rtw88` 主线驱动已包含在内，无需安装。对于较旧的内核：

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) git
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
```

**对于 AWUS036ACM（MT7612U），零安装：**

MediaTek MT7612U 驱动自 Linux 4.19 版本起已包含在内核中。插入即可使用：

```bash
lsusb
# Bus 001 Device 005: ID 0e8d:7612 MediaTek Inc.

iw dev
# wlan0 应自动出现
```

**对于 AWUS036AXML / AWUS036AXM（MT7921AUN）：**

自 Linux 5.18 起包含在内核中，但需要固件文件：

```bash
sudo apt install -y firmware-misc-nonfree
# 验证固件是否存在：
ls /lib/firmware/mediatek/
# WIFI_MT7922_patch_mcu_1_1_hdr.bin
# WIFI_RAM_CODE_MT7922_1.bin
```

#### 第三步：配置 USB 透传

1. 将 ALFA 网卡插入 Mac 的 USB-C/Thunderbolt 端口（如需请使用 USB-C 转 USB-A 适配器）
2. 在 UTM 中：虚拟机菜单栏，USB，选择 ALFA 设备，分配给虚拟机
3. 在 Parallels 中：虚拟机设置，硬件，USB 和蓝牙，勾选"USB 3.0"，将 ALFA 设备分配给虚拟机

#### 第四步：验证监听模式和数据包注入

```bash
# 验证虚拟机内已识别设备
lsusb
# Bus 003 Device 005: ID 0bda:8812 Realtek ... RTL8812AU

# 启用监听模式
sudo airmon-ng start wlan0
# (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)

# 确认监听模式已激活
iw dev wlan0mon info
# Mode: monitor

# 测试数据包注入能力
sudo aireplay-ng --test wlan0mon
# "Injection is working!" 确认成功
```

### 5.3 已知问题与故障排除

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| 重度扫描期间网卡断开 | USB 3.0 模式切换 bug（morrownr/USB-WiFi #676） | 在网卡和 Mac 之间使用 USB 2.0 集线器 |
| `airmon-ng` 看不到网卡 | 虚拟机设置中 USB 控制器不正确 | 将虚拟机 USB 设置为 USB 3.0（xHCI），而非 USB 2.0 |
| 驱动在虚拟机中无法编译 | 缺少内核头文件 | `sudo apt install linux-headers-$(uname -r)` |
| 网卡已识别但无监听模式 | RTL8832BU 芯片组（AWUS036AX/AXER） | 此芯片组监听模式支持有限，改用 AWUS036ACH |

### 5.4 替代方案：Raspberry Pi 作为远程渗透测试节点

对于偏好专用硬件方案的团队，运行 Kali Linux 的 **Raspberry Pi 4 或 5** 是出色的便携式无线审计节点。Mac 仅用作 SSH 终端。

**优势：**
- 完全绕过 macOS 驱动问题
- AWUS036ACM 在 Pi 上即插即用（内核驱动，零安装）
- 成本：Pi 5 + ALFA 网卡低于 200 美元
- 便携且不影响主工作机

```bash
# 从 Mac SSH 到 Pi：
ssh kali@192.168.1.100

# 在 Pi 上运行无线审计：
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
sudo aireplay-ng --test wlan1mon
```

---

## 5. USB 硬件指南：在 Mac 上使用哪个端口

ALFA 网卡是 USB 2.0 或 USB 3.0 设备，通常采用 USB-A 接口，功耗在 500 mA（2.5 W）到 900 mA（4.5 W）之间。并非所有 Mac USB 端口都提供足够的功率，Mac Mini M4（2024）有一个你需要知道的关键特性。

### 6.1 Mac USB 端口功率参考

| Mac 型号 | USB-A 端口 | USB-A 功率 | USB-C/TB 端口 | USB-C 功率 | ALFA 直插？ |
|-----------|-------------|-------------|----------------|-------------|-------------------|
| MacBook 12"（2015–2017） | ❌ 无 | 不适用 | 1× USB-C 3.1 Gen 1 | 900 mA | ❌ 需要适配器 |
| MacBook Air Intel（2010–2017） | ✅ 2× | 900 mA | 1× TB1/TB2 | 不适用 | ✅ 直插 |
| MacBook Air Intel（2018–2020） | ❌ 无 | 不适用 | 2× TB3 | 15 W / 7.5 W | ❌ 需要适配器 |
| MacBook Air M1/M2/M3 | ❌ 无 | 不适用 | 2× TB/USB 4 | 15 W / 7.5 W | ❌ 需要适配器 |
| MacBook Pro Intel（2012–2015） | ✅ 2× | 900 mA | 2× TB2 | 不适用 | ✅ 直插（最佳时代） |
| MacBook Pro Intel（2016–2019） | ❌ 无 | 不适用 | 4× TB3 | 15 W / 7.5 W | ❌ 需要适配器 |
| MacBook Pro M1（2020） | ❌ 无 | 不适用 | 2× TB/USB 4 | 15 W / 7.5 W | ❌ 需要适配器 |
| MacBook Pro M1 Pro/Max（2021+） | ❌ 无 | 不适用 | 3× TB4 | 每端口 15 W | ❌ 需要适配器 |
| MacBook Pro M2/M3/M4 Pro/Max | ❌ 无 | 不适用 | 3× TB4 或 TB5 | 每端口 15 W+ | ❌ 需要适配器 |
| Mac Mini Intel（2014） | ✅ 4× | 900 mA | 2× TB2 | 不适用 | ✅ 直插 |
| Mac Mini Intel（2018） | ✅ 2× | 900 mA | 4× TB3 | 15 W / 7.5 W | ✅ 直插 |
| Mac Mini M1（2020） | ✅ 2× | 900 mA | 2× TB/USB 4 | 15 W / 7.5 W | ✅ 直插 |
| Mac Mini M2/M2 Pro（2023） | ✅ 2× | 900 mA | 2–4× TB4 | 每端口 15 W | ✅ 直插 |
| **Mac Mini M4/M4 Pro（2024）** | **❌ 无** | **不适用** | 前置：2× USB-C / 后置：3× TB4 或 TB5 | **前置：500 mA / 后置：900 mA+** | **❌ 仅后置 TB 端口** |
| Mac Studio（所有代） | ✅ 2×（后置） | 900 mA | 4× TB4 或 TB5（后置） | 每端口 15 W | ✅ 直插 |

### 6.2 关键警告：Mac Mini M4（2024）

Mac Mini M4/M4 Pro 是 **首款没有 USB-A 端口的 Mac Mini。** 更重要的是，两个前置 USB-C 端口仅提供 **约 500 mA** 功率，不足以支持需要 900 mA 的 USB 3.0 ALFA 网卡。

> [!WARNING]
> 在 Mac Mini M4 上，**始终将 ALFA 网卡插入后置 Thunderbolt 4/5 端口**，使用 USB-C 转 USB-A 适配器。前置 USB-C 端口（500 mA）会导致高功耗 ALFA 网卡出现电源不稳定和连接断开。

### 6.3 Thunderbolt 功率分配规则

- **Thunderbolt 3（Intel Mac，2016–2020）：** 前两个端口 15 W（3 A），额外端口 7.5 W（1.5 A），先到先得。优先插入 ALFA 网卡以占用完整的 15 W。
- **Thunderbolt 4（Apple Silicon，2021+）：** 每端口 15 W（3 A），无分配限制。
- **USB-A 端口（所有配备该端口的 Mac）：** 始终 900 mA（USB 3.0 规范），足以支持任何 ALFA 网卡。

---

## 6. 按使用场景的购买建议

### 7.1 针对 Apple Silicon Mac 用户（M1/M2/M3/M4）

| 使用场景 | 推荐网卡 | 原因 | 设置方式 |
|----------|---------|-----|----------|
| **最佳监听模式和数据包注入** | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | RTL8812AU，Kali Linux 黄金标准，驱动最成熟 | 虚拟机 + USB 透传 |
| **最佳即插即用体验** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | MT7612U，Linux 4.19 起即内核驱动，零驱动安装 | 虚拟机 + USB 透传 |
| **Wi-Fi 6E / 6 GHz 测试** | [AWUS036AXML](https://yupitek.com/en/products/alfa/awus036axml/) | MT7921AUN，Linux 5.18 起即内核驱动，三频 + BT 5.2 | 虚拟机 + USB 透传 |
| **预算 / 入门** | [AWUS036ACS](https://yupitek.com/en/products/alfa/awus036acs/) | RTL8811AU，经济实惠，支持监听模式和数据包注入 | 虚拟机 + USB 透传 |
| **便携式专用节点** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | Raspberry Pi 上零安装，低功耗（600 mA） | Raspberry Pi + Kali |

### 7.2 针对 Intel Mac 用户（仅限客户端连接）

| macOS 版本 | 推荐网卡 | 驱动方式 | 限制 |
|---------------|-----------------|---------------|----------|
| 10.15 Catalina 或更早 | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | 官方 ALFA 驱动 | 仅客户端，无监听模式 |
| 11 Big Sur 或更新 | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | [chris1111 驱动](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter)（关闭 SIP） | 仅客户端，无监听模式 |

> [!IMPORTANT]
> 在 **任何** Mac（Intel 或 Apple Silicon）上进行无线安全审计，你仍然需要 Linux，无论是在虚拟机中还是在 Raspberry Pi 上。macOS 驱动程序不支持监听模式或数据包注入，没有例外。

### 7.3 Mac 用户应避免的网卡

| 网卡 | 避免原因 |
|------|-----------|
| AWUS036AX / AWUS036AXER（RTL8832BU） | Linux 中监听模式支持有限且不稳定，无 macOS 驱动 |
| AWUS036EACS（RTL8821CU） | 完全 **不支持** 监听模式，不适合安全审计 |
| AWUS036ACHM（MT7610U） | 无 macOS 驱动（chris1111 不支持 MediaTek），需要 Linux 编译 |

---

## 7. 常见问题：ALFA 无线网卡在 Apple Mac 上

> [!NOTE]
> 本 FAQ 部分采用答案引擎优化（AEO）结构。每个问题在第一句话中给出明确回答，以便 AI 搜索引擎（ChatGPT、Perplexity、Google AI Overviews）可以直接引用这些答案。

### ALFA AWUS036ACH 能在 M1/M2/M3/M4 Mac 上运行吗？

**不能。** AWUS036ACH（RTL8812AU）无法在任何 Apple Silicon Mac 上原生运行。Realtek 的 macOS 驱动仅针对 x86_64 编译，无法在 ARM64 内核上加载。不过，它在 Linux 虚拟机（UTM/Parallels）中通过 USB 透传运行完美，包括完整的监听模式和数据包注入支持。

### 我能在 macOS 上使用 ALFA 无线网卡进行监听模式吗？

**不能。** ALFA 的 macOS 驱动程序不实现监听模式或数据包注入功能，仅支持基本 Wi-Fi 客户端连接。这适用于 Intel 和 Apple Silicon Mac 上的所有 macOS 版本。如需监听模式，必须使用 Linux（在虚拟机中或单独的 Raspberry Pi 设备上）。

### 哪款 ALFA 无线网卡最适合 Mac 用户？

对于进行无线安全审计的 Mac 用户，**AWUS036ACH**（RTL8812AU）是最佳选择，它是 Kali Linux 监听模式和数据包注入的黄金标准。对于 Linux 虚拟机中的零安装即插即用体验，推荐 **AWUS036ACM**（MT7612U），因为其驱动自 Linux 4.19 起已包含在内核中。

### 为什么我的 ALFA 网卡在我的 MacBook Pro M3 上无法工作？

Apple Silicon Mac（M1/M2/M3/M4）使用无法加载 x86_64 内核扩展的 ARM64 内核。Realtek 的 macOS Wi-Fi 驱动仅支持 x86_64，Rosetta 2 无法翻译内核扩展。此外，Apple 的 NetworkingDriverKit 框架仅支持以太网，不支持 Wi-Fi，因此没有现代 DriverKit 路径。Realtek 已放弃 macOS 驱动开发。

### 是否有任何 USB Wi-Fi 适配器能在 Apple Silicon macOS 上运行？

**没有。** 截至 2026 年，没有任何第三方 USB Wi-Fi 适配器（ALFA、TP-Link、Netgear、ASUS 等）能在 Apple Silicon macOS 上原生运行。这是架构层面的限制，而非驱动可用性问题。Apple 的官方建议使用带以太网的旅行路由器替代。

### 我能使用 Mac 内置 Wi-Fi 进行监听模式吗？

**可以，但有局限性。** macOS 内置 Wi-Fi 通过 `airport` 实用程序（`sudo airport en0 sniff 11`）支持基本监听模式。然而，它一次只能在一个信道上捕获，不支持数据包注入，且内置天线范围有限。对于专业无线审计，需要在 Linux 虚拟机中使用外部 ALFA 网卡。

### 让 ALFA 网卡在 Mac 上工作的最简单方法是什么？

最简单的方法是：安装 [UTM](https://mac.getutm.app/)（免费），创建 Kali Linux ARM 虚拟机，插入 AWUS036ACM（MT7612U），通过 USB 透传分配给虚拟机。MT7612U 驱动自 Linux 4.19 起即包含在内核中，无需安装驱动，插入即用。

### 我需要在 Mac 上使用带供电的 USB 集线器连接 ALFA 网卡吗？

在配备 USB-A 端口的 Mac（Mac Mini、Mac Studio、较旧的 MacBook Pro/Air）上，不需要，900 mA 输出已足够。在仅配备 USB-C/Thunderbolt 端口的 Mac 上，15 W（3 A）输出绰绰有余。唯一的例外是 Mac Mini M4 的前置 USB-C 端口，仅提供 500 mA，请使用后置 Thunderbolt 端口。

---

## 8. 资源与驱动链接

### 官方资源

| 资源 | URL |
|----------|-----|
| Yupitek 官方网站 | [https://www.yupitek.com](https://www.yupitek.com) |
| Yupitek ALFA 产品页 | [https://yupitek.com/en/products/alfa/](https://yupitek.com/en/products/alfa/) |
| ALFA Network 官方 | [https://www.alfa.com.tw](https://www.alfa.com.tw) |
| Yupitek ALFA 对比表 | [https://yupitek.com/alfa_compare.html](https://yupitek.com/alfa_compare.html) |

### Linux 驱动仓库（GitHub）

| 芯片组 | ALFA 型号 | GitHub 仓库 | 驱动类型 |
|---------|-------------|-------------------|-------------|
| RTL8812AU | AWUS036ACH, AWUS036ACS | [morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820) | DKMS（推荐） |
| RTL8812AU | AWUS036ACH | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) | 社区（已弃用） |
| RTL8812AU | AWUS036ACH | [lwfinger/rtw88](https://github.com/lwfinger/rtw88) | 主线（内核≥6.14） |
| MT7612U | AWUS036ACM | Linux 即内核（`mt76`） | 即内核（≥4.19） |
| MT7921AUN | AWUS036AXML, AWUS036AXM | Linux 即内核（`mt7921u`） | 即内核（≥5.18） |
| MT7610U | AWUS036ACHM | [imzyxwvu/mt7610u](https://github.com/imzyxwvu/mt7610u) | 内核外 |
| RTL8832BU | AWUS036AX, AWUS036AXER | [morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi) | 有限支持 |

### macOS 驱动（仅限 Intel Mac）

| 驱动 | URL | 支持的 macOS | Apple Silicon |
|--------|-----|-----------------|---------------|
| chris1111 Wireless-USB-Big-Sur-Adapter | [GitHub](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) | Catalina 至 Tahoe 26 | ❌ 仅限 Intel |

### Apple 开发者文档

| 文档 | URL |
|----------|-----|
| 已弃用的内核扩展 | [developer.apple.com/support/kernel-extensions/](https://developer.apple.com/support/kernel-extensions/) |
| NetworkingDriverKit（仅以太网） | [developer.apple.com/documentation/networkingdriverkit](https://developer.apple.com/documentation/networkingdriverkit) |
| 安全扩展内核 | [support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) |

### 虚拟机软件

| 软件 | URL | 费用 |
|----------|-----|------|
| UTM | [mac.getutm.app](https://mac.getutm.app/) | 免费 |
| Parallels Desktop | [parallels.com](https://www.parallels.com/) | 99 美元/年 |
| VMware Fusion | [vmware.com](https://www.vmware.com/products/fusion.html) | 个人使用免费 |

---

*本文基于从 Apple 开发者文档、GitHub 仓库（chris1111、aircrack-ng、morrownr）、ALFA Network 产品规格、Reddit/GitHub 社区报告以及实际测试文档中整理而成的技术研究。所有产品推荐均基于 Yupitek 当前在售的 ALFA 产品线。*

*⚠️ 本文所述设备和技术仅用于授权的信息安全审计和合法渗透测试。用户必须确保遵守当地法律法规。*

---
*文章版本：1.0 | 2026-06-20 | Yupitek Ltd.*