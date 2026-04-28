---
title: "ALFA AWUS036AXM 驱动程序 (driver) 安装指南（中国区）：Kali Linux, Ubuntu, Debian 和树莓派"
description: "专为国内用户准备的 ALFA AWUS036AXM 驱动程序 (driver) 分步安装教程。使用国内镜像源，涵盖 MT7921AUN WiFi 6E 内核驱动程序 (driver)，支持监听模式 (monitor mode) 和 VIF。适用于 Kali Linux, Ubuntu, Debian 以及树莓派。无需访问 GitHub。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["驱动程序指南"]
series: ["Alfa 中国安装指南"]
related_product: "/zh-cn/products/alfa/awus036axm/"
---

AWUS036AXM 是 ALFA 的 WiFi 6E 三频适配器，配有节省空间的 L 型 USB-A 接口。它的 MT7921AUN 芯片使用 `mt7921u` 驱动程序 (driver)，自 5.18 版本起已内置于 Linux 内核中。L 型接口可以让笔记本电脑上相邻的 USB 端口保持空闲。本指南将带你完成完整安装——包括固件 (firmware)、驱动程序 (driver) 验证、监听模式 (monitor mode)、数据包注入 (packet injection) 和 VIF——全程无需访问 GitHub。

## 开始之前

请确保你已准备好：

1. **ALFA AWUS036AXM** 适配器
2. 有源 USB 集线器（Hub）——如果你使用的是树莓派，这是必须的
3. 能够连接国内镜像源的互联网连接

插入适配器，然后确认系统识别到了它：

```bash
lsusb
```

在输出中寻找这一行：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

如果你看到了 `0e8d:7961`，说明系统已检测到适配器。请移步下方对应的操作系统部分。

如果没看到，请尝试换一个 USB-A 端口，然后再次运行 `lsusb`。

## 选择你的操作系统

点击跳转到适合你系统的部分：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 (Raspberry Pi) 4B / 5](#raspberry-pi-4b--5)

已经安装好了？直接跳转到：

- [开启监听模式 (monitor mode)](#enable-monitor-mode)
- [测试数据包注入 (packet injection)](#test-packet-injection)
- [虚拟接口 (VIF)](#virtual-interface-vif)
- [虚拟机 USB 透传](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7921AUN 的驱动程序 (driver) 已经包含在 Kali 内核中了。你只需要从国内镜像源安装 MediaTek 的固件 (firmware) 包即可。

### 第一步：切换到国内镜像源

在终端中打开软件源列表。

```bash
sudo nano /etc/apt/sources.list
```

删除其中的所有内容，然后粘贴下面这一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：按 **Ctrl+O**，然后回车，最后按 **Ctrl+X** 退出。刷新软件包索引。

```bash
sudo apt update
```

> **备用镜像：** 如果中科大 (USTC) 速度较慢，可以改用清华大学镜像：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安装固件 (firmware)

MT7921AUN 需要来自 `firmware-misc-nonfree` 和 `linux-firmware` 的固件 (firmware) 文件。如果没有这些文件，驱动程序 (driver) 虽然能加载，但适配器将无法初始化。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 第三步：验证驱动程序 (driver)

重启后，插入适配器并进行检查。

```bash
lsmod | grep mt7921
```

你应该在输出中看到 `mt7921u`。然后确认是否出现了无线接口。

```bash
iwconfig
```

寻找 `wlan0` 或 `wlan1`。如果出现了，说明驱动程序 (driver) 工作正常。

---

### 第四步：开启监听模式 (monitor mode) {#enable-monitor-mode}

先检查接口名称。

```bash
iwconfig
```

使用你看到的名称（例如 `wlan1`）。杀掉干扰进程，然后切换到监听模式 (monitor mode)。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

确认切换成功。

```bash
iwconfig
```

在对应的接口上寻找 `Mode:Monitor` 字样。

---

### 第五步：测试数据包注入 (packet injection) {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

成功的结果如下：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

如果失败了，请重启系统再试一次。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 内核 6.8，即插即用

Ubuntu 24.04 搭载了 6.8 内核，原生支持 MT7921AUN 驱动程序 (driver)。

### 第一步：切换到国内镜像源

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

删除所有内容并粘贴：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

```bash
sudo apt update
```

### 第二步：安装固件 (firmware)

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### 第三步：验证并开启监听模式 (monitor mode)

重启后，运行 `lsmod | grep mt7921` 确认驱动程序 (driver) 已加载，然后按照上方 Kali 的步骤（第四步）操作。

---

### Ubuntu 22.04 (Jammy) — 需要 HWE 内核

Ubuntu 22.04 默认搭载的是 5.15 内核。MT7921AUN 的驱动程序 (driver) 需要 5.18 或更高版本的内核。请先安装 HWE 内核。

### 第一步：切换到国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

将所有行替换为：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

保存并退出（`Ctrl+O`，然后 `Ctrl+X`）。

```bash
sudo apt update
```

### 第二步：安装 HWE 内核

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

重启后，确认内核版本：

```bash
uname -r
```

你应该能看到 5.19 或更高版本。接着按照上文安装固件 (firmware) 并开启监听模式 (monitor mode)。

### 第三步：安装固件 (firmware)

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### 第一步：切换到国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

删除所有内容并粘贴（针对 Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

```bash
sudo apt update
```

### 第二步：安装固件 (firmware)

Debian 12 Bookworm 搭载的是 6.1 内核——完美兼容 MT7921AUN。

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### 第三步：验证并开启监听模式 (monitor mode)

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 第四步：测试数据包注入 (packet injection)

```bash
sudo aireplay-ng --test wlan1
```

看到 `Injection is working!` 就说明你的适配器已经完全准备就绪了。

---

## 树莓派 (Raspberry Pi) 4B / 5

> AWUS036AXM 在负载下功耗可达 2.7W。在树莓派上使用时，请务必连接有源 USB 集线器。

### 第一步：下载 Kali Linux ARM64 镜像

官方页面：https://www.kali.org/get-kali/#kali-arm

选择 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)** —— 必须使用 64 位版本。

> **国内镜像：** https://repo.huaweicloud.com/kali-images/ —— 浏览到最新版本文件夹并下载 ARM64 镜像。

### 第二步：烧录到 MicroSD 卡

```bash
lsblk
# 将 /dev/sdX 替换为你实际的 SD 卡盘符
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

默认账号密码：**kali / kali**。

### 第三步：切换国内镜像源并安装固件 (firmware)

```bash
sudo nano /etc/apt/sources.list
```

替换为：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

然后运行：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### 第四步：验证驱动程序 (driver)

```bash
lsmod | grep mt7921
```

应该会出现 `mt7921u`。

### 第五步：开启监听模式 (monitor mode)

在带有内置 Wi-Fi 的树莓派上，AWUS036AXM 通常显示为 `wlan1`。

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 第六步：测试数据包注入 (packet injection)

```bash
sudo aireplay-ng --test wlan1
```

---

## 虚拟机 USB 透传 {#virtual-machine-usb-passthrough}

### VirtualBox

1. 关闭虚拟机。进入 **设置 → USB**。
2. 启用 **USB 3.0 (xHCI) 控制器**。
3. 点击 **+** 图标添加 USB 筛选器。
4. 选择：**MediaTek Inc.** (ID: 0e8d:7961)。
5. 启动虚拟机 —— 适配器就会出现在 Kali 中。

在虚拟机中运行 `lsusb` 确认看到 `0e8d:7961`，然后按照上文 Kali 的步骤操作。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. 启动虚拟机。
2. 菜单：**虚拟机 → USB 和蓝牙**。
3. 找到 **MediaTek MT7921AUN** 并点击 **连接**。
4. 在虚拟机中运行 `lsusb` 确认，然后按照上文 Kali 的步骤操作。

---

## 虚拟接口 (VIF) {#virtual-interface-vif}

MT7921AUN 具有完美的内核原生 VIF 支持。你可以在同一个适配器上同时运行监听接口和普通接口——无需任何补丁。

### 在普通模式旁创建一个监听接口

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

你应该能看到 `wlan0`（普通模式）和 `mon0`（监听模式）同时处于活动状态。

### 在保持连接的同时进行监听

```bash
sudo airodump-ng mon0
```

`wlan0` 保持连接，而 `mon0` 负责抓取范围内的所有数据。

### Fake AP + 监听

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> **关于 hostapd 的提示：** 完整的 AP 运行需要配置 `hostapd`。上述步骤仅确认适配器可以创建该接口——具体的 AP 配置是一个独立的话题。

---

## 常见问题排查

| 现象 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| `lsusb` 不显示 0e8d:7961 | 适配器未通电或线缆不良 | 尝试换一个 USB-A 端口。在树莓派上请使用有源集线器。 |
| `lsmod` 不显示 mt7921u | 未安装固件 (firmware) 或内核版本过低 | 运行 `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` |
| Ubuntu 22.04 无法加载驱动程序 (driver) | 5.15 内核太旧了 | 安装 HWE：`sudo apt install linux-generic-hwe-22.04` |
| 接口出现了但无法连接 | 缺少固件 (firmware) 文件 | 运行 `sudo apt install firmware-misc-nonfree` 然后重启 |
| 切换监听模式 (monitor mode) 失败 | 接口仍处于开启状态 | 在执行 `iw dev` 命令前先运行 `sudo ip link set wlan1 down` |
| 注入测试显示 "No Answer" | AP 太远或接口选错 | 靠近一些。使用 `iwconfig` 确认 `Mode:Monitor`。 |
| 创建 VIF 接口失败 | 驱动程序 (driver) 未完全加载 | 拔掉适配器，然后运行：`sudo rmmod mt7921u && sudo modprobe mt7921u` |

## 中国区镜像源参考

| 资源 | 网址 | 用途 |
|----------|-----|---------|
| Alfa 官方驱动程序 (driver) | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动包、固件 (firmware) |
| Alfa 文档中心 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 产品手册 |
| 清华大学镜像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像站 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (推荐) |
| 中科大镜像站 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (推荐) |
| 华为云镜像站 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 镜像 (备用) |

## 更多针对中国区的 Alfa 适配器指南

这是 **Alfa 中国安装指南** 系列文章的一部分：

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU, 高功率
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U, 完整 VIF 支持
- [AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/) — RTL8811AU, 监听模式 (monitor mode)
- [AWUS036AX 中国安装指南](/zh-cn/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中国安装指南](/zh-cn/blog/awus036axer-china-install-guide/) — RTL8832BU, 迷你型
- AWUS036AXM ← 你在这里
- [AWUS036AXML 中国安装指南](/zh-cn/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国安装指南](/zh-cn/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows 版

有问题？欢迎在下方留言，或通过 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
