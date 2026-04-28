---
title: "ALFA AWUS036AXER 中国安装全攻略：Kali Linux / Ubuntu / Debian / 树莓派"
description: "手把手教你在中国网络环境下安装 ALFA AWUS036AXER 驱动，全程使用国内镜像，无需翻墙。覆盖 Kali Linux、Ubuntu 22/24、Debian 和树莓派。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "驱动", "中国", "wifi6", "rtl8832bu"]
categories: ["驱动安装指南"]
series: ["Alfa 中国安装全攻略"]
related_product: "/zh-cn/products/alfa/awus036axer/"
---

刚拿到 AWUS036AXER，插上去 Linux 没反应？正常。这块网卡用的是 RTL8832BU 芯片，在内核版本 6.14 以下驱动不是开箱即用的。好在 Ubuntu 24.04（内核 6.8）已经原生集成了，其他系统我们用 Gitee 镜像也能 10 分钟搞定。

> **安全研究注意：** RTL8832BU 的监听模式支持比较有限。如果你追求极致的数据包注入稳定性，建议选择 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/) 或 [AWUS036ACH](/zh-cn/blog/awus036ach-china-install-guide/)。

> **信号注意：** AXER 是迷你型网卡，天线是内置的。虽然方便携带，但如果你需要远距离抓包，带外置大天线的型号会更猛。

## 开始之前

1. **ALFA AWUS036AXER** 网卡
2. USB 数据线
3. 能访问国内镜像的网络

插好网卡，确认系统认到了：

```bash
lsusb
```

找这一行：

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## 选择你的系统

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### 第一步：切换国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

粘贴这一行：

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

### 第三步：从 Gitee 下载驱动

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **提示：** 如果 Gitee 这个地址打不开，搜 `rtl8852bu` 找个最近有更新的就行。

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

### 第五步：开启监听模式 {#enable-monitor-mode}

> **注意：** 这块网卡的监听模式比较挑系统，不一定百分百成功。

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

如果注入不稳定，还是那句话：换 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/)。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 内核自带，直接用

24.04 的内核比较新，通常插上就能用。先换个阿里云镜像：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

看到接口就搞定了！

---

### Ubuntu 22.04 (Jammy) — 需要手动装

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

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
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
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

## Raspberry Pi 4B / 5

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

## 虚拟机 USB 直通 {#virtual-machine-usb-passthrough}

### VirtualBox

1. **设置 → USB** → 启用 **USB 3.0 (xHCI)**。
2. 添加过滤器：**Realtek** (ID: 0bda:885a)。
3. 启动虚拟机，按 Kali 步骤操作。

### VMware

1. **虚拟机 → USB 与蓝牙** → 找到 **Realtek RTL8832BU** → **连接**。
2. 确认 `lsusb` 能看到后，按 Kali 步骤操作。

---

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| `lsusb` 没反应 | 没插好或供电不足 | 换个口试试 |
| `install-driver.sh` 报错 | 缺少头文件 | `sudo apt install linux-headers-$(uname -r)` |
| Gitee 下载太慢 | 网络波动 | 换个镜像仓库试试 |
| 监听模式不行 | 硬件限制 | 正常，这块网卡主打的是 WiFi 6 高速上网 |

## 国内镜像速查

| 资源 | 地址 | 用途 |
|------|------|------|
| Alfa 官方驱动 | [files.alfa.com.tw](https://files.alfa.com.tw) | 原始包 |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | 驱动源码 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 安装指南](/zh-cn/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安装指南](/zh-cn/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安装指南](/zh-cn/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安装指南](/zh-cn/blog/awus036ax-china-install-guide/)
- AWUS036AXER ← 你在这里
- [AWUS036AXM 安装指南](/zh-cn/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安装指南](/zh-cn/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安装指南](/zh-cn/blog/awus036eacs-china-install-guide/)

有问题？在下面留言，或者来 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
