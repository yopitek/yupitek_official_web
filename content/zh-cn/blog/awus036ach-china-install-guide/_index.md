---
title: "ALFA AWUS036ACH 中国安装全攻略：Kali Linux / Ubuntu / Debian / 树莓派"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "驱动", "中国", "monitor-mode"]
categories: ["驱动安装指南"]
series: ["Alfa 中国安装全攻略"]
description: "手把手教你在中国网络环境下安装 ALFA AWUS036ACH 驱动，全程使用国内镜像，无需翻墙。覆盖 Kali Linux、Ubuntu 22/24、Debian 和树莓派。"
related_product: "/zh-cn/products/alfa/awus036ach/"
---

刚拿到 AWUS036ACH，插上去 Linux 没反应？正常。这块网卡用的是 RTL8812AU 芯片，驱动不是开箱即用的。整个安装过程大概 30 分钟，全程用国内镜像，不需要连 GitHub。

## 开始之前

先把这几样东西准备好：

1. **ALFA AWUS036ACH** 网卡
2. USB 数据线（盒子里附带的那根就行）
3. 有源 USB 集线器 — 树莓派必须用，否则供电不够
4. 能访问国内镜像源的网络

插好网卡，先确认系统认到了：

```bash
lsusb
```

在输出里找这一行：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

看到 `0bda:8812` 就说明网卡已经识别，直接跳到你对应的系统部分。

没看到？换个 USB 口试试，或者换根数据线，然后再跑一次 `lsusb`。

## 选择你的系统

跳到对应章节：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

已经装好驱动了？直接跳到：

- [开启监听模式（Monitor Mode）](#enable-monitor-mode)
- [测试数据包注入（Packet Injection）](#test-packet-injection)
- [虚拟机 USB 直通](#virtual-machine-usb-passthrough)

---

## Kali Linux

Kali 自带了很完整的无线工具链。装好 AWUS036ACH 驱动只需要四步，先切换到国内镜像源，后面所有下载都快很多。

### 第一步：切换国内镜像源

在终端打开软件源配置文件：

```bash
sudo nano /etc/apt/sources.list
```

把里面的内容全部删掉，粘贴这一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：按 **Ctrl+O**，回车，再按 Ctrl+X 退出。然后刷新软件包索引：

```bash
sudo apt update
```

> **备用镜像：** 如果中科大那边速度慢，换清华的：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### 第二步：安装驱动

Kali 的软件仓库里有预编译好的 DKMS 驱动包，一条命令搞定：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

装了 DKMS 以后，内核升级会自动重新编译驱动，不用手动重装。

验证驱动加载正常：

```bash
modinfo 88XXau | grep -E "filename|version"
```

能看到以 `.ko` 结尾的 `filename` 行和一个版本号（比如 `5.6.4.2`），就说明驱动就绪了。

---

### 第二步（备选方案）：手动从源码编译

只有上面 `apt install` 失败了才需要走这条路。先装编译依赖：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

从 Gitee 下载驱动源码：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **注意：** 如果这个地址打不开，去 Gitee 搜索 `rtl8812au`，选最近有更新的 fork。也可以直接从 [files.alfa.com.tw](https://files.alfa.com.tw) 下载源码包。

进入目录，编译并安装：

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

把驱动加载进内核：

```bash
sudo modprobe 88XXau
```

---

### 第三步：开启监听模式（Monitor Mode） {#enable-monitor-mode}

切换监听模式之前，先看看系统给网卡分配了哪个接口名：

```bash
iwconfig
```

找 `wlan0` 或 `wlan1` 那一行，后面的命令里用你实际看到的名字。

停掉 NetworkManager 和 wpa_supplicant，它们会跟网卡抢占，导致监听模式开不起来：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

确认切换成功：

```bash
iwconfig
```

看到 `wlan0mon`，并且 `Mode:Monitor`，网卡就可以抓包了。

---

### 第四步：测试数据包注入（Packet Injection） {#test-packet-injection}

对监听接口跑注入测试：

```bash
sudo aireplay-ng --test wlan0mon
```

成功的输出长这样：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

如果测试失败，重启机器再试一次。重启后还是失败的话，跑 `iwconfig` 确认接口状态，确保只有 `wlan0mon` 在用，没有别的进程占着这块网卡。

---

## Ubuntu 22.04 / 24.04

Ubuntu 两个版本的软件源格式不一样，下面分别处理。镜像用**阿里云**，速度稳定。

### 第一步：切换国内镜像源

按你的 Ubuntu 版本选一个路径，只做对应那个就行。

#### Ubuntu 24.04 (Noble)

打开新格式的 DEB822 软件源文件：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

把文件里的内容全部清掉，粘贴以下内容：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

#### Ubuntu 22.04 (Jammy)

打开旧格式的软件源文件：

```bash
sudo nano /etc/apt/sources.list
```

把所有内容替换成这几行：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

同样按 `Ctrl+O` 保存，`Ctrl+X` 退出。

#### 刷新软件包索引

两个版本都要跑这一步：

```bash
sudo apt update
```

---

### 第二步：安装编译依赖

驱动需要从源码编译，先把内核头文件和编译工具装上：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

`$(uname -r)` 会自动检测你当前跑的内核版本，不用手动填。

---

### 第三步：下载驱动源码（国内镜像）

从 Gitee 克隆驱动仓库，国内直接访问：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

进入克隆好的目录：

```bash
cd rtl8812au
```

> **提示：** 如果这个地址超时或报 404，去 [gitee.com](https://gitee.com) 搜 `rtl8812au`，选提交日期最近的 fork。

---

### 第四步：编译并安装

编译内核模块：

```bash
make
```

安装到系统：

```bash
sudo make install
```

注册到 DKMS，以后内核升级会自动重建：

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

把模块加载进当前内核：

```bash
sudo modprobe 88XXau
```

验证模块加载成功：

```bash
modinfo 88XXau | grep filename
```

输出里能看到 `88XXau.ko` 路径就说明驱动已经在跑了。

---

### 第五步：开启监听模式

先杀掉可能干扰的进程：

```bash
sudo airmon-ng check kill
```

然后把网卡切换到监听模式：

```bash
sudo airmon-ng start wlan0
```

> **提示：** 你的接口可能是 `wlan1` 而不是 `wlan0`。先跑 `iwconfig` 看一下所有无线接口，把上面命令里的名字换成实际的。

---

### 第六步：测试数据包注入

```bash
sudo aireplay-ng --test wlan0mon
```

成功的话会出现 `Injection is working!`。如果报接口相关的错，用 `iwconfig wlan0mon` 检查一下监听模式有没有真正开起来。

---

## Debian

Debian 默认指向海外服务器。换成清华大学镜像之后，下载速度从爬变跑。

### 第一步：切换国内镜像源

打开软件源列表：

```bash
sudo nano /etc/apt/sources.list
```

全部删掉，粘贴这三行（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出，然后刷新索引：

```bash
sudo apt update
```

### 第二步：安装编译依赖

AWUS036ACH 驱动要从源码编译，先把内核头文件和工具装上：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

这条命令会自动匹配你当前的内核版本。

### 第三步：下载驱动源码（国内镜像）

从 Gitee 克隆驱动仓库：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

进入项目目录：

```bash
cd rtl8812au
```

> **地址打不开？** 去 Gitee 搜 `rtl8812au`，选最近更新的 fork。

### 第四步：编译并安装

在 `rtl8812au` 目录里依次执行：

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

DKMS 会帮你在内核升级后自动重建驱动，不用再手动来一遍。

### 第五步：开启监听模式

先杀掉抢网卡的进程：

```bash
sudo airmon-ng check kill
```

开启监听模式：

```bash
sudo airmon-ng start wlan0
```

如果系统没有 `airmon-ng`，先装：

```bash
sudo apt install -y aircrack-ng
```

确认接口已经起来：

```bash
iwconfig
```

输出里能看到 `wlan0mon` 就对了。

### 第六步：测试数据包注入

```bash
sudo aireplay-ng --test wlan0mon
```

看到注入测试结果刷屏说明网卡工作正常，可以开干了。

---

## Raspberry Pi 4B / 5

> AWUS036ACH 功耗约 500mW。直接插树莓派 USB 口在高负载下可能导致 Pi 限速甚至重启。**一定要用有源 USB 集线器。**

---

### 第一步：下载 Kali Linux ARM64 镜像

去 Kali 官方 ARM 下载页：
https://www.kali.org/get-kali/#kali-arm

选 **Raspberry Pi 4 (64-bit)** 或 **Raspberry Pi 5 (64-bit)**，对应你的板子。不要下 32 位镜像，驱动编译需要 64 位内核。

> **国内备用：** kali.org 加载慢的话，用华为云：
> https://repo.huaweicloud.com/kali-images/
> 进最新版本目录，下载同款 ARM64 镜像。

---

### 第二步：烧录到 MicroSD 卡

插入 MicroSD 卡，写入前先确认设备路径：

```bash
lsblk
```

找到你的卡，一般显示为 `sdb` 或 `mmcblk0`。然后烧录，把 `/dev/sdX` 换成实际路径：

```bash
# 替换 /dev/sdX 为你的 SD 卡路径（用 lsblk 确认）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

`sync` 结束后再拔卡。把卡插到 Pi 上启动，默认账号密码是 **kali / kali**。

---

### 第三步：切换国内镜像源

第一次开机后，打开软件源文件：

```bash
sudo nano /etc/apt/sources.list
```

删掉全部内容，换成这一行：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

按 **Ctrl+O** 保存，回车，Ctrl+X 退出。然后更新并升级系统：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

重启是为了把内核更新也带进来，之后装驱动才不会出问题。

---

### 第四步：安装驱动（ARM64）

ARM64 上用 DKMS 包和 x86 完全一样，没有额外步骤：

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

如果提示找不到这个包，就从源码编译：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### 第五步：开启监听模式

先看看 Pi 给网卡分配了哪个接口名：

```bash
iwconfig
```

Pi 有内置 Wi-Fi，AWUS036ACH 通常会被分配成 `wlan1`，内置网卡占 `wlan0`。用 `iwconfig` 里看到的名字替换下面命令里的接口名：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

再跑一次 `iwconfig`，看到以 `mon` 结尾的接口（Pi 上通常是 `wlan1mon`）并且 `Mode:Monitor`，说明切换成功了。

---

### 第六步：测试数据包注入

```bash
sudo aireplay-ng --test wlan1mon
```

`wlan1mon` 换成你第五步里看到的实际接口名。能看到 `Injection is working!` 说明网卡工作正常。测试失败的话，重启再试一次。Pi 上最常见的原因是 USB 集线器没有独立供电，确认一下。

---

## 虚拟机 USB 直通 {#virtual-machine-usb-passthrough}

在 macOS 或 Windows 的虚拟机里跑 Kali Linux？需要把 USB 网卡直通给虚拟机。

### VirtualBox

1. 关闭虚拟机，进入 **Settings → USB**。
2. 启用 **USB 3.0 (xHCI) Controller**。
3. 点 **+** 添加 USB 过滤器。
4. 选择 **Realtek 802.11ac NIC [...]**（ID: 0bda:8812）。
5. 启动虚拟机，网卡就出现在 Kali 里了。

进虚拟机后跑 `lsusb` 确认 `0bda:8812` 出现，然后按上面的 Kali Linux 步骤继续。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. 启动虚拟机。
2. 菜单选 **Virtual Machine → USB & Bluetooth**。
3. 找到 **Realtek 802.11ac NIC**，点 **Connect**。
4. 网卡从宿主机断开，进入虚拟机。

在虚拟机里跑 `lsusb` 确认后，按 Kali Linux 步骤操作。

### 关于 VIF（虚拟接口）

RTL8812AU 芯片在 Linux 上的 VIF 支持有限制。同一块网卡不能同时可靠地跑管理模式和监听模式（或 AP 模式）。

如果你需要同时挂多个虚拟接口，比如一边开假 AP 一边监听，AWUS036ACH 不适合这个需求。可以看看 [AWUS036ACM 安装指南](/zh-cn/blog/awus036acm-china-install-guide/)，那款网卡用的是 MT7612U 芯片，内核原生支持 VIF，不需要打补丁。

---

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| `lsusb` 里没有 0bda:8812 | 网卡没通电或数据线有问题 | 换个 USB 口试试。树莓派必须用有源集线器。 |
| `make` 报头文件错误 | 内核头文件缺失或版本不对 | 跑 `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` 失败 | Secure Boot 拦截了未签名模块 | 在 BIOS 里关掉 Secure Boot，或者给模块签名 |
| 内核更新后驱动消失 | 驱动没注册到 DKMS | 在源码目录重新跑 `sudo dkms install rtl8812au/$(cat VERSION)` |
| `airmon-ng start wlan0` 失败 | NetworkManager 还在运行 | 先跑 `sudo airmon-ng check kill` |
| 监听模式开了但抓不到流量 | 频道不对或接口名用错了 | 用 `iwconfig` 检查接口。手动设频道：`iwconfig wlan0mon channel 6` |
| 注入测试显示 "No Answer" | AP 太远，或用错了接口名 | 靠近 AP。用 `wlan0mon` 而不是 `wlan0` |

## 国内镜像速查

本文用到的所有资源，不需要 GitHub：

| 资源 | 地址 | 用途 |
|------|------|------|
| Alfa 官方驱动 | [files.alfa.com.tw](https://files.alfa.com.tw) | 驱动包、固件 |
| Alfa 文档 | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 产品手册 |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推荐） |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推荐） |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM 镜像（备用） |
| RTL8812AU 驱动（Gitee） | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | 手动编译备选 |

## 更多 Alfa 网卡中国安装指南

这是 **Alfa 中国安装全攻略**系列的一部分，每篇文章对应一个型号：

- AWUS036ACH ← 你在这里
- [AWUS036ACM 安装指南](/zh-cn/blog/awus036acm-china-install-guide/) — MT7612U，最佳 VIF 支持
- [AWUS036ACS 安装指南](/zh-cn/blog/awus036acs-china-install-guide/)
- [AWUS036AX 安装指南](/zh-cn/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 安装指南](/zh-cn/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 安装指南](/zh-cn/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 安装指南](/zh-cn/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 安装指南](/zh-cn/blog/awus036eacs-china-install-guide/)

有问题？在下面留言，或者来 [yupitek.com](https://yupitek.com/zh-cn/contact/) 联系我们。
