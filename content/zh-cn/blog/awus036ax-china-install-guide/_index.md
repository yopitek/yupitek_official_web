---
title: "ALFA AWUS036AX 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
description: "手把手教你在中国境内使用国内镜像源安装 ALFA AWUS036AX 驱动。包含 RTL8832BU 驱动安装、WiFi 6 AX1800 性能说明。支持 Kali Linux, Ubuntu 22/24 (24.04 内置驱动), Debian 和 树莓派。无需访问 GitHub。"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "驱动", "中国", "wifi6", "rtl8832bu"]
categories: ["驱动指南"]
series: ["alfa-china-install-guide"]
related_product: "/zh-cn/products/alfa/awus036ax/"
series_order: 4
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
faq:
  - question: "AWUS036AX 用什么芯片？支持 WiFi 6 吗？"
    answer: "采用 Realtek RTL8832BU 芯片，支持 WiFi 6 (802.11ax) 高速网络。"
  - question: "AWUS036AX 在 Ubuntu 24.04 上需要安装驱动吗？"
    answer: "不需要，Ubuntu 24.04 核心已原生支持 RTL8832BU，插上即用。"
  - question: "AWUS036AX 适合做无线安全研究吗？"
    answer: "较不适合，RTL8832BU 的监听模式支持有限，建议改用 AWUS036ACM 或 AWUS036ACH。"
  - question: "在中国安装 AWUS036AX 需要翻墙吗？"
    answer: "不需要，从 Gitee 下载 rtl8852bu 源码并用国内镜像安装编译工具即可。"
  - question: "AWUS036AX 的 USB ID 是多少？"
    answer: "Realtek RTL8832BU 的 USB ID 为 0bda:8832，用 lsusb 可确认。"
---




想要在 Linux 上体验 WiFi 6 的极速？AWUS036AX 是个不错的选择。它采用的 RTL8832BU 芯片在旧内核系统上可能需要咱们手动“调教”一下驱动。不过有个好消息：如果你用的是 Ubuntu 24.04，驱动已经内置好了，插上就能飞。

{{< tldr >}}
AWUS036AX 采用 RTL8832BU 芯片支持 WiFi 6，Ubuntu 24.04 免驱即用，Kali/Ubuntu 22.04 从 Gitee 下载 rtl8852bu 编译安装。
{{< /tldr >}}


国内的小伙伴不用担心 GitHub 连不上的问题，本指南全程使用 Gitee 镜像。咱们现在就开始一步步把它跑起来！

> **安全研究避坑指南：** 虽然 AX 速度很快，但 RTL8832BU 的监听模式支持比较有限。如果你是冲着数据包注入和 Kali Linux 深度渗透去的，我更推荐你看看 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/) 或 [AWUS036ACH](/zh-cn/blog/awus036ach-china-install-guide/)。

## 动手前的准备

1. **ALFA AWUS036AX** 网卡本人
2. 包装盒里的 USB 3.0 数据线
3. 畅通的网络（用来下载镜像源）

插上网卡，咱们先看看系统有没有认出它。打开终端输入：

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

```bash
sudo nano /etc/apt/sources.list
```

把内容换成中科大的，下载嗖嗖快：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，**Enter** 确认，再按 **Ctrl+X** 退出。然后让系统刷新一下：

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

不用翻墙，咱们直接用 Gitee 镜像。

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

重启回来，检查下网卡有没有乖乖上岗：

```bash
lsmod | grep 88x2bu
iwconfig
```

---

### 5. 开启监听模式 {#enable-monitor-mode}

> **注意：** 这一步仅供测试，因为该网卡的监听模式支持并不算完美。

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
# 将 URIs 改为 http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo modprobe 88x2bu
iwconfig
```

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

建议直接用 Kali ARM64，操作和上面的 Kali 章节差不多：

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
3. 添加过滤：**Realtek (ID: 0bda:885a)**。

### VMware
1. 在顶部菜单选 **虚拟机 -> USB 与蓝牙**。
2. 找到 **Realtek RTL8832BU**，点 **连接**。

---

## 常见问题“救火”站

| 遇到的麻烦 | 可能的原因 | 怎么解决 |
|---------|-------------|-----|
| `lsusb` 刷不出 0bda:885a | USB 接口或供电问题 | 尝试插在电脑背后的 USB 3.0 蓝色接口上 |
| `install-driver.sh` 报错 | 缺少内核头文件 | 跑 `sudo apt install linux-headers-$(uname -r)` |
| 监听模式不稳定 | 芯片本身限制 | 如果需要深度渗透，建议换成 ACM 型号 |

## 国内常用资源汇总

| 资源名称 | 地址 | 说明 |
|----------|-----|---------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动离线包 |
| rtl8852bu 驱动镜像 | [Gitee 镜像](https://gitee.com/mirrors/rtl8852bu) | 国内克隆专用 |
| 清华大学镜像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Debian/Ubuntu 推荐 |


{{< faq >}}

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU, 高功率
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U, 支持 VIF
- [AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/) — RTL8811AU, 监听模式
- AWUS036AX ← 你在这里
- [AWUS036AXER 中国安装指南](/zh-cn/blog/awus036axer-china-install-guide/) — RTL8832BU, 迷你型
- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — MT7921AUN, L型接口
- [AWUS036AXML 中国安装指南](/zh-cn/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国安装指南](/zh-cn/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

折腾过程中遇到搞不定的，欢迎在下面留言，或者去 [yupitek.com](https://yupitek.com/zh-cn/contact/) 找我们。

## 参考文献

1. [Realtek 官方网站](https://www.realtek.com/)
2. [ALFA Network 官网](https://www.alfa.com.tw/)
3. [Kali Linux 官方文档](https://www.kali.org/docs/)
4. [Gitee rtl8852bu 镜像](https://gitee.com/mirrors/rtl8852bu)
