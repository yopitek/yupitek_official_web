---
title: "ALFA 无线网卡 Windows 10/11 安装配置完整指南"
description: "如何在 Windows 10/11 上安装和配置 ALFA USB WiFi 无线网卡。驱动下载、使用 Acrylic WiFi 的监听模式、故障排查及 Windows 用户网卡对比。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "wifi-网卡", "驱动安装", "acrylic-wifi"]
---

ALFA Network USB WiFi 无线网卡在安全研究和网络工程领域广为人知，但大多数教程都以 Linux 为主。对于 Windows 用户来说，有个好消息：所有主流 ALFA 网卡均可在 Windows 10 和 Windows 11 上通过厂商提供的驱动正常运行——无需编译源代码。

与 Linux 的关键区别在于监听模式（Monitor Mode）。在 Linux 上，`aircrack-ng`、`airodump-ng` 等工具借助原始 802.11 捕获能力实现数据包注入。而在 Windows 上，驱动模型（NDIS，网络驱动接口规范）并未暴露相同的硬件能力。**Windows 原生不支持完整的监听模式和数据包注入。** Windows 的优势在于即插即用的网络连接，以及搭配 Acrylic WiFi Analyzer 等成熟工具的 WiFi 扫描能力。

本指南涵盖驱动安装、WiFi 扫描，以及对 Windows 平台使用 ALFA 网卡能力边界的客观评估。

---

## 适用于 Windows 的 ALFA 网卡型号

以下所有网卡均已在 Windows 10 和 Windows 11 上获得官方支持。驱动可用性和监听模式支持情况因芯片组而异。

| 型号 | 芯片组 | Windows 10 | Windows 11 | 监听模式支持 |
|---|---|---|---|---|
| [AWUS036ACH](/zh-cn/products/alfa/awus036ach/) | RTL8812AU | ✅ 完整支持 | ✅ 完整支持 | ⚠️ 仅被动扫描（Acrylic WiFi Pro） |
| [AWUS036ACM](/zh-cn/products/alfa/awus036acm/) | MT7612U | ✅ 完整支持 | ✅ 完整支持 | ⚠️ 仅被动扫描 |
| [AWUS036ACS](/zh-cn/products/alfa/awus036acs/) | RTL8811AU | ✅ 完整支持 | ✅ 完整支持 | ⚠️ 仅被动扫描 |
| [AWUS036AX](/zh-cn/products/alfa/awus036ax/) | RTL8832BU | ⚠️ 需手动下载驱动 | ✅ 系统内置驱动 | ⚠️ 有限支持 |
| [AWUS036AXER](/zh-cn/products/alfa/awus036axer/) | RTL8832BU | ⚠️ 需手动下载驱动 | ✅ 系统内置驱动 | ⚠️ 有限支持 |
| [AWUS036AXM](/zh-cn/products/alfa/awus036axm/) | MT7921AUN | ⚠️ 需手动下载驱动 | ✅ 系统内置驱动 | ❌ 不支持 |
| [AWUS036AXML](/zh-cn/products/alfa/awus036axml/) | MT7921AUN | ⚠️ 需手动下载驱动 | ✅ 系统内置驱动 | ❌ 不支持 |

{{< alert "circle-info" >}}
日常 Windows 使用的首选是 AWUS036ACH（RTL8812AU）和 AWUS036ACM（MT7612U）。两款网卡均配备经 WHQL 认证签名的 Realtek/MediaTek 驱动，Windows 兼容性记录最为完善。
{{< /alert >}}

---

## 安装驱动

### 方法 A：通过 Windows Update 安装（推荐）

Windows Update 是大多数网卡最便捷的驱动安装途径。将受支持的 ALFA 网卡插入后，Windows 会自动查询 Windows Update 以匹配对应的 NDIS 驱动。

1. 将 ALFA 网卡插入 USB 3.0 接口。
2. 等待 30–60 秒。Windows 10 会显示通知：*"设备驱动程序软件已成功安装"*；Windows 11 则会静默完成安装。
3. 打开**设备管理器**（`Win + X` → 设备管理器）。
4. 展开**网络适配器**。您应能看到该网卡（例如 *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* 或 *"MediaTek Wi-Fi 6 MT7921U Wireless LAN Card"*）。
5. 若网卡显示黄色警告图标，请继续使用方法 B。

{{< alert "circle-info" >}}
Windows Update 需要有效的互联网连接才能下载驱动。如果您正在配置隔离的实验环境，请在另一台计算机上下载驱动包，手动传输后再使用方法 B 安装。
{{< /alert >}}

### 方法 B：手动安装驱动 — RTL8812AU（AWUS036ACH / AWUS036ACM / AWUS036ACS）

1. 前往 [ALFA Network 下载页面](https://www.alfa.com.tw/service_1.html) 或 Realtek 驱动归档站点，下载最新 RTL8812AU 的 Windows WHQL 驱动。
2. 将 `.zip` 压缩包解压至本地文件夹（例如 `C:\Drivers\RTL8812AU`）。
3. 以管理员身份运行 `.exe` 安装程序，并接受 UAC 提示。
4. 按照安装向导操作，安装路径保持默认。
5. 安装完成后重启系统。
6. 打开**设备管理器** → **网络适配器**，确认网卡显示无警告图标。

验证驱动版本：

1. 在设备管理器中右键单击网卡 → **属性**。
2. 点击**驱动程序**标签页。
3. 记录**驱动程序版本**和**驱动程序日期**，以备日后参考。

### 方法 B：手动安装驱动 — MT7921AUN（AWUS036AX / AWUS036AXER / AWUS036AXM / AWUS036AXML）

MediaTek MT7921AUN 驱动已内置于 Windows 11 驱动存储库（build 22000+）。对于 Windows 10：

1. 从 [MediaTek 官方网站](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) 或 ALFA Network 支持页面下载 MediaTek MT7921 驱动包。
2. 解压后以管理员身份运行 `Setup.exe`。
3. 安装后重启系统。

{{< alert "circle-info" >}}
使用 MT7921AUN/MT7921AUN 网卡的 Windows 11 用户，通常在插入网卡后数分钟内即可获得可用驱动，全新安装系统亦无需手动下载。
{{< /alert >}}

### 常见设备管理器错误代码

| 错误代码 | 含义 | 首要解决方法 |
|---|---|---|
| **Code 43** | 驱动程序报告故障 | 卸载驱动 → 重启 → 重新安装 |
| **Code 10** | 设备无法启动 | 尝试其他 USB 接口；禁用 USB 选择性挂起 |
| **Code 28** | 未安装驱动 | 运行 Windows Update 或手动安装驱动 |
| **Code 45** | 设备未连接 | 重新连接网卡；如使用延长线请更换 USB 数据线 |

---

## 在 Windows 上使用 ALFA 网卡进行 WiFi 扫描

### Windows 原生命令行扫描

Windows 内置 WiFi 扫描命令，无需额外软件：

```cmd
netsh wlan show networks mode=bssid
```

此命令输出所有可见 SSID，包括 BSSID（MAC 地址）、信号强度、无线电类型、信道及认证类型。适合快速诊断，但缺乏实时信道图表或隐藏 SSID 检测功能。

### Acrylic WiFi Analyzer（免费版）

在 Windows 上进行专业 WiFi 分析，推荐使用 [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/)。免费版功能包括：

- 实时扫描 2.4 GHz、5 GHz 及 6 GHz 频段
- 信道占用图表——即时识别拥塞信道
- 隐藏 SSID 检测（显示广播空 SSID 的网络）
- 单个接入点的信号历史曲线
- 通过 BSSID 进行厂商 OUI 查询

Acrylic WiFi 兼容所有 Windows 支持的 WiFi 网卡，包括上述所有 ALFA 型号。其 NDIS 驱动扩展直接集成于 Windows 无线协议栈，因此无需 Linux 式的监听模式即可正常工作。

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer 是 Windows 上最接近 `airodump-ng` 的被动扫描工具。如果您的工作流涉及 WiFi 勘测、站点分析或信道规划，它几乎可以满足全部需求，无需离开 Windows 环境。
{{< /alert >}}

### 在 Windows 上使用 Wireshark 抓包

借助 Npcap，Wireshark 可在 Windows 上捕获 WiFi 流量（详见下方专项章节）。但在没有真正监听模式的情况下，您只能捕获：

- 发往本机网卡的帧（单播至本机 MAC）
- 已关联网络上的广播帧和多播帧

在交换网络中以混杂模式（Promiscuous Mode）运行 Wireshark 时，**您无法捕获其他设备之间的流量**（除非它们恰好在同一广播域）。完整 802.11 帧捕获（管理帧、来自其他 AP 的信标帧）受到限制。

---

## Windows 监听模式的实情

以下内容需要明确预期。

**Windows 上的监听模式与 Linux 监听模式存在本质差异。**

在 Linux 上，`aircrack-ng/rtl8812au` 等驱动暴露真正的监听模式接口（`wlan0mon`），可接收无线环境中所有 802.11 帧——包括管理帧、其他网络的数据帧、探测请求和信标帧——无需关联任何网络。同时支持数据包注入：在硬件层发送原始 802.11 帧。

在 Windows 上，NDIS 驱动模型不具备上述能力。Windows 平台监控的两种可行方案为：

**方案 A：Acrylic WiFi Pro + 兼容驱动**

Acrylic WiFi Pro 通过自定义 NDIS 驱动扩展实现*被动 802.11 扫描*，可接收未关联接入点的信标帧和探测响应——足以支撑射频勘测、信道分析和 AP 枚举。**不支持**数据包注入或完整握手包捕获。

**方案 B：Kali Linux Live USB**

对于需要完整监听模式和数据包注入的工作流——WPA 握手包捕获、去认证测试、信标洪泛——正确的平台是 Kali Linux。有两种部署选项：

- 在同一台机器上启动 **Kali Linux Live USB**（裸机运行，完整硬件访问权限）
- 运行 **Kali Linux 虚拟机**（VMware 或 VirtualBox），通过 USB 直通将 ALFA 网卡直接交给虚拟机的 USB 控制器

详细虚拟机配置说明请参阅 [VirtualBox/VMware USB 直通指南](/zh-cn/blog/alfa-adapter-virtualbox-vmware-usb/)。

{{< alert "triangle-exclamation" >}}
如果您的工作流需要监听模式和数据包注入——用于 WPA 握手包捕获、去认证帧发送或任何主动 802.11 攻击——Windows 无法可靠地完成这些任务。Kali Linux（裸机或带 USB 直通的虚拟机）才是正确平台。目前没有任何 Windows 驱动支持 ALFA 网卡的原始 802.11 注入。
{{< /alert >}}

---

## 故障排查

### 网卡完全无法识别

1. 更换 USB 接口——优先使用 USB 3.0（蓝色接口）。部分 USB Hub 供电不足，无法驱动双频网卡。
2. 打开设备管理器，在**其他设备**下查找带黄色问号的条目，确认 Windows 检测到硬件但缺少驱动。
3. 右键单击 → **更新驱动程序** → **浏览我的计算机以查找驱动程序**，指向手动下载的驱动文件夹。
4. 若设备管理器的**其他设备**下也未出现任何条目，请更换 USB 数据线（如使用延长线），或在其他计算机上测试该网卡以排除硬件故障。

### 设备管理器中可见但无法搜索到网络

1. 临时禁用 Windows Defender 防火墙，确认是否阻碍了网卡初始化；测试后及时重新启用。
2. 在设备管理器中右键单击网卡 → **属性** → **高级**标签页，查找**无线模式**或**频段**设置。若设置为仅 5 GHz，在纯 2.4 GHz 环境中将搜索不到任何网络。
3. 确认网卡未被禁用：右键单击 → **启用设备**。
4. 在提升权限的命令提示符中运行 `netsh wlan show interfaces`，验证网卡的运行状态。

### Windows 11 下速度缓慢或频繁断线

Windows 11 的 **Connected Standby**（现代待机，Modern Standby）会激进地挂起 USB 设备，可能干扰 USB WiFi 网卡的正常工作。

禁用 USB 选择性挂起：

1. 打开**控制面板** → **电源选项** → **更改计划设置** → **更改高级电源设置**。
2. 展开 **USB 设置** → **USB 选择性挂起设置**。
3. 将**使用电池**和**已接通电源**均设置为**已禁用**。
4. 点击**应用** → **确定**，然后重启系统。

### Code 43：驱动程序报告故障

1. 打开设备管理器，右键单击网卡 → **卸载设备**。如出现"删除此设备的驱动程序软件"选项，请勾选。
2. 拔出网卡。
3. 重启计算机。
4. 重新插入网卡。
5. 按上述方法 B 重新安装驱动。

若全新安装后 Code 43 仍然存在，请更换 USB 接口或在其他机器上测试。多台机器均出现持续性 Code 43，通常表明网卡本身存在硬件故障。

---

## ALFA 网卡 + Wireshark 配置

Windows 上的 Wireshark 需要 **Npcap** 作为数据包捕获库。WinPcap（旧版替代方案）已停止维护，对现代 Windows 版本的支持不可靠。

### 第一步：安装 Npcap

1. 从 [https://npcap.com/](https://npcap.com/) 下载 Npcap（个人和教育用途免费）。
2. 以管理员身份运行安装程序。
3. 安装过程中，如需与 Wireshark 同时使用旧版工具，请勾选 **"Install Npcap in WinPcap API-compatible mode"**。
4. 重启系统。

### 第二步：配置 Wireshark

1. 打开 Wireshark，ALFA 网卡将显示在接口列表中。
2. 双击该接口开始捕获。
3. 若要过滤 802.11 管理帧（信标帧、探测请求），使用以下 Wireshark 显示过滤器：

```
wlan.fc.type == 0
```

4. 仅过滤探测请求：

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
`wlan.fc.type` 过滤器仅在 Wireshark 收到包含可见头部的真实 802.11 帧时生效。在 Windows 未启用监听模式的情况下，大多数捕获结果显示的是 Ethernet II 帧——NDIS 层在将帧传递给 Npcap 之前已剥离 802.11 头部。完整的 802.11 头部捕获需要真正的监听模式接口，该功能仅在 Linux 上可用。
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
未经授权捕获网络流量在大多数司法管辖区属于违法行为。请仅在您拥有或已获得明确书面授权的网络上进行抓包。
{{< /alert >}}

---

## 总结：ALFA 网卡在 Windows 与 Linux 上的对比

| 功能 | Windows 10/11 | Kali Linux |
|---|---|---|
| **即插即用** | ✅ 自动安装驱动 | ⚠️ 因芯片组而异 |
| **WiFi 扫描** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **监听模式** | ⚠️ 仅被动（Acrylic Pro） | ✅ 完整监听模式 |
| **数据包注入** | ❌ 不支持 | ✅ 完整注入 |
| **Wireshark 抓包** | ⚠️ 有限（无 802.11 头部） | ✅ 完整 802.11 捕获 |
| **WPA 握手包捕获** | ❌ 不可靠 | ✅ aircrack-ng / hcxdumptool |
| **最佳使用场景** | 日常网络连接、WiFi 勘测、信道分析 | 安全测试、CTF 挑战、渗透测试 |

结论：当您的目标是网络连接、WiFi 分析和信道规划时，Windows 是使用 ALFA 网卡的优秀平台。一旦工作流需要原始 802.11 帧注入或 WPA 握手包捕获，请切换至 Kali Linux——无论是裸机运行还是带 USB 直通的虚拟机。

---

## 相关指南

- [VirtualBox 和 VMware USB 直通配置 ALFA 网卡](/zh-cn/blog/alfa-adapter-virtualbox-vmware-usb/) — 在虚拟机中以完整 ALFA 网卡支持运行 Kali Linux
- [Kali Linux 和 Ubuntu 驱动安装指南](/zh-cn/blog/install-alfa-driver-kali-ubuntu/) — 各芯片组完整驱动安装步骤
- [ALFA WiFi 网卡选购指南 2026](/zh-cn/blog/alfa-wifi-adapter-buyer-guide-2026/) — 根据使用场景选择合适的网卡
