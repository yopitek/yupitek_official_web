---
title: "ALFA 网卡 USB 直通：VirtualBox 与 VMware 设置指南"
description: "逐步教程：在 VirtualBox 和 VMware Workstation 上为 Kali Linux 配置 ALFA USB WiFi 网卡的 USB 直通。涵盖 AWUS036ACH、AWUS036AXML、USB 3.0 过滤器、Extension Pack 及故障排除。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
---

在虚拟机内使用 ALFA WiFi 网卡并非像插入后等待客户端操作系统自动识别那么简单。与共享文件夹或桥接网络不同，监听模式和原始数据包注入需要**完整的 USB 控制权**——虚拟机必须独占 USB 设备，而不是通过主机的网络栈共享。这称为 USB 直通（USB passthrough），正确配置是在 VM 环境中工作的渗透测试人员和 CTF 玩家最常遇到的设置失败原因。

本指南涵盖 **VirtualBox 7.x** 和 **VMware Workstation 17+ / VMware Fusion 13+** 的完整直通设置，以 Kali Linux 作为客户端操作系统。文中针对 AWUS036ACH（RTL8812AU 芯片组）和较新的 AWUS036AXML（MT7921AUN 芯片组）分别说明行为差异。

完成后，您的 ALFA 网卡将在 Kali 中通过 `lsusb` 显示，正确驱动程序已加载，且 `airmon-ng` 确认监听模式正常工作。

---

## 前提条件

开始之前，请确认您的环境符合以下要求。缺少任何一项——尤其是 VirtualBox Extension Pack——是大多数直通失败的根本原因。

| 需求 | 详细说明 |
|---|---|
| **虚拟化平台** | VirtualBox 7.x + Extension Pack **或** VMware Workstation 17+ / Fusion 13+ |
| **客户端操作系统** | Kali Linux 2024.x 或更新版本（已在 2024.1–2025.1 测试） |
| **ALFA 网卡** | AWUS036ACH、AWUS036AXML、AWUS036ACM，或任何 RTL8812AU / MT7921AUN 设备 |
| **主机 USB 接口** | 建议使用 USB 3.0（尤其是 AWUS036AXML） |
| **主机操作系统** | Windows 10/11、Linux 或 macOS（Fusion） |
| **Sudo 权限** | Kali VM 内部需要 |

{{< alert "circle-info" >}}
若您尚未在 Kali 内安装驱动程序，请先完成本指南的 USB 直通步骤。网卡在 VM 中可见后，再按照 [ALFA 驱动程序安装指南](/zh-cn/blog/install-alfa-driver-kali-ubuntu/) 编译并加载正确的驱动程序。
{{< /alert >}}

---

## VirtualBox USB 直通——逐步操作

VirtualBox 需要一个额外的组件——**Extension Pack**——才能支持 USB 2.0 和 USB 3.0 直通。若未安装，只能使用 USB 1.1（OHCI），这对现代 ALFA 网卡来说是不够的。

### 安装 VirtualBox Extension Pack

1. 打开 [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)。
2. 在 **VirtualBox Extension Pack** 下，点击 **All supported platforms** 下载 `.vbox-extpack` 文件。版本必须与您安装的 VirtualBox 版本完全一致。
3. 打开 VirtualBox，前往 **文件 → 首选项 → 扩展**（macOS：**VirtualBox → 偏好设置 → 扩展**）。
4. 点击 **+** 图标，浏览到下载的 `.vbox-extpack`，然后安装。出现提示时接受许可证。

从命令行验证 Extension Pack 是否已激活：

```bash
VBoxManage list extpacks
```

预期输出：

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
若 **Usable** 字段显示 `false`，表示 Extension Pack 版本与 VirtualBox 版本不匹配。请卸载后重新安装正确版本。
{{< /alert >}}

### 将用户添加到 vboxusers 组（仅限 Linux 主机）

在 Linux 主机上，您的用户账号必须是 `vboxusers` 组的成员才能访问 USB 设备。

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

执行后，请**注销并重新登录**（或重启）使组更改生效。可以用以下命令验证：

```bash
groups $USER
```

输出应包含 `vboxusers`。

### 在 VM 设置中启用 USB 控制器

1. 若 Kali VM 正在运行，请先关闭。
2. 选择 VM，点击 **设置 → USB**。
3. 勾选 **启用 USB 控制器**。
4. 从单选按钮选择 **USB 3.0 (xHCI) 控制器**。

{{< alert "circle-info" >}}
AWUS036AXML 需要 USB 3.0（xHCI）。AWUS036ACH 本身是 USB 2.0 设备，使用 USB 2.0（EHCI）在技术上已足够，但使用 xHCI 不会造成问题，且能保持配置一致性。
{{< /alert >}}

### 添加 USB 设备过滤器

1. 在同一个 **设置 → USB** 面板中，点击 **+** 图标（从设备添加 USB 过滤器）。
2. 若 ALFA 网卡尚未连接，现在插入。VirtualBox 会在下拉菜单中显示它。
3. 选择设备。通常显示为 **"Realtek 802.11ac NIC"**（AWUS036ACH）或 **"MediaTek Corp. 802.11 b/g/n"**（AWUS036AXML）。
4. 点击 **确定** 保存。

### 启动 VM 并用 lsusb 验证

启动 Kali VM。桌面加载后，打开终端并运行：

```bash
lsusb
```

您应该看到类似以下的输出：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

或 AWUS036AXML：

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

### 加载驱动程序

**AWUS036ACH（RTL8812AU）：**

```bash
sudo modprobe 88XXau
```

若失败（找不到模块），请先安装 DKMS 软件包：

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML（MT7921AUN）：**

```bash
sudo modprobe mt7921u
```

### 验证监听模式

```bash
sudo airmon-ng start wlan1
sudo iwconfig wlan1mon
```

**Mode** 字段应显示 `Monitor`。

### VirtualBox 常见错误

| 错误 | 原因 | 修复方法 |
|---|---|---|
| USB 设置中"无可用 USB 设备" | 未安装 Extension Pack 或版本不符 | 安装对应版本的 Extension Pack |
| 网卡未被捕获 / lsusb 中不可见 | 用户不在 `vboxusers` 组（Linux 主机） | `sudo usermod -aG vboxusers $USER`，然后注销/登录 |
| "USB 设备正被先前的请求使用" | 主机上的其他进程正在使用该设备 | 启动 VM 前拔出并重新插入网卡 |
| 设备在 VM 内持续断线 | 未启用 USB 3.0 控制器；VM 使用 OHCI | 在 VM 设置 → USB 中切换至 USB 3.0（xHCI） |
| 过滤器已添加但设备未自动捕获 | 在安装 Extension Pack 之前创建过滤器 | 删除过滤器，安装 Extension Pack，再重新添加 |

---

## VMware Workstation / VMware Fusion USB 直通

VMware 处理 USB 直通的方式与 VirtualBox 不同。无需安装额外扩展——USB 2.0 和 3.0 支持已内置于 VMware Workstation 17+ 和 Fusion 13+。主要机制是 **USB 仲裁器服务**，负责监控主机 USB 事件并将设备路由至 VM。

### 通过设备菜单连接网卡

在 VM 运行期间插入 ALFA 网卡时，VMware 通常会显示弹出窗口询问哪个 VM 应拥有该设备。若错过弹出窗口：

1. 在 Kali VM 运行时，前往菜单栏的 **VM → 可移动设备**。
2. 展开列表，找到您的 ALFA 网卡（例如 **Realtek 802.11ac NIC**）。
3. 点击 **连接（从主机断开）**。

### VMware Fusion（macOS）

1. 前往 **虚拟机 → USB 与蓝牙**。
2. 在列表中找到 ALFA 网卡。
3. 将连接切换至 **连接到 Linux**（或您的 Kali VM 名称）。

### 验证并加载驱动程序

连接后，在 Kali 内部验证：

```bash
lsusb
```

然后按照上述 VirtualBox 章节加载适当的驱动程序。

### 检查 VMware USB 仲裁器服务

若 ALFA 网卡未出现在 **可移动设备** 菜单中，USB 仲裁器服务可能未运行。在 Linux 主机上：

```bash
sudo systemctl status vmware-usbarbitrator
```

若已停止：

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

### 在 VMware 中启用 USB 3.0

打开 Kali VM 的 `.vmx` 文件，确认或添加：

```
usb_xhci.present = "TRUE"
```

{{< alert "triangle-exclamation" >}}
需要 VMware 硬件版本 14 或更新版本才能支持 USB 3.0（xHCI）。若您的 VM 是以旧版硬件版本创建的，请通过 **VM → 管理 → 更改硬件兼容性** 升级。
{{< /alert >}}

### VMware 常见错误

| 错误 | 原因 | 修复方法 |
|---|---|---|
| 可移动设备菜单中找不到网卡 | USB 仲裁器未运行 | 启动 `vmware-usbarbitrator` 服务 |
| 设备连接后立即断线 | 主机操作系统驱动程序夺回设备 | 禁用主机的网卡 WiFi 驱动程序，或更快速地重新连接 |
| "设备已被主机使用" | 主机操作系统已声明该设备 | 在 VM 中连接前，先从主机移除 |
| VM 内无 USB 3.0 速度 | VM 硬件版本 < 14 或未启用 xHCI | 升级硬件版本，在 .vmx 中添加 `usb_xhci.present = "TRUE"` |
| 直通后监听模式仍失败 | Kali 内驱动程序错误或缺失 | 按照 [驱动程序安装指南](/zh-cn/blog/install-alfa-driver-kali-ubuntu/) 操作 |

---

## 网卡特定说明

### AWUS036ACH（RTL8812AU）

AWUS036ACH 是 **USB 2.0** 设备，在 VM 环境中是测试最充分的网卡之一。VirtualBox 和 VMware 都能可靠地处理它。驱动程序包：`realtek-rtl88xxau-dkms`。模块名称：`88XXau`。

### AWUS036AXML（MT7921AUN）

AWUS036AXML 是支持 WiFi 6E 的 **USB 3.0** 设备，在 VM 环境中有一些特殊情况。**必须**使用 USB 3.0（xHCI）控制器。固件包：`firmware-misc-nonfree`。某些早期型号在 VirtualBox USB 3.0 仲裁下可能发生周期性冻结问题。VMware Workstation 对 AWUS036AXML 的 USB 3.0 直通通常比 VirtualBox 更稳定。

完整评测：[AWUS036AXML WiFi 6E 评测](/zh-cn/blog/awus036axml-wifi-6e-review/)。

### AWUS036ACM（RTL8812AU，单天线）

从驱动程序和直通角度来看，与 AWUS036ACH 行为完全相同。使用相同的 `88XXau` 模块和相同的 VirtualBox/VMware 设置。

---

## 性能调优建议

**禁用主机的 USB 自动挂起：**

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

**分配足够的 VM 资源：**
- **2 个 CPU 核心**（建议 4 个）
- **2 GB RAM**（若运行完整 Kali 桌面，建议 4 GB）

**在渗透测试任务前创建 VM 快照。**

{{< alert "circle-info" >}}
对于超过 30 分钟的抓包会话，考虑在网卡和主机之间使用有源 USB 集线器，以提供稳定电源，防止电压降导致网卡在关键抓包期间断线。
{{< /alert >}}

---

## 裸机 vs VM：诚实对比

| 功能 | 裸机 Kali | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **驱动程序支持** | 完整、直接 | 良好（需 Extension Pack） | 良好（内置 USB） |
| **监听模式稳定性** | 优秀 | 良好 | 良好–优秀 |
| **数据包注入可靠性** | 优秀 | 良好（偶尔丢包） | 良好–优秀 |
| **设置时间** | 高（需专用硬件） | 低–中 | 低–中 |
| **可移植性** | 低 | 高（快照、可移植） | 高 |
| **CTF / 实验室使用** | 大材小用 | 理想 | 理想 |
| **专业渗透测试** | 推荐 | 可接受 | 可接受 |

---

## 故障排除快速参考

| 症状 | 最可能原因 | 解决方案 |
|---|---|---|
| Kali 内 `lsusb` 无显示 | USB 直通未配置 | 添加 USB 过滤器（VBox）或通过可移动设备连接（VMware） |
| VirtualBox USB 设置中"无 USB 设备" | Extension Pack 缺失或版本不符 | 安装对应版本的 Extension Pack |
| `lsusb` 可见网卡但无 `wlan` 接口 | 驱动程序未加载 | `sudo modprobe 88XXau` 或 `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | 未安装 DKMS 包 | `sudo apt install realtek-rtl88xxau-dkms` |
| 接口出现后消失 | USB 自动挂起或 VBox xHCI 仲裁 | 禁用自动挂起；ACH 尝试 USB 2.0 控制器 |
| `airmon-ng` 启动但监听模式静默失败 | 驱动程序错误或网络管理器冲突 | `sudo airmon-ng check kill`，然后重试 |
| VirtualBox USB 过滤器开机时未自动捕获 | 在安装 Extension Pack 之前添加过滤器 | 删除过滤器，安装 Extension Pack，重新添加 |
| VMware 在长时间会话中丢失设备 | VMware USB 仲裁器服务停止 | 重新启用并设为自动启动 |

---

## 后续步骤

- **安装或更新驱动程序：** [Kali 与 Ubuntu 的 ALFA 驱动程序安装指南](/zh-cn/blog/install-alfa-driver-kali-ubuntu/)
- **完整 AWUS036ACH 设置教程：** [AWUS036ACH Kali Linux 设置指南](/zh-cn/blog/awus036ach-kali-linux-setup/)
- **AWUS036AXML 硬件评测：** [AWUS036AXML WiFi 6E 评测](/zh-cn/blog/awus036axml-wifi-6e-review/)
