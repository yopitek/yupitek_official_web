---
title: "在 macOS 使用 ALFA WiFi 网卡：VMware Fusion 与 Parallels USB 直通完整指南"
description: "如何在 macOS 使用 ALFA USB WiFi 网卡。涵盖 macOS 原生支持、VMware Fusion USB 直通、Parallels Desktop，以及在 Kali Linux 启用监听模式与数据包注入。"
date: 2026-04-15
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
---

macOS 是一个精致、适合生产环境的操作系统，但它并非为无线安全研究而设计。每位渗透测试人员工具箱中最核心的两项功能——**监听模式（Monitor Mode）**与**数据包注入（Packet Injection）**——在 macOS 的 Wi-Fi 协议栈中完全不存在。Apple 的 Wi-Fi 驱动程序提供了一个干净、功能完整的网络接口，仅此而已。

ALFA Network 网卡在 Linux 上改变了这一局面，驱动程序支持深入且经过社区验证。在 macOS 上情况则不同。即使 ALFA 网卡被 macOS 识别，原生网络协议栈也不允许你将其切换至监听模式或注入原始数据包。唯一可靠的解决路径是在**虚拟机中运行 Kali Linux**，并将 USB 网卡直接透传给客户端操作系统，完全绕过 macOS。

本指南涵盖如何在两大主流 macOS 虚拟化软件——VMware Fusion 与 Parallels Desktop——上正确完成这项配置，并特别针对 **Apple Silicon（M1/M2/M3）** 提供说明，因为 ARM 架构对网卡与 ISO 镜像的选择有额外限制。

---

## macOS 原生支持：不需 VM 可以做到什么

在直接进入 VM 配置前，了解 macOS 搭配 ALFA 网卡能做什么、不能做什么是有价值的。

**AWUS036AXML（MT7921AU 芯片）：** macOS 会将此网卡识别为通用 USB 网络设备。macOS 13 Ventura 及更新版本内置的 **MT7921AU** 驱动程序会自动识别此网卡。它会出现在**系统偏好设置 → 网络**（Ventura 以上为**系统设置 → 网络**）中，可像普通网卡一样连接 Wi-Fi。在较旧的 macOS 版本上可能完全无法识别。

**RTL8812AU 系列网卡（AWUS036ACH、AWUS036ACM）：** 这些网卡在 macOS 上需要第三方驱动程序。社区和商业驱动套件都有，但兼容性不稳定。macOS 小版本更新后常需重新安装驱动程序，macOS 11 起内核扩展签名要求更加严格，而在 Apple Silicon 上由于 Rosetta 对内核扩展的限制，情况更加脆弱。

**硬性限制——没有监听模式：** 无论使用哪款网卡或安装何种驱动程序，macOS 不提供原始监听模式接口。CoreWLAN 框架与底层 `IO80211Family.kext` 架构不支持第三方网卡的监听模式。对于安全测试，必须使用搭载 USB 直通的 Kali Linux VM。

{{< alert "circle-info" >}}
如果你的目标仅是被动 Wi-Fi 流量捕获（用于调试，非安全测试），macOS 允许按住 Option 并点击菜单栏的 Wi-Fi 图标进入诊断模式。但这无法取代正式的监听模式工作流程。
{{< /alert >}}

---

## Apple Silicon（M1/M2/M3）vs Intel Mac

你的 Mac 架构决定了需要哪个 Kali Linux 镜像，以及哪些虚拟化软件可用。

**Intel Mac（x86_64）：**
三大主流虚拟化软件——VMware Fusion、Parallels Desktop 与 VirtualBox——在 Intel Mac 上均可原生运行。可使用来自 kali.org 官方下载页面的标准 **Kali Linux x86_64 ISO**。VM 内的驱动程序编译步骤与所有在线 Kali 指南一致。

**Apple Silicon（M1/M2/M3）：**
Apple Silicon 是 ARM64 架构。标准 x86_64 Kali ISO 即使在虚拟化软件内也无法在 Apple Silicon 硬件上启动——没有 x86 模拟层（Rosetta 只适用于 macOS 用户空间应用程序，不适用于完整 OS 虚拟化）。必须使用 **Kali Linux ARM64** 镜像，可在 [kali.org/get-kali](https://www.kali.org/get-kali/) 的 Apple Silicon / ARM 区段找到。

| 虚拟化软件 | Intel Mac | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ 个人使用免费 | ✅ 支持 ARM64 VM |
| Parallels Desktop 19+ | ✅ | ✅ Apple Silicon 最佳性能 |
| VirtualBox 7.x | ✅ | ⚠️ Apple Silicon 上仍为实验性 |

{{< alert "triangle-exclamation" >}}
VirtualBox 对 Apple Silicon 的支持仍标记为实验性。USB 直通在 M 芯片 Mac 上存在已知问题。对于安全测试工作流程，请在 Apple Silicon 硬件上使用 VMware Fusion 或 Parallels Desktop。
{{< /alert >}}

**USB 直通与架构无关：** ALFA 网卡本身是 USB 设备。主机 CPU 是 x86_64 还是 ARM64 不影响 USB 直通的运作方式。网卡通过 USB 总线移交给客户端 VM，由 Kali 内的驱动程序接管。架构只影响使用哪个 Kali 镜像以及 VM 内驱动程序的编译方式。

---

## 方案 A：VMware Fusion USB 直通

VMware Fusion 自 Fusion 13 起个人使用免费，是 macOS 用户寻求零成本虚拟化软件的默认推荐，且具备稳定的 USB 直通支持。

### 步骤 1 — 安装 VMware Fusion 13+

从 [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html) 下载 VMware Fusion。安装时需在**系统偏好设置 → 安全性与隐私 → 通用**中允许 VMware 系统扩展。此扩展批准是 USB 直通正常运作的必要条件。批准后 macOS 可能要求重启，请完成重启后再继续。

### 步骤 2 — 创建 Kali Linux VM

- **Apple Silicon Mac：** 从 kali.org 下载 Kali Linux ARM64 安装 ISO 或预构建的 VMware ARM 镜像，在 VMware Fusion 中创建新 VM 并选择该 ARM64 ISO。
- **Intel Mac：** 下载标准 Kali Linux x86_64 安装 ISO，创建新 VM 并选择该 ISO 作为安装介质。

至少分配 **4 GB RAM** 与 **40 GB 磁盘**。Kali 安装时选择完整默认软件包集，以预先安装无线工具（aircrack-ng、airmon-ng、airodump-ng）。

### 步骤 3 — 通过 USB 直通连接 ALFA 网卡

在 Kali VM 运行中且 ALFA 网卡插入 Mac USB 端口的情况下：

1. VMware Fusion 会显示弹出窗口：**"USB 设备正在请求连接到您的虚拟机。"**
2. 点击**连接到 [VM 名称]** 将网卡直接移交给 Kali VM。
3. macOS 此时会失去对该网卡的可见性——它现在由 VM 独占。

{{< alert "circle-info" >}}
如果弹出窗口未出现，请前往 VMware Fusion 菜单栏：**虚拟机 → USB 与蓝牙 → [ALFA 网卡名称] → 连接（从 Mac 断开连接）**，手动将 USB 设备分配给 VM。
{{< /alert >}}

### 步骤 4 — 在 Kali 内验证

在 Kali VM 的终端中确认网卡可见：

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AU: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

### 步骤 5 — 加载驱动程序并验证监听模式

MT7921AU（AWUS036AXML）的驱动程序已内置于 Kali 内核。RTL8812AU 网卡需要安装驱动程序——请参阅[驱动程序安装指南](/zh-cn/blog/install-alfa-driver-kali-ubuntu/)。驱动程序激活后：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

---

## 方案 B：Parallels Desktop USB 直通

Parallels Desktop 是 Apple Silicon Mac 性能优先时的首选虚拟化软件。它需要订阅授权，但其 ARM64 VM 支持与 USB 直通实现在 Apple Silicon 硬件上比 VMware Fusion 更成熟。

### 步骤 1 — Parallels Desktop 19+

从 [parallels.com](https://www.parallels.com) 安装 Parallels Desktop。与 VMware Fusion 相同，需在**安全性与隐私**中允许 Parallels 系统扩展并重启。

### 步骤 2 — 创建 Kali Linux ARM64 VM

在 Apple Silicon 上，Parallels 仅支持 ARM64 客户端 OS 镜像。从 kali.org 下载 Kali Linux ARM64 镜像，在 Parallels 中使用该镜像创建新 VM。

{{< alert "circle-info" >}}
Parallels Desktop 19+ 在 Apple Silicon 上的新 VM 向导中可直接下载并安装 Kali Linux ARM——你可能不需要手动下载 ISO。
{{< /alert >}}

在 Intel Mac 上，标准 x86_64 Kali ISO 可直接在 Parallels 中使用。

### 步骤 3 — 通过 USB 连接 ALFA 网卡

在 Kali VM 运行中且 ALFA 网卡插入的情况下：

1. 在 macOS 菜单栏，前往**设备 → USB 与蓝牙**。
2. 在列表中找到你的 ALFA 网卡（可能显示为 **Realtek 802.11ac NIC**、**MediaTek Wi-Fi** 或类似名称）。
3. 点击它并选择**连接到 Linux**（或你的 VM 名称）。

### 步骤 4 — 使用 lsusb 验证

在 Kali VM 终端中：

```bash
lsusb
ip link show
```

{{< alert "circle-info" >}}
在 Apple Silicon 上，Parallels 的 I/O 密集型 VM 工作负载性能通常优于 VMware Fusion。如果你进行长时间的 airodump-ng 会话或大量数据包捕获，Parallels 通常会产生较低的 CPU 开销。
{{< /alert >}}

---

## Kali on Apple Silicon：ARM64 驱动程序说明

**RTL8812AU on ARM64：**
来自 [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) 的 RTL8812AU 驱动程序可在 ARM64 上正确编译。DKMS 构建流程与 x86_64 相同：

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**MT7921U on ARM64：**
`mt7921u` 驱动程序自 **Linux 5.18 起已内置于内核**，包含在 Kali ARM64 2024.x 及更新版本中。AWUS036AXML 在 Kali ARM64 上不需要手动编译，USB 直通后网卡会自动识别。

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**M 芯片 Mac 推荐：** 如果你是专门为在 Apple Silicon Mac 上的 VM 中使用而购买 ALFA 网卡，**AWUS036AXML（MT7921AU）** 是更好的选择。其内置内核驱动程序完全省去 DKMS 编译步骤，并在 ARM64 Kali 上可靠运作。

---

## 监听模式与注入测试

完成 USB 直通后，执行以下命令序列验证完整协议栈是否正常运作：

```bash
# 1. 确认 USB 设备可见
lsusb

# 2. 列出无线接口
ip link show

# 3. 终止冲突的进程
sudo airmon-ng check kill

# 4. 在无线接口上启动监听模式
sudo airmon-ng start wlan1

# 5. 确认监听接口已创建
ip link show wlan1mon

# 6. 开始被动扫描
sudo airodump-ng wlan1mon
```

**如果直通后 `wlan1` 未出现：**
拔出 ALFA 网卡，等待五秒后重新插入，通过 Hypervisor 的 USB 设备菜单重新分配给 VM，然后在 Kali 内再次执行 `lsusb` 确认设备出现。

{{< alert "triangle-exclamation" >}}
不要尝试对 VM 内默认的 `wlan0` 接口执行 `airmon-ng start wlan0`——该接口通常是 VMware/Parallels 用于互联网连接的虚拟网络接口，而非透传的 ALFA 网卡。
{{< /alert >}}

---

## 性能与限制

**USB 直通延迟：** 通过 Hypervisor 层传递 USB 设备比在裸机 Linux 上使用网卡多约 1–2 ms 的处理延迟。对于 802.11 安全测试目的，这个延迟在操作上并不显著。

**独占所有权：** macOS 无法同时与 Kali VM 共享 ALFA 网卡。一旦网卡透传给 VM，它就会从 macOS 完全消失。若要将网卡还给 macOS，请通过 Hypervisor 的 USB 设备菜单从 VM 断开连接，然后拔出并重新插入网卡。

**电力消耗：** 在 VM 中运行 USB Wi-Fi 网卡同时还运行 Mac 自身的 Wi-Fi 无线电，电力消耗相当可观。**长时间测试时请使用充电器**，尤其是在 Apple Silicon MacBook 上。

---

## 故障排除

| 症状 | 可能原因 | 解决方案 |
|---|---|---|
| ALFA 网卡未出现在 Hypervisor USB 菜单 | macOS 系统扩展未批准 | **系统偏好设置 → 安全性与隐私 → 通用** → 允许 VMware/Parallels 扩展，然后重启 |
| Kali VM 内 `lsusb` 未显示 ALFA 网卡 | USB 直通未完成 | 通过 VM → USB 与蓝牙菜单手动连接；重新插拔网卡 |
| 直通后缺少 `wlan1` 接口 | 驱动程序未加载（RTL8812AU） | 通过 DKMS 安装 RTL8812AU 驱动程序；请参阅[驱动程序安装指南](/zh-cn/blog/install-alfa-driver-kali-ubuntu/) |
| `airmon-ng start wlan1` 失败并显示「Operation not permitted」 | NetworkManager 占用接口 | 先执行 `sudo airmon-ng check kill`，然后重试 |
| 监听模式启动但 airodump-ng 未显示网络 | 信道或接口错误 | 用 `ip link show` 确认 `wlan1mon` 存在；尝试 `sudo airodump-ng --band abg wlan1mon` |
| 插入 ALFA 网卡时 VM 卡死 | USB 控制器冲突（VMware） | 关闭 VM，前往 VM 设置 → USB，将控制器从 USB 3.0 切换为 USB 2.0，重新启动 VM |

{{< alert "circle-info" >}}
在 Apple Silicon 上，如果 ALFA 网卡被识别但接口未出现在 Kali 中，请在插入后立即执行 `dmesg | tail -30`，输出会显示内核是否检测到设备以及哪个驱动程序正在尝试绑定。
{{< /alert >}}

---

## 相关指南

针对在 Windows 和 Linux 主机上使用 VirtualBox 或 VMware Workstation 的用户，请参阅配套指南：[ALFA 网卡 USB 直通：VirtualBox 与 VMware 配置指南](/zh-cn/blog/alfa-adapter-virtualbox-vmware-usb/)。

有关本指南推荐的 AWUS036AXML 网卡详细信息，请参阅完整评测：[ALFA AWUS036AXML WiFi 6E 评测](/zh-cn/blog/awus036axml-wifi-6e-review/)。
