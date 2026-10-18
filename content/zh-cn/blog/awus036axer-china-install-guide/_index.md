---
title: "ALFA AWUS036AXER 中国安装全攻略：Kali Linux / Ubuntu / Debian / 树莓派"
description: "手把手教你在中国网络环境下安装 ALFA AWUS036AXER 驱动，编译工具使用国内镜像，驱动源码取自 GitHub。覆盖 Kali Linux、Ubuntu 22/24、Debian 和树莓派。"
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
    answer: "Realtek RTL8832BU 的厂商 ID 为 0bda，产品 ID 视机型为 8832 或 885a，请用 lsusb 确认你手上的设备。"
  - question: "在中国安装 AWUS036AXER 需要翻墙吗？"
    answer: "不一定。从已验证的 GitHub 仓库（morrownr/rtl8852bu-20250826）下载驱动源码；如果 GitHub 速度较慢，请使用你信任的代理或镜像。编译工具仍可用国内镜像安装。"
---




刚收到这款小巧玲珑的 AWUS036AXER，插上去发现 Linux 没反应？别担心，这很正常。AWUS036AXER 的 RTL8832BU 芯片没有 Linux 内核内置驱动，因此在所有发行版（包括 Ubuntu 24.04）上都需要通过 DKMS 编译一次社区版 rtl8852bu 驱动。驱动源码从已验证的 GitHub 仓库下载；如果 GitHub 速度较慢，请使用你信任的代理或镜像。该驱动不支持 Monitor mode。

{{< tldr >}}
AWUS036AXER 采用 RTL8832BU 芯片，支持 WiFi 6。驱动不在内核中：所有发行版（包括 Ubuntu 24.04）都需要通过 DKMS 编译 rtl8852bu。不支持 Monitor mode。
{{< /tldr >}}


国内访问 GitHub 可能比较慢，本指南的驱动源码取自已验证的 GitHub 仓库；如果速度不佳，请使用你信任的代理或镜像。咱们现在就开始吧！

> **安全研究提示：** 社区版 rtl8852bu 驱动不支持 Monitor mode 和封包注入。做安全研究请改用内核内置 MediaTek 驱动的网卡，例如 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/)。

> **信号小贴士：** AXER 是迷你型网卡，天线是内置的，主打的是便携。如果你需要远距离抓包或信号覆盖，带外置大天线的型号会更适合你。

## 动手前的准备

1. **ALFA AWUS036AXER** 网卡本人
2. 畅通的网络（用来下载镜像源）

插好网卡，咱们先看看系统有没有认出它。打开终端输入：

```bash
lsusb
```

扫一眼输出，寻找类似下面这样的一行（以下为示例输出；厂商 ID 始终是 `0bda`，产品 ID 视机型为 `8832` 或 `885a`）：

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

看到厂商 ID 为 `0bda`（产品 ID 为 `8832` 或 `885a`）就稳了。接着根据你的系统选教程。

## 你的系统是哪一个？

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

如果是老手，可以直接跳转到：
- [开启监听模式（不支持）](#enable-monitor-mode)
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

### 3. 从 GitHub 把驱动“搬”过来

GitHub 速度较慢时，请先使用你信任的代理或镜像，再克隆驱动源码：

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **注意：** 维护中的上游驱动为 [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)。如果 GitHub 速度较慢，请使用你信任的代理或镜像。你也可以从 [files.alfa.com.tw](https://files.alfa.com.tw) 下载压缩包。

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

### 6. 测试封包注入 {#test-packet-injection}

> **不支持：** 封包注入依赖 Monitor mode，而此驱动不提供 Monitor mode。请使用 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/)（内核内置 MediaTek 驱动）进行注入测试。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 需要 DKMS

Ubuntu 24.04（内核 6.8）并未内置 RTL8832BU 的驱动。先换成国内镜像源，再按下方 Ubuntu 22.04 的方式编译驱动。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 将 URIs 换成阿里云的：http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
# deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
# deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

### 1. 换成清华镜像

```bash
sudo nano /etc/apt/sources.list
# deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
# deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
# deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware

sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## 树莓派 (Raspberry Pi) 4B / 5

直接用 Kali ARM64 镜像最省事：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## 虚拟机 USB 透传避坑指南 {#virtual-machine-usb-passthrough}

### VirtualBox
1. 关掉虚拟机。
2. **设置 -> USB** -> 勾选 **USB 3.0 (xHCI) 控制器**。
3. 点那个 **+** 图标，选 **Realtek (厂商 ID：0bda，产品 ID：8832 或 885a)**。

### VMware
1. 在顶部菜单选 **虚拟机 -> USB 与蓝牙**。
2. 找到 **Realtek RTL8832BU**，点 **连接**。

---

## 常见问题“救火”站

| 遇到的麻烦 | 可能的原因 | 怎么解决 |
|------|----------|----------|
| `lsusb` 刷不出 0bda:8832 或 0bda:885a | 未检测到网卡 | 换个 USB 接口试试 |
| `install-driver.sh` 报错 | 缺少内核头文件 | 跑 `sudo apt install linux-headers-$(uname -r)` |
| 克隆 GitHub 失败或很慢 | 网络问题 | 使用你信任的代理或镜像 |
| `modprobe 8852bu` 失败 | 驱动未编译或未加载 | 重新执行 `sudo ./install-driver.sh`，用 `sudo dkms status` 检查后重启 |
| Monitor mode／封包注入无法使用 | rtl8852bu 驱动不支持 | 做渗透测试请改用 AWUS036ACM |

> **关于 VIF：** RTL8832BU 的内核外驱动不支持虚拟接口（VIF）。

## 国内常用资源汇总

| 资源名称 | 地址 | 说明 |
|------|------|------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 官方驱动包 |
| rtl8852bu 驱动（GitHub） | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | 驱动源码 |
| 清华大学镜像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像站 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像站 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像站 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |


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
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
