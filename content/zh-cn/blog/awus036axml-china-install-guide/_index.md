---
title: "ALFA AWUS036AXML 中国安装全攻略：Kali Linux / Ubuntu / Debian / 树莓派"
description: "手把手教你在中国网络环境下安装 ALFA AWUS036AXML 驱动，全程使用国内镜像，无需翻墙。MT7921AUN 芯片，原生内核支持，完美监听模式与 VIF 虚拟接口。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "驱动", "中国", "monitor-mode", "wifi6e", "vif"]
categories: ["驱动安装指南"]
series: ["Alfa 中国安装全攻略"]
related_product: "/zh-cn/products/alfa/awus036axml/"
---

AWUS036AXML 是 ALFA 的 WiFi 6E 旗舰——三频 USB-C 网卡，支持 2.4 GHz、5 GHz 和干扰极少的 6 GHz 频段。它用的是 MT7921AUN 芯片，内核 5.18 以上就已经原生支持了（也就是不需要手动编译驱动）。在 Ubuntu 24.04 或 Kali 2025 上，只要装好国内镜像的固件包，插上就能飞。本攻略教你全程不连 GitHub，搞定固件、监听模式和 VIF。

## 开始之前

先准备好这些：

1. **ALFA AWUS036AXML** 网卡和 USB-C 数据线
2. **有源 USB 集线器** — 树莓派用户必带，否则带不动
3. 能访问国内镜像的网络

插好网卡，先确认系统认到了：

```bash
lsusb
```

找这一行：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

看到 `0e8d:7961` 就说明网卡识别了，直接跳到你对应的系统部分。

没看到？换个 USB-C 口或线试试，然后再跑一次 `lsusb`。

## 选择你的系统

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

已经装好了？直接看：

- [开启监听模式（Monitor Mode）](#enable-monitor-mode)
- [测试数据包注入](#test-packet-injection)
- [VIF 虚拟接口高级玩法](#virtual-interface-vif)
- [虚拟机 USB 直通](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7921AUN 的驱动就在内核里。你只需要装好 MediaTek 的固件包，国内镜像下载极快。

### 第一步：切换国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

把内容全删了，粘贴：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，回车，Ctrl+X 退出。刷新软件源：

```bash
sudo apt update
```

> **备用镜像：** 中科大慢的话换清华：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安装固件

MT7921AUN 需要 `firmware-misc-nonfree` 和 `linux-firmware` 里的固件文件。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### 第三步：验证驱动

重启后插上网卡：

```bash
lsmod | grep mt7921
```

看到 `mt7921u` 就说明驱动跑起来了。再确认接口：

```bash
iwconfig
```

看到 `wlan0` 或 `wlan1` 就对了。

---

### 第四步：开启监听模式 {#enable-monitor-mode}

先看一眼接口名（比如是 `wlan1`）：

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

确认切换成功：

```bash
iwconfig
```

看到 `Mode:Monitor` 就大功告成。

---

### 第五步：测试数据包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

看到 `Injection is working!` 说明网卡非常健康。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — 内核 6.8，插上就用

24.04 的内核非常新，原生支持。

### 第一步：切换国内镜像源

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

删掉全部内容，粘贴阿里云源：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
```

### 第二步：安装固件

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

### Ubuntu 22.04 (Jammy) — 需要升级 HWE 内核

22.04 默认内核是 5.15，驱动需要 5.18+。我们要装 HWE 内核。

### 第一步：切换国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

替换为：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

### 第二步：安装 HWE 内核

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

重启后检查 `uname -r` 应该是 5.19 或更高。

### 第三步：安装固件

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### 第一步：切换国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

粘贴清华大学源（Debian 12）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### 第二步：安装固件

Debian 12 内核是 6.1，完美兼容。

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

---

## Raspberry Pi 4B / 5

> AWUS036AXML 功耗大，高负载能到 2.7W。**树莓派务必用有源集线器。**

### 第一步：下载镜像

去 Kali 官网下 ARM64 镜像。

> **国内镜像：** https://repo.huaweicloud.com/kali-images/ 进最新版本目录下载。

### 第二步：切换镜像源并装固件

```bash
sudo nano /etc/apt/sources.list
```

换成：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

更新系统：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

## 虚拟机 USB 直通 {#virtual-machine-usb-passthrough}

### VirtualBox

1. **设置 → USB** → 启用 **USB 3.0 (xHCI)**。
2. 添加过滤器：**MediaTek Inc.** (ID: 0e8d:7961)。
3. 启动，跑 `lsusb` 确认。

### VMware

1. **虚拟机 → USB 与蓝牙** → 找到 **MediaTek MT7921AUN** → **连接**。

---

## VIF 虚拟接口高级玩法 {#virtual-interface-vif}

MT7921AUN 原生支持 VIF，你可以一边连着 Wi-Fi 上网，一边开监听模式，不需要打任何补丁。

### 同时开启监听和普通模式

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

现在你会看到 `wlan0`（连网）和 `mon0`（监听）都在跑。

### 钓鱼 AP + 监听

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| `lsusb` 没反应 | 线不好或供电不足 | 换线。树莓派用有源集线器。 |
| `lsmod` 看不到 mt7921u | 固件没装或内核太老 | 装 `linux-firmware`。Ubuntu 22.04 要升 HWE 内核。 |
| 有接口但搜不到信号 | 固件包没装全 | `sudo apt install firmware-misc-nonfree` |
| 注入测试报 "No Answer" | 太远了 | 靠近点再试。 |

## 国内镜像速查

| 资源 | 地址 | 用途 |
|------|------|------|
| Alfa 官方驱动 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动、固件 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 安装指南](/zh-cn/blog/awus036ach-china-install-guide/)
- [AWUS036ACM 安装指南](/zh-cn/blog/awus036acm-china-install-guide/)
- [AWUS036ACS 安装指南](/zh-cn/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安装指南](/zh-cn/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安装指南](/zh-cn/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安装指南](/zh-cn/blog/awus036axm-china-install-guide/)
- AWUS036AXML ← 你在这里
- [AWUS036EACS 安装指南](/zh-cn/blog/awus036eacs-china-install-guide/)

有问题？在下面留言，或者来 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
