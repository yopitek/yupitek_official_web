---
title: "ALFA AWUS036AXER 中国安装全攻略：Kali Linux / Ubuntu / Debian / 树莓派"
description: "手把手教你在中国网络环境下安装 ALFA AWUS036AXER 驱动，全程使用国内镜像，无需翻墙。覆盖 Kali Linux、Ubuntu 22/24、Debian 和树莓派。"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
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
faq:
  - question: "AWUS036AXER 用什么芯片？跟 AWUS036AX 一样吗？"
    answer: "同样采用 Realtek RTL8832BU 芯片，支持 WiFi 6，但体积更小更便携。"
  - question: "AWUS036AXER 在 Ubuntu 24.04 上需要安装驱动吗？"
    answer: "需要。RTL8832BU 不在 Ubuntu 24.04 内核中，请通过 DKMS 编译一次社区版 rtl8852bu 驱动（morrownr/rtl8852bu-20250826），之后内核更新时会自动重新编译。"
  - question: "AWUS036AXER 适合做无线安全研究吗？"
    answer: "不适合。社区版 rtl8852bu 驱动不支持 Monitor mode 和封包注入，建议改用内核内置 MediaTek 驱动的 AWUS036ACM。"
  - question: "AWUS036AXER 的 USB ID 是多少？"
    answer: "Realtek RTL8832BU 的 USB ID 为 0bda:885a，用 lsusb 可确认。"
  - question: "在中国安装 AWUS036AXER 需要翻墙吗？"
    answer: "不需要，从 Gitee 下载 rtl8852bu 源码并用国内镜像安装编译工具即可。"
---




刚收到这款小巧玲珑的 AWUS036AXER，插上去发现 Linux 没反应？别担心，这很正常。AWUS036AXER 的 RTL8832BU 芯片没有 Linux 内核内置驱动，因此在所有发行版（包括 Ubuntu 24.04）上都需要通过 DKMS 编译一次社区版 rtl8852bu 驱动。本指南使用 Gitee 镜像，无需访问 GitHub。该驱动不支持 Monitor mode。

{{< tldr >}}
AWUS036AXER 采用 RTL8832BU 芯片，支持 WiFi 6。驱动不在内核中：所有发行版（包括 Ubuntu 24.04）都需要通过 DKMS 编译 rtl8852bu。不支持 Monitor mode。
{{< /tldr >}}


对于其他系统的用户，我也帮大家找好了国内的 Gitee 镜像。不用翻墙，咱们花个 10 分钟就能把它“调教”好。

> **安全研究提示：** 社区版 rtl8852bu 驱动不支持 Monitor mode 和封包注入。做安全研究请改用内核内置 MediaTek 驱动的网卡，例如 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/)。

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
lsmod | grep 8852bu
iwconfig
```

---

### 5. 开启监听模式 {#enable-monitor-mode}

> **不支持：** RTL8832BU 的社区版 rtl8852bu 驱动不支持 Monitor mode，这里没有可执行的命令。如需 Monitor mode，请改用内核内置 MediaTek 驱动的网卡，例如 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/)。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 需要 DKMS

Ubuntu 24.04（内核 6.8）并未内置 RTL8832BU 的驱动。先换成国内镜像源，再按下方 Ubuntu 22.04 的方式编译驱动。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 将 URIs 换成阿里云的：http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

重启后执行 `sudo modprobe 8852bu` 和 `iwconfig`。如果模块成功加载并出现网卡接口，就完成了（仅支持 Managed 模式，不支持 Monitor mode）。

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
| Monitor mode／封包注入无法使用 | rtl8852bu 驱动不支持 | 做渗透测试请改用 AWUS036ACM |

## 国内常用资源汇总

| 资源名称 | 地址 | 说明 |
|------|------|------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 官方驱动包 |
| rtl8852bu 驱动镜像 | [Gitee 镜像](https://gitee.com/mirrors/rtl8852bu) | 国内克隆专用 |
| 清华大学镜像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Debian/Ubuntu 推荐 |


{{< faq >}}

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

## 参考文献

1. [Realtek 官方网站](https://www.realtek.com/)
2. [ALFA Network 官网](https://www.alfa.com.tw/)
3. [Kali Linux 官方文档](https://www.kali.org/docs/)
4. [Gitee rtl8852bu 镜像](https://gitee.com/mirrors/rtl8852bu)
