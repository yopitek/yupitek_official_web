---
title: "ALFA AWUS036ACS 中国安装指南：Kali Linux, Ubuntu, Debian 和 树莓派"
description: "手把手教你在中国境内使用国内镜像源安装 ALFA AWUS036ACS 驱动。包含 RTL8811AU DKMS 驱动安装、监听模式和数据包注入教程。支持 Kali Linux, Ubuntu 22/24, Debian 和 树莓派。无需访问 GitHub。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "驱动", "中国", "监听模式", "rtl8811au"]
categories: ["驱动指南"]
series: ["Alfa 中国安装指南"]
related_product: "/zh-cn/products/alfa/awus036acs/"
---

AWUS036ACS 是 ALFA 推出的一款紧凑型双频安全研究网卡。它采用的 RTL8811AU 芯片在 Kali Linux 上完美支持监听模式（monitor mode）和数据包注入（packet injection）。不过，由于其驱动程序不在 Linux 内核中，你需要手动编译安装。考虑到国内访问 GitHub 比较困难，本指南将全程使用 Gitee 镜像名。无需 GitHub，让我们开始吧！

## 在你开始之前

请确保你已准备好以下物品：

1. **ALFA AWUS036ACS** 网卡
2. USB 数据线（USB-A 2.0，包装盒里的那根就可以）
3. 稳定的网络连接（用于访问国内镜像源）

插上网卡，首先确认你的系统是否识别到了它：

```bash
lsusb
```

在输出结果中寻找这一行：

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

如果你看到了 `0bda:0811`，说明网卡已识别。请根据你的操作系统查看下方的相应章节。

## 选择你的操作系统

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#raspberry-pi-4b--5)

已经安装好了？直接跳转到：

- [启用监听模式](#enable-monitor-mode)
- [测试数据包注入](#test-packet-injection)
- [虚拟机 USB 透传](#virtual-machine-usb-passthrough)

---

## Kali Linux

### 第一步：切换到国内镜像源

为了下载速度更快，我们先切换到国内的镜像源。

```bash
sudo nano /etc/apt/sources.list
```

删除文件中原有的内容，粘贴以下内容：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，回车确认，然后按 **Ctrl+X** 退出。刷新软件包列表：

```bash
sudo apt update
```

> **备用镜像：** 如果中科大（USTC）速度不理想，可以尝试清华源：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安装编译所需的依赖

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### 第三步：从 Gitee 克隆驱动程序

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **注意：** 如果上面的 Gitee 链接无法访问，请在 Gitee 上搜索 `8821au` 并选择一个最近更新的分支。你也可以从 [files.alfa.com.tw](https://files.alfa.com.tw) 下载驱动压缩包。

---

### 第四步：编译并安装

```bash
sudo ./install-driver.sh
sudo reboot
```

重启后，确认驱动程序是否已加载。

```bash
lsmod | grep 88XXau
```

你应该能看到 `88XXau` 模块。接着确认无线接口是否出现。

```bash
iwconfig
```

寻找 `wlan0` 或 `wlan1`。

---

### 第五步：启用监听模式 {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

使用 `iwconfig` 确认——寻找带有 `Mode:Monitor` 的 `wlan1mon` 接口。

---

### 第六步：测试数据包注入 {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

如果成功，你会看到：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### 第一步：切换到国内镜像源

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

删除原有内容，粘贴：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

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

---

### 第二步：安装编译依赖

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### 第三步：从 Gitee 克隆并安装驱动

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### 第四步：启用监听模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### 第五步：测试数据包注入

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### 第一步：切换到国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

粘贴以下内容（适用于 Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### 第二步：安装编译依赖

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### 第三步：克隆并安装

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### 第四步：启用监听模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

使用 `iwconfig` 确认是否出现了 `Mode:Monitor` 的 `wlan1mon`。

### 第五步：测试数据包注入

```bash
sudo aireplay-ng --test wlan1mon
```

---

## 树莓派 4B / 5

### 第一步：下载并烧录 Kali ARM64

官方地址：https://www.kali.org/get-kali/#kali-arm —— 选择树莓派 4/5 64-bit 版本。

国内镜像：https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

默认账号密码：**kali / kali**。

### 第二步：切换到国内镜像源

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 第三步：安装编译依赖

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### 第四步：克隆并安装驱动

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### 第五步：启用监听模式

在带有内置 Wi-Fi 的树莓派上，AWUS036ACS 通常显示为 `wlan1`。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### 第六步：测试数据包注入

```bash
sudo aireplay-ng --test wlan1mon
```

---

## 虚拟机 USB 透传 {#virtual-machine-usb-passthrough}

### VirtualBox

1. 关闭虚拟机 → **设置 → USB** → 启用 **USB 2.0 控制器**。
2. 点击 **+** 图标 → 选择：**Realtek** (ID: 0bda:0811)。
3. 启动虚拟机。在虚拟机内运行 `lsusb` 确认看到 `0bda:0811`，然后按照上文的 Kali 步骤操作。

### VMware Fusion / Workstation

1. **虚拟机 → USB 与蓝牙** → 找到 **Realtek 8811AU** → 点击 **连接**。
2. 运行 `lsusb` 确认，然后按照上文的 Kali 步骤操作。

---

## 常见问题排除

| 问题 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| `lsusb` 看不到 0bda:0811 | 网卡未供电或线材问题 | 尝试更换 USB 接口 |
| `install-driver.sh` 运行失败 | 缺少内核头文件 | 运行 `sudo apt install linux-headers-$(uname -r)` |
| Gitee 克隆失败 | 网络不稳定 | 在 gitee.com 搜索 `8821au` 换一个仓库试试 |
| `airmon-ng start` 失败 | NetworkManager 干扰 | 先运行 `sudo airmon-ng check kill` |
| 监听模式下看不到流量 | 信道设置错误 | 设置信道：`iwconfig wlan1mon channel 6` |
| 注入测试显示 "No Answer" | 距离 AP 太远 | 靠近一点。确保使用的是 `wlan1mon` 而不是 `wlan1`。 |

> **关于 VIF 的说明：** RTL8811AU 驱动不支持虚拟接口（VIF）。这意味着这款网卡无法同时开启监听模式和正常上网模式。

## 国内资源参考

| 资源类型 | 地址 | 说明 |
|----------|-----|---------|
| Alfa 官方下载 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动包下载 |
| Alfa 官方文档 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 产品手册 |
| 8821au 驱动 (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | RTL8811AU 国内镜像驱动 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu 推荐 |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali 推荐 |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 镜像 |

## 更多 Alfa 网卡中国安装指南

- [AWUS036ACH 中国安装指南](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU, 高功率
- [AWUS036ACM 中国安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U, 支持 VIF
- AWUS036ACS ← 你在这里
- [AWUS036AX 中国安装指南](/zh-cn/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中国安装指南](/zh-cn/blog/awus036axer-china-install-guide/) — RTL8832BU, 迷你型
- [AWUS036AXM 中国安装指南](/zh-cn/blog/awus036axm-china-install-guide/) — MT7921AUN, L型接口
- [AWUS036AXML 中国安装指南](/zh-cn/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国安装指南](/zh-cn/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

有问题？欢迎在下方留言，或通过 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
