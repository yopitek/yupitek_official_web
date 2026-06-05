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
series: ["alfa-china-install-guide"]
related_product: "/zh-cn/products/alfa/awus036axer/"
series_order: 5
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
---

刚收到这款小巧玲珑的 AWUS036AXER，插上去发现 Linux 没反应？别担心，这很正常。这块网卡用的是 RTL8832BU 芯片，在内核版本 6.14 以下驱动不是开箱即用的。好在如果你用的是 Ubuntu 24.04，系统已经内置好了，插上就能飞。

对于其他系统的用户，我也帮大家找好了国内的 Gitee 镜像。不用翻墙，咱们花个 10 分钟就能把它“调教”好。

> **安全研究避坑指南：** AXER 虽然支持 WiFi 6，但它的 RTL8832BU 芯片在监听模式上的表现比较一般。如果你是为了深度渗透和数据包注入而来的，我更建议你选择 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/) 或 [AWUS036ACH](/zh-cn/blog/awus036ach-china-install-guide/)。

> **信号小贴士：** AXER 是迷你型网卡，天线是内置的，主打的是便携。如果你需要远距离抓包或信号覆盖，带外置大天线的型号会更适合你。

## 动手前的准备

1. **ALFA AWUS036AXER** 网卡本人
2. 畅通的网络（用来下载镜像源）

插好网卡，咱们先看看系统有没有认出它。打开终端输入：

```bash
lsusb
```

扫一眼输出，寻找这一行：

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

看到 `0bda:885a` 就稳了。接着根据你的系统选教程。

## 你的系统是哪一个？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

如果是老手，可以直接跳转到：
- [开启监听模式（测试版）](#enable-monitor-mode)
- [虚拟机 USB 透传避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 1. 先换个“快车道”（切换国内镜像）

为了下载不卡顿，咱们先给系统换上中科大的镜像源。

```bash
sudo nano /etc/apt/sources.list
```

把里面的内容全删了，换成这个：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，**Enter** 确认，再按 **Ctrl+X** 退出。然后跑一下更新：

```bash
sudo apt update
```

---

### 2. 把编译工具装齐

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### 3. 从 Gitee 把驱动“搬”过来

不用翻墙，咱们直接用国内的 Gitee 镜像。

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

---

### 4. 正式安装并重启

```bash
sudo ./install-driver.sh
sudo reboot
```

重启回来，检查下驱动有没有乖乖工作：

```bash
lsmod | grep 88x2bu
iwconfig
```

---

### 5. 开启监听模式 {#enable-monitor-mode}

> **注意：** 这一步仅供测试，因为该网卡的监听模式支持并不完美。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

---

## Ubuntu 22.04 / 24.04

### 如果你是 Ubuntu 24.04 (Noble) — 躺赢模式

Ubuntu 24.04 内核已经原生支持，插上就能用。建议换个阿里云源让更新更快：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 将 URIs 换成阿里云的：http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo modprobe 88x2bu
iwconfig
```

看到接口出现就大功告成了！

---

### 如果你是 Ubuntu 22.04 (Jammy) — 需要手动装一下

```bash
# 换成阿里云
sudo nano /etc/apt/sources.list
# deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

### 1. 换成清华镜像

```bash
sudo nano /etc/apt/sources.list
# deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware

sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 树莓派 (Raspberry Pi) 4B / 5

直接用 Kali ARM64 镜像最省事：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 虚拟机 USB 透传避坑指南 {#virtual-machine-usb-passthrough}

### VirtualBox
1. 关掉虚拟机。
2. **设置 -> USB** -> 勾选 **USB 3.0 (xHCI) 控制器**。
3. 点那个 **+** 图标，选 **Realtek (ID: 0bda:885a)**。

### VMware
1. 在顶部菜单选 **虚拟机 -> USB 与蓝牙**。
2. 找到 **Realtek RTL8832BU**，点 **连接**。

---

## 常见问题“救火”站

| 遇到的麻烦 | 可能的原因 | 怎么解决 |
|------|----------|----------|
| `lsusb` 刷不出 0bda:885a | 没插紧或 USB 供电不足 | 换个口试试，直接插主板背后的口 |
| `install-driver.sh` 报错 | 缺少内核头文件 | 跑 `sudo apt install linux-headers-$(uname -r)` |
| 监听模式不稳定 | 芯片本身限制 | 正常，这块网卡主打的是 WiFi 6 便携上网 |

## 国内常用资源汇总

| 资源名称 | 地址 | 说明 |
|------|------|------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 官方驱动包 |
| rtl8852bu 驱动镜像 | [Gitee 镜像](https://gitee.com/mirrors/rtl8852bu) | 国内克隆专用 |
| 清华大学镜像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Debian/Ubuntu 推荐 |

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 安装指南](/zh-cn/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安装指南](/zh-cn/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安装指南](/zh-cn/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安装指南](/zh-cn/blog/awus036ax-china-install-guide/)
- AWUS036AXER ← 你在这里
- [AWUS036AXM 安装指南](/zh-cn/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安装指南](/zh-cn/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 安装指南](/zh-cn/blog/awus036eacs-china-install-guide/)

折腾过程中遇到搞不定的，欢迎在下面留言，或者去 [yupitek.com](https://yupitek.com/zh-cn/contact/) 找我们。
