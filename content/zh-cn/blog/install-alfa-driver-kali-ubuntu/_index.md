---
title: "如何在 Kali Linux 与 Ubuntu 24.04 安装 ALFA USB WiFi 驱动程序（2026）"
description: "完整教程：在 Kali Linux 2024 和 Ubuntu 24.04 安装 ALFA Network USB WiFi 网卡驱动，覆盖 RTL8812AU、MT7612U 和 MT7921AUN 芯片组，附故障排除技巧。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["驱动安装", "Kali-Linux", "Ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
---

让 USB WiFi 网卡在 Linux 上正常工作，归根结底取决于一件事：驱动程序。与 Windows 上厂商提供可执行安装包的方式不同，Linux 使用内核模块——编译后由操作系统加载、用于与硬件通信的代码文件。理解这一机制，驱动排障就会变得简单明了，安装过程也将有迹可循。

本指南涵盖 Kali Linux 2024/2025 和 Ubuntu 24.04 LTS 上所有主流 ALFA Network USB WiFi 网卡芯片组的驱动安装方法。

---

## Linux USB WiFi 驱动的工作原理

### 内核模块

Linux WiFi 驱动是一个**内核模块**——一个在启动时或按需加载到运行内核中的 `.ko` 文件。插入 USB 设备时，内核读取其 USB 厂商 ID 和产品 ID，在数据库中查找对应模块，然后自动加载。

对于 MediaTek MT7612U 等常见芯片组，这一过程完全透明：插入网卡，模块自动加载，无线接口随即出现。而对于较新或较少见的芯片组，内核树中没有对应模块，你就必须从源码编译。

### 树外驱动（Out-of-Tree Driver）

当驱动程序未包含在内核主线中（称为"树外"或"外部"驱动）时，你需要：

1. 下载驱动源码
2. 针对运行中内核的头文件进行编译
3. 将生成的 `.ko` 文件安装到内核模块目录
4. 用 `modprobe` 加载它

编译步骤要求内核头文件已安装，且与运行中的内核版本完全匹配。这是驱动安装失败最常见的原因。

### DKMS：动态内核模块支持

普通的 `make install` 仅针对当前内核编译驱动。当 Kali 或 Ubuntu 更新内核——这种情况经常发生——旧驱动将无法加载，必须手动重新编译。

**DKMS** 通过将驱动源码注册到系统守护进程来解决这个问题，每当安装新内核时，系统会自动为所有已注册的模块重新编译。对于任何需要树外驱动的网卡，这是推荐的安装方式。

---

## 确认你的芯片组

所需驱动程序完全取决于芯片组，而非网卡的商品名称。同一款网卡的不同硬件版本可能使用不同的芯片组。

### ALFA 型号与芯片组对应表

| ALFA 型号 | 芯片组 | USB ID | 驱动程序 |
|---|---|---|---|
| [AWUS036ACH](/zh-cn/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACM](/zh-cn/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u（内核内置） |
| [AWUS036AX](/zh-cn/products/alfa/awus036ax/) | RTL8832BU | 0e8d:885a | OOK driver (<6.14) |
| [AWUS036AXML](/zh-cn/products/alfa/awus036axml/) | MT7921AUN | 0e8d:7961 | mt7921u（内核 5.18+） |

### 用 lsusb 确认网卡型号

插入网卡后运行：

```bash
lsusb
```

示例输出：

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
```

将 `ID xx:xx` 的值与上表对照，确认你的芯片组型号。

---

## 准备系统环境

无论使用哪款芯片组，都请先安装通用编译依赖：

**Kali Linux：**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04：**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

确认已为当前运行的内核安装了头文件：

```bash
uname -r
# 示例：6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# 该目录应存在；若不存在，说明头文件未安装
```

---

## RTL8812AU 驱动（AWUS036ACH）

RTL8812AU 需要树外驱动程序。社区维护了两个分支，根据操作系统选择合适的版本。

### 选项 A：aircrack-ng/rtl8812au（Kali Linux 推荐）

此分支由 Aircrack-ng 团队维护，针对 Kali 做了专门的兼容性优化，数据包注入支持也经过专项加强：

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

验证接口是否出现：

```bash
ip link show | grep wlan
# 应显示 wlan0 或类似接口名
```

### 选项 B：morrownr/8812au-20210708（Ubuntu 24.04 推荐）

morrownr 分支针对 Ubuntu 做了优化，并提供集成了 DKMS 的便捷安装脚本：

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

安装脚本会自动处理 DKMS 注册。安装完成后：

```bash
# 重启以加载新模块
sudo reboot

# 重启后验证
lsmod | grep 8812au
```

### 手动 DKMS 注册（两个分支均适用）

如果你希望手动控制整个过程：

```bash
# 克隆驱动（使用任意一个分支）
git clone https://github.com/aircrack-ng/rtl8812au

# 从 Makefile 获取版本号
grep "^MODULE_VERSION" rtl8812au/Makefile
# 记录版本号，例如 v5.6.4.2 → 使用 5.6.4.2

# 将源码复制到 DKMS 目录
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# 注册、编译、安装
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# 验证
dkms status
# 预期：rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### 成功安装后的预期输出

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## MT7612U 驱动（AWUS036ACM、AWUS036ACX）

MT7612U 芯片组是四款中最容易上手的，因为它的驱动程序自 Linux **内核 4.19 版本**起已进入主线。在 Kali Linux 2022+ 和 Ubuntu 20.04+ 上，完全不需要安装任何驱动程序。

### 检查内核版本

```bash
uname -r
```

任何现代 Kali 或 Ubuntu 系统的输出都会在 4.19 以上，`mt76x2u` 模块均可用。

### 加载模块

```bash
sudo modprobe mt76x2u
```

验证加载结果：

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

无线接口应立即出现：

```bash
ip link show
# wlan0: ...
```

### 设置开机自动加载模块

大多数系统会在检测到网卡时自动加载模块。若要显式确保开机加载：

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### 无需编译

这是 MT7612U 芯片组的核心优势：无需编译、无需驱动源码、无需依赖内核头文件。在所有支持的发行版上开箱即用。对于不想折腾驱动管理的用户，[AWUS036ACM](/zh-cn/products/alfa/awus036acm/) 是现有渗透测试网卡中即插即用体验最好的一款。

---

## MT7921AUN 驱动（AWUS036AXM、AWUS036AXML — Wi-Fi 6E）

MT7921AUN 是 MediaTek 的 Wi-Fi 6E 芯片组，其 Linux 驱动 `mt7921u` 已于 **内核 5.18 版本**合并入主线。

### 检查内核版本

```bash
uname -r
```

**Kali Linux 2022.2 及以后版本**搭载内核 5.18 或更新——已支持。
**Ubuntu 22.04 LTS** 搭载内核 5.15——**不支持**，需升级内核。
**Ubuntu 24.04 LTS** 搭载内核 6.8——完全支持。

### 加载模块（内核 5.18+）

```bash
sudo modprobe mt7921u
```

验证：

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04：内核升级路径

若你使用的是搭载内核 5.15 的 Ubuntu 22.04，有两种解决方案：

**方案 A：HWE 内核**（推荐）

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

Ubuntu 22.04 的 HWE（硬件使能）内核版本为 6.2+，支持 mt7921u。

**方案 B：升级到 Ubuntu 24.04**

Ubuntu 24.04 LTS 搭载内核 6.8，完全支持 mt7921u，是更干净的长期解决方案。

### Wi-Fi 6E 与监听模式现状

截至 2026 年，mt7921u 驱动在 2.4 GHz、5 GHz 和 6 GHz 三个频段上均可稳定连接网络（管理模式）。2.4 GHz 和 5 GHz 的监听模式功能正常。**6 GHz 监听模式**仍在持续完善中——在将其用于 6 GHz 评估之前，请先查阅 `mt76` 内核驱动的 issue 追踪器确认最新状态。

---

---

## DKMS：确保驱动在内核更新后持续可用

Kali Linux 和 Ubuntu 都会定期更新内核。没有 DKMS 的情况下，树外驱动（RTL8812AU）在内核更新后将停止工作，直到手动重新编译。

正确配置 DKMS 后，重新编译会在 `apt upgrade` 期间自动发生。

### 验证 DKMS 是否正在管理你的驱动

```bash
dkms status
```

正常管理的驱动示例输出：

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### 内核更新时的自动处理流程

```
apt upgrade
→ 下载新内核包
→ 触发 DKMS 钩子
→ 为新内核重新编译 rtl8812au 源码
→ 安装新的 .ko 文件
→ 系统重启进入新内核
→ 驱动自动加载
```

若 DKMS 在升级过程中失败（通过 `dkms status` 看到显示 "built" 但未 "installed"），手动重新安装：

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## 故障排除

| 症状 | 可能原因 | 解决方案 |
|---|---|---|
| 插入后无 wlan 接口 | 驱动未加载 | `sudo modprobe 88XXau` 或 `sudo modprobe mt76x2u` |
| `modprobe: FATAL: Module not found` | 驱动未为当前内核编译 | 重新编译驱动或运行 `sudo dkms install` |
| 接口出现后几秒消失 | 电源管理干扰 | `sudo iwconfig wlan0 power off` |
| `make` 报错 "linux/module.h not found" | 内核头文件未安装 | `sudo apt install linux-headers-$(uname -r)` |
| `make` 报版本不匹配 | 头文件与运行内核不符 | 对比 `uname -r` 与 `ls /lib/modules`，重新安装匹配版本的头文件 |
| lsusb 可见但无接口 | 模块已加载但未创建接口 | 检查 `dmesg \| tail -30` 查看错误信息 |
| 监听模式失败："Operation not supported" | 驱动版本不支持监听模式 | 使用 aircrack-ng 分支而非发行版自带驱动 |
| aireplay-ng 注入测试：0% | 接口未处于监听模式 | 用 `iwconfig` 确认，重新运行 `airmon-ng start` |
| 驱动工作正常但重启后失效 | 模块未添加到 initramfs | `sudo update-initramfs -u` 或使用 DKMS |
| 内核更新后 DKMS 编译失败 | 新内核缺少头文件 | `sudo apt install linux-headers-$(uname -r)` |

### 详细诊断命令

```bash
# 检查所有已加载的无线模块
lsmod | grep -E "8812|8814|mt76|mt79"

# 查看 USB 和无线相关的内核消息
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# 列出所有无线接口
iw dev

# 查看指定接口使用的驱动程序
ethtool -i wlan0 | grep driver

# 查看 USB 设备详情
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# 验证所有已注册模块的 DKMS 状态
dkms status
```

---

## 快速参考：各网卡对应驱动一览

| 你的网卡 | 芯片组 | Kali Linux | Ubuntu 24.04 |
|---|---|---|---|
| [AWUS036ACH](/zh-cn/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` | `morrownr/8812au-20210708` |
| [AWUS036ACM](/zh-cn/products/alfa/awus036acm/) | MT7612U | 内置（`mt76x2u`） | 内置（`mt76x2u`） |
| [AWUS036AX](/zh-cn/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) |
| [AWUS036AXML](/zh-cn/products/alfa/awus036axml/) | MT7921AUN | 内置（`mt7921u`，内核 5.18+） | 内置（`mt7921u`，内核 6.8） |

---

## 确保购买到正品硬件

驱动问题有时源于仿冒网卡——它们可能伪报 USB ID，或使用与标称型号不符的劣质芯片组。而从授权经销商购买的正品 ALFA Network 网卡，其行为与官方文档完全一致，不会出现意外。

Yopitek 是 ALFA Network 授权经销商。浏览完整的 [ALFA Network 产品系列](/zh-cn/products/alfa/)，确保购买到享有厂商保修且驱动兼容性有保障的正品硬件。

---

## 总结

Linux WiFi 驱动安装遵循简单的决策树：

1. **用 `lsusb` 和上方对照表确认你的芯片组**
2. **MT7612U 或 MT7921AUN（内核 5.18+）？** → 直接运行 `modprobe`，完成
3. **RTL8812AU?？** → 克隆对应仓库，运行 `make && sudo make install`，启用 DKMS 实现持久化
4. **出现问题？** → 查阅故障排除表，确认头文件与内核版本匹配，检查 `dmesg`

ALFA Network 网卡的一大优势在于：所有四款主流芯片组都有文档完善、持续维护的驱动方案，你永远不会陷入无解的境地。
