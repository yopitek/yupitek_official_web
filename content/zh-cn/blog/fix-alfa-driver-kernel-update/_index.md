---
title: "ALFA 驱动程序在内核更新后失效？完整修复指南"
description: "Linux 内核更新后 ALFA USB WiFi 网卡无法使用？完整修复指南：涵盖 Kali Linux 与 Ubuntu 上的 RTL8812AU、RTL8811AU 及 MT7921AUN 驱动程序修复方式。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
---

你执行了 `sudo apt upgrade`，重新启动后 ALFA 网卡消失了——没有接口、没有指示灯、什么都没有。这是 Linux 用户询问 ALFA Network USB WiFi 网卡时最常见的问题，而内核更新几乎是所有问题的根源。本指南将带你系统性地诊断并修复两种最常受影响的芯片组：**RTL8812AU**（AWUS036ACH、ACM、ACS）与 **MT7921AUN**（AWUS036AXM、AXML）。按照各节步骤操作，你的网卡应在 15 分钟内恢复正常。

---

## 为什么内核更新会破坏驱动程序

Linux WiFi 驱动程序分为两种：**内核内置**驱动（随内核源码一同发布）与**内核外**驱动（独立存在于内核之外）。了解你使用的是哪一种，就能清楚知道为何更新会造成问题。

### 内核外驱动程序与 DKMS

RTL8812AU 芯片组使用由社区维护的内核外驱动（最常见的是 `aircrack-ng/rtl8812au` 分支）。由于它不属于官方内核源码，必须**针对你目前运行的内核头文件（headers）重新编译**。每当内核版本变更——即使只是小版本更新，如 `6.6.15` → `6.6.20`——已编译的模块便不再兼容，内核会拒绝加载它。

**DKMS（动态内核模块支持）** 是标准解决方案。DKMS 会将驱动程序的源代码注册至系统级的钩子，每当安装新内核软件包时自动重新编译模块。若 DKMS 设置正确，内核更新对你来说是透明的：重新启动进入新内核后，网卡已自动就绪。

DKMS 可能在以下两种情况下静默失败：

1. **缺少内核头文件** — 编译器需要在新内核安装时同步安装 `linux-headers-$(uname -r)`。若头文件在内核之后才到，DKMS 就错过了构建时机。
2. **过时的 `dkms.conf`** — 若已安装驱动程序版本的配置文件已不符合源代码树的结构，构建将以不明确的错误信息失败。

### 内核内置驱动程序（MT7921U）

MT7921U 芯片组自内核 **5.18** 版本起已纳入主线内核。这意味着不需要编译步骤——内核已内置与硬件通信的能力。然而，驱动程序仍依赖一个由独立软件包提供的**固件二进制文件**（`mt7921u.bin`）。若该软件包缺失，或内核更新改变了预期的固件 API，网卡可能看似已加载但无法连接。

### 快速诊断命令

在动手修改任何设置前，先执行以下两条命令了解当前状况：

```bash
# 目前运行的内核版本是什么？
uname -r

# 哪些 DKMS 模块已构建（以及针对哪些内核）？
sudo dkms status
```

若 `dkms status` 显示 RTL8812AU 驱动程序只针对*旧版*内核构建，而非当前内核，那你已找到问题所在。

---

## 第一步：诊断驱动程序状况

依序执行以下诊断步骤，每个检查都能在你开始修改前缩小问题根源。

```bash
# 确认目前内核版本
uname -r

# 确认是否存在任何无线接口
ip link show | grep -E "wlan|wlp"

# 确认驱动程序模块是否已加载
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# 确认 RTL8812AU 网卡的 DKMS 构建状态
sudo dkms status

# 扫描内核消息缓冲区中的相关错误
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**解读结果：**

| 输出 | 含义 |
|---|---|
| `ip link` 未显示无线接口 | 内核模块未加载或硬件未被枚举 |
| `lsmod` 未显示对应模块 | 模块加载失败——检查 `dmesg` 的错误信息 |
| `dkms status` 显示当前内核为 `broken` 或缺失 | DKMS 构建失败——请按 RTL8812AU 修复步骤操作 |
| `dmesg` 显示 `firmware: failed to load mt7921u` | 固件软件包缺失——请按 MT7921U 修复步骤操作 |
| `dmesg` 显示 `disagrees about version of symbol` | 模块针对错误的内核头文件构建 |

{{< alert "triangle-exclamation" >}}
若 `ip link` 显示接口存在，但使用时接口消失，请直接跳至网卡特定问题排除表格。可见但无法正常使用的接口与完全消失的接口，其原因不同。
{{< /alert >}}

---

## 修复：RTL8812AU 驱动程序（AWUS036ACH、ACM、ACS、EACS）

RTL8812AU 是 ALFA 芯片组中用于渗透测试最广泛的型号，原因在于其双频支持与可靠的监听模式。它需要内核外驱动，因此也是最常被内核更新破坏的芯片组。

### 4.1 — 安装内核头文件

在修改任何驱动程序之前，第一步是确认*当前*内核的头文件已安装：

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

若命令顺利完成，头文件现已存在，DKMS 重建可以继续。若报告找不到软件包，你的内核可能太新，目前的软件源快照尚无对应版本——请先执行 `sudo apt full-upgrade` 获取匹配的头文件，然后重新启动再继续。

### 4.2 — 通过 DKMS 重建（最快路径）

头文件就绪后，请 DKMS 为当前运行的内核重建所有已注册的模块：

```bash
sudo dkms autoinstall
```

仔细观察输出。成功的构建以 `DKMS: install completed` 结束。若成功，无需重新启动即可重新加载模块：

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

若接口出现，即完成。继续步骤 4.4 验证监听模式。

### 4.3 — 从源码完整重装（DKMS 失败时）

若 `dkms autoinstall` 报告错误，代表已注册的驱动程序源码已损坏或过旧。请完整移除后，从最新上游源码重新安装：

```bash
# 移除所有 DKMS 已注册的驱动程序版本
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# 克隆最新驱动程序源码
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 一步完成：向 DKMS 注册源码、编译并安装
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
`dkms remove` 命令中的版本号 `5.6.4.2` 是常见版本，你的版本可能不同。请先执行 `sudo dkms status` 确认输出中显示的确切版本字符串。
{{< /alert >}}

构建完成后：

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — 验证监听模式

网卡实体存在且驱动程序已加载。确认监听模式——这也是使此网卡适用于安全测试的功能——仍然正常：

```bash
sudo airmon-ng start wlan0
```

请将 `wlan0` 替换为 `ip link` 显示的实际接口名称。成功响应将显示 `monitor mode vif enabled`，并出现如 `wlan0mon` 的新接口名称。

### 4.5 — Kali 软件包方法（最简便）

Kali Linux 提供预先打包的 RTL8812AU 驱动程序 DKMS 构建，与 Kali 内核保持同步。如果你使用 Kali，请使用此方法而非从 GitHub 克隆：

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

此单一命令将安装驱动程序源码、向 DKMS 注册，并针对当前内核进行构建。后续的 `apt full-upgrade` 执行将自动保持头文件与驱动程序同步。

---

## 修复：MT7921U 驱动程序（AWUS036AXM、AXML）

MT7921U（Wi-Fi 6E）芯片组采用完全不同的路径。由于自 Linux 5.18 起即为**内核内置驱动程序**，无需 DKMS、无需编译、也无需从 GitHub 克隆。内核更新本不应破坏它——但固件打包问题有时会造成影响。

### 5.1 — 安装固件软件包

内核模块（`mt7921u.ko`）已存在，但它需要来自用户空间的固件二进制文件来初始化硬件：

```bash
sudo apt install firmware-misc-nonfree
```

在 Ubuntu 上，此软件包位于 `non-free` 软件源组件中。若命令失败，请确认 `/etc/apt/sources.list` 中已启用非自由软件源。

### 5.2 — 重新加载驱动程序

安装固件后，无需重新启动即可强制重新加载驱动程序：

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

然后检查接口：

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — 确认内核版本

MT7921U 驱动程序需要内核 **5.18 或更新版本**。若你安装的是早于此内核版本的 Kali 或 Ubuntu 最小镜像，模块根本不存在：

```bash
uname -r
# 输出必须为 5.18.x 或更高
```

若内核版本低于 5.18，请升级内核（步骤 5.4）。

### 5.4 — 升级内核

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
请使用 `full-upgrade` 而非 `upgrade`。`upgrade` 子命令会搁置需要移除其他软件包的更新——这通常意味着内核软件包本身被保留不更新。`full-upgrade` 允许进行必要的依赖关系解析。
{{< /alert >}}

### 5.5 — 重新启动后验证

重新启动进入新内核后，确认一切正常运行：

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

健康的 `dmesg` 输出将显示固件成功加载，以及 USB 设备被注册为网络接口。

---

## 让驱动程序在未来更新后保持正常

预防比修复简单。以下做法可防止内核更新再次破坏你的网卡。

**在 Kali rolling 上始终使用 `full-upgrade`：**

```bash
sudo apt update && sudo apt full-upgrade
```

`full-upgrade` 命令确保当安装新内核软件包时，匹配的 `linux-headers` 软件包在*同一次事务*中安装。DKMS 钩子在软件包安装期间触发——若头文件在内核之后才通过另一次 `apt` 执行到达，DKMS 就会错过构建。

**安装 DKMS 元软件包：**

```bash
sudo apt install dkms linux-headers-generic
```

这将 `linux-headers-generic` 作为 DKMS 软件包的依赖项引入，使头文件始终与内核保持同步更新。

**Ubuntu HWE 内核栈：**

在 Ubuntu LTS 上，硬件启用内核栈比 GA 内核接收更频繁的更新和更好的硬件支持。安装一次后，更新将自动处理：

```bash
sudo apt install linux-generic-hwe-24.04
```

**验证 DKMS 自动安装已启用：**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

若此行被注释或设为 `no`，DKMS 将不会自动重建模块。请在 `/etc/dkms/framework.conf` 中取消注释或设为 `yes`。

---

## 网卡特定问题排除表格

| 症状 | 可能芯片组 | 根本原因 | 快速修复 |
|---|---|---|---|
| 重新启动后接口消失 | RTL8812AU | DKMS 构建失败 | `sudo dkms autoinstall` |
| 接口消失，`dmesg` 显示固件错误 | MT7921AUN | 缺少固件软件包 | `sudo apt install firmware-misc-nonfree` |
| 接口出现但 30 秒后消失 | RTL8812AU | 模块版本不符 | `sudo dkms remove --all && sudo make dkms_install` |
| 监听模式失败，显示 `SIOCSIFFLAGS` | RTL8812AU | 驱动程序分支错误 | 克隆 `aircrack-ng/rtl8812au` 并重新安装 |
| `iwconfig` 显示无无线扩展功能 | 任何 | 模块未加载 | `sudo modprobe 88XXau` 或 `sudo modprobe mt7921u` |
| 接口存在但找不到任何网络 | MT7921AUN | 内核 < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status` 显示 `broken` | RTL8812AU | 源码/头文件不符 | `sudo apt install linux-headers-$(uname -r)` 后重建 |
| 发射功率限制在 20 dBm | RTL8812AU | 监管域锁定 | `sudo iw reg set US`（依你的地区调整） |

---

## 若一切都无效：全新安装方法

当多次重建尝试均失败，且 `dkms status` 显示来自多次部分安装的混乱输出时，从头开始比调试更快：

```bash
# 若已安装 Kali 软件包，请先移除
sudo apt purge realtek-rtl88xxau-dkms

# 移除所有 rtl8812au 的 DKMS 条目
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# 移除残留的源码目录（若存在）
sudo rm -rf /usr/src/rtl8812au*

# 清除任何过期的模块缓存
sudo depmod -a

# 全新克隆并安装
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
移除 DKMS 条目的循环若找不到任何版本将静默失败——这是正常的。重要步骤是 `sudo rm -rf /usr/src/rtl8812au*`，它能移除任何可能处于损坏状态的源码树。
{{< /alert >}}

---

## 预防清单

在每次系统更新前使用此清单，避免在执行任务时出现意外：

**在 `apt upgrade` 之前：**

```bash
# 确认哪些内核软件包正在等待更新
apt list --upgradable 2>/dev/null | grep linux-image
```

若有新内核即将到来，请在任何生产工作前安排测试重新启动。

**每次升级并重新启动后：**

```bash
# 确认网卡已恢复
ip link show | grep -E "wlan|wlp"

# 确认监听模式仍然正常
sudo airmon-ng check
```

**保留备用方案：**
- 准备一个装有 Kali Live 镜像的 USB 闪存盘（或备用网卡使用已知正常运行的驱动程序）。在预约好的测试期间发生连接问题代价高昂——一个实体备用方案只需几分钟即可准备好，关键时刻能救你一命。

**在 Kali 上锁定关键驱动程序软件包：**

```bash
# 防止特定驱动程序软件包在升级期间被自动移除
sudo apt-mark hold realtek-rtl88xxau-dkms
```

在明确升级驱动程序之前，先解除锁定：

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

## 总结

ALFA 驱动程序在内核更新后的失效问题遵循可预测的模式，也有可预测的解决方案。RTL8812AU 网卡需要 `dkms autoinstall`（或从 `aircrack-ng/rtl8812au` 全新克隆）加上匹配的内核头文件。MT7921U 网卡需要 `firmware-misc-nonfree` 以及 5.18 或更新的内核。两种情况的长期修复方案，都是确保以 `apt full-upgrade` 而非 `apt upgrade` 作为标准更新命令，让头文件与内核保持同步。

---

**相关指南：**
- [如何在 Kali Linux 与 Ubuntu 上安装 ALFA USB WiFi 驱动程序](/zh-cn/blog/install-alfa-driver-kali-ubuntu/) — 若你从未安装过驱动程序，请从这里开始
- [AWUS036ACH Kali Linux 设置指南](/zh-cn/blog/awus036ach-kali-linux-setup/) — 完整设置说明，包含监听模式与数据包注入验证
