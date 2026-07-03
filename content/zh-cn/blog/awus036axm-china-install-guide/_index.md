---



title: "ALFA AWUS036AXM 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
description: "专为国内用户准备的 ALFA AWUS036AXM 安装教程。使用国内镜像源，涵盖 MT7921AUN WiFi 6E 驱动配置，支持监听模式和 VIF。适用于 Kali Linux, Ubuntu, Debian 以及树莓派。无需访问 GitHub。"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "驱动", "中国", "监听模式", "wifi6e", "vif"]
categories: ["驱动指南"]
series: ["alfa-china-install-guide"]
related_product: "/zh-cn/products/alfa/awus036axm/"
series_order: 6
featureimage: "/images/blog/awus036axm-china-install-guide.webp"
faq:
  - question: "AWUS036AXM 用什么芯片？支持 WiFi 6E 吗？"
    answer: "采用 MediaTek MT7921AUN 芯片，支持 WiFi 6E 三频段（2.4G/5G/6G Hz）。"
  - question: "AWUS036AXM 的驱动需要手动安装吗？"
    answer: "不需要，mt7921u 驱动自 Linux 核心 5.18 起已内置，仅需安装固件软件包。"
  - question: "AWUS036AXM 支持 VIF 虚拟接口吗？"
    answer: "支持，MT7921AUN 完整支持核心原生 VIF，可同时连网与监听数据包。"
  - question: "Ubuntu 22.04 安装 AWUS036AXM 为什么驱动加载失败？"
    answer: "Ubuntu 22.04 默认核心 5.15 太旧，需安装 HWE 核心升级至 5.18 以上。"
  - question: "AWUS036AXM 的 USB ID 是多少？"
    answer: "MediaTek MT7921AUN 的 USB ID 为 0e8d:7961，用 lsusb 可确认。"
---




想要体验 WiFi 6E 的极速？AWUS036AXM 是个非常硬核的选择，而且它那个节省空间的 L 型接口设计真的很贴心，不会挡住笔记本相邻的 USB 口。

{{< tldr >}}
AWUS036AXM 采用 MT7921AUN 芯片支持 WiFi 6E，驱动核心内置，安装固件软件包后即可使用监听模式、数据包注入与 VIF 功能。
{{< /tldr >}}


它的 MT7921AUN 芯片其实已经内置在 5.18 以上版本的 Linux 内核里了，但国内的小伙伴在实际使用中往往会卡在“固件下载”这一步。本指南将带你避开所有网络坑，全程使用国内镜像源，手把手教你搞定监听模式、数据包注入和好用的 VIF 功能。

## 动手前的准备

在开始折腾之前，请确保你手边有：

1. **ALFA AWUS036AXM** 网卡本人
2. **有源 USB 集线器（Hub）**——如果你用的是树莓派，这一步非常关键，因为这网卡功耗有点大
3. 畅通的网络（用来下载镜像源）

插上网卡，咱们先看看系统认出它没。打开终端输入：

```bash
lsusb
```

扫一眼输出，寻找这一行：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

看到 `0e8d:7961` 就稳了。接着根据你的系统选教程。

## 你的系统是哪一个？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

如果是老手，可以直接跳转到：
- [开启监听模式](#enable-monitor-mode)
- [测试数据包注入](#test-packet-injection)
- [虚拟接口 (VIF) 高级玩法](#virtual-interface-vif)
- [虚拟机 USB 透传避坑指南](#virtual-machine-usb-passthrough)

---

## Kali Linux

好消息是，MT7921AUN 的驱动已经内置在 Kali 核心里了。咱们只需要把 MediaTek 的固件包装上，它就能动起来。

### 1. 先换个“快车道”（切换国内镜像）

为了下载嗖嗖快，咱们先换成中科大的镜像源。

```bash
sudo nano /etc/apt/sources.list
```

把内容换成这个：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，**Enter** 确认，再按 **Ctrl+X** 退出。然后跑一下更新：

```bash
sudo apt update
```

---

### 2. 把固件装齐

这一步非常关键，没有这些固件，驱动虽然加载了，网卡也是动不了的。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 3. 检查成果

重启回来，咱们看看驱动有没有乖乖工作：

```bash
lsmod | grep mt7921
iwconfig
```

看到 `mt7921u` 模块和 `wlan0` 或 `wlan1` 接口就算大功告成了。

---

### 4. 开启监听模式 {#enable-monitor-mode}

这是安全研究最关键的一步。

```bash
# 杀掉干扰进程
sudo airmon-ng check kill
# 切换模式
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

再用 `iwconfig` 确认下，看到 `Mode:Monitor` 了吗？

---

### 5. 测试数据包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

如果看到 `Injection is working!`，恭喜你，你的 AXM 已经完全解锁了。

---

## Ubuntu 22.04 / 24.04

### 如果你是 Ubuntu 24.04 (Noble) — 躺赢模式

Ubuntu 24.04 内核已经原生支持。换个阿里云源，装个固件就完事：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 换成阿里云：URIs: http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

### 如果你是 Ubuntu 22.04 (Jammy) — 需要升下内核

Ubuntu 22.04 默认的 5.15 内核太老了，带不动这款网卡，咱们得升到 HWE 内核。

```bash
# 换成阿里云
sudo nano /etc/apt/sources.list
# deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse

sudo apt update
sudo apt install -y linux-generic-hwe-22.04 linux-firmware
sudo reboot
```

重启后跑 `uname -r`，看到内核版本大于 5.18 就可以按前面的步骤玩了。

---

## Debian

### 1. 换成清华镜像

```bash
sudo nano /etc/apt/sources.list
# 换成清华：deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware

sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

之后的操作和 Kali 是一样一样的。

---

## 树莓派 (Raspberry Pi) 4B / 5

> **特别提醒：** AXM 在高负载下功耗不小，树莓派用户请务必配合 **有源 USB Hub** 使用。

建议直接用 Kali ARM64 镜像（选 64 位版本）。
国内镜像下载：[华为云 Kali 镜像](https://repo.huaweicloud.com/kali-images/)。

```bash
# 换源并装固件
sudo nano /etc/apt/sources.list
# 换成中科大：deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware

sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

## 虚拟机 USB 透传避坑指南 {#virtual-machine-usb-passthrough}

### VirtualBox
1. 关掉虚拟机，进 **设置 -> USB**。
2. 选 **USB 3.0 (xHCI) 控制器**。
3. 点 **+** 图标，选 **MediaTek Inc. (ID: 0e8d:7961)**。

### VMware
1. 在顶部菜单选 **虚拟机 -> USB 与蓝牙**。
2. 找到 **MediaTek MT7921AUN**，点 **连接**。

---

## 虚拟接口 (VIF) 高级玩法 {#virtual-interface-vif}

AXM 的 MT7921AUN 芯片对 VIF 支持得极其完美。你可以一边连着 WiFi 上网，一边开着监听接口抓包，互不干扰！

### 1. 在连网的同时开启监听

```bash
# 创建一个新的虚拟接口 mon0
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
# 现在你就可以用 mon0 抓包了，而 wlan0 还能继续上网
sudo airodump-ng mon0
```

### 2. Fake AP + 监听（同时开三个接口都没问题）

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 常见问题“救火”站

| 遇到的麻烦 | 可能的原因 | 怎么解决 |
|---------|-------------|-----|
| `lsusb` 刷不出网卡 | 没插紧或供电不足 | 换个口，树莓派务必加有源 Hub |
| `lsmod` 看不到 mt7921u | 固件没装或内核太老 | 跑一遍固件安装命令，Ubuntu 22.04 记得升 HWE 内核 |
| 注入测试是 "No Answer" | AP 太远或接口选错 | 凑近点，确认用的是正确的接口名 |
| 无法创建 VIF 接口 | 驱动没加载好 | 试试重启，或者手动 `modprobe mt7921u` |

## 国内常用资源汇总

| 资源名称 | 地址 | 说明 |
|----------|-----|---------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 官方离线驱动/固件 |
| 中科大镜像站 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 推荐 |
| 阿里云镜像站 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推荐 |


{{< faq >}}

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 中国安装指南](/zh-cn/blog/awus036acs-china-install-guide/)
- [AWUS036AX 中国安装指南](/zh-cn/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 中国安装指南](/zh-cn/blog/awus036axer-china-install-guide/)
- AWUS036AXM ← 你在这里
- [AWUS036AXML 中国安装指南](/zh-cn/blog/awus036axml-china-install-guide/)
- [AWUS036EACS 中国安装指南](/zh-cn/blog/awus036eacs-china-install-guide/)

折腾过程中遇到搞不定的，欢迎在下面评论区留言，或者去 [yupitek.com](https://yupitek.com/zh-cn/contact/) 找我们。

## 参考文献

1. [Linux Kernel mt7921 驱动](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng 官方文档](https://www.aircrack-ng.org/)
3. [ALFA Network 官网](https://www.alfa.com.tw/)
4. [Kali Linux 官方文档](https://www.kali.org/docs/)
