---
title: "ALFA WiFi 网卡购买指南 2026：哪款型号最适合你？"
description: "2026年完整ALFA Network USB WiFi网卡购买指南。比较AWUS036ACH、ACM、ACS、AX、AXER、AXM、AXML、EACS的驱动支持、监控模式、操作系统兼容性与价格。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
---

本指南专为网络安全工程师、企业IT专业人员及红队成员而撰写，帮助你在2026年选出最适合的ALFA Network USB WiFi网卡。我们完整涵盖八款现行量产型号——[AWUS036ACS](/zh-cn/products/alfa/awus036acs/)、[AWUS036ACH](/zh-cn/products/alfa/awus036ach/)、[AWUS036ACM](/zh-cn/products/alfa/awus036acm/)、[AWUS036EACS](/zh-cn/products/alfa/awus036eacs/)、[AWUS036AX](/zh-cn/products/alfa/awus036ax/)、[AWUS036AXER](/zh-cn/products/alfa/awus036axer/)、[AWUS036AXM](/zh-cn/products/alfa/awus036axm/) 与 [AWUS036AXML](/zh-cn/products/alfa/awus036axml/)——比较芯片组、驱动成熟度、操作系统支持与实际使用场景，让你少花时间排查驱动问题，专注于真正重要的工作。

---

## 如何选择：4个关键问题

在打开任何产品页面之前，请先回答以下四个问题。你的答案将立即帮助你排除大部分选项。

### (a) 你使用的是哪个操作系统？

驱动支持决定一切。使用近期内核版本的Kali Linux与Ubuntu用户拥有最广泛的选择。macOS对所有型号的支持都相当有限。Windows 10/11普遍支持良好。如果你使用的是Raspberry Pi或ARM平台，芯片组的选择至关重要。

- **Kali Linux / Debian：** RTL8812AU（`dkms-rtl8812au`）与MT7921AUN（内核原生支持 ≥ 5.18）是两大主要芯片家族。
- **Ubuntu 22.04 / 24.04：** 驱动环境相同，但你可能需要安装HWE内核或`firmware-misc-nonfree`以支持MT7921AUN。
- **Windows 10/11：** ALFA提供所有现行型号的已签名驱动，安装流程简单。
- **macOS Sonoma：** 仅有少数型号拥有社区维护的kext支持，预期会遇到阻力；请规划使用VM工作流程。
- **Raspberry Pi（Kali NetHunter、ARM）：** RTL8812AU型号是最安全的选择。MT7921AUN可以运行，但需要`firmware-misc-nonfree`软件包与足够新的内核。

### (b) 你需要监控模式与数据包注入吗？

如果答案是肯定的——任何渗透测试或无线审计工作都应如此——请立即将[AWUS036EACS](/zh-cn/products/alfa/awus036eacs/)从你的清单中划掉。其RTL8821CU芯片在Linux下不可靠地支持监控模式或注入功能。本指南中的其他所有型号均支持。

### (c) 虚拟机还是裸机？

VirtualBox与VMware的USB直通会增加一层复杂性。此清单上的任何型号在正确配置直通后均可运行，但RTL8812AU网卡（ACH、ACM）在VM环境中拥有最长的验证记录。如果你只使用直通至VM，应避免使用依赖运行时加载固件的网卡——USB连接中断意味着固件丢失。

详细配置说明请参阅[ALFA网卡在VirtualBox与VMware中的配置](/zh-cn/blog/alfa-adapter-virtualbox-vmware-usb/)。

### (d) 预算是多少？

Wi-Fi 5世代（ACH、ACM、ACS）价格较低、驱动更稳定，如果预算有限或驱动稳定性是首要考量，这是正确的选择。Wi-Fi 6/6E世代（AX、AXER、AXM、AXML）是硬件发展方向，但你需要支付更高费用，并在非主线内核上接受一些驱动边界情况。

---

## 完整ALFA网卡对比表

<div style="overflow-x: auto;">

| 型号 | WiFi代际 | 芯片 | 最高速度 | 监控模式 | Kali驱动 | Windows | macOS | 天线 | 最适用途 |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/zh-cn/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | 轻量旅行装备 |
| [AWUS036ACH](/zh-cn/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | 红队作战 |
| [AWUS036ACM](/zh-cn/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | 平价双频 |
| [AWUS036EACS](/zh-cn/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ⚠️ | rtl88xxcu | ✅ | ✅ | 1× RP-SMA | 普通使用（不支持注入）|
| [AWUS036AX](/zh-cn/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated | Wi-Fi 6审计 |
| [AWUS036AXER](/zh-cn/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated nano | 延伸范围Wi-Fi 6 |
| [AWUS036AXM](/zh-cn/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E入门 |
| [AWUS036AXML](/zh-cn/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | 旗舰6E |

</div>

**图例：** ✅ 支持 · ⚠️ 有限/部分支持 · ❌ 不支持

{{< alert "circle-info" >}}
**macOS注意事项：** 所有ALFA网卡在macOS Ventura与Sonoma上都面临驱动挑战。最常见的社区方案是在VM中使用Kali Linux搭配USB直通。AWUS036EACS是例外——可能通过原生macOS Realtek驱动运行，但不支持监控模式。
{{< /alert >}}

---

## Wi-Fi 5网卡（最成熟的驱动支持）

Wi-Fi 5世代背后拥有多年的社区开发积累。如果你的优先考量是坚如磐石的驱动稳定性——尤其用于CTF竞赛、专业审计，或内核更新后不容有驱动故障的环境——从这里开始选择。

### AWUS036ACH — 红队作战标准配置

[AWUS036ACH](/zh-cn/products/alfa/awus036ach/)在安全社区中依然是部署最广泛的ALFA网卡，原因充分。其RTL8812AU芯片组由`aircrack-ng/rtl8812au`驱动支持，多年来针对每个主要Kali Linux版本进行维护与测试。

**硬件规格：**
- 芯片组：RTL8812AU（Realtek）
- 两个可拆卸RP-SMA天线接口——兼容完整ALFA天线产品线
- 500 mW发射功率——Wi-Fi 5产品线中最高
- 双频：2.4 GHz与5 GHz

**为何领先红队场景：** 500 mW发射功率搭配双外部天线与成熟的注入支持，让你在远距离作业时仍能可靠地传输数据包。将备附的全向天线换成[APA-M25](/zh-cn/products/alfa/apa-m25/)定向面板天线，即可打造一套严肃的远距离平台。双天线设计在连接目标网络时也能实现正确的2T2R MIMO。

**在Kali上安装驱动：**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
在内核 ≥ 6.2上，旧版Kali镜像所含的原版`rtl8812au`模块可能无法加载。请务必从Kali仓库安装`dkms-rtl8812au`——它会追踪内核变更，并通过DKMS在内核更新时自动重新编译。
{{< /alert >}}

### AWUS036ACM — 平价双频首选

[AWUS036ACM](/zh-cn/products/alfa/awus036acm/)采用MediaTek MT7612U芯片组——与ACH的RTL8812AU属于不同家族。其最大优势是自内核4.19起以`mt76x2u`驱动整合至Linux主线内核，这意味着在任何现代Kali Linux或Ubuntu系统上都无需编译驱动。出厂配备两个RP-SMA接口，支持双天线操作。

功能上，监控模式与注入支持对安全工作完全适用。

如果你只需要一个天线端口，且不需要ACH的扩展发射功率，ACM以更低的成本覆盖相同的使用场景。对于需要大量购买供审计团队使用的情况，这是常见选择。

**何时选ACM而非ACH：** 零麻烦的Linux驱动设置、在Ubuntu/Kali上无需编译即插即用、以比ACH更低的价格实现双天线覆盖。

### AWUS036ACS — 轻巧便携

[AWUS036ACS](/zh-cn/products/alfa/awus036acs/)使用RTL8811AU芯片组——发射功率略低于RTL8812AU，但仍完全支持监控模式与数据包注入。其紧凑的外形与单天线设计，使其成为频繁出差顾问的首选——无需携带多根RP-SMA天线通过机场安检。

RTL8811AU驱动在Kali上使用相同的`rtl8812au-dkms`包，安装流程完全一致。

**与ACH/ACM的权衡：** 较低发射功率（远距离范围较小）、单天线（无MIMO）、AC600对AC1200最高吞吐量。对于大多数抓包与注入工作流程，这些差异无关紧要。对于远距离操作，则有所影响。

### AWUS036EACS — 普通使用，不适用于渗透测试

[AWUS036EACS](/zh-cn/products/alfa/awus036eacs/)采用Realtek RTL8821CU芯片组。RTL8821CU的Linux驱动支持有限——不支持监控模式与数据包注入。此网卡专为Windows客户端连接设计，并包含蓝牙4.2，不适用于安全测试任务。

{{< alert "triangle-exclamation" >}}
**请勿将AWUS036EACS用于渗透测试、红队作战或任何需要监控模式或数据包注入的任务。** 它适合一般无线连接、DJI无人机控制器距离延伸（常见配对用途），以及标准客户端网卡行为可接受的Windows优先部署环境。
{{< /alert >}}

---

## Wi-Fi 6网卡（Windows优先）

Wi-Fi 6（802.11ax）在密集环境性能、目标丰富的MU-MIMO场景与用于网络识别的BSS着色方面带来了显著改进。AWUS036AX与AWUS036AXER是ALFA的Wi-Fi 6网卡，主要针对Windows连接设计。

两款Wi-Fi 6 ALFA网卡均使用Realtek RTL8832BU芯片组。在Linux上，RTL8832BU驱动在内核6.14以下为核外驱动（OOK），这意味着**监控模式与数据包注入支持有限**。如果你的主要使用场景是在Linux上进行渗透测试，请选择AWUS036ACH或AWUS036AXML。

### AWUS036AX — Wi-Fi 6 Windows网卡

[AWUS036AX](/zh-cn/products/alfa/awus036ax/)是ALFA的Wi-Fi 6网卡，配备集成天线（无外接RP-SMA接口）。在2.4和5 GHz双频上提供AX1200速度，非常适合Windows 10/11连接使用。

**驱动状态：**
- Windows：通过ALFA提供的驱动完整支持
- Linux内核 ≥ 6.14：内核内置RTL8832BU驱动
- Linux内核 < 6.14：需要核外驱动
- 监控模式：⚠️ 有限
- 数据包注入：⚠️ 有限

{{< alert "triangle-exclamation" >}}
**Linux渗透测试注意事项：** AWUS036AX使用RTL8832BU芯片组，在Linux内核6.14以下的监控模式与数据包注入支持有限。如需Kali Linux安全工作，请改用[AWUS036ACH](/zh-cn/products/alfa/awus036ach/)（RTL8812AU）或[AWUS036AXML](/zh-cn/products/alfa/awus036axml/)（MT7921AUN）。
{{< /alert >}}

### AWUS036AXER — 轻巧旅行Wi-Fi 6网卡

[AWUS036AXER](/zh-cn/products/alfa/awus036axer/)采用与AWUS036AX相同的RTL8832BU芯片组，但采用超紧凑纳米外形（10.5g）。驱动情况完全相同——同样的RTL8832BU、同样的Linux限制、同样的Windows兼容性。

当携带便利性是决定性因素时，请选择AXER而非AX：商务出行、最小化部署，或偏好紧凑加密狗而非全尺寸网卡的情况。

---

## Wi-Fi 6E网卡（面向未来）

Wi-Fi 6E将802.11ax扩展至6 GHz频段，提供对新5.925–7.125 GHz频谱的访问。实际上，这意味着更少的干扰、更宽的信道宽度（最高160 MHz），以及旧设备无法看到或到达的频段。随着企业网络部署Wi-Fi 6E基础设施，审计人员需要6E能力的网卡来评估完整的攻击面。

两款Wi-Fi 6E ALFA网卡都需要内核 ≥ 5.18才能支持6 GHz。6 GHz频段要求正确设置无线电监管域——大多数司法管辖区对6 GHz的监管执行比2.4/5 GHz更严格。

### AWUS036AXM — Wi-Fi 6E入门款

[AWUS036AXM](/zh-cn/products/alfa/awus036axm/)使用MT7921AUN芯片组，完整支持三频包含6 GHz。出厂配备两个RP-SMA接口，支持2T2R双天线操作。

对于主要在2.4和5 GHz环境工作，但希望在不支付旗舰价格的情况下具备6 GHz能力以应对新兴网络评估的操作人员，AXM是合乎逻辑的入门点。

**频段覆盖：** 2.4 GHz、5 GHz、6 GHz（三频）
**天线：** 2× RP-SMA——可更换为任何兼容的ALFA天线

### AWUS036AXML — 旗舰6E网卡

[AWUS036AXML](/zh-cn/products/alfa/awus036axml/)是ALFA目前的旗舰网卡。具备MT7921AUN芯片组、USB-C 3.2连接、蓝牙5.2，以及单一高增益RP-SMA接口。

**关键规格：**
- 芯片组：MT7921AUN（MediaTek）
- 1× RP-SMA接口——兼容完整ALFA天线产品线
- 三频：2.4 GHz + 5 GHz + 6 GHz
- AX3000级别（跨频段理论最高3000 Mbps）
- USB-C 3.2——比USB-A更快的主机总线带宽

{{< alert "triangle-exclamation" >}}
**AWUS036AXML固件注意事项：** 在内核6.1以下，部分用户在AXML的监控模式与管理模式之间重复切换时会遇到固件崩溃。如果你的工作流程需要频繁切换模式，请使用内核 ≥ 6.1并安装最新的`firmware-misc-nonfree`包。
{{< /alert >}}

---

## 驱动兼容性深入分析

<div style="overflow-x: auto;">

| 型号 | 芯片 | Kali软件包 | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/zh-cn/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | 手动编译 | ✅ rtl8812au-dkms | ✅ ALFA驱动 |
| [AWUS036ACH](/zh-cn/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | 手动编译 | ✅ rtl8812au-dkms | ✅ ALFA驱动 |
| [AWUS036ACM](/zh-cn/products/alfa/awus036acm/) | MT7612U | `mt76x2u` (in-kernel) | 内核 ≥ 4.19 | ✅ mt76x2u (≥4.19) | ✅ ALFA驱动 |
| [AWUS036EACS](/zh-cn/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` | 内核内置 | ⚠️ 有限 | ✅ 内置 |
| [AWUS036AX](/zh-cn/products/alfa/awus036ax/) | RTL8832BU | `firmware-misc-nonfree` | 内核 ≥ 5.18 | ⚠️ 需要固件 | ✅ ALFA驱动 |
| [AWUS036AXER](/zh-cn/products/alfa/awus036axer/) | RTL8832BU | `firmware-misc-nonfree` | 内核 ≥ 5.18 | ⚠️ 需要固件 | ✅ ALFA驱动 |
| [AWUS036AXM](/zh-cn/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | 内核 ≥ 5.18 | ⚠️ 需要固件 | ✅ ALFA驱动 |
| [AWUS036AXML](/zh-cn/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | 内核 ≥ 5.18 | ⚠️ 需要固件 | ✅ ALFA驱动 |

</div>

**RTL8812AU内核历史：** RTL8812AU驱动在Linux 5.2中部分整合至主线内核，但有显著限制——无监控模式、无注入。完整的渗透测试能力需要树外`rtl8812au`驱动，在Kali上打包为`dkms-rtl8812au`。DKMS包在内核更新时自动重新编译，在Kali Linux系统上几乎免维护。

**MT7921AUN内核历史：** 原生集成于Linux 5.18，通过`mt7921u` USB驱动实现。固件文件`WIFI_MT7961_patch_mcu_1_2_hdr.bin`（及相关固件）必须存在于`/lib/firmware/mediatek/`。在Kali上由`firmware-misc-nonfree`提供。在Ubuntu 22.04 LTS默认内核上，可能需要安装HWE栈（`linux-generic-hwe-22.04`）才能达到 ≥ 5.18。

**Raspberry Pi特别说明：** RTL8812AU驱动在Raspberry Pi OS（32位与64位）上使用`dkms-rtl8812au`可以顺利编译，是NetHunter部署的最安全选择。MT7921AUN网卡在Pi 4/5上可以运行，但需要`firmware-misc-nonfree`与足够新的Raspberry Pi OS内核（2023年以后的镜像应可正常使用）。

---

## 按使用场景推荐最佳ALFA网卡

### 红队作战

**推荐：[AWUS036ACH](/zh-cn/products/alfa/awus036ach/)**

ACH的500 mW发射功率、双天线与久经验证的RTL8812AU驱动，使其成为红队任务的默认选择。内核更新后可靠运行、VM直通稳定，接受你携带的任何RP-SMA天线。如果预算允许且6E覆盖在范围内，可加入[AWUS036AXML](/zh-cn/products/alfa/awus036axml/)作为6 GHz网络探索的辅助网卡。

### CTF竞赛

**推荐：[AWUS036ACM](/zh-cn/products/alfa/awus036acm/)**

CTF无线挑战通常在受控环境中进行，发射功率并非关键变量。ACM以更低的价格提供完整的监控模式与注入能力。其紧凑的单天线外形易于携带和部署。如果CTF涉及Wi-Fi 6挑战（仍然罕见但在增加），请改用[AWUS036AX](/zh-cn/products/alfa/awus036ax/)。

### Raspberry Pi / Kali NetHunter

**推荐：[AWUS036ACH](/zh-cn/products/alfa/awus036ach/) 或 [AWUS036ACM](/zh-cn/products/alfa/awus036acm/)**

两款RTL8812AU网卡在Raspberry Pi硬件上都有久经验证的记录。除非你已确认在特定镜像上的内核与固件兼容性，否则请避免在Pi部署中使用MT7921AUN型号。如果你正在构建需要在外勤中可靠运行的专用NetHunter Pi，ACH是更安全的选择。

### 企业无线审计

**推荐：[AWUS036AXML](/zh-cn/products/alfa/awus036axml/) + [AWUS036ACH](/zh-cn/products/alfa/awus036ach/)**

现代企业无线审计应覆盖2.4、5与6 GHz频段。AXML覆盖包含6E的完整三频段，而ACH为5 GHz工作提供稳定、高功率的备选方案。使用独立捕获接口同时运行两者，可在不妥协驱动的情况下提供完整的频段覆盖。使用ACH执行主动注入任务，AXML进行被动6 GHz监听。

### DJI无人机距离延伸

**推荐：[AWUS036EACS](/zh-cn/products/alfa/awus036eacs/)**

通过Litchi或DJI GO进行DJI距离延伸是常见的合法使用场景。此处特别推荐EACS搭配RTL8821CU，因为它在Windows（DJI软件运行平台）上无需额外驱动即可原生运行，且其通用连接特性适合此使用场景。无需监控模式；客户端连接能力与发射功率才是重点。搭配[APA-M25](/zh-cn/products/alfa/apa-m25/)面板天线以获得最大有效距离。

---

## 操作系统专属建议

### Kali Linux

Kali Linux是所有用于安全工作的ALFA网卡的主要支持平台。Kali仓库包含RTL8812AU/RTL8811AU网卡的`dkms-rtl8812au`，以及MT7921AUN/MT7921AUN网卡的`firmware-misc-nonfree`。保持Kali安装更新——DKMS包会自动追踪内核变更。

**快速配置（RTL8812AU家族）：**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**快速配置（MT7921AUN家族）：**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# 重新启动或重新加载模块：
sudo modprobe mt7921u
```

**启用监控模式：**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04搭载内核6.8。安装`firmware-misc-nonfree`后，MT7921AUN网卡可直接使用：
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

Ubuntu上的RTL8812AU支持需要编译DKMS模块：
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

所有ALFA网卡均附带Windows 10/11兼容驱动。可从ALFA Network官网下载驱动包，或通过Windows Update安装MT7921AUN（Microsoft提供WHQL签名的收件箱驱动）。RTL8812AU网卡需要ALFA提供的Realtek驱动包；Windows Update对RTL8812AU的驱动支持不一致。

### macOS Sonoma

2026年没有官方支持的ALFA macOS Sonoma网卡。RTL8812AU的社区kext项目存在，但未签名且需要禁用系统完整性保护（SIP）。实际建议是在VM（Parallels、VMware Fusion或UTM）中运行Kali Linux，并对ALFA网卡进行USB直通。

### Raspberry Pi / Kali NetHunter

在运行Kali NetHunter的Raspberry Pi 4和Pi 5上：

```bash
# 用于RTL8812AU网卡：
sudo apt update && sudo apt install -y dkms-rtl8812au

# 用于MT7921AUN网卡（建议使用配备近期内核的Pi 5）：
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
如果你正在构建专用的NetHunter投放盒，请使用[AWUS036ACH](/zh-cn/products/alfa/awus036ach/)或[AWUS036ACM](/zh-cn/products/alfa/awus036acm/)。其RTL8812AU驱动在ARM上可靠编译，且没有固件文件依赖。MT7921AUN型号在Pi上可以运行，但在离线部署中增加了固件依赖的麻烦。
{{< /alert >}}

---

## 最终推荐

评估所有八款网卡的驱动成熟度、硬件能力与实际使用场景后，以下三款选择涵盖了大多数专业人员的需求：

**平价首选：[AWUS036ACM](/zh-cn/products/alfa/awus036acm/)**
单天线RTL8812AU网卡以双频产品线中最低的价格提供完整的监控模式与数据包注入支持。非常适合希望在不超支的情况下获得可靠工具的顾问，或大量购买的团队。

**万能首选：[AWUS036ACH](/zh-cn/products/alfa/awus036ach/)**
双天线、500 mW RTL8812AU网卡是安全专业人员中推荐最广的单款网卡。覆盖2.4和5 GHz，接受外部天线，拥有此清单中任何网卡中最成熟的驱动栈，且价格仅比ACM略高。如果你只买一款网卡且尚未确定需求，就买这款。

**企业/面向未来首选：[AWUS036AXML](/zh-cn/products/alfa/awus036axml/)**
如果你的审计范围包含Wi-Fi 6E基础设施——2026年开始的任何任务都应该如此——AXML是唯一能提供双天线6 GHz能力的网卡。与ACH搭配组成双网卡套件，可无妥协地覆盖从2.4 GHz到6 GHz的每个频段。

更多详细配置说明，请参阅：
- [在Kali Linux和Ubuntu上安装ALFA驱动](/zh-cn/blog/install-alfa-driver-kali-ubuntu/)
- [内核更新后修复ALFA驱动](/zh-cn/blog/fix-alfa-driver-kernel-update/)
- [在Kali Linux上启用监控模式](/zh-cn/blog/enable-monitor-mode-kali-linux/)
- [AWUS036AXML Wi-Fi 6E评测与驱动测试](/zh-cn/blog/awus036axml-wifi-6e-review/)
