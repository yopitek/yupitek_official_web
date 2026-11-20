---
title: "ALFA AWUS036AX 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
description: "手把手教你在中国境内使用国内镜像源安装 ALFA AWUS036AX 驱动。包含 RTL8832BU 驱动安装、WiFi 6 AX1800 性能说明。支持 Kali Linux, Ubuntu 22/24 (DKMS), Debian 和 树莓派。"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
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
    answer: "看内核版本。Linux 内核 6.17 以上（例如 Ubuntu 24.04 HWE / kernel 6.17）已内置 rtw89_8852bu 驱动，插上即认、免 DKMS；只有内核低于 6.17 时，才需要通过 DKMS 编译一次社区版 rtl8852bu 驱动（morrownr/rtl8852bu-20250826）。先用 uname -r 确认内核版本。"
  - question: "AWUS036AX 适合做无线安全研究吗？"
    answer: "适合。在内核 6.17+ 的内置 rtw89_8852bu 驱动下，实测 Monitor mode 与封包注入都可用（我们在 Ubuntu 24.04 / kernel 6.17 实测注入 2.4GHz 96%，并端到端捕获 WPA .22000）。注意：若在旧内核改用社区版 DKMS 驱动，Monitor 支持可能受限。仅限自有或已授权的网络。"
  - question: "在中国安装 AWUS036AX 需要翻墙吗？"
    answer: "不一定。从已验证的 GitHub 仓库（morrownr/rtl8852bu-20250826）下载驱动源码；如果 GitHub 速度较慢，请使用你信任的代理或镜像。编译工具仍可用国内镜像安装。"
  - question: "AWUS036AX 的 USB ID 是多少？"
    answer: "Realtek RTL8832BU 的厂商 ID 为 0bda，产品 ID 视机型为 8832 或 885a，请用 lsusb 确认你手上的设备。"
---




想要在 Linux 上体验 WiFi 6 的极速？AWUS036AX 是个不错的选择。它的 RTL8832BU 芯片在 **Linux 内核 6.17 以上**（例如 Ubuntu 24.04 HWE / kernel 6.17）已由内置的 rtw89_8852bu 驱动支持，插上即认、免编译；只有在**旧内核**（低于 6.17）上，才需要通过 DKMS 编译一次社区版 rtl8852bu 驱动。本指南涵盖这两种情形——驱动源码从已验证的 GitHub 仓库下载；如果 GitHub 速度较慢，请使用你信任的代理或镜像。

{{< tldr >}}
AWUS036AX 采用 RTL8832BU 芯片，支持 WiFi 6。内核 6.17+（含 Ubuntu 24.04 / kernel 6.17）已内置 rtw89_8852bu 驱动，免 DKMS、Monitor 与注入实测可用；旧内核才需 DKMS 编译社区版 rtl8852bu。
{{< /tldr >}}


国内访问 GitHub 可能比较慢，本指南的驱动源码取自已验证的 GitHub 仓库；如果速度不佳，请使用你信任的代理或镜像。咱们现在就开始一步步把它跑起来！

> **安全研究提示：** 在**内核 6.17+ 的内置 rtw89_8852bu 驱动**下，AWUS036AX 的 Monitor mode 与封包注入实测可用（Ubuntu 24.04 / kernel 6.17 实测注入 2.4GHz 96%、端到端 WPA .22000）。仅在旧内核改用社区版 DKMS 驱动时，Monitor 支持才可能受限。请先用 `uname -r` 确认内核版本。仅限自有或已授权的网络。

## 动手前的准备

1. **ALFA AWUS036AX** 网卡本人
2. USB-A 数据线
3. 畅通的网络（用来下载镜像源）

插上网卡，咱们先看看系统有没有认出它。打开终端输入：

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
- [开启监听模式](#enable-monitor-mode)
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

重启回来，检查下网卡有没有乖乖上岗：

```bash
lsmod | grep 8852bu
iwconfig
```

---

### 5. 开启监听模式 {#enable-monitor-mode}

> **内核 6.17+ 可用：** 在内置的 rtw89_8852bu 驱动下，Monitor mode 实测可用：
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> 若你在**旧内核**上改用社区版 DKMS 驱动，该版本 Monitor 支持可能受限——此时可改用内核内置 MediaTek 驱动的网卡（例如 [AWUS036ACM](/zh-cn/blog/awus036acm-china-install-guide/)）。

### 6. 测试封包注入 {#test-packet-injection}

> **内核 6.17+ 可用：** 进入 Monitor mode 后，用 aireplay-ng 测试注入（实测 2.4GHz 96%）：
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> 仅限自有或已授权的网络。旧内核的社区版 DKMS 驱动若不提供 Monitor，注入亦不可用。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 需要 DKMS

Ubuntu 24.04 的 GA 内核 6.8 与 HWE 内核 6.14 都未内置该芯片的驱动，需内核 6.17 以上（例如 24.04.4 的 HWE）。先换成国内镜像源，再按下方 Ubuntu 22.04 的方式编译驱动。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
# 将 URIs 改为 http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

重启后执行 `sudo modprobe 8852bu` 和 `iwconfig`。如果模块成功加载并出现网卡接口，就完成了（此为旧内核的社区版 DKMS 驱动路径，Monitor 支持可能受限；内核 6.17+ 请用内置 rtw89_8852bu，Monitor 与注入实测可用）。

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

## 树莓派 (Raspberry Pi) 4B / 5 {#raspberry-pi-4b--5}

建议直接用 Kali ARM64，操作和上面的 Kali 章节差不多：

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
3. 添加过滤：**Realtek (厂商 ID：0bda，产品 ID：8832 或 885a)**。

### VMware
1. 在顶部菜单选 **虚拟机 -> USB 与蓝牙**。
2. 找到 **Realtek RTL8832BU**，点 **连接**。

---

## 常见问题“救火”站

| 遇到的麻烦 | 可能的原因 | 怎么解决 |
|---------|-------------|-----|
| `lsusb` 刷不出 0bda:8832 或 0bda:885a | 未检测到网卡 | 换个 USB 接口试试 |
| `install-driver.sh` 报错 | 缺少内核头文件 | 跑 `sudo apt install linux-headers-$(uname -r)` |
| 克隆 GitHub 失败或很慢 | 网络问题 | 使用你信任的代理或镜像 |
| `modprobe 8852bu` 失败 | 驱动未编译或未加载 | 重新执行 `sudo ./install-driver.sh`，用 `sudo dkms status` 检查后重启 |
| Monitor mode／封包注入无法使用 | 内核低于 6.17 且使用社区版 rtl8852bu DKMS 驱动（Monitor 支持可能受限） | 先用 `uname -r` 确认；请使用内核 6.17+（内置 rtw89_8852bu），旧内核可改用 AWUS036ACM |

> **关于 VIF：** RTL8832BU 的内核外驱动不支持虚拟接口（VIF）。

## 国内常用资源汇总

| 资源名称 | 地址 | 说明 |
|----------|-----|---------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动离线包 |
| rtl8852bu 驱动（GitHub） | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | 驱动源码 |
| 清华大学镜像站 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像站 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像站 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像站 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |


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
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
