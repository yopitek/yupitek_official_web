---
title: "ALFA AWUS036ACM 中国安装全攻略：Kali Linux / Ubuntu / Debian / 树莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "驱动", "中国", "monitor-mode", "vif"]
categories: ["驱动安装指南"]
series: ["Alfa 中国安装全攻略"]
description: "手把手教你在中国网络环境下安装 ALFA AWUS036ACM 驱动，全程使用国内镜像，无需翻墙。MT7612U 内核原生驱动，完整 VIF 支持。覆盖 Kali Linux、Ubuntu 22/24、Debian 和树莓派。"
related_product: "/zh-cn/products/alfa/awus036acm/"
---

AWUS036ACM 是 Alfa 无线网卡里最好装的一款。它用的是 MT7612U 芯片，驱动 `mt76x2u` 从 Linux 4.19 起就已经内置进内核了。大多数情况下，插上就能用，最多跑两三条命令。这篇文章覆盖完整流程：驱动验证、监听模式、封包注入，以及 VIF（虚拟接口）——全部使用国内镜像，不需要访问 GitHub。

## 准备工作

请确认以下几样东西都备齐了：

1. **ALFA AWUS036ACM** 无线网卡
2. USB 数据线（盒子里附带的就行）
3. 带独立供电的 USB Hub——树莓派用户必备
4. 能访问国内镜像的网络连接

把网卡插上，确认系统能识别到：

```bash
lsusb
```

在输出里找这一行：

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

看到 `0e8d:7612` 就说明识别成功了，直接跳到对应系统的章节。

如果没看到，换个 USB 口或者换根线，再跑一次 `lsusb`。

## 选择你的系统

直接跳到对应的章节：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [树莓派 4B / 5](#树莓派-4b--5)

已经装好驱动了？直接跳到：

- [开启监听模式](#开启监听模式)
- [测试封包注入](#测试封包注入)
- [虚拟接口（VIF）](#虚拟接口vif)
- [虚拟机 USB 直通](#虚拟机-usb-直通)

---

## Kali Linux

MT7612U 的驱动已经内置在 Kali 内核里了。绝大多数情况下，网卡插上去就可以用。下面的步骤帮你确认驱动已经加载，然后直接进入监听模式。

### 第一步：切换到国内镜像

打开软件源文件：

```bash
sudo nano /etc/apt/sources.list
```

把里面的内容全删掉，粘贴下面这一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：按 **Ctrl+O**，回车，再按 Ctrl+X 退出。刷新软件包索引：

```bash
sudo apt update
```

> **备用镜像：** 如果中科大镜像速度慢，换清华大学镜像：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：验证驱动

检查插上网卡后内核有没有自动加载模块：

```bash
lsmod | grep mt76
```

输出里应该有 `mt76x2u`。如果没有，手动加载：

```bash
sudo modprobe mt76x2u
```

再跑一次 `lsmod | grep mt76` 确认。然后验证网卡接口是否出现：

```bash
iwconfig
```

如果看到 `wlan0` 或 `wlan1` 的接口，驱动就没问题了。

---

### 第二步（备选）：安装额外内核模块

如果 `modprobe mt76x2u` 报"找不到模块"，说明你的内核没有包含 MT76 模块，从国内镜像安装：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

装完再加载一次：

```bash
sudo modprobe mt76x2u
```

如果连这个包都找不到，就从源码编译：

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **注意：** 如果那个 Gitee 地址打不开，在 Gitee 搜索 `mt76` 找最近更新的 fork。也可以直接从 [files.alfa.com.tw](https://files.alfa.com.tw) 下载驱动包。

---

### 第三步：开启监听模式 {#开启监听模式}

先看看系统给网卡分配了什么接口名：

```bash
iwconfig
```

找到 `wlan0` 或 `wlan1`，记下来，下面的命令用那个名字。

停掉 NetworkManager 和 wpa_supplicant，不然它们会抢占接口：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

确认切换成功：

```bash
iwconfig
```

看到 `wlan0mon` 且显示 `Mode:Monitor`，就说明监听模式开启成功了。

---

### 第四步：测试封包注入 {#测试封包注入}

```bash
sudo aireplay-ng --test wlan0mon
```

成功的输出长这样：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

如果失败了，重启机器再试一次。还是不行的话，用 `iwconfig` 确认没有其他进程占用这个接口。

---

## Ubuntu 22.04 / 24.04

MT7612U 驱动同样内置在 Ubuntu 内核里，不过有时候需要安装 `linux-modules-extra` 才能加载上。

### 第一步：切换到国内镜像

#### Ubuntu 24.04 (Noble)

打开 DEB822 格式的软件源文件：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

全部删掉，粘贴以下内容：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

`Ctrl+O` 保存，`Ctrl+X` 退出。

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

替换全部内容为：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

保存退出，然后刷新：

```bash
sudo apt update
```

---

### 第二步：加载驱动

直接尝试加载模块：

```bash
sudo modprobe mt76x2u
```

如果提示找不到模块，安装额外模块包：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

确认接口出现：

```bash
iwconfig
```

---

### 第三步：安装无线工具

```bash
sudo apt install -y aircrack-ng
```

---

### 第四步：开启监听模式

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **注意：** 如果有其他无线网卡，接口名可能是 `wlan1`，先用 `iwconfig` 确认。

---

### 第五步：测试封包注入

```bash
sudo aireplay-ng --test wlan0mon
```

出现 `Injection is working!` 就成功了。

---

## Debian

MT7612U 的驱动在 Debian 内核里，但有时候需要安装 `firmware-misc-nonfree` 固件包才能完整初始化。

### 第一步：切换到国内镜像

```bash
sudo nano /etc/apt/sources.list
```

全部删掉，粘贴以下内容（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

保存退出，刷新：

```bash
sudo apt update
```

### 第二步：安装非自由固件

MT7612U 需要 `firmware-misc-nonfree` 里的固件文件，少了这个网卡能识别但无法正常工作：

```bash
sudo apt install -y firmware-misc-nonfree
```

### 第三步：加载驱动

```bash
sudo modprobe mt76x2u
```

如果模块找不到：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

用 `iwconfig` 确认接口出现。

### 第四步：开启监听模式

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

用 `iwconfig` 确认出现 `wlan0mon` 且模式为 `Monitor`。

### 第五步：测试封包注入

```bash
sudo aireplay-ng --test wlan0mon
```

看到 `Injection is working!` 就搞定了。

---

## 树莓派 4B / 5

> AWUS036ACM 满载约消耗 400mW，建议使用带独立供电的 USB Hub，避免树莓派限流。

---

### 第一步：下载 Kali Linux ARM64 镜像

访问官方 Kali ARM 下载页面：
https://www.kali.org/get-kali/#kali-arm

选 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)**，不要选 32 位版本。

> **国内镜像：** kali.org 慢的话用华为云：
> https://repo.huaweicloud.com/kali-images/
> 找最新版本文件夹，下载同款 ARM64 镜像。

---

### 第二步：写入 MicroSD

先查 SD 卡的设备路径：

```bash
lsblk
```

找到你的卡（比如 `sdb` 或 `mmcblk0`），然后写入：

```bash
# 把 /dev/sdX 换成你实际的 SD 卡路径（用 lsblk 确认）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

等 `sync` 跑完再拔卡，用 SD 卡启动树莓派。默认账号：**kali / kali**。

---

### 第三步：切换到国内镜像

```bash
sudo nano /etc/apt/sources.list
```

全部替换为：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存，更新并升级：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### 第四步：验证驱动

重启后插上网卡，检查模块：

```bash
lsmod | grep mt76
```

看到 `mt76x2u` 就没问题。如果没有：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### 第五步：开启监听模式

树莓派有内置 Wi-Fi，AWUS036ACM 通常会被分配到 `wlan1`：

```bash
iwconfig
```

确认接口名，然后：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

用 `iwconfig` 确认出现 `wlan1mon` 且模式为 `Monitor`。

---

### 第六步：测试封包注入

```bash
sudo aireplay-ng --test wlan1mon
```

看到 `Injection is working!` 就完成了。如果失败，检查是否使用了带供电的 USB Hub。

---

## 虚拟机 USB 直通

### VirtualBox

1. 关闭虚拟机，进入 **设置 → USB**。
2. 启用 **USB 3.0 (xHCI) 控制器**。
3. 点 **+** 添加 USB 过滤器。
4. 选择：**MediaTek Inc. MT7612U**（ID: 0e8d:7612）。
5. 启动虚拟机，网卡就会出现在 Kali 里。

在虚拟机里用 `lsusb` 确认 `0e8d:7612`，然后按上面的 Kali 步骤操作。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. 启动虚拟机。
2. 菜单：**虚拟机 → USB 和蓝牙**。
3. 找到 **MediaTek MT7612U**，点 **连接**。
4. 在虚拟机里 `lsusb` 确认，然后按 Kali 步骤操作。

---

## 虚拟接口（VIF）

这是 AWUS036ACM 比 AWUS036ACH 强的地方。MT7612U 芯片完整支持内核原生 VIF，可以在同一张网卡上同时运行监听接口和托管模式（或 AP 模式）——不需要打补丁，开箱即用。

### 创建第二个虚拟接口

在网卡以 `wlan0` 连接网络（托管模式）的同时，再加一个监听接口：

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

验证两个接口都在运行：

```bash
iwconfig
```

你应该能同时看到 `wlan0`（已连接，托管模式）和 `mon0`（监听模式）。一张网卡，两个功能同时跑。

### 用法一：连着网同时抓包

`wlan0` 保持连接，`mon0` 在后台扫描流量：

```bash
sudo airodump-ng mon0
```

适合需要同时在线又要分析周边流量的场景。

### 用法二：伪 AP + 监听

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

`iwconfig` 确认 `wlan0`、`ap0`、`mon0` 三个接口都在。

> **注意：** 完整的 AP 运行还需要配置 `hostapd`，那是另一个话题了。上面的命令只是验证网卡能创建这些接口。

---

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| `lsusb` 看不到 0e8d:7612 | 网卡没通电或数据线有问题 | 换 USB 口，树莓派用带供电的 Hub |
| `modprobe mt76x2u` 说找不到模块 | 内核缺少额外模块 | 执行 `sudo apt install linux-modules-extra-$(uname -r)` |
| 接口出现但无法连接 | 固件文件缺失 | Debian 执行 `sudo apt install firmware-misc-nonfree` |
| `airmon-ng start wlan0` 失败 | NetworkManager 还在运行 | 先执行 `sudo airmon-ng check kill` |
| 监听模式开启但抓不到流量 | 信道或接口名错误 | 设置信道：`iwconfig wlan0mon channel 6` |
| 注入测试返回"No Answer" | AP 太远或接口名错误 | 靠近 AP，确认用的是 `wlan0mon` |
| VIF 接口创建失败 | 驱动没完整加载 | `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## 国内镜像参考

本文用到的所有资源，全部不需要 GitHub：

| 资源 | 地址 | 用途 |
|------|------|------|
| Alfa 官方驱动 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动包、固件 |
| Alfa 文档 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 产品手册 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推荐） |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推荐） |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 镜像（备用） |
| MT76 驱动（Gitee） | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | 手动编译备选 |

## 系列文章

本文是 **Alfa 网卡中国安装全攻略** 系列的一部分，每篇文章对应一款型号：

- [AWUS036ACH 中国安装全攻略](/zh-cn/blog/awus036ach-china-install-guide/) — RTL8812AU，大功率
- AWUS036ACM ← 当前文章
- [AWUS036ACS 中国安装全攻略](/zh-cn/blog/awus036acs-china-install-guide/)
- [AWUS036AX 中国安装全攻略](/zh-cn/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 中国安装全攻略](/zh-cn/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 中国安装全攻略](/zh-cn/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 中国安装全攻略](/zh-cn/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 中国安装全攻略](/zh-cn/blog/awus036eacs-china-install-guide/)

有问题？在下方留言，或通过 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
