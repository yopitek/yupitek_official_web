---
title: "ALFA AWUS036AX 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
description: "手把手教你在中国境内使用国内镜像源安装 ALFA AWUS036AX 驱动。包含 RTL8832BU 驱动安装、WiFi 6 AX1800 性能说明。支持 Kali Linux, Ubuntu 22/24 (24.04 内置驱动), Debian 和 树莓派。无需访问 GitHub。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "驱动", "中国", "wifi6", "rtl8832bu"]
categories: ["驱动指南"]
series: ["Alfa 中国安装指南"]
related_product: "/zh-cn/products/alfa/awus036ax/"
---

AWUS036AX 是 ALFA 推出的一款 WiFi 6 AX1800 双频网卡。它采用的 RTL8832BU 芯片在 Linux 内核 6.14 以下版本中需要手动安装驱动——但好消息是，Ubuntu 24.04（内核 6.8）已经原生内置了该驱动。本指南将教你如何在旧内核系统上使用 Gitee 镜像安装驱动，以及在 Ubuntu 24.04 上如何直接启用。无需 GitHub，让我们开始吧！

> **安全研究提示：** RTL8832BU 的监听模式（monitor mode）支持有限，效果取决于内核和驱动版本。如果你需要更稳定的 Kali Linux 数据包注入，建议选择 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/) 或 [AWUS036ACH](/zh-cn/blog/awus036ach-china-install-guide/)。

## 在你开始之前

1. **ALFA AWUS036AX** 网卡
2. USB 数据线
3. 稳定的网络连接

确认系统是否识别网卡：

```bash
lsusb
```

寻找到这一行：

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## 选择你的操作系统

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### 第一步：切换到国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### 第二步：安装编译依赖

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### 第三步：从 Gitee 克隆驱动

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **注意：** 如果 Gitee 链接失效，请搜索 `rtl8852bu` 并选择最近更新的仓库。

### 第四步：编译并安装

```bash
sudo ./install-driver.sh
sudo reboot
```

验证驱动：

```bash
lsmod | grep 88x2bu
iwconfig
```

### 第五步：启用监听模式 {#enable-monitor-mode}

> **注意：** 该网卡监听模式支持有限，建议仅用于测试。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### 第六步：测试数据包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 内置驱动，无需 Gitee

Ubuntu 24.04 使用内核 6.8，已内置驱动。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

切换镜像到阿里云：
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

---

### Ubuntu 22.04 (Jammy) — 需要安装 DKMS

```bash
sudo nano /etc/apt/sources.list
```

切换到阿里云：
`deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse`

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 树莓派 4B / 5

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 虚拟机 USB 透传 {#virtual-machine-usb-passthrough}

### VirtualBox

1. **设置 → USB** → 启用 **USB 3.0 (xHCI)**。
2. 添加过滤器：**Realtek** (ID: 0bda:885a)。
3. 启动 VM → 运行 `lsusb` 确认。

### VMware

1. **虚拟机 → USB 与蓝牙** → 找到 **Realtek RTL8832BU** → **连接**。

---

## 常见问题排除

| 问题 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| `lsusb` 看不到 0bda:885a | 识别失败 | 换个接口试试 |
| `install-driver.sh` 报错 | 缺少头文件 | 安装 `linux-headers-$(uname -r)` |
| 监听模式不稳定 | 芯片限制 | 建议换 ACM 型号进行渗透测试 |

> **注意：** 该驱动不支持虚拟接口（VIF）。

## 国内资源参考

| 资源类型 | 地址 | 说明 |
|----------|-----|---------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动包 |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | 国内镜像驱动 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU, 高功率
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U, 支持 VIF
- [AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/) — RTL8811AU, 监听模式
- AWUS036AX ← 你在这里
- [AWUS036AXER 中国安装指南](/zh-cn/blog/awus036axer-china-install-guide/) — RTL8832BU, 迷你型
- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — MT7921AUN, L型接口
- [AWUS036AXML 中国安装指南](/zh-cn/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国安装指南](/zh-cn/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

有问题？欢迎在下方留言，或通过 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
