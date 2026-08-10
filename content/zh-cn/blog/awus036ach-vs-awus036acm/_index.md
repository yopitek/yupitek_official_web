---
title: "ALFA AWUS036ACH vs AWUS036ACM：Kali Linux 全面对比（2026）"
description: "详细对比 ALFA AWUS036ACH 与 AWUS036ACM——芯片组、监听模式、数据包注入、驱动支持，以及哪款更适合 Kali Linux 渗透测试。"
date: 2026-03-23
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "对比", "Kali-Linux", "RTL8812AU", "MT7612U"]
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
faq:
  - question: "AWUS036ACH 和 AWUS036ACM 驱动安装有什么差异？"
    answer: "AWUS036ACH 采 RTL8812AU 芯片，需通过 DKMS 编译安装 aircrack-ng 社群驱动，内核更新后可能需重新编译；AWUS036ACM 的 MT7612U 驱动自核心 4.19 起整合进主线，即插即用无需编译。"
  - question: "哪款更适合 Monitor Mode 监听？"
    answer: "AWUS036ACH 监听模式更稳定，双天线与 30 dBm 高功率在密集 AP 环境下数据包遗失率更低；ACM 亦支持监听但单天线功率较低，适合近距离捕获。"
  - question: "新手应该选 ACH 还是 ACM？"
    answer: "新手建议选 AWUS036ACM，MT7612U 核心原生驱动即插即用免编译；若需最强信号与最多教学资源且不怕 DKMS 编译流程，再选 AWUS036ACH。"
  - question: "VM 虚拟机环境推荐哪款？"
    answer: "VM 环境推荐 AWUS036ACM，USB 直通后核心原生驱动立即识别可用，无需在虚拟机内安装编译工具链；ACH 需在 VM 内额外安装驱动方能使用。"
---
在 Kali Linux 渗透测试领域，ALFA Network 最受欢迎的两款 USB 网卡分别代表着截然不同的取舍方向。**AWUS036ACH** 是高功率、双天线的实力派，背后有久经考验的驱动历史；**AWUS036ACM** 则是紧凑型、内核原生方案，以简洁易用换取了部分性能上的让步。本文从每一个对渗透测试工程师真正重要的维度，全面剖析这两款网卡。

## 概述

{{< tldr >}}
AWUS036ACH 适合专业任务，RTL8812AU 驱动搭配 30 dBm 双天线，监听注入最强；AWUS036ACM 求便携，MT7612U 核心原生驱动零编译，价格约 $30–40。
{{< /tldr >}}


专业渗透测试选 AWUS036ACH：RTL8812AU 驱动成熟、30 dBm 双天线带来最强监听与数据包注入。求即插即用便携选 AWUS036ACM：MT7612U 核心原生驱动，自核心 4.19 起即插即用零编译。




---

## AWUS036ACH — AC1200，RTL8812AU，高功率

[AWUS036ACH](/zh-cn/products/alfa/awus036ach/) 自发布以来便是专业和业余 WiFi 安全测试的标配，也是 2017 年至今绝大多数 Kali Linux 无线渗透测试教程、课程和解题报告所引用的网卡。

**完整规格：**
- **WiFi 标准：** IEEE 802.11a/b/g/n/ac（Wi-Fi 5）
- **芯片组：** Realtek RTL8812AU
- **工作频段：** 2.4 GHz + 5 GHz（双频）
- **最高吞吐量：** AC1200（300 + 867 Mbps）
- **天线：** 2× 可拆卸 RP-SMA 接口（双天线分集）
- **默认天线：** 2× 5 dBi 全向天线
- **USB 接口：** USB-C（兼容 USB 3.0）
- **发射功率：** 最高 30 dBm — USB 网卡中最高功率之列
- **外形尺寸：** 较大机身（适合台式/出差使用）

双 RP-SMA 接口是一项显著优势：你可以随时更换高增益定向或全向天线，大幅延伸覆盖范围，这对远距离审计场景至关重要。

---

## AWUS036ACM — AC600，MT7612U，紧凑型

[AWUS036ACM](/zh-cn/products/alfa/awus036acm/) 面向优先追求简洁性、便携性和内核原生驱动支持的用户。它采用 MediaTek MT7612U（或 MT7612UN）芯片组，该驱动自 Linux **内核 4.19 版本**起已进入主线，这意味着在任何现代 Kali Linux 系统上**无需安装任何驱动程序**。

**完整规格：**
- **WiFi 标准：** IEEE 802.11a/b/g/n/ac（Wi-Fi 5）
- **芯片组：** MediaTek MT7612U / MT7612UN
- **工作频段：** 2.4 GHz + 5 GHz（双频）
- **最高吞吐量：** AC600（150 + 433 Mbps）
- **天线：** 1× 可拆卸 RP-SMA 接口
- **默认天线：** 1× 5 dBi 全向天线
- **USB 接口：** USB-C（兼容 USB 3.0）
- **发射功率：** 标准功率（低于 ACH）
- **外形尺寸：** 紧凑机身（便携使用）

单天线和较低的发射功率意味着远距离性能不及 ACH，但干净的内核驱动体验和小巧的机身，使它在需要隐蔽性或机动性的场景中颇具实用价值。

---

## 完整规格对比表

| 特性 | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **WiFi 标准** | 802.11ac（Wi-Fi 5） | 802.11ac（Wi-Fi 5） |
| **芯片组** | RTL8812AU | MT7612U / MT7612UN |
| **工作频段** | 2.4 GHz + 5 GHz | 2.4 GHz + 5 GHz |
| **最高吞吐量** | AC1200 | AC600 |
| **RP-SMA 接口** | 2× | 1× |
| **发射功率** | 最高 30 dBm | 标准功率 |
| **USB 接口** | USB-C | USB-C |
| **驱动来源** | 树外驱动（DKMS） | 内核主线（4.19+） |
| **驱动安装** | 手动编译 | 即插即用 |
| **监听模式** | ★★★★★ | ★★★★☆ |
| **数据包注入** | ★★★★★ | ★★★★☆ |
| **外形尺寸** | 较大 | 紧凑 |
| **参考价格** | 约 $40–50 | 约 $30–40 |

---

## 芯片组深度解析

### RTL8812AU（AWUS036ACH）

Realtek RTL8812AU 是无线安全研究领域测试最为广泛的芯片组之一。社区维护的驱动程序托管在 [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)，自 2017 年以来持续开发和修复。

**Kali Linux 安装方法：**

```bash
sudo apt update
sudo apt install dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

通过 DKMS 安装后，模块在内核更新时会自动持久化。该驱动支持：

- **监听模式** — 功能完整，极为稳定
- **帧注入** — 支持所有注入类型（deauth、beacon、probe、data）
- **多虚拟接口** — 可同时运行监听模式和管理模式接口
- **WPA3-SAE 握手包捕获** — 在近期内核/驱动组合下已确认可用

主要权衡：安装新内核时**必须重新编译**（DKMS 通常会自动处理）。偶尔某个新的 Kali 内核版本会导致编译暂时失败，需等待驱动更新修复。这是可以管理的真实风险，但确实存在。

### MT7612U（AWUS036ACM）

MediaTek MT7612U 的驱动程序（`mt76x2u`）于 **2018 年 10 月随 Linux 内核 4.19 版本**合并入主线。这意味着在任何运行 4.19 及以上内核的 Kali Linux 系统上——涵盖 2018 年底以来的所有 Kali 版本——AWUS036ACM 都是**即插即用**的。

```bash
# 验证模块是否已加载
lsmod | grep mt76x2u

# 如需手动加载
sudo modprobe mt76x2u
```

驱动关键特性：

- **无需编译** — 在隔离网络或受限环境中尤为有利
- **监听模式** — 已支持，功能正常
- **数据包注入** — 已支持，整体可靠
- **稳定性** — 内核原生驱动在内核更新时往往更为稳定
- **社区支持** — 持续增长，但规模仍小于 RTL8812AU 生态系统

一个细节：部分 ACM 批次采用 MT7612UN 变体，在 Linux 下的行为与 MT7612U 完全相同，均由 `mt76x2u` 模块驱动。

---

## 监听模式对比

两款网卡均支持监听模式，但实际使用体验存在差异。

**AWUS036ACH（RTL8812AU）：**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# 创建处于监听模式的 wlan0mon 接口
iwconfig wlan0mon
```

监听模式下的信道切换即时且可靠。即便在高流量环境（大量 AP 密集分布、众多客户端）中，以正常抓包速率工作时也不会出现丢包现象。

**AWUS036ACM（MT7612U）：**

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# 或通过 airmon-ng：
sudo airmon-ng start wlan0
```

监听模式功能正常，已在 Wireshark、tcpdump、airodump-ng 和 kismet 下得到确认。不过，在某些内核版本上，部分用户反映直接使用 `iw` 比使用 airmon-ng 更为稳定可靠。

---

## 数据包注入对比

**AWUS036ACH：** 数据包注入是其最突出的卖点之一，所有 aireplay-ng 攻击模式均可稳定使用：

```bash
# 测试注入
sudo aireplay-ng --test wlan0mon

# deauth 攻击
sudo aireplay-ng -0 5 -a [BSSID] wlan0mon

# 通过 deauth 捕获 WPA 握手包
sudo airodump-ng -c [CH] --bssid [BSSID] -w capture wlan0mon &
sudo aireplay-ng -0 3 -a [BSSID] wlan0mon
```

**AWUS036ACM：** 注入功能在所有标准攻击类型上均可使用，但有用户反映，在某些内核版本上以极高速率注入时，接口偶尔会出现卡顿。对于典型的渗透测试工作流（受控 deauth、PMKID 捕获、KRACK 测试），表现总体可靠。

---

## 驱动安装复杂度对比

| 场景 | AWUS036ACH | AWUS036ACM |
|---|---|---|
| 全新 Kali 安装后插入网卡 | 无法识别，需安装驱动 | 立即识别 |
| 内核更新后 | DKMS 通常自动重编译 | 无需任何操作 |
| 离线（隔离网络）环境 | 需提前准备离线安装包 | 原生支持，无需网络 |
| Kali Live USB 环境 | 需在当前会话中安装驱动 | 开箱即用 |
| VirtualBox/VMware USB 直通 | 在虚拟机中安装驱动后可用 | 在虚拟机中立即可用 |

ACM 的零安装体验在以下场景中具有真实优势：Live 启动环境、客户提供的机器、或 CTF 比赛中时间紧迫且追求简洁的场合。

---

## 尺寸与便携性

**AWUS036ACH** 的 PCB 和外壳明显更大，这部分源于双 RP-SMA 接口和 30 dBm 输出所需的更大功率元器件。放在笔记本电脑包里没有问题，但谈不上"口袋"级别的便携。

**AWUS036ACM** 体积明显更小，可以在实地安全评估时低调使用，或在大型 USB 网卡容易引起注意的环境中保持隐蔽。它的功耗也更低，对于长时间外出作业仅靠笔记本电池供电的情况来说，这一点很有价值。

---

## 价格与价值

AWUS036ACH 售价约 $40–50，溢价主要来自双天线配置、高发射功率和久经考验的驱动积累。对于可靠性和信号强度直接影响交付质量的专业项目，这份溢价物有所值。

AWUS036ACM 约 $30–40，以下人群能从中获得极高性价比：
- 希望即插即用、快速上手无线安全学习的学生
- 主要在近距离环境中作业的测试人员
- 需要备用或第二块网卡的团队
- 任何优先追求无编译、干净工作流的人

---


{{< faq >}}

## 选购结论

**选择 [AWUS036ACH](/zh-cn/products/alfa/awus036ach/)，适合：**
- 专业、正式的渗透测试项目
- 追求监听模式和数据包注入的最高可靠性
- 需要外置天线支持（双 RP-SMA）的远距离评估
- 信号强度至关重要的场景（停车场审计、定向目标）
- 对现有教程、课程和文档兼容性要求最高的情况

**选择 [AWUS036ACM](/zh-cn/products/alfa/awus036acm/)，适合：**
- 追求零驱动编译的即插即用体验
- 便携、低调的作业场景
- 预算有限或作为第二块备用网卡
- Kali Live USB 工作流
- 在内核原生稳定性优先于社区驱动的情况

如果只能拥有一款网卡，**AWUS036ACH** 在渗透测试方面是更强的选择。如果你需要一个零配置、随时可用的出行伴侣，**AWUS036ACM** 绝对值得在工具包中占有一席之地。

## 参考文献

1. aircrack-ng 社群维护 RTL8812AU 驱动程序仓库 — [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. Linux 核心主线 MT76 驱动程序（`mt76x2u`，自核心 4.19 起整合）— [kernel.org — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
3. ALFA Network 官方网站与产品规格 — [alfa.com.tw](https://www.alfa.com.tw)
4. Yupitek — ALFA Network 台湾授权经销商 — [yupitek.com](https://www.yupitek.com)
